import math, numpy as np, pandas as pd
from numba import njit
HP0=28; QI0=110; GAT=2; GDEF=7
GOLPE,TORM,CERRAR,RECORD,ECO=range(5)

@njit
def dice(n,f):
 s=0
 for _ in range(n): s+=np.random.randint(1,f+1)
 return s

@njit
def rs(root,o1,o2):
 if root==0: ra,rd,bc,nd,fd,fl=1,0,7,2,6,2
 elif root==1: ra,rd,bc,nd,fd,fl=2,0,6,1,10,3
 else: ra,rd,bc,nd,fd,fl=0,2,6,2,6,0
 c=bc;ab=0;cm=20;add=0;burn=0;de=0;dd=0
 if root==0:
  if o1==1: burn=2
  elif o1==2:add=1
  else:ab+=3
  if o2==1:c-=1
  elif o2==2:ab+=4
  else:cm=19
 elif root==1:
  if o1==1:ab+=3
  elif o1==2:add=1
  else:cm=19
  if o2==1:c-=1;cm=19
  elif o2==2:ab+=4
  else:de=-2;dd=1
 else:
  if o1==1:de=-1;dd=1
  elif o1==2:add=1
  else:ab+=3
  if o2==1:c-=1
  elif o2==2:ab+=4
  else:cm=19
 c=max(math.ceil(bc*.7),c-1)
 return ra,rd,c,nd,fd,fl+1,ab,cm,add,burn,de,dd

@njit
def hit(atk,df,crit=20,eva=0):
 r=np.random.randint(1,21)
 if r==1:return 0,0
 cr=1 if r>=crit else 0
 if r==20 or cr:return 1,cr
 return (1 if r+atk>=df+max(0,int(np.rint(eva/5.0))) else 0),0

@njit
def root_attack(root,o1,o2,patt,qi,bhp,burn,de,dt,defn=0,res=0,resper=3,eva=0):
 ra,rd,c,nd,fd,fl,ab,cm,add,rb,rde,rdd=rs(root,o1,o2)
 if qi<c:
  h,cr=hit(patt,13+defn,20,eva);d=0
  if h:
   d=dice(1,8);d=math.ceil(d*1.5) if cr else d
   if res>0:a=min(d,resper,res);d-=a;res-=a
   bhp-=d
  return qi,bhp,burn,de,dt,res,0
 qi-=c;h,cr=hit(patt+ab,13+defn,cm,eva);d=0
 if h:
  d=dice(nd,fd)+fl+(dice(1,4) if add else 0);d=math.ceil(d*1.5) if cr else d
  if res>0:a=min(d,resper,res);d-=a;res-=a
  bhp-=d
  if d>0 and rb:burn=2
  if d>0 and rde:de=rde;dt=rdd
 return qi,bhp,burn,de,dt,res,1

@njit
def phase1(tool,root,o1,o2,seed):
 np.random.seed(seed);ra,rd,tc,nd0,fd0,fl0,ab0,cm0,add0,b0,de0,dd0=rs(root,o1,o2);patt=1+ra+3+GAT;pdef=10+rd+GDEF
 hp=28;qi=110;pot=1;bhp=150;g1=g2=0;burn=de=dt=defn=0;pev=pt=pg=pc=0;reson=0;ten=tn=cd=0
 for r in range(1,81):
  if bhp<=0 or hp<=0:break
  cy=(r-1)%4; act=1
  if hp<=9 and pot:act=3
  elif cy==3:act=0
  elif cy==2:
   if tool==0:act=4 if qi>=5 else 2
   elif tool==1:act=1 if pc>0 else (5 if qi>=5 else 2)
   else:
    fc=5 if root==2 else 6;act=6 if ten<=0 and cd<=0 and qi>=fc else 2
  if act==1 and qi<tc:act=0
  skip=0;used=0
  if act==3:hp=min(28,hp+dice(3,6)+6);pot=0
  elif act==2:pg=pc=0;g1=np.random.randint(35,51);g2=np.random.randint(25,41);qi=min(110,qi+3)
  elif act==4:qi-=5;pev=25;pt=3
  elif act==5:qi-=5;g1=g2=0;pg=5;pc=10
  elif act==6:
   fc=5 if root==2 else 6;qi-=fc;used=1;cd=1;x=np.random.randint(1,21);ok=(x==20) or (x!=1 and x+patt+4>=15)
   if ok:bhp-=np.random.randint(1,4)+np.random.randint(1,5);ten=2;tn=1;skip=1
  elif act==0:
   h,cr=hit(patt,13+defn);d=0
   if h:d=dice(1,8);d=math.ceil(d*1.5) if cr else d;bhp-=d
   defn=0
  else:
   qi,bhp,burn,de,dt,_,_=root_attack(root,o1,o2,patt,qi,bhp,burn,de,dt,defn);defn=0
  if bhp<=0:break
  if cd>0 and not used:cd-=1
  if ten>0 and not tn:ten-=1
  tn=0
  if skip:pass
  elif cy==3:defn=3;reson=1 if tool==1 else reson
  else:
   h,cr=hit(4+(de if dt>0 else 0),pdef,20,pev if pt>0 else 0);d=0
   if h:d=dice(2,6)+2 if cy==2 else dice(1,6)+2;d=math.ceil(d*1.5) if cr else d
   if tool==1 and cy==0 and reson and d>0 and pc>0:d=math.ceil(d*1.75)
   if d>0 and pc>0:a=min(d,pg,pc);d-=a;pc-=a;pg=pg if pc>0 else 0
   elif d>0 and g1>0:d-=math.floor(d*g1/100);g1=g2;g2=0
   elif d>0 and g2>0:d-=math.floor(d*g2/100);g2=0
   hp-=d
   if cy==0:reson=0
  if burn>0 and bhp>0:bhp-=np.random.randint(1,4);burn-=1
  if dt>0:dt-=1;de=0 if dt<=0 else de
  if pt>0:pt-=1;pev=0 if pt<=0 else pev
 return (1 if bhp<=0 and hp>0 else 0),max(0,hp),qi,pot,g1,g2

