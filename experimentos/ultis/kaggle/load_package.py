#!/usr/bin/env python3
import base64, hashlib, json, pathlib, shutil, urllib.parse, urllib.request, zipfile

OWNER="Shein25"
REPO="La-Grulla-Blanca"
BRANCH="experiment/ultis-kaggle-3familias-v0.1"
ROOT_PATH="experimentos/ultis/kaggle/package_chunks_v3"
EXPECTED_SHA256="2fbaafd40367f1104b6bd5a479601b1b64f09e0849d04700735e4618fcd52775"
WORK=pathlib.Path("/kaggle/working")
WORK.mkdir(parents=True, exist_ok=True)

def github_text(path):
    ref=urllib.parse.quote(BRANCH, safe="")
    path_q="/".join(urllib.parse.quote(x, safe="") for x in path.split("/"))
    url=f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{path_q}?ref={ref}"
    req=urllib.request.Request(url, headers={"Accept":"application/vnd.github+json","User-Agent":"La-Grulla-Blanca-Kaggle-LAB/1.2"})
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
    raise RuntimeError(f"SHA-256 mismatch: {sha}; expected={EXPECTED_SHA256}; manifest={manifest['sha256']}")
zip_path=WORK/manifest["package"]
zip_path.write_bytes(data)
extract_dir=WORK/"ulti3f_pkg"
if extract_dir.exists(): shutil.rmtree(extract_dir)
extract_dir.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path) as z:
    bad=z.testzip()
    if bad: raise RuntimeError(f"ZIP corrupt member: {bad}")
    z.extractall(extract_dir)
print("GIT_PACKAGE_OK")
print("revision:", manifest.get("revision"))
print("branch:", BRANCH)
print("sha256:", sha)
print("extract_dir:", extract_dir)
