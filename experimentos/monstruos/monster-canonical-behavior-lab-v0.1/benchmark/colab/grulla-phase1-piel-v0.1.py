# Grulla Blanca — Fase I-B · Piel de Cobre aislada · Monte Carlo reproducible
# SOLO Fase I. No Paso, no Filamento, no Fase II/III.
# Respeta el checkpoint: técnica raíz con 2 PT + Piel con 0..2 PT.
# 16 configuraciones legales de Piel por cada una de las 27 formas raíz.
#
# Modos:
#   selección:    python grulla-phase1-piel-v0.1.py --mode grid --runs 5000
#   confirmación: python grulla-phase1-piel-v0.1.py --mode confirm --runs 20000 --finalists 1-2,1-3,2-2
#
# La Guardia de ver74 se modela como burbuja/reserva:
#   capacidad = guardia * duración
#   absorción por golpe = min(daño, guardia, capacidad restante)
#   no decae por rondas ni por impactos fallidos.

import argparse
import math
import numpy as np
import pandas as pd

DEFAULT_GRID_RUNS = 5_000
DEFAULT_CONFIRM_RUNS = 20_000

PLAYER_MAX_HP = 28
PLAYER_MAX_QI = 110
GEAR_ATTACK = 2
GEAR_DEFENSE = 7

BOSS_HP = 150
BOSS_ATTACK = 4
BOSS_BASIC = (1, 6, 2)      # 1d6+2
BOSS_CAMPANADA = (2, 6, 2)  # 2d6+2
PATA_DEF_BONUS = 3

READER_BASELINE = {13: 0.609, 14: 0.547}

ROOTS = {
    "fuego": {
        "attack":1,"defense":0,"baseCost":7,"baseDamage":(2,6,2),
        "r1":[{"burn":(1,3,2)},{"damage":(1,4,0)},{"attack":3}],
        "r2":[{"cost":-1},{"attack":4},{"critMin":19}],
    },
    "metal": {
        "attack":2,"defense":0,"baseCost":6,"baseDamage":(1,10,3),
        "r1":[{"attack":3},{"damage":(1,4,0)},{"critMin":19}],
        "r2":[{"cost":-1,"critMin":19},{"attack":4},{"debil":(-2,1)}],
    },
    "agua": {
        "attack":0,"defense":2,"baseCost":6,"baseDamage":(2,6,0),
        "r1":[{"debil":(-1,1)},{"damage":(1,4,0)},{"attack":3}],
        "r2":[{"cost":-1},{"attack":4},{"critMin":19}],
    },
}

# Piel de Cobre ver74.
PIEL_BASE = {"cost":5, "guard":3, "duration":2}
PIEL_R1 = [
    {"guard":6},         # 1 Cobre endurecido
    {"durationExtra":1}, # 2 Cobre flexible
    {"cost":-1},         # 3 Cobre sobrio
]
PIEL_R2 = [
    {"cost":-1},         # 1 Aliento económico
    {"guard":7},         # 2 Cobre grueso
    {"durationExtra":1}, # 3 Placas continuas
]

PIEL_NAMES_R1 = {
    0: "—",
    1: "Cobre endurecido",
    2: "Cobre flexible",
    3: "Cobre sobrio",
}
PIEL_NAMES_R2 = {
    0: "—",
    1: "Aliento económico",
    2: "Cobre grueso",
    3: "Placas continuas",
}

# 0 = sin PT en ese tramo.
# 1 base + 3 sólo T1 + 3 sólo T2 + 9 T1+T2 = 16 configuraciones.
PIEL_CONFIGS = [(0,0)]
PIEL_CONFIGS += [(a,0) for a in range(1,4)]
PIEL_CONFIGS += [(0,b) for b in range(1,4)]
PIEL_CONFIGS += [(a,b) for a in range(1,4) for b in range(1,4)]

