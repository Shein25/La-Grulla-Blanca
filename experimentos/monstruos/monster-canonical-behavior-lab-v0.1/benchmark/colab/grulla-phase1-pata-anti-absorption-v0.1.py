# Grulla Blanca — Fase I · Pata Inmóvil prepara golpe anti-absorción v0.1
# SOLO laboratorio experimental. No Fase II/III.
#
# Mecánica:
# - Pata Inmóvil conserva +3 DEF contra la siguiente ofensiva del jugador.
# - además prepara el siguiente Golpe de Ala;
# - si ese golpe conecta mientras Piel de Cobre está activa, aplica el counter elegido;
# - el counter se consume aunque el golpe falle (el ataque especial ya ocurrió).
#
# Modelos de Piel:
# CURRENT  = base G3 D2 / Endurecido6 / Grueso7
# G345_D1  = base G3 D1 / Endurecido4 / Grueso5
# G234_D1  = base G2 D1 / Endurecido3 / Grueso4
#
# Counters:
# BASELINE
# OVERLOAD_125
# OVERLOAD_150
# PIERCE_50
# SHATTER
# PIERCE50_OV150
#
# Uso:
# python grulla-phase1-pata-anti-absorption-v0.1.py --model G345_D1 --counter OVERLOAD_150 --mode grid --runs 5000
# python grulla-phase1-pata-anti-absorption-v0.1.py --model G345_D1 --counter OVERLOAD_150 --mode confirm --runs 20000 --finalists 2-2,1-3,3-2\n# python grulla-phase1-pata-anti-absorption-v0.1.py --model G345_D1 --counter OVERLOAD_175 --mode confirm --runs 20000 --finalists 2-2

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
READER_BASELINE={13:0.609,14:0.547}

MODEL_NAMES=["CURRENT","G345_D1","G234_D1"]
COUNTER_NAMES=["BASELINE","OVERLOAD_125","OVERLOAD_150","PIERCE_50","SHATTER","PIERCE50_OV150","OVERLOAD_175"]

CONFIGS=[(0,0)]+[(a,0) for a in range(1,4)]+[(0,b) for b in range(1,4)]+[(a,b) for a in range(1,4) for b in range(1,4)]

N1={0:"—",1:"Cobre endurecido",2:"Cobre flexible",3:"Cobre sobrio"}
N2={0:"—",1:"Aliento económico",2:"Cobre grueso",3:"Placas continuas"}

@njit
def dice(n,f):
    s=0
    for _ in range(n): s+=np.random.randint(1,f+1)
    return s

@njit
def root_stats(root,o1,o2):
    if root==0: ratt=1; rdef=0; basecost=7; nd=2; fd=6; flat=2
    elif root==1: ratt=2; rdef=0; basecost=6; nd=1; fd=10; flat=3
    else: ratt=0; rdef=2; basecost=6; nd=2; fd=6; flat=0
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
    if model==0:
        base_guard=3; base_dur=2; hard=6; thick=7
    elif model==1:
        base_guard=3; base_dur=1; hard=4; thick=5
    else:
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
def apply_counter(dmg,counter,guard,cap):
    if dmg<=0 or cap<=0:
        return dmg,guard,cap
    if counter==4: # SHATTER
        return dmg,0,0

    raw=dmg
    if counter==1: raw=math.ceil(raw*1.25)
    elif counter==2: raw=math.ceil(raw*1.50)
    elif counter==5: raw=math.ceil(raw*1.50)\n    elif counter==6: raw=math.ceil(raw*1.75)

    if counter==3 or counter==5:
        bypass=math.ceil(raw*0.5)
        shieldable=raw-bypass
        absorb=min(shieldable,guard,cap)
        cap-=absorb
        return bypass+(shieldable-absorb),(guard if cap>0 else 0),cap

    absorb=min(raw,guard,cap)
    cap-=absorb
    return raw-absorb,(guard if cap>0 else 0),cap

