# Grulla Blanca — Fase II-A · toolkit mínimo · Monte Carlo reproducible
# SOLO Fase II — LAS ALAS RECUERDAN. No Fase III.
#
# Objetivo:
# - HP Fase II = 100 (baseline restaurado 150/100/50)
# - cerebro adaptativo = lógica de grulla-boss-brain-v0.1.mjs
# - toolkit jugador = raíz + BASIC + DEFENDER + 1 poción
# - comparar tres perfiles numéricos cercanos sin declararlos canónicos.
#
# Perfiles:
# SAME   : ATQ 4, DEF 13, Golpe 1d6+2
# DAMAGE : ATQ 4, DEF 13, Golpe 1d6+3
# ATTACK : ATQ 5, DEF 13, Golpe 1d6+2
#
# FX provisionales heredados del benchmark histórico:
# Tormenta      +3 ATQ, 2d6+3, drena 2 qi si hace daño
# Cerrar Alas   absorción 4 / reserva 8
# Recordar Filo +20 Esquiva contra la siguiente ofensiva
# Eco Meridiano drena 4 qi
#
# Estrategias:
# SPAM               misma técnica; entra con counter heredado de Fase I
# SPAM_DEFENSE       misma técnica + DEFENDER ante Tormenta; counter heredado
# ALTERNATE          raíz/BASIC alternados
# READER             lee Recordar/Eco/Tormenta y evita repetir técnica
#
# Uso:
#   python grulla-phase2-minimal-grid-v0.1.py --runs 5000

import argparse, math
import numpy as np
import pandas as pd
from numba import njit

PLAYER_HP=28
PLAYER_QI=110
GEAR_ATK=2
GEAR_DEF=7
BOSS_HP=100

PROFILES={
  0:("SAME",4,13,2),
  1:("DAMAGE",4,13,3),
  2:("ATTACK",5,13,2),
}
STRATEGIES={0:"SPAM",1:"SPAM_DEFENSE",2:"ALTERNATE",3:"READER"}

# intents
GOLPE=0
TORMENTA=1
CERRAR=2
RECORDAR=3
ECO=4

@njit
def dice(n,f):
    s=0
    for _ in range(n): s+=np.random.randint(1,f+1)
    return s

@njit
def root_stats(root,o1,o2):
    if root==0: # fuego
        ratt=1; rdef=0; basecost=7; nd=2; fd=6; flat=2
    elif root==1: # metal
        ratt=2; rdef=0; basecost=6; nd=1; fd=10; flat=3
    else: # agua
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
    cost=max(math.ceil(basecost*.7),cost-1) # afinidad: -1 adicional
    return ratt,rdef,cost,nd,fd,flat+1,ab,crit,add,burn,deba,debdur

@njit
def hit_roll(atk,defense,crit_min=20,eva_bonus=0):
    r=np.random.randint(1,21)
    if r==1: return 0,0
    crit=1 if r>=crit_min else 0
    if r==20 or crit: return 1,crit
    extra=max(0,int(np.rint(eva_bonus/5.0)))
    return (1 if r+atk>=defense+extra else 0),0

@njit
def intent_recent(recent,a,depth):
    n=len(recent)
    start=max(0,n-depth)
    for i in range(start,n):
        if recent[i]==a: return 1
    return 0

@njit
def choose_intent(hist_type,hist_tech,hist_elem,hist_qi,hist_band,hist_n,
                  recent,recent_n,php,pqi,bhp,rng_noise):
    # últimas 2/3 acciones
    t1=hist_type[hist_n-1] if hist_n>=1 else -1
    t2=hist_type[hist_n-2] if hist_n>=2 else -1
    tech1=hist_tech[hist_n-1] if hist_n>=1 else -1
    tech2=hist_tech[hist_n-2] if hist_n>=2 else -1
    elem1=hist_elem[hist_n-1] if hist_n>=1 else -1
    elem2=hist_elem[hist_n-2] if hist_n>=2 else -1
    qi1=hist_qi[hist_n-1] if hist_n>=1 else 0
    qi2=hist_qi[hist_n-2] if hist_n>=2 else 0

    tech_repeat=hist_n>=2 and tech1>=0 and tech1==tech2
    elem_repeat=hist_n>=2 and elem1>=0 and elem1==elem2
    offense_streak=hist_n>=2 and t1<=2 and t2<=2  # BASIC/TECH/CONTROL enc. 0..2
    qi_streak=hist_n>=2 and qi1>0 and qi2>0

    control_recent=0; heavy_recent=0
    for k in range(max(0,hist_n-3),hist_n):
        if hist_type[k]==2: control_recent=1
    for k in range(max(0,hist_n-2),hist_n):
        if hist_band[k]>=2: heavy_recent=1

    recover_recent=(hist_n>=1 and t1==4) or (hist_n>=2 and t2==4)
    player_low=php<=.30
    self_low=bhp<=.30
    qi_low=pqi<=.25
    qi_high=pqi>=.65

    inherited_repeat=1 if (hist_n>=1 and tech1==0) else 0 # raíz dominante heredada de Fase I

    scores=np.empty(5,np.float64)
    jit=np.array([1.0,1.0,.8,.6,.6])
    scores[GOLPE]=30
    scores[TORMENTA]=28+(12 if qi_high else 0)+(10 if player_low else 0)-(40 if intent_recent(recent[:recent_n],TORMENTA,2) else 0)
    scores[CERRAR]=18+(18 if offense_streak else 0)+(20 if heavy_recent else 0)+(16 if self_low else 0)-(35 if intent_recent(recent[:recent_n],CERRAR,2) else 0)+(8 if control_recent else 0)
    scores[RECORDAR]=12+(38 if tech_repeat else 0)+(18 if elem_repeat else 0)+inherited_repeat*8-(42 if intent_recent(recent[:recent_n],RECORDAR,2) else 0)
    scores[ECO]=12+(34 if qi_streak else 0)+(8 if qi_low else 0)+(6 if recover_recent else 0)-(40 if intent_recent(recent[:recent_n],ECO,2) else 0)

    best=0; bestv=-1e9
    for i in range(5):
        v=scores[i]+(rng_noise[i]-.5)*jit[i]
        if v>bestv:
            bestv=v; best=i
    return best

