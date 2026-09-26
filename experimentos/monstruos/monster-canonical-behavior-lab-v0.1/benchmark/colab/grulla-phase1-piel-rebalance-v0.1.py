# Grulla Blanca — Fase I · sensibilidad de rebalance de Piel de Cobre v0.1
# SOLO Fase I. Conserva semántica de burbuja ver74 y política PIEL_READER.
# No Paso, no Filamento, no Fase II/III.
#
# Objetivo:
# - variar únicamente Guardia base / Guardia de ramas y duración base;
# - mantener coste, +duración, persistencia y reserva = Guardia × duración;
# - detectar un rango que ayude sin trivializar.
#
# Uso:
#   python grulla-phase1-piel-rebalance-v0.1.py --mode sensitivity --runs 2000
#   python grulla-phase1-piel-rebalance-v0.1.py --mode grid --model G345_D1 --runs 5000
#   python grulla-phase1-piel-rebalance-v0.1.py --mode confirm --model G345_D1 --runs 20000 --finalists 1-2,1-3,2-2

import argparse, math
import numpy as np
import pandas as pd

PLAYER_MAX_HP=28
PLAYER_MAX_QI=110
GEAR_ATTACK=2
GEAR_DEFENSE=7
BOSS_HP=150
BOSS_ATTACK=4
PATA_DEF_BONUS=3
READER_BASELINE={13:0.609,14:0.547}

ROOTS={
 "fuego":{"attack":1,"defense":0,"baseCost":7,"baseDamage":(2,6,2),
          "r1":[{"burn":(1,3,2)},{"damage":(1,4,0)},{"attack":3}],
          "r2":[{"cost":-1},{"attack":4},{"critMin":19}]},
 "metal":{"attack":2,"defense":0,"baseCost":6,"baseDamage":(1,10,3),
          "r1":[{"attack":3},{"damage":(1,4,0)},{"critMin":19}],
          "r2":[{"cost":-1,"critMin":19},{"attack":4},{"debil":(-2,1)}]},
 "agua":{"attack":0,"defense":2,"baseCost":6,"baseDamage":(2,6,0),
         "r1":[{"debil":(-1,1)},{"damage":(1,4,0)},{"attack":3}],
         "r2":[{"cost":-1},{"attack":4},{"critMin":19}]},
}

# (guardia base, duración base, Cobre endurecido, Cobre grueso)
MODELS={
 "CURRENT": (3,2,6,7),
 "G345_D2": (3,2,4,5),
 "G234_D2": (2,2,3,4),
 "G345_D1": (3,1,4,5),
 "G234_D1": (2,1,3,4),
 "G344_D1": (3,1,4,4),
}

PIEL_NAMES_R1={0:"—",1:"Cobre endurecido",2:"Cobre flexible",3:"Cobre sobrio"}
PIEL_NAMES_R2={0:"—",1:"Aliento económico",2:"Cobre grueso",3:"Placas continuas"}
PIEL_CONFIGS=[(0,0)]+[(a,0) for a in range(1,4)]+[(0,b) for b in range(1,4)]+[(a,b) for a in range(1,4) for b in range(1,4)]

def root_conf(root,o1,o2):
 q=ROOTS[root]
 cost=q["baseCost"]; attack_bonus=0; crit_min=20
 dice=[q["baseDamage"][:2]]; flat=q["baseDamage"][2]+1
 burn=None; debil=None
 for m in (q["r1"][o1-1],q["r2"][o2-1]):
  cost+=m.get("cost",0); attack_bonus+=m.get("attack",0)
  crit_min=min(crit_min,m.get("critMin",20))
  if "damage" in m: dice.append(m["damage"][:2]); flat+=m["damage"][2]
  if "burn" in m: burn=m["burn"]
  if "debil" in m: debil=m["debil"]
 cost=max(math.ceil(q["baseCost"]*.7),max(1,cost-1))
 return dict(cost=cost,attack_bonus=attack_bonus,crit_min=crit_min,dice=dice,flat=flat,burn=burn,debil=debil)

def piel_conf(model,p1,p2):
 base_guard,base_duration,t1_guard,t2_guard=MODELS[model]
 cost=5; guard=base_guard; duration=base_duration
 if p1==1: guard=t1_guard
 elif p1==2: duration+=1
 elif p1==3: cost-=1
 if p2==1: cost-=1
 elif p2==2: guard=t2_guard
 elif p2==3: duration+=1
 cost=max(math.ceil(5*.7),max(1,cost))
 return dict(cost=cost,guard=guard,duration=duration,capacity=guard*duration)

def config_name(p1,p2):
 a,b=PIEL_NAMES_R1[p1],PIEL_NAMES_R2[p2]
 return f"{a} + {b}" if p1 and p2 else a if p1 else b if p2 else "Piel base"

