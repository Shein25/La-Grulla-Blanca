# PROMPT PARA CONTINUAR — V67 GUARDIANES AOE CON ULTIS

Continúa mi proyecto MUD **La Grulla Blanca**, repositorio **Shein25/La-Grulla-Blanca**, desde la batería V66 final de guardianes AOE. **NO reinicies la investigación desde cero ni repitas las simulaciones cerradas.**

## Fuente de restauración obligatoria
- Rama de handoff/backup Git: \`handoff/v66-guardianes-aoe-2026-10-10\`.
- Leer primero: \`experimentos/balance_nuevo/handoffs/V66_GUARDIANES_AOE_2026-10-10/HANDOFF_V66_COMPLETO_2026-10-10.md\`.
- Decisión humana: \`experimentos/balance_nuevo/adaptive_six_revalidation_v0.1/DECISION_HUMANA_GUARDIANES_AOE_IDENTIDADES_UBICACIONES_2026-10-07.md\`.
- Los cuatro T0 históricos ratificados se encuentran en el commit \`45c3a9c240ea74208a0d8fd4d5be187bc817df35\`; Custodio de Tierra todavía no tiene T0 ni spawn ratificados.
- Backup portable V66: \`GRULLA_V66_GUARDIANES_AOE_DESGLOSE_5_RAICES_2026-10-10.zip\`, SHA-256 \`e8402ca195ba9f2d4fe97ae4a71351d25f691c7601a81c49693cdf77198d3a39\`. Si no está adjunto al chat, pedí ese ZIP antes de afirmar haber auditado los CSV o ejecutar sobre fuentes reproducibles.

## Estado real
- V66 completo: **63.000 combates nuevos**, 36.000 control/candidato más 27.000 sensibilidad, sin Ultis ni Concordancias extranjeras, 0 fallos reportados.
- LianQi III **PRE_AOE**, 4 puntos legales; 5 raíces × 5 guardianes, 3 builds × 2 equipos × 3 políticas. Matriz sin Ulti en el handoff; 720 combates por celda.
- Guardianes **correctos**: Sapo/Fuego, Rey Escarabajo/Metal, Guardián de Coral/Agua, Mantis de Nube/Viento, Custodio del Eco Pétreo/Tierra. **El Centinela de plumas NO es un guardián AOE.**
- Son únicos, sin respawn, manual AOE por victoria una sola vez; aparecen legalmente desde LIII aun si algunas habitaciones están en zonas LII. No tienen fases obligatorias: kits continuos y telegráficos.
- V65 es candidato de ajustes de 5 guardianes, NO ratificación; cuatro T0 previos son autoridad. Custodio no tiene ficha ni spawn canónico.

## Lo que sigue: V67
**Objetivo principal:** conectar el ejecutor REAL y autorizado de las **25 Ultis** (V03.1 y decisiones humanas) a los combates completos de guardianes y ejecutar pruebas pareadas \`NO_ULTI\` vs \`MAIN_ROOT_ULTI_READY\` con semillas iguales, gastando realmente acciones, Qi y demás recursos. Primero auditá la conexión y sus fuentes; **no inventes el daño de las Ultis**.

En LIII puede usarse la Ulti de la raíz principal si la rama está \`APRENDIDA_AL_MAXIMO\`, independientemente de cuántos nodos haya activos en la tercera familia; como máximo una activación de Ulti por combate. La Ulti del injerto se habilita en LIV: **no incluirla en LIII**. Sin acceso legal, el combate queda en brazo NO_ULTI; no regalar la habilidad.

Separar por **cada uno de los cinco jefes y cada raíz**: victoria, TTK de victoria (mediana y percentiles), derrota del guardián en <=3 acciones (prohibir trivialización), turnos de ejecución de Ulti, fallos por Qi o disponibilidad, daño efectivamente aportado, HP/Qi final, telegráficos aprovechados, Fisura/Lectura/Resonancia/Calor. Medir equipos y builds por separado y evitar agregados que oculten problemas.

**Problemas focales según V66:** Agua→Coral solo 19,7% (mediana 14 turnos); Tierra→Custodio 31,1% (13 turnos); Fuego→Rey demasiado fácil 83,2%; Sapo/Mantis son candidatos razonables. No corregir Coral bajando solo 2 Qi de drenaje, no regalar una DEF menor al Custodio sin medir Fuego, no añadir +1 DEF permanente a Rey. Buscar contrajuego propio y recompensar preparación; con Ulti estudiar si hay muertes de jefe <=3 acciones.

**AOE:** previo al guardián, el jugador NO posee la técnica AOE del manual. Posterior: x0,65 contra UN enemigo hostil de cualquier categoría, x1 por objetivo si >=2; una acción/un coste Qi, impactos independientes, sin límite de objetivos ni acompañantes inventados. No mezclar PRE_AOE con POST_AOE.

## Restricciones duras
NO tocar main, no merge, no HTML ni ROOMS.exits, no pushes productivos, no editar T0 ratificados, spawns, NPC, economía, A07, manuales o gates sin aprobación humana. No inventar nuevos jefes, zonas, estados ni técnicas. No aplicar T1–T4 persistente de especies repetibles a jefes únicos.

Primero presentame auditoría de fuentes y viabilidad del puente de Ultis, luego ejecutá el test V67 o construí Colab reproducible si requiere cómputo intenso. Entregá resultados por raíz y jefe, SHA-256, runner y un dictamen sobre qué candidatos de kits mantener, cambiar o dejar bloqueados.
