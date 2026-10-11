# V69 — Eco del Caído: habilidades nuevas y evaluación del límite 70%

**Fecha:** 10 de octubre de 2026. **Estado:** `HUMAN_AUTHORIZED_NEW_ABILITIES / LAB_PASS / NO_PRODUCTION_PATCH / PENDING_T0_AUTHORITY_RECONCILIATION`.

## 1. Decisión humana, alcance, guardas

El autor pidió **añadir nuevas habilidades al élite Eco del Caído** y que la **victoria del jugador no supere el 70%**. El frente ha sido ejecutado y verificado numéricamente en el motor físico E1/ETAPA19B de LianQi II, **solo 1v1 PRE-AOE**. Los valores son un candidato de integración, NO la certificación del HTML real. Autoridad estructurada: [`ECO_DEL_CAIDO_HABILIDADES_V69_CANDIDATO.json`](ECO_DEL_CAIDO_HABILIDADES_V69_CANDIDATO.json).

Se dejó intacta la ficha candidata E8 de PRE-A08/V39 (HP 84, PREC 96, EVA 18, DEF 1, TEN 18, básico `1d2+4`, sin especial original), sin aumentar vida/DEF ni modificar la Sobretúnica superior de LII.

## 2. Tres habilidades de élite

**Veta Resentida — reserva de la veta.** En el primer cruce a HP ≤60%, mientras vive, obtiene 12 puntos de absorción de una sola activación, sin regenerarse ni aumentar DEF. Daño directo y DOT reales consumen la misma reserva.

**Lamento del Caído — invocación espiritual telegráfica.** Se avisa al jugador antes de su acción en cada 4ª ronda. Al resolverse la acción voluntaria del élite, intenta `1d2+3` directo; si conecta y el jugador sigue vivo, aplica `1d2+3` espiritual ×2 pulsos, sin apilar el mismo origen. El daño espiritual atraviesa DEF plana, NO absorción. Si el jugador activa de verdad una defensiva y paga Qi durante el aviso, la aflicción se reduce a 1 pulso de 50% daño; si conecta una ofensiva que elimina ≥18% HPmax del Eco durante el aviso, interrumpe el Lamento. Control válido que impida acción del Eco también la cancela. No crear relojes o timers nuevos: `FightState.round_no` es la autoridad.

**Reverberación del Agravio — remordimiento del golpe.** Un golpe conectado que quite realmente ≥12% HPmax del Eco mientras éste sigue vivo prepara una réplica para su **siguiente acción voluntaria**. El aviso permite activar defensiva pagada o Control válido para cancelar la marca. Si no se evita: `1d2+8` de daño espiritual, atraviesa DEF pero respeta absorción. Máximo dos marcas por combate y cooldown de tres rondas. No mira la raíz del jugador; se desencadena por HP real perdido, no daño absorbido.

Estas habilidades son **reacciones locales T0 del encuentro único**; NO constituyen cadena adaptativa T1–T4, ni Mutante, ni técnica AOE, ni asignan nuevas habilidades al jugador.

## 3. Validación física independiente y controles

La batería definitiva se recalculó íntegramente después de corregir el wrapper experimental de un turno omitido por Control (bug **solo del LAB**, no del runtime). **192.000 combates nuevos**: 5 brazos ×38.400 peleas con 5 raíces ×3 builds legales de 2 PT LII ×2 equipamientos máximos LII ×4 políticas ×320 semillas nuevas por estrato. Se retuvo una semilla inicial por escenario en los cinco brazos; el consumo posterior del RNG puede divergir si las habilidades añaden eventos. 0 timeouts.

| Brazo físico | Victorias del jugador |
|---|---:|
| Eco E8 original sin habilidades | **98,97%** |
| E8 + solo Veta Resentida | 95,81% |
| E8 + Veta + Lamento | 69,45% |
| E8 + Veta + Reverberación | 80,00% |
| **E8 + las tres habilidades V69** | **45,27%** |

QA: **1.050 parejas de regresión E1** compararon sin habilidades el wrapper contra el original en HP, Qi, rondas y daño y produjeron **0 diferencias**. Adicionalmente: invariantes de 192.000 filas, 5 brazos completos, procs/cooldowns/acumulaciones correctos, ningún timeout, 0 fallos.

