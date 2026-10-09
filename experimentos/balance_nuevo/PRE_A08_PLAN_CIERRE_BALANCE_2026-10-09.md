# La Grulla Blanca — cierre de balance antes de A08

**Fecha:** 2026-10-09  
**Autoridad:** aclaración humana: *Astra recibirá el paquete una vez cerrados equipamiento, técnicas y monstruos*. A08 **NO** es una dependencia para balancear esos sistemas.  
**Estado:** ORDEN DE TRABAJO CORREGIDO / PLAN, NO FREEZE.  
**Rama:** `experiment/lii-tramo1-multirraiz-v08-2026-10-08`; no tocar main, no merge, no implementación de runtime.

## Corrección de secuencia y dependencia

El handoff `lii_concordancias_v16/HANDOFF_PARIDAD_Y_AUTORIDAD_PARA_ASTRA_2026-10-09.md` es **PREPARACIÓN FUTURA / DIFERIDO**: no debe mandarse a Astra como prerequisito del balance ni exigirse que A08 o un HTML integrado existan primero.

**Orden:**
1. **Cerrar técnicas y Concordancias** de LianQi II sobre motor de laboratorio y contratos aprobados, fijando por decisión humana los números/semántica que aún falten. Preservar LianQi I (0 PT, sin defensivas ni AOE).
2. **Cruce técnicas × seis monstruos normales LII** T0–T2 con 2 PT y equipo por etapa. Ajustar monstruos solo si persiste evidencia tras cerrar jugador y equipo de referencia.
3. **Ajustar equipamiento y disponibilidad/economía** LII: estadísticas, acceso real por etapa, fuentes de drops, extracción distinta del drop, intercambios/precios y contribución **no gastable** conforme a contratos previos. Repetir cruces focales de equipo con técnicas y monstruos; no inventar objetos, NPC, misiones, tiendas, gates o asignaciones.
4. **Cierre integral y freezes reproducibles** de técnicas, Concordancias, seis monstruos, equipo y economía/acceso, con manifiestos, criterios de regresión LI, SHA-256, runners reproducibles y decisiones humanas explícitas.
5. **Entregar paquete cerrado a Astra para iniciar A08** y solicitar entonces paridad de eventos en HTML/integración. Fallos que Astra detecte se devuelven como incidencias de paridad, no se reinterpreta unilateralmente el balance.

Este orden puede implicar iterar **técnicas → monstruos → equipo → contraste focal monstruos/equipo** sin reiniciar pruebas generales ya cerradas.

## Estado heredado de los laboratorios

- **V05–V09:** dificultad de seis monstruos, uso del Tramo I, builds y técnicas ajenas; evidencias útiles pero parte de adquisición/coste ajeno era hipotética.
- **V10–V14:** sensibilidad y pruebas estructurales de Concordancias; múltiples escalas experimentales, **no canónicas**. Cuatro relaciones sin escala ratificada: `METAL_TO_FUEGO`, `AGUA_TO_METAL`, `AGUA_TO_VIENTO`, `TIERRA_TO_VIENTO`. Cuatro conflictos de prioridad `AGUA_TO_VIENTO` en Paso de Nube. Verificar PRE_COST y Espejo de Luna Eficiencia; Placa Fundacional y Embalse.
- **V15:** cruce V07 original/candidato vs Concordancias defensivas BASE; candidate-only.
- **V16:** cruce físico estructural de Placa/Embalse con ORIGINAL/V07: **73.728** combates de laboratorio, **no freeze integral**. La falta de paridad con HTML antiguo no debe bloquear los números del laboratorio; debe quedar como riesgo de futura integración.
- No reutilizar un candidato HTML antiguo (siete secuencias) como autoridad para las veinte relaciones actuales.

## Decisiones humanas que se deben resolver en ESTE frente (no delegar a Astra A08)

- Prioridades conflictivas de hooks con base en contratos; cuando exista contradicción real, presentar alternativas y obtener aprobación humana.
- Escalas específicas de Concordancias defensivas LII, incluidas cuatro nuevas y efectos estructurales. Buscar **candidatos con microtests reproducibles** y proponer decisión, nunca canon por defecto.
- Determinar si Tramo I Espejo de Luna Eficiencia necesita ajuste por breakpoint de Qi; mantener costo base LI intacto.
- Resolver condiciones mecánicas y costes reales que deben regir técnica ajena **en diseño**: lo no establecido no puede convertirse en hecho del HTML actual.
- Seleccionar, posponer o descartar V07 para Fuego, Metal y Viento después de ver la interacción con Concordancias.
- Establecer gate global de equipo/monstruos con `POST_M03`, `LI_CARRYOVER` y `EXPECTED_STAGE`, sin equiparar tier de adaptación T0–T2 a cultivo.

## Criterio de entrega final a A08

Debe existir un paquete de autoridad versionada que incluya:
1. Tabla definitiva de todas las técnicas LII (BASE, 3 rutas de Tramo I, costes, efectos, prioridad y concordancias; 2 PT legales).
2. Tabla definitiva de seis especies normales por T0/T1/T2, comportamientos y adversarios por equipo/raíz.
3. Catálogo de equipo LII y acceso/economía cerrados, incluyendo cómo adquirir/comprar/vender intercambiar, sin tocar contribución gastable.
4. Decisiones explícitas; reportes finales estadísticos con seeds, metodología, limitaciones; suites de regresión LI y LII y manifiestos/hashes.
5. Distinción entre **números/diseño congelados** (responsabilidad frente de balance) y **paridad/integración en HTML** (responsabilidad A08 de Astra).

### Guardias permanentes
No main, no merge, no push canónico; no cambios de `ROOMS.exits`; no invención de NPC/rooms/misiones/vendedores; no elite LII ni T3/T4 en la batería normal; no reabrir freezes de LI por defecto. Nada se considera aprobado por el usuario hasta revisión humana.

**Siguiente acción del frente:** preparar el paquete de *decisiones de Concordancias/técnicas LII* a partir de V12–V16, con recomendaciones numéricas y riesgos cuantificados. **NO enviar todavía a Astra**.
