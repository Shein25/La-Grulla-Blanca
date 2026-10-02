#!/usr/bin/env python3
import base64, hashlib, json, pathlib, urllib.request, zipfile

OWNER="Shein25"
REPO="La-Grulla-Blanca"
BRANCH="experiment/ultis-kaggle-3familias-v0.1"
ROOT="experimentos/ultis/kaggle/package_chunks_v2"
RAW=f"https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{ROOT}"
WORK=pathlib.Path("/kaggle/working")
WORK.mkdir(parents=True, exist_ok=True)

def get_text(url):
    req=urllib.request.Request(url, headers={"User-Agent":"La-Grulla-Blanca-Kaggle-LAB/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")

manifest=json.loads(get_text(f"{RAW}/manifest.json"))
joined="".join(get_text(f"{RAW}/{name}").strip() for name in manifest["parts"])
if len(joined) != manifest["base64_length"]:
    raise RuntimeError(f"Base64 length mismatch: {len(joined)} != {manifest['base64_length']}")

data=base64.b64decode(joined, validate=True)
if len(data) != manifest["decoded_size_bytes"]:
    raise RuntimeError(f"ZIP size mismatch: {len(data)} != {manifest['decoded_size_bytes']}")

sha=hashlib.sha256(data).hexdigest()
if sha != manifest["sha256"]:
    raise RuntimeError(f"SHA-256 mismatch: {sha} != {manifest['sha256']}")

zip_path=WORK / manifest["package"]
zip_path.write_bytes(data)
extract_dir=WORK / "ULTI_3F_KAGGLE_PACKAGE_2026-10-02"
if extract_dir.exists():
    import shutil; shutil.rmtree(extract_dir)
with zipfile.ZipFile(zip_path) as z:
    bad=z.testzip()
    if bad:
        raise RuntimeError(f"ZIP corrupt member: {bad}")
    z.extractall(extract_dir)

print("GIT_PACKAGE_OK")
print("zip:", zip_path)
print("sha256:", sha)
print("extract_dir:", extract_dir)
