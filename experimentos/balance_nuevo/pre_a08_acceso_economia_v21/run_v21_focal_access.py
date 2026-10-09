#!/usr/bin/env python3
"""V21 PRE-A08: focal LI carry-over and M03 design-reference against six LII normal monsters.
NOT a proof of acquisition: the analyzed ver74 has QUESTS={} and CATALOGO=[].
V17 skills; representative BASE scalar Concordance only. No antivenom simulation in bridge.
T0/T1/T2 adaptation (not cultivation), 5 roots, 16 builds, two policies, paired CRN.
V19 knobs only vary for cangrejo/jabali in T1/T2. Non-canonical, no HTML edit.
"""
from __future__ import annotations
import argparse,copy,csv,gzip,hashlib,json,time
from pathlib import Path
import pandas as pd
import run_v20 as b

HERE=Path(__file__).resolve().parent
GEARS={'PROLOGUE_DESIGN':b.A,'M03_ISSUED_DESIGN':b.M}
METRICS=['win','rounds','hp_final_pct','qi_final','qi_spent','def_casts','foreign_casts',
         'resolutions','due_missed','timeout','seed','def_absorbed','def_prevented',
         'evades','source_attempt','defense_attempt']
FIELDS=['cohort','monster','root','foreign','tier','policy','build','rep','kit','monster_arm']+METRICS

def arms(monster,tier):
    return ('ORIGINAL','CANDIDATE_V19') if monster in b.v19.KNOBS and tier in ('T1','T2') else ('ORIGINAL',)

def run(cohort,start,reps):
    assert cohort in ('DISCOVERY','HOLDOUT') and reps>0
    assert tuple(b.f.MONSTERS)==tuple(b.f.ref.G['freeze']['T1']['species'])[:len(b.f.MONSTERS)] or len(b.f.MONSTERS)==6
    b.tech.ACTIVE[0]='SKILLS_V17'
    frozen=b.f.ref.G['freeze']['T1']['species']
    original={m:copy.deepcopy(frozen[m]['ability']) for m in b.f.MONSTERS}
    sel=b.f.ref.selected_gear
    count=0;start_time=time.monotonic()
    outfile=HERE/f'RAW_V21_{cohort}.csv.gz'
    try:
        with gzip.open(outfile,'wt',newline='',compresslevel=4) as fh:
            w=csv.DictWriter(fh,fieldnames=FIELDS);w.writeheader()
            for mon in b.f.MONSTERS:
                for root in b.f.ROOTS:
                    foreign=b.REP_FOREIGN[root]
                    assert b.v19.REL[b.v.v04b.relation_id(foreign,root)]['kind']=='SCALAR'
                    for tier in b.TIERS:
                        for pol in b.POLICIES:
                            for bid,paths in b.BUILDS[root].items():
                                for rep in range(start,start+reps):
                                    for kit,items in GEARS.items():
                                        for arm in arms(mon,tier):
                                            b.f.ref.selected_gear=lambda label,ids=items:ids
                                            frozen[mon]['ability']=copy.deepcopy(original[mon])
                                            if arm=='CANDIDATE_V19':
                                                key,old,new=b.v19.KNOBS[mon]
                                                assert frozen[mon]['ability'][key]==old
                                                frozen[mon]['ability'][key]=new
                                            z=b.v.fighter(mon,root,foreign,b.SEED_GEAR,tier,bid,paths,rep,pol,'FRACTION_100')
                                            assert z['due_missed']==z['timeout']==0,(mon,root,tier,kit,arm,z)
                                            w.writerow(dict(cohort=cohort,monster=mon,root=root,foreign=foreign,
                                                        tier=tier,policy=pol,build=bid,rep=rep,kit=kit,
                                                        monster_arm=arm,**z))
                                            count+=1
                print('DONE',cohort,mon,count,'elapsed',round(time.monotonic()-start_time,2),'sec',flush=True)
    finally:
        b.f.ref.selected_gear=sel
        for mon in original:frozen[mon]['ability']=original[mon]
    assert all(frozen[m]['ability']==original[m] for m in original)
    expected=sum(len(arms(m,t)) for m in b.f.MONSTERS for t in b.TIERS)*len(b.f.ROOTS)*len(b.POLICIES)*16*reps*len(GEARS)
    assert count==expected,(count,expected)
    d=pd.read_csv(outfile)
    key=['monster','root','tier','policy','build','rep','kit']
    assert len(d)==count and not d.duplicated(key+['monster_arm']).any()
    paired=d.groupby(key,sort=False)
    assert (paired.seed.nunique()==1).all(),'Seed mismatch across monster arms'
    gear_key=['monster','root','tier','policy','build','rep','monster_arm']
    assert (d.groupby(gear_key,sort=False).seed.nunique()==1).all(),'Seed mismatch across gear kits'
    assert d.timeout.sum()==d.due_missed.sum()==0
    assert not (d.qi_final<0).any()
    out=(d.groupby(['monster','tier','kit','monster_arm'],as_index=False)
          .agg(n=('win','size'),player_wr_pct=('win',lambda v:round(100*v.mean(),4)),
               qi_spent_mean=('qi_spent','mean'),qi_final_mean=('qi_final','mean'),
               hp_final_pct_mean=('hp_final_pct','mean'),rounds_mean=('rounds','mean')))
    path=HERE/f'SUMMARY_V21_{cohort}.csv';out.to_csv(path,index=False)
    sha={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in (outfile,path)}
    qa={'status':'PASS_FOCAL_LAB_NOT_CANON','cohort':cohort,'seed_start':start,'reps':reps,
        'fights':count,'six_normal_monsters':len(b.f.MONSTERS),'tiers':list(b.TIERS),'roots':len(b.f.ROOTS),
        'builds_per_root':16,'policies':list(b.POLICIES),'kits':list(GEARS),
        'concordance':'V17 one representative scalar BASE per root',
        'candidate_arms':'only cangrejo/jabali T1/T2',
        'material_economy_simulated':False,'antidotes_simulated':False,
        'affliction_simulated':False,'qi_spend_metrics':True,
        'due_missed':0,'timeouts':0,'seed_match':True,'mutable_abilities_restored':True,
        'availability_limitation':'PROLOGUE/M03 are design references; new LII pieces not verified in ver74 runtime',
        'files_sha256':sha}
    (HERE/f'QA_V21_{cohort}.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
    print('QA',json.dumps(qa,ensure_ascii=False),flush=True)
    print('T2 summary\n',out[out.tier=='T2'].to_string(index=False),flush=True)
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--cohort',required=True,choices=['DISCOVERY','HOLDOUT'])
    ap.add_argument('--start',required=True,type=int)
    ap.add_argument('--reps',type=int,default=2)
    a=ap.parse_args();run(a.cohort,a.start,a.reps)
