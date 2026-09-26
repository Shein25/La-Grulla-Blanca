# Grulla Blanca — Fase I · sensibilidad anti-absorción de Campanada v0.1
# Ruta alternativa al nerf numérico puro. SOLO laboratorio experimental.
#
# Compara CURRENT y G234_D1 manteniendo PIEL_READER, pero hace que Campanada
# tenga propiedades específicas contra burbujas de Guardia de técnica.
#
# Modos:
# BASELINE          -> Campanada normal.
# PIERCE_50         -> 50% del daño de Campanada atraviesa Piel; el resto puede absorberse.
# OVERLOAD_125      -> si Piel está activa, Campanada hace x1.25 daño antes de absorción.
# OVERLOAD_150      -> si Piel está activa, Campanada hace x1.50 daño antes de absorción.
# SHATTER           -> Campanada conectada ignora Piel y destruye toda su reserva restante.
# PIERCE50_OV125    -> x1.25 daño y 50% atraviesa Piel.
#
# Un fallo no activa ninguna propiedad. DEFENDER no cuenta como Piel y conserva
# su semántica porcentual normal.
#
# Uso:
#   python grulla-phase1-campanada-anti-absorption-v0.1.py --runs 2000

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
PATA_DEF_BONUS=3

MODELS={0:"CURRENT",1:"G234_D1"}
COUNTERS={0:"BASELINE",1:"PIERCE_50",2:"OVERLOAD_125",3:"OVERLOAD_150",4:"SHATTER",5:"PIERCE50_OV125"}

# cfg = p1*4+p2; 0 means no choice.
CONFIGS=[]
for p1,p2 in [(0,0)]+[(a,0) for a in range(1,4)]+[(0,b) for b in range(1,4)]+[(a,b) for a in range(1,4) for b in range(1,4)]:
    CONFIGS.append((p1,p2))

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
def piel_stats(model,p1,p2):
    if model==0: # CURRENT
        base_guard=3; base_dur=2; hard=6; thick=7
    else:        # G234_D1
        base_guard=2; base_dur=1; hard=3; thick=4
    cost=5; guard=base_guard; dur=base_dur
    if p1==1: guard=hard
    elif p1==2: dur+=1
    elif p1==3: cost-=1
    if p2==1: cost-=1
    elif p2==2: guard=thick
    elif p2==3: dur+=1
    cost=max(math.ceil(5*.7),cost)
    return cost,guard,dur,guard*dur

@njit
def apply_campanada_counter(dmg,counter,piel_guard,piel_cap):
    # Devuelve (daño a HP, nueva guardia, nueva reserva)
    if dmg<=0 or piel_cap<=0:
        return dmg,piel_guard,piel_cap

    if counter==4: # SHATTER
        return dmg,0,0

    raw=dmg
    if counter==2:      # x1.25
        raw=math.ceil(raw*1.25)
    elif counter==3:    # x1.50
        raw=math.ceil(raw*1.50)
    elif counter==5:    # x1.25 + pierce 50
        raw=math.ceil(raw*1.25)

    if counter==1 or counter==5:
        bypass=math.ceil(raw*0.5)
        shieldable=raw-bypass
        absorb=min(shieldable,piel_guard,piel_cap)
        newcap=piel_cap-absorb
        return bypass+(shieldable-absorb),(piel_guard if newcap>0 else 0),newcap

    absorb=min(raw,piel_guard,piel_cap)
    newcap=piel_cap-absorb
    return raw-absorb,(piel_guard if newcap>0 else 0),newcap

@njit
def one_duel(model,counter,root,o1,o2,p1,p2,boss_def):
    ratt,rdef,root_cost,nd,fd,flat,root_ab,critmin,add,root_burn,root_deb,root_debdur=root_stats(root,o1,o2)
    piel_cost,piel_guard_max,piel_dur,piel_cap_max=piel_stats(model,p1,p2)
    patt=1+ratt+3+GEAR_ATTACK
    pdef=10+rdef+GEAR_DEFENSE

    hp=PLAYER_MAX_HP; qi=PLAYER_MAX_QI; bhp=BOSS_HP; potion=1
    def1=0; def2=0
    piel_guard=0; piel_cap=0
    burn_turns=0; deb=0; deb_turns=0; def_next=0

    for rnd in range(1,81):
        cyc=(rnd-1)%4
        # PIEL_READER ya validado.
        if cyc<2: act=1
        elif cyc==2:
            act=1 if piel_cap>0 else (5 if qi>=piel_cost else 2)
        else: act=0
        if hp<=9 and potion: act=3
        if act==1 and qi<root_cost: act=0

        if act==3:
            hp=min(PLAYER_MAX_HP,hp+dice(3,6)+6); potion=0
        elif act==2:
            piel_guard=0; piel_cap=0
            def1=np.random.randint(35,51); def2=np.random.randint(25,41)
            qi=min(PLAYER_MAX_QI,qi+3)
        elif act==5:
            qi-=piel_cost; def1=0; def2=0
            piel_guard=piel_guard_max; piel_cap=piel_cap_max
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

        if cyc==3:
            def_next=PATA_DEF_BONUS
        else:
            batt=BOSS_ATTACK+(deb if deb_turns>0 else 0)
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and r+batt>=pdef)
            dmg=0
            if hit:
                dmg=dice(2,6)+2 if cyc==2 else dice(1,6)+2
                if r==20: dmg=math.ceil(dmg*1.5)

            if dmg>0 and piel_cap>0:
                if cyc==2:
                    dmg,piel_guard,piel_cap=apply_campanada_counter(dmg,counter,piel_guard,piel_cap)
                else:
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
        if hp<=0: return 0
    return 0

@njit
def scenario(runs,seed,model,counter,root,o1,o2,p1,p2,boss_def):
    np.random.seed(seed)
    wins=0
    for _ in range(runs):
        wins+=one_duel(model,counter,root,o1,o2,p1,p2,boss_def)
    return wins/runs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs",type=int,default=2000)
    args=ap.parse_args()
    scenario(3,1,0,0,0,1,1,0,0,13)

    rows=[]
    for model in range(2):
      for counter in range(6):
       for p1,p2 in CONFIGS:
        for root in range(3):
         for o1 in range(1,4):
          for o2 in range(1,4):
           for bdef in (13,14):
            seed=(model*1000000000+counter*100000000+(p1*4+p2)*1000000+
                  (root+1)*100000+o1*10000+o2*1000+bdef*10) & 0xffffffff
            rows.append(dict(
                model=MODELS[model],counter=COUNTERS[counter],p1=p1,p2=p2,
                root=root,o1=o1,o2=o2,boss_def=bdef,
                winRate=scenario(args.runs,seed,model,counter,root,o1,o2,p1,p2,bdef)
            ))
    df=pd.DataFrame(rows)
    cfg=df.groupby(["model","counter","p1","p2","boss_def"]).winRate.agg(["mean","min","max"]).reset_index()
    best=(cfg.sort_values(["model","counter","boss_def","mean"],ascending=[True,True,True,False])
            .groupby(["model","counter","boss_def"],as_index=False).first())
    print("\n=== MEJOR CONFIGURACIÓN POR MODELO / COUNTER / DEF ===")
    print(best.to_string(index=False))
    df.to_csv("grulla_phase1_campanada_anti_absorption_v0.1.csv",index=False)
    cfg.to_csv("grulla_phase1_campanada_anti_absorption_configs_v0.1.csv",index=False)
    best.to_csv("grulla_phase1_campanada_anti_absorption_best_v0.1.csv",index=False)

if __name__=="__main__":
    main()
