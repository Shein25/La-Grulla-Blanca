"""Streaming aggregation local to Rata T1 lab; never stores fight rows."""
from __future__ import annotations
from collections import Counter,defaultdict
import statistics

def percentile(values,q):
    xs=sorted(float(x) for x in values)
    if not xs:return 0.0
    pos=(len(xs)-1)*q;lo=int(pos);hi=min(lo+1,len(xs)-1);f=pos-lo
    return xs[lo]*(1-f)+xs[hi]*f

class StreamingFightAggregate:
    def __init__(self):
        self.n=0;self.wins=0;self.losses=0;self.timeouts=0
        self.rounds=[];self.hp=[];self.hpmin=[];self.qi=[];self.monster_damage=[]
        self.sum=Counter();self.death_causes=Counter()
        self.root=defaultdict(lambda:{"fights":0,"wins":0,"hp":0.0})
        self.loadout=defaultdict(lambda:{"fights":0,"wins":0,"hp":0.0})

    def add(self,r):
        self.n+=1;self.wins+=int(bool(r["win"]));self.losses+=int(bool(r["loss"]));self.timeouts+=int(bool(r["timeout"]))
        self.rounds.append(float(r["rounds"]));self.hp.append(float(r["player_hp_final_pct"]))
        self.hpmin.append(float(r["player_hp_min_pct"]));self.qi.append(float(r["player_qi_final"]))
        for k in ("player_qi_spent","player_qi_drained","defensive_activations","potion_uses","monster_skill_uses","monster_basic_uses","monster_skipped_actions","forced_basic_due_to_qi","monster_dot_damage","monster_basic_damage","monster_skill_direct_damage"):
            self.sum[k]+=float(r[k])
        m=r["metrics"]
        for k in ("player_attempts","player_hits","monster_attempts","monster_hits","monster_evades","control_attempts","control_successes"):
            self.sum[k]+=float(m.get(k,0))
        total=float(r["monster_dot_damage"])+float(r["monster_basic_damage"])+float(r["monster_skill_direct_damage"])
        self.monster_damage.append(total)
        self.death_causes[r.get("death_cause") or "NONE"]+=1
        rb=self.root[r["root"]];rb["fights"]+=1;rb["wins"]+=int(bool(r["win"]));rb["hp"]+=float(r["player_hp_final_pct"])
        lb=self.loadout[r["loadout_profile"]];lb["fights"]+=1;lb["wins"]+=int(bool(r["win"]));lb["hp"]+=float(r["player_hp_final_pct"])

    def _breakdown(self,d):
        return {k:{"fights":v["fights"],"wins":v["wins"],"win_rate":v["wins"]/v["fights"],"hp_final_pct_mean":v["hp"]/v["fights"]} for k,v in d.items()}

    def finish(self):
        if not self.n:raise ValueError("no fights")
        s=self.sum;n=self.n
        dot=s["monster_dot_damage"];direct=s["monster_basic_damage"]+s["monster_skill_direct_damage"];total=dot+direct
        return {
            "fights":n,"win_rate":self.wins/n,"loss_rate":self.losses/n,"timeout_rate":self.timeouts/n,
            "rounds_mean":statistics.fmean(self.rounds),"rounds_p10":percentile(self.rounds,.10),"rounds_p50":percentile(self.rounds,.50),"rounds_p90":percentile(self.rounds,.90),
            "hp_final_pct_mean":statistics.fmean(self.hp),"hp_final_pct_p10":percentile(self.hp,.10),"hp_final_pct_p50":percentile(self.hp,.50),"hp_final_pct_p90":percentile(self.hp,.90),
            "hp_min_pct_mean":statistics.fmean(self.hpmin),"qi_final_mean":statistics.fmean(self.qi),
            "qi_spent_mean":s["player_qi_spent"]/n,"qi_drained_mean":s["player_qi_drained"]/n,
            "player_hit_rate":s["player_hits"]/s["player_attempts"] if s["player_attempts"] else 0.0,
            "monster_hit_rate":s["monster_hits"]/s["monster_attempts"] if s["monster_attempts"] else 0.0,
            "monster_evades_per_fight":s["monster_evades"]/n,
            "control_success_rate":s["control_successes"]/s["control_attempts"] if s["control_attempts"] else 0.0,
            "defensive_activation_mean":s["defensive_activations"]/n,"potion_use_rate":s["potion_uses"]/n,
            "monster_skill_use_mean":s["monster_skill_uses"]/n,"monster_basic_use_mean":s["monster_basic_uses"]/n,
            "monster_skipped_action_mean":s["monster_skipped_actions"]/n,"forced_basic_due_to_qi_mean":s["forced_basic_due_to_qi"]/n,
            "monster_damage_total_mean":total/n,"monster_damage_total_p90":percentile(self.monster_damage,.90),
            "monster_dot_damage_mean":dot/n,"monster_direct_damage_mean":direct/n,
            "monster_dot_fraction":dot/total if total else 0.0,
            "death_causes":dict(self.death_causes),"root_breakdown":self._breakdown(self.root),"loadout_breakdown":self._breakdown(self.loadout),
        }
