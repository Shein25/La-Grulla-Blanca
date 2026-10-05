# Backup V03 para handoff V03.1

Este directorio conserva un backup compacto del estado V03 auditado antes de construir V03.1.

Archivo reconstruido:

`GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.zip`

SHA-256 esperado:

`24bd80b3a6bdf636ed747f1ef8e953e3d3f4d30857b0a37d6c210366bc219c5b`

Tamaño esperado: 46,244 bytes.

El ZIP fue codificado en Base64 y dividido en 5 partes de texto para conservarlo en Git sin tocar `main`.

Partes, en orden:
1. `GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part01.b64`
2. `GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part02.b64`
3. `GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part03.b64`
4. `GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part04.b64`
5. `GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part05.b64`

SHA-256 de cada parte:
- part01: `876402ee6e13624a57b463838ddf6716238709fa285199cb362b115f578e1ff0`
- part02: `c3683954127aa9b1db75d3ce8d201f13ff539254670a2da6e6bd68af6436bd02`
- part03: `0b77ead919220071e51d914b830b4ee54dd4807241c4ce4b648957c3b717ddc4`
- part04: `d6e98cd29560a28862d8843e189b8018da613bea91fa44c78513bd052128a52e`
- part05: `4101e328fe416cdc7e9691c9112082d04cc04b44c7f50ed0d529c0dc2af5864c`

En Linux/macOS:

```bash
cat GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part*.b64 | base64 -d > GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.zip
sha256sum GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.zip
```

En Python:

```python
from pathlib import Path
import base64, hashlib

parts = sorted(Path(".").glob("GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.part*.b64"))
raw = base64.b64decode("".join(p.read_text() for p in parts))
Path("GRULLA_ULTI25_V03_HANDOFF_BACKUP_2026-10-04.zip").write_bytes(raw)
print(hashlib.sha256(raw).hexdigest())
```

Contenido del ZIP: handoff, snapshot de auditoría, prompt para el siguiente chat, resumen/issues del QUICK y las fuentes/configuración V03 necesarias para continuar la corrección.

Este backup es histórico. No convertirlo en V03.1 editándolo in-place: extraer/copiar y producir archivos V03.1 nuevos.
