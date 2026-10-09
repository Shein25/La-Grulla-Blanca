# La Grulla Blanca — CIERRE DE BALANCE DE HABILIDADES PRE-A08 · V17

**Estado: PERFIL NUMÉRICO DE LABORATORIO FIJADO PARA EL BALANCE DE MONSTRUOS · NO ES FREEZE CANÓNICO NI PARIDAD HTML.**

## Decisión de alcance
- Se cierra una única **línea base experimental** de habilidades de LianQi II para no recalibrar monstruos con números cambiantes. El usuario aún deberá ratificar los números finales antes de la entrega a Astra A08.
- LianQi I intacto: 0 PT, solo unitarget BASE, sin defensivas ni AOE; no se aplican efectos V17 a LI.
- LianQi II: exactamente 2 PT; Tramo I permitido; ofensiva BASE, defensa BASE; sin AOE, sin Tramo II/III. 16 builds legales por raíz, 80 en total.
- Sin tocar monstruos, equipos, economía, main ni HTML. Elementos: multiplicador neutral ×1.0.

## Cambios numéricos de técnicas seleccionados para la línea base
| Raíz / técnica | Nodo T1 | Antes | Línea base de laboratorio |
|---|---|---|---|
| Fuego · Palma Ardiente | Ascua Adherente | 2 daño por pulso | **1 daño por pulso** |
| Metal · Destello de Plata | Ejecución | +0 pp de crítico extra | **+10 pp crítico extra**, sin quitar la precisión existente |
| Viento · Lanza que Parte Nubes | Daño Directo/Punta de Tormenta | +20% daño directo | **+30% daño directo** |
| Agua · Espejo de Luna | Eficiencia | raw 4.50 → 5 Qi | **raw 4.125 → 4 Qi** en LII, equivalente a t1_flat_cost -1.50 en catálogo experimental |
| Tierra | Todas | valores actuales | **sin cambios** |

Los cuatro cambios están encerrados por nodo y etapa; las otras 64 builds monorraíz permanecieron idénticas en comparaciones pareadas.

## QA técnico de técnicas, Concordancias y prioridad
- **184.320 combates** de técnica con 16 semillas independientes; **92.160** contextos ORIGINAL vs V17; **73.728** contextos sin nodo modificado con igualdad exacta. Cero timeouts/acciones programadas omitidas.
- **248.832 combates** ON/OFF en dos cohortes de Concordancias defensivas BASE, con semillas independientes; **6.912** controles negativos exactos; cero timeouts, cero omisiones de cadencia y cero resoluciones OFF.
- Matriz LII de 20 relaciones: 17 escalares, dos estructurales (Placa Fundacional y Embalse) y una sin receptor BASE. **Los dos efectos estructurales fueron probados físicamente en V13/V16, no en la nueva campaña V17**.
- Censo 80 builds × 4 raíces extranjeras = 320 prioridades: 240 BASE_ONLY, 24 casos donde gana hook condicional por prioridad, 56 donde gana el BASE pese a exponer una rama. Se adopta el mapeo específico para Paso de Nube con Agua BASE = duración; RESPONSE con Agua = REACTIVE_RESPONSE (primer hook compatible). Es una **resolución de diseño para futura implementación**, no paridad demostrada.

## Valores numéricos de Concordancias DEFENSIVAS para el siguiente frente
La tabla versionada `CONCORDANCIAS_DEF_LII_V17_CANDIDATE.csv/json` tiene los 20 pares ORIGEN→DESTINO y sus hooks. **Es específica de LianQi II; NO sustituye los valores LianQi I V04B**. Las cuatro relaciones sin magnitud se dotan de candidatos relativos (Metal→Fuego 20%, Agua→Metal 20%, Agua→Viento 20%, Tierra→Viento 20%).
Los saltos grandes heredados se reducen a escala conservadora: Agua→Tierra 25%; Fuego→Metal 18,75%; Fuego→Viento 18,75%; Tierra→Metal Placa 15,625%. Estas cifras son **propuesta de laboratorio**, no canon humano.
- Un único Eco resuelve un solo hook primario; no se crea daño universal; NONE no consume por Concordancia; toda magnitud se escala sobre el **hook receptor propio**, no sobre una estadística global.
- Metal→Agua/Viento→Agua con Espejo Eficiencia: coste en PRE_COST antes de pago y HALF_UP una sola vez. Agua→Fuego con Cuerpo-Horno CONVERSION habilita INTERNAL_RESOURCE condicional aunque BASE sea NONE; escala experimental 10%, **sin prueba física aún**.

## Resultados selectivos del control T2, equipamiento temprano, 16 semillas
| Raíz (solo builds cuyo nodo cambió) | Win ORIGINAL | Win V17 | Delta pp |
|---|---:|---:|---:|
| Fuego | 93.36% | 83.07% | -10.29 |
| Metal | 65.62% | 73.57% | +7.94 |
| Viento | 65.10% | 74.22% | +9.11 |
| Agua | 73.05% | 73.44% | +0.39 |

### Concordancias defensivas BASE con equipo temprano contra T2 (holdout, cuatro semillas)
| Raíz receptora | OFF | ON | Delta pp |
|---|---:|---:|---:|
| Fuego | 67.74% | 68.03% | +0.29 |
| Metal | 67.45% | 71.70% | +4.25 |
| Agua | 67.19% | 67.19% | +0.00 |
| Tierra | 72.04% | 73.76% | +1.73 |
| Viento | 56.18% | 59.47% | +3.29 |

**Importante:** los ON/OFF anteriores no ejecutan hooks condicionales T1 ni los dos estructurales en el mismo combate. Tampoco verifican el coste/acceso de la técnica extranjera contra el HTML oficial. Por ello NO son una validación integral de A08.

## Restricciones y transición a monstruos
- Usar la matriz V17 como **única fuente de valores del jugador para el siguiente laboratorio de monstruos**, evitando mezclar V07 original, porcentajes LI V04B y los escalados masivos de V11–V13.
- Comparar los seis enemigos normales T0/T1/T2 por raíz, políticas, builds y equipo de comienzo/arrastre LI/esperado, luego ajustar stats de monstruos **solo si persisten anomalías**.
- El siguiente frente de monstruos puede empezar con esta línea base. En la entrega A08 hay que implementar fielmente hooks condicionales, PRE_COST, Placa, Embalse, adquisición y comprobar paridad de eventos. No adelantar un PASS HTML.
- No abrir élite, T3/T4, AOE o LianQi III en el balance de normales LII.

## Trazabilidad y reproducción
Archivos: `PROFILE_LII_SKILLS_V17.json`, `CONCORDANCIAS_DEF_LII_V17_CANDIDATE.json`, `RESOLUCION_HOOKS_TRAMO_I_V17.csv`, `QA_CIERRE_HABILIDADES_V17.json`, runners V17 y datos crudos de ambas campañas. Los datos V13/V15/V16 previos justifican solapamientos y efectos estructurales; no se declaran repetidos en V17.

**Decisión:** CIERRE DE LABORATORIO DEL PERFIL DE HABILIDADES PARA PASAR A MONSTRUOS. La ratificación canónica del usuario y la paridad A08 siguen siendo gates posteriores; no congelar silenciosamente runtime.**