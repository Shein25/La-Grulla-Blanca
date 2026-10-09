# La Grulla Blanca — V33: balancear monstruos, no debilitar equipo

**Fecha:** 2026-10-09. **Estado:** `LAB_PASS` / seis cambios NUMÉRICOS CANDIDATOS / **NO CANON / NO HTML / NO MAIN / SIN PRE-A08 FREEZE**.

## Decisión de prioridad

Se detiene la reiteración de pruebas de la Sobretúnica: **mantener como original y sin cambios `sobretunica_patrulla` DEF+2/HP+2**. El laboratorio vuelve a los seis monstruos normales LianQi II; su dificultad se ajusta desde sus propios perfiles y roles en vez de quitar poder al equipo del jugador.

## Candidatos concretos (solo LAB)

| Monstruo / rol | Parámetro de monstruo | Original | Candidato probado |
|---|---|---|---|
| Jabalí de Pizarra | `technique.params.direct_damage` | `1d3+6` | **`1d3+8`** |
| Búho de la Niebla Gris | `technique.params.direct_damage` | `1d2+7` | **`1d2+8`** |
| Zorro de los Bancales | `stats.evasion` | `19` | **`21`** |
| Cangrejo del Cauce Pétreo | `technique.params.direct_damage` | `1d2+7` | **`1d2+8`** |
| Murciélago Resonante | `technique.params.direct_damage` | `1d2+5` | **`1d2+6`** |
| Araña de la Veta Sombría | `stats.hp` | `71` | **`75`** |

Notas: Serpiente/Avispa no forman parte de los seis normales LII de este frente; Araña conserva veneno **idéntico** (solo HP). Murciélago conserva drenaje de Qi=6 (cambiarlo solo a 8–10 no había mostrado ventaja útil); se prueba daño directo del Pulso +1. Cangrejo abandona la propuesta de aumentar +2/+4 el daño especial, que castigaba demasiado a los recién llegados: su candidato ahora es **+1**. Los perfiles concretos originales permanecen inalterados.

## Matriz y pruebas ejecutadas

- **V33 exploratoria:** 69.120 DISCOVERY + 69.120 HOLDOUT = **138.240** duelos nuevos, original/moderado/fuerte para seis criaturas, cuatro equipos, T0/T1/T2, cinco raíces, 16 builds por raíz y dos políticas. Permite DESCARTAR propuestas excesivas o poco eficaces.
- **V33B focal:** 23.040 DISCOVERY + 23.040 HOLDOUT = **46.080** duelos nuevos para Cangrejo (+1/+2 daño) y Murciélago (+1/+2 daño directo), distinguiéndolos de las variantes V33 inadecuadas.
- **V33C finalista:** 46.080 DISCOVERY (110100–110101) + 46.080 HOLDOUT (110500–110501) = **92.160** duelos nuevos, **46.080 contextos pareados**; seis monstruos originales comparados con seis modificaciones moderadas elegidas por rol.
- **Totales V33 + V33B + V33C = 276.480 duelos nuevos**. No se incluyen 960 del piloto ni los Cold porque tienen naturaleza distinta.
- **COLD V33C:** 23.040 filas × 32 columnas reproducidas exactamente, comparadas con semilla 110100 de DISCOVERY. No se suman a nuevos combates.
- **QA:** timeouts=0, cadencias incumplidas=0, mismo seed por brazo, equipo original restaurado, habilidades originales T1 restauradas y modificaciones solo sobre perfiles temporales.

## Resultados T2, equipamiento inicial M03 (n=640 pares por especie)

| Monstruo | Original | Candidato | Δ jugador |
|---|---:|---:|---:|
| Jabalí de Pizarra | 76.09% | 64.84% | -11.25 pp |
| Búho de la Niebla Gris | 66.72% | 60.16% | -6.56 pp |
| Zorro de los Bancales | 76.25% | 72.03% | -4.22 pp |
| Cangrejo del Cauce Pétreo | 64.84% | 55.00% | -9.84 pp |
| Murciélago Resonante | 73.75% | 67.81% | -5.94 pp |
| Araña de la Veta Sombría | 67.03% | 58.59% | -8.44 pp |

**Gate de progresión:** el uniforme inicial sigue permitiendo victorias en todos los enfrentamientos; el Cangrejo y la Araña exigen mayor atención (aprox. 55% y 59% de victoria en el brazo elegido) sin convertirlos automáticamente en el mismo enemigo.

