# PRE-A08 V27 — Aflicciones persistentes y supervivencia secuencial
**Fecha:** 2026-10-09. **Estado:** LAB PASS / EXPOSICIÓN CONTROLADA / NO CANON / NO RUNTIME. **Precios y comercio EXCLUIDOS.**

## Fuentes de autoridad verificadas
- Persistencia de referencia **ver74**, Git blob `d34f7ea3f9de9344130aa072fac34d14a7a474d6`: contrato 14410–14437; `aplicarAfliccion/avanzarAflicciones/tratarAfliccion` 16498–16561; `beber` 19992–20015; acción de medicina en combate 15217–15271.
- HP LianQi II Templada **Estable, 3d4+9** ya ratificado en `ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json`, blob `1bf62d905bc2eb1399c3fafb5da9c8d0069932f1`. No se modifica.
- Veneno Jade I o Quemadura Ceniza I: `tipo,familia,grado=1, daño=1d2,duracion=3,origen`; remedios correctos específicos. Exposición se **inyecta controladamente después de ganar la primera pelea**: NO deriva de Rata de Qi ni valida bridge productivo de monstruos. Motor LAB V19 usa `MONSTER_DOT` solo intraduelo.

## Configuración
Primer duelo real contra Rata de Qi T0 (LI), ganado; después se inyecta una aflicción Jade I o Ceniza I; una acción física caminar aplica un tick sin muerte exterior (mínimo 1 HP); segundo duelo real contra una de seis especies LII originales V19 (Araña, Búho, Zorro, Murciélago, Cangrejo, Jabalí) T1/T2. Cinco raíces, 16 builds por raíz, políticas EARLY/DELAYED_TRIGGER, M03 o Sobretúnica de patrulla **DEF+1/HP+2 candidata**. HP y Qi se transportan sin recuperación gratuita. Se supone disponible cada medicina para aislar efecto: **NO** se prueba inventario/adquisición/recetas/economía.

Comparar semillas pareadas: UNTREATED; CURE_BEFORE_WALK; CURE_AFTER_WALK; INCOMPATIBLE_MED; HP_POTION_ONLY; CURE_PLUS_HP_POTION; CURE_IN_COMBAT. Fuera de combate usar medicina no hace tick de aflicción; en combate consume una acción completa, con respuesta enemiga y tick.

## Resultados y QA
| Medida | Resultado |
|---|---:|
| Primeras peleas únicas, compartidas en brazos comparativos | 1.280 |
| Segundas peleas físicamente ejecutadas | 212.856 |
| **Ejecuciones nuevas** | **214.136** |
| Escenarios comparativos (incluye caída previa) | **215.040** |
| DISCOVERY, semillas 101200–101201 | 107.520 escenarios |
| HOLDOUT, semillas 101600–101601 | 107.520 escenarios |
| COLD semilla 101200, comprobación exacta | **53.760 filas × 37 columnas** |
| Timeouts / turnos monstruo omitidos | **0 / 0** |
| Control negativo, remedio incompatible | **idéntico a UNTREATED** |

Porcentaje de victoria **segundo combate T2**, condicionada a ganar el primero, Sobretúnica DEF1 candidata; `n=3804` por aflicción y estrategia:

| Estrategia | Jade I | Ceniza I |
|---|---:|---:|
| Sin tratamiento | 2,84 % | 2,79 % |
| Incompatible | 2,84 % | 2,79 % |
| Remedio después de caminar | 4,21 % | 4,36 % |
| Remedio antes de caminar | 5,23 % | 5,23 % |
| Remedio durante combate | 2,23 % | 2,34 % |
| Medicina HP Templada estable | 15,96 % | 15,90 % |
| **Remedio correcto + medicina HP** | **24,00 %** | **24,03 %** |

Contraste pareado T2/DEF1: **Jade cura+HP vs solo HP +8,04 pp [7,14; 8,95]**; **Ceniza +8,12 pp [7,24; 9,01]** (IC 95% aproximado). Curar antes vs después de caminar: Jade +1,03 pp [0,66; 1,39]; Ceniza +0,87 pp [0,54; 1,20].

**Advertencia:** Qi medio al iniciar segundo encuentro ≈7,03; tasas absolutas tan bajas representan una expedición agotada **sin reposición de Qi**, NO dificultad normal con recursos llenos. En combate el tratamiento desplaza acción ofensiva; ninguna cifra autoriza nerfear el remedio o el monstruo.

## Dictamen y límites
La persistencia/control de tratamiento basada en el contrato ver74 funciona en **adaptador LAB**; la fuente de veneno/quemadura en combate y su transformación `impact actual_hp_damage -> player.aflicciones -> guardar/cargar` **no queda validada** en el nuevo motor productivo. Tampoco probaron T3/T4, jefe, AOE, Qi potion ni disponibilidad. La Sobretúnica DEF1/HP2 y las propuestas V19 no se aplicaron; monstruos originales intactos. V26 Concordancias condicionales siguen magnitudes LAB sin ratificar; V25 Embalse requiere diagnóstico de utilidad. **No declarar PRE-A08 FREEZE integral.**

Reproducibilidad portable en ZIP `GRULLA_PRE_A08_V27_BALANCE_PURO_AFLICCIONES_SECUENCIALES_2026-10-09.zip` (se entrega separado de Git) SHA-256 `b319dbc0f066fdc799a0af36685f8650559ff1409721bc2603c017115afa4d16`; **56 archivos; CRC+manifest PASS; test contract PASS; control COLD desde extracción independiente exacto 53.760 filas**. Fuente ejecutada `run_v27_persistence.py` SHA256 `deb19a0c43444cd8d17ed007aeb5a1a19c01538cc8a1b72325b5c272c8dd2722`; análisis `analyze_v27.py` SHA256 `103c74551205591671efe90afdca54c900b6d89c0c7e7ce113699c3bcf31914a`.

Guardias: no main, no merge, no HTML, no ROOMS.exits, no A07, no canon; comercio y precios fuera del frente.
