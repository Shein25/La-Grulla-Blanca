# Grulla Blanca — Fase I · multi-optionals con Piel G345_D1 · Monte Carlo reproducible
# SOLO Fase I. No Fase II/III.
#
# Root = 2 PT fijos. Paso/Piel/Filamento comparten como máximo 2 PT adicionales.
# Se prueban loadouts de 2 o 3 opcionales y se deduplican por efecto real antes del MC.
#
# Selección:
#   python grulla-phase1-multi-optionals-v0.1.py --loadout paso_piel --runs 5000
#   python grulla-phase1-multi-optionals-v0.1.py --loadout paso_filamento --runs 5000
#   python grulla-phase1-multi-optionals-v0.1.py --loadout piel_filamento --runs 5000
#   python grulla-phase1-multi-optionals-v0.1.py --loadout triple --runs 5000
#
# Confirmación:
#   python grulla-phase1-multi-optionals-v0.1.py --loadout paso_piel --mode confirm --runs 20000 --ids P12_C00
#
# Política MULTI_READER_RES (stress-test táctico, sin RNG futuro):
# Pata telegraphía Resonancia. Paso, si existe, se reserva para esa ventana.
# Resonancia x1.50 sólo se aplica al Golpe siguiente si impacta con Piel activa.
#   Golpe 1: si Piel está preparada y no queda burbuja, precargar Piel; si no, raíz.
#   Golpe 2: si Paso está preparado y no cubriría Campanada, precargar Paso; si no, raíz.
#   Campanada:
#       1) Filamento si está legal (sin Tenacidad/CD y con qi);
#       2) si ya hay Piel/Paso activo, atacar con raíz;
#       3) si no hay protección: Piel, luego Paso, luego DEFENDER.
#   Pata: ATACAR básico.
#   Poción crítica conserva prioridad.
#
# No hay lectura del resultado futuro de control, esquiva, impacto, daño ni crítico.

import argparse
import itertools
import math
import numpy as np
import pandas as pd
import zlib

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

BASE_CONFIGS=[(0,0)]
BASE_CONFIGS += [(a,0) for a in range(1,4)]
BASE_CONFIGS += [(0,b) for b in range(1,4)]
BASE_CONFIGS += [(a,b) for a in range(1,4) for b in range(1,4)]

PASO_R1=[{"durationExtra":1},{"evasion":22},{"cost":-1}]
PASO_R2=[{"cost":-1},{"evasion":25},{"durationExtra":1}]
PIEL_R1=[{"guard":4},{"durationExtra":1},{"cost":-1}]
PIEL_R2=[{"cost":-1},{"guard":5},{"durationExtra":1}]
FIL_R1=[{"cost":-1},{"damage_bind":(1,3)},{"control":3}]
FIL_R2=[{"atadura":2},{"control":4},{"damage_bind":(1,4)}]

LOADOUTS = {
    "paso_piel": ("paso","piel"),
    "paso_filamento": ("paso","filamento"),
    "piel_filamento": ("piel","filamento"),
    "triple": ("paso","piel","filamento"),
}

def pts(cfg):
    return int(cfg[0]>0)+int(cfg[1]>0)

def root_conf(root,o1,o2):
    q=ROOTS[root]
    cost=q["baseCost"]; attack_bonus=0; crit_min=20
    dice=[q["baseDamage"][:2]]; flat=q["baseDamage"][2]+1
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

def paso_conf(cfg):
    p1,p2=cfg; cost=5; evasion=15; duration=2
    for opt,table in ((p1,PASO_R1),(p2,PASO_R2)):
        if not opt: continue
        m=table[opt-1]
        cost += m.get("cost",0)
        if "evasion" in m: evasion=m["evasion"]
        duration += m.get("durationExtra",0)
    cost=max(math.ceil(5*.7),max(1,cost))
    return dict(cost=cost,evasion=evasion,duration=duration)

def piel_conf(cfg):
    p1,p2=cfg; cost=5; guard=3; duration=1
    for opt,table in ((p1,PIEL_R1),(p2,PIEL_R2)):
        if not opt: continue
        m=table[opt-1]
        cost += m.get("cost",0)
        if "guard" in m: guard=m["guard"]
        duration += m.get("durationExtra",0)
    cost=max(math.ceil(5*.7),max(1,cost))
    return dict(cost=cost,guard=guard,duration=duration,capacity=guard*duration)