@njit
def duel(profile,strategy,root,o1,o2,seed):
    np.random.seed(seed)
    ratt,rdef,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd=root_stats(root,o1,o2)
    # profile mapping
    if profile==0: bat=4; bdef=13; bflat=2
    elif profile==1: bat=4; bdef=13; bflat=3
    else: bat=5; bdef=13; bflat=2

    patt=1+ratt+3+GEAR_ATK
    pdef=10+rdef+GEAR_DEF

    hp=PLAYER_HP; qi=PLAYER_QI; bhp=BOSS_HP; potion=1
    guard1=0; guard2=0
    reserve=0; evade_next=0
    burn_turns=0; deb=0; debturn=0

    # counter: SPAM/SPAM_DEFENSE heredaron dependencia exclusiva de Fase I.
    locked=1 if strategy<=1 else 0

    # history encodings: type BASIC=0 TECH=1 CONTROL=2 DEFEND=3 RECOVER=4
    ht=np.full(8,-1,np.int8); htech=np.full(8,-1,np.int8); helem=np.full(8,-1,np.int8)
    hqi=np.zeros(8,np.int16); hband=np.zeros(8,np.int8); hn=0
    recent=np.full(4,-1,np.int8); rn=0

    for rnd in range(1,81):
        if bhp<=0: return 1,rnd-1,hp,qi,locked
        if hp<=0: return 0,rnd-1,0,qi,locked

        noise=np.random.random(5)
        intent=choose_intent(ht,htech,helem,hqi,hband,hn,recent,rn,hp/PLAYER_HP,qi/PLAYER_QI,bhp/BOSS_HP,noise)

        # action enc: BASIC0 TECH1 DEFEND3 RECOVER4
        if strategy==0: # SPAM
            act=1 if qi>=tcost else 3
        elif strategy==1: # spam + defense contra Tormenta
            act=3 if intent==TORMENTA else (1 if qi>=tcost else 3)
        elif strategy==2: # alternate
            if hp<=8 and potion: act=4
            else: act=1 if rnd%2==1 and qi>=tcost else 0
        else: # reader
            if hp<=9 and potion:
                act=4
            elif locked or intent==RECORDAR or intent==ECO:
                act=0
            elif intent==TORMENTA and hp<=17:
                act=3
            else:
                # no dos técnicas raíz consecutivas
                lasttech=htech[hn-1] if hn>0 else -1
                act=1 if qi>=tcost and lasttech!=0 else 0

        band=0; qspent=0; techid=-1; elem=-1

        if act==4:
            hp=min(PLAYER_HP,hp+dice(3,6)+6); potion=0
        elif act==3:
            guard1=np.random.randint(35,51); guard2=np.random.randint(25,41)
            qi=min(PLAYER_QI,qi+3)
        elif act==0:
            hit,crit=hit_roll(patt,bdef,20,evade_next)
            dmg=0
            if hit:
                dmg=dice(1,8)
                if crit: dmg=math.ceil(dmg*1.5)
                if reserve>0:
                    a=min(dmg,4,reserve); dmg-=a; reserve-=a
                bhp-=dmg
                band=2 if dmg>=8 else 1
            evade_next=0
            # BASIC rompe counter activo
            if locked: locked=0
        else:
            qspent=tcost; techid=0; elem=root
            qi-=tcost
            # tercera repetición todavía resuelve; sólo repetición posterior queda bloqueada.
            if not locked:
                hit,crit=hit_roll(patt+tab,bdef,tcrit,evade_next)
                dmg=0
                if hit:
                    dmg=dice(nd,fd)+tflat+(dice(1,4) if add else 0)
                    if crit: dmg=math.ceil(dmg*1.5)
                    if reserve>0:
                        a=min(dmg,4,reserve); dmg-=a; reserve-=a
                    bhp-=dmg
                    band=2 if dmg>=8 else 1
                    if dmg>0 and rburn: burn_turns=2
                    if dmg>0 and rdeb: deb=rdeb; debturn=rdebd
            evade_next=0

        # append action to history before evaluating next counter, but boss intent stays committed.
        if hn<8:
            pos=hn; hn+=1
        else:
            ht[:-1]=ht[1:]; htech[:-1]=htech[1:]; helem[:-1]=helem[1:]; hqi[:-1]=hqi[1:]; hband[:-1]=hband[1:]
            pos=7
        ht[pos]=act; htech[pos]=techid; helem[pos]=elem; hqi[pos]=qspent; hband[pos]=band

        # lock normal de Fase II: 3 usos consecutivos misma técnica.
        if locked:
            # DEFEND/RECOVER no borran. BASIC ya borró arriba.
            pass
        elif hn>=3 and htech[hn-1]==0 and htech[hn-2]==0 and htech[hn-3]==0:
            locked=1

        if bhp<=0:
            return 1,rnd,hp,qi,locked

        # resolve committed boss intent
        if intent==GOLPE:
            hit,crit=hit_roll(bat+(deb if debturn>0 else 0),pdef)
            dmg=0
            if hit:
                dmg=dice(1,6)+bflat
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100); guard1=guard2; guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100); guard2=0
            hp-=dmg
        elif intent==TORMENTA:
            hit,crit=hit_roll(bat+3+(deb if debturn>0 else 0),pdef)
            dmg=0
            if hit:
                dmg=dice(2,6)+3
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100); guard1=guard2; guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100); guard2=0
            hp-=dmg
            if dmg>0: qi=max(0,qi-2)
        elif intent==CERRAR:
            reserve=8
        elif intent==RECORDAR:
            evade_next=20
        else: # ECO
            qi=max(0,qi-4)

        if burn_turns>0 and bhp>0:
            bhp-=np.random.randint(1,4); burn_turns-=1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0

        # recent intents
        if rn<4:
            recent[rn]=intent; rn+=1
        else:
            recent[:-1]=recent[1:]; recent[3]=intent

    return (1 if bhp<=0 and hp>0 else 0),80,max(0,hp),qi,locked

