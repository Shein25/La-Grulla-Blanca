# V39 — Eco del Caído: etapa de acceso y sensibilidad E8 T0
**2026-10-09 · LAB_PASS / E8 NOT RATIFIED / NO CANON / NO HTML / NO MAIN.**

## Estado humano previo
**Viento V38 ratificado**: `lanza_nubes` cuesta 5 Qi en LianQi II, y 4 Qi si se eligió `lanza_t1_eff`. En LianQi I cuesta 6 Qi. V36 permanece: Direct T1 30%, Precisión T1 `2d4+4`, Paso evasión T1 45. Seis normales LII cerrados (V35), Sobretúnica DEF+2/HP+2 **intacta**. Fuente primaria: `experimentos/balance_nuevo/handoffs/CIERRE_RATIFICADO_VIENTO_Y_NORMALES_2026-10-09/RATIFICACION_LANZA_QI5_V38_2026-10-09.json`.

## Punto estructural hallado: encuentro demasiado temprano
El HTML histórico ver74 (Git blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`) contiene 329 salas y 11 puertas de progresión. Una búsqueda de rutas determinista halló **20 movimientos desde `patio_raices` hasta `cruce_vetas` sin atravesar gates cerrados**, por rutas válidas en `ROOMS.exits`. Allí figura como único `eco_caido`. La sala `cruce_vetas` está marcada `oculta:true`, que oculta la salida en la interfaz, pero `cmd_ir` + `bloqueoPaso` sólo controlan la existencia de arista y gates, no el nivel LianQi del personaje. La última transición es `terraza_cantera --sur--> cruce_vetas`.

**Importante:** esto es una vulnerabilidad de progresión en la fuente ver74, no prueba de que ver76 productivo carezca de un control adicional. Podría ser una amenaza secreta intencional. **No se modificaron rutas, misiones ni gates.**

## E8 original y límites
Del handoff Git `handoff/lii-monsters-close-2026-10-08`, blob `a0ecb21dafe126d05d897349ee1889198b8c088b`: HP=84, PREC=96, EVA=18, DEF=1, TEN=18, daño básico `1d2+4`. **Control no recuperado** y `technique=null` en el registro moderno. Para simulación se puso `control=0` en clon de RAM `READY`. Al repetir **20 pares / 40 peleas de control** con `control=0` vs 60, *todas* las métricas de T0 coincidieron; ello **no ratifica** el campo Control, demuestra solamente que E8 sin técnica especial no lo utiliza en esa ruta del motor.

El registro original continúa `PENDING_INTEGRAL_REBALANCE`, sin técnicas, `BLOCKED_UNTIL_T0_READY`, sin activar T1/T2.

## Batería V39 nueva
- **18.240 peleas nuevas**: DISCOVERY 9.120 y HOLDOUT 9.120, dos cohortes independientes. De ellas **2.880 LI** (Eco, Sapo READY y Escarabajo READY), y **15.360 LII** (sólo Eco).
- **2.160 filas ×19 columnas COLD idénticas**, no sumadas; 0 timeouts, fuentes y equipo sin modificar. ZIP extraído en carpeta nueva: CHECKS, COLD y análisis PASS.
- Cinco raíces; LI sólo ofensiva sin Tramos con dotación de Prólogo garantizada; LII 16 builds T1 por raíz y dos políticas, con equipo P, después de M03, vestidura de patrulla M04 **opcional de diagnóstico** o Sauces M05 **opcional de diagnóstico**.
- E8 T0 comparado solo bajo cifras históricas recuperadas; **sin Concordancias condicionales completas, aflicciones persistentes ni paridad productiva**. El uso de una defensiva LII en el fixture **no demuestra que esté realmente aprendida**.

### LI, equipo P, solo ofensiva (960 peleas cada enemigo)
| Rival | WR jugador | IC95 Wilson |
|---|---:|---:|
| **Eco E8** | **9,69%** | 7,97–11,72 |
| Escarabajo de Hierro READY | 9,48% | 7,78–11,50 |
| Sapo de Ceniza READY | 42,71% | 39,61–45,86 |

**Eco no es una pelea de dificultad LI ordinaria**. Contra Eco E8 por raíz LI: Fuego 29,17%, Agua 6,77%, Tierra 6,25%, Viento 4,17%, Metal 2,08% (n=192 cada uno).

### LII, contra E8
| Equipo | Política | WR jugador | n |
|---|---|---:|---:|
| Prólogo garantizado | Sólo ofensiva | 69,43% | 1.920 |
| Post-M03 garantizado | Sólo ofensiva | 70,52% | 1.920 |
| Post-M03 garantizado | Defensa hipotética | 81,41% | 1.920 |
| **Sobretúnica M04 opcional** | Sólo ofensiva | **96,67%** | 1.920 |
| **Sobretúnica M04 opcional** | Defensa hipotética | **98,80%** | 1.920 |
| Sauces M05 opcional | Sólo ofensiva | 77,14% | 1.920 |
| Sauces M05 opcional | Defensa hipotética | 84,01% | 1.920 |

Pareados con kit P sobre 3.840 contextos (2 políticas, 5 raíces, 16 builds, 2 cohortes): M03 +1,67 pp, Sobretúnica opcional **+23,44 pp**, Sauces opcional +6,28 pp. **No interpretar esas tasas como acceso efectivamente acreditado**. Viento LII kit P con Qi5: 69,79% ofensiva / 70,31% defensiva, n=384 por celda.

## Dictamen
**No ratificar E8 todavía**: LI casi siempre pierde si llega temprano, mientras que con la mejor vestidura LII un E8 basado solo en ataques básicos suele caer. El diseño debe determinar expresamente si su acceso previo a LII es una amenaza secreta deliberada, o si la **activación del encuentro** requiere una condición de progresión preexistente, **sin tocar `ROOMS.exits`**. Una vez decidido el momento esperado, evaluar su **identidad de élite y presión especial propia** en LAB; no empeorar al jugador ni debilitar la Sobretúnica.

No inventar NPCs, quests, puertas, monstruos ni estados canónicos y no tocar `main`. Repetir campañas históricas V02 o V33–V38 no aporta a este gate.

## Reproducción
ZIP portable **`GRULLA_PRE_A08_V39_ECO_ETAPA_Y_GATES_T0_2026-10-09.zip`**, SHA256 **`eb9c8fd127df1120decf5584dfbd1d26d78ad47c47fbe91f40495d428d244bbd`**, **26 entradas**, 532.693 bytes. CRC + manifiesto SHA256 PASS; COLD + QA + análisis ejecutados desde carpeta limpia PASS. Runner SHA256 `cbb0fd3f40ba5b93d4e41997c6b8acb502590ba506c349f949a5e5fdc94963dd`; análisis SHA256 `9828f745c3302fba3facb5441ed97889cd6935ee80780fa0b09448a158b5abd9`. El ZIP con fuentes originales LAB y CSV brutos está adjunto en la conversación, no subido a Git.

**Guardias:** no main, no merge, no HTML, no ROOM exits, no A07, sin alteraciones a monstruos normales, Viento V38, equipo, mercado ni precios.
