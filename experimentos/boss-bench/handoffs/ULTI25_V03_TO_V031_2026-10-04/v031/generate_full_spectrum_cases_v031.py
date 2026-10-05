#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, random
from pathlib import Path
HERE=Path(__file__).resolve().parent
MODES=json.loads((HERE/"ULTI25_MODE_INDEX_V02.json").read_text(encoding="utf-8"))
MATRIX=json.loads((HERE/"ULTI25_FULL_SPECTRUM_MATRIX_V031.json").read_text(encoding="utf-8"))
FAM=lambda u:"FUEGO" if u.startswith("FIRE_") else "METAL" if u.startswith("METAL_") else "AGUA" if u.startswith("WATER_") else "TIERRA" if u.startswith("EARTH_") else "VIENTO"

def seed_of(*parts):
    return int.from_bytes(hashlib.sha256("|".join(map(str,parts)).encode()).digest()[:8],"big")
def cid(c):
    return hashlib.sha256(json.dumps(c,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()[:24]
def add(out,suite,**kw):
    c={"suite":suite,**kw};c["case_id"]=cid(c);out.append(c)

def build_local_acceptance():
    out=[];eq="EXPECTED_STAGE";ps="FULL";windows=MATRIX["critical_local_windows"]
    # Every one of the 38 accepted semantic modes in critical F1/F2/F3 windows.
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for w in windows:
        add(out,"LOCAL_MODE_CRITICAL",ultimate=u,family=fam,mode=mode,window=w,player_state=ps,equipment_profile=eq,seed=seed_of("LOCAL_MODE",u,mode,w),progression_mode="MECHANICAL_STRESS")
    # Rejected Río paired causal-equivalence probe.
    s=seed_of("LOCAL_RIO_REJECT")
    pair="LOCAL_RIO_REJECT_EQUIV"
    add(out,"CORE_CONTINUOUS",ultimate="WIND_RIO_CELESTE_SIN_ORILLAS",family="VIENTO",mode="FULL",window="F1_EARLY",player_state="FULL",equipment_profile=eq,seed=s,pair_id=pair,arm="ULTI",progression_mode="MECHANICAL_STRESS")
    add(out,"PAIRED_BASELINE",ultimate=None,family="VIENTO",mode="NO_ULTI",window="F1_EARLY",player_state="FULL",equipment_profile=eq,seed=s,pair_id=pair,arm="BASELINE",progression_mode="MECHANICAL_STRESS")
    # Every cooldown edge for all 25 Ultis.
    for u,modes in MODES.items():
      fam=FAM(u)
      for edge in MATRIX["activation_edges"]:
       add(out,"ACTIVATION_COOLDOWN",ultimate=u,family=fam,mode=modes[0],window="F1_EARLY",player_state="FULL",equipment_profile=eq,activation_edge=edge,seed=seed_of("LOCAL_CD",u,edge),progression_mode="MECHANICAL_STRESS")
    # Every transition edge at both F1->F2 and F2->F3.
    for edge in MATRIX["transition_edges"]:
      for ph in MATRIX.get("transition_phases",["F1","F2"]):
       add(out,"PHASE_TRANSITION",ultimate=None,family="FUEGO",mode="NO_ULTI",window="TRANSITION_EDGE",player_state="BALANCED",equipment_profile=eq,transition_edge=edge,transition_phase=ph,seed=seed_of("LOCAL_TR",edge,ph),progression_mode="MECHANICAL_STRESS",transition_fixture="V031_EXPLICIT_TRANSITION_STRESS")
    return out


def build(preset):
    if preset=="local_acceptance": return build_local_acceptance()
    cfg=MATRIX["presets"][preset]; reps=cfg["core_reps"]; out=[]
    windows=MATRIX["continuous_windows"];states=MATRIX["player_states"];eqs=MATRIX["equipment_profiles"]
    # Core treatment + exact paired baseline for every semantic scenario.
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for w in windows:
        for ps in states:
         for eq in eqs:
          for rep in range(reps):
           s=seed_of("PAIR",u,mode,w,ps,eq,rep)
           pair=f"{u}|{mode}|{w}|{ps}|{eq}|{rep}"
           add(out,"CORE_CONTINUOUS",ultimate=u,family=fam,mode=mode,window=w,player_state=ps,equipment_profile=eq,replicate=rep,seed=s,pair_id=pair,arm="ULTI",progression_mode="MECHANICAL_STRESS")
           add(out,"PAIRED_BASELINE",ultimate=None,family=fam,mode="NO_ULTI",window=w,player_state=ps,equipment_profile=eq,replicate=rep,seed=s,pair_id=pair,arm="BASELINE",progression_mode="MECHANICAL_STRESS")
    # Exact resource boundaries.
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for qb in MATRIX["qi_boundaries"]:
        for eq in eqs:
         for rep in range(max(1,reps//2)):
          add(out,"QI_BOUNDARY",ultimate=u,family=fam,mode=mode,window="F2_ENTRY",player_state="FULL",equipment_profile=eq,qi_boundary=qb,replicate=rep,seed=seed_of("QI",u,mode,qb,eq,rep),progression_mode="MECHANICAL_STRESS")
       for hb in MATRIX["hp_boundaries"]:
        for rep in range(max(1,reps//2)):
         add(out,"HP_BOUNDARY",ultimate=u,family=fam,mode=mode,window="F3_ENTRY",player_state="FULL",equipment_profile="EXPECTED_STAGE",hp_boundary=hb,replicate=rep,seed=seed_of("HP",u,mode,hb,rep),progression_mode="MECHANICAL_STRESS")
    # One-use / OOC exact boundary.
    for u in MODES:
      fam=FAM(u)
      for edge in MATRIX["activation_edges"]:
       for eq in eqs:
        for rep in range(max(1,reps//2)):
         add(out,"ACTIVATION_COOLDOWN",ultimate=u,family=fam,mode=MODES[u][0],window="F1_EARLY",player_state="FULL",equipment_profile=eq,activation_edge=edge,replicate=rep,seed=seed_of("ACT",u,edge,eq,rep),progression_mode="MECHANICAL_STRESS")
    # Phase-boundary attacks / persistence.
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for edge in MATRIX["transition_edges"]:
        for ph in MATRIX.get("transition_phases",["F1","F2"]):
         for rep in range(max(1,reps//2)):
          add(out,"PHASE_TRANSITION",ultimate=u,family=fam,mode=mode,window="TRANSITION_EDGE",player_state="BALANCED",equipment_profile="EXPECTED_STAGE",transition_edge=edge,transition_phase=ph,transition_fixture="V031_EXPLICIT_TRANSITION_STRESS",replicate=rep,seed=seed_of("TR",u,mode,edge,ph,rep),progression_mode="MECHANICAL_STRESS")
    # CRN boss-axis stress: same seed across arms.
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for rep in range(max(1,reps//2)):
        s=seed_of("BOSS_STRESS",u,mode,rep)
        for bp in MATRIX["boss_numeric_stress"]:
         add(out,"BOSS_CRN_STRESS",ultimate=u,family=fam,mode=mode,window="F3_ENTRY",player_state="BALANCED",equipment_profile="EXPECTED_STAGE",boss_stress=bp,replicate=rep,seed=s,stress_pair=f"{u}|{mode}|{rep}",progression_mode="MECHANICAL_STRESS")
    # AOE target topology (synthetic adds, mechanics only).
    for u,modes in MODES.items():
      fam=FAM(u)
      for mode in modes:
       for top in MATRIX["target_topologies"]:
        for rep in range(max(1,reps//2)):
         add(out,"TARGET_TOPOLOGY",ultimate=u,family=fam,mode=mode,window="F2_ENTRY",player_state="FULL",equipment_profile="NAKED",target_topology=top,replicate=rep,seed=seed_of("AOE",u,mode,top,rep),progression_mode="MECHANICAL_STRESS")
    # Reproducible property fuzz.
    for u,modes in MODES.items():
      fam=FAM(u);rr=random.Random(seed_of("FUZZ",preset,u))
      for i in range(cfg["fuzz_per_ulti"]):
       add(out,"PROPERTY_FUZZ",ultimate=u,family=fam,mode=modes[rr.randrange(len(modes))],window=windows[rr.randrange(len(windows))],player_state=states[rr.randrange(len(states))],equipment_profile=eqs[rr.randrange(len(eqs))],fuzz_token=rr.getrandbits(63),replicate=i,seed=seed_of("FUZZCASE",u,i),progression_mode="MECHANICAL_STRESS")
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--preset",choices=("local_acceptance","quick","standard","deep"),default="quick");ap.add_argument("--out",default="FULL_SPECTRUM_CASES_V031.jsonl");a=ap.parse_args()
    cs=build(a.preset)
    with Path(a.out).open("w",encoding="utf-8") as f:
      for c in cs:f.write(json.dumps(c,ensure_ascii=False,separators=(",",":"))+"\n")
    by={}
    for c in cs:by[c["suite"]]=by.get(c["suite"],0)+1
    print(json.dumps({"preset":a.preset,"cases":len(cs),"by_suite":by,"out":a.out},indent=2))
if __name__=="__main__":main()
