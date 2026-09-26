# Grulla Blanca — Fase I · G345_D1 + Pata anti-absorción + Piel/Filamento v0.1
# SOLO Fase I. No Paso, no Fase II/III.
# Máximo 2 PT opcionales entre Piel y Filamento.
#
# Pata Inmóvil:
# - +3 DEF contra siguiente ofensiva del jugador;
# - prepara el siguiente Golpe de Ala;
# - si ese Golpe conecta con Piel activa, daño bruto x1.50 antes de absorción;
# - se consume aunque falle.
#
# Selección:
# python grulla-phase1-piel-g345d1-pata-filamento-v0.1.py --mode grid --runs 5000
# Confirmación:
# python grulla-phase1-piel-g345d1-pata-filamento-v0.1.py --mode confirm --runs 20000 --ids C22_F00,C02_F03,C13_F00

import argparse,itertools,math,zlib
import numpy as np
import pandas as pd
from numba import njit

PH=28; PQ=110; GAT=2; GDEF=7
BHP=150; BAT=4; PATA=3
READER={13:.609,14:.547}

ROOTS={
 0:{"attack":1,"defense":0,"baseCost":7,"baseDamage":(2,6,2)},
 1:{"attack":2,"defense":0,"baseCost":6,"baseDamage":(1,10,3)},
 2:{"attack":0,"defense":2,"baseCost":6,"baseDamage":(2,6,0)},
}
BASE=[(0,0)]+[(a,0) for a in range(1,4)]+[(0,b) for b in range(1,4)]+[(a,b) for a in range(1,4) for b in range(1,4)]
FIL_R1=[{"cost":-1},{"damage":(1,3)},{"control":3}]
FIL_R2=[{"atadura":2},{"control":4},{"damage":(1,4)}]

def pts(c): return int(c[0]>0)+int(c[1]>0)

def piel_conf(c):
 p1,p2=c; cost=5; guard=3; dur=1
 if p1==1: guard=4
 elif p1==2: dur+=1
 elif p1==3: cost-=1
 if p2==1: cost-=1
 elif p2==2: guard=5
 elif p2==3: dur+=1
 cost=max(math.ceil(5*.7),cost)
 return (cost,guard,dur,guard*dur)

def fil_conf(root,c):
 p1,p2=c; cost=6; ctrl=4; dmg=[]; atad=1
 for opt,tab in ((p1,FIL_R1),(p2,FIL_R2)):
  if not opt: continue
  m=tab[opt-1]; cost+=m.get("cost",0); ctrl+=m.get("control",0)
  if "damage" in m: dmg.append(m["damage"])
  if "atadura" in m: atad+=m["atadura"]-1
 if root==2: cost-=1
 cost=max(math.ceil(6*.7),cost)
 return (cost,1,ctrl,tuple(dmg)) # jefe unico: atadura real 1

def cid(pc,fc): return f"C{pc[0]}{pc[1]}_F{fc[0]}{fc[1]}"

def dedup():
 raw=[]; best={}
 for pc,fc in itertools.product(BASE,repeat=2):
  total=pts(pc)+pts(fc)
  if total>2: continue
  eff=tuple((piel_conf(pc),fil_conf(r,fc)) for r in range(3))
  raw.append((pc,fc,total,eff))
  cand=(total,pc,fc)
  if eff not in best or cand<best[eff][0]: best[eff]=(cand,(pc,fc))
 out=[v[1] for v in best.values()]
 out.sort(key=lambda x:(pts(x[0])+pts(x[1]),cid(*x)))
 return raw,out

@njit
def dice(n,f):
 s=0
 for _ in range(n): s+=np.random.randint(1,f+1)
 return s