@njit
def duel(model,counter,root,o1,o2,p1,p2,boss_def):
    ratt,rdef,root_cost,nd,fd,flat,root_ab,critmin,add,root_burn,root_deb,root_debdur=root_stats(root,o1,o2)
    piel_cost,pgmax,pdur,pcapmax=piel_stats(model,p1,p2)
    patt=1+ratt+3+GEAR_ATTACK
    pdef=10+rdef+GEAR_DEFENSE

    hp=PLAYER_MAX_HP; qi=PLAYER_MAX_QI; bhp=BOSS_HP; potion=1
    def1=0; def2=0
    pguard=0; pcap=0
    burn=0; deb=0; debturn=0; defnext=0
    anti_next=0

    for rnd in range(1,81):
        cyc=(rnd-1)%4

        # PIEL_READER cerrado.
        if cyc<2: act=1
        elif cyc==2: act=1 if pcap>0 else (5 if qi>=piel_cost else 2)
        else: act=0

        if hp<=9 and potion: act=3
        if act==1 and qi<root_cost: act=0

        if act==3:
            hp=min(PLAYER_MAX_HP,hp+dice(3,6)+6); potion=0
        elif act==2:
            pguard=0; pcap=0
            def1=np.random.randint(35,51); def2=np.random.randint(25,41)
            qi=min(PLAYER_MAX_QI,qi+3)
        elif act==5:
            qi-=piel_cost
            def1=0; def2=0
            pguard=pgmax; pcap=pcapmax
        elif act==0:
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and r+patt>=boss_def+defnext)
            if hit:
                d=dice(1,8)
                if r==20: d=math.ceil(d*1.5)
                bhp-=d
            defnext=0
        else:
            qi-=root_cost
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and ((r>=critmin) or (r+patt+root_ab>=boss_def+defnext)))
            if hit:
                d=dice(nd,fd)+flat+(dice(1,4) if add else 0)
                if r>=critmin: d=math.ceil(d*1.5)
                bhp-=d
                if root_burn: burn=2
                if root_deb: deb=root_deb; debturn=root_debdur
            defnext=0

        if bhp<=0: return 1

        if cyc==3:
            defnext=PATA_DEF_BONUS
            anti_next=1
        else:
            batt=BOSS_ATTACK+(deb if debturn>0 else 0)
            r=np.random.randint(1,21)
            hit=(r==20) or (r!=1 and r+batt>=pdef)
            d=0
            if hit:
                d=dice(2,6)+2 if cyc==2 else dice(1,6)+2
                if r==20: d=math.ceil(d*1.5)

            if d>0 and pcap>0:
                if anti_next:
                    d,pguard,pcap=apply_counter(d,counter,pguard,pcap)
                else:
                    absorb=min(d,pguard,pcap)
                    d-=absorb; pcap-=absorb
                    if pcap<=0: pguard=0
            elif d>0:
                if def1>0:
                    d-=math.floor(d*def1/100); def1=def2; def2=0
                elif def2>0:
                    d-=math.floor(d*def2/100); def2=0
            hp-=d

            # El golpe preparado se consume aunque falle.
            if cyc==0 and anti_next:
                anti_next=0

        if burn>0:
            bhp-=np.random.randint(1,4); burn-=1
            if bhp<=0: return 1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0
        if hp<=0: return 0
    return 0

@njit
def scenario(runs,seed,model,counter,root,o1,o2,p1,p2,boss_def):
    np.random.seed(seed)
    wins=0
    for _ in range(runs):
        wins+=duel(model,counter,root,o1,o2,p1,p2,boss_def)
    return wins/runs

def parse_cfgs(raw):
    out=[]
    for x in (raw or "").split(","):
        if not x.strip(): continue
        a,b=map(int,x.split("-"))
        if (a,b) not in CONFIGS: raise ValueError(x)
        out.append((a,b))
    return out

def cfg_name(p1,p2):
    if p1 and p2: return f"{N1[p1]} + {N2[p2]}"
    if p1: return N1[p1]
    if p2: return N2[p2]
    return "Piel base"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--model",choices=MODEL_NAMES,required=True)
    ap.add_argument("--counter",choices=COUNTER_NAMES,required=True)
    ap.add_argument("--mode",choices=("grid","confirm"),default="grid")
    ap.add_argument("--runs",type=int,default=None)
    ap.add_argument("--finalists",default="")
    args=ap.parse_args()

    model=MODEL_NAMES.index(args.model)
    counter=COUNTER_NAMES.index(args.counter)
    configs=CONFIGS if args.mode=="grid" else parse_cfgs(args.finalists)
    if not configs: raise SystemExit("confirm requiere --finalists")
    runs=args.runs or (5000 if args.mode=="grid" else 20000)

    scenario(2,1,model,counter,0,1,1,0,0,13)
    rows=[]
    for p1,p2 in configs:
      pcost,pguard,pdur,pcap=piel_stats(model,p1,p2)
      for root in range(3):
       for o1 in range(1,4):
        for o2 in range(1,4):
         for bdef in (13,14):
          seed=(model*1000000000+counter*100000000+(p1*4+p2)*1000000+
                (root+1)*100000+o1*10000+o2*1000+bdef*10+
                (50000000 if args.mode=="confirm" else 0)) & 0xffffffff
          rows.append(dict(
              model=args.model,counter=args.counter,p1=p1,p2=p2,
              name=cfg_name(p1,p2),cost=pcost,guard=pguard,duration=pdur,capacity=pcap,
              root=root,o1=o1,o2=o2,boss_def=bdef,
              winRate=scenario(runs,seed,model,counter,root,o1,o2,p1,p2,bdef)
          ))

    df=pd.DataFrame(rows)
    cfg=df.groupby(["p1","p2","name","cost","guard","duration","capacity","boss_def"]).winRate.agg(["mean","min","max"]).reset_index()
    print(cfg.sort_values(["boss_def","mean"],ascending=[True,False]).to_string(index=False))
    suffix=f"{args.model}_{args.counter}_{args.mode}"
    df.to_csv(f"grulla_phase1_pata_anti_absorption_{suffix}_v0.1.csv",index=False)
    cfg.to_csv(f"grulla_phase1_pata_anti_absorption_{suffix}_configs_v0.1.csv",index=False)

if __name__=="__main__":
    main()
