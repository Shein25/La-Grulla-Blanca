# Boss UI — backup experimental

Checkpoint guardado: **B14 · REGISTRO LIMPIO**
Fecha: **2026-09-27**
Rama: **implement/3c5-npc-ver74**
Estado: **experimento aislado, no integrado al juego**

## Archivo
`BOSS_UI_B14_REGISTRO_LIMPIO_2026-09-27.html.gz.b64`

El archivo contiene el HTML completo comprimido con gzip y codificado en Base64.

SHA-256 del HTML original:
`279cd260b662d2e68f48f3246d7a72e92738b463f693526f5ed98a92ec9c58da`

## Estado funcional del checkpoint
- room previa `nucleo_santuario_vinculo`;
- el combate se dispara con `atacar`, `atacar grulla` o `atacar la grulla`;
- Fase I: 150 HP;
- Fase II: 100 HP;
- Fase III: 50 HP;
- anillo exterior = vida de la fase;
- respiración del anillo por franjas de vida;
- PACTO central se fractura/progresa por fase;
- nombres de fase centrados y progresivos;
- nombre LA GRULLA con cambio cromático desde Fase II;
- descripciones narrativas permanecen hasta que aparece una intención;
- la intención reemplaza la caja y permanece hasta el cambio de fase;
- registro de combate sin banners artificiales de fase, combate o rondas;
- botón de laboratorio ATACAR hace 10 de daño;
- UI todavía experimental, sin motor real de La Grulla.

## Restauración
Linux/macOS:
```bash
base64 -d BOSS_UI_B14_REGISTRO_LIMPIO_2026-09-27.html.gz.b64 | gzip -d > BOSS_UI_B14_REGISTRO_LIMPIO.html
```

PowerShell:
```powershell
$raw = [Convert]::FromBase64String((Get-Content .\BOSS_UI_B14_REGISTRO_LIMPIO_2026-09-27.html.gz.b64 -Raw))
[IO.File]::WriteAllBytes(".\BOSS_UI_B14_REGISTRO_LIMPIO.html.gz", $raw)
```
Después descomprimir el `.gz`.

No usar este checkpoint como canon de producción: es una copia de seguridad del laboratorio visual.
