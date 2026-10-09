# La Grulla Blanca — V18 · Diagnóstico de seis monstruos LII y microbalance de reacción T1

**Fecha:** 2026-10-09. **Estado: PASS DE LABORATORIO / NO CONGELADO / NO RUNTIME**.
**Fuente de habilidades:** perfil experimental V17 PRE-A08 fijo. **Fuente de fauna:** seis criaturas LII NATURAL no mutantes del adaptador V07. **Concordancias:** OFF en esta batería; los resultados anteriores V17 ON/OFF sirven de referencia, NO están sumados a estos resultados. Sin pociones, sin costes oficiales de técnicas ajenas, sin multitud y sin élites.

## Qué se probó aquí, sin necesidad de Colab

**Diagnóstico V18 A:** 138.240 combates completos en dos campañas independientes de 69.120; semillas 71000–71003 y 72000–72003. Factores: seis especies × cinco raíces × 16 builds monorraíz legales × T0/T1/T2 × cuatro kits × tres políticas × ocho semillas en total. Kits: PRE_M03, POST_M03, CARRY_OVER_LI_HIGH (**estrés, adquisición no certificada**) y EXPECTED_STAGE (**candidato de etapa, acceso no certificado**). Políticas: OFFENSE_ONLY, DEFENSE_REFRESH y QI_RESERVE_BASIC. Cada trío T0/T1/T2 conserva la misma semilla y sus condiciones dentro del juego (si divergen acciones/RNG, no equivale a mismas tiradas posteriores).

**Microbalance V18 B:** 61.440 combates en dos campañas independientes de 30.720, semillas 73000–73003 y 74000–74003. Cuatro hipótesis T1 ensayadas contra ORIGINAL con la misma semilla, sin tocar el archivo nativo ni las estadísticas T0: Cangrejo DEFENSE_UP +3→+2; Jabalí MITIGATE_NEXT 40%→35%; Zorro MITIGATE_NEXT 25%→30%; Araña MITIGATE_NEXT 35%→30%. Cinco raíces, 16 builds, T1/T2, PRE_M03/POST_M03/EXPECTED_STAGE y dos políticas OFFENSE_ONLY/DEFENSE_REFRESH. **No se aprueban estos cuatro candidatos automáticamente.**

**Total V18:** **199.680 combates nuevos**. T0 sin adaptación, T1 sin anticipación; T2 sí reconoce categorías según contrato. QA completa: **0 timeouts y 0 técnicas canónicas debidas omitidas**. Ninguna estadística de monstruo se escribió al registro ni al HTML.

## Dificultad observada con POST_M03 en T2

| Criatura | WR del jugador V18 A, todas las raíces/builds/tres políticas |
|---|---:|
| Zorro de Bancales | 69,22% |
| Murciélago Resonante | 62,92% |
| Jabalí de Pizarra | 61,04% |
| Búho de Niebla Gris | 61,77% |
| Araña de Veta Sombría | 58,23% |
| Cangrejo de Cauce | 55,42% |

NOTA: la muestra V17 anterior incluía dos políticas y dio porcentajes diferentes; no confundir ese total con el de V18 (tres políticas, incluyendo QI_RESERVE_BASIC). Se conservaron pesos iguales para builds, raíces y políticas; no se afirma que reflejen distribución real de jugadores.

## Brechas de equipo (T2)

| Criatura | PRE_M03 | POST_M03 | CARRY_OVER_LI_HIGH | EXPECTED_STAGE | Salto esperado frente a POST_M03 |
|---|---:|---:|---:|---:|---:|
| Araña | 59,17% | 58,23% | 62,92% | 91,25% | +33,02 pp |
| Búho | 54,84% | 61,77% | 61,98% | 92,34% | +30,57 pp |
| Cangrejo | 54,48% | 55,42% | 60,73% | 99,48% | **+44,06 pp** |
| Jabalí | 58,28% | 61,04% | 65,21% | 95,99% | +34,95 pp |
| Murciélago | 59,84% | 62,92% | 67,92% | 95,99% | +33,07 pp |
| Zorro | 63,85% | 69,22% | 72,08% | 95,36% | +26,15 pp |

**No son diferencias causales pareadas de equipo**, ya que el generador de semilla varía según kit. Son comparaciones de cohortes equilibradas por raíz/build/política. Este salto sugiere priorizar la auditoría de disponibilidad y potencia del equipamiento antes de inflar estadísticas de los monstruos.

## Brechas por raíz (T2, POST_M03)

