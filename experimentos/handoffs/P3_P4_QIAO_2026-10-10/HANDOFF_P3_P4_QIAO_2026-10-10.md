# HANDOFF — La Grulla Blanca — P3/P4 — Qiao NEW
**Corte:** 2026-10-10  
**Repositorio:** Shein25/La-Grulla-Blanca  
**Rama de respaldo:** `handoff/p3-p4-qiao-new-2026-10-10`  
**Guardia:** main intocable; sin merge, sin promoción productiva.

## Autoridad de fuente
- Última candidata experimental aportada por Astra: `CANDIDATE(4).html`, SHA-256 **9f0bbde077e39edffda1ab75c70f0de85a40df7a51bba4e92fccc5d63b469f43**, 3 867 516 bytes.
- Última candidata previa / hotfix inventario: `CANDIDATE(3).html`, SHA-256 **a766671d9430be06d157fdccd821bba52532fb74ce28dcacd99dd54af9ff1927**.
- Backup reproducible completo de Astra: `ASTRA_QIAO_NEW_MATERIAL_DELIVERY_REVIEW_2026-10-09.zip`, SHA-256 **3b985ba6ab0d5300ef0f5355eca5cc0323a50000ba351390d5f3e5b0c8390941**. El backup local compartido en la conversación de ChatGPT incluye ese ZIP sin alteraciones, candidata exacta y demos UI.
- Astra reportó trabajo sobre rama `integrate/astra-arc1-ai-v0.1` HEAD `d535f4f52cb36231d6ad95e6ab0e1d8ef6932b23`, **no validado como HEAD remoto por esta nota**.
- El archivo de candidato en esta carpeta (si presente) puede ser una copia textual con saltos de línea normalizados; **el SHA-256 de la copia local ZIP anterior es la autoridad binaria**. No equiparar hashes distintos silenciosamente.

## Contratos aprobados antes de esta entrega
- P1/P2 M03: etapa real sigue **Lianqi I**, Shen muñeco + meditación + formalización Qiao.
- Productores privados de derrota/movimiento NEW: evidencia legítima, sin créditos de misión automática.
- Ecología NEW: 6 ratas normales añadidas en Valle(2), Sauces(2), Bosque Bajo(2), separadas de la rata especial `errant:rata_despensa` de M02; respawn crea nueva vida con identidad propia y protección contra duplicación. Sin tocar salas ni `ROOMS.exits`.
- Cadáveres y extracciones difíciles NEW → materiales físicos con procedencia individual → inventario NEW independiente. Hotfix `inventario` conserva pociones/equipo/piedras ordinarios y añade sección NEW.
- Estas aprobaciones son **experimentales**, nunca equivalen a P3 completo integrado.

## Bloque Qiao en revisión
- Nueva transferencia física privada de seis materiales NEW: **3 Cámaras de jade** de `avispa_jade` y **3 Membranas férreas** de `escarabajo_hierro`.
- Interacción nativa `ENTREGAR QIAO REN` con confirmación MC; selección con identidad y procedencia, doble validación, rechazo por sala/actor/contexto, cancelación sin consumo, anti-replay, consumo/recepción atómicos e idempotentes.
- No concede misión P3 completada, reconocimiento, píldora, etapa II ni defensivas P4. `missionActive=false`; no SAVE/LOAD NEW.
- **Astra reporta:** Chromium 5 raíces = 50 PASS/5 BLOCKED; material inventory 105 PASS/15 BLOCKED; lifecycle 97 PASS; P2 330 PASS; M02 37 PASS/2 NOT_RUN; ratas 140 PASS/5 BLOCKED; UNIT 174 PASS; VM 89 PASS. Son pruebas de **Astra**, no independientes.
- **Revisión independiente de esta conversación:** integridad 1532/1532 y UNIT 174/174 reportadas como repetidas; ejecución completa independiente **Fuego** obtuvo 3+3 extracciones auténticas, un solo recibo de seis ítems, inventario consumido, permanencia en Lianqi I y guardias contra callback obsoleto/cancelación/repetición. Ejecución independiente total de las cinco raíces excedió tiempo: **NO afirmar certificación independiente de las cinco**.

## Bloqueos y decisiones de diseño pendientes
1. **SAVE/LOAD NEW auténtico:** persistir lifecycle, vidas, cadáveres, extracciones, materiales, transacción de entrega, recibos, flags de Qiao, M02/M03 y preventores de replay. No simularlo con diagnósticos.
2. **Misión P3 completa NO activada:** objetivos **provisionales** 40 victorias reales, 3 especies, hasta 6 ratas, 10 extracciones difíciles de 2+ especies (3+ por especie), 75% exploración accesible, entrega de 6 piezas (3+3). Aprobación de dificultad después de simulación real en cinco raíces.
3. **Decisión 75%**: 185 salas (139) o diez áreas (8) y visitas previas a misión: no asumir denominador ni retroactividad.
4. **Píldora del Primer Umbral NEW**, no reutilizar Píldora de Consolidación. Reposición corta tras fallo todavía por ratificar. Cancelar antes de iniciar no consume; tras comenzar, consumo según contrato; fallos de infraestructura requieren rollback/compensación.
5. **Ritual V08** sólo tras `meditar` en Patio de Respiración después de misión/píldora. Tres fases 3+3+4 brechas; al final **sólo clic central dentro del núcleo**, sin botón externo duplicado. V08 es demo, **NO integrada**.
6. **Ascenso II** exclusivamente con `CultivationDomain` y `applyStage` NEW, transacción autoritativa; no cambios ficticios ni legacy.
7. **P4**: enseñanza de cinco defensivas Shen sólo después de II real, orden libre, ocultar aprendidas y retirar servicio al terminar cinco, preservando ofensivas y diálogo. V06 es demo.

## Próximo chat: orden de trabajo
(1) Leer handoff y recuperar candidata SHA exacta. (2) Cerrar auditoría de entrega Qiao en las cinco raíces sin inventar PASS. (3) Revisar atomicidad y casos negativos. (4) Diseñar/implementar SAVE NEW experimental con aceptación y replay. (5) Ratificar balance y exploración; integrar P3, píldora, V08 y sólo después P4. Mantener main intacta; sin merge ni pushes de integración no autorizados. No reabrir M01–M03/A07 ni cambiar `ROOMS.exits`.
