# Grulla Blanca — cadena Fase I -> II -> III · M_A reproducible v0.1
# Fase I y Fase II congeladas. Fase III M_A en validación.
# No modifica stats/cerebro de las fases cerradas.
#
# Mide:
# - llegada a Fase II;
# - HP/QI/poción de entrada;
# - victoria condicional de Fase II;
# - victoria total I+II;
# - anti-spam heredado.
#
# Uso:
#   python grulla-phase12-chain-v0.1.py --runs 5000

import argparse, math
import numpy as np
import pandas as pd
from numba import njit

MAX_HP=28
MAX_QI=110
GEAR_ATK=2
GEAR_DEF=7

# estrategias
SPAM=0
SPAM_DEF=1
ALTERNATE=2
READER=3
STRATEGY_NAMES={0:"SPAM",1:"SPAM_DEFENSE",2:"ALTERNATE",3:"READER"}

# FX Fase II
TACT_C=0
TACT_D=1
CHAIN_A=2
CHAIN_B=3
CHAIN_C=4
FX_NAMES={0:"TACT_C",1:"TACT_D",2:"CHAIN_A",3:"CHAIN_B",4:"CHAIN_C"}

# intents Fase II
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
def hit_roll(atk,defense,crit_min=20,eva_bonus=0):
    r=np.random.randint(1,21)
    if r==1: return 0,0
    crit=1 if r>=crit_min else 0
    if r==20 or crit: return 1,crit
    extra=max(0,int(np.rint(eva_bonus/5.0)))
    return (1 if r+atk>=defense+extra else 0),0

@njit
def apply_player_attack(act,locked,root,patt,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd,
                        bdef,def_next,evade_next,reserve,reserve_per,qi,bhp,burn_turns,deb,debturn):
    qspent=0; techid=-1; elem=-1; band=0
    if act==0: # BASIC
        hit,crit=hit_roll(patt,bdef+def_next,20,evade_next)
        dmg=0
        if hit:
            dmg=dice(1,8)
            if crit: dmg=math.ceil(dmg*1.5)
            if reserve>0:
                a=min(dmg,reserve_per,reserve); dmg-=a; reserve-=a
            bhp-=dmg; band=2 if dmg>=8 else 1
        locked=0
    else: # TECH
        qspent=tcost; techid=0; elem=root; qi-=tcost
        if not locked:
            hit,crit=hit_roll(patt+tab,bdef+def_next,tcrit,evade_next)
            dmg=0
            if hit:
                dmg=dice(nd,fd)+tflat+(dice(1,4) if add else 0)
                if crit: dmg=math.ceil(dmg*1.5)
                if reserve>0:
                    a=min(dmg,reserve_per,reserve); dmg-=a; reserve-=a
                bhp-=dmg; band=2 if dmg>=8 else 1
                if dmg>0 and rburn: burn_turns=2
                if dmg>0 and rdeb: deb=rdeb; debturn=rdebd
    return locked,qi,bhp,burn_turns,deb,debturn,reserve,qspent,techid,elem,band