| Criatura | Agua | Fuego | Metal | Tierra | Viento | Diferencia máx−mín |
|---|---:|---:|---:|---:|---:|---:|
| Araña | 71,88% | 69,01% | 41,41% | 54,17% | 54,69% | 30,47 pp |
| Búho | 69,27% | 67,71% | 58,85% | 63,02% | 50,00% | 19,27 pp |
| Cangrejo | 51,56% | 72,92% | 55,73% | 50,52% | 46,35% | 26,56 pp |
| Jabalí | 76,04% | 70,05% | 48,18% | 61,46% | 49,48% | 27,86 pp |
| Murciélago | 68,49% | 62,24% | 60,16% | 68,75% | 54,95% | 13,80 pp |
| Zorro | 79,69% | 70,57% | 65,89% | 73,70% | 56,25% | 23,44 pp |

Las diferencias no justifican un bono por raíz del monstruo: debe conservarse neutralidad elemental ×1,0 y distinguir disponibilidad de técnicas/Concordancias, tácticas y equipo.

## Tiers adaptativos

Las reacciones T1 y T2 sí influyen. Media global por especie de diferencia de WR T1−T0 y T2−T1 (todas las raíces/equipos/políticas): Araña −6,84/−3,23 pp; Búho −6,60/−2,34; Cangrejo −8,79/−2,36; Jabalí −9,02/−5,29; Murciélago −5,95/−2,43; Zorro −5,08/−3,24. Sin alertas de T0 adaptativo ni anticipación T1; se registraron 35.406 anticipaciones T2 en 138.240 peleas.

## Política de combate y roles

En T2 POST_M03, la política DEFENSE_REFRESH frente a OFFENSE_ONLY mejora Búho (+17,5 pp), Cangrejo (+12,0), Jabalí (+12,5), Murciélago (+16,6), Zorro (+19,5). En Araña, DEFENSE_REFRESH **pierde** frente a OFFENSE_ONLY (57,97 vs 61,09%) por la interacción con veneno/DoT que atraviesa defensa. Es una diferencia de rol valiosa, no necesariamente un bug.

Murciélago drena en promedio 8,14 Qi con defensa refrescada, 8,62 sin ella y 10,79 con QI_RESERVE_BASIC, en T2 POST_M03; no eliminar su identidad. La disponibilidad y uso de consumibles/alquimia está fuera de la simulación y será necesaria antes de congelar Araña.

## Resultado del microbalance T1/T2 focal (T2 POST_M03)

| Criatura | Hipótesis T1 | WR jugador ORIGINAL | WR con hipótesis | Delta | IC95 exploratorio por ocho semillas |
|---|---|---:|---:|---:|---:|
| Cangrejo | DEFENSE_UP +3→+2 | 59,92% | 66,64% | **+6,72 pp** | +5,51 a +7,93 pp |
| Jabalí | MITIGATE_NEXT 40→35% | 65,23% | 68,52% | **+3,28 pp** | +1,98 a +4,58 pp |
| Zorro | MITIGATE_NEXT 25→30% | 73,67% | 70,78% | **−2,89 pp** | −4,04 a −1,74 pp |
| Araña | MITIGATE_NEXT 35→30% | 62,34% | 63,59% | +1,25 pp | +0,20 a +2,30 pp |

El orden de filas NO es ranking aprobado ni objetivo de convergencia. La muestra micro excluye QI_RESERVE_BASIC y CARRY_OVER_LI_HIGH, por eso sus porcentajes difieren de la pantalla global. IC95 basado en medias de 8 semillas como clusters, no en miles de peleas independientes; es solo evidencia comparativa.

**Recomendación de diseño para la siguiente iteración:**
- Cangrejo +3→+2 es el candidato más consistente sin cambiar su defensa básica (DEF2), Pinza ni perfil defensivo. Aun así, la brecha elemental queda grande: 28,1→25,4 pp en el microtest.
- Jabalí 40→35% es candidato secundario para suavizar presión T1/T2 sin tocar Embestida.
- Zorro 25→30% es un candidato opcional si se decide igualar acceso/dificultad; no nerfear por promedios sin fijar primero la distribución de equipo y tácticas.
- Araña 35→30% aporta escasa compensación; **preservar** y testear veneno, mitigación real por consumible/antídoto y aflicción entre combates.
- Búho y Murciélago: **sin cambios propuestos** en V18.

No congelo los seis monstruos: faltan Concordancias V17 ON más estructuras/condicionales físicamente completos, equipo accesible real por misión y política de consumibles. En particular, **no inflar HP/dificultad del Cangrejo** para contrarrestar un loadout EXPECTED_STAGE cuya disponibilidad no se ha demostrado.

## Siguiente gate pre-A08

Elegir candidatos T1 focales por decisión humana o comparar en un microgate de robustez con combinación de técnicas/Concordancias BASE V17. Completar kit de equipo progresivo realmente obtenible, diferenciar equipamiento potencial versus adquisición canónica, y verificar supervivencia/muerte/cadencia por especie. Solo si el espacio crece a millones, llevar esa campaña a Colab/Kaggle con checkpoints y compresión. **A08 a Astra después del cierre de habilidades, seis monstruos, equipo y economía.**