#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,importlib.util,json,math,hashlib,sys
from pathlib import Path

def load(path):
 p=Path(path);spec=importlib.util.spec_from_file_location("runner",p);m=importlib.util.module_from_spec(spec);sys.modules["runner"]=m;spec.loader.exec_module(m);return m,p
def scalars(x,prefix=""):
 if isinstance(x,dict):
  for k,v in x.items():yield from scalars(v,prefix+"."+str(k) if prefix else str(k))
 elif isinstance(x,(list,tuple)):
  for i,v in enumerate(x):yield from scalars(v,f"{prefix}[{i}]")
 elif isinstance(x,(int,float)) and not isinstance(x,bool):yield prefix,float(x)

def issues_for(c,r):
 out=[];suite=c.get("suite")
 if r.get("error"):out.append("simulation_error")
 for k,v in scalars(r):
  if not math.isfinite(v):out.append("nonfinite_metric:"+k)
 for k in ("player_hp_end","player_qi_end","boss_hp_end","boss_abs_end"):
  if isinstance(r.get(k),(int,float)) and r[k]<-1e-9:out.append("negative:"+k)
 if float(r.get("ultimate_uses",0) or 0)>1:out.append("ultimate_uses_gt_1")
 if float(r.get("f3_kill_before_first_real_action",0) or 0)>0:out.append("f3_kill_before_first_real_action")
 if float(r.get("f3_pact_release_count",0) or 0)>1:out.append("pact_release_count_gt_1")
 if c.get("window")=="F3_CONTROL_DENIED_FIRST_INTENT" and r.get("phase_end")=="F3":
  if int(r.get("f3_first_denied_observed",0) or 0)<1:out.append("first_control_denied_probe_not_observed")
  if int(r.get("pact_active_after_first_denied",0) or 0)!=1:out.append("pact_released_by_first_denied_intent")
 # Scope cooldown contracts by suite + activation_edge. Do not demand unrelated telemetry.
 if suite=="ACTIVATION_COOLDOWN":
  edge=c.get("activation_edge")
  if edge=="FIRST_USE" and int(r.get("ultimate_uses",0) or 0)!=1:out.append("contract_first_use")
  elif edge=="SECOND_USE_SAME_COMBAT" and int(r.get("reactivation_blocked",0) or 0)!=1:out.append("contract_second_use")
  elif edge=="OOC_39" and bool(r.get("cooldown_ready")):out.append("contract_ooc39")
  elif edge in ("OOC_40","OOC_41") and not bool(r.get("cooldown_ready")):out.append("contract_ooc40plus")
 elif int(r.get("reactivation_probe_performed",0) or 0)==1:
  if int(r.get("reactivation_blocked",0) or 0)!=1:out.append("second_activation_not_blocked")
  if int(r.get("ooc_ready_39",0) or 0)!=0:out.append("ooc_ready_too_early")
  if int(r.get("ooc_ready_40",0) or 0)!=1:out.append("ooc_not_ready_at_40")
  if int(r.get("ooc_ready_41",0) or 0)!=1:out.append("ooc_not_ready_at_41")
 if suite=="PHASE_TRANSITION":
  if int(r.get("transition_edge_observed",0) or 0)!=1:out.append("transition_edge_not_observed")
  if int(r.get("transition_edge_pass",0) or 0)!=1:out.append("transition_edge_contract_failed")
  if bool(r.get("balance_authoritative",False)):out.append("transition_fixture_marked_balance_authoritative")
 return sorted(set(out))

def flatten(c,r):
 um=r.get("ultimate_metrics") or {}
 return {
  "case_id":c["case_id"],"suite":c["suite"],"pair_id":c.get("pair_id",""),"arm":c.get("arm",""),
  "ultimate":c.get("ultimate"),"family":c.get("family"),"mode":c.get("mode"),"window":c.get("window"),
  "transition_edge":c.get("transition_edge"),"transition_phase":c.get("transition_phase"),"activation_edge":c.get("activation_edge"),
  "player_state":c.get("player_state"),"equipment_profile":c.get("equipment_profile"),"seed":c.get("seed"),
  "outcome":r.get("outcome"),"phase_end":r.get("phase_end"),"rounds_total":r.get("rounds_total",0),
  "player_hp_end":r.get("player_hp_end",0),"player_qi_end":r.get("player_qi_end",0),"boss_hp_end":r.get("boss_hp_end",0),"boss_abs_end":r.get("boss_abs_end",0),
  "ultimate_uses":r.get("ultimate_uses",0),"activation_reason":r.get("ultimate_activation_reason",""),
  "damage_total":um.get("damage_total",0),"ultimate_damage_direct":um.get("ultimate_damage_direct",0),"turns_denied":um.get("turns_denied",0),
  "hp_healed":um.get("hp_healed",0),"qi_restored":um.get("qi_restored",0),"qi_saved":um.get("qi_saved",0),"absorption_granted":um.get("absorption_granted",0),
  "climax":um.get("climax",0),"mechanic_success":um.get("mechanic_success",0),"duration_violation":um.get("duration_violation",0),"aoe_scalar_violation":um.get("aoe_scalar_violation",0),
  "f3_lethal_preventions":r.get("f3_lethal_preventions",0),"f3_prevented_lethal_damage":r.get("f3_prevented_lethal_damage",0),
  "f3_first_denied_observed":r.get("f3_first_denied_observed",0),"pact_active_after_first_denied":r.get("pact_active_after_first_denied",0),
  "transition_edge_observed":r.get("transition_edge_observed",0),"transition_edge_pass":r.get("transition_edge_pass",0),
  "synthetic_enemy_control_suppressed":r.get("synthetic_enemy_control_suppressed",0),
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--cases",required=True);ap.add_argument("--runner",required=True);ap.add_argument("--out",default="CONTINUOUS_FULL_SPECTRUM_V031");ap.add_argument("--max-cases",type=int,default=0);a=ap.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);runner,rp=load(a.runner);auth=runner.authority_report()
 selfcheck=runner.self_check() if callable(getattr(runner,"self_check",None)) else {"pass":False,"errors":["RUNNER_SELFCHECK_MISSING"]}
 (out/"runner_self_check.json").write_text(json.dumps(selfcheck,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 if not selfcheck.get("pass"):
  summary={"pass":False,"status":"RUNNER_SELFCHECK_FAIL","authority_report":auth,"self_check":selfcheck,"mass_run_allowed":False}
  (out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2));return 5
 rows=[];issue_rows=[];raw=[];n=0
 for line in Path(a.cases).read_text(encoding="utf-8").splitlines():
  if not line.strip():continue
  if a.max_cases and n>=a.max_cases:break
  c=json.loads(line);n+=1
  try:r=runner.run_case(c);iss=issues_for(c,r)
  except Exception as e:r={"error":repr(e)};iss=["simulation_exception"]
  row=flatten(c,r);row["issues"]=";".join(iss);rows.append(row)
  raw.append({"case":c,"result":r,"issues":iss})
  for x in iss:issue_rows.append({"case_id":c["case_id"],"suite":c["suite"],"issue":x})
 # Strong causal oracle for rejected Río: treatment must equal paired baseline in all combat state/trace fields.
 row_by_case={x["case_id"]:x for x in rows}
 raw_by_pair={}
 for item in raw:
  pid=item["case"].get("pair_id");arm=item["case"].get("arm")
  if pid and arm:raw_by_pair.setdefault(pid,{})[arm]=item
 for pid,d in raw_by_pair.items():
  if "ULTI" not in d or "BASELINE" not in d:continue
  ui,bi=d["ULTI"],d["BASELINE"];uc,ur=ui["case"],ui["result"];br=bi["result"]
  if uc.get("ultimate")=="WIND_RIO_CELESTE_SIN_ORILLAS" and ur.get("ultimate_activation_reason")=="IMPLEMENTATION_REJECTED":
   if callable(getattr(runner,"_rio_equivalence_signature",None)):
    same=runner._rio_equivalence_signature(ur)==runner._rio_equivalence_signature(br)
   else:
    keys=("outcome","phase_end","rounds_total","player_hp_end","player_qi_end","boss_hp_end","boss_abs_end","phase_trace","phase_transitions","player_actions","boss_actions","player_actions_by_phase","boss_actions_by_phase","causal_trace","brain_state_hash")
    same=all(ur.get(k)==br.get(k) for k in keys)
   if not same:
    issue="rio_rejected_not_baseline_equivalent";ui["issues"].append(issue);issue_rows.append({"case_id":uc["case_id"],"suite":uc["suite"],"issue":issue})
    row=row_by_case.get(uc["case_id"])
    if row:row["issues"]=";".join(sorted(set(filter(None,(row.get("issues",""),issue)))))
 # paired mechanical deltas; explicitly not canonical balance
 bypair={}
 for row in rows:
  if row["pair_id"]:bypair.setdefault(row["pair_id"],{})[row["arm"]]=row
 deltas=[]
 for pid,d in bypair.items():
  if "ULTI" in d and "BASELINE" in d:
   u,b=d["ULTI"],d["BASELINE"]
   deltas.append({"pair_id":pid,"ultimate":u["ultimate"],"mode":u["mode"],"window":u["window"],"player_state":u["player_state"],"equipment_profile":u["equipment_profile"],
    "delta_player_hp_end":float(u["player_hp_end"])-float(b["player_hp_end"]),"delta_player_qi_end":float(u["player_qi_end"])-float(b["player_qi_end"]),
    "delta_boss_hp_end":float(u["boss_hp_end"])-float(b["boss_hp_end"]),"delta_rounds":float(u["rounds_total"])-float(b["rounds_total"]),
    "baseline_outcome":b["outcome"],"ulti_outcome":u["outcome"],"mechanical_only":True})
 def writecsv(path,data):
  if not data:path.write_text("",encoding="utf-8");return
  keys=list(data[0]); 
  with path.open("w",encoding="utf-8-sig",newline="") as f:w=csv.DictWriter(f,fieldnames=keys,extrasaction="ignore");w.writeheader();w.writerows(data)
 writecsv(out/"results.csv",rows);writecsv(out/"issues.csv",issue_rows);writecsv(out/"paired_mechanical_deltas.csv",deltas)
 balance_flags=[{"ultimate":"METAL_SENTENCIA_FILO_CELESTIAL","flag":"BALANCE_PRIORITY","action":"HUMAN_REVIEW_ONLY_NO_AUTO_NERF_OR_BUFF","authority":False}]
 (out/"balance_flags.json").write_text(json.dumps(balance_flags,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 (out/"raw_results.json").write_text(json.dumps(raw,ensure_ascii=False),encoding="utf-8")
 summary={"pass":not issue_rows,"status":"PASS" if not issue_rows else "FAIL","cases_executed":n,"hard_issue_count":len(issue_rows),
  "paired_rows":len(deltas),"runner_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),"authority_report":auth,"self_check":selfcheck,
  "balance_authoritative":False,"mechanical_progression_fixture":True,"mass_run_allowed":False,"balance_priority":["METAL_SENTENCIA_FILO_CELESTIAL"],"automatic_balance_changes":False}
 (out/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,ensure_ascii=False,indent=2));return 0 if not issue_rows else 2
if __name__=="__main__":raise SystemExit(main())