## Resultados T2, Sobretúnica DEF+2 sin alterar (n=640 pares por especie)

| Monstruo | Original | Candidato | Δ jugador |
|---|---:|---:|---:|
| Jabalí de Pizarra | 92.97% | 87.19% | -5.78 pp |
| Búho de la Niebla Gris | 83.59% | 78.91% | -4.69 pp |
| Zorro de los Bancales | 93.75% | 92.03% | -1.72 pp |
| Cangrejo del Cauce Pétreo | 95.16% | 91.25% | -3.91 pp |
| Murciélago Resonante | 91.72% | 87.66% | -4.06 pp |
| Araña de la Veta Sombría | 80.47% | 73.28% | -7.19 pp |

## Resultados T2, dotación avanzada M05 + Sobretúnica original

| Monstruo | Original | Candidato | Δ jugador |
|---|---:|---:|---:|
| Jabalí de Pizarra | 98.91% | 96.25% | -2.66 pp |
| Búho de la Niebla Gris | 92.34% | 89.38% | -2.97 pp |
| Zorro de los Bancales | 98.28% | 97.34% | -0.94 pp |
| Cangrejo del Cauce Pétreo | 99.84% | 99.53% | -0.31 pp |
| Murciélago Resonante | 97.19% | 96.25% | -0.94 pp |
| Araña de la Veta Sombría | 92.50% | 87.97% | -4.53 pp |

## Verificación progresión y resiliencia

Ganancia de jugador media T2 por equipo ante seis especies:

| Equipo real de referencia | Original | Candidatos | Cambio |
|---|---:|---:|---:|
| Uniforme inicial | 70.78% | **63.07%** | -7.71 pp |
| Sobretúnica DEF+2 | 89.61% | **85.05%** | -4.56 pp |
| Avanzado+Sobretúnica | 96.51% | **94.45%** | -2.06 pp |
| Avanzado+Sauces | 88.10% | **83.36%** | -4.74 pp |

La Sobretúnica mantiene un **premio importante de supervivencia** respecto del uniforme sin reducirse su DEF. El equipo avanzado sigue ganando más que el intermedio. En términos de expectativa del jugador, el cambio aumenta el desafío contra monstruos de nivel apropiado sin borrar lo ganado al equiparse.

## Conclusiones y límites

1. **Seis cambios concretos disponibles como candidatos**, uno por monstruo, en `CANDIDATOS_BALANCE_MONSTRUOS_V33.json`. Mantener originales como control hasta ratificación humana. No se envía a Astra como cambio canónico sin aprobación.
2. **No aplicar variantes fuertes de forma general**. En las baterías exploratorias hicieron caer en exceso la tasa de victoria del jugador con equipo inicial, especialmente ante Cangrejo.
3. **No tocar todavía** la potencia del veneno de la Araña, la regla de aflicciones persistentes, estadísticas de equipo, técnicas del jugador ni precios. El veneno del jugador −10% recuperación de Qi extracomabte (V30) sigue aceptado en diseño y no intervenido.
4. La inclusión de una sola Concordancia BASE escalar V17 representativa por raíz es un **límite real** del modelo: faltan consumidores condicionales/estructurales, secuencias con persistencia, élites, minibosses, 2+ enemigos y AOE. No extrapolar resultados de criaturas normales a jefes.
5. Los altos porcentajes con equipo avanzado contra criaturas normales NO implican nerfear el equipo: son consistentes con progresión. La dificultad tardía debe venir de enemigos apropiados de esa etapa, no de homogeneizar las recompensas.
6. El alcance permanece en LAB en la rama `experiment/lii-tramo1-multirraiz-v08-2026-10-08`; no se modificaron `main`, HTML, A07, `ROOMS.exits`, los registros de monstruos originales, catálogo de equipo ni comercio.

## Archivos auditables

- Runner de conjunto final `run_v33_final_candidates.py`.
- Pruebas exploratorias `run_v33_monsters.py` y corrección focal `run_v33_focal_crab_bat.py`.
- `RAW_V33C_{DISCOVERY,HOLDOUT,COLD}.csv.gz`, `PAIRED_FINAL_V33C.csv.gz`, tablas por cohorte, monstruo, tier, raíz y equipo; QA individuales y auditoría COLD.
- ZIP externo reproducible con dependencias LII V20/V17, manifiesto SHA256 y CRC. El ZIP se entrega aparte; Git contiene el dictamen y el contrato de candidatos.