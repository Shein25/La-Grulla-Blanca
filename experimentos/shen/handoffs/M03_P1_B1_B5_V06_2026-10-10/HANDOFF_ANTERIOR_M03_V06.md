# LA GRULLA BLANCA — HANDOFF AUTORIZACIÓN EXPERIMENTAL

Fecha: 2026-10-09
Base: `grulla-blanca_ver76_A07_9_G03_B1_B5_CANDIDATE.html`
UI de referencia: `GRULLA_UI_DEFENSIVAS_LIANQI_II_V06_TERMINAL_UNICA.html`
Repositorio: https://github.com/Shein25/La-Grulla-Blanca

## Autoridad humana recién ratificada

1. Las **cinco defensivas básicas NEW** se enseñan únicamente desde **Lianqi II auténtico**.
2. El usuario autoriza **Shen Baojun como NPC oferente de las cinco defensivas básicas** dentro de su conversación auténtica, sin cambiar la autoridad social de A07.
3. Las cinco ofertas se abren **simultáneamente**, en **orden enteramente libre** y sin prioridad de la raíz propia.
4. **Antes de Lianqi II: ninguna mención** en el diálogo de Shen a este servicio, a las cinco defensivas, a un futuro desbloqueo, a opciones bloqueadas ni a «vuelve en II». La práctica previa de M03 puede mencionarse sólo como ejercicio básico de postura/respiración/instrucción, sin nombres de defensivas.
5. La opción **«Estudiar defensivas básicas» sólo existe mientras quede al menos una NEW defensiva pendiente**. Una vez las cinco estén aprendidas, esa opción desaparece por completo y no se reintroduce en conversaciones futuras, siempre preservando opciones sociales y aprendizaje ofensivo.
6. El aprendizaje es real, una técnica a la vez con su pedagogía aprobada; no es un grant por llegar a II. Una ceremonia sólo **visualiza** un `LEARNED` ya confirmado; no puede concederlo ni duplicarlo.
7. Eliminar el **grant legacy de Piel de Cobre en M03** y su dependencia para resolver el muñeco. **No eliminar** el identificador canónico `piel_cobre`, su catálogo/efecto balanceado, ni mecanismos defensivos generales legítimos: reaparece como defensiva NEW de Tierra desde II mediante `Player Learning`.

Catálogo de defensivas (IDs existentes, no inventar):

| Elemento | ID | Nombre |
|---|---|---|
| Fuego | `cuerpo_horno` | Respiración del Cuerpo-Horno |
| Metal | `armadura_plata` | Armadura de Plata |
| Agua | `espejo_luna` | Espejo de Luna |
| Tierra | `piel_cobre` | Piel de Cobre |
| Viento | `paso_nube` | Paso de Nube Ligera |

## Cambio crítico M03 — resolver en este orden

En la candidata B1-B5 actual:
- `gestionarMisionesNpc('shen_baojun')` durante M03 activa inyecta `player.tecnicas.piel_cobre`, la prepara, registra `TECNICA_PIEL_COBRE_APRENDIDA` y `M03_PIEL_COBRE_INSTRUIDA`;
- `registrarUso(tid,...,objetivo)` marca `M03_PRACTICA_MUNECO_COMPLETADA` sólo para `tid==='piel_cobre'` y muñeco Arc 1 en patio marcial;
- `progresoArc1('M03')` menciona y exige Piel de Cobre;
- `cerrarArc1('M02')` ancla a Shen hasta el hito legado `M03_PIEL_COBRE_INSTRUIDA`;
- normalizadores/fixtures de legacy contienen también los hitos de Piel de Cobre.

**Sustitución limitada aprobada por el usuario:**
- Durante M03, Shen enseña un **fundamento/práctica básica**, no una defensiva NEW ni una defensa prestada; no se nombra Piel de Cobre.
- La misión conserva el **muñeco existente de `patio_marcial`**, la evaluación en `patio_respiracion` y la formalización por Qiao Ren en `pabellon_disciplina`.
- El hito `M03_PRACTICA_MUNECO_COMPLETADA` debe provenir de un recibo/evento auténtico del dominio de entrenamiento autorizado, **no** de flags, contadores/client claims, fake combat, muerte de monstruo ni una llamada legacy artificial.
- Resolver el criterio exacto del ejercicio mediante el contrato real; no inventar umbrales, Qi, daño, stats del muñeco, tick/timers ni nuevos rooms.
- Conectar la práctica y el recorrido auténtico con la finalización y promoción/cultivo Lianqi II conforme a sus autoridades. **M03 hecha y Lianqi II pueden ser hitos distintos**: nunca equiparar uno automáticamente con el otro.
- Eliminar los grants legacy en M03 y referencias/hints obsoletos, incluyendo anclaje y pruebas, sin romper fuentes ajenas. Eliminar semánticas viejas sólo si se sustituye su consumidor de forma completa, sin conservar flags huérfanos usados como prerrequisito.
- Si las fuentes de Training, meditación o cultivo no están conectadas y no puede acreditarse un recorrido auténtico: **declarar BLOCKED** con punto exacto; no abrir defensivas mediante un nivel simulado ni afirmar campaña completa.

