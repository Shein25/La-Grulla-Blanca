# Grulla Blanca — Fase I · sensibilidad final de Pata Inmóvil v0.1
# SOLO Fase I. No Fase II/III.
# Compara Pata +2/+3/+4 sobre rutas representativas ya cerradas.
#
# Rutas:
# - READER universal
# - Paso óptimo: Paso prolongado + Paso velado
# - Filamento óptimo por sensibilidad DEF
# - Piel G234_D1 óptima: Cobre flexible + Cobre grueso
#
# Uso:
#   python grulla-phase1-final-pata-sensitivity-v0.1.py --runs 20000

import argparse, math
import numpy as np
import pandas as pd
from numba import njit

PLAYER_MAX_HP=28
PLAYER_MAX_QI=110
GEAR_ATTACK=2
GEAR_DEFENSE=7
BOSS_HP=150
BOSS_ATTACK=4

ROOTS={
 0:{"attack":1,"defense":0,"baseCost":7,"baseDamage":(2,6,2)},
 1:{"attack":2,"defense":0,"baseCost":6,"baseDamage":(1,10,3)},
 2:{"attack":0,"defense":2,"baseCost":6,"baseDamage":(2,6,0)},
}
STRATEGIES={0:"READER",1:"PASO",2:"FILAMENTO",3:"PIEL_G234_D1"}

@njit
def dice(n,f):
    s=0
    for _ in range(n): s+=np.random.randint(1,f+1)
    return s

@njit
def root_stats(root,o1,o2):
    if root==0:
        ratt=1; rdef=0; basecost=7; nd=2; fd=6; flat=2
    elif root==1:
        ratt=2; rdef=0; basecost=6; nd=1; fd=10; flat=3
    else:
        ratt=0; rdef=2; basecost=6; nd=2; fd=6; flat=0
    cost=basecost; ab=0; crit=20; add=0; burn=0; deba=0; debdur=0
    if root==0:
        if o1==1: burn=2
        elif o1==2: add=1
        else: ab+=3
        if o2==1: cost-=1
        elif o2==2: ab+=4
        else: crit=19
    elif root==1:
        if o1==1: ab+=3
        elif o1==2: add=1
        else: crit=19
        if o2==1: cost-=1; crit=19
        elif o2==2: ab+=4
        else: deba=-2; debdur=1
    else:
        if o1==1: deba=-1; debdur=1
        elif o1==2: add=1
        else: ab+=3
        if o2==1: cost-=1
        elif o2==2: ab+=4
        else: crit=19
    cost=max(math.ceil(basecost*.7),cost-1)
    return ratt,rdef,cost,nd,fd,flat+1,ab,crit,add,burn,deba,debdur

