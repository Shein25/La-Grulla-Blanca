"""Streaming aggregates for parallel Arc1 labs. Raw fight rows are never persisted."""
from __future__ import annotations
from collections import Counter,defaultdict
import statistics

def percentile(values,q):
    xs=sorted(float(x) for x in values)
    if not xs:return 0.0
    pos=(len(xs)-1)*q
    lo=int(pos);hi=min(lo+1,len(xs)-1);f=pos-lo
    return xs[lo]*(1-f)+xs[hi]*f

class StreamingAggregate:
    def __init__(self):
        self.n=0;self.wins=0;self.losses=0;self.timeouts=0
        self.rounds=[];self.hp=[];self.hpmin=[];self.qi=[];self.damage=[]
        self.sum=Counter()
        self.root=defaultdict(lambda:{"fights":0,"wins":0,"hp":0.0,"qi":0.0})
        self.loadout=defaultdict(lambda:{"fights":0,"wins":0,"hp":0.0,"qi":0.0})

    def add(self,r):
        self.n+=1
        self.wins+=int(bool(r["win"]));self.losses+=int(bool(r["loss"]));self.timeouts+=int(bool(r["timeout"]))
        self.rounds.append(float(r["rounds"]))
        self.hp.append(float(r["player_hp_final_pct"]))
        self.hpmin.append(float(r["player_hp_min_pct"]))
        self.qi.append(float(r["player_qi_final"]))
        for k in ("player_qi_spent","player_qi_drained","defensive_activations","monster_skill_uses","monster_basic_uses","monster_skipped_actions","forced_basic_due_to_qi","monster_dot_damage","monster_basic_damage","monster_skill_direct_damage"):
            self.sum[k]+=float(r.get(k,0))
        m=r["metrics"]
        for k in ("player_attempts","player_hits","monster_attempts","monster_hits","control_attempts","control_successes","monster_evades"):
            self.sum[k]+=float(m.get(k,0))
        total=float(r.get("monster_dot_damage",0))+float(r.get("monster_basic_damage",0))+float(r.get("monster_skill_direct_damage",0))
        self.damage.append(total)
        for store,key in ((self.root,r["root"]),(self.loadout,r["loadout_profile"])):
            x=store[key];x["fights"]+=1;x["wins"]+=int(bool(r["win"]));x["hp"]+=float(r["player_hp_final_pct"]);x["qi"]+=float(r["player_qi_final"])

    def _breakdown(self,d):
        return {k:{
            "fights":v["fights"],"win_rate":v["wins"]/v["fights"],
            "hp_final_pct_mean":v["hp"]/v["fights"],"qi_final_mean":v["qi"]/v["fights"]
        } for k,v in d.items()}

    def finish(self):
        if not self.n:raise ValueError("no fights")
        n=self.n;s=self.sum
        dot=s["monster_dot_damage"];direct=s["monster_basic_damage"]+s["monster_skill_direct_damage"];total=dot+direct
        return {
            "fights":n,"win_rate":self.wins/n,"loss_rate":self.losses/n,"timeout_rate":self.timeouts/n,
            "rounds_mean":statistics.fmean(self.rounds),"rounds_p90":percentile(self.rounds,.90),
            "hp_final_pct_mean":statistics.fmean(self.hp),"hp_final_pct_p10":percentile(self.hp,.10),"hp_min_pct_mean":statistics.fmean(self.hpmin),
            "qi_final_mean":statistics.fmean(self.qi),"qi_spent_mean":s["player_qi_spent"]/n,"qi_drained_mean":s["player_qi_drained"]/n,
            "forced_basic_due_to_qi_mean":s["forced_basic_due_to_qi"]/n,
            "player_hit_rate":s["player_hits"]/s["player_attempts"] if s["player_attempts"] else 0.0,
            "monster_hit_rate":s["monster_hits"]/s["monster_attempts"] if s["monster_attempts"] else 0.0,
            "monster_evades_mean":s["monster_evades"]/n,
            "control_success_rate":s["control_successes"]/s["control_attempts"] if s["control_attempts"] else 0.0,
            "monster_skill_use_mean":s["monster_skill_uses"]/n,"monster_basic_use_mean":s["monster_basic_uses"]/n,
            "monster_damage_total_mean":total/n,"monster_damage_total_p90":percentile(self.damage,.90),
            "monster_dot_damage_mean":dot/n,"monster_direct_damage_mean":direct/n,
            "monster_dot_fraction":dot/total if total else 0.0,
            "root_breakdown":self._breakdown(self.root),"loadout_breakdown":self._breakdown(self.loadout),
        }
