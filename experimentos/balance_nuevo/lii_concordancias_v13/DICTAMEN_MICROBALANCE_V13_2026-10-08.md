# La Grulla Blanca · LianQi II · V13 — Microbalance de Concordancias defensivas y Qi

**Fecha:** 2026-10-08  
**Estado:** LAB PASS EXPERIMENTAL / NO CANON / NO HTML / NO FREEZE

## 1. Contexto y reglas inalterables

V12 mostró saltos defensivos especialmente grandes de Agua→Tierra, Fuego→Metal y Fuego→Viento. En V13 se analizan con más resolución de escala y semillas nuevas. Los números de referencia **proceden del paquete experimental LI V04B** y no están ratificados como valores LII. Las fracciones 12,5 %, 25 %, 50 % y 100 % **multiplican ese pack anterior**, no representan porcentajes de bonus universal ni recomendaciones de implementación.

- Progresión: LI 0 PT y sin defensivas/AOE; LII 2 PT, Tramo I, unitarget + defensivas, sin AOE.
- Seis monstruos repetibles normales LII, T1/T2 (T0 ya cubierto en V12); excluye élite, T3/T4 y jefes.
- Cinco raíces, multiplicador elemental neutral ×1,00, 16 builds legales por raíz receptora, equipos POST_M03 / EXPECTED_STAGE y políticas EARLY / DELAYED_TRIGGER.
- Las técnicas BASE de otra raíz se suponen aprendidas solo para crear el Eco: adquisición, permiso y coste no se han contrastado con el HTML definitivo.
- No modificar stats de monstruos, balance V07, catálogo, equipamiento, LI, main ni runtime. No merge.

## 2. Batería A · Sensibilidad escalar

- **92.160 combates físicos**, **18.432 contextos completos de cinco brazos** (OFF y cuatro intensidades), semillas 9000–9007, emparejados por spawn, build, equipo, política y criatura.
- Relaciones analizadas: AGUA_TO_TIERRA, FUEGO_TO_METAL, FUEGO_TO_VIENTO.
- QA: **0 timeouts**, **0 omisiones de ataques canónicos**, mismo seed en los cinco brazos; OFF registra 0 resoluciones, ON **15.902** por intensidad. El número de resoluciones es idéntico en cada brazo no nulo.

T2, POST_M03, promedio EARLY+DELAYED, victorias adicionales del jugador respecto a OFF. **1.536 pares por relación e intensidad**:

| Relación | 12,5 % | 25 % | 50 % | 100 % |
|---|---:|---:|---:|---:|
| Agua→Tierra | +5,66 pp | +9,11 pp | +12,43 pp | +17,06 pp |
| Fuego→Metal | +6,71 pp | +7,23 pp | +10,29 pp | +11,65 pp |
| Fuego→Viento | +3,19 pp | +6,64 pp | +15,36 pp | +20,38 pp |

**Lectura causal:** Agua→Tierra y Fuego→Metal ya producen ventajas significativas en el primer punto de sensibilidad; Fuego→Viento amplifica fuertemente al escalar. Los comportamientos proceden de la magnitud receptora, redondeos, DEF/absorción y trayectoria de combate: no asignar una escala genérica de LII. Un aumento de la tasa de victorias no equivale a un error por sí solo, pero los saltos obligan a comparar con otras relaciones, builds y equipo antes de ratificar.

## 3. Batería B · Placa Fundacional y Embalse físicos

- **61.440 combates**, **12.288 contextos completos de cinco brazos**, mismas semillas nuevas 9000–9007.
- Tierra→Metal (Placa Fundacional) y Tierra→Agua (Embalse) usan el parche físico experimental del corredor LI V04B adaptado a LII. **No son simulaciones del HTML definitivo.**
- QA: **0 timeouts**, 0 técnicas programadas omitidas, 0 cambios estructurales en OFF. Placa preservó **5.530** primeras placas y reforzó **5.452** impactos por cada brazo ON (la cantidad de eventos no depende de la intensidad).
- Embalse con 12,5 % almacenó **193,18** y liberó **160,99** unidades; con 100 % almacenó **1.516,42** y liberó **1.256,56**. Se respetó liberación ≤ almacenamiento y no hubo fugas en OFF.

