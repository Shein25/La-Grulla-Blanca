# PRE-A08 V31 — Cruce focal de balance puro
**2026-10-09 · LAB PASS / NO CANON / NO RUNTIME / NO FREEZE.**
Se continúa V30 sin reabrir economía, comercio, NPCs ni precios.

## Experimento
Monstruos normales **Cangrejo de Cauce** y **Jabalí de Pizarra**, habilidades V19 originales versus candidatos (Cangrejo DEFENSE_UP +3→+2; Jabalí MITIGATE_NEXT 40%→35%). Raíces **Agua/Tierra (Embalse)** y **Metal/Tierra (Placa Fundacional)**, Concordancia estructural OFF/ON. Dotaciones M03, Sobretúnica de patrulla DEF+2/HP+2 actual, o DEF+1/HP+2 candidata; tiers T1/T2, 16 builds por raíz y dos políticas. Recurso aislado: 7 Qi previos más recuperación hipotética de 20 Qi (27) versus aplicar el −10% de Veneno V30 sobre esa recuperación (25). **Esto no inyecta una aflicción ni un DOT, y 20 Qi no es un valor ratificado de medicina o meditación.**

DISCOVERY 106100–106103: **24.576 duelos**. HOLDOUT 106500–106503: **24.576 duelos**. Total **49.152 duelos nuevos**, 6.144 contextos con 8 brazos pareados (equipo fijo). COLD 106100: **6.144 filas × 32 columnas exactas**, no contadas como combates nuevos. **0 timeouts / 0 acciones debidas omitidas**, semillas equivalentes entre brazos, definición canónica de DEF y habilidades originales de ambos monstruos restauradas tras la prueba.

## T2: monstruos originales, estructura OFF y Qi 27
| Equipo | Victorias (n=1024 por grupo) |
|---|---:|
| M03 | 32,23% |
| Sobretúnica DEF+1/HP+2 | 37,11% |
| Sobretúnica DEF+2/HP+2 | **84,38%** |

Incremento DEF1→DEF2 de **47,27 pp** a causa del breakpoint de defensa plana en este escenario de Qi inicial limitado. **No comparar directamente tasas absolutas con V23–V24**, que usaron otra reserva de Qi.

## Concordancias estructurales T2: monstruos originales, Qi 27
| Situación | OFF | ON | Diferencia |
|---|---:|---:|---:|
| Agua, Sobretúnica DEF+1 | 37,50% | 37,50% | 0,00 pp |
| Metal, Sobretúnica DEF+1 | 36,72% | 43,16% | **+6,45 pp** |
| Metal, Sobretúnica DEF+2 | 86,72% | 88,09% | +1,37 pp |
| Metal, M03 | 31,84% | 36,91% | +5,08 pp |

Embalse sigue activándose y liberando absorción (p.ej. 472 resoluciones y 106,2458 unidades de reserva liberada para Agua/DEF1), pero **sin cambios de victoria** en estos contextos. Necesita auditoría del consumo útil y del orden de impactos antes de tocar sus números. Placa Fundacional sí beneficia a las construcciones sin la defensa plana dominante.

## Candidatos V19 en T2 y Sobretúnica DEF+1
Promedio de Agua+Metal, estructura ON/OFF y Qi 27/25:
| Monstruo | Original | Propuesta | Δ victorias jugador |
|---|---:|---:|---:|
| Cangrejo | 29,59% | 34,28% | +4,69 pp |
| Jabalí | 44,92% | 49,12% | +4,20 pp |

**No ratifica los nerfs**. Mantener ambos monstruos originales como control por ahora.

## Sensibilidad de Qi V30 (T2, DEF1, monstruos originales, estructura ON)
| Raíz | Qi 27 | Qi 25 | Δ |
|---|---:|---:|---:|
| Agua | 37,50% | 31,64% | −5,86 pp |
| Metal | 43,16% | 43,16% | 0,00 pp |

El umbral de recursos afecta algunas rotaciones, pero esto **NO mide el impacto real de veneno en una expedición**. V27–V30 cubren específicamente aflicciones y tratamiento. El diseño aprobado del veneno es −10% de recuperación Qi **solo fuera del combate**; no agregar costes de Qi adicionales.

## Dictamen
1. **Sobretúnica DEF+1/HP+2** continúa siendo el candidato numérico preferido, pero **NO está ratificado ni aplicado**.
2. Placa Fundacional: conservar provisionalmente. Embalse: auditar eficacia física real antes de aumentar escala.
3. Cangrejo/Jabalí: conservar originales hasta decidir objetivos de dificultad y aprobar cambios, sin acumular nerfs prematuramente.
4. La mecánica Veneno −10% recuperación Qi fuera de combate ya fue elegida por el usuario; la semántica de fuente/redondeo V30 es propuesta de integración. **No se alteran estadísticas de medicina ni combate**.
5. Concordancias condicionales V26, Embalse y consumidores A08 productivos **aún requieren cierre**. No declarar freeze PRE-A08 ni dar vía libre a Astra B01.

## Reproducibilidad
Paquete completo independiente de Git: `GRULLA_PRE_A08_V31_BALANCE_CRUCE_DEFENSA_MONSTRUOS_Y_QI_2026-10-09.zip`; SHA-256 `1724472e0de19ab5f23d62c6ed5a56797d02fa19db01b691800d6c54f5906b59`, 114 archivos, CRC y manifiesto PASS. Runner `run_v31_factorial.py` SHA-256 `4a5c71a6c9404c89aa5ee60e29f5f243639c701baeb1cda5067a7856ef531727`, analizador `analyze_v31.py` SHA-256 `309b05ab142f55171eeaae3c7efcad18478d751f9d2f23c8f21f4b8a1dde5541`. Ejecutada de nuevo desde ZIP descomprimido en carpeta independiente: **COLD y análisis PASS / 6.144 filas exactas**. ZIP adjunto en conversación, no subido a Git.

Guardias: sin `main`, merge, cambios HTML, `ROOMS.exits`, A07, NPC, economía, precios, nuevos monstruos, reescritura de contratos ni modificaciones de registros canónicos.