@njit
def phase1(strategy,root,o1,o2,seed):
    np.random.seed(seed)
    ratt,rdef,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd=root_stats(root,o1,o2)
    patt=1+ratt+3+GEAR_ATK
    pdef=10+rdef+GEAR_DEF
    hp=MAX_HP; qi=MAX_QI; potion=1; bhp=150
    guard1=0; guard2=0
    burn_turns=0; deb=0; debturn=0; def_next=0
    tech_uses=0; basic_uses=0

    for rnd in range(1,81):
        if bhp<=0 or hp<=0: break
        cyc=(rnd-1)%4

        if strategy==SPAM:
            # PURE_SINGLE_SKILL: si no alcanza el qi, defiende; nunca usa BASIC.
            act=1 if qi>=tcost else 2
        elif strategy==SPAM_DEF:
            act=2 if cyc==2 else (1 if qi>=tcost else 0)
        elif strategy==ALTERNATE:
            if hp<=8 and potion: act=3
            else: act=1 if rnd%2==1 and qi>=tcost else 0
        else: # READER Fase I cerrada
            if hp<=9 and potion: act=3
            elif cyc==2: act=2
            elif cyc==3: act=0
            else: act=1 if qi>=tcost else 0

        if act==3:
            hp=min(MAX_HP,hp+dice(3,6)+6); potion=0
        elif act==2:
            guard1=np.random.randint(35,51); guard2=np.random.randint(25,41)
            qi=min(MAX_QI,qi+3)
        else:
            if act==1: tech_uses+=1
            else: basic_uses+=1
            z=apply_player_attack(act,0,root,patt,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd,
                                  13,def_next,0,0,4,qi,bhp,burn_turns,deb,debturn)
            _,qi,bhp,burn_turns,deb,debturn,_,_,_,_,_=z
            def_next=0

        if bhp<=0: break

        if cyc==3:
            def_next=3
        else:
            bat=4+(deb if debturn>0 else 0)
            hit,crit=hit_roll(bat,pdef)
            dmg=0
            if hit:
                if cyc==2: dmg=dice(2,6)+2
                else: dmg=dice(1,6)+2
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100); guard1=guard2; guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100); guard2=0
            hp-=dmg

        if burn_turns>0 and bhp>0:
            bhp-=np.random.randint(1,4); burn_turns-=1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0

    reached=1 if bhp<=0 and hp>0 else 0
    inherited_lock=1 if reached and tech_uses>=2 and basic_uses==0 else 0
    return reached,max(0,hp),qi,potion,guard1,guard2,inherited_lock

@njit
def intent_recent(recent,rn,a,depth):
    for i in range(max(0,rn-depth),rn):
        if recent[i]==a: return 1
    return 0

@njit
def choose_phase2_intent(ht,htech,helem,hqi,hband,hn,recent,rn,php,pqi,bhp):
    t1=ht[hn-1] if hn>=1 else -1
    t2=ht[hn-2] if hn>=2 else -1
    tech1=htech[hn-1] if hn>=1 else -1
    tech2=htech[hn-2] if hn>=2 else -1
    elem1=helem[hn-1] if hn>=1 else -1
    elem2=helem[hn-2] if hn>=2 else -1
    qi1=hqi[hn-1] if hn>=1 else 0
    qi2=hqi[hn-2] if hn>=2 else 0

    tech_repeat=hn>=2 and tech1>=0 and tech1==tech2
    elem_repeat=hn>=2 and elem1>=0 and elem1==elem2
    offense_streak=hn>=2 and t1<=2 and t2<=2
    qi_streak=hn>=2 and qi1>0 and qi2>0
    heavy_recent=0
    for k in range(max(0,hn-2),hn):
        if hband[k]>=2: heavy_recent=1
    recover_recent=(hn>=1 and t1==4) or (hn>=2 and t2==4)
    inherited_repeat=1 if hn>=1 and tech1==0 else 0

    scores=np.empty(5,np.float64)
    jit=np.array([1.0,1.0,.8,.6,.6])
    scores[GOLPE]=30
    scores[TORMENTA]=28+(12 if pqi>=.65 else 0)+(10 if php<=.30 else 0)-(40 if intent_recent(recent,rn,TORMENTA,2) else 0)
    scores[CERRAR]=18+(18 if offense_streak else 0)+(20 if heavy_recent else 0)+(16 if bhp<=.30 else 0)-(35 if intent_recent(recent,rn,CERRAR,2) else 0)
    scores[RECORDAR]=12+(38 if tech_repeat else 0)+(18 if elem_repeat else 0)+inherited_repeat*8-(42 if intent_recent(recent,rn,RECORDAR,2) else 0)
    scores[ECO]=12+(34 if qi_streak else 0)+(8 if pqi<=.25 else 0)+(6 if recover_recent else 0)-(40 if intent_recent(recent,rn,ECO,2) else 0)

    best=0; bestv=-1e9
    for i in range(5):
        v=scores[i]+(np.random.random()-.5)*jit[i]
        if v>bestv:
            bestv=v; best=i
    return best

