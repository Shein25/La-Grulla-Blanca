# Grulla Blanca — Fase I-B · Filamento de Agua aislado · Monte Carlo reproducible
# SOLO Fase I. No Paso, no Piel, no Fase II/III.
# Técnica raíz con 2 PT + Filamento con 0..2 PT. Máximo 4 PT total.
#
# Modos:
#   selección:    python grulla-phase1-filamento-v0.1.py --mode grid --runs 5000
#   confirmación: python grulla-phase1-filamento-v0.1.py --mode confirm --runs 20000 --finalists 3-2,2-2,3-3
#
# Semántica ver74:
# - controlBono base = 2 + maestría; aquí Filamento está en maestría 2 -> +4.
# - prueba: d20 con natural 1 falla / natural 20 acierta; ATQ efectivo vs DEF jefe +2 por unico.
# - jefe unico: toda atadura queda capada a 1 acción.
# - al acertar, jefe obtiene Tenacidad 2 rondas.
# - cooldown del Filamento contra jefe = 1 ronda (duración real capada a 1).
# - dañoAtar sólo ocurre si el control acierta.
# - afinidad Agua: -1 qi para raíz Agua, respetando piso 70%.

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
BOSS_BASIC = (1, 6, 2)
BOSS_CAMPANADA = (2, 6, 2)
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

FIL_BASE = {"cost":6, "atadura":1, "control_bonus":4, "damage_bind":None}
FIL_R1 = [
    {"cost":-1},              # 1 Nudo ligero
    {"damage_bind":(1,3)},    # 2 Hilo cortante
    {"control":3},            # 3 Nudo firme
]
FIL_R2 = [
    {"atadura":2},            # 1 Lazo doble
    {"control":4},            # 2 Nudo perseguidor
    {"damage_bind":(1,4)},    # 3 Lazo medido
]
FIL_NAMES_R1 = {0:"—",1:"Nudo ligero",2:"Hilo cortante",3:"Nudo firme"}
FIL_NAMES_R2 = {0:"—",1:"Lazo doble",2:"Nudo perseguidor",3:"Lazo medido"}

FIL_CONFIGS=[(0,0)]
FIL_CONFIGS += [(a,0) for a in range(1,4)]
FIL_CONFIGS += [(0,b) for b in range(1,4)]
FIL_CONFIGS += [(a,b) for a in range(1,4) for b in range(1,4)]

def root_conf(root,o1,o2):
    q=ROOTS[root]
    cost=q["baseCost"]; attack_bonus=0; crit_min=20
    dice=[q["baseDamage"][:2]]
    flat=q["baseDamage"][2]+1
    burn=None; debil=None
    for m in (q["r1"][o1-1],q["r2"][o2-1]):
        cost += m.get("cost",0)
        attack_bonus += m.get("attack",0)
        crit_min=min(crit_min,m.get("critMin",20))
        if "damage" in m:
            dice.append(m["damage"][:2]); flat += m["damage"][2]
        if "burn" in m: burn=m["burn"]
        if "debil" in m: debil=m["debil"]
    cost=max(math.ceil(q["baseCost"]*.7),max(1,cost-1))
    return dict(cost=cost,attack_bonus=attack_bonus,crit_min=crit_min,
                dice=dice,flat=flat,burn=burn,debil=debil)

def fil_conf(root,p1,p2):
    cost=FIL_BASE["cost"]
    atadura=FIL_BASE["atadura"]
    control=FIL_BASE["control_bonus"]
    damages=[]
    for opt,table in ((p1,FIL_R1),(p2,FIL_R2)):
        if not opt: continue
        m=table[opt-1]
        cost += m.get("cost",0)
        control += m.get("control",0)
        if "atadura" in m:
            # ver74 suma delta respecto de base 1. En maestría 2 un único Lazo doble -> 2.
            atadura += m["atadura"] - FIL_BASE["atadura"]
        if "damage_bind" in m:
            damages.append(m["damage_bind"])
    # Afinidad principal de Filamento sólo para raíz Agua.
    if root=="agua":
        cost-=1
    cost=max(math.ceil(FIL_BASE["cost"]*.7),max(1,cost))
    return dict(cost=cost,atadura=max(1,min(3,atadura)),
                boss_atadura=1,control_bonus=control,damage_bind=damages)