@njit
def root_stats(root,o1,o2):
 if root==0: ra=1; rd=0; bc=7; nd=2; fd=6; flat=2
 elif root==1: ra=2; rd=0; bc=6; nd=1; fd=10; flat=3
 else: ra=0; rd=2; bc=6; nd=2; fd=6; flat=0
 cost=bc; ab=0; crit=20; add=0; burn=0; deb=0; debdur=0
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
  else: deb=-2; debdur=1
 else:
  if o1==1: deb=-1; debdur=1
  elif o1==2: add=1
  else: ab+=3
  if o2==1: cost-=1
  elif o2==2: ab+=4
  else: crit=19
 cost=max(math.ceil(bc*.7),cost-1)
 return ra,rd,cost,nd,fd,flat+1,ab,crit,add,burn,deb,debdur

@njit
def pstats(p1,p2):
 cost=5; g=3; dur=1
 if p1==1: g=4
 elif p1==2: dur+=1
 elif p1==3: cost-=1
 if p2==1: cost-=1
 elif p2==2: g=5
 elif p2==3: dur+=1
 cost=max(math.ceil(5*.7),cost)
 return cost,g,g*dur

@njit
def fstats(root,p1,p2):
 cost=6; ctrl=4; d1=0; d2=0
 if p1==1: cost-=1
 elif p1==2: d1=3
 elif p1==3: ctrl+=3
 if p2==1: pass
 elif p2==2: ctrl+=4
 elif p2==3: d2=4
 if root==2: cost-=1
 cost=max(math.ceil(6*.7),cost)
 return cost,ctrl,d1,d2