def root_conf(root,o1,o2):
    q=ROOTS[root]
    cost=q["baseCost"]
    attack_bonus=0
    crit_min=20
    dice=[q["baseDamage"][:2]]
    flat=q["baseDamage"][2]+1  # afinidad principal
    burn=None
    debil=None

    for m in (q["r1"][o1-1],q["r2"][o2-1]):
        cost += m.get("cost",0)
        attack_bonus += m.get("attack",0)
        crit_min=min(crit_min,m.get("critMin",20))
        if "damage" in m:
            dice.append(m["damage"][:2])
            flat += m["damage"][2]
        if "burn" in m: burn=m["burn"]
        if "debil" in m: debil=m["debil"]

    # Igual que Fase I-A/Paso: afinidad principal aplica -1 y luego piso 70%.
    cost=max(math.ceil(q["baseCost"]*.7),max(1,cost-1))
    return dict(
        cost=cost,attack_bonus=attack_bonus,crit_min=crit_min,
        dice=dice,flat=flat,burn=burn,debil=debil
    )

def piel_conf(p1,p2):
    cost=PIEL_BASE["cost"]
    guard=PIEL_BASE["guard"]
    duration=PIEL_BASE["duration"]

    for opt,table in ((p1,PIEL_R1),(p2,PIEL_R2)):
        if not opt:
            continue
        m=table[opt-1]
        cost += m.get("cost",0)
        if "guard" in m:
            guard=m["guard"]
        duration += m.get("durationExtra",0)

    # Piel es Mortal/Tierra y este grid sólo usa raíces Fuego/Metal/Agua:
    # no se presupone afinidad Tierra adicional.
    cost=max(math.ceil(PIEL_BASE["cost"]*.7),max(1,cost))
    capacity=guard*duration
    return dict(cost=cost,guard=guard,duration=duration,capacity=capacity)

def config_label(p1,p2):
    return f"T1-{p1 or 0} + T2-{p2 or 0}"

def config_name(p1,p2):
    a=PIEL_NAMES_R1[p1]
    b=PIEL_NAMES_R2[p2]
    if p1 and p2:
        return f"{a} + {b}"
    return a if p1 else b if p2 else "Piel base"

def parse_finalists(raw):
    if not raw:
        return []
    out=[]
    for token in raw.split(","):
        token=token.strip()
        if not token:
            continue
        a,b=token.split("-")
        cfg=(int(a),int(b))
        if cfg not in PIEL_CONFIGS:
            raise ValueError(f"Configuración finalista ilegal: {token}")
        out.append(cfg)
    return out

