# V12 — Batería GENERAL de Concordancias defensivas · LianQi II
Fecha: 2026-10-08. **PASS PARCIAL DE LABORATORIO / NO CANON / NO RUNTIME / NO FREEZE**.

## Autoridad y alcance
Progresión aprobada: LI=0 Tramos y sin defensivas; LII=Tramo I con 2 PT, técnicas unitarget BASE y defensivas; no AOE. Elementos neutrales ×1,00. Se preservan monstruos, equipo, LI, HTML y main. Élite, T3/T4 y AOE fuera.
Sistemas de referencia: LI V04B *candidato experimental de Concordancias por relación*; LII V07/V10/V11 laboratorios. La compatibilidad real del HTML actualizado, aprendizaje ajeno y prioridad de hooks condicionales siguen pendientes.

## A: sensibilidad escalar sobre la defensa BASE
**516.096 combates** = 129.024 contextos × 4 brazos (OFF, y 25%, 50%, 100% de cada escala LI-V04B); **8 semillas**, 5 raíces, 16 builds legales por raíz, seis especies normales, T0/T1/T2, dos equipos (POST_M03/EXPECTED_STAGE), dos políticas (EARLY/DELAYED_TRIGGER).

Cobertura global de 20 relaciones dirigidas: **13 escalares** de prueba; **1 BASE NONE**; **4 con hook pero sin magnitud numérica** (METAL_TO_FUEGO, AGUA_TO_METAL, AGUA_TO_VIENTO, TIERRA_TO_VIENTO), bloqueadas; **2 estructurales** ensayadas aparte. La matriz A incluye 14 relaciones (13 escalares + NONE).

QA: **0 timeouts**, **0 omisiones de técnica programada**, **9.216 contextos negativos idénticos entre OFF/25/50/100**, **104.160 resoluciones ON por cada brazo de intensidad** y ninguna OFF. Semillas y contextos idénticos entre brazos.

Delta medio de victoria del jugador vs OFF (promedio EARLY+DELAYED, relaciones numéricas incluidas; unidades: puntos porcentuales):
| Equipo | Tier | 25 % | 50 % | 100 % |
|---|---|---:|---:|---:|
| POST_M03 | T0 | +1,68 | +2,53 | +3,31 |
| POST_M03 | T1 | +2,09 | +3,22 | +4,22 |
| POST_M03 | T2 | +2,26 | +3,46 | +4,63 |
| EXPECTED_STAGE | T0 | +0,13 | +0,23 | +0,27 |
| EXPECTED_STAGE | T1 | +0,25 | +0,37 | +0,51 |
| EXPECTED_STAGE | T2 | +0,29 | +0,43 | +0,63 |

T2 POST_M03, por raíz (25/50/100 %, ambas políticas): Fuego ≈0/0/0; Agua ≈0,1/0,1/0,1; Tierra +2,6/+3,7/+4,6; Metal +4,6/+6,8/+7,6; Viento +5,9/+9,9/+15,5 pp. **No comparar raíces como ranking definitivo**: la cobertura numérica es desigual (Fuego 3, Tierra 4, Agua 3, Metal 2, Viento 2 relaciones). Grandes sensibilidades T2 EARLY en 100 % prestado: Agua→Tierra +17,32; Fuego→Viento +16,93; Fuego→Metal +13,02 pp. Ninguna cifra autoriza escalas de LII.

## B: Placa Fundacional y Embalse FÍSICOS en el puente experimental
**36.864 combates**, 18.432 pares ON/OFF; Tierra→Metal y Tierra→Agua, 16 builds/receptor × seis especies × T0/T1/T2 × 2 equipos × 2 políticas × 8 semillas. Se usa el parche estructural LI-V04B físicamente, **no el HTML de producción**.
- Placa: 8.290 primeros impactos preservaron placa y 8.145 impactos reforzados; frente a T2 POST_M03: EARLY +8,85 pp y DELAYED +9,24 pp. Requiere recalibrar magnitud; no aprobar 1,25 prestado.
- Embalse: almacenó 2.207,27 unidades de absorción y liberó 1.849,52; cumplió los invariantes de almacenamiento/liberación. T2 POST_M03 no modificó WR en este protocolo, aunque el efecto físico sí se activó.
- 15.921 resoluciones estructurales ON; 0 OFF; 0 timeouts; 0 técnicas programadas omitidas. El ensayo NO demuestra paridad con el motor HTML.

## Reproducción / evidencia
ZIP: `GRULLA_LII_V12_BATERIA_GENERAL_CONCORDANCIAS_2026-10-08.zip`
SHA-256: `6e6af6b37d0395f5ef45f80440e512590777545af169b77fd9b1114024eaab74`.
32 entradas, CRC + SHA-256 PASS, fuentes locales, código V12, datos RAW, summaries y manifiesto.
Ejecución íntegra: `python GRULLA_LII_CONCORDANCE_GLOBAL_V12/run_v12.py --reps 8` y `python GRULLA_LII_CONCORDANCE_GLOBAL_V12/run_structural_v12.py --reps 8` desde raíz del paquete extraído. Reproducción en carpeta nueva: **64.512 filas numéricas + 4.608 estructurales** idénticas a rep=7000/8000 de los RAW completos, en todas las columnas. Archivo principal SHA-256 `92bac2e345e49bd7b741c8e8df455b8cca33c6f0549f717b582cc72328a2eabc`. Runner estructural SHA-256 `7f0e9b8704f91602ed81f24d385583dd1175b0637086477c712af90201766915`. El paquete ZIP está entregado en la conversación; los archivos binarios grandes NO se añadieron a Git.

## Decisiones y bloqueos
**NO congelar V07 ni los seis monstruos**. No generalizar el paquete LI-V04B sobre defensivas LII: picos 10–17 pp y comportamiento desigual.
1. Calibrar individualmente por receptor las 4 relaciones sin escala; no inventar % ni fallback.
2. Revalidar los dos efectos estructurales en motor vigente.
3. Resolver hooks condicionales reales de Tramo I y PRE_COST/redondeo (especialmente Espejo de Luna Eficiencia: ahorro nominal pero 0 Qi efectivo en compilador LAB).
4. Verificar adquisición/coste reales de técnica BASE ajena y paridad de eventos contra el **HTML vigente**, no un candidato viejo.
5. Solo después cruzar V07 con Concordancias completas, LianQi I freeze (V10), técnicas, 6 monstruos y economía de equipo.

Guardias: no main, no merge, no runtime HTML, no cambio de monstruos, sin élite, sin T3/T4, no auto-freeze.
