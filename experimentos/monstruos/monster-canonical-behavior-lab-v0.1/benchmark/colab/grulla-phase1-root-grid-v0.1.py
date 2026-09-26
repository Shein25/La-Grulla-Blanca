# Grulla Blanca — Fase I (150 HP) · Monte Carlo reproducible
# Diseñado para ejecutar en Google Colab o Python 3 con numpy/pandas.
# Alcance deliberado: SOLO 27 formas de técnica raíz. No Fase II/III.
# Default: 20.000 duelos por escenario.

import math
import numpy as np
import pandas as pd

RUNS = 20_000
PLAYER_MAX_HP = 28
PLAYER_MAX_QI = 110
GEAR_ATTACK = 2
GEAR_DEFENSE = 7
BOSS_HP = 150
BOSS_ATTACK = 4
BOSS_BASIC = (1, 6, 2)      # 1d6+2
BOSS_CAMPANADA = (2, 6, 2)  # 2d6+2
PATA_DEF_BONUS = 3           # supuesto actual del laboratorio, no histórico cerrado

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

STRATEGIES = ("SPAM","ALTERNATE","READER")

def technique_conf(root,o1,o2):
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
            dice.append(m["damage"][:2]); flat += m["damage"][2]
        if "burn" in m: burn=m["burn"]
        if "debil" in m: debil=m["debil"]
    cost=max(math.ceil(q["baseCost"]*.7),max(1,cost-1))
    return dict(cost=cost,attack_bonus=attack_bonus,crit_min=crit_min,dice=dice,flat=flat,burn=burn,debil=debil)

def roll_terms(rng,terms,flat,size):
    out=np.full(size,flat,dtype=np.int16)
    for n,f in terms:
        out += rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
    return out

def simulate(root,o1,o2,boss_def,strategy,runs=RUNS,seed=1):
    rng=np.random.default_rng(seed)
    q=ROOTS[root]
    tc=technique_conf(root,o1,o2)
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
    rounds=np.zeros(runs,dtype=np.int16)

    for rnd in range(1,81):
        active=alive & ~win
        if not active.any(): break
        idx=np.flatnonzero(active); rounds[idx]+=1
        cycle=(rnd-1)%4  # Golpe, Golpe, Campanada, Pata

        act=np.zeros(idx.size,dtype=np.int8) # 0 basic,1 tech,2 defend,3 potion
        if strategy=="SPAM":
            act[:]=np.where(qi[idx]>=tc["cost"],1,0)
        elif strategy=="ALTERNATE":
            act[:]=1 if rnd%2 else 0
            act[(hp[idx]<=8)&potion[idx]]=3
            act[(act==1)&(qi[idx]<tc["cost"])]=0
        elif strategy=="READER":
            act[:]=0 if cycle==3 else (2 if cycle==2 else 1)
            act[(hp[idx]<=9)&potion[idx]]=3
            act[(act==1)&(qi[idx]<tc["cost"])]=0

        sel=idx[act==3]
        if sel.size:
            heal=rng.integers(1,7,size=(3,sel.size),dtype=np.int16).sum(axis=0)+6
            hp[sel]=np.minimum(PLAYER_MAX_HP,hp[sel]+heal); potion[sel]=False

        sel=idx[act==2]
        if sel.size:
            guard1[sel]=rng.integers(35,51,size=sel.size,dtype=np.int16)
            guard2[sel]=rng.integers(25,41,size=sel.size,dtype=np.int16)
            qi[sel]=np.minimum(PLAYER_MAX_QI,qi[sel]+3)

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
            hit=(d20==20)|((d20!=1)&((d20>=tc["crit_min"])|(d20+p_attack+tc["attack_bonus"]>=boss_def+def_next[sel])))
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
                g1=guard1[sel]; g2=guard2[sel]
                use1=(dmg>0)&(g1>0); use2=(dmg>0)&(~use1)&(g2>0)
                red=np.zeros(sel.size,dtype=np.int16)
                red[use1]=np.floor(dmg[use1]*g1[use1]/100).astype(np.int16)
                red[use2]=np.floor(dmg[use2]*g2[use2]/100).astype(np.int16)
                hp[sel]-=dmg-red
                if use1.any():
                    s=sel[use1]; guard1[s]=guard2[s]; guard2[s]=0
                if use2.any(): guard2[sel[use2]]=0

        sel=np.flatnonzero(alive & ~win & (burn_turns>0))
        if sel.size:
            bhp[sel]-=rng.integers(1,4,size=sel.size,dtype=np.int16)
            burn_turns[sel]-=1
            win[(bhp<=0)&alive]=True

        sel=np.flatnonzero(debil_turns>0)
        if sel.size:
            debil_turns[sel]-=1
            debil[sel[debil_turns[sel]<=0]]=0

        alive[(hp<=0)&alive]=False

    return dict(winRate=float(win.mean()),avgRounds=float(rounds.mean()))

rows=[]
roots=list(ROOTS)
for root in roots:
    for o1 in range(1,4):
        for o2 in range(1,4):
            for boss_def in (13,14):
                for strategy in STRATEGIES:
                    seed=(roots.index(root)+1)*100000+o1*10000+o2*1000+boss_def*10+STRATEGIES.index(strategy)
                    rows.append(dict(root=root,o1=o1,o2=o2,boss_def=boss_def,strategy=strategy,
                                     **simulate(root,o1,o2,boss_def,strategy,RUNS,seed)))

df=pd.DataFrame(rows)
print(df.groupby(["boss_def","strategy","root"]).winRate.agg(["mean","min","max"]).to_string())
df.to_csv("grulla_phase1_root_grid_v0.1.csv",index=False)