def roll_terms(rng,terms,flat,size):
    out=np.full(size,flat,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def apply_guard_damage(hp, sel, dmg, defender1, defender2, piel_guard, piel_capacity):
    """Aplica exactamente una categoría guardia: burbuja Piel o DEFENDER."""
    # Piel tiene prioridad si existe; en juego real ambas comparten categoría y no coexisten.
    cap=piel_capacity[sel]
    has_piel=(dmg>0)&(cap>0)
    if has_piel.any():
        absorb=np.zeros(sel.size,dtype=np.int16)
        absorb[has_piel]=np.minimum(
            dmg[has_piel],
            np.minimum(piel_guard[sel[has_piel]],cap[has_piel])
        )
        hp[sel]-=dmg-absorb
        s=sel[has_piel]
        piel_capacity[s]-=absorb[has_piel]
        piel_guard[s]=np.where(piel_capacity[s]>0,piel_guard[s],0)

    no_piel=~has_piel
    if no_piel.any():
        local=np.flatnonzero(no_piel)
        s=sel[local]
        d=dmg[local]
        g1=defender1[s]
        g2=defender2[s]
        use1=(d>0)&(g1>0)
        use2=(d>0)&(~use1)&(g2>0)
        red=np.zeros(local.size,dtype=np.int16)
        red[use1]=np.floor(d[use1]*g1[use1]/100).astype(np.int16)
        red[use2]=np.floor(d[use2]*g2[use2]/100).astype(np.int16)
        hp[s]-=d-red
        if use1.any():
            ss=s[use1]
            defender1[ss]=defender2[ss]
            defender2[ss]=0
        if use2.any():
            defender2[s[use2]]=0

def simulate(root,o1,o2,p1,p2,boss_def,runs,seed=1):
    rng=np.random.default_rng(seed)
    q=ROOTS[root]
    tc=root_conf(root,o1,o2)
    pc=piel_conf(p1,p2)

    p_attack=1+q["attack"]+3+GEAR_ATTACK
    p_def=10+q["defense"]+GEAR_DEFENSE

    hp=np.full(runs,PLAYER_MAX_HP,dtype=np.int16)
    qi=np.full(runs,PLAYER_MAX_QI,dtype=np.int16)
    bhp=np.full(runs,BOSS_HP,dtype=np.int16)
    alive=np.ones(runs,dtype=bool)
    win=np.zeros(runs,dtype=bool)
    potion=np.ones(runs,dtype=bool)

    # DEFENDER: porcentaje para los próximos dos impactos reales.
    defender1=np.zeros(runs,dtype=np.int16)
    defender2=np.zeros(runs,dtype=np.int16)

    # Piel ver74: tope por golpe + reserva. No tiene tick temporal.
    piel_guard=np.zeros(runs,dtype=np.int16)
    piel_capacity=np.zeros(runs,dtype=np.int16)

    burn_turns=np.zeros(runs,dtype=np.int8)
    debil=np.zeros(runs,dtype=np.int8)
    debil_turns=np.zeros(runs,dtype=np.int8)
    def_next=np.zeros(runs,dtype=np.int8)
    rounds=np.zeros(runs,dtype=np.int16)
    piel_casts=np.zeros(runs,dtype=np.int16)
    absorbed=np.zeros(runs,dtype=np.int16)

    for rnd in range(1,81):
        active=alive & ~win
        if not active.any():
            break
        idx=np.flatnonzero(active)
        rounds[idx]+=1
        cycle=(rnd-1)%4  # Golpe, Golpe, Campanada, Pata

        # PIEL_READER:
        # - Golpes: técnica raíz.
        # - Campanada:
        #     * si no queda burbuja -> Piel;
        #     * si la burbuja sigue activa -> técnica raíz;
        #     * si no puede pagar Piel -> DEFENDER.
        # - Pata: ATACAR básico.
        # - poción crítica conserva prioridad del READER universal.
        act=np.zeros(idx.size,dtype=np.int8) # 0 basic,1 root,2 defend,3 potion,4 piel
        if cycle in (0,1):
            act[:]=1
        elif cycle==2:
            bubble_alive=piel_capacity[idx]>0
            act[:]=np.where(bubble_alive,1,4)
        else:
            act[:]=0

        act[(hp[idx]<=9)&potion[idx]]=3
        act[(act==1)&(qi[idx]<tc["cost"])]=0
        act[(act==4)&(qi[idx]<pc["cost"])]=2

        # poción
        sel=idx[act==3]
        if sel.size:
            heal=rng.integers(1,7,size=(3,sel.size),dtype=np.int16).sum(axis=0)+6
            hp[sel]=np.minimum(PLAYER_MAX_HP,hp[sel]+heal)
            potion[sel]=False

        # DEFENDER reemplaza cualquier guardia de la categoría, como ver74.
        sel=idx[act==2]
        if sel.size:
            piel_guard[sel]=0
            piel_capacity[sel]=0
            defender1[sel]=rng.integers(35,51,size=sel.size,dtype=np.int16)
            defender2[sel]=rng.integers(25,41,size=sel.size,dtype=np.int16)
            qi[sel]=np.minimum(PLAYER_MAX_QI,qi[sel]+3)

        # Piel reemplaza cualquier DEFENDER, como ver74.
        sel=idx[act==4]
        if sel.size:
            qi[sel]-=pc["cost"]
            defender1[sel]=0
            defender2[sel]=0
            piel_guard[sel]=pc["guard"]
            piel_capacity[sel]=pc["capacity"]
            piel_casts[sel]+=1

        # ATACAR básico
        sel=idx[act==0]
        if sel.size:
            d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
            hit=(d20==20)|((d20!=1)&(d20+p_attack>=boss_def+def_next[sel]))
            crit=hit&(d20==20)
            dmg=rng.integers(1,9,size=sel.size,dtype=np.int16)
            dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
            bhp[sel]-=np.where(hit,dmg,0)
            def_next[sel]=0

        # técnica raíz
        sel=idx[act==1]
        if sel.size:
            qi[sel]-=tc["cost"]
            d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
            hit=(d20==20)|((d20!=1)&(
                (d20>=tc["crit_min"])|
                (d20+p_attack+tc["attack_bonus"]>=boss_def+def_next[sel])
            ))
            crit=hit&(d20>=tc["crit_min"])
            dmg=roll_terms(rng,tc["dice"],tc["flat"],sel.size)
            dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
            dmg=np.where(hit,dmg,0)
            bhp[sel]-=dmg
            if tc["burn"]:
                burn_turns[sel]=np.where(dmg>0,tc["burn"][2],burn_turns[sel])
            if tc["debil"]:
                debil[sel]=np.where(dmg>0,tc["debil"][0],debil[sel])
                debil_turns[sel]=np.where(dmg>0,tc["debil"][1],debil_turns[sel])
            def_next[sel]=0

        win[(bhp<=0)&alive]=True

        # respuesta de la Grulla
        sel=np.flatnonzero(alive & ~win)
        if sel.size:
            if cycle==3:
                def_next[sel]=PATA_DEF_BONUS
            else:
                atk=BOSS_ATTACK+np.where(debil_turns[sel]>0,debil[sel],0)
                d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
                hit=(d20==20)|((d20!=1)&(d20+atk>=p_def))
                crit=hit&(d20==20)

                n,f,flat=BOSS_CAMPANADA if cycle==2 else BOSS_BASIC
                dmg=rng.integers(1,f+1,size=(n,sel.size),dtype=np.int16).sum(axis=0)+flat
                dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
                dmg=np.where(hit,dmg,0)

                hp_before=hp[sel].copy()
                apply_guard_damage(
                    hp,sel,dmg,defender1,defender2,piel_guard,piel_capacity
                )
                absorbed[sel]+=np.maximum(0,(hp_before-dmg)-hp[sel])*-1  # overwritten below

                # Métrica robusta: daño bruto menos daño real recibido.
                real=np.maximum(0,hp_before-hp[sel])
                absorbed[sel]+=np.maximum(0,dmg-real)

        # DOT de raíz
        sel=np.flatnonzero(alive & ~win & (burn_turns>0))
        if sel.size:
            bhp[sel]-=rng.integers(1,4,size=sel.size,dtype=np.int16)
            burn_turns[sel]-=1
            win[(bhp<=0)&alive]=True

        # debuff de raíz
        sel=np.flatnonzero(debil_turns>0)
        if sel.size:
            debil_turns[sel]-=1
            debil[sel[debil_turns[sel]<=0]]=0

        alive[(hp<=0)&alive]=False

    return dict(
        winRate=float(win.mean()),
        avgRounds=float(rounds.mean()),
        avgHp=float(np.maximum(hp,0).mean()),
        avgQi=float(np.maximum(qi,0).mean()),
        avgPielCasts=float(piel_casts.mean()),
        avgPielCapacityLeft=float(np.maximum(piel_capacity,0).mean()),
    )

def run_grid(configs,runs,mode):
    rows=[]
    roots=list(ROOTS)
    for root in roots:
        for o1 in range(1,4):
            for o2 in range(1,4):
                for p1,p2 in configs:
                    pc=piel_conf(p1,p2)
                    for boss_def in (13,14):
                        cfg_id=p1*4+p2
                        seed=(
                            (roots.index(root)+1)*10_000_000
                            +o1*1_000_000
                            +o2*100_000
                            +cfg_id*1_000
                            +boss_def
                            +(0 if mode=="grid" else 50_000_000)
                        )
                        rows.append(dict(
                            root=root,o1=o1,o2=o2,
                            piel_t1=p1,piel_t2=p2,
                            piel_name=config_name(p1,p2),
                            piel_pt=(p1>0)+(p2>0),
                            piel_cost=pc["cost"],
                            piel_guard=pc["guard"],
                            piel_duration=pc["duration"],
                            piel_capacity=pc["capacity"],
                            boss_def=boss_def,
                            **simulate(root,o1,o2,p1,p2,boss_def,runs,seed)
                        ))
    return pd.DataFrame(rows)

def print_summary(df):
    cfg=(df.groupby(
        ["boss_def","piel_t1","piel_t2","piel_name","piel_cost","piel_guard","piel_duration","piel_capacity"]
    ).winRate.agg(["mean","min","max"]).reset_index())

    print("\n=== PROMEDIO POR CONFIGURACIÓN DE PIEL ===")
    print(cfg.sort_values(["boss_def","mean"],ascending=[True,False]).to_string(index=False))

    print("\n=== MEJOR CONFIGURACIÓN PROMEDIO POR DEF ===")
    for d in (13,14):
        z=cfg[cfg.boss_def==d].sort_values("mean",ascending=False).iloc[0]
        delta=(float(z["mean"])-READER_BASELINE[d])*100
        print({
            "boss_def":d,
            "piel_t1":int(z["piel_t1"]),
            "piel_t2":int(z["piel_t2"]),
            "piel_name":z["piel_name"],
            "winRate":float(z["mean"]),
            "delta_vs_reader_pp":delta,
        })

    return cfg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("grid","confirm"),default="grid")
    ap.add_argument("--runs",type=int,default=None)
    ap.add_argument(
        "--finalists",
        default="",
        help="Sólo confirm: pares T1-T2 separados por coma, ej. 1-2,1-3,2-2",
    )
    args=ap.parse_args()

    if len(PIEL_CONFIGS)!=16:
        raise RuntimeError(f"Se esperaban 16 configuraciones legales, hay {len(PIEL_CONFIGS)}")
    if any(((a>0)+(b>0))>2 for a,b in PIEL_CONFIGS):
        raise RuntimeError("Una configuración excede los 2 PT disponibles para Piel")

    if args.mode=="grid":
        configs=PIEL_CONFIGS
        runs=args.runs or DEFAULT_GRID_RUNS
    else:
        configs=parse_finalists(args.finalists)
        if not configs:
            raise SystemExit("--mode confirm requiere --finalists")
        runs=args.runs or DEFAULT_CONFIRM_RUNS

    print("=== GRULLA FASE I-B / PIEL DE COBRE ===")
    print(f"modo={args.mode} · runs/escenario={runs} · configs={len(configs)}")
    print("PIEL_READER: raíz en Golpes; Piel ante Campanada sólo si no hay burbuja;")
    print("             con burbuja viva usa raíz; fallback DEFENDER; básico en Pata.")
    print("Guardia ver74: reserva=Guardia×duración; no decae por rondas.")

    df=run_grid(configs,runs,args.mode)
    cfg=print_summary(df)

    suffix="grid" if args.mode=="grid" else "confirm"
    df.to_csv(f"grulla_phase1_piel_{suffix}_v0.1.csv",index=False)
    cfg.to_csv(f"grulla_phase1_piel_{suffix}_configs_v0.1.csv",index=False)

if __name__=="__main__":
    main()
