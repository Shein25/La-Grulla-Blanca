# LII — Adaptive T1/T2 Bridge Contract Gate V01 — Review

Fecha: 2026-10-07.
Estado: **PASS_BRIDGE_ONLY**, NO LII BALANCE FREEZE.
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`.

## Evidencia

- Artefacto: `LII_T1_T2_ADAPTIVE_BRIDGE_CONTRACT_GATE_V01_REVIEW.zip`
- SHA-256: `c11647a1ef08099dd597fae693eede65059fb2166730cf38297bc073f537da66`
- Source HEAD: `667fe65871f7f2beef1dd525b6979a1e93a318af`
- Runner in ZIP SHA-256: `e530afaaff1e99639d62b0c51b309db4f3d6fd6ade4fcdeb15a9fa5aaa6b0dae`
- ZIP CRC: PASS.
- Manifiesto: 8/8 archivos con hash y tamaño coincidentes; 9 integrantes del ZIP, incluido PACKAGE_MANIFEST.
- SOURCE_LOCK: 8 blobs exactos, incluidos T0/T1/T2 LII frozen.
- Hotfix necesario confirmado: `params_status: READY` es metadato de `profile.technique`; parámetros de combate y stats T0 coincidieron sin excepciones.

## Gate

- 10/10 pruebas de eventos: PASS.
- 80 builds monorraíz, 4 perfiles de equipo, 2 especies LII, 2 políticas, 3 tiers.
- 3.840 contextos × R8 = 30.720 combates.
- 60 checkpoints.
- No AOE, no NaN/inf, sin resultados duplicados, sin timeouts.
- 0 supresiones de técnicas debidas por cadencia.
- T1 natural: 17.545 activaciones; T2 anticipación: 6.631.
- T0 sin activaciones adaptativas, T1 sin anticipaciones.

## Observaciones preliminares (NO valores meta)

Victorías agregadas sobre todas las configuraciones (ponderación uniforme de los contextos):
- T0: **89,209%**.
- T1: **77,266%**.
- T2: **74,316%**.

Win por especie/gear T2:
- Escarabajo T2 MANDATORY_ENTRY: **46,33%**; CARRY_OVER_LI_HIGH: **53,83%**; EXPECTED: **96,02%**; HIGH_ROLL: **91,25%**.
- Sapo T2 MANDATORY_ENTRY: **59,45%**; CARRY_OVER_LI_HIGH: **64,53%**; EXPECTED: **89,45%**; HIGH_ROLL: **93,67%**.

DEFENSE_OPEN vs UNITARGET_FIRST (mismos contextos, política distinta; NO experimento causal plenamente bloqueado en secuencia de acciones):
- Agregado T0/T1/T2: +2,858 pp win, +4,023 pp HP final, +3,177 Qi gasto, +1,296 rondas.
- T2 por raíz: Agua +3,12 pp; Fuego **−2,34 pp**; Metal +7,23 pp; Tierra +8,50 pp; Viento +0,88 pp.
- T2 T1 diferencias sobre el mismo contexto pueden llegar a 5 pp en algunos grupos, pero sólo R8.

Interpretación:
- T2 añade presión útil sin apagar cadencia.
- Las defensivas no son equivalentes en el uso de apertura; Fuego/Viento requieren controles de timing, no buff automático.
- EXPECTED y HIGH_ROLL muestran techo; los perfiles ENTRY/CARRY_OVER y pruebas de timing deben tener peso en la decisión.
- **No extrapolar balances finales desde R8**, ni comparar winrates de perfiles de gear como prueba de dominancia sin pares causalmente comparables.

## Límites de este gate

El adapter cumple la cobertura de eventos enumerada, no demuestra formalmente todas las trazas posibles. Las nuevas estrategias defensivas y Tramo I todavía no se han aislado con políticas comparadas y R adecuado. Builds multielementales quedan fuera de este subespacio monorraíz. No se introdujeron ajustes productivos.

## Decisión

**PASS_BRIDGE_ONLY.** Autoriza elaborar/ejecutar el microgate causal de defensivas LII T1/T2 sin tocar T0/T1/T2 ni equipo LI. Si aparecen discrepancias de paridad del puente, investigar antes de balancear. Posteriormente expansión legal multielemental y Concordancias LII.

Astra recibe resultados al cierre del laboratorio; no integración HTML, no `main`, no merge.