@njit
def scenario(runs,seed,profile,strategy,root,o1,o2):
    np.random.seed(seed)
    wins=0; rounds=0; hp=0; qi=0; locks=0
    for i in range(runs):
        # duel reseedea para reproducibilidad por duelo
        z=duel(profile,strategy,root,o1,o2,seed+i*7919+17)
        wins+=z[0]; rounds+=z[1]; hp+=z[2]; qi+=z[3]; locks+=z[4]
    return wins/runs,rounds/runs,hp/runs,qi/runs,locks/runs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs",type=int,default=5000)
    args=ap.parse_args()
    duel(0,2,0,1,1,1) # JIT warmup

    rows=[]
    for profile in range(3):
      for strategy in range(4):
       for root in range(3):
        for o1 in range(1,4):
         for o2 in range(1,4):
          seed=(profile+1)*100000000+(strategy+1)*10000000+(root+1)*1000000+o1*10000+o2*100
          w,rr,h,q,l=scenario(args.runs,seed,profile,strategy,root,o1,o2)
          rows.append(dict(profile=PROFILES[profile][0],strategy=STRATEGIES[strategy],root=root,o1=o1,o2=o2,
                           winRate=w,avgRounds=rr,avgHp=h,avgQi=q,lockEndRate=l))
    df=pd.DataFrame(rows)
    summary=df.groupby(["profile","strategy","root"]).winRate.agg(["mean","min","max"]).reset_index()
    global_summary=df.groupby(["profile","strategy"]).winRate.agg(["mean","min","max"]).reset_index()
    print("\n=== GLOBAL ===")
    print(global_summary.to_string(index=False))
    print("\n=== POR RAIZ ===")
    print(summary.to_string(index=False))
    print("\n=== INVARIANTES ===")
    for p in PROFILES.values():
        z=df[df.profile==p[0]]
        print(p[0],
              "SPAM_ZERO",bool((z[z.strategy=="SPAM"].winRate==0).all()),
              "SPAM_DEF_ZERO",bool((z[z.strategy=="SPAM_DEFENSE"].winRate==0).all()))
    df.to_csv("grulla_phase2_minimal_grid_v0.1.csv",index=False)
    summary.to_csv("grulla_phase2_minimal_grid_roots_v0.1.csv",index=False)
    global_summary.to_csv("grulla_phase2_minimal_grid_global_v0.1.csv",index=False)

if __name__=="__main__":
    main()
