#!/usr/bin/env python3
"""Verify the downloaded V16 preclose archive without trusting summary figures.
Usage: python verify_v16_archive.py /path/to/GRULLA_LII_V16_PRECIERRE_ESTRUCTURAS_Y_PARIDAD_2026-10-09.zip
This checks integrity and experimental guards, NOT official runtime parity.
"""
from __future__ import annotations
import sys,io,csv,gzip,json,hashlib,zipfile
from collections import defaultdict,Counter

def main(filename):
    with zipfile.ZipFile(filename) as z:
        assert z.testzip() is None, "ZIP CRC failed"
        manifest=json.loads(z.read("MANIFEST_SHA256_V16.json"))
        for member,sha in manifest.items():
            assert hashlib.sha256(z.read(member)).hexdigest()==sha,member
        counts=Counter()
        contexts=defaultdict(dict)
        for cohort in ("GRULLA_LII_V16_DISCOVERY","GRULLA_LII_V16_HOLDOUT"):
            filename=cohort+"/RAW_V16_STRUCT.csv.gz"
            with z.open(filename) as handle:
                with gzip.GzipFile(fileobj=handle,mode="rb") as gz:
                    rows=csv.DictReader(io.TextIOWrapper(gz,encoding="utf-8"))
                    for row in rows:
                        assert row["timeout"]=="0" and row["due_missed"]=="0"
                        if row["arm"].endswith("_OFF"):
                            assert row["resolutions"]=="0"
                        if row["root"]=="agua":
                            assert row["selected"]=="0"
                        key=(cohort,)+tuple(row[k] for k in
                            ("root","foreign","monster","tier","gear","policy","build","rep"))
                        assert row["arm"] not in contexts[key]
                        contexts[key][row["arm"]]=row
                        counts[cohort]+=1
            assert counts[cohort]==36864,(cohort,counts[cohort])
        relevant=("win","rounds","hp_final_pct","qi_final","qi_spent",
                  "foreign_casts","def_casts","resolutions",
                  "fundational_first_preserves","fundational_reinforced_hits",
                  "embalse_stored","embalse_released","timeout","due_missed")
        unselected=0
        for key,arms in contexts.items():
            assert set(arms)=={"ORIGINAL_OFF","ORIGINAL_ON","V07_OFF","V07_ON"}
            assert len({arms[a]["seed"] for a in arms})==1,key
            if arms["V07_ON"]["selected"]=="0":
                unselected+=1
                for mode in ("OFF","ON"):
                    for metric in relevant:
                        assert (arms["ORIGINAL_"+mode][metric] ==
                                arms["V07_"+mode][metric]),(key,mode,metric)
        assert len(contexts)==18432
        assert unselected==16128
        return {"status":"PASS_LAB_ARCHIVE","fights":sum(counts.values()),
                "four_arm_contexts":len(contexts),
                "unselected_exact_contexts":unselected,
                "sha256_members_verified":len(manifest)}

if __name__=="__main__":
    assert len(sys.argv)==2,"Provide the V16 ZIP path"
    print(json.dumps(main(sys.argv[1]),ensure_ascii=False,indent=2))