@njit
def recent(a,n,x,d):
 for i in range(max(0,n-d),n):
  if a[i]==x:return 1
 return 0

@njit
def intent(ht,hk,hq,hb,n,ri,rn,hp,qi,bhp):
 t1=ht[n-1] if n else -1;t2=ht[n-2] if n>1 else -1;k1=hk[n-1] if n else -1;k2=hk[n-2] if n>1 else -1
 rep=n>1 and k1>=0 and k1==k2;off=n>1 and t1<=2 and t2<=2;qs=n>1 and hq[n-1]>0 and hq[n-2]>0
 heavy=0
 for j in range(max(0,n-2),n):heavy=max(heavy,1 if hb[j]>=2 else 0)
 sc=np.zeros(5);jit=np.array([1.,1.,.8,.6,.6]);sc[0]=30;sc[1]=28+(12 if qi>=72 else 0)+(10 if hp<=8 else 0)-(40 if recent(ri,rn,1,2) else 0);sc[2]=18+(18 if off else 0)+(20 if heavy else 0)+(16 if bhp<=30 else 0)-(35 if recent(ri,rn,2,2) else 0);sc[3]=12+(38 if rep else 0)-(42 if recent(ri,rn,3,2) else 0);sc[4]=12+(34 if qs else 0)+(8 if qi<=27 else 0)-(40 if recent(ri,rn,4,2) else 0)
 b=0;bv=-1e9
 for i in range(5):
  v=sc[i]+(np.random.random()-.5)*jit[i]
  if v>bv:bv=v;b=i
 return b

