# Dictamen V77 — AOE × Concordancias (tres combinaciones pedidas)

**2026-10-10 — primera batería estructural y de daño E1, NO balance definitivo ni simulador HTML.**

## Cierre de balance anterior
El autor ordenó guardar la versión intermedia **Sentencia de Metal V76 B** (65% apertura, 65% remate, +10pp penetración adicional, hemorragia una carga potencia2 × dos acciones, 16 Qi) como autoridad de diseño vigente. **Sombra Ahogada** se cierra como **élite único LIII**, ficha de diseño **V72: HP110 / DEF1 / Velo CD4 y veneno ×2 / Espejo8**. Se conservaron como históricos Metal V67 y T0 Sombra HP51; no hay HTML modificado, merge ni escritura a `main`. No confundir Sombra con los cinco guardianes AOE.

## Primera prueba realmente ejecutada
Runner nuevo `v77_concordance_aoe.py` reutiliza `resolve_player_direct` **sin alterar la física E1** y distribuye una acción entre un conjunto de 1/2/3 blancos hostiles **sintéticos**, descontando una sola vez Qi. Se simulan **dos acciones consecutivas sin turnos de monstruo intermedios**; calcula daño directo E1 y apunta un evento de **hook base seleccionable**, pero **NO implementa el bono numérico/manifestación de Concordancia** (no autorizado ni disponible en E1).

Se ejecutaron **19.200 secuencias** ×2 acciones = **38.400 ejecuciones**, con las cinco raíces:

| Secuencia | Secuencias | Pares raíz diferentes con un hook BASE |
|---|---:|---|
| AOE(A) → AOE(B), A≠B | 7.680 | **14/20** |
| AOE(A) → UNITARGET(B), A≠B | 7.680 | **16/20** |
| AOE(A) → la misma AOE(A) | 1.920 | **0/5**, por identidad de raíz |
| AOE(A) → UNITARGET(A) | 1.920 | **0/5** |

Los **6 BASE NONE** de AOE→AOE pueden abrir recepción por Tramo I/II: Metal→Círculo Fuego vía DOT, Agua→Lluvia Metal vía precisión de Eficiencia, Metal→Marea Agua vía precisión, Viento→Marea Agua vía precisión, Fuego→Tijera Viento vía crítico de daño I+II y Metal→Tijera Viento vía precisión de Circulación. **6/6** confirmados por compilación de rutas en la fuente E1, con ≤2 PT en técnica receptora, sin Tramo III LIV. No se ha verificado adquisición de esos manuales extranjeros ni magnitud final de la Concordancia.

**Medias de daño directo E1 de la SEGUNDA acción (sin mejoras de Concordancia aplicadas):**

| Patrón | Un hostil | Dos hostiles | Tres hostiles | Qi medio de esa acción |
|---|---:|---:|---:|---:|
| AOE de otra raíz | 3,26 | 10,80 | 16,01 | 8,8 |
| Unitarget de otra raíz | 8,02 | 8,10 | 8,09 | 6 |
| Repetir la misma AOE | 3,36 | 10,87 | 15,99 | 8,8 |

AOE: **un blanco daño directo ×0,65 antes de DEF; 2+ ×1 por blanco**, sin repartición de daño y Qi por acción, NO por blanco. Media Qi 8,8 por cuatro raíces 9 y Agua 8 en compilación E1 sin especialización. Cada técnica válida crea/reemplaza un Eco de su propio elemento; cuando no hay hook compatible, no se inventa bonificación por Concordancia, pero se reemplaza el Eco al ejecutar válidamente la receptora. Si repite la misma AOE, paga un segundo coste real y NO genera Concordancia A→A.

## QA y límites de interpretación

**600/600 regresiones EXACTAS** contra `execute_player_technique` E1 1v1 en HP, Qi, impactos, críticos, DOT y debuffs. **15/15** rechazos sin manual y **5/5** sin Qi preservaron estado; **5/5** casos de matar un objetivo de dos y volver a disparar AOE recontaron 1 blanco y usaron ×0,65. Sin diferencias; ZIP extraído aislado, scripts corridos de nuevo y CSV reproducidos byte a byte.

**Muy importante:** NO se calcularon tasas de victoria o bonus de Concordancia. La selección de hooks no garantiza su activación si requiere impacto/estado; tampoco ejecuta transformaciones estructurales por objetivo. El motor V66 original solo da 1v1; V77 hace bucle de blanco como primer adaptador sintético, sin turnos enemigos, condiciones de salas reales, manuales ganados, builds completas 4PT/equipo real, adquisición, DoT evolutivo, adaptaciones o paridad NEW/HTML. En especial, las AOE ajenas se marcaron **fixture hipotético** y los blancos no representan un spawn autorizado.

**Archivo reproducible:** `GRULLA_V77_AOE_CONCORDANCIAS_TRES_COMBINACIONES_2026-10-10.zip`, SHA256 `aad31df3f8d4cf96eb4d606a1018102f2b3f6461e005726f13fee4428be62059`, **922.790 bytes / 16 archivos**; motor V66 original sellado adentro, runner, matriz CSV completa, resumen, prueba de 6 hooks condicionales, manifiesto SHA256, QA, informe. CRC/manifiesto PASS y ejecución desde extracción aislada PASS. ZIP adjunto a conversación, no subido a Git.

## Siguiente gate para porcentajes reales
Paridad con motor multiblanco NEW/HTML y resolver del contrato de **20 Concordancias dirigidas**, aplicar porcentajes acordados sobre hooks propios y manifestaciones estructurales por `ActionContext` una vez; confirmar aprendizaje LEGAL de AOE extranjera y puertas PRE/POST_MANUAL; correr combates completos LIII (raíces, tres builds de cuatro PT, equipamiento adquirido, IA enemiga, DOT, 1/2/3 hostiles reales verificables), comparar OFF/ON con seeds pareadas. **No tocar `main`, merge, HTML, `ROOMS.exits`, guardianes, balance del élite ni V76 en esta etapa.**
