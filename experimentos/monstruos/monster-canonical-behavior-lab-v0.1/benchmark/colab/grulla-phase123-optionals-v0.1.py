# Grulla Blanca — cadena I -> II -> III con opcionales · v0.1
# Fase I y II congeladas. Fase III M_A + MASTER_READER en validación.
#
# Reutiliza exactamente las políticas opcionales cerradas de:
#   grulla-phase12-chain-optionals-v0.1.py
# y el cerebro/estadísticas FIII de:
#   grulla-phase123-chain-ma-v0.1.py
#
# La opcional en FIII sólo sustituye DEFENDER ante CAMPANA/ROMPER con HP <= 10.
# No se usa como rotación principal.
#
# Uso:
#   python grulla-phase123-optionals-v0.1.py --runs 15000 --use-opt-f3 1
#   python grulla-phase123-optionals-v0.1.py --runs 15000 --use-opt-f3 0

import argparse, importlib.util, math
from pathlib import Path
import numpy as np
import pandas as pd
from numba import njit

HERE = Path(__file__).resolve().parent

# Cargar sólo definiciones del script I->II cerrado, sin ejecutar su grid final.
p12_path = HERE / "grulla-phase12-chain-optionals-v0.1.py"
src = p12_path.read_text(encoding="utf-8")
marker = "scenario(2,1,0,0,1,1,1)"
if marker not in src:
    raise RuntimeError("No se encontró marcador de corte en phase12 optionals")
ns = {}
exec(src.split(marker,1)[0], ns)

# Cargar módulo de cadena M_A; tiene main guard y no ejecuta benchmark al importar.
p123_path = HERE / "grulla-phase123-chain-ma-v0.1.py"
spec = importlib.util.spec_from_file_location("grulla_p123_ma", p123_path)
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)

phase1 = ns["phase1"]
phase2 = ns["phase2"]

