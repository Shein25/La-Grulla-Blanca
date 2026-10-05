#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, hashlib, json, re
from pathlib import Path

EXPECTED_SOURCE_PAYLOAD_SHA256 = "f1cb59aae1d69f39f2024a7ad3c8d8c50566081fd3dd4963c7e1ef8209d55038"
EXPECTED_STANDARD_CASES = 133856
EXPECTED_OUTPUT_NOTEBOOK_SHA256 = "531003aa6701151528716e88e0f7550bb49ccb3b26b2ffd28a933ef3abe0470d"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_notebook")
    ap.add_argument("output_notebook")
    a = ap.parse_args()
    src = Path(a.source_notebook)
    dst = Path(a.output_notebook)
    nb = json.loads(src.read_text(encoding="utf-8"))

    payload_src = "".join(nb["cells"][2]["source"])
    declared = re.search(r"PAYLOAD_SHA256='([0-9a-f]{64})'", payload_src)
    embedded = re.search("PAYLOAD_B64='''(.*?)'''", payload_src, re.S)
    if not declared or not embedded:
        raise SystemExit("PAYLOAD_MARKERS_NOT_FOUND")
    payload_sha = hashlib.sha256(base64.b64decode(embedded.group(1))).hexdigest()
    if declared.group(1) != EXPECTED_SOURCE_PAYLOAD_SHA256 or payload_sha != EXPECTED_SOURCE_PAYLOAD_SHA256:
        raise SystemExit(f"PAYLOAD_SHA_MISMATCH:{declared.group(1)}:{payload_sha}")

    nb["cells"][0]["source"] = [
        "# La Grulla Blanca — 25 Ultis · Continuous Full Spectrum V03.1 — STANDARD\n", "\n",
        "**STANDARD V03.1 autorizado** después de QUICK V03.1 limpio: 28.464/28.464, 0 hard issues.\n",
        "El payload, runner, V05, catálogo de Ultis, oráculos y autoridad numérica permanecen idénticos al QUICK aprobado.\n",
        "Stress fixtures no son autoridad de balance; `Sentencia` sigue siendo sólo `BALANCE_PRIORITY`.\n",
    ]
    nb["cells"][1]["source"] = [
        "PRESET='standard'  # autorizado tras QUICK V03.1 PASS / 0 hard issues\n",
        "MAX_CASES=0\n", "EXPECTED_CASES=133856\n",
        "assert PRESET=='standard', 'STANDARD_V031_PRESET_GUARD'\n",
        "print('Preset autorizado:',PRESET,'Casos esperados:',EXPECTED_CASES,'Max cases:',MAX_CASES)\n",
    ]
    nb["cells"][4]["source"] = [
        "cases=work/'FULL_SPECTRUM_CASES_V031_STANDARD.jsonl'\n",
        "subprocess.run([sys.executable,str(work/'generate_full_spectrum_cases_v031.py'),'--preset',PRESET,'--out',str(cases)],check=True)\n",
        "generated_cases=sum(1 for line in cases.open(encoding='utf-8') if line.strip())\n",
        "print('Casos STANDARD generados:',generated_cases)\n",
        "assert generated_cases==EXPECTED_CASES,('STANDARD_CASE_COUNT_MISMATCH',generated_cases,EXPECTED_CASES)\n",
        "out=work/'CONTINUOUS_FULL_SPECTRUM_V031_STANDARD'\n",
        "cmd=[sys.executable,str(work/'run_full_spectrum_v031.py'),'--cases',str(cases),'--runner',str(work/'grulla_continuous_ulti_runner_v031.py'),'--out',str(out)]\n",
        "if MAX_CASES: cmd += ['--max-cases',str(MAX_CASES)]\n",
        "cp=subprocess.run(cmd,text=True,capture_output=True)\n",
        "print(cp.stdout); print(cp.stderr)\n",
        "summary=json.loads((out/'summary.json').read_text()) if (out/'summary.json').exists() else {}\n",
        "print(json.dumps(summary,indent=2,ensure_ascii=False))\n",
        "assert summary.get('cases_executed')==EXPECTED_CASES,('STANDARD_INCOMPLETE',summary)\n",
        "assert summary.get('hard_issue_count')==0,('STANDARD_HARD_ISSUES',summary)\n",
        "assert summary.get('pass'),('STANDARD_V031_NOT_CLEAN',summary)\n",
    ]
    nb["cells"][5]["source"] = [
        "import shutil\n",
        "result_zip=pathlib.Path('/kaggle/working/CONTINUOUS_FULL_SPECTRUM_V031_STANDARD.zip')\n",
        "if result_zip.exists(): result_zip.unlink()\n",
        "shutil.make_archive(str(result_zip.with_suffix('')),'zip',root_dir=out)\n",
        "print('RESULT ZIP:',result_zip,'SHA256:',hashlib.sha256(result_zip.read_bytes()).hexdigest())\n",
    ]
    for c in nb["cells"]:
        if c.get("cell_type") == "code":
            c["execution_count"] = None
            c["outputs"] = []

    dst.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    got = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(json.dumps({"output": str(dst), "sha256": got, "expected": EXPECTED_OUTPUT_NOTEBOOK_SHA256, "payload_sha256": payload_sha}, indent=2))
    if got != EXPECTED_OUTPUT_NOTEBOOK_SHA256:
        raise SystemExit("STANDARD_NOTEBOOK_SHA_MISMATCH")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
