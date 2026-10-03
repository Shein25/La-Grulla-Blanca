#!/usr/bin/env python3
from pathlib import Path
import zipfile, hashlib, json, re, sys

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def compact(src: Path, dst: Path):
    with zipfile.ZipFile(src, "r") as zin:
        state = json.loads(zin.read("state.json"))
        phases = state.get("phases", {})
        completed = {
            key.split(":", 1)[1]
            for key, val in phases.items()
            if key.startswith("TECHNIQUE:") and isinstance(val, dict) and val.get("status") == "COMPLETE"
        }
        removed = []
        kept = []
        for info in zin.infolist():
            name = info.filename
            if name == "MANIFEST_SHA256.txt":
                continue
            parts = name.split("/")
            prune = (
                len(parts) >= 7
                and parts[0] == "roots"
                and parts[2] in completed
                and parts[3] == "finalists"
                and re.fullmatch(r"R\d+", parts[5] or "") is not None
            )
            if prune:
                removed.append((name, info.compress_size, info.file_size))
            else:
                kept.append((name, zin.read(name)))

    report = {
        "status": "SAFE_COMPLETED_TECHNIQUE_RAW_COMPACTION",
        "source_checkpoint": src.name,
        "source_sha256": sha256(src.read_bytes()),
        "completed_techniques_detected": sorted(completed),
        "removed_files": len(removed),
        "removed_uncompressed_bytes": sum(x[2] for x in removed),
        "removed_original_zip_compressed_bytes": sum(x[1] for x in removed),
        "policy": "Only raw finalist R<replicates>/ batches of TECHNIQUE:<id>=COMPLETE are removed. Summary JSON, human shortlist, studies, baselines, authority and state are retained.",
        "resume_semantics": "Campaign.technique() skips COMPLETE techniques; aggregate() consumes human_shortlist.json, not raw finalist batches."
    }
    kept.append(("COMPACTION_REPORT.json", json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()))

    manifest = [f"{sha256(data)}  {name}" for name, data in sorted(kept)]
    tmp = dst.with_suffix(dst.suffix + ".pending")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=3) as zout:
        for name, data in sorted(kept):
            zout.writestr(name, data)
        zout.writestr("MANIFEST_SHA256.txt", "\n".join(manifest) + "\n")
    tmp.replace(dst)

    with zipfile.ZipFile(dst) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) and z.testzip() is None
        listed = {}
        for line in z.read("MANIFEST_SHA256.txt").decode().splitlines():
            h, name = line.split("  ", 1)
            assert name not in listed and name in names and sha256(z.read(name)) == h
            listed[name] = h
        assert set(listed) == set(names) - {"MANIFEST_SHA256.txt"}

    return {
        "source_bytes": src.stat().st_size,
        "compact_bytes": dst.stat().st_size,
        "saved_bytes": src.stat().st_size - dst.stat().st_size,
        "sha256": sha256(dst.read_bytes()),
        **report,
    }

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: compact_techniques_checkpoint.py CHECKPOINT.zip [OUTPUT.zip]")
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) == 3 else src.with_name(src.stem + "_COMPACT.zip")
    result = compact(src, dst)
    print(json.dumps(result, indent=2, ensure_ascii=False))