@njit
def phase3_optional(tool,root,o1,o2,seed,hp,qi,potion,heavy_hp=10,useopt=1):
    np.random.seed(seed)
    ratt,rdef,tcost,nd,fd,tflat,tab,tcrit,add,rburn,rdeb,rdebd=ma.root_stats(root,o1,o2)
    patt=1+ratt+3+ma.GEAR_ATK
    pdef=10+rdef+ma.GEAR_DEF
    bhp=50

    burn_turns=0;deb=0;debturn=0
    evade_next=0;def_next=0
    guard1=0;guard2=0
    locked=-1
    tech_streak=0

    paso_ev=0;paso_turns=0
    piel_guard=0;piel_cap=0
    tenacity=0;tenacity_new=0;cooldown=0

    ht=np.full(8,-1,np.int8);htech=np.full(8,-1,np.int8);helem=np.full(8,-1,np.int8)
    hqi=np.zeros(8,np.int16);hband=np.zeros(8,np.int8);hn=0
    recent=np.full(4,-1,np.int8);rn=0

    plan=0;armed=0;followup=-1;reftech=-1;refelem=-1
    silencio=0;buscar=0;armed_n=0;broken=0;romper=0;opt_uses=0

    for rnd in range(1,81):
        if bhp<=0 or hp<=0: break

        intent=ma.choose_phase3_intent(
            ht,htech,helem,hqi,hband,hn,recent,rn,hp,qi,bhp,armed,followup
        )
        if intent==ma.SILENCIO: silencio+=1
        if intent==ma.BUSCAR: buscar+=1
        if intent==ma.ROMPER: romper+=1

        if not armed and intent==ma.SILENCIO:
            plan=1;followup=ma.ROMPER
            reftech=htech[hn-1] if hn else -1
            refelem=helem[hn-1] if hn else -1
        elif not armed and intent==ma.BUSCAR:
            plan=2;followup=ma.CAMPANA
            reftech=-1;refelem=-1

        # 0 BASIC, 1 root, 2 DEFENDER, 3 potion, 4 Paso, 5 Piel, 6 Filamento
        if hp<=9 and potion:
            act=3
        elif intent==ma.SILENCIO or intent==ma.BUSCAR:
            act=0
        elif (intent==ma.CAMPANA or intent==ma.ROMPER) and hp<=heavy_hp:
            if useopt and tool==0 and qi>=5 and locked!=1:
                act=4
            elif useopt and tool==1 and qi>=5 and piel_cap<=0 and locked!=1:
                act=5
            elif useopt and tool==2 and qi>=(5 if root==2 else 6) and tenacity<=0 and cooldown<=0 and locked!=1:
                act=6
            else:
                act=2
        else:
            act=1 if qi>=tcost and locked!=0 and tech_streak<2 else 0

        qspent=0;techid=-1;elem=-1;band=0
        skip_boss=0;used_fil=0

        if act==3:
            hp=min(ma.MAX_HP,hp+ma.dice(3,6)+6);potion=0;tech_streak=0
        elif act==2:
            piel_guard=0;piel_cap=0
            guard1=np.random.randint(35,51);guard2=np.random.randint(25,41)
            qi=min(ma.MAX_QI,qi+3);tech_streak=0
        elif act==4:
            qi-=5;qspent=5;techid=1;opt_uses+=1
            paso_ev=25;paso_turns=3;tech_streak=0
        elif act==5:
            qi-=5;qspent=5;techid=1;opt_uses+=1
            guard1=0;guard2=0;piel_guard=5;piel_cap=10;tech_streak=0
        elif act==6:
            fc=5 if root==2 else 6
            qi-=fc;qspent=fc;techid=1;opt_uses+=1;used_fil=1;cooldown=1;tech_streak=0
            r=np.random.randint(1,21)
            ok=(r==20) or (r!=1 and r+patt+4>=15)
            if ok:
                bhp-=np.random.randint(1,4)+np.random.randint(1,5)
                tenacity=2;tenacity_new=1;skip_boss=1
        elif act==0:
            hit,crit=ma.hit_roll(patt,13+def_next,20,evade_next)
            dmg=0
            if hit:
                dmg=ma.dice(1,8)
                if crit: dmg=math.ceil(dmg*1.5)
                bhp-=dmg;band=2 if dmg>=8 else 1
            def_next=0;evade_next=0;locked=-1;tech_streak=0
        else:
            qi-=tcost;qspent=tcost;techid=0;elem=root
            if locked!=0:
                hit,crit=ma.hit_roll(patt+tab,13+def_next,tcrit,evade_next)
                dmg=0
                if hit:
                    dmg=ma.dice(nd,fd)+tflat+(ma.dice(1,4) if add else 0)
                    if crit: dmg=math.ceil(dmg*1.5)
                    bhp-=dmg;band=2 if dmg>=8 else 1
                    if dmg>0 and rburn: burn_turns=2
                    if dmg>0 and rdeb: deb=rdeb;debturn=rdebd
            def_next=0;evade_next=0;tech_streak+=1

        if armed:
            armed=0;plan=0;followup=-1
        elif plan==1:
            repeats_tech=reftech>=0 and techid==reftech
            repeats_elem=refelem>=0 and elem==refelem and act==1
            if repeats_tech or repeats_elem:
                armed=1;armed_n+=1
            else:
                plan=0;followup=-1;broken+=1
        elif plan==2:
            if qspent>0 and act in (1,4,5,6):
                armed=1;armed_n+=1
            else:
                plan=0;followup=-1;broken+=1

        if hn<8:
            pos=hn;hn+=1
        else:
            ht[:-1]=ht[1:];htech[:-1]=htech[1:];helem[:-1]=helem[1:]
            hqi[:-1]=hqi[1:];hband[:-1]=hband[1:];pos=7
        ht[pos]=act;htech[pos]=techid;helem[pos]=elem;hqi[pos]=qspent;hband[pos]=band

        if locked>=0:
            if act==0 or (techid>=0 and techid!=locked): locked=-1
        elif hn>=3 and htech[hn-1]>=0 and htech[hn-1]==htech[hn-2] and htech[hn-2]==htech[hn-3]:
            locked=htech[hn-1]

        if bhp<=0: break

        if cooldown>0 and not used_fil: cooldown-=1
        if tenacity>0 and not tenacity_new: tenacity-=1
        tenacity_new=0

        dmg=0
        if not skip_boss:
            if intent==ma.PICOTAZO:
                hit,crit=ma.hit_roll(5+(deb if debturn>0 else 0),pdef,20,paso_ev if paso_turns>0 else 0)
                if hit:
                    dmg=ma.dice(1,4)+1
                    if crit: dmg=math.ceil(dmg*1.5)
            elif intent==ma.CAMPANA:
                hit,crit=ma.hit_roll(5+(deb if debturn>0 else 0),pdef,20,paso_ev if paso_turns>0 else 0)
                if hit:
                    dmg=ma.dice(1,6)+2
                    if crit: dmg=math.ceil(dmg*1.5)
                if dmg>0: qi=max(0,qi-2)
            elif intent==ma.ALA_VACIA:
                evade_next=10
            elif intent==ma.PATA3:
                def_next=3
            elif intent==ma.ROMPER:
                hit,crit=ma.hit_roll(6+(deb if debturn>0 else 0),pdef,20,paso_ev if paso_turns>0 else 0)
                if hit:
                    dmg=ma.dice(1,6)+2
                    if crit: dmg=math.ceil(dmg*1.5)

            if dmg>0 and piel_cap>0:
                absorb=min(dmg,piel_guard,piel_cap);dmg-=absorb;piel_cap-=absorb
                if piel_cap<=0: piel_guard=0
            elif dmg>0 and guard1>0:
                dmg-=math.floor(dmg*guard1/100);guard1=guard2;guard2=0
            elif dmg>0 and guard2>0:
                dmg-=math.floor(dmg*guard2/100);guard2=0
            hp-=dmg

        if burn_turns>0 and bhp>0:
            bhp-=np.random.randint(1,4);burn_turns-=1
        if debturn>0:
            debturn-=1
            if debturn<=0: deb=0
        if paso_turns>0:
            paso_turns-=1
            if paso_turns<=0: paso_ev=0

        if rn<4:
            recent[rn]=intent;rn+=1
        else:
            recent[:-1]=recent[1:];recent[3]=intent

    return (1 if bhp<=0 and hp>0 else 0),silencio,buscar,armed_n,broken,romper,opt_uses