@njit
def phase2(fx,strategy,root,o1,o2,seed,hp,qi,potion,guard1,guard2,locked):
    np.random.seed(seed)
    ratt,rdef,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd=root_stats(root,o1,o2)
    patt=1+ratt+3+GEAR_ATK
    pdef=10+rdef+GEAR_DEF
    bhp=100
    bat=4; bdef=13

    if fx==TACT_C:
        basic_n=1; basic_f=6; basic_flat=2
        storm_ab=1; storm_n=2; storm_f=6; storm_flat=2; storm_drain=1
        close_guard=3; close_cap=6; remember_eva=10; eco_drain=3
    elif fx==TACT_D:
        basic_n=1; basic_f=6; basic_flat=2
        storm_ab=2; storm_n=1; storm_f=8; storm_flat=3; storm_drain=1
        close_guard=3; close_cap=6; remember_eva=15; eco_drain=3
    elif fx==CHAIN_A:
        basic_n=1; basic_f=4; basic_flat=0
        storm_ab=0; storm_n=1; storm_f=6; storm_flat=1; storm_drain=1
        close_guard=3; close_cap=6; remember_eva=10; eco_drain=3
    elif fx==CHAIN_B:
        basic_n=1; basic_f=3; basic_flat=1
        storm_ab=0; storm_n=1; storm_f=6; storm_flat=1; storm_drain=1
        close_guard=3; close_cap=6; remember_eva=10; eco_drain=3
    else:
        basic_n=1; basic_f=4; basic_flat=1
        storm_ab=0; storm_n=1; storm_f=6; storm_flat=1; storm_drain=1
        close_guard=3; close_cap=6; remember_eva=10; eco_drain=3

    reserve=0; evade_next=0
    burn_turns=0; deb=0; debturn=0

    ht=np.full(8,-1,np.int8); htech=np.full(8,-1,np.int8); helem=np.full(8,-1,np.int8)
    hqi=np.zeros(8,np.int16); hband=np.zeros(8,np.int8); hn=0
    recent=np.full(4,-1,np.int8); rn=0

    for rnd in range(1,81):
        if bhp<=0 or hp<=0: break
        intent=choose_phase2_intent(ht,htech,helem,hqi,hband,hn,recent,rn,hp/MAX_HP,qi/MAX_QI,bhp/100)

        if strategy==SPAM:
            act=1 if qi>=tcost else 2
        elif strategy==SPAM_DEF:
            act=2 if intent==TORMENTA else (1 if qi>=tcost else 2)
        elif strategy==ALTERNATE:
            if hp<=8 and potion: act=3
            else: act=1 if rnd%2==1 and qi>=tcost else 0
        else:
            if hp<=9 and potion:
                act=3
            elif locked or evade_next>0 or intent==ECO:
                act=0
            elif intent==TORMENTA and hp<=14:
                act=2
            else:
                lasttech=htech[hn-1] if hn>0 else -1
                act=1 if qi>=tcost and lasttech!=0 else 0

        band=0; qspent=0; techid=-1; elem=-1

        if act==3:
            hp=min(MAX_HP,hp+dice(3,6)+6); potion=0
        elif act==2:
            guard1=np.random.randint(35,51); guard2=np.random.randint(25,41)
            qi=min(MAX_QI,qi+3)
        else:
            z=apply_player_attack(act,locked,root,patt,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd,
                                  bdef,0,evade_next,reserve,close_guard,qi,bhp,burn_turns,deb,debturn)
            locked,qi,bhp,burn_turns,deb,debturn,reserve,qspent,techid,elem,band=z
            evade_next=0

        # observar acción y consolidar counter
        if hn<8:
            pos=hn; hn+=1
        else:
            ht[:-1]=ht[1:]; htech[:-1]=htech[1:]; helem[:-1]=helem[1:]; hqi[:-1]=hqi[1:]; hband[:-1]=hband[1:]
            pos=7
        ht[pos]=act; htech[pos]=techid; helem[pos]=elem; hqi[pos]=qspent; hband[pos]=band
        if not locked and hn>=3 and htech[hn-1]==0 and htech[hn-2]==0 and htech[hn-3]==0:
            locked=1

        if bhp<=0: break

        if intent==GOLPE:
            hit,crit=hit_roll(bat+(deb if debturn>0 else 0),pdef)
            dmg=0
            if hit:
                dmg=dice(basic_n,basic_f)+basic_flat
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100); guard1=guard2; guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100); guard2=0
            hp-=dmg
        elif intent==TORMENTA:
            hit,crit=hit_roll(bat+storm_ab+(deb if debturn>0 else 0),pdef)
            dmg=0
            if hit:
                dmg=dice(storm_n,storm_f)+storm_flat
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100); guard1=guard2; guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100); guard2=0
            hp-=dmg
            if dmg>0: qi=max(0,qi-storm_drain)
        elif intent==CERRAR:
            reserve=close_cap
        elif intent==RECORDAR:
            evade_next=remember_eva
        else:
            if qspent>0: qi=max(0,qi-eco_drain)

        if burn_turns>0 and bhp>0:
            bhp-=np.random.randint(1,4); burn_turns-=1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0

        if rn<4:
            recent[rn]=intent; rn+=1
        else:
            recent[:-1]=recent[1:]; recent[3]=intent

    return (1 if bhp<=0 and hp>0 else 0),max(0,hp),qi,potion


