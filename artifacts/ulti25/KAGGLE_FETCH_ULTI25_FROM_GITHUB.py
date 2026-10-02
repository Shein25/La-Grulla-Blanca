from pathlib import Path
import base64
import hashlib
import shutil
import urllib.request
import zipfile

# Paquete ULTI25 fijado a un commit inmutable de la rama experimental.
REPO = "Shein25/La-Grulla-Blanca"
COMMIT = "7b8cc5d1d028772e9b1dbe0a158c0e1cd9da2967"
DIR = "artifacts/ulti25"
NAME = "ULTI_25_MASS_KAGGLE_PACKAGE_2026-10-02.zip"
EXPECTED_SHA256 = "5e87a2534025a380d80e910836230bcf828214b0ee877cbef84f6d62773b02a6"

PARTS = [
    f"{NAME}.b64.part00",
    f"{NAME}.b64.part01",
    f"{NAME}.b64.part02",
    f"{NAME}.b64.part03",
    f"{NAME}.b64.tail00",
    f"{NAME}.b64.tail01",
    f"{NAME}.b64.tail02",
    f"{NAME}.b64.tail03",
    f"{NAME}.b64.tail04",
    f"{NAME}.b64.tail05",
    f"{NAME}.b64.tail06",
    f"{NAME}.b64.tail07",
]

BASE = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{DIR}"
WORK = Path("/kaggle/working")
ZIP = WORK / NAME
ROOT = WORK / "ulti25_mass_pkg"

chunks = []
for part in PARTS:
    url = f"{BASE}/{part}"
    print("Descargando:", part)
    with urllib.request.urlopen(url, timeout=60) as response:
        chunks.append(response.read().decode("ascii").strip())

payload = base64.b64decode("".join(chunks), validate=True)
actual_sha256 = hashlib.sha256(payload).hexdigest()

if actual_sha256 != EXPECTED_SHA256:
    raise RuntimeError(
        f"SHA-256 incorrecto: {actual_sha256} != {EXPECTED_SHA256}"
    )

ZIP.write_bytes(payload)

if ROOT.exists():
    shutil.rmtree(ROOT)
ROOT.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(ZIP, "r") as zf:
    zf.extractall(ROOT)

expected_files = {
    "run_ultimates_25_mass_kaggle.py",
    "base_3families_runner_v02.py",
    "combat_engine_new_stats_lab_v0_2.py",
    "metal_variants_v01.json",
    "optuna_adversarial_ultimates.py",
    "ULTIMATES_25_CATALOG_V0_3.json",
    "README_KAGGLE_ULTIS_25_MASS.md",
    "KAGGLE_RUN_ULTIS_25_MASS.ipynb",
    "HANDOFF_MOTOR_AUTORITATIVO_ULTIS_2026-10-02.md",
    "SMOKE_VALIDATION_2026-10-02.md",
    "PACKAGE_MANIFEST.json",
}

missing = sorted(name for name in expected_files if not (ROOT / name).exists())
if missing:
    raise RuntimeError(f"Paquete reconstruido pero faltan archivos: {missing}")

print()
print("ULTI25_GITHUB_FETCH: PASS")
print("ZIP:", ZIP)
print("SHA256:", actual_sha256)
print("ROOT:", ROOT)
print("ARCHIVOS:", len(expected_files))
