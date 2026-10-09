# La Grulla Blanca — V21: auditoría de adquisición, economía y cruce focal
Fecha: 2026-10-09. **ESTADO: LAB PASS / EVIDENCIA PARCIAL / SIN APROBACIÓN CANÓNICA.** Solo rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`. HEAD inspeccionado antes del trabajo `770d0c2845ae86c102d01142eef8d7ead2316a03`.

## 1. Autoridad previa preservada
- Handoff `../handoffs/HANDOFF_PRE_A08_V20_2026-10-09.md`, registry de backup y dictamen/parche/QA/README `../pre_a08_equipo_v20/` comprobados en Git. V20 **284.160 duelos válidos**, 55.680 filas exactas de la reproducción anterior, sin repetirlos aquí.
- V17 habilidades/Concordancias fijadas solo en laboratorio, no canónicas. V19 candidatos Cangrejo T1 `DEFENSE_UP.defense_bonus` +3→+2; Jabalí T1 `MITIGATE_NEXT.damage_reduction_pct` 40→35. V20 candidato Sobretúnica `stats.defense` 2→1, manteniendo `stats.hp_max=2`. No se han modificado catálogos ni HTML.
- LI cero PT, sin defensivas/AOE. LII dos PT y Tramo I, sin AOE. T0/T1/T2 son niveles de adaptación de las seis especies normales, NO cultivo.

## 2. Evidencias de fuentes, no confundir diseño con acceso
- Catálogo Etapa18 v0.2: 68 objetos (14 LI, **21 LII**, 19 LIII, 14 LIV), fuente SHA256 `83754d92456564ed29bf0501c9b4bf2d21497100275c7b768bba77138de47190`. Todas las piezas LII `availability: OPTIONAL`; diseño: M04 8, M05 9, M06 4.
- Único HTML en este HEAD: `grulla-blanca_ver74.html`, Git blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`. Ahí `QUESTS = {}`, `CATALOGO = []`; `cmd_comprar`, `cmd_tienda`, `cmd_servicios`, `cmd_canjear` son placeholders. Los 21 IDs del equipo v0.2 no están presentes. **Cero rutas jugables verificadas para las 21 piezas en esta versión**, sin extrapolar a ver76 o integraciones externas.
- Cinco personas realmente mencionadas en HTML (13 piezas atribuidas): Jiang Rui (3), Lu Cheng (4), Ning Cai (4), Chen Bo (1), Lan Meihua (1). Nombre registrado no garantiza stock ni capacidad comercial. Otras ocho fuentes se refieren a colectivos de diseño `Puestos del Mercado del Valle` y `Artesanos de Sauces` (4 piezas cada uno), sin vendedor operativo ver74. No inventar NPC.
- `required_permission` de catálogo = **etiqueta propuesta sin gate confirmado**. Los slots y `source_mission` tampoco prueban recepción. En el HTML `gastarContribucion` y la ayuda conservan gasto legacy, expresamente contradicho por la **decisión humana vigente: Contribución no se gasta**. Ningún precio legacy se traduce automáticamente a nuevo gate o requisito de mérito.
- 14 piezas tienen `price_stones`; 10 tienen `price_contribution` (tres con ambos, **siete solo Contribución**). No se ponen 0 piedras a las siete: precio pendiente. Solo `amuleto_colmillo_montado` requiere material `colmillo_lobo_legitimo` +4 piedras; ese ID no aparece en ver74, por tanto fuente no demostrada.
- Ver74 empieza con cero piedras, conserva `entregarRecompensa` y ciertos drops legacy como bolsas de 12 piedras; no hay rendimiento económico sostenible demostrado para M04–M06. Los drops se resuelven en `mob.loot` y la extracción manual por sus propios contratos, **no confundirlos**. Las seis especies normales del runner de laboratorio no aportan una tabla oficial de botín comercial.