# intents Fase III
PICOTAZO=0
CAMPANA=1
ALA_VACIA=2
PATA3=3
SILENCIO=4
ROMPER=5
BUSCAR=6

GREEDY3=0
MASTER3=1
P3_POLICY_NAMES={0:"GREEDY",1:"MASTER_READER"}

@njit
def choose_phase3_intent(ht,htech,helem,hqi,hband,hn,recent,rn,hp,qi,bhp,armed,followup):
    if armed:
        return followup
    k1=htech[hn-1] if hn else -1
    k2=htech[hn-2] if hn>1 else -1
    e1=helem[hn-1] if hn else -1
    e2=helem[hn-2] if hn>1 else -1
    t1=ht[hn-1] if hn else -1
    t2=ht[hn-2] if hn>1 else -1
    technique_repeat=hn>1 and k1>=0 and k1==k2
    element_repeat=hn>1 and e1>=0 and e1==e2
    offense_streak=hn>1 and t1<=1 and t2<=1
    qi_streak=hn>1 and hqi[hn-1]>0 and hqi[hn-2]>0
    heavy_recent=0
    for j in range(max(0,hn-2),hn):
        if hband[j]>=2: heavy_recent=1

    scores=np.zeros(7)
    jitter=np.array([.5,.5,.4,.4,.2,0.,.2])
    scores[PICOTAZO]=25+(8 if hp<=8 else 0)
    scores[CAMPANA]=24+(24 if hp<=8 else 0)+(8 if qi>=72 else 0)-(45 if intent_recent(recent,rn,CAMPANA,2) else 0)
    scores[ALA_VACIA]=16+(17 if offense_streak else 0)+(14 if heavy_recent else 0)-(30 if intent_recent(recent,rn,ALA_VACIA,2) else 0)
    scores[PATA3]=15+(15 if bhp<=15 else 0)-(30 if intent_recent(recent,rn,PATA3,2) else 0)
    scores[SILENCIO]=10+(32 if technique_repeat else 0)+(18 if element_repeat else 0)-(50 if intent_recent(recent,rn,SILENCIO,3) else 0)
    scores[ROMPER]=-1e6
    scores[BUSCAR]=10+(28 if qi_streak else 0)+(10 if qi>=72 else 0)-(50 if intent_recent(recent,rn,BUSCAR,3) else 0)

    best=0; bestv=-1e9
    for i in range(7):
        v=scores[i]+(np.random.random()-.5)*jitter[i]
        if v>bestv:
            bestv=v;best=i
    return best

