#!/usr/bin/env python3
import base64, hashlib, json, pathlib, shutil, urllib.parse, urllib.request, zipfile

OWNER="Shein25"
REPO="La-Grulla-Blanca"
BRANCH="experiment/ultis-kaggle-3familias-v0.1"
ROOT_PATH="experimentos/ultis/kaggle/package_chunks_v2"
EXPECTED_SHA256="18314ab1614d930b7fce22919a3fc5c63c846980c9fc0fe5222eaefb2aa29744"
WORK=pathlib.Path("/kaggle/working")
WORK.mkdir(parents=True, exist_ok=True)

def github_text(path):
    ref=urllib.parse.quote(BRANCH, safe="")
    path_q="/".join(urllib.parse.quote(x, safe="") for x in path.split("/"))
    url=f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path_q}?ref={ref}"
    req=urllib.request.Request(url, headers={
        "Accept":"application/vnd.github+json",
        "User-Agent":"La-Grulla-Blanca-Kaggle-LAB/1.0",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        obj=json.loads(r.read().decode("utf-8"))
    if obj.get("encoding")!="base64":
        raise RuntimeError(f"Unexpected GitHub encoding for {path}: {obj.get('encoding')}")
    return base64.b64decode(obj["content"]).decode("utf-8")

manifest=json.loads(github_text(f"{ROOT_PATH}/manifest.json"))
joined="".join(github_text(f"{ROOT_PATH}/{name}").strip() for name in manifest["parts"])
if len(joined)!=manifest["base64_length"]:
    raise RuntimeError(f"Base64 length mismatch: {len(joined)} != {manifest['base64_length']}")

data=base64.b64decode(joined, validate=True)
if len(data)!=manifest["decoded_size_bytes"]:
    raise RuntimeError(f"ZIP size mismatch: {len(data)} != {manifest['decoded_size_bytes']}")

sha=hashlib.sha256(data).hexdigest()
if sha!=EXPECTED_SHA256 or sha!=manifest["sha256"]:
    raise RuntimeError(f"SHA-256 mismatch: {sha}")

zip_path=WORK/manifest["package"]
zip_path.write_bytes(data)
extract_dir=WORK/"ULTI_3F_KAGGLE_PACKAGE_2026-10-02"
if extract_dir.exists():
    shutil.rmtree(extract_dir)
with zipfile.ZipFile(zip_path) as z:
    bad=z.testzip()
    if bad:
        raise RuntimeError(f"ZIP corrupt member: {bad}")
    z.extractall(extract_dir)

print("GIT_PACKAGE_OK")
print("branch:", BRANCH)
print("zip:", zip_path)
print("sha256:", sha)
print("extract_dir:", extract_dir)