def fil_conf(root,cfg):
    p1,p2=cfg; cost=6; atadura=1; control=4; damage_bind=[]
    for opt,table in ((p1,FIL_R1),(p2,FIL_R2)):
        if not opt: continue
        m=table[opt-1]
        cost += m.get("cost",0)
        control += m.get("control",0)
        if "atadura" in m: atadura += m["atadura"]-1
        if "damage_bind" in m: damage_bind.append(m["damage_bind"])
    if root=="agua": cost-=1
    cost=max(math.ceil(6*.7),max(1,cost))
    return dict(cost=cost,atadura=max(1,min(3,atadura)),
                boss_atadura=1,control_bonus=control,
                damage_bind=tuple(damage_bind))

def effective_tuple(root,tech,cfg):
    if tech=="paso":
        c=paso_conf(cfg); return (c["cost"],c["evasion"],c["duration"])
    if tech=="piel":
        c=piel_conf(cfg); return (c["cost"],c["guard"],c["duration"],c["capacity"])
    c=fil_conf(root,cfg)
    # Contra jefe único la atadura nominal >1 no cambia duración ni cooldown reales.
    return (c["cost"],c["boss_atadura"],c["control_bonus"],c["damage_bind"])

def cfg_id(techs,choices):
    by={t:c for t,c in zip(techs,choices)}
    out=[]
    if "paso" in by: out.append(f"P{by['paso'][0]}{by['paso'][1]}")
    if "piel" in by: out.append(f"C{by['piel'][0]}{by['piel'][1]}")
    if "filamento" in by: out.append(f"F{by['filamento'][0]}{by['filamento'][1]}")
    return "_".join(out)

def generate_dedup(loadout):
    techs=LOADOUTS[loadout]
    raw=[]
    for choices in itertools.product(BASE_CONFIGS, repeat=len(techs)):
        total=sum(pts(c) for c in choices)
        if total>2: continue
        # Equivalencia global: debe ser idéntica para las tres raíces.
        eff=tuple(
            tuple(effective_tuple(root,t,c) for t,c in zip(techs,choices))
            for root in ("fuego","metal","agua")
        )
        raw.append((choices,total,eff))
    best={}
    for choices,total,eff in raw:
        candidate=(total,choices)
        if eff not in best or candidate < best[eff][0]:
            best[eff]=(candidate,choices)
    dedup=[v[1] for v in best.values()]
    dedup.sort(key=lambda ch:(sum(pts(c) for c in ch),cfg_id(techs,ch)))
    return raw,dedup