@njit
def phase3_ma(root,o1,o2,seed,hp,qi,potion,policy,heavy_hp=10):
    np.random.seed(seed)
    ratt,rdef,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd=root_stats(root,o1,o2)
    patt=1+ratt+3+GEAR_ATK
    pdef=10+rdef+GEAR_DEF
    bhp=50
    burn_turns=0;deb=0;debturn=0
    evade_next=0;def_next=0
    guard1=0;guard2=0
    locked=0
    tech_streak=0

    ht=np.full(8,-1,np.int8);htech=np.full(8,-1,np.int8);helem=np.full(8,-1,np.int8)
    hqi=np.zeros(8,np.int16);hband=np.zeros(8,np.int8);hn=0
    recent=np.full(4,-1,np.int8);rn=0

    plan=0;armed=0;followup=-1;reftech=-1;refelem=-1
    silencio_count=0;buscar_count=0;armed_count=0;broken_count=0;romper_count=0

    for rnd in range(1,81):
        if bhp<=0 or hp<=0: break
        intent=choose_phase3_intent(ht,htech,helem,hqi,hband,hn,recent,rn,hp,qi,bhp,armed,followup)
        if intent==SILENCIO: silencio_count+=1
        if intent==BUSCAR: buscar_count+=1
        if intent==ROMPER: romper_count+=1

        if not armed and intent==SILENCIO:
            plan=1;followup=ROMPER
            reftech=htech[hn-1] if hn else -1
            refelem=helem[hn-1] if hn else -1
        elif not armed and intent==BUSCAR:
            plan=2;followup=CAMPANA
            reftech=-1;refelem=-1

        if hp<=9 and potion:
            act=3
        elif policy==GREEDY3:
            act=1 if qi>=tcost and not locked else 0
        else:
            if intent==SILENCIO or intent==BUSCAR:
                act=0
            elif (intent==CAMPANA or intent==ROMPER) and hp<=heavy_hp:
                act=2
            else:
                act=1 if qi>=tcost and not locked and tech_streak<2 else 0

        qspent=0;techid=-1;elem=-1;band=0
        if act==3:
            hp=min(MAX_HP,hp+dice(3,6)+6);potion=0;tech_streak=0
        elif act==2:
            guard1=np.random.randint(35,51);guard2=np.random.randint(25,41)
            qi=min(MAX_QI,qi+3);tech_streak=0
        else:
            z=apply_player_attack(act,locked,root,patt,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd,
                                  13,def_next,evade_next,0,3,qi,bhp,burn_turns,deb,debturn)
            locked,qi,bhp,burn_turns,deb,debturn,_,qspent,techid,elem,band=z
            def_next=0;evade_next=0
            if act==0: tech_streak=0
            else: tech_streak+=1

        # plan observes only the resolved player action
        if armed:
            armed=0;plan=0;followup=-1
        elif plan==1:
            repeats_tech=reftech>=0 and techid==reftech
            repeats_elem=refelem>=0 and elem==refelem and act==1
            if repeats_tech or repeats_elem:
                armed=1;armed_count+=1
            else:
                plan=0;followup=-1;broken_count+=1
        elif plan==2:
            if qspent>0 and act==1:
                armed=1;armed_count+=1
            else:
                plan=0;followup=-1;broken_count+=1

        if hn<8:
            pos=hn;hn+=1
        else:
            ht[:-1]=ht[1:];htech[:-1]=htech[1:];helem[:-1]=helem[1:];hqi[:-1]=hqi[1:];hband[:-1]=hband[1:]
            pos=7
        ht[pos]=act;htech[pos]=techid;helem[pos]=elem;hqi[pos]=qspent;hband[pos]=band

        if locked:
            if act==0: locked=0
        elif hn>=3 and htech[hn-1]>=0 and htech[hn-1]==htech[hn-2] and htech[hn-2]==htech[hn-3]:
            locked=1

        if bhp<=0: break

        dmg=0
        if intent==PICOTAZO:
            hit,crit=hit_roll(5+(deb if debturn>0 else 0),pdef)
            if hit:
                dmg=dice(1,4)+1
                if crit: dmg=math.ceil(dmg*1.5)
        elif intent==CAMPANA:
            hit,crit=hit_roll(5+(deb if debturn>0 else 0),pdef)
            if hit:
                dmg=dice(1,6)+2
                if crit: dmg=math.ceil(dmg*1.5)
            if dmg>0: qi=max(0,qi-2)
        elif intent==ALA_VACIA:
            evade_next=10
        elif intent==PATA3:
            def_next=3
        elif intent==ROMPER:
            hit,crit=hit_roll(6+(deb if debturn>0 else 0),pdef)
            if hit:
                dmg=dice(1,6)+2
                if crit: dmg=math.ceil(dmg*1.5)

        if dmg>0 and guard1>0:
            dmg-=math.floor(dmg*guard1/100);guard1=guard2;guard2=0
        elif dmg>0 and guard2>0:
            dmg-=math.floor(dmg*guard2/100);guard2=0
        hp-=dmg

        if burn_turns>0 and bhp>0:
            bhp-=np.random.randint(1,4);burn_turns-=1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0

        if rn<4:
            recent[rn]=intent;rn+=1
        else:
            recent[:-1]=recent[1:];recent[3]=intent

    return (1 if bhp<=0 and hp>0 else 0),silencio_count,buscar_count,armed_count,broken_count,romper_count