def parse_finalists(raw):
 out=[]
 for token in (raw or "").split(","):
  token=token.strip()
  if not token: continue
  a,b=map(int,token.split("-")); cfg=(a,b)
  if cfg not in PIEL_CONFIGS: raise ValueError(token)
  out.append(cfg)
 return out

def roll_terms(rng,terms,flat,size):
 out=np.full(size,flat,dtype=np.int16)
 for n,f in terms:
  out+=rng.integers(1,f+1,size=(n,size),dtype=np.int16).sum(axis=0)
 return out

def apply_guard(hp,sel,dmg,def1,def2,pguard,pcap):
 cap=pcap[sel]; has=(dmg>0)&(cap>0)
 if has.any():
  absorb=np.zeros(sel.size,dtype=np.int16)
  absorb[has]=np.minimum(dmg[has],np.minimum(pguard[sel[has]],cap[has]))
  hp[sel]-=dmg-absorb
  s=sel[has]; pcap[s]-=absorb[has]; pguard[s]=np.where(pcap[s]>0,pguard[s],0)
 no=~has
 if no.any():
  loc=np.flatnonzero(no); s=sel[loc]; d=dmg[loc]
  g1=def1[s]; g2=def2[s]
  u1=(d>0)&(g1>0); u2=(d>0)&(~u1)&(g2>0)
  red=np.zeros(loc.size,dtype=np.int16)
  red[u1]=np.floor(d[u1]*g1[u1]/100).astype(np.int16)
  red[u2]=np.floor(d[u2]*g2[u2]/100).astype(np.int16)
  hp[s]-=d-red
  if u1.any():
   ss=s[u1]; def1[ss]=def2[ss]; def2[ss]=0
  if u2.any(): def2[s[u2]]=0

def simulate(model,root,o1,o2,p1,p2,boss_def,runs,seed):
 rng=np.random.default_rng(seed)
 q=ROOTS[root]; tc=root_conf(root,o1,o2); pc=piel_conf(model,p1,p2)
 p_attack=1+q["attack"]+3+GEAR_ATTACK
 p_def=10+q["defense"]+GEAR_DEFENSE

 hp=np.full(runs,PLAYER_MAX_HP,dtype=np.int16)
 qi=np.full(runs,PLAYER_MAX_QI,dtype=np.int16)
 bhp=np.full(runs,BOSS_HP,dtype=np.int16)
 alive=np.ones(runs,dtype=bool); win=np.zeros(runs,dtype=bool); potion=np.ones(runs,dtype=bool)
 def1=np.zeros(runs,dtype=np.int16); def2=np.zeros(runs,dtype=np.int16)
 pguard=np.zeros(runs,dtype=np.int16); pcap=np.zeros(runs,dtype=np.int16)
 burn_turns=np.zeros(runs,dtype=np.int8)
 debil=np.zeros(runs,dtype=np.int8); debil_turns=np.zeros(runs,dtype=np.int8)
 def_next=np.zeros(runs,dtype=np.int8)

 for rnd in range(1,81):
  active=alive&~win
  if not active.any(): break
  idx=np.flatnonzero(active); cycle=(rnd-1)%4

  act=np.zeros(idx.size,dtype=np.int8) # 0 basic,1 root,2 defend,3 potion,4 piel
  if cycle in (0,1): act[:]=1
  elif cycle==2: act[:]=np.where(pcap[idx]>0,1,4)
  else: act[:]=0
  act[(hp[idx]<=9)&potion[idx]]=3
  act[(act==1)&(qi[idx]<tc["cost"])]=0
  act[(act==4)&(qi[idx]<pc["cost"])]=2

  sel=idx[act==3]
  if sel.size:
   heal=rng.integers(1,7,size=(3,sel.size),dtype=np.int16).sum(axis=0)+6
   hp[sel]=np.minimum(PLAYER_MAX_HP,hp[sel]+heal); potion[sel]=False

  sel=idx[act==2]
  if sel.size:
   pguard[sel]=0; pcap[sel]=0
   def1[sel]=rng.integers(35,51,size=sel.size,dtype=np.int16)
   def2[sel]=rng.integers(25,41,size=sel.size,dtype=np.int16)
   qi[sel]=np.minimum(PLAYER_MAX_QI,qi[sel]+3)

  sel=idx[act==4]
  if sel.size:
   qi[sel]-=pc["cost"]; def1[sel]=0; def2[sel]=0
   pguard[sel]=pc["guard"]; pcap[sel]=pc["capacity"]

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
   dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg); dmg=np.where(hit,dmg,0)
   bhp[sel]-=dmg
   if tc["burn"]: burn_turns[sel]=np.where(dmg>0,tc["burn"][2],burn_turns[sel])
   if tc["debil"]:
    debil[sel]=np.where(dmg>0,tc["debil"][0],debil[sel])
    debil_turns[sel]=np.where(dmg>0,tc["debil"][1],debil_turns[sel])
   def_next[sel]=0

  win[(bhp<=0)&alive]=True
  sel=np.flatnonzero(alive&~win)
  if sel.size:
   if cycle==3: def_next[sel]=PATA_DEF_BONUS
   else:
    atk=BOSS_ATTACK+np.where(debil_turns[sel]>0,debil[sel],0)
    d20=rng.integers(1,21,size=sel.size,dtype=np.int16)
    hit=(d20==20)|((d20!=1)&(d20+atk>=p_def)); crit=hit&(d20==20)
    if cycle==2:
     dmg=rng.integers(1,7,size=(2,sel.size),dtype=np.int16).sum(axis=0)+2
    else:
     dmg=rng.integers(1,7,size=sel.size,dtype=np.int16)+2
    dmg=np.where(crit,np.ceil(dmg*1.5).astype(np.int16),dmg); dmg=np.where(hit,dmg,0)
    apply_guard(hp,sel,dmg,def1,def2,pguard,pcap)

  sel=np.flatnonzero(alive&~win&(burn_turns>0))
  if sel.size:
   bhp[sel]-=rng.integers(1,4,size=sel.size,dtype=np.int16); burn_turns[sel]-=1
   win[(bhp<=0)&alive]=True
  sel=np.flatnonzero(debil_turns>0)
  if sel.size:
   debil_turns[sel]-=1; debil[sel[debil_turns[sel]<=0]]=0
  alive[(hp<=0)&alive]=False

 return float(win.mean())