def roll_terms(rng,terms,flat,size):
    out=np.full(size,flat,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def roll_bind_damage(rng,terms,size):
    out=np.zeros(size,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def control_hit(d20,attack,defense):
    return (d20==20)|((d20!=1)&(d20+attack>=defense))

def simulate(root,o1,o2,techs,choices,boss_def,runs,seed=1):
    rng=np.random.default_rng(seed)
    q=ROOTS[root]; tc=root_conf(root,o1,o2)
    chosen={t:c for t,c in zip(techs,choices)}
    pc=paso_conf(chosen["paso"]) if "paso" in chosen else None
    cc=piel_conf(chosen["piel"]) if "piel" in chosen else None
    fc=fil_conf(root,chosen["filamento"]) if "filamento" in chosen else None

    p_attack=1+q["attack"]+3+GEAR_ATTACK
    p_def=10+q["defense"]+GEAR_DEFENSE

    hp=np.full(runs,PLAYER_MAX_HP,dtype=np.int16)
    qi=np.full(runs,PLAYER_MAX_QI,dtype=np.int16)
    bhp=np.full(runs,BOSS_HP,dtype=np.int16)
    alive=np.ones(runs,dtype=bool); win=np.zeros(runs,dtype=bool)
    potion=np.ones(runs,dtype=bool)

    guard1=np.zeros(runs,dtype=np.int16); guard2=np.zeros(runs,dtype=np.int16)
    piel_guard=np.zeros(runs,dtype=np.int16); piel_capacity=np.zeros(runs,dtype=np.int16)
    paso_bonus=np.zeros(runs,dtype=np.int16); paso_turns=np.zeros(runs,dtype=np.int8)

    bound=np.zeros(runs,dtype=np.int8)
    tenacity=np.zeros(runs,dtype=np.int8); tenacity_new=np.zeros(runs,dtype=bool)
    cooldown=np.zeros(runs,dtype=np.int8); fil_used=np.zeros(runs,dtype=bool)

    burn_turns=np.zeros(runs,dtype=np.int8)
    debil=np.zeros(runs,dtype=np.int8); debil_turns=np.zeros(runs,dtype=np.int8)
    def_next=np.zeros(runs,dtype=np.int8); rounds=np.zeros(runs,dtype=np.int16)\n    resonance_ready=np.zeros(runs,dtype=bool)

    casts_paso=np.zeros(runs,dtype=np.int16)
    casts_piel=np.zeros(runs,dtype=np.int16)
    attempts_fil=np.zeros(runs,dtype=np.int16); success_fil=np.zeros(runs,dtype=np.int16)

    for rnd in range(1,81):
        active=alive & ~win
        if not active.any(): break
        idx=np.flatnonzero(active); rounds[idx]+=1
        cycle=(rnd-1)%4

        act=np.zeros(idx.size,dtype=np.int8) # 0 basic,1 root,2 defend,3 potion,4 paso,5 piel,6 fil

        if cycle==0:
            # Tras Pata, reservar Paso para la ventana telegráfica de Resonancia.
            act[:]=1
            if pc is not None:
                adapt=resonance_ready[idx]&(piel_capacity[idx]>0)&(qi[idx]>=pc["cost"])
                act[adapt]=4
            if cc is not None:
                need=(act==1)&(piel_capacity[idx]<=0)&(qi[idx]>=cc["cost"])
                act[need]=5
        elif cycle==1:
            # No precargar Paso para Campanada: se conserva para Resonancia.
            act[:]=1
        elif cycle==2:
            # Campanada: control primero. No se conoce de antemano si acertará.
            act[:]=2
            if fc is not None:
                legal=(tenacity[idx]<=0)&(cooldown[idx]<=0)&(qi[idx]>=fc["cost"])
                act[legal]=6
            not_fil=act!=6
            protected=(piel_capacity[idx]>0)|(paso_turns[idx]>0)
            # Si ya hay protección y no se puede/decide controlar, aprovechar la ventana para atacar.
            root_ok=not_fil & protected & (qi[idx]>=tc["cost"])
            act[root_ok]=1
            remain=not_fil & ~protected
            if cc is not None:
                use=remain & (qi[idx]>=cc["cost"])
                act[use]=5; remain &= ~use
            if pc is not None:
                use=remain & (qi[idx]>=pc["cost"])
                act[use]=4; remain &= ~use
            # lo restante conserva DEFENDER
        else:
            act[:]=0

        # Prioridad de poción crítica.
        act[(hp[idx]<=9)&potion[idx]]=3
        act[(act==1)&(qi[idx]<tc["cost"])]=0

        fil_used[:] = False

        sel=idx[act==3]
        if sel.size:
            heal=rng.integers(1,7,size=(3,sel.size),dtype=np.int16).sum(axis=0)+6
            hp[sel]=np.minimum(PLAYER_MAX_HP,hp[sel]+heal); potion[sel]=False

        sel=idx[act==2]
        if sel.size:
            # DEFENDER reemplaza Guardia/Piel, igual que ver74.
            piel_guard[sel]=0; piel_capacity[sel]=0
            guard1[sel]=rng.integers(35,51,size=sel.size,dtype=np.int16)
            guard2[sel]=rng.integers(25,41,size=sel.size,dtype=np.int16)
            qi[sel]=np.minimum(PLAYER_MAX_QI,qi[sel]+3)

        sel=idx[act==4]
        if sel.size:
            qi[sel]-=pc["cost"]; casts_paso[sel]+=1
            paso_bonus[sel]=pc["evasion"]; paso_turns[sel]=pc["duration"]

        sel=idx[act==5]
        if sel.size:
            qi[sel]-=cc["cost"]; casts_piel[sel]+=1
            # Piel reemplaza DEFENDER, misma categoría guardia.
            guard1[sel]=0; guard2[sel]=0
            piel_guard[sel]=cc["guard"]; piel_capacity[sel]=cc["capacity"]

        sel=idx[act==6]
        if sel.size:
            qi[sel]-=fc["cost"]; attempts_fil[sel]+=1; fil_used[sel]=True
            cooldown[sel]=1
            d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
            ok=control_hit(d20,p_attack+fc["control_bonus"],boss_def+2)
            succ=sel[ok]
            if succ.size:
                success_fil[succ]+=1; bound[succ]=1
                tenacity[succ]=2; tenacity_new[succ]=True
                if fc["damage_bind"]:
                    bhp[succ]-=roll_bind_damage(rng,fc["damage_bind"],succ.size)

        sel=idx[act==0]
        if sel.size:
            d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
            hit=(d20==20)|((d20!=1)&(d20+p_attack>=boss_def+def_next[sel]))
            crit=hit&(d20==20)
            dmg=rng.integers(1,9,size=sel.size,dtype=np.int16)
            dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
            bhp[sel]-=np.where(hit,dmg,0); def_next[sel]=0

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
            dmg=np.where(hit,dmg,0); bhp[sel]-=dmg
            if tc["burn"]:
                burn_turns[sel]=np.where(dmg>0,tc["burn"][2],burn_turns[sel])
            if tc["debil"]:
                debil[sel]=np.where(dmg>0,tc["debil"][0],debil[sel])
                debil_turns[sel]=np.where(dmg>0,tc["debil"][1],debil_turns[sel])
            def_next[sel]=0

        win[(bhp<=0)&alive]=True

        # Temporizadores de control antes de la respuesta enemiga.
        sel=np.flatnonzero(active & ~fil_used & (cooldown>0))
        if sel.size: cooldown[sel]-=1
        sel=np.flatnonzero(active & (tenacity>0) & ~tenacity_new)
        if sel.size: tenacity[sel]-=1
        tenacity_new[:] = False

        sel=np.flatnonzero(alive & ~win)
        if sel.size:
            tied=bound[sel]>0
            if tied.any(): bound[sel[tied]]-=1
            free=sel[~tied]
            if free.size:
                if cycle==3:
                    def_next[free]=PATA_DEF_BONUS\n                    resonance_ready[free]=True
                else:
                    atk=BOSS_ATTACK+np.where(debil_turns[free]>0,debil[free],0)
                    d20=rng.integers(1,21,size=free.size,dtype=np.int16)
                    evade_extra=np.rint(paso_bonus[free]/5.0).astype(np.int16)
                    hit=(d20==20)|((d20!=1)&(d20+atk>=p_def+evade_extra))
                    crit=hit&(d20==20)
                    n,f,flat=BOSS_CAMPANADA if cycle==2 else BOSS_BASIC
                    dmg=rng.integers(1,f+1,size=(n,free.size),dtype=np.int16).sum(axis=0)+flat
                    dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg)
                    dmg=np.where(hit,dmg,0)

                    # Golpe posterior a Pata: x1.50 bruto si conecta con Piel activa.
                    resonant=(cycle==0)&resonance_ready[free]&(dmg>0)&(piel_capacity[free]>0)
                    if resonant.any():
                        dmg[resonant]=np.ceil(dmg[resonant]*1.50).astype(np.int16)

                    # Piel/Guardia de técnica si existe.
                    cap=piel_capacity[free]
                    has_piel=(dmg>0)&(cap>0)
                    remaining=dmg.copy()
                    if has_piel.any():
                        absorb=np.zeros(free.size,dtype=np.int16)
                        absorb[has_piel]=np.minimum(
                            dmg[has_piel],
                            np.minimum(piel_guard[free[has_piel]],cap[has_piel])
                        )
                        remaining-=absorb
                        s=free[has_piel]
                        piel_capacity[s]-=absorb[has_piel]
                        piel_guard[s]=np.where(piel_capacity[s]>0,piel_guard[s],0)

                    # DEFENDER sólo donde no hay Piel; ambas no coexisten por categoría.
                    no_piel=~has_piel
                    if no_piel.any():
                        loc=np.flatnonzero(no_piel); s=free[loc]; d=remaining[loc]
                        g1=guard1[s]; g2=guard2[s]
                        use1=(d>0)&(g1>0); use2=(d>0)&(~use1)&(g2>0)
                        red=np.zeros(loc.size,dtype=np.int16)
                        red[use1]=np.floor(d[use1]*g1[use1]/100).astype(np.int16)
                        red[use2]=np.floor(d[use2]*g2[use2]/100).astype(np.int16)
                        remaining[loc]-=red
                        if use1.any():
                            ss=s[use1]; guard1[ss]=guard2[ss]; guard2[ss]=0
                        if use2.any(): guard2[s[use2]]=0
                    hp[free]-=remaining\n\n                    # La Resonancia se consume aunque el Golpe falle.\n                    if cycle==0:\n                        resonance_ready[free]=False

        # DOT/debuff raíz.
        sel=np.flatnonzero(alive & ~win & (burn_turns>0))
        if sel.size:
            bhp[sel]-=rng.integers(1,4,size=sel.size,dtype=np.int16)
            burn_turns[sel]-=1; win[(bhp<=0)&alive]=True
        sel=np.flatnonzero(debil_turns>0)
        if sel.size:
            debil_turns[sel]-=1; debil[sel[debil_turns[sel]<=0]]=0

        # Paso decae tras respuesta enemiga, igual que el bloque aislado.
        sel=np.flatnonzero(paso_turns>0)
        if sel.size:
            paso_turns[sel]-=1
            exp=sel[paso_turns[sel]<=0]
            if exp.size: paso_bonus[exp]=0

        alive[(hp<=0)&alive]=False

    attempts=attempts_fil.sum(); succ=success_fil.sum()
    return dict(
        winRate=float(win.mean()),
        avgRounds=float(rounds.mean()),
        avgHp=float(np.maximum(hp,0).mean()),
        avgQi=float(np.maximum(qi,0).mean()),
        avgPasoCasts=float(casts_paso.mean()),
        avgPielCasts=float(casts_piel.mean()),
        avgFilAttempts=float(attempts_fil.mean()),
        filSuccessRate=float(succ/attempts) if attempts else 0.0,
    )

def parse_ids(raw):
    return {x.strip() for x in (raw or "").split(",") if x.strip()}

def run(loadout,runs,mode,ids=None):
    techs=LOADOUTS[loadout]
    raw,dedup=generate_dedup(loadout)
    if mode=="confirm":
        wanted=parse_ids(ids)
        dedup=[ch for ch in dedup if cfg_id(techs,ch) in wanted]
        if not dedup: raise SystemExit("Ningún --ids coincide con configuraciones deduplicadas.")
    print(f"raw={len(raw)} dedup={len(dedup)} loadout={loadout} runs={runs}")

    rows=[]; roots=list(ROOTS)
    for choices in dedup:
        cid=cfg_id(techs,choices); optional_pts=sum(pts(c) for c in choices)
        for root in roots:
            chosen={t:c for t,c in zip(techs,choices)}
            pc=paso_conf(chosen["paso"]) if "paso" in chosen else None
            cc=piel_conf(chosen["piel"]) if "piel" in chosen else None
            fc=fil_conf(root,chosen["filamento"]) if "filamento" in chosen else None
            for o1 in range(1,4):
                for o2 in range(1,4):
                    for boss_def in (13,14):
                        seed=zlib.crc32(f"{loadout}|{cid}|{root}|{o1}|{o2}|{boss_def}|{mode}".encode("utf-8")) & 0xffffffff
                        row=dict(loadout=loadout,config_id=cid,optional_pts=optional_pts,
                                 root=root,o1=o1,o2=o2,boss_def=boss_def)
                        if pc:
                            row.update(paso_cost=pc["cost"],paso_evasion=pc["evasion"],paso_duration=pc["duration"])
                        if cc:
                            row.update(piel_cost=cc["cost"],piel_guard=cc["guard"],piel_capacity=cc["capacity"])
                        if fc:
                            row.update(fil_cost=fc["cost"],fil_control=fc["control_bonus"],
                                       fil_damage="+".join(f"{n}d{f}" for n,f in fc["damage_bind"]) or "—")
                        row.update(simulate(root,o1,o2,techs,choices,boss_def,runs,seed))
                        rows.append(row)
    return pd.DataFrame(rows),len(raw),len(dedup)

def summarize(df):
    cfg=df.groupby(["loadout","config_id","optional_pts","boss_def"]).winRate.agg(["mean","min","max"]).reset_index()
    print("\n=== TOP 15 POR DEF ===")
    for d in (13,14):
        print(f"\nDEF {d}")
        print(cfg[cfg.boss_def==d].sort_values("mean",ascending=False).head(15).to_string(index=False))
    print("\n=== MEJOR POR DEF ===")
    for d in (13,14):
        z=cfg[cfg.boss_def==d].sort_values("mean",ascending=False).iloc[0]
        print(dict(boss_def=d,config_id=z.config_id,winRate=float(z["mean"]),
                   delta_vs_reader_pp=(float(z["mean"])-READER_BASELINE[d])*100))
    return cfg

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--loadout",choices=tuple(LOADOUTS),required=True)
    ap.add_argument("--mode",choices=("grid","confirm"),default="grid")
    ap.add_argument("--runs",type=int,default=None)
    ap.add_argument("--ids",default="")
    args=ap.parse_args()
    runs=args.runs or (DEFAULT_GRID_RUNS if args.mode=="grid" else DEFAULT_CONFIRM_RUNS)
    df,raw_count,dedup_count=run(args.loadout,runs,args.mode,args.ids)
    cfg=summarize(df)
    suffix="grid" if args.mode=="grid" else "confirm"
    df.to_csv(f"grulla_phase1_multi_{args.loadout}_{suffix}_v0.1.csv",index=False)
    cfg.to_csv(f"grulla_phase1_multi_{args.loadout}_{suffix}_configs_v0.1.csv",index=False)
    print(f"\nraw={raw_count} -> dedup={dedup_count}")

if __name__=="__main__":
    main()