## Conexión UI V06 (NO copiar el simulador como motor)

La V06 es **referencia visual y de interacciones**, no fuente de autoridad de misión ni de aprendizaje. Reutilizar únicamente CSS/HTML/SVG/Canvas y patrón de fases compatible con host productivo; eliminar el estado mock, diálogos ficticios y `learned` local de demo. Prohibido crear una segunda terminal.

- Mantener la terminal original única `form#form` / `input#entrada` y flujo A07 original.
- El jugador inicia voluntariamente el diálogo con `hablar shen` / `hablar shen baojun`. Nada se inicia al entrar a la sala o tras subir de nivel.
- Antes de Lianqi II, no mostrar servicio, nombres, pestañas ni pistas sobre defensivas. Las tres opciones sociales originales y la enseñanza ofensiva permitida se mantienen.
- Desde Lianqi II auténtico, y sólo si faltan defensivas, ofrecer la opción de servicio defensivo; escoger una lección no concede nada.
- Las dos evidencias pedagógicas por técnica deben ser autoritativas (Teaching), diferenciadas y sin examenes/combates inventados; la UI registra intentos/errores visuales sin alterar el motor.
- Solo un `LEARNED` auténtico del dominio Player Learning con `knowledgeRevision` actualizada cambia la lista y permite la ceremonia final; V06 no debe emitir `LEARNED` desde `skip`, `close`, `reset`, CSS ni JS local.
- Las cinco ramas disponibles desde inicio de II; cualquiera se aprende primero; cada técnica aprendida desaparece de ofertas. La quinta oculta la opción completa del diálogo, **no todo el NPC**.
- Cancelar antes de `LEARNED` no concede; cerrar después conserva la adquisición. Control de reentrada, diálogos de otro NPC y callbacks antiguos; `prefers-reduced-motion`; cero bloqueo de teclado; foco devuelto a la terminal tras cerrar; imágenes externas, bibliotecas, llamadas de red prohibidas.
- V13 de ofensivas y B1-B5 aprobadas se preservan intactas. No reabrir NPC core A07 ni modificar IA A07/G03, balance, drops, equipo, Pi, Qi, XP, ramificaciones, injertos, ultis o SAVE/LOAD fuera de una dependencia estricta reportada.

## Obligación de verificación

Pruebas reales en Chromium sin inyección de estado ni mutación oculta del jugador:
1. Desde partida nueva, en **Lianqi I** hablar con Shen. Cero textos/opciones/listas de defensivas, incluso a través de M03 activa y reentrada; ofensivas conservadas.
2. Completar M01, M02, M03 por ruta auténtica: sin grant de Piel, con práctica genuina del muñeco, evaluación y Qiao; confirmar cultivo hasta **Lianqi II** por evento auténtico.
3. Al alcanzar Lianqi II, ofrecer las **cinco defensivas** y permitir comenzar por cualquiera de las cinco raíces.
4. Al aprender una, probar su `LEARNED` real y ceremonia V06 después; comprobar `knownIds`/`knowledgeRevision`, ausencia de duplicados, efectos y stats sin cambios no autorizados.
5. Probar secuencias de las cinco defensivas en **orden distinto**, hasta 5/5. Tras la quinta, desaparece solamente el servicio; diálogos sociales y ofensivas siguen operativos.
6. Probar mala elección y corrección, cancelar antes y después del commit, Escape, callbacks obsoletos, entradas de otros NPC y nueva partida.
7. Regresiones G03→M02, B1-B4/B1-B5, A07/Teaching, V13 ofensivas, guardias de combate, muestreo de 5 raíces.
8. Establecer ausencia de menciones defensivas PRE-II mediante auditar texto de NPC, quest hints y menús, no sólo `display:none`.

Entregar nueva candidata experimental HTML **separada**, sources/diffs, manifiesto hashes, logs/capturas Chromium, fixtures y evidencia de hitos. Clasificar PASS / FAIL / BLOCKED / NOT_RUN. No tocar `main`, no merge, no push ni sobrescribir las candidatas aceptadas. **Detenerse para auditoría independiente.**

### Estado de los insumos

Ambos HTML incluidos son bases de referencia existentes. **Este paquete NO contiene una integración productiva de las defensivas**: esa es la tarea autorizada para Astra.
