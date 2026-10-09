# PRE-A08 V34 — Validación independiente de los monstruos LianQi II

**2026-10-09 · LAB PASS / V33 MODERADOS RESPALDADOS / NO CANON / SIN A08 FREEZE.**

## Alcance y guardia humana
Se parte de los seis perfiles originales del motor de laboratorio y los seis candidatos moderados V33 (sin aplicarlos a los originales). Se añade una tercera magnitud `ROLE_STRONG` **exclusivamente diagnóstica**, para descartar el fortalecimiento excesivo. **Sobretúnica de patrulla conserva DEF+2/HP+2**, tal como manda el principio de expectativa/progresión ratificado. No precios, economía, HTML, NPC, A07 ni `main`.

T0/T1/T2 identifican **tiers adaptativos**, no etapas de cultivo. Seis monstruos normales LianQi II, 5 raíces, 16 builds por raíz, EARLY/DELAYED_TRIGGER, equipo original M03 / M04 Sobretúnica / M05 dotación avanzada Sobretúnica / M05 dotación avanzada Sauces. Se usa una relación escalar BASE V17 representativa por raíz, no toda la red de Concordancias.

## Batería reproducible
- Discovery, semillas **111100–111101**: **69.120** duelos.
- Holdout, semillas **111500–111501**: **69.120** duelos.
- **138.240 duelos nuevos**, en **46.080 contextos pareados de tres versiones** de monstruo.
- COLD con semilla 111100: **34.560 filas × 32 columnas idénticas**, salvo etiqueta `cohort`; **no** se cuentan como duelos nuevos.
- **0 timeouts, 0 cadencias incumplidas**; equipamiento íntegro y habilidades Survival T1 originales restauradas.
- Paquete extraído en otra carpeta: CHECKS, reejecución COLD y análisis completo **PASS**.

## Victoria del jugador en T2 (n=3.840 por equipo y versión)
| Dotación | Monstruos originales | V33 moderado | Estrés fuerte |
|---|---:|---:|---:|
| Uniforme M03 | 67,73% | **60,36%** | 51,93% |
| **Sobretúnica DEF2** | 88,88% | **82,92%** | 75,68% |
| Avanzada + Sobretúnica | 96,46% | **94,30%** | 90,00% |
| Avanzada + Sauces | 87,68% | **83,18%** | 75,78% |

Cada mejora de equipamiento sigue siendo perceptible. En T2, bajo monstruos V33 moderados, de 3.840 contextos comparables, la Sobretúnica dio **893 victorias exclusivas** frente al uniforme inicial y el uniforme solo **27 victorias exclusivas** frente a ella. La dotación avanzada con Sobretúnica produjo **1.317 victorias exclusivas** respecto del uniforme frente a **14** en sentido contrario. No se debilita el equipo.

## Monstruos T2 contra uniforme M03 (n=640 cada versión)
| Especie | Original | Moderado V33 | Fuerte diagnóstico |
|---|---:|---:|---:|
| Araña de la Veta Sombría | 61,09% | **52,50%** | 42,03% |
| Cangrejo del Cauce Pétreo | 60,94% | **52,19%** | 46,09% |
| Jabalí de Pizarra | 70,78% | **59,84%** | 48,28% |
| Búho de la Niebla Gris | 67,97% | **63,12%** | 50,94% |
| Murciélago Resonante | 71,09% | **63,12%** | 57,50% |
| Zorro de los Bancales | 74,53% | **71,41%** | 66,72% |

En T0 con uniforme, el candidato moderado más difícil es la Araña, con **63,75%** victorias; el estrés fuerte da márgenes inferiores al 50% en T2 con uniforme contra Araña, Cangrejo y Jabalí. **No escalar más esos monstruos sin un nuevo contrato humano de dificultad**. No existe un umbral 50% ratificado; se usa únicamente como alerta diagnóstica.

## Valores moderados a mantener como candidatos (NO RATIFICADOS)
| Monstruo | Campo | Original | Moderado V33 | Fuerte de descarte |
|---|---|---|---|---|
| Jabalí de Pizarra | Embestida, daño especial | `1d3+6` | **`1d3+8`** | `1d3+10` |
| Búho de Niebla Gris | Picado, daño especial | `1d2+7` | **`1d2+8`** | `1d2+10` |
| Zorro de Bancales | Evasión | `19` | **`21`** | `23` |
| Cangrejo de Cauce | Pinza, daño especial | `1d2+7` | **`1d2+8`** | `1d2+9` |
| Murciélago Resonante | Pulso, daño especial | `1d2+5` | **`1d2+6`** | `1d2+7` |
| Araña de Veta Sombría | Vida base | `71` | **`75`** | `79` |

Se preservan todas las habilidades Survival T1, cadencias, aflicciones, drenajes Qi y otros campos. No aplicar viejos ajustes de reducción Cangrejo/Jabalí V19 simultáneamente sin comprobar compatibilidad.

## Advertencia focal
**Viento con uniforme y T2** mantiene el promedio más exigente: **55,86% original → 48,96% moderado**; con Sobretúnica pasa a **77,21%** y con dotación avanzada pesada a **91,41%**. El problema ya existía en parte con monstruos originales. No inferir automáticamente que todos los monstruos necesitan retroceder ni que la raíz Viento necesita un buff; hay que valorar técnicas y momento real de acceso en el frente correspondiente.

## Dictamen
**Recomendación:** sostener los seis V33 moderados como candidatos preferidos; descartar los seis extremos fuertes. **No hay aprobación de estadísticas canónicas ni pase definitivo a Astra.** V34 no mide AOE, aflicciones persistentes poscombate, Concordancias estructurales/condicionales completas, miniboss, T3/T4, Grulla ni paridad runtime. El equipo M05 es configuración hipotética, no prueba de adquisición efectiva; el comercio permanece totalmente fuera del alcance.

## Reproducción e integridad
Paquete: `GRULLA_PRE_A08_V34_VALIDACION_MONSTRUOS_Y_PROGRESION_2026-10-09.zip`, **56 entradas, 2.727.974 bytes**, SHA256 `c49ea86b9eb819348f547c53f3deaa50c60a8d5f9a31313bcef5a2f13488b558`. Manifiesto SHA256 y CRC PASS; **cold+analysis desde una carpeta recién extraída PASS**. Ejecutable `run_v34_monster_stage.py` SHA `36e6461eb8b100815a3395d9e951f0d46fda9eb0b5b675ad9491484ff2d48b39`; analizador `analyze_v34.py` SHA `9de2b556aa09cc82b9c10437432319147aba332420eed3f685e9757c67b2018d`. ZIP asociado a esta conversación, no subido a Git.

**Guardias:** ninguna edición a `main`, ni merge, `ROOMS.exits`, HTML, A07, tiendas, precios ni registro canónico. 