@njit
def one_duel(strategy,root,o1,o2,boss_def,pata_bonus):
    ratt,rdef,root_cost,nd,fd,flat,root_ab,critmin,add,root_burn,root_deb,root_debdur=root_stats(root,o1,o2)
    patt=1+ratt+3+GEAR_ATTACK
    pdef=10+rdef+GEAR_DEFENSE

    # Paso óptimo: coste 5, esquiva 25, duración 3.
    paso_cost=5; paso_ev=25; paso_dur=3
    # Piel G234_D1 óptima: coste 5, Guardia 4, duración 2, reserva 8.
    piel_cost=5; piel_guard_max=4; piel_cap_max=8

    # Filamento óptimo por DEF.
    if boss_def==13:
        fil_ctrl=4; fil_dm1=3; fil_dm2=4  # Hilo cortante + Lazo medido
    else:
        fil_ctrl=7; fil_dm1=0; fil_dm2=4  # Nudo firme + Lazo medido
    fil_cost=5 if root==2 else 6

    hp=PLAYER_MAX_HP; qi=PLAYER_MAX_QI; bhp=BOSS_HP; potion=1
    def1=0; def2=0
    paso_bonus_active=0; paso_turns=0
    piel_guard=0; piel_cap=0
    bound=0; tenacity=0; tenacity_new=0; cooldown=0
    burn_turns=0; deb=0; deb_turns=0; def_next=0

    for rnd in range(1,81):
        cyc=(rnd-1)%4
        # actions: 0 basic,1 root,2 defend,3 potion,4 paso,5 piel,6 fil
        if strategy==0: # universal reader
            if cyc<2: act=1
            elif cyc==2: act=2
            else: act=0
        elif strategy==1: # PASO_READER
            if cyc<2: act=1
            elif cyc==2: act=4 if qi>=paso_cost else 2
            else: act=0
        elif strategy==2: # FILAMENTO_READER
            if cyc<2: act=1
            elif cyc==2:
                act=6 if (tenacity<=0 and cooldown<=0 and qi>=fil_cost) else 2
            else: act=0
        else: # PIEL_READER
            if cyc<2: act=1
            elif cyc==2:
                act=1 if piel_cap>0 else (5 if qi>=piel_cost else 2)
            else: act=0

        if hp<=9 and potion: act=3
        if act==1 and qi<root_cost: act=0

        used_fil=0
        if act==3:
            hp=min(PLAYER_MAX_HP,hp+dice(3,6)+6); potion=0
        elif act==2:
            piel_guard=0; piel_cap=0
            def1=np.random.randint(35,51); def2=np.random.randint(25,41)
            qi=min(PLAYER_MAX_QI,qi+3)
        elif act==4:
            qi-=paso_cost; paso_bonus_active=paso_ev; paso_turns=paso_dur
        elif act==5:
            qi-=piel_cost; def1=0; def2=0
            piel_guard=piel_guard_max; piel_cap=piel_cap_max
        elif act==6:
            qi-=fil_cost; used_fil=1; cooldown=1
            r=np.random.randint(1,21)
            ok=(r==20) or (r!=1 and r+patt+fil_ctrl>=boss_def+2)
            if ok:
                bound=1; tenacity=2; tenacity_new=1
                if fil_dm1: bhp-=np.random.randint(1,fil_dm1+1)
                if fil_dm2: bhp-=np.random.randint(1,fil_dm2+1)
        elif act==0:
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and r+patt>=boss_def+def_next)
            if hit:
                dmg=dice(1,8)
                if r==20: dmg=math.ceil(dmg*1.5)
                bhp-=dmg
            def_next=0
        else:
            qi-=root_cost
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and ((r>=critmin) or (r+patt+root_ab>=boss_def+def_next)))
            if hit:
                dmg=dice(nd,fd)+flat+(dice(1,4) if add else 0)
                if r>=critmin: dmg=math.ceil(dmg*1.5)
                bhp-=dmg
                if root_burn: burn_turns=2
                if root_deb: deb=root_deb; deb_turns=root_debdur
            def_next=0

        if bhp<=0: return 1

        if cooldown>0 and not used_fil: cooldown-=1
        if tenacity>0 and not tenacity_new: tenacity-=1
        tenacity_new=0

        if bound>0:
            bound-=1
        else:
            if cyc==3:
                def_next=pata_bonus
            else:
                batt=BOSS_ATTACK+(deb if deb_turns>0 else 0)
                r=np.random.randint(1,21)
                evade_extra=int(np.rint(paso_bonus_active/5.0)) if paso_turns>0 else 0
                hit=(r==20) or (r!=1 and r+batt>=pdef+evade_extra)
                dmg=0
                if hit:
                    dmg=dice(2,6)+2 if cyc==2 else dice(1,6)+2
                    if r==20: dmg=math.ceil(dmg*1.5)
                if dmg>0 and piel_cap>0:
                    absorb=min(dmg,piel_guard,piel_cap)
                    dmg-=absorb; piel_cap-=absorb
                    if piel_cap<=0: piel_guard=0
                elif dmg>0:
                    if def1>0:
                        dmg-=math.floor(dmg*def1/100); def1=def2; def2=0
                    elif def2>0:
                        dmg-=math.floor(dmg*def2/100); def2=0
                hp-=dmg

        if burn_turns>0:
            bhp-=np.random.randint(1,4); burn_turns-=1
            if bhp<=0: return 1
        if deb_turns>0:
            deb_turns-=1
            if deb_turns<=0: deb=0
        if paso_turns>0:
            paso_turns-=1
            if paso_turns<=0: paso_bonus_active=0
        if hp<=0: return 0
    return 0

@njit
def scenario(runs,seed,strategy,root,o1,o2,boss_def,pata_bonus):
    np.random.seed(seed)
    wins=0
    for _ in range(runs):
        wins+=one_duel(strategy,root,o1,o2,boss_def,pata_bonus)
    return wins/runs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs",type=int,default=20_000)
    args=ap.parse_args()
    scenario(3,1,0,0,1,1,13,3) # warm JIT

    rows=[]
    for pata in (2,3,4):
        for strategy,name in STRATEGIES.items():
            for root in range(3):
                for o1 in range(1,4):
                    for o2 in range(1,4):
                        for bdef in (13,14):
                            seed=(pata*100000000+strategy*10000000+(root+1)*1000000+
                                  o1*100000+o2*10000+bdef*10) & 0xffffffff
                            rows.append(dict(
                                pata=pata,strategy=name,root=root,o1=o1,o2=o2,boss_def=bdef,
                                winRate=scenario(args.runs,seed,strategy,root,o1,o2,bdef,pata)
                            ))
    df=pd.DataFrame(rows)
    summary=df.groupby(["pata","strategy","boss_def"]).winRate.agg(["mean","min","max"]).reset_index()
    print(summary.to_string(index=False))
    df.to_csv("grulla_phase1_pata_sensitivity_v0.1.csv",index=False)
    summary.to_csv("grulla_phase1_pata_sensitivity_summary_v0.1.csv",index=False)

if __name__=="__main__":
    main()