T2, POST_M03, promedio EARLY+DELAYED, 1.536 pares por intensidad:

| Transformación | 12,5 % | 25 % | 50 % | 100 % |
|---|---:|---:|---:|---:|
| Placa Fundacional | +3,65 pp | +5,08 pp | +6,12 pp | +6,84 pp |
| Embalse | +0,00 pp | +0,00 pp | +0,00 pp | +0,00 pp |

La primera preservación de Placa es **estructural**, por lo que reducir su escala numérica no elimina su contribución táctica. Embalse no generó conversiones de derrota a victoria **en estas políticas y combates**, aunque sí se almacenó y liberó absorción; comprobar duración, timing y defensas reiteradas antes de concluir que el hook es inútil.

## 4. Batería C · Qi de Espejo de Luna (sin escala inventada)

Auditoría determinista: **160 builds×equipos compilados**, todas las 16 builds por raíz y dos equipos. En Agua se compararon las ocho filas de Eficiencia con su receptor BASE:

- BASE: 5,25 Qi bruto → 5 Qi efectivos.
- Eficiencia Tramo I: 4,50 Qi bruto → 5 Qi efectivos.
- Todas las magnitudes defensivas compiladas son iguales cuando se excluyen exclusivamente los metadatos de elecciones y el coste bruto.
- Contraste operativo: **768 activaciones pareadas** (4 builds de Eficiencia × 6 monstruos × 2 equipos × 16 semillas) comprobaron Qi posterior, Qi gastado, reserva y duración: **0 diferencias**.
- Viento/Eficiencia sí reduce 7 → 6 Qi.

Es un nodo de Agua sin beneficio inmediato en el puente de laboratorio. **No se verifica aquí PRE_COST/Concordancia condicional**, ni paridad con el HTML vigente: no implementar un cambio hasta revisar ambas semánticas.

## 5. Cobertura incompleta y próximos bloqueos

Las relaciones **METAL_TO_FUEGO, AGUA_TO_METAL, AGUA_TO_VIENTO, TIERRA_TO_VIENTO** muestran potencial receptor defensivo BASE, pero LI-V04B no posee magnitud para ellas. **NO se inventó escala ni se ejecutó un bonus numérico para esos casos.** También falta resolver prioridades condicionales de Tramo I y comprobar recetas estructurales en el runtime vigente.

- Validar mecánicas y adquisición/coste legal de técnica BASE ajena en el HTML candidato **vigente** (el archivo antiguo consultado no constituye autoridad de paridad).
- Calibrar la matriz por receptor, no solo el win-rate medio por raíz; probar raíces ajenas legalmente aprendidas, mutantes y políticas tácticas realistas.
- Ejecutar V07 ON/OFF con todas las Concordancias LII **cuando el resolvedor esté ratificado**. LI congelado requiere regresión antes de integrar.
- No congelar V07, magnitudes LII de Concordancias ni seis especies normales todavía.

## 6. Reproducción e integridad

Directorio V13: `GRULLA_LII_CONCORDANCE_MICRO_V13/` y bases V12/V11/V10/V07 incluidas en el paquete ZIP entregado. Runners: `run_v13.py`, `audit_qi_v13.py`, `verify_water_qi_v13.py`. Semillas nuevas 9000–9007; `python run_v13.py --reps 8 --mode scalar`, `--mode structural` ejecutados por separado en proceso fresco.

Todos los resultados son **experimentos**, no modificaciones del juego. Los hashes individuales de cada archivo y el del ZIP están en el manifiesto de entrega.

## 7. Verificación adicional antes del registro en Git

- Archivo ZIP comprobado con CRC y SHA-256 de 38 entradas.
- Reproducción independiente desde carpeta limpia con semillas 9000: **11.520 combates escalares + 7.680 combates estructurales**, idénticos fila por fila a la batería principal en todas las columnas; tests QA del compilador y 768 activaciones concordaron.
- SHA-256 ZIP: `c30a090249e4fd2f6ee6253027271af65a6fab9169032cd8c8acbf9497b87129`.
- Los CSV comprimidos permanecen en el ZIP reproducible entregado en la conversación. Este commit guarda el dictamen, no el archivo binario.