def run_models(models,configs,runs,mode):
 rows=[]; roots=list(ROOTS)
 for model in models:
  for root in roots:
   for o1 in range(1,4):
    for o2 in range(1,4):
     for p1,p2 in configs:
      pc=piel_conf(model,p1,p2)
      for boss_def in (13,14):
       seed=(sum(ord(c) for c in model)*1000003 +(roots.index(root)+1)*10000000+
             o1*1000000+o2*100000+(p1*4+p2)*1000+boss_def+(50000000 if mode=="confirm" else 0)) & 0xffffffff
       rows.append(dict(model=model,root=root,o1=o1,o2=o2,piel_t1=p1,piel_t2=p2,
         piel_name=config_name(p1,p2),piel_cost=pc["cost"],piel_guard=pc["guard"],
         piel_duration=pc["duration"],piel_capacity=pc["capacity"],boss_def=boss_def,
         winRate=simulate(model,root,o1,o2,p1,p2,boss_def,runs,seed)))
 return pd.DataFrame(rows)

def summarize(df):
 cfg=(df.groupby(["model","boss_def","piel_t1","piel_t2","piel_name","piel_cost","piel_guard","piel_duration","piel_capacity"])
        .winRate.agg(["mean","min","max"]).reset_index())
 best=(cfg.sort_values(["model","boss_def","mean"],ascending=[True,True,False])
       .groupby(["model","boss_def"]).head(1))
 print("\n=== MEJOR CONFIGURACIÓN POR MODELO / DEF ===")
 print(best.to_string(index=False))
 print("\n=== PIEL BASE POR MODELO ===")
 print(cfg[(cfg.piel_t1==0)&(cfg.piel_t2==0)].to_string(index=False))
 return cfg,best

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--mode",choices=("sensitivity","grid","confirm"),default="sensitivity")
 ap.add_argument("--model",choices=tuple(MODELS),default=None)
 ap.add_argument("--runs",type=int,default=None)
 ap.add_argument("--finalists",default="")
 args=ap.parse_args()

 if args.mode=="sensitivity":
  models=list(MODELS); configs=PIEL_CONFIGS; runs=args.runs or 2000
 elif args.mode=="grid":
  if not args.model: raise SystemExit("--mode grid requiere --model")
  models=[args.model]; configs=PIEL_CONFIGS; runs=args.runs or 5000
 else:
  if not args.model: raise SystemExit("--mode confirm requiere --model")
  configs=parse_finalists(args.finalists)
  if not configs: raise SystemExit("--mode confirm requiere --finalists")
  models=[args.model]; runs=args.runs or 20000

 print(f"mode={args.mode} runs={runs} models={models} configs={len(configs)}")
 df=run_models(models,configs,runs,args.mode)
 cfg,best=summarize(df)
 suffix=args.mode if args.mode=="sensitivity" else f"{args.model}_{args.mode}"
 df.to_csv(f"grulla_phase1_piel_rebalance_{suffix}_v0.1.csv",index=False)
 cfg.to_csv(f"grulla_phase1_piel_rebalance_{suffix}_configs_v0.1.csv",index=False)

if __name__=="__main__":
 main()