@njit
def scenario123(runs,seed,root,o1,o2,policy,heavy_hp=10,force_qi=-1,force_potion=-1):
    reach3=0;win3=0
    entry_hp=0.;entry_qi=0.
    sil=0.;bus=0.;arm=0.;bro=0.;rom=0.
    for i in range(runs):
        s=seed+i*1009+31
        a=phase1(READER,root,o1,o2,s)
        if not a[0]: continue
        b=phase2(CHAIN_A,READER,root,o1,o2,s^0x5A5A5A5A,a[1],a[2],a[3],a[4],a[5],a[6])
        if not b[0]: continue
        reach3+=1
        hp=b[1]; qi=b[2] if force_qi<0 else force_qi
        pot=b[3] if force_potion<0 else force_potion
        entry_hp+=hp;entry_qi+=qi
        c=phase3_ma(root,o1,o2,s^0xA55AA55A,hp,qi,pot,policy,heavy_hp)
        win3+=c[0];sil+=c[1];bus+=c[2];arm+=c[3];bro+=c[4];rom+=c[5]
    if reach3==0:
        return (0.,0.,0.,0.,0.,0.,0.,0.,0.,0.)
    return (reach3/runs,win3/reach3,win3/runs,entry_hp/reach3,entry_qi/reach3,
            sil/reach3,bus/reach3,arm/reach3,bro/reach3,rom/reach3)

@njit
def standalone_zero_qi(runs,seed,root,o1,o2,policy,heavy_hp=10):
    wins=0
    for i in range(runs):
        c=phase3_ma(root,o1,o2,seed+i*1009+31,28,0,0,policy,heavy_hp)
        wins+=c[0]
    return wins/runs

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=("baseline","chain-zero-qi","standalone-zero-qi"),default="baseline")
    ap.add_argument("--policy",choices=("greedy","master"),default="master")
    ap.add_argument("--runs",type=int,default=15000)
    ap.add_argument("--heavy-hp",type=int,default=10)
    args=ap.parse_args()
    policy=GREEDY3 if args.policy=="greedy" else MASTER3
    scenario123(2,1,0,1,1,policy,args.heavy_hp,-1,-1)

    rows=[]
    for root in range(3):
      for o1 in range(1,4):
       for o2 in range(1,4):
        seed=1300000000+(root+1)*1000000+o1*10000+o2*100
        if args.mode=="standalone-zero-qi":
            z=standalone_zero_qi(args.runs,seed,root,o1,o2,policy,args.heavy_hp)
            rows.append(dict(root=root,o1=o1,o2=o2,win=z))
        else:
            fq=0 if args.mode=="chain-zero-qi" else -1
            fp=0 if args.mode=="chain-zero-qi" else -1
            z=scenario123(args.runs,seed,root,o1,o2,policy,args.heavy_hp,fq,fp)
            rows.append(dict(root=root,o1=o1,o2=o2,reach=z[0],cond=z[1],total=z[2],
                             entryHp=z[3],entryQi=z[4],silencio=z[5],buscar=z[6],
                             armed=z[7],broken=z[8],romper=z[9]))
    df=pd.DataFrame(rows)
    if args.mode=="standalone-zero-qi":
        print(df.groupby("root").win.agg(["mean","min","max"]).to_string())
        print("\nGLOBAL",df.win.mean(),df.win.min(),df.win.max())
    else:
        print(df.groupby("root")[["reach","cond","total","entryHp","entryQi"]].mean().to_string())
        print("\nGLOBAL")
        print(df[["reach","cond","total","entryHp","entryQi","silencio","buscar","armed","broken","romper"]].mean().to_string())
        print("\nCOND RANGE",df.cond.min(),df.cond.max())
    df.to_csv("grulla_phase123_"+args.mode+"_"+args.policy+"_v0.1.csv",index=False)

if __name__=="__main__":
    main()