## 3. Matriz 21/21 LII (solamente datos escritos en el catálogo)
| ID | Slot | Hito propuesto | Fuente nominal (NO acreditada como vendedor) | Piedras de diseño | Contribución legacy rechazada |
|---|---|---|---|---:|---:|
| `espada_hierro_equilibrada` | ARMA | M04 | Lu Cheng | 12 | 5 |
| `sable_patrulla_valle` | ARMA | M04 | Lu Cheng | 10 | — |
| `aguja_acero_frio` | ARMA | M06 | Lu Cheng | — | 5 |
| `bandana_cuero_reforzada` | TOCADO | M04 | Ning Cai | 7 | 2 |
| `capucha_observador_valle` | TOCADO | M05 | Puestos del Mercado del Valle | 7 | — |
| `sobretunica_patrulla` | VESTIDURA | M04 | Jiang Rui | — | 3 |
| `tunica_ruta_sauces` | VESTIDURA | M05 | Artesanos de Sauces | 10 | — |
| `brazales_cuero_cruzado` | BRAZALES | M04 | Ning Cai | 9 | 3 |
| `brazales_pulso_firme` | BRAZALES | M06 | Chen Bo | — | 3 |
| `fajin_patrulla` | FAJIN | M04 | Jiang Rui | — | 2 |
| `calzas_sendero_pinos` | PIERNAS | M04 | Ning Cai | 8 | — |
| `sandalias_corriente_ligera` | CALZADO | M05 | Artesanos de Sauces | 11 | — |
| `botas_piedra_humeda` | CALZADO | M05 | Puestos del Mercado del Valle | 9 | — |
| `amuleto_colmillo_montado` | AMULETO | M05 | Ning Cai | 4 | — |
| `amuleto_sauce_sereno` | AMULETO | M05 | Artesanos de Sauces | 10 | — |
| `pulsera_cauce_trenzado` | PULSERA | M05 | Artesanos de Sauces | 8 | — |
| `anillo_sello_hierro` | ANILLO | M06 | Lu Cheng | — | 4 |
| `anillo_corriente_clara` | ANILLO | M05 | Puestos del Mercado del Valle | 10 | — |
| `pulsera_tension_meridiana` | PULSERA | M06 | Lan Meihua | — | 4 |
| `calzas_guardia_externa` | PIERNAS | M04 | Jiang Rui | — | 2 |
| `anillo_reserva_menor` | ANILLO | M05 | Puestos del Mercado del Valle | 8 | — |

Se guarda también `MATRIZ_21_LII_V21.csv` con `source_type`, sala de diseño, etiquetas de permisos, materiales y estadísticas, junto con estado de adquisición. Todos los registros son **DISEÑO SIN DISPONIBILIDAD JUGABLE PROBADA EN VER74**, no una recomendación de suministrar estos objetos automáticamente.

## 4. Hipótesis económica para revisión, no ratificadas
1. **No gasto de Contribución** en compra, venta, intercambio, servicios ni alquimia. Merito histórico podría informar rangos ya reconocidos; **no se crea gate** ni se inventa permiso nuevo.
2. Mantener 14 precios de piedras como **anclas de simulación**; siete restantes como `PENDIENTE` hasta auditar fuentes efectivas y coste de oportunidad, sin conversión arbitraria de puntos de Contribución a piedras.
3. Considerar una sensibilidad de reventa de **25–40% del precio de compra**, como rango a ensayar, no tarifa ni decisión aprobada. Prohibir arbitraje infinito vendedor→reventa y materiales→craft→reventa. Stock y repetibilidad sin especificar hasta encontrar vendedores operativos.
4. Intercambio y recompensa de materiales solo con IDs existentes y fuente comprobada. Los contratos de requisiciones y oficios son propuestas de diseño, no misiones ejecutables `QUESTS` en ver74.
5. Priorizar reconstrucción del ingreso de piedras por misión/derrota/exploración, fuentes de drops (separadas de extracción), acceso NPC/servicios, stock y permisos existentes antes de congelar economía.

## 5. Cruce focal de combate V21 nuevo, sin repetir V17–V20
- El runner `run_v21_focal_access.py` usa **la implementación de laboratorio V20 reproducible**, conserva habilidades V17, cinco Concordancias escalares BASE representativas (una por raíz); no supone físicamente las 20 relaciones ni hooks estructurales/condicionales. Se modela técnica ajena como aprendida, según limitación ya reconocida.
- Se hicieron dos cohortes independientes: DISCOVERY reps semillas 99100–99101 y HOLDOUT 99200–99201, **14.080 duelos cada una = 28.160 válidos**, seis monstruos normales, cinco raíces, 16 builds por raíz, T0/T1/T2, EARLY/DELAYED_TRIGGER. Control `PROLOGUE_DESIGN` vs `M03_ISSUED_DESIGN`. Estas son **dotaciones de referencia de diseño**, no prueba de obtención real por ver74. No se equipa ninguna de las 21 LII no verificadas.
- Comparaciones pareadas con mismo RNG de ORIGINAL/CANDIDATE V19 solo en Cangrejo/Jabalí T1/T2; en otras especies se preserva habilidad original. Sin timeouts, sin acciones `due_missed`, capacidades originales restauradas y sin cambiar runtime.