| Raíz | Victoria del jugador |
|---|---:|
| Fuego | 62,86% |
| Metal | 34,69% |
| Agua | 55,49% |
| Tierra | 35,60% |
| Viento | 37,71% |

| Política del laboratorio | Victoria del jugador |
|---|---:|
| Solo ataque ofensivo | 26,91% |
| Defender primera ronda y atacar | 32,21% |
| Defender ante Lamento | 54,24% |
| **Leer ambos avisos y defender correctamente** | **67,73%** |

| Equipo máximo LII | Victoria del jugador |
|---|---:|
| Defensivo | 55,54% |
| Evasivo | 35,01% |

### Interpretación estricta del «70%»

**PASS en promedios:** 45,27% global, las cinco raíces por separado, ambos equipos por separado y las cuatro políticas por separado son todos ≤70%. **NO se promete un techo de cada microcohorte**, que además contradiría el principio de pericia táctica. En particular, **máximo DEF LII + política que lee ambos avisos** tuvo **79,46%** de victorias. Este porcentaje está explícitamente documentado, no oculto. No imponer un 70% artificial por RNG o derrota forzada; si el autor exige techo en TODAS las combinaciones, reabrir una prueba específica, consciente del coste de penalizar a Metal/Tierra/Viento.

### Archivos y reproducibilidad

ZIP portable **`GRULLA_V69_ECO_DEL_CAIDO_HABILIDADES_BALANCE_2026-10-10.zip`**, SHA-256 `4e59f1cbb3fbcda45824a9b69c28a2bb168044a771e6c2be3afed975f63041f2`, **2.131.643 bytes, 14 archivos, CRC + manifiesto SHA256 PASS**. Contiene:
- `v66_original.zip`: fuente física original sellada.
- `eco_v69_engine.py`, `eco_v69_main_holdout.py`, `eco_v69_qa.py`, `eco_v69_finalize.py`: runner, QA y report reproducibles.
- `ECO_V69_HOLDOUT_RESULTS.csv` (192.000 combates), agregados, estratos cruzados, pares base/final.
- Configuración machine-readable, informe, hashes y README.

**El ZIP con scripts está adjunto a esta conversación pero NO se ha subido al Git**; el repositorio guarda la decisión, números y QA. No afirmar que HTML ha recibido los cambios.

## 4. Bloqueos antes de integrar en runtime

**Conflicto T0 no resuelto:** commit `45c3a9c240ea74208a0d8fd4d5be187bc817df35` fechado el 2/10 declara `eco_caido` HP 51, `READY`, `UNIQUE_T0_CLOSED_NO_T1_T4`; rama PRE-A08 posterior/V39 usa E8 HP 84 `PENDING`. El usuario autorizó habilidades nuevas y el límite de dificultad, pero NO decidió sustituir oficialmente el T0 ratificado anterior. No reescribir ninguna fuente hasta conciliar.

**Acceso:** en ver74 existía ruta oculta a `cruce_vetas` desde LI sin gate. V39 advierte ~9,69% de victorias LI frente E8 antes de las nuevas habilidades; añadir habilidades haría más peligroso un acceso temprano. No se ha comprobado paridad de acceso en ver76 y el autor NO ha decidido si el riesgo secreto LI es intencional. Prohibido inventar gates/salas o cambiar `ROOMS.exits`.

**UI e IA:** los avisos se representaron en policies del LAB, no en un HUD/registro auténtico. Falta conexión con NEW, selección de acciones, coste de defensa, Control, DOT, absorción, antídotos, SAVE/LOAD y ciclo de muerte única. Revalidar con equipo realmente adquirible y Concordancias legales antes de aplicar.

**Orden siguiente:** decisión humana de autoridad T0 y exposición LI; integración Astra de tres habilidades con telegráficos auténticos y pruebas E1/HTML; después continuar test AOE contra repetibles LIII. No reabrir V35 seis normales LII, los T0 ratificados, las Ultis V67 ni los cinco guardianes.

**Guardas permanentes:** NO MAIN, NO MERGE, NO HTML/productivo, NO `ROOMS.exits`, NO gate nuevo, NO nerf de equipo, NO adaptación T1–T4 del único, NO alterar economía/drops/misiones/NPC/A07.
