"""ETAPA 19C — LianQi I exhaustivo lógico + screen masivo.

No toca runtime/HTML. Consume ETAPA19B como autoridad del laboratorio 1v1.

Pipeline LI:
A) enumera las 6.144 combinaciones estructurales de equipo;
B) colapsa firmas mecánicas equivalentes conservando multiplicidad/loadouts;
C) cruza 5 raíces × 5 monstruos LI × T0/T1 × políticas;
D) permite screen Monte Carlo low-N por lotes/checkpoints;
E) selecciona frontera/anomalías/cobertura para refinamiento high-N.

La factibilidad económica sigue fuera: UNCONSTRAINED_STAGE_AVAILABLE_GEAR.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable, Sequence
import argparse
import hashlib
import json
import math

import pandas as pd

from etapa19b_combat_engine import (
    ROOT_TECHNIQUES,
    LabSignalBridge,
    load_json,
    monte_carlo,
    TECHNIQUE_CATALOG_PATH,
    MONSTER_CATALOG_PATH,
    EQUIPMENT_CATALOG_PATH,
)
from etapa19_skill_buildspace import enumerate_skill_builds

HERE = Path(__file__).resolve().parent
STAGE = "LianQi_I"
TIERS = ("T0", "T1")
DEFAULT_POLICIES = ("UNITARGET_FIRST", "DEFENSE_OPEN", "AOE_FIRST")
STAGE_ORDER = {"LianQi_I":1, "LianQi_II":2, "LianQi_III":3, "LianQi_IV":4}

# Sólo estos campos cambian el combate 1v1 de ETAPA19B.
COMBAT_STAT_KEYS = (
    "hp_max","qi_max","precision","evasion","defense","control","tenacity",
    "crit_chance_pp","crit_damage_pp","percent_penetration_pp",
    "basic_attack_flat","technique_direct_damage_percent",
)

OUT_OF_COMBAT_SCOPES = {"OUT_OF_COMBAT_PENDING"}


@dataclass(frozen=True)
class GearSignature:
    signature_id: str
    stats: tuple[tuple[str,float], ...]
    combat_effects: tuple[str, ...]


def _canonical_effect(effect: dict | None) -> str | None:
    if not effect:
        return None
    if effect.get("simulation_scope") in OUT_OF_COMBAT_SCOPES:
        return None
    return json.dumps(effect, sort_keys=True, ensure_ascii=False, separators=(",",":"))


def _signature(stats: dict, effects: Iterable[dict]) -> GearSignature:
    stat_tuple = tuple(
        (k, float(stats.get(k, 0)))
        for k in COMBAT_STAT_KEYS
        if float(stats.get(k, 0)) != 0
    )
    effect_tuple = tuple(sorted(
        x for x in (_canonical_effect(e) for e in effects) if x is not None
    ))
    raw = json.dumps(
        {"stats":stat_tuple,"effects":effect_tuple},
        ensure_ascii=False, sort_keys=True, separators=(",",":")
    )
    sid = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]
    return GearSignature(sid, stat_tuple, effect_tuple)


def _available_items(equipment: dict, stage: str=STAGE) -> list[dict]:
    rank = STAGE_ORDER[stage]
    return [x for x in equipment["items"] if STAGE_ORDER[x["min_stage"]] <= rank]


def enumerate_loadouts(equipment: dict, stage: str=STAGE):
    """Enumera cada loadout estructural legal sin reemplazo y permitiendo vacío."""
    items = _available_items(equipment, stage)
    by_slot = defaultdict(list)
    for item in items:
        by_slot[item["slot"]].append(item)

    slot_options = []
    for slot, capacity in equipment["slots"].items():
        pool = by_slot.get(slot, [])
        opts = []
        for k in range(0, min(capacity, len(pool)) + 1):
            opts.extend(combinations(pool, k))
        slot_options.append((slot, opts))

    for combo in product(*(opts for _, opts in slot_options)):
        flat = tuple(item for group in combo for item in group)
        yield flat


def aggregate_loadout(loadout: Sequence[dict]) -> tuple[dict,list[dict]]:
    stats = Counter()
    effects = []
    for item in loadout:
        for k,v in item.get("stats",{}).items():
            stats[k] += float(v)
        if item.get("effect"):
            effects.append(dict(item["effect"]))
    return dict(stats), effects


def build_li_signature_catalog(equipment: dict) -> tuple[pd.DataFrame,pd.DataFrame]:
    """Devuelve firmas únicas y mapping loadout→firma con trazabilidad completa."""
    grouped = {}
    map_rows = []

    for idx, loadout in enumerate(enumerate_loadouts(equipment, STAGE)):
        stats,effects = aggregate_loadout(loadout)
        sig = _signature(stats,effects)
        item_ids = tuple(x["item_id"] for x in loadout)

        row = grouped.setdefault(sig.signature_id,{
            "signature_id":sig.signature_id,
            "stats_json":json.dumps(dict(sig.stats),sort_keys=True),
            "combat_effects_json":json.dumps(list(sig.combat_effects),sort_keys=True),
            "multiplicity":0,
            "representative_items_json":json.dumps(item_ids),
            "all_loadouts":[],
        })
        row["multiplicity"] += 1
        row["all_loadouts"].append(item_ids)

        map_rows.append({
            "loadout_id":f"LI_{idx:04d}",
            "signature_id":sig.signature_id,
            "item_ids_json":json.dumps(item_ids),
        })

    sig_rows = []
    for row in grouped.values():
        out = dict(row)
        out["all_loadouts_json"] = json.dumps(out.pop("all_loadouts"))
        sig_rows.append(out)

    signatures = pd.DataFrame(sig_rows).sort_values("signature_id").reset_index(drop=True)
    mapping = pd.DataFrame(map_rows)
    return signatures,mapping


def _paths_li(root: str) -> dict[str,tuple]:
    b = next(enumerate_skill_builds(root,STAGE))
    return {p.technique_id:p.choices for p in b.paths}


def native_li_monsters(monsters: dict) -> list[dict]:
    return [
        p for p in monsters["profiles"].values()
        if p["native_stage"] == STAGE
    ]


def expected_counts(equipment: dict) -> dict:
    signatures,mapping = build_li_signature_catalog(equipment)
    return {
        "raw_loadouts":len(mapping),
        "unique_gear_signatures":len(signatures),
        "gear_reduction_pct":1-len(signatures)/len(mapping),
        "roots":len(ROOT_TECHNIQUES),
        "unique_player_builds":len(signatures)*len(ROOT_TECHNIQUES),
        "raw_player_builds":len(mapping)*len(ROOT_TECHNIQUES),
    }


def coverage_signature_ids(
    signatures: pd.DataFrame,
    mapping: pd.DataFrame,
    equipment: dict,
) -> set[str]:
    """Garantiza al menos una firma por item + loadouts de referencia + extremos."""
    chosen = set()

    # Cada objeto LI debe aparecer en al menos una firma.
    item_to_sig = {}
    for row in mapping.itertuples(index=False):
        ids = json.loads(row.item_ids_json)
        for iid in ids:
            item_to_sig.setdefault(iid,row.signature_id)
    for item in _available_items(equipment,STAGE):
        if item["item_id"] in item_to_sig:
            chosen.add(item_to_sig[item["item_id"]])

    # MANDATORY / EXPECTED / HIGH_ROLL.
    for profile in ("MANDATORY_ENTRY","EXPECTED_STAGE","HIGH_ROLL_STRESS"):
        ids = tuple(equipment["simulation_loadouts"][profile][STAGE])
        target = json.dumps(ids)
        hit = mapping.loc[mapping["item_ids_json"]==target,"signature_id"]
        if not hit.empty:
            chosen.add(hit.iloc[0])

    # Extremos por cada stat presente.
    expanded = signatures.copy()
    parsed = expanded["stats_json"].map(json.loads)
    for key in COMBAT_STAT_KEYS:
        vals = parsed.map(lambda d:float(d.get(key,0)))
        if len(vals):
            chosen.add(expanded.loc[vals.idxmin(),"signature_id"])
            chosen.add(expanded.loc[vals.idxmax(),"signature_id"])

    return chosen


def _screen_cell(
    *,
    signature_row,
    root:str,
    monster:dict,
    tier:str,
    policy:str,
    iterations:int,
    seed:int,
    techniques:dict,
    equipment:dict,
    signal_bridge:LabSignalBridge,
) -> dict:
    item_ids = json.loads(signature_row.representative_items_json)
    result = monte_carlo(
        iterations=iterations,
        seed=seed,
        stage=STAGE,
        root=root,
        item_ids=item_ids,
        paths=_paths_li(root),
        monster_profile=monster,
        tier=tier,
        policy=policy,
        signal_bridge=signal_bridge,
        technique_catalog=techniques,
        equipment_catalog=equipment,
    )
    return {
        "signature_id":signature_row.signature_id,
        "multiplicity":int(signature_row.multiplicity),
        "representative_items_json":signature_row.representative_items_json,
        **result,
    }


def run_signature_screen(
    signatures: pd.DataFrame,
    *,
    iterations:int,
    seed:int=20260930,
    policies:Sequence[str]=DEFAULT_POLICIES,
    only_signature_ids:set[str]|None=None,
    checkpoint_dir:str|Path|None=None,
    chunk_size:int=128,
) -> pd.DataFrame:
    techniques = load_json(TECHNIQUE_CATALOG_PATH)
    monsters = load_json(MONSTER_CATALOG_PATH)
    equipment = load_json(EQUIPMENT_CATALOG_PATH)
    native = native_li_monsters(monsters)
    bridge = LabSignalBridge()

    use = signatures
    if only_signature_ids is not None:
        use = signatures[signatures["signature_id"].isin(only_signature_ids)]

    checkpoint = Path(checkpoint_dir) if checkpoint_dir else None
    if checkpoint:
        checkpoint.mkdir(parents=True,exist_ok=True)

    rows=[]
    buffered=[]
    cell_no=0
    for sig in use.itertuples(index=False):
        for root in ROOT_TECHNIQUES:
            for monster in native:
                for tier in TIERS:
                    for policy in policies:
                        # Seed estable por celda, independiente del orden/chunking.
                        token=f"{sig.signature_id}|{root}|{monster['monster_id']}|{tier}|{policy}|{seed}"
                        cell_seed=seed+int(hashlib.sha1(token.encode()).hexdigest()[:8],16)
                        row=_screen_cell(
                            signature_row=sig,root=root,monster=monster,tier=tier,
                            policy=policy,iterations=iterations,seed=cell_seed,
                            techniques=techniques,equipment=equipment,signal_bridge=bridge,
                        )
                        rows.append(row);buffered.append(row);cell_no+=1
                        if checkpoint and len(buffered)>=chunk_size:
                            pd.DataFrame(buffered).to_parquet(
                                checkpoint/f"li_screen_{cell_no-len(buffered)+1:07d}_{cell_no:07d}.parquet",
                                index=False
                            )
                            buffered=[]

    if checkpoint and buffered:
        pd.DataFrame(buffered).to_parquet(
            checkpoint/f"li_screen_{cell_no-len(buffered)+1:07d}_{cell_no:07d}.parquet",
            index=False
        )
    return pd.DataFrame(rows)


def select_refinement_cells(
    screen:pd.DataFrame,
    mapping:pd.DataFrame,
    equipment:dict,
    *,
    frontier_low:float=0.30,
    frontier_high:float=0.70,
    per_matchup_extremes:int=3,
) -> pd.DataFrame:
    """Selecciona frontera, extremos y sensibilidad T0→T1 sin elegir builds a ojo."""
    selected=set()

    # Frontera.
    frontier=screen[(screen.win_rate>=frontier_low)&(screen.win_rate<=frontier_high)]
    selected.update(frontier.index.tolist())

    # Extremos por root/monster/tier/policy.
    groups=["root","monster_id","tier","policy"]
    for _,g in screen.groupby(groups,sort=False):
        selected.update(g.nlargest(per_matchup_extremes,"win_rate").index.tolist())
        selected.update(g.nsmallest(per_matchup_extremes,"win_rate").index.tolist())

    # Sensibilidad T0→T1.
    pivot=screen.pivot_table(
        index=["signature_id","root","monster_id","policy"],
        columns="tier",values="win_rate",aggfunc="first"
    ).dropna()
    if {"T0","T1"}.issubset(pivot.columns):
        pivot["delta_abs"]=(pivot["T1"]-pivot["T0"]).abs()
        sensitive=pivot.nlargest(min(500,len(pivot)),"delta_abs").reset_index()
        keys=set(tuple(x) for x in sensitive[["signature_id","root","monster_id","policy"]].itertuples(index=False,name=None))
        mask=screen.apply(
            lambda r:(r.signature_id,r.root,r.monster_id,r.policy) in keys,
            axis=1
        )
        selected.update(screen[mask].index.tolist())

    # Cobertura de items/perfiles.
    sigs=screen[["signature_id"]].drop_duplicates().merge(
        screen[["signature_id","representative_items_json"]].drop_duplicates(),
        on="signature_id",how="left"
    )
    coverage=coverage_signature_ids(
        pd.DataFrame({
            "signature_id":sigs.signature_id,
            "stats_json":"{}",
            "representative_items_json":sigs.representative_items_json,
        }),
        mapping,equipment
    )
    selected.update(screen[screen.signature_id.isin(coverage)].index.tolist())

    return screen.loc[sorted(selected)].copy()


def write_catalog_outputs(outdir:str|Path) -> dict:
    out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
    equipment=load_json(EQUIPMENT_CATALOG_PATH)
    signatures,mapping=build_li_signature_catalog(equipment)
    signatures.to_parquet(out/"li_gear_signatures.parquet",index=False)
    mapping.to_parquet(out/"li_loadout_to_signature.parquet",index=False)
    counts=expected_counts(equipment)
    (out/"li_counts.json").write_text(
        json.dumps(counts,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    return counts


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--outdir",default="etapa19c_li_output")
    ap.add_argument("--plan-only",action="store_true")
    ap.add_argument("--coverage-only",action="store_true")
    ap.add_argument("--iterations",type=int,default=5)
    ap.add_argument("--seed",type=int,default=20260930)
    ap.add_argument("--chunk-size",type=int,default=128)
    args=ap.parse_args()

    out=Path(args.outdir);out.mkdir(parents=True,exist_ok=True)
    equipment=load_json(EQUIPMENT_CATALOG_PATH)
    signatures,mapping=build_li_signature_catalog(equipment)
    counts=expected_counts(equipment)

    print(json.dumps(counts,indent=2))
    if counts["raw_loadouts"]!=6144:
        raise SystemExit(f"RAW_LOADOUT_COUNT:{counts['raw_loadouts']}!=6144")
    if counts["unique_gear_signatures"]!=4864:
        raise SystemExit(f"SIGNATURE_COUNT:{counts['unique_gear_signatures']}!=4864")

    signatures.to_parquet(out/"li_gear_signatures.parquet",index=False)
    mapping.to_parquet(out/"li_loadout_to_signature.parquet",index=False)
    if args.plan_only:
        return

    only=None
    if args.coverage_only:
        only=coverage_signature_ids(signatures,mapping,equipment)
        print(f"coverage signatures: {len(only)}")

    screen=run_signature_screen(
        signatures,iterations=args.iterations,seed=args.seed,
        only_signature_ids=only,checkpoint_dir=out/"checkpoints",
        chunk_size=args.chunk_size,
    )
    screen.to_parquet(out/"li_screen.parquet",index=False)

    refinement=select_refinement_cells(screen,mapping,equipment)
    refinement.to_parquet(out/"li_refinement_cells.parquet",index=False)

    summary={
        **counts,
        "screen_signatures":screen.signature_id.nunique(),
        "screen_cells":len(screen),
        "iterations_per_cell":args.iterations,
        "refinement_cells":len(refinement),
        "policies":list(DEFAULT_POLICIES),
        "tiers":list(TIERS),
        "seed":args.seed,
        "gear_mode":"UNCONSTRAINED_STAGE_AVAILABLE_GEAR",
        "status":"LAB_SCREEN_NOT_BALANCE_DECISION",
    }
    (out/"li_screen_summary.json").write_text(
        json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"
    )
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