| Especie T2 / referencia M03 | Original jugador | Candidato V19 | Diferencia |
|---|---:|---:|---:|
| Araña veta sombría | 67,03% | — | — |
| Búho niebla gris | 72,03% | — | — |
| Zorro bancales | 76,41% | — | — |
| Murciélago resonante | 74,22% | — | — |
| **Cangrejo cauce** | **64,84%** | **70,94%** | **+6,09 pp** |
| **Jabalí pizarra** | **74,53%** | **76,41%** | **+1,88 pp** |

- En T1, Cangrejo 67,03→72,03% (+5,00 pp) y Jabalí 80,16→81,56% (+1,41 pp). Todos los porcentajes son victoria jugador y estimaciones Monte Carlo del laboratorio, no dificultad aprobada.
- **Economía Qi:** se miden `qi_spent` y `qi_final`; Murciélago T2 M03 consume en promedio 36,213 Qi y acaba con 0,267 Qi (reserva final), con victoria 74,22% frente a 74,38% del Prólogo. La información es sensible a modelo, semilla, políticas y builds; no conclusión universal.
- **Aflicciones/antídotos:** ver74 posee recetas `antidoto_jade` (veneno jade grado I) y `balsamo_ceniza` (quemadura ceniza grado I), pero el runner V20/V21 no procesa persistencia de aflicciones ni uso de antídotos. Por tanto **veneno, antídotos y coste de curación quedan SIN PRUEBA**, especialmente contra Araña. No inventar resultados de cobertura.

## 6. QA y reproducibilidad
- PASS 28.160 combates nuevos, 0 timeouts, 0 turnos de monstruo omitidos, semillas comunes entre brazos, sin manipulación permanente del monstruo, `qi_final>=0`. Control frío independiente: **7.040/7.040 filas idénticas, todas las columnas**. No se reinició ninguna batería antigua.
- Dependencias Python 3.11+ y `pandas`, fuente y hojas brutas dentro del ZIP V21 separado. El runner se conserva aquí en Git y debe copiarse al lado de `run_v20.py` al ejecutar con la estructura original del paquete V20; Git no incluye los datasets ZIP crudos.
- ZIP V21 `GRULLA_PRE_A08_V21_ACCESO_ECONOMIA_Y_FOCAL_2026-10-09.zip`: SHA256 `d9f5b7e952c4c617c82b7fca9746a2e1aef15b8f6b0b42e9a54a936a4dd1e01a`, **56 entradas, CRC PASS**. Baseline backup completo V17–V20 SHA256 `96a0bbe760d62590217f104d5400e1963ac57ea0da440d84f41b71378c09f30d`. Ver `QA_V21_2026-10-09.json` para hashes de CSV y evidencias.

## 7. Dictamen y bloqueo a Astra
- Candidatos **NO RATIFICADOS**: V20 Sobretúnica DEF2→1, HP+2; V19 Cangrejo +3→+2 y Jabalí 40→35. Mantener control de nivel LI, los dos PT de LII y ausencia de AOE.
- **NO EMITIR FREEZE FINAL PRE-A08**: para las 21 LII falta ruta real; para siete no hay alternativa de piedras, falta oferta/stock, recompensas y material `colmillo_lobo_legitimo`, políticas compra/venta/canje y antiarbitraje, prueba de persistencia de aflicciones/antídotos y posterior regresión sobre dotaciones *obtenibles* tras cerrar la economía. V17 Concordancias estructurales/condicionales tampoco representadas aquí.
- La responsabilidad de balance permanece en este frente. Paridad HTML e integración futura corresponden a Astra después de decisiones humanas explícitas. Ningún cambio a `main`, ningún merge, ninguna escritura en HTML, `ROOMS.exits`, NPC, misiones, vendors ni gates.