@njit
def phase2(tool,root,o1,o2,seed,hp,qi,pot,g1,g2,useopt):
 np.random.seed(seed);ra,rd,tc,nd0,fd0,fl0,ab0,cm0,add0,b0,de0,dd0=rs(root,o1,o2);patt=1+ra+3+GAT;pdef=10+rd+GDEF;bhp=100;res=evn=burn=de=dt=0;pev=pt=pg=pc=ten=tn=cd=0
 ht=np.full(8,-1,np.int8);hk=np.full(8,-1,np.int8);hq=np.zeros(8,np.int16);hb=np.zeros(8,np.int8);n=0;ri=np.full(4,-1,np.int8);rn=0;locked=-1
 for r in range(1,81):
  if bhp<=0 or hp<=0:break
  it=intent(ht,hk,hq,hb,n,ri,rn,hp,qi,bhp)
  if hp<=9 and pot:act=4
  elif locked>=0 or evn>0 or it==ECO:act=0
  elif it==TORM and hp<=14:
   if useopt==1 and tool==0 and qi>=5:act=2
   elif useopt==1 and tool==1 and qi>=5 and pc<=0:act=2
   elif useopt==1 and tool==2 and qi>=(5 if root==2 else 6) and ten<=0 and cd<=0:act=2
   else:act=3
  else:
   last=hk[n-1] if n else -1;act=1 if qi>=tc and last!=0 else 0
  qsp=0;tid=-1;band=0;skip=0;used=0
  if act==4:hp=min(28,hp+dice(3,6)+6);pot=0
  elif act==3:pg=pc=0;g1=np.random.randint(35,51);g2=np.random.randint(25,41);qi=min(110,qi+3)
  elif act==2:
   tid=1;blocked=(locked==1)
   if tool==0:qi-=5;qsp=5;pev=pev if blocked else 25;pt=pt if blocked else 3
   elif tool==1:qi-=5;qsp=5;pg=pg if blocked else 5;pc=pc if blocked else 10
   else:
    fc=5 if root==2 else 6;qi-=fc;qsp=fc;used=1;cd=1
    if not blocked:
     x=np.random.randint(1,21);ok=(x==20) or (x!=1 and x+patt+4>=15)
     if ok:bhp-=np.random.randint(1,4)+np.random.randint(1,5);ten=2;tn=1;skip=1
  elif act==0:
   h,cr=hit(patt,13,20,evn);d=0
   if h:d=dice(1,8);d=math.ceil(d*1.5) if cr else d;a=min(d,3,res) if res>0 else 0;d-=a;res-=a;bhp-=d;band=2 if d>=8 else 1
   locked=-1;evn=0
  else:
   tid=0;qsp=tc;qi-=tc;blocked=(locked==0)
   if not blocked:
    z=root_attack(root,o1,o2,patt,qi+tc,bhp,burn,de,dt,0,res,3,evn);qi,bhp,burn,de,dt,res,_=z
   evn=0
  if n<8:pos=n;n+=1
  else:ht[:-1]=ht[1:];hk[:-1]=hk[1:];hq[:-1]=hq[1:];hb[:-1]=hb[1:];pos=7
  ht[pos]=act;hk[pos]=tid;hq[pos]=qsp;hb[pos]=band
  if locked>=0:
   if act==0 or (tid>=0 and tid!=locked):locked=-1
  elif n>=3 and hk[n-1]>=0 and hk[n-1]==hk[n-2] and hk[n-2]==hk[n-3]:locked=hk[n-1]
  if bhp<=0:break
  if cd>0 and not used:cd-=1
  if ten>0 and not tn:ten-=1
  tn=0
  if not skip:
   d=0
   if it==GOLPE:
    h,cr=hit(4+(de if dt>0 else 0),pdef,20,pev if pt>0 else 0);d=dice(1,4) if h else 0;d=math.ceil(d*1.5) if h and cr else d
   elif it==TORM:
    h,cr=hit(4+(de if dt>0 else 0),pdef,20,pev if pt>0 else 0);d=dice(1,6)+1 if h else 0;d=math.ceil(d*1.5) if h and cr else d;qi=max(0,qi-1) if d>0 else qi
   elif it==CERRAR:res=6
   elif it==RECORD:evn=10
   else:qi=max(0,qi-3) if qsp>0 else qi
   if d>0:
    if pc>0:a=min(d,pg,pc);d-=a;pc-=a;pg=pg if pc>0 else 0
    elif g1>0:d-=math.floor(d*g1/100);g1=g2;g2=0
    elif g2>0:d-=math.floor(d*g2/100);g2=0
    hp-=d
  if burn>0 and bhp>0:bhp-=np.random.randint(1,4);burn-=1
  if dt>0:dt-=1;de=0 if dt<=0 else de
  if pt>0:pt-=1;pev=0 if pt<=0 else pev
  if rn<4:ri[rn]=it;rn+=1
  else:ri[:-1]=ri[1:];ri[3]=it
 return 1 if bhp<=0 and hp>0 else 0

@njit
def scenario(n,seed,tool,root,o1,o2,useopt):
 reach=win=0;eh=eq=ep=0.
 for i in range(n):
  s=seed+i*1009+31;p=phase1(tool,root,o1,o2,s)
  if p[0]:
   reach+=1;eh+=p[1];eq+=p[2];ep+=p[3];win+=phase2(tool,root,o1,o2,s^0x5A5A5A5A,p[1],p[2],p[3],p[4],p[5],useopt)
 return reach/n,(win/reach if reach else 0),win/n,(eh/reach if reach else 0),(eq/reach if reach else 0),(ep/reach if reach else 0)

scenario(2,1,0,0,1,1,1)
rows=[];runs=20000
for tool in range(3):
 for root in range(3):
  for o1 in range(1,4):
   for o2 in range(1,4):
    z=scenario(runs,(tool+1)*100000000+(root+1)*1000000+o1*10000+o2*100,tool,root,o1,o2,1)
    rows.append((tool,root,o1,o2,*z))
df=pd.DataFrame(rows,columns="tool root o1 o2 reach cond total entryHp entryQi entryPot".split())
print(df.groupby("tool")[["reach","cond","total","entryHp","entryQi","entryPot"]].mean().to_string())
print("\nby root")
print(df.groupby(["tool","root"])[["reach","cond","total"]].mean().to_string())
print("\nranges")
print(df.groupby("tool")["cond"].agg(["min","max"]).to_string())