@njit
def scenario123_optional(runs,seed,tool,root,o1,o2,useopt3,heavy_hp):
    reach2=0;reach3=0;win3=0
    eh=0.;eq=0.;ep=0.;sil=0.;bus=0.;arm=0.;bro=0.;rom=0.;opt=0.
    for i in range(runs):
        s=seed+i*1009+31
        a=phase1(tool,root,o1,o2,s)
        if not a[0]: continue
        reach2+=1
        b=phase2(tool,root,o1,o2,s^0x5A5A5A5A,a[1],a[2],a[3],a[4],a[5],1)
        if not b[0]: continue
        reach3+=1;eh+=b[1];eq+=b[2];ep+=b[3]
        c=phase3_optional(tool,root,o1,o2,s^0xA55AA55A,b[1],b[2],b[3],heavy_hp,useopt3)
        win3+=c[0];sil+=c[1];bus+=c[2];arm+=c[3];bro+=c[4];rom+=c[5];opt+=c[6]

    if reach3==0:
        return (reach2/runs,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.)
    return (
        reach2/runs,reach3/runs,win3/reach3,win3/runs,
        eh/reach3,eq/reach3,ep/reach3,
        sil/reach3,bus/reach3,arm/reach3,bro/reach3,rom/reach3,opt/reach3
    )

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs",type=int,default=15000)
    ap.add_argument("--use-opt-f3",type=int,choices=(0,1),default=1)
    ap.add_argument("--heavy-hp",type=int,default=10)
    args=ap.parse_args()

    scenario123_optional(2,1,0,0,1,1,args.use_opt_f3,args.heavy_hp)
    rows=[]
    for tool in range(3):
        for root in range(3):
            for o1 in range(1,4):
                for o2 in range(1,4):
                    seed=(tool+1)*100000000+(root+1)*1000000+o1*10000+o2*100
                    z=scenario123_optional(
                        args.runs,seed,tool,root,o1,o2,args.use_opt_f3,args.heavy_hp
                    )
                    rows.append((tool,root,o1,o2,*z))

    cols="tool root o1 o2 reach2 reach3 cond3 total entryHp entryQi entryPot silencio buscar armed broken romper optUse".split()
    df=pd.DataFrame(rows,columns=cols)
    print(df.groupby("tool")[["reach2","reach3","cond3","total","entryHp","entryQi","entryPot","optUse"]].mean().to_string())
    print("\nby root")
    print(df.groupby(["tool","root"])[["reach3","cond3","total"]].mean().to_string())
    print("\nranges")
    print(df.groupby("tool").cond3.agg(["min","max"]).to_string())
    df.to_csv(f"grulla_phase123_optionals_use{args.use_opt_f3}_v0.1.csv",index=False)

if __name__=="__main__":
    main()