def config_name(p1,p2):
    if p1 and p2: return f"{FIL_NAMES_R1[p1]} + {FIL_NAMES_R2[p2]}"
    if p1: return FIL_NAMES_R1[p1]
    if p2: return FIL_NAMES_R2[p2]
    return "Filamento base"

def parse_finalists(raw):
    out=[]
    for token in (raw or "").split(","):
        token=token.strip()
        if not token: continue
        a,b=map(int,token.split("-")); cfg=(a,b)
        if cfg not in FIL_CONFIGS: raise ValueError(f"Configuración ilegal: {token}")
        out.append(cfg)
    return out

def roll_terms(rng,terms,flat,size):
    out=np.full(size,flat,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def roll_bind_damage(rng,terms,size):
    if not terms: return np.zeros(size,dtype=np.int16)
    out=np.zeros(size,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def control_hit(d20,attack,defense):
    return (d20==20)|((d20!=1)&(d20+attack>=defense))

def simulate(root,o1,o2,p1,p2,boss_def,runs,seed=1):
    rng=np.random.default_rng(seed)
    q=ROOTS[root]
    tc=root_conf(root,o1,o2)
    fc=fil_conf(root,p1,p2)

    p_attack=1+q["attack"]+3+GEAR_ATTACK
    p_def=10+q["defense"]+GEAR_DEFENSE

    hp=np.full(runs,PLAYER_MAX_HP,dtype=np.int16)
    qi=np.full(runs,PLAYER_MAX_QI,dtype=np.int16)
    bhp=np.full(runs,BOSS_HP,dtype=np.int16)
    alive=np.ones(runs,dtype=bool)
    win=np.zeros(runs,dtype=bool)
    potion=np.ones(runs,dtype=bool)

    guard1=np.zeros(runs,dtype=np.int16)
    guard2=np.zeros(runs,dtype=np.int16)
    burn_turns=np.zeros(runs,dtype=np.int8)
    debil=np.zeros(runs,dtype=np.int8)
    debil_turns=np.zeros(runs,dtype=np.int8)
    def_next=np.zeros(runs,dtype=np.int8)

    # Estado control ver74, individual por duelo.
    bound=np.zeros(runs,dtype=np.int8)       # jefe pierde próxima acción si >0
    tenacity=np.zeros(runs,dtype=np.int8)    # 2 tras control exitoso
    tenacity_new=np.zeros(runs,dtype=bool)   # evita decremento el turno de aplicación
    cooldown=np.zeros(runs,dtype=np.int8)    # 1 contra jefe único
    fil_used_this_turn=np.zeros(runs,dtype=bool)

    rounds=np.zeros(runs,dtype=np.int16)
    fil_attempts=np.zeros(runs,dtype=np.int16)
    fil_success=np.zeros(runs,dtype=np.int16)

    for rnd in range(1,81):
        active=alive & ~win
        if not active.any(): break
        idx=np.flatnonzero(active)
        rounds[idx]+=1
        cycle=(rnd-1)%4

        # FILAMENTO_READER:
        # Golpes -> raíz.
        # Campanada -> Filamento si es legal; si Tenacidad/CD/falta qi -> DEFENDER.
        # Pata -> básico.
        # Poción crítica conserva prioridad.
        act=np.zeros(idx.size,dtype=np.int8) # 0 basic,1 root,2 defend,3 potion,4 fil
        if cycle in (0,1):
            act[:]=1
        elif cycle==2:
            legal=(tenacity[idx]<=0)&(cooldown[idx]<=0)&(qi[idx]>=fc["cost"])
            act[:]=np.where(legal,4,2)
        else:
            act[:]=0

        act[(hp[idx]<=9)&potion[idx]]=3
        act[(act==1)&(qi[idx]<tc["cost"])]=0

        fil_used_this_turn[:] = False

        # poción
        sel=idx[act==3]
        if sel.size:
            heal=rng.integers(1,7,size=(3,sel.size),dtype=np.int16).sum(axis=0)+6
            hp[sel]=np.minimum(PLAYER_MAX_HP,hp[sel]+heal); potion[sel]=False

        # DEFENDER
        sel=idx[act==2]
        if sel.size:
            guard1[sel]=rng.integers(35,51,size=sel.size,dtype=np.int16)
            guard2[sel]=rng.integers(25,41,size=sel.size,dtype=np.int16)
            qi[sel]=np.minimum(PLAYER_MAX_QI,qi[sel]+3)

        # Filamento
        sel=idx[act==4]
        if sel.size:
            qi[sel]-=fc["cost"]
            fil_attempts[sel]+=1
            fil_used_this_turn[sel]=True
            cooldown[sel]=1  # jefe único -> duración real 1
            # defensa control = DEF jefe +2 por unico
            d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
            atk_control=p_attack+fc["control_bonus"]
            ok=control_hit(d20,atk_control,boss_def+2)
            succ=sel[ok]
            if succ.size:
                fil_success[succ]+=1
                bound[succ]=1
                tenacity[succ]=2
                tenacity_new[succ]=True
                if fc["damage_bind"]:
                    bhp[succ]-=roll_bind_damage(rng,fc["damage_bind"],succ.size)

        # básico
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

        # avanzarTemporizadores() sucede antes de respuestaEnemigos().
        # CD usado este turno no baja. Tenacidad nueva tampoco baja.
        sel=np.flatnonzero(active & ~fil_used_this_turn & (cooldown>0))
        if sel.size: cooldown[sel]-=1

        sel=np.flatnonzero(active & (tenacity>0) & ~tenacity_new)
        if sel.size: tenacity[sel]-=1
        tenacity_new[:] = False

        # respuesta de Grulla; atadura consume exactamente esta acción.
        sel=np.flatnonzero(alive & ~win)
        if sel.size:
            tied=bound[sel]>0
            if tied.any():
                s=sel[tied]
                bound[s]-=1
            free=sel[~tied]
            if free.size:
                if cycle==3:
                    def_next[free]=PATA_DEF_BONUS
                else:
                    atk=BOSS_ATTACK+np.where(debil_turns[free]>0,debil[free],0)
                    d20=rng.integers(1,21,size=free.size,dtype=np.int16)
                    hit=(d20==20)|((d20!=1)&(d20+atk>=p_def))
                    crit=hit&(d20==20)
                    n,f,flat=BOSS_CAMPANADA if cycle==2 else BOSS_BASIC
                    dmg=rng.integers(1,f+1,size=(n,free.size),dtype=np.int16).sum(axis=0)+flat
                    dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
                    dmg=np.where(hit,dmg,0)

                    g1=guard1[free]; g2=guard2[free]
                    use1=(dmg>0)&(g1>0); use2=(dmg>0)&(~use1)&(g2>0)
                    red=np.zeros(free.size,dtype=np.int16)
                    red[use1]=np.floor(dmg[use1]*g1[use1]/100).astype(np.int16)
                    red[use2]=np.floor(dmg[use2]*g2[use2]/100).astype(np.int16)
                    hp[free]-=dmg-red
                    if use1.any():
                        s=free[use1]; guard1[s]=guard2[s]; guard2[s]=0
                    if use2.any(): guard2[free[use2]]=0

        # DOT raíz
        sel=np.flatnonzero(alive & ~win & (burn_turns>0))
        if sel.size:
            bhp[sel]-=rng.integers(1,4,size=sel.size,dtype=np.int16)
            burn_turns[sel]-=1
            win[(bhp<=0)&alive]=True

        # debuff raíz
        sel=np.flatnonzero(debil_turns>0)
        if sel.size:
            debil_turns[sel]-=1
            debil[sel[debil_turns[sel]<=0]]=0

        alive[(hp<=0)&alive]=False

    attempts=fil_attempts.sum()
    successes=fil_success.sum()
    return dict(
        winRate=float(win.mean()),
        avgRounds=float(rounds.mean()),
        avgHp=float(np.maximum(hp,0).mean()),
        avgQi=float(np.maximum(qi,0).mean()),
        avgFilAttempts=float(fil_attempts.mean()),
        filSuccessRate=float(successes/attempts) if attempts else 0.0,
    )

def run_grid(configs,runs,mode):
    rows=[]
    roots=list(ROOTS)
    for root in roots:
        for o1 in range(1,4):
            for o2 in range(1,4):
                for p1,p2 in configs:
                    fc=fil_conf(root,p1,p2)
                    for boss_def in (13,14):
                        cfg_id=p1*4+p2
                        seed=((roots.index(root)+1)*10_000_000+o1*1_000_000+o2*100_000+
                              cfg_id*1_000+boss_def+(0 if mode=="grid" else 50_000_000))
                        rows.append(dict(
                            root=root,o1=o1,o2=o2,
                            fil_t1=p1,fil_t2=p2,fil_name=config_name(p1,p2),
                            fil_pt=(p1>0)+(p2>0),
                            fil_cost=fc["cost"],fil_atadura=fc["atadura"],
                            fil_boss_atadura=fc["boss_atadura"],
                            fil_control_bonus=fc["control_bonus"],
                            fil_damage_bind="+".join(f"{n}d{f}" for n,f in fc["damage_bind"]) or "—",
                            boss_def=boss_def,
                            **simulate(root,o1,o2,p1,p2,boss_def,runs,seed)
                        ))
    return pd.DataFrame(rows)

def print_summary(df):
    group_cols=["boss_def","fil_t1","fil_t2","fil_name","fil_pt",
                "fil_atadura","fil_boss_atadura","fil_control_bonus","fil_damage_bind"]
    # Coste depende de afinidad raíz, por eso se reporta aparte por raíz y no como clave global.
    cfg=df.groupby(group_cols).agg(
        mean=("winRate","mean"),min=("winRate","min"),max=("winRate","max"),
        controlSuccess=("filSuccessRate","mean")
    ).reset_index()
    print("\n=== PROMEDIO POR CONFIGURACIÓN DE FILAMENTO ===")
    print(cfg.sort_values(["boss_def","mean"],ascending=[True,False]).to_string(index=False))

    print("\n=== COSTE POR RAÍZ ===")
    print(df.groupby(["fil_t1","fil_t2","fil_name","root"]).fil_cost.first().to_string())

    print("\n=== MEJOR CONFIGURACIÓN PROMEDIO POR DEF ===")
    for d in (13,14):
        z=cfg[cfg.boss_def==d].sort_values("mean",ascending=False).iloc[0]
        print({
            "boss_def":d,
            "fil_t1":int(z.fil_t1),"fil_t2":int(z.fil_t2),
            "fil_name":z.fil_name,
            "winRate":float(z["mean"]),
            "delta_vs_reader_pp":(float(z["mean"])-READER_BASELINE[d])*100,
            "control_success":float(z.controlSuccess),
        })
    return cfg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("grid","confirm"),default="grid")
    ap.add_argument("--runs",type=int,default=None)
    ap.add_argument("--finalists",default="",
                    help="Sólo confirm: pares T1-T2 separados por coma, ej. 3-2,2-2,3-3")
    args=ap.parse_args()

    if len(FIL_CONFIGS)!=16:
        raise RuntimeError(f"Se esperaban 16 configuraciones, hay {len(FIL_CONFIGS)}")

    if args.mode=="grid":
        configs=FIL_CONFIGS; runs=args.runs or DEFAULT_GRID_RUNS
    else:
        configs=parse_finalists(args.finalists)
        if not configs: raise SystemExit("--mode confirm requiere --finalists")
        runs=args.runs or DEFAULT_CONFIRM_RUNS

    print("=== GRULLA FASE I-B / FILAMENTO DE AGUA ===")
    print(f"modo={args.mode} · runs/escenario={runs} · configs={len(configs)}")
    print("FILAMENTO_READER: raíz en Golpes; Filamento ante Campanada si legal;")
    print("                  fallback DEFENDER; básico en Pata; poción crítica prioritaria.")
    print("Jefe único: atadura máxima 1 acción + Tenacidad 2; cooldown real 1.")

    df=run_grid(configs,runs,args.mode)
    cfg=print_summary(df)
    suffix="grid" if args.mode=="grid" else "confirm"
    df.to_csv(f"grulla_phase1_filamento_{suffix}_v0.1.csv",index=False)
    cfg.to_csv(f"grulla_phase1_filamento_{suffix}_configs_v0.1.csv",index=False)

if __name__=="__main__":
    main()
