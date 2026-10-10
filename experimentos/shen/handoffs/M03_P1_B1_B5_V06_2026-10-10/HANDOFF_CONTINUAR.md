# HANDOFF — La Grulla Blanca | Shen, B1-B5, M03 P1 y UI defensiva V06
Fecha de cierre: 2026-10-10. Repositorio: https://github.com/Shein25/La-Grulla-Blanca

## AUTORIDAD Y ESTADO
- Última candidata del frente: `grulla-blanca_ver76_A07_9_G03_M03_P1_CANDIDATE.html` (original SHA-256 `f199fb5c798da17b17dbc2a0be7d0ec0d979db4e2b7898128e16ebad1a978731`).
- Base aceptada: `grulla-blanca_ver76_A07_9_G03_B1_B5_CANDIDATE.html` (original SHA-256 `3a734ea5b2d1908d71f3a78d9b10aeb729f6263dbe5f4a72d3863682aac8e3c0`).
- UI de referencia (NO productiva): `GRULLA_UI_DEFENSIVAS_LIANQI_II_V06_TERMINAL_UNICA.html`, original SHA-256 `d6725a805ff812837a26a5ed06e1ba42d5e4665df61d01f5e6927bbebc5c1fe0`.
- B1-B5 **aprobado experimentalmente**: enseñanza de cinco ofensivas con su servicio social y continuación de Shen en M03 activa; última auditoría: nueve recorridos independientes y 323/323 comprobaciones documentales. NO se ha probado como completada M03.
- M03-P1 **aprobado experimentalmente**: Shen instruye fundamentos; ejercicio real ante el muñeco del Patio Marcial, sin enseñar Piel de Cobre legacy. Auditoría independiente: 33/33 unitarias, 61 PASS de P1 en Chromium + 30 PASS compatibilidad Teaching, 10 BLOCKED esperados por P2/P3, 1 NOT_RUN; paquete de Astra con 636/636 comprobaciones estructurales. No confundir con M03 completada.
- P2 **PENDIENTE**: el usuario pidió a Astra **primero los criterios narrativos y mecánicos concretos, sin implementar**, para evaluar circulación en Patio de Respiración y permitir formalización de Qiao Ren.
- P3 **BLOCKED**: faltan autoridad NEW de `cultivation_progress`, `cultivation_threshold`, `breakthrough_requirements` y emisor auténtico de evento I→II. M03 hecha, afiliación/estatus institucional y alcanzar Lianqi II son cosas distintas. No usar barra de Qi de combate ni etapa legacy como autoridad.
- P4 **PENDIENTE**: integración auténtica de cinco defensivas NEW con UI V06. No comenzar antes de autenticar Lianqi II NEW.

## DECISIONES HUMANAS FIRMES
1. **En Lianqi I ninguna defensiva**. Shen no menciona el futuro servicio, sus nombres, condiciones ni 'vuelve en Lianqi II', tampoco en opciones inactivas.
2. Piel de Cobre legacy se retira exclusivamente de la instrucción/práctica obligatoria M03. **`piel_cobre` NEW canónica NO se borra**.
3. Las cinco defensivas disponibles simultáneamente desde Lianqi II auténtico, en orden libre y sin priorizar la raíz:
   - Fuego `cuerpo_horno` — Respiración del Cuerpo-Horno
   - Metal `armadura_plata` — Armadura de Plata
   - Agua `espejo_luna` — Espejo de Luna
   - Tierra `piel_cobre` — Piel de Cobre
   - Viento `paso_nube` — Paso de Nube Ligera.
4. Sólo Teaching y Player Learning productivos conceden cada `LEARNED`. Ceremonia visual después del commit, nunca como concesión. Cada técnica adquirida desaparece de ofertas; tras 5/5 se oculta SOLO el servicio defensivo, preservando diálogo social y ofensivas.
5. UI V06 **es demo visual**, no integrada en el HTML del juego: terminal inferior ÚNICA (`form#form`, `input#entrada`), sin diálogo automático; el jugador escribe `hablar shen` para iniciarlo. Conservar animaciones y estilos diferenciados.
6. M03-P1 actual: `M03_FUNDAMENTOS_INSTRUIDOS`; práctica PREPARATION → EXECUTION → CORRECTION mediante `examinar muneco`; equivocación, cancelación, reentrada, callbacks obsoletos protegidos; un único `M03_PRACTICA_MUNECO_COMPLETADA`. No stats, Qi, maestría ni Player Learning concedidos.
7. Preservar G03→M02, A07 NPC, B1-B5, V13 ofensivas, las salas existentes y la lógica NEW. No main, no merge, no push de candidata productiva, no sobrescribir aprobadas, sin alterar balance, monstruos, equipo, SAVE/LOAD.

## ALCANCE DEL SIGUIENTE CHAT
El usuario traerá la **respuesta de Astra al pedido de contrato P2**. Leer íntegramente respuesta/ZIP y comparar:
- evaluación auténtica en Patio de Respiración posterior a P1;
- criterios verificables de respiración, estabilidad y coordinación; errores/correcciones, cancelación, replay;
- evidencia privada para `EVALUACION_CIRCULACION_SUPERADA` y `evaluacionCirculacion=SUPERADA`;
- Qiao Ren sólo valida práctica+evaluación para formalización, NO otorga Lianqi II;
- sin métricas o Qi inventados ni hito por mera presencia o `meditar` una vez.
Emitir diagnóstico, decidir si ratificar contrato y luego eventualmente autorizar implementación experimental P2. No asumir que P2 se implementó.
P3/P4 siguen separados.

## PROVENIENCIA GIT / RESTAURACIÓN
Esta rama de respaldo deriva de `implement/3c6-prologo-m01-m07` en `748bd4480e37fd2523fa833081b20522b9724dab`, NO de la rama local `integrate/astra-arc1-ai-v0.1` declarada por Astra (`d535f4f52cb36231d6ad95e6ab0e1d8ef6932b23`; no publicada aquí).
Se guardan los HTML experimentales como **objetos/documentos en carpeta de handoff**, sin sustituir runtime de Git. Los dos HTML gigantes tienen saltos CR normalizados a LF por el canal de lectura: sus blobs Git difieren a nivel byte del original. El respaldo ZIP descargable conserva **bytes originales de todos los archivos citados y evidencias Astra**. Consultar `MANIFEST_BACKUP.json` para hashes de original y blob Git.
No presentar esta rama como release ni integrar a main. No se generan cambios de motor en este cierre.