@njit
def duel(root,o1,o2,cp1,cp2,fp1,fp2,bdef):
 ra,rd,rc,nd,fd,flat,rab,crit,add,rburn,rdeb,rdebd=root_stats(root,o1,o2)
 pcost,pgmax,pcapmax=pstats(cp1,cp2)
 fcost,fctrl,fd1,fd2=fstats(root,fp1,fp2)
 patt=1+ra+3+GAT; pdef=10+rd+GDEF

 hp=PH; qi=PQ; bhp=BHP; pot=1
 g1=0; g2=0; pg=0; pcap=0
 bound=0; ten=0; tennew=0; cd=0
 burn=0; deb=0; debturn=0; defnext=0
 anti_next=0

 for rnd in range(1,81):
  cyc=(rnd-1)%4

  # MULTI_READER Piel+Filamento
  if cyc==0:
   act=5 if (pcap<=0 and qi>=pcost) else 1
  elif cyc==1:
   act=1
  elif cyc==2:
   if ten<=0 and cd<=0 and qi>=fcost: act=6
   elif pcap>0 and qi>=rc: act=1
   elif pcap<=0 and qi>=pcost: act=5
   else: act=2
  else:
   act=0

  if hp<=9 and pot: act=3
  if act==1 and qi<rc: act=0
  usedfil=0

  if act==3:
   hp=min(PH,hp+dice(3,6)+6); pot=0
  elif act==2:
   pg=0; pcap=0; g1=np.random.randint(35,51); g2=np.random.randint(25,41); qi=min(PQ,qi+3)
  elif act==5:
   qi-=pcost; g1=0; g2=0; pg=pgmax; pcap=pcapmax
  elif act==6:
   qi-=fcost; usedfil=1; cd=1
   r=np.random.randint(1,21)
   ok=(r==20) or (r!=1 and r+patt+fctrl>=bdef+2)
   if ok:
    bound=1; ten=2; tennew=1
    if fd1: bhp-=np.random.randint(1,fd1+1)
    if fd2: bhp-=np.random.randint(1,fd2+1)
  elif act==0:
   r=np.random.randint(1,21)
   hit=(r==20) or (r!=1 and r+patt>=bdef+defnext)
   if hit:
    d=dice(1,8)
    if r==20: d=math.ceil(d*1.5)
    bhp-=d
   defnext=0
  else:
   qi-=rc
   r=np.random.randint(1,21)
   hit=(r==20) or (r!=1 and ((r>=crit) or (r+patt+rab>=bdef+defnext)))
   if hit:
    d=dice(nd,fd)+flat+(dice(1,4) if add else 0)
    if r>=crit: d=math.ceil(d*1.5)
    bhp-=d
    if rburn: burn=2
    if rdeb: deb=rdeb; debturn=rdebd
   defnext=0

  if bhp<=0: return 1

  if cd>0 and not usedfil: cd-=1
  if ten>0 and not tennew: ten-=1
  tennew=0

  if bound>0:
   bound-=1
  else:
   if cyc==3:
    defnext=PATA
    anti_next=1
   else:
    ba=BAT+(deb if debturn>0 else 0)
    r=np.random.randint(1,21)
    hit=(r==20) or (r!=1 and r+ba>=pdef)
    d=0
    if hit:
     d=dice(2,6)+2 if cyc==2 else dice(1,6)+2
     if r==20: d=math.ceil(d*1.5)

    if d>0 and pcap>0:
     if anti_next:
      d=math.ceil(d*1.5)
     a=min(d,pg,pcap); d-=a; pcap-=a
     if pcap<=0: pg=0
    elif d>0:
     if g1>0: d-=math.floor(d*g1/100); g1=g2; g2=0
     elif g2>0: d-=math.floor(d*g2/100); g2=0
    hp-=d

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
def scen(n,seed,root,o1,o2,cp1,cp2,fp1,fp2,bdef):
 np.random.seed(seed); w=0
 for _ in range(n): w+=duel(root,o1,o2,cp1,cp2,fp1,fp2,bdef)
 return w/n

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--mode",choices=("grid","confirm"),default="grid")
 ap.add_argument("--runs",type=int,default=None)
 ap.add_argument("--ids",default="")
 ap.add_argument("--chunk",type=int,default=None)
 ap.add_argument("--chunks",type=int,default=1)
 args=ap.parse_args()
 raw,cfgs=dedup()
 if args.mode=="confirm":
  wanted={x.strip() for x in args.ids.split(",") if x.strip()}
  cfgs=[x for x in cfgs if cid(*x) in wanted]
  if not cfgs: raise SystemExit("sin ids")
 if args.chunk is not None:
  cfgs=[x for i,x in enumerate(cfgs) if i%args.chunks==args.chunk]
 runs=args.runs or (5000 if args.mode=="grid" else 20000)
 scen(2,1,0,1,1,0,0,0,0,13)

 rows=[]
 for pc,fc in cfgs:
  id_=cid(pc,fc); total=pts(pc)+pts(fc)
  for root in range(3):
   for o1 in range(1,4):
    for o2 in range(1,4):
     for bd in (13,14):
      seed=zlib.crc32(f"{id_}|{root}|{o1}|{o2}|{bd}|{args.mode}".encode())&0xffffffff
      rows.append(dict(config_id=id_,optional_pts=total,root=root,o1=o1,o2=o2,boss_def=bd,
                       winRate=scen(runs,seed,root,o1,o2,pc[0],pc[1],fc[0],fc[1],bd)))
 df=pd.DataFrame(rows)
 print(f"raw={len(raw)} dedup={len(dedup()[1])} selected={len(cfgs)}")
 cfg=df.groupby(["config_id","optional_pts","boss_def"]).winRate.agg(["mean","min","max"]).reset_index()
 for bd in (13,14):
  print("\nDEF",bd)
  print(cfg[cfg.boss_def==bd].sort_values("mean",ascending=False).head(12).to_string(index=False))
 suffix=f"{args.mode}"+(f"_chunk{args.chunk}" if args.chunk is not None else "")
 df.to_csv(f"grulla_phase1_g345d1_pata_piel_filamento_{suffix}_v0.1.csv",index=False)
 cfg.to_csv(f"grulla_phase1_g345d1_pata_piel_filamento_{suffix}_configs_v0.1.csv",index=False)

if __name__=="__main__": main()
