# La Grulla Blanca — Auditoría independiente M03 P1 (09/10/2026)

## Objeto

- Entrega: `ASTRA_M03_P1_FOUNDATION_PRACTICE_REVIEW_2026-10-09.zip`.
- Candidata: `grulla-blanca_ver76_A07_9_G03_M03_P1_CANDIDATE.html`.
- SHA-256: `f199fb5c798da17b17dbc2a0be7d0ec0d979db4e2b7898128e16ebad1a978731`.
- Alcance: sustitución experimental de Piel de Cobre legacy en la instrucción y práctica de M03, sin resolver la evaluación P2 ni el ascenso de cultivo P3.

## Integridad

- HTML adjunto idéntico a la copia de ZIP.
- Verificador del paquete: 636/636 comprobaciones, PASS.
- B1-B5 fuente base disponible localmente con SHA-256 `3a734ea5b2d1908d71f3a78d9b10aeb729f6263dbe5f4a72d3863682aac8e3c0`.
- No verificación remota adicional de la rama ni de los archivos de Git; la ausencia de cambios en `main` es una declaración de manifiestos de Astra, no una constatación independiente remota.

## Prueba independiente ejecutada

- `node --test tests/foundation.test.mjs`: 33 PASS, 0 FAIL.
- `harness/test_p1_chromium.cjs`, sobre la candidata entregada, cinco raíces: 61 PASS, 10 BLOCKED, 1 NOT_RUN, 0 FAIL y 0 errores JS.
- Para salvar el bloqueo de navegación localhost y file:// del entorno, se modificó únicamente la copia local del harness (no la candidata) para usar Playwright `page.setContent(...)`. Los comandos de juego siguieron enviándose por `#entrada` y las aserciones mantuvieron la lectura de estado sólo para verificación.
- `test_p1_teaching_compatibility.cjs`: se completaron 24 PASS de las primeras cuatro raíces y 6 PASS de Viento en una ejecución separada. El primer intento se interrumpió por límite de tiempo después de 24 PASS, **no por fallo funcional**.
- Total comprobado en Chromium en esta auditoría: 91 PASS (61 P1 + 30 compatibilidad), 10 BLOCKED declarados y 1 NOT_RUN; no contabilizar la primera ejecución interrumpida como una batería completa.

## Evidencias de comportamiento

1. Recorrido genuino de P/M01/M02 activa M03 en las cinco raíces.
2. Shen autoriza un hito nuevo `M03_FUNDAMENTOS_INSTRUIDOS`; no concede ni prepara `piel_cobre`.
3. `examinar muneco` en Patio Marcial inicia la práctica sin acreditarla. Ejercicio: PREPARATION → EXECUTION → CORRECTION. Errores no avanzan; cancelar impide commit y los callbacks obsoletos no cuentan.
4. Las tres elecciones correctas producen un único `M03_PRACTICA_MUNECO_COMPLETADA`, sin alterar al muñeco, atributos, Qi, maestría, técnica o Player Learning.
5. Reentrada/replay no conceden práctica duplicada; una partida nueva limpia el estado.
6. En todas las raíces, con dos y con cinco ofensivas aprendidas auténticamente, la práctica funciona y Shen conserva sus tres opciones sociales y el servicio ofensivo según disponibilidad.
7. Después de la práctica M03 **sigue activa**, `EVALUACION_CIRCULACION_SUPERADA` no existe y el owner permanece en `LianQi_I`; esto es el comportamiento esperado mientras P2/P3 no estén conectados.

## Revisión de fuente

- El texto de concesión de Piel, el hito `TECNICA_PIEL_COBRE_APRENDIDA` y `M03_PIEL_COBRE_INSTRUIDA` no aparecen en el HTML experimental entregado.
- La fuente del dominio distingue recibos privados y verifica actor/generación/sala/misión/encuentro; no usa el Monster Owner para el muñeco ni reintroduce el `registrarUso` legacy de Piel.
- No se comprobó en esta auditoría la ejecución independiente de todas las regresiones M02/B14/V13 y A07 de Astra. Sus resultados declarados son adicionales, no parte del total independiente anterior.

## Dictamen

**P1 APROBABLE EXPERIMENTALMENTE** dentro de su alcance. No autoriza integración a `main`, merge, push, promoción del producto ni declara completada M03. La UI V06 no está integrada en P1.

## Próxima decisión humana recomendada

P2: evaluar al personaje en el Patio de Respiración después de completar P1, con una secuencia verificable de regulación del aliento, coordinación y corrección; input nativo, consecuencias semánticas sólo una vez y sin modificar Qi de combate. Se necesita contrato final de éxito/error/cancelación y productor privado de `EVALUACION_CIRCULACION_SUPERADA` / `evaluacionCirculacion=SUPERADA`. Qiao valida P1+P2; no concede automáticamente Lianqi II. P3 sigue condicionado a las autoridades NEW de progreso de cultivo, umbral, requisitos y emisor I→II. Solo luego se considera la UI V06 para defensivas.
