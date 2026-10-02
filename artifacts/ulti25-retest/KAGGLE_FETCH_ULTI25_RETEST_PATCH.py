from pathlib import Path
import base64
import hashlib
import urllib.request
import zipfile

# ULTI25 focal retest patch. Fixed immutable commit containing all Base64 parts.
REPO = "Shein25/La-Grulla-Blanca"
PARTS_COMMIT = "b8724117930a99ddbc7546a9b3751360229291b2"
DIR = "artifacts/ulti25-retest"
NAME = "ULTI_25_RETEST_PATCH_V01.zip"
EXPECTED_SHA256 = "153d4d4d79ef17542e2d5df88c5b02de8b7283e7082d94dc541f5a7b8fc0e7e0"

PARTS = [
    f"{NAME}.b64.part00",
    f"{NAME}.b64.part01",
    f"{NAME}.b64.part02",
]

BASE = f"https://raw.githubusercontent.com/{REPO}/{PARTS_COMMIT}/{DIR}"
WORK = Path("/kaggle/working")
PATCH = WORK / NAME
ROOT = WORK / "ulti25_mass_pkg"

if not ROOT.exists():
    raise RuntimeError(
        "No existe /kaggle/working/ulti25_mass_pkg. "
        "Ejecuta primero KAGGLE_FETCH_ULTI25_FROM_GITHUB.py para reconstruir el paquete base."
    )

chunks = []
for part in PARTS:
    url = f"{BASE}/{part}"
    print("Descargando patch:", part)
    with urllib.request.urlopen(url, timeout=60) as response:
        chunks.append(response.read().decode("ascii").strip())

payload = base64.b64decode("".join(chunks), validate=True)
actual_sha256 = hashlib.sha256(payload).hexdigest()
if actual_sha256 != EXPECTED_SHA256:
    raise RuntimeError(
        f"SHA-256 incorrecto del patch: {actual_sha256} != {EXPECTED_SHA256}"
    )

PATCH.write_bytes(payload)
with zipfile.ZipFile(PATCH, "r") as zf:
    zf.extractall(ROOT)

required = {
    "run_ultimates_25_retest_kaggle.py",
    "optuna_adversarial_ultimates_retest.py",
    "AUDITORIA_ULTI25_FULL_RESULTS_2026-10-02.md",
    "RETEST_AUTHORITY_2026-10-02.md",
    "README_KAGGLE_ULTI25_RETEST.md",
    "RETEST_PACKAGE_MANIFEST.json",
}
missing = sorted(name for name in required if not (ROOT / name).exists())
if missing:
    raise RuntimeError(f"Patch extraído pero faltan archivos: {missing}")

print()
print("ULTI25_RETEST_PATCH_FETCH: PASS")
print("PATCH:", PATCH)
print("SHA256:", actual_sha256)
print("ROOT:", ROOT)
print("ARCHIVOS PATCH:", len(required))
