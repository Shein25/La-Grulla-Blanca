# Decisión de diseño — Sentencia del Filo Celestial: cierre numérico V76

**Fecha:** 2026-10-10.
**Decisión:** tras revisar el problema del nerf V67, el usuario preguntó «Entonces qué opinas? ¿Dejamos ese balance intermedio?» y el asistente recomendó afirmativamente **conservar el punto intermedio V76 B**. Se registra esta aceptación conversacional como **selección de la ficha de diseño para continuar**, sin pretender que la pregunta por sí sola autorice modificación del HTML o merge. Esta es la autoridad numérica seleccionada hasta otra orden humana expresa.

## Ficha seleccionada: `METAL_CANDIDATE_V76_MID_B`

- Raíz **Metal**, Ulti principal `METAL_SENTENCIA_FILO_CELESTIAL`, LianQi III con dominio completo.
- Apertura: **65%** del daño directo original; **+30 precisión** original conservada.
- Penetración **adicional** de la Ulti: **+10 puntos porcentuales**; NO eliminar ni sustituir la penetración habitual del personaje.
- Hemorragia: **1 carga**, potencia **2**, durante **2 activaciones de acciones voluntarias**, solo si golpe impacta vida real; atraviesa DEF pero respeta absorción/inmunidad correspondiente.
- **Punto de Ruptura:** se conserva requisito de 2 activaciones reales de hemorragia y siguiente ataque Metal enlazado; daño **65%** de `14–20 + 4 × cargas restantes`, sin crítico ni nueva tirada de evasión.
- **Coste 16 Qi**; **máximo una Ulti por combate**, como antes.
- **El jugador decide cuándo lanzarla**. La ronda 4 fue solo una política favorable *de laboratorio*, **no** imponer ronda 4 en motor, ni prohibir primera ronda.
- Sin alteraciones de las técnicas normales de Metal, la Ulti de Viento `SOFT_W01`, los demás elementos, enemigos, equipo o progresión.

## Por qué elegir V76 B y no volver a V03.1

Contra Sombra Ahogada V72 (110HP): con SOFT_M02 en ronda 4, **43,43%** de victorias; con V76 B en ronda 4, **54,83%**. Contra Rey Escarabajo: **72,92%** vs **83,56%**. Otros guardianes V76 B, ronda 4: Sapo **69,33%**, Mantis **77,86%**, Coral **39,67%**, Custodio **40,48%**. Nada de 99–100% de la antigua versión original en los escenarios estudiados y **cero caídas de guardianes antes de ronda 4** bajo esa política.

Las comparaciones son **1v1 PRE_AOE** sobre el adaptador E1/V03.1/V67, no paridad HTML ni test de las 25 Ultis. Tres equipos, 4 PT de LIII y gate de Ulti asumido por fixture, no concedido como recompensa automática. Inmunidad al sangrado de Coral/Custodio y números del Custodio siguen siendo hipótesis de laboratorio que afectan a sus tasas; no elevar esos aspectos a canónicos.

## Autoridad / límites de la ratificación

- **V76 B pasa a ser la ficha numérica seleccionada para Metal**, supersediendo **solo esa Ulti** respecto de la especificación V67 aprobada históricamente. Preservar V67 como documento histórico y referencia de regresión, **NO sobrescribirlo**.
- **Viento V67 SOFT_W01 permanece intacta**.
- **Cierre de balance de laboratorio y diseño únicamente.** No es afirmación de que la Ulti haya sido implementada, ni marca `READY` del HTML. La integración requiere autorización y paridad REAL de Qi, DOT, absorción, enlace y remate.
- **NO MAIN**, no merge, no HTML, no `ROOMS.exits`, no misión/spawns/guardianes afectados.
- Fuentes: [dictamen V76](DICTAMEN_V76_METAL_PUNTO_INTERMEDIO.md), [candidato previo](METAL_SENTENCIA_V76_CANDIDATO_NO_APROBADO.json). ZIP portable V76 SHA-256 `6d0891daf20dedda7ff2d387d748435b03d27baa79ef7b07c8a61706422ab15c` disponible en conversación.
