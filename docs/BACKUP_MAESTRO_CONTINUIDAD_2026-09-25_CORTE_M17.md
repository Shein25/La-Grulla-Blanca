# BACKUP MAESTRO DE CONTINUIDAD — La Grulla Blanca

**Fecha:** 2026-09-25  
**Objetivo:** permitir continuar el proyecto en un chat nuevo sin perder estado, jerarquía documental, ramas, SHAs, auditorías, pendientes ni guardarraíles.  
**Repositorio:** `Shein25/La-Grulla-Blanca`

---

# 0. INSTRUCCIÓN PARA UN CHAT NUEVO

Usá este archivo como punto de entrada del proyecto.

Reglas:

1. No mezclar propuestas históricas con canon posterior.
2. No inventar rooms, conexiones, NPC, gates, revelaciones, permisos ni estados.
3. Las decisiones humanas posteriores explícitas prevalecen sobre documentación anterior.
4. El trabajo documental y los experimentos NPC son frentes separados.
5. No implementar ni hacer merge sin contrato y auditoría correspondiente.
6. `ROOMS.exits` y la topología 329 están congelados salvo autorización explícita.
7. No modularizar el HTML durante etapas 3C activas.
8. M16 está cerrada documentalmente; M17 es el frente documental activo en REV1. M18 todavía no fue iniciado.

---

# 1. BASELINE CANÓNICO DEL JUEGO

`grulla-blanca_ver74.html`

SHA-256:
`8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

`SAVE_SCHEMA_VERSION = 2`

Mundo congelado:

- 329 salas;
- 17 áreas;
- 787 salidas dirigidas;
- 786 internas + 1 externa;
- 0 reciprocidades rotas;
- 0 salas aisladas;
- 1 componente físico;
- 185 salas inicialmente alcanzables;
- 144 inicialmente bloqueadas;
- 63 articulation rooms;
- 70 bridges;
- 13 alojamientos;
- 6 atajos de Primera Ala.

Etapas ya cerradas antes de misiones:
`PRE-3C`, `3C.1`, `3C.1R`, `3C.1B`, `3C.2`, `3C.3A`, `3C.3B`, `3C.3`, `3C.4`, `3C.5`.

3C.5 quedó aprobado con:
- 32/32 NPC;
- 398/398 PASS en navegador;
- ROOMS.exits y GATES_329 intactos;
- sin scheduler NPC, Utility AI, GOAP ni misiones nuevas en producción.

---

# 2. 3C.6A — PRÓLOGO + M01–M07 DOCUMENTAL

**Estado:** `CERRADA_DOCUMENTALMENTE_APTA_PARA_CONTRATO`.

Rama:
`audit/3c6a-rev3-1`

HEAD actual verificado:
`0043af92b22d003e3ce4859a3556fd770ee1130d`

Commit realmente auditado en el cierre:
`3a9f9e59cf7b84a346de52ffda2b332055177216`

Documentos clave:
- `docs/3C6A/Auditoria_Final_3C6A_REV3_1_CLAUDE.md`;
- `docs/3C6A/CIERRE_3C6A_REV3_1.md`;
- `docs/3C6A/Reconciliacion_3C6A_Prologo_M01_M07_REV3_1.md`;
- `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3_1.json`.

Matriz canónica SHA-256:
`96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881`

Veredicto:
`3C6A_REV3_1_APTA_PARA_CONTRATO`.

Invariantes de frontera:
`SECTA_INTERIOR=false => M12=false => ATAJO_ALA_*=false`.

Regla congelada M06:
cuando se registra por primera vez un nuevo tipo de `flags.arc1.evidenciaTerritorial.tipos`, ejecutar inmediatamente `reconciliarProgresionArc1()` en la misma acción.

Gate LII→LIII:
`player.etapa>=3 + qi>=45 + pildora_consolidacion consumida + M04 HECHA + M05 HECHA + evidenciaTerritorial>=SUFICIENTE + informeFronteraAceptado=true`.

Efecto one-shot:
`arc1.estado=LIII_INVESTIGACION`, `SECTA_INTERIOR=true`, `M12=false`, todos los `ATAJO_ALA_*` permanecen falsos.

---

# 3. 3C.6 IMPLEMENTACIÓN — BLOQUEO ACTUAL DE PRODUCCIÓN

Contrato:
`contract/3c6-prologo-m01-m07`

HEAD contrato:
`b0d90ea70ab17b3d6a7e85951e19f00c7935c8f2`

Rama de implementación:
`implement/3c6-prologo-m01-m07`

HEAD actual verificado:
`748bd4480e37fd2523fa833081b20522b9724dab`

Candidato:
`grulla-blanca_ver75.html`

SHA-256 candidato:
`513d7333abc6d0286603f1368198ba5595e865025995fe10331a9393f0fb8fdc`

Auditoría Claude real Chromium:
`REQUIERE_CORRECCIONES`.

Problema principal H-1:
`deserializar()` ejecuta `temporal.entrarSala()` y luego copia estado persistente modificado por la entrada de sala. Cargar partida puede alterar `visitadas`, `flags`, `quests`, inventario/cadáveres u otros hitos.

Casos sensibles ya identificados:
- `descansillo` durante Prólogo;
- `dormitorio_externos` durante M01;
- `deposito_comun` durante M02;
- `bosque_refugio_patrulla` durante M04;
- `mercado_valle` / `granero_valle` durante M05;
- `sauces_casa_huespedes` durante M05.

Solución requerida:
separar normalización/migración persistente de la materialización de la sala. `entrarSala()` puede derivar `vivos`/cooldown, pero sus nuevos efectos persistentes no deben reimportarse durante load.

H-2:
corregir el informe de implementación: la afirmación histórica de “cero nuevos fallos” no fue válida bajo Chromium real.

H-3:
no crear flags redundantes. Equivalencias documentales:
- `PRIMERA_PATRULLA_VALIDADA` → cierre efectivo M04 / `M04_RETORNO_INFORMADO`;
- `RUTA_SAUCES_VALIDADA` → cuatro checkpoints M05;
- `EVIDENCIA_TERRITORIAL_SUFICIENTE` → `evidenciaTerritorial.nivel >= SUFICIENTE`.

**Estado actual:** producción ejecutable sigue bloqueada detrás de la corrección/re-auditoría de 3C.6. No mergear ver75.

---

# 4. 3C.7A — M08–M11 REV2

Rama documental central:
`audit/3c7a-fase1-rev2`

Documentos:
- `docs/3C7A/Reconciliacion_3C7A_M08_M11_REV2.md`;
- `docs/3C7A/Matriz_Implementacion_3C7A_M08_M11_REV2.json`.

Estado:
`REV2 preparada; falta cierre/auditoría independiente antes del contrato ejecutable`.

Columna:
`M08/M09/M10 paralelas → M11`.

Revelaciones:
- M08 → R2 CONFIRMADO;
- M09 → R3 PARCIAL;
- M10 → R4 CONFIRMADO;
- M11 → R3 CONFIRMADO.

M11 produce:
`M11=HECHA`, `R3=CONFIRMADO`, `flags.arc1.sintesis.DOS_ALAS=PRINCIPIO`, +1 Comprensión one-shot `ARC1_M11_DOS_ALAS`, `M11_SELLO_ANTIGUO_RECONOCIDO`; M12 disponible derivada.

No crear `DOS_ALAS=COMPRENDIDAS` como persistencia redundante.

Pendientes relevantes:
- semántica física de `ARCHIVO_RESTRINGIDO`;
- trigger exacto de activación M11;
- runtime predecesor 3C.6 aprobado.

---

# 5. M12 + GATE LIII→LIV REV2 — CERRADO

Estado:
`3C7A_M12_GATE_REV2_CERRADA_DOCUMENTALMENTE_APTA_PARA_CONTRATO`.

Documento de cierre:
`docs/3C7A/CIERRE_3C7A_M12_GATE_REV2.md`.

Matriz SHA-256:
`4741f6bc28a36d71d4309783dff51ee8b9a8a187f6250e93a450616d8c222978`

Veredicto Claude:
`3C7A_M12_GATE_REV2_APTA_PARA_CONTRATO`.

Correcciones REV2 cerradas:
`H-A1 RESUELTO`, `H-A2 RESUELTO`, `H-A3 RESUELTO`.

Reglas centrales:
- `SUFICIENTE` habilita progreso/protocolo pero no cierra M12;
- `CONCLUYENTE = SUFICIENTE + CORROBORACION_FUERTE_INDEPENDIENTE`;
- Custodio terminal es requisito separado de cierre;
- atajos opcionales, nunca 6/6 obligatorio;
- `PASO_MANTENIMIENTO=false` durante M12;
- no crear rooms `ala_control_este/oeste`;
- no crear `DOS_ALAS=COMPRENDIDAS`;
- `PUERTAS[4]` legacy debe retirarse/neutralizarse para etapa 3→4.

Gate T288 LIII→LIV:
`qi>=75 + M11 HECHA + M12 HECHA + R3 CONFIRMADO + R5 CONFIRMADO + autorización institucional`.

Al superar:
`player.etapa=4`, `arc1.estado=LIV_REVELACION`, M13 disponible derivada.

Pendientes permitidos para contrato:
- fuente concreta de `CORROBORACION_FUERTE_INDEPENDIENTE`;
- mecanismo PROTOCOLO del Custodio;
- localización final del Custodio;
- modelo uniforme de permisos;
- balance numérico;
- sustitución técnica exacta de `PUERTAS[4]`;
- runtime 3C.6 aprobado.

---

# 6. M13–M15 REV2 — CERRADO

Estado:
`3C7A_M13_M15_REV2_CERRADA_DOCUMENTALMENTE_APTA_PARA_CONTRATO`.

Documento de cierre:
`docs/3C7A/CIERRE_3C7A_M13_M15_REV2.md`.

Matriz SHA-256:
`53d3bc817713aba9177d86bb55cf2a44c1b1a02fcdeff0b194137fe36ecab846`

Veredicto Claude:
`3C7A_M13_M15_REV2_APTA_PARA_CONTRATO`.

Correcciones REV2 cerradas:
`H-B1 RESUELTO`, `H-B2 RESUELTO`, `H-B3 RESUELTO`.

M13:
R6 CONFIRMADO; prueba consumo/operación actual, no R7; abre `PASO_MANTENIMIENTO`.

M14:
R8 CONFIRMADO; consentimiento original; `NUCLEO_SUPERIOR`; abre sólo `PASO_NUCLEO`; no R9/R7/R10.

M15:
R9 CONFIRMADO. `RELEVO_PREVISTO` es premisa, no cuarto aplazamiento. Tres aplazamientos: técnico → ruptura → normalización.

Al final M15:
`PASO_PULSO=false`, `NUCLEO_PROFUNDO=false`, R7 cerrado, R10 cerrado, LIBERAR/CUSTODIAR no decidido.

M15 NO activa M16 en el mismo evento y no usa tiempo diegético.

Borrador de contrato existente:
`docs/3C7A/BORRADOR_Contrato_Implementacion_3C7_M12_M15_REV1.md`

Estado:
`BORRADOR_NO_LISTO_PARA_IMPLEMENTACION`.

---

# 7. M16 — ÚLTIMO FRENTE ABIERTO

Nombre:
`M16 · Cuando falla el centro`.

Estado actual:
`3C7A_M16_REV1_CERRADA_DOCUMENTALMENTE_APTA_CON_DECISION_TECNICA_PENDIENTE`.

Autoridad principal:
Fuente Maestra ver55 T281 (posterior a T260).

Archivos:
- `docs/3C7A/Reconciliacion_3C7A_M16_REV1.md` — blob `52f712b84919ac6ad21aea9dcae2bb8ceb327bac`;
- `docs/3C7A/Matriz_Implementacion_3C7A_M16_REV1.json` — blob `44f7b042c0aec0008e57d6881a61fda558389247`;
- `docs/3C7A/fuentes/Fuente_Maestra_T281_M16_EXTRACTO.md` — blob `64aab58a214270188719df85e9f1817b1d11bf7f`;
- `docs/3C7A/PROMPT_AUDITORIA_3C7A_M16_REV1_CLAUDE.md` — blob `b9fc933797f04203306e93ed26050f30bcd7bc7e`.

Snapshot enviado/preparado para Claude:
`f575a45f322575680f972e2313c1bfadbf73616d`.

Paquete local enviado/preparado:
`Paquete_Autocontenido_Auditoria_3C7A_M16_REV1_Claude.zip`.

### Activación

M16 debe activarse en evento separado posterior a M15:
`M16=ACTIVA`, `arc1.estado=LIV_CRISIS`, seis frentes `PENDIENTE`, `EMERGENCIA_SECTA=ACTIVA`.

El disparador exacto todavía es `DECISION_TECNICA_PRECONTRATO`: debe ser explícito, alcanzable, one-shot, sin RNG, sin reloj y sin `entrarSala()` genérico.

### Seis frentes

`MEDICINA`, `RUTAS`, `FORMACIONES`, `RECURSOS`, `SAUCES`, `JARDINES`.

Modelo propuesto:
`flags.arc1.crisisM16.frentes[ID] = PENDIENTE | ESTABLE | COSTOSO | DAÑADO`.

Los booleanos `crisis_<frente>_resuelta` deben ser derivados, no segunda persistencia.

No existe `FALLIDO`.

`DAÑADO` implica coste real pero NUNCA bloquea M17, Fundación/ZhuJi, receta obligatoria ni llave de progreso.

Resolución macro determinista con factores:
`RESPONSABLE + PREPARACION + APOYO + INTERVENCION`.

Sin RNG macro. `resolverFrente()` one-shot/idempotente.

Jugador:
aproximadamente dos intervenciones principales; no contador visible 2/2; entrar a una región no cuenta.

Compañeros:
autónomos, no asignables por UI. Afinidad no controla capacidad básica.

Responsables:
- Medicina: Lan Meihua + Chen Bo + Yao Fen;
- Rutas: Jiang Rui + Ren Bo;
- Formaciones: He Zhen + Wen Tao;
- Recursos: Duan Shibo + Ma Qiren + Lu Cheng;
- Sauces: Xu An + apoyo local;
- Jardines: Su Lian.

`EMERGENCIA_SECTA`:
permiso temporal, sólo conexiones que lo acepten; no sustituye ARCHIVO_RESTRINGIDO, PRIMERA_ALA_INVESTIGACION ni NUCLEO_PROFUNDO; expira al cerrar M16.

Cierre:
`todos los frentes != PENDIENTE` → `M16=HECHA`, emergencia expirada, estabilización provisional, M17 disponible derivada; `arc1.estado` permanece `LIV_CRISIS`.

M16 NO abre PASO_PULSO/NUCLEO_PROFUNDO, NO confirma R7/R10 y NO decide LIBERAR/CUSTODIAR.

Auditoría Claude registrada en:
`docs/3C7A/Auditoria_3C7A_M16_REV1_CLAUDE.md`.

Documento de cierre:
`docs/3C7A/CIERRE_3C7A_M16_REV1.md`.

Veredicto:
`3C7A_M16_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`.

No hubo bloqueantes ni soft-locks nuevos.

Decisiones técnicas pendientes:
- DT-M16-01: el tope “uno o dos apoyos externos importantes” no es literal de T281 y queda `DECISION_TECNICA_3C7_AUDITAR`;
- DT-M16-02: decidir si se conserva atribución “resuelto por quién” como metadato separado del estado terminal o se descarta explícitamente;
- DHP-1 trazado: T281 es la única versión M16 localizada y se adopta como autoridad única.

Test futuro obligatorio:
`0 requisiciones opcionales + 0 únicos + pocos atajos => M16 sigue completable`.

**M16 no requiere REV2 salvo que una decisión técnica futura contradiga T281 o cree soft-lock.**

---

# 8. M17 — FRENTE DOCUMENTAL ACTIVO

**Rama:** `audit/3c9-m17-rev1`.

**Estado:** `3C9_M17_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`.

Archivos creados:
- `docs/3C9/Reconciliacion_3C9_M17_REV1.md`;
- `docs/3C9/Matriz_Implementacion_3C9_M17_REV1.json`;
- `docs/3C9/fuentes/Fuente_Maestra_T290_M17_EXTRACTO.md`;
- `docs/3C9/fuentes/Fuente_Maestra_T257_M17_Tecnica_EXTRACTO.md`;
- `docs/3C9/fuentes/Fuente_Maestra_T240_Nucleo_M17_EXTRACTO.md`;
- `docs/3C9/PROMPT_AUDITORIA_3C9_M17_REV1_CLAUDE.md`.

Autoridad:
T290 principal; T257 técnico; T240 topología; T254/T222 + Auditoría 6; ver74 infraestructura.

Estructura REV1:
`CONSEJO → AUTORIZACIÓN → DESCENSO → R7 → CENTINELA → SALA_RELEVO → R10 → UMBRAL → M17 HECHA`.

Reglas congeladas/propuestas:
- requiere M16 HECHA;
- `arc1.estado` permanece `LIV_CRISIS`; NO crear `LIV_DESCENSO`;
- Consejo en `interior_sala_consejo`;
- Ji Xueying preside; Qiao Ren autoriza;
- permiso `NUCLEO_PROFUNDO` fuente=ORDEN origen=M17;
- abre exclusivamente `GATES_329.PASO_PULSO`: `nucleo_archivo_promesa ↔ nucleo_descenso_pulso`;
- R7 antes de R10;
- R7 principal: `conocimiento.nucleo.dependenciaViva=CONFIRMADO`;
- Centinela: combate/protocolo equivalentes, sin reliquia/cadáver/restos;
- Sala de Relevo obligatoria y conocida por movimiento real;
- R10 en `nucleo_exterior_ancla`: misma Grulla original;
- Cámara de Memoria opcional;
- Comprensión +1 one-shot `ARC1_M17_DEPENDENCIA_VIVA`;
- cierre propuesto al alcanzar `nucleo_umbral_santuario` con R10 confirmado;
- M18 queda disponible, pero no empieza;
- no volver al Consejo;
- no entrar automáticamente al Santuario;
- no avanzar M18.

Legacy ver74 detectado:
`centinela_pluma` sigue en `alturas_mirador_grulla`, tiene loot, restos examinables y lógica histórica de `reliquia_pluma`. Todo eso queda `LEGACY_A_REEMPLAZAR_3C9`; no permitir dos Centinelas únicos simultáneos.

Decisiones a auditar:
- trigger exacto del Consejo;
- movilidad de He Zhen/Lan Meihua/Song Rui en Consejo;
- trigger exacto de R7;
- enum/estado persistente del Centinela;
- room exacta del Centinela (candidata REV1: `nucleo_camara_regulacion`);
- interfaz de protocolo;
- forma de bloquear paso sin tocar `ROOMS.exits`;
- modelo uniforme de permisos;
- balance;
- si exigir el Umbral para cerrar M17 es respaldo literal de T290 o sobreespecificación.

**Siguiente paso:** preparar paquete autocontenido y enviar M17 REV1 a Claude. No implementar ni avanzar M18.

# 8B. M18+

**Estado:** NO INICIADO.

No redactar ni implementar M18 hasta procesar la auditoría de M17 REV1.

---

# 9. ESTRATEGIA FINAL PARA CODEX

Decisión humana actual:
cuando estén reconciliadas y auditadas **todas las misiones M01 hasta la última del Arc1**, preparar un paquete final para Codex.

Codex recibirá el arco completo para conocer todas las dependencias, pero la implementación deberá hacerse por bloques auditables, no como un único cambio gigante.

Principio:
`Arc1 ya está diseñado; Codex implementa el contrato, no rediseña ni rellena huecos`.

Paquete final deberá contener:
- fuentes canónicas;
- reconciliaciones finales;
- matrices;
- cierres de auditoría;
- contrato global;
- contratos por bloque;
- runtime base aprobado;
- invariantes 329/17/787;
- persistencia/save-load;
- gates/permisos;
- NPC/anclajes;
- tests obligatorios;
- canon negativo;
- lista explícita de cosas que Codex no puede inventar.

---

# 10. EXPERIMENTOS DE NPC — SEPARADOS DE PRODUCCIÓN

El laboratorio NPC NO está integrado al runtime canónico ver74/ver75.

Motor NPC Vivo v0.1.1:
`V011_APTO_PARA_GOAP`.

Commit experimental auditado:
`8249378a0c572799a051d8d024f8567f8fec63eb`.

PR #1 squash merge:
`404411f09c0e110f02c92689ffeb1a3c69a213ab`.

Resultado:
44 PASS, 0 FAIL + cinco stress tests de 10.000 casos PASS.

Arquitectura futura deseada:
`Utility AI → selecciona OBJETIVO → GOAP construye PLAN → Executor aplica/verifica → replanning si cambia el mundo`.

Ramas experimentales actuales verificadas:
- `experiment/motor-npc-v0.1.1` → `8249378a0c572799a051d8d024f8567f8fec63eb`;
- `experiment/motor-npc-v0.2-goap` → `552117cc3f01530d43e4523de8c7d41ec986373e`;
- `experiment/motor-npc-v0.3-memory` → `bcfe2cac1a0dc603f328583be569e6dae71ed9bb`;
- `experiment/npc-autonomous-loop-v0.1` → `ddff6e7b386b401ae1e471cbfe05f0bd113bb866`;
- `experiment/npc-executor-replanning-v0.1` → `fb7d4c415f269d22f50fa6f367501afe8bd4e094`;
- `experiment/npc-scheduler-v0.1` → `4b40619a78c134ea7526e4edfceb5dc84d433d4f`.

Regla de integración futura:
el cerebro NPC NO redefine canon. La capa canónica fija identidad, territorio, conocimiento, permisos, relaciones, responsabilidades y anclajes; Utility/GOAP/Executor sólo decide y ejecuta acciones válidas dentro de esas restricciones.

M16 es un futuro banco de prueba ideal para esa integración porque exige NPC autónomos actuando en frentes simultáneos.

**No mezclar los experimentos con la rama documental/producción mientras el laboratorio no esté cerrado y auditado.**

---

# 11. RAMAS Y SHAs CRÍTICOS

- baseline NPC/producción 3C.5: `grulla-blanca_ver74.html` SHA-256 `8cd2d2f5...59566`;
- `audit/3c6a-rev3-1` HEAD `0043af92b22d003e3ce4859a3556fd770ee1130d`;
- `contract/3c6-prologo-m01-m07` HEAD `b0d90ea70ab17b3d6a7e85951e19f00c7935c8f2`;
- `implement/3c6-prologo-m01-m07` HEAD `748bd4480e37fd2523fa833081b20522b9724dab` — REQUIERE CORRECCIONES;
- `audit/3c7a-fase1-rev2` snapshot de trabajo antes de este backup `f575a45f322575680f972e2313c1bfadbf73616d`.

---

# 12. ORDEN EXACTO DE CONTINUIDAD

Si un chat nuevo retoma el proyecto, proceder así:

1. Leer este backup.
2. NO tocar `main` ni mergear.
3. M16 ya está auditada y cerrada documentalmente; no crear REV2 salvo contradicción futura real.
4. M17 REV1 ya está preparada en `audit/3c9-m17-rev1`; enviar a Claude y procesar auditoría.
5. No avanzar M18 antes de procesar M17.
6. En paralelo, recuperar resultado pendiente de M08–M11 y cierre de implementación 3C.6.
7. No iniciar implementación global de 3C.7/3C.9 hasta que 3C.6 runtime pase y los contratos correspondientes estén cerrados.
8. Reconciliar M18/epílogo antes de preparar implementación global.
9. Cuando todo Arc1 esté cerrado y auditado, preparar paquete global para Codex e implementar por bloques.

---

# 13. PROHIBICIONES ACTIVAS

- No inventar canon faltante.
- No crear rooms nuevas para resolver documentos históricos ambiguos.
- No modificar `ROOMS.exits`.
- No abrir `PASO_PULSO` antes de su misión correspondiente.
- No confirmar R7/R10 prematuramente.
- No decidir LIBERAR/CUSTODIAR antes del tramo final.
- No convertir opcionales, atajos, únicos ecológicos, afinidad o skills en llaves ocultas obligatorias.
- No usar tiempo diegético/timers narrativos para progresión principal.
- No hacer que load complete progreso por entrar a una sala.
- No integrar Utility/GOAP/Executor en producción todavía.
- No modularizar antes de terminar 3C.10 y congelar HTML dorado.

---

# 14. ESTADO RESUMIDO

```text
3C.5 / ver74
→ APROBADO / baseline

3C.6A M01–M07 documental
→ CERRADO

3C.6 implementación ver75
→ REQUIERE CORRECCIONES (save/load)

M08–M11 REV2
→ preparada; falta cierre independiente

M12 + gate REV2
→ CERRADA / APTA PARA CONTRATO

M13–M15 REV2
→ CERRADA / APTA PARA CONTRATO

M16 REV1
→ CERRADA / APTA CON DECISIONES TÉCNICAS PENDIENTES

M17 REV1
→ LISTA PARA AUDITORÍA CLAUDE

M18+
→ NO INICIADO

Experimentos NPC
→ laboratorio separado; no integrado

Producción global Arc1
→ todavía bloqueada por 3C.6 runtime
```

---

# 15. SIGUIENTE ACCIÓN EXACTA

**Siguiente acción exacta: preparar/enviar el paquete autocontenido de M17 REV1 a Claude y procesar su auditoría.**

No avanzar M18. En paralelo siguen pendientes el cierre independiente de M08–M11 y la corrección/re-auditoría runtime de 3C.6.

---

**FIN DEL BACKUP MAESTRO DE CONTINUIDAD — 2026-09-25**


---

# 16. CORTE CONVERSACIONAL EXACTO — ANTES DE ABRIR CHAT NUEVO

Este bloque describe **exactamente dónde se interrumpió la conversación actual**.

## 16.1 Solicitud activa del usuario

El usuario pidió:

`dame el zip para claude`

referido a la auditoría externa de **3C.9 M17 REV1**.

Se comenzó a preparar el paquete autocontenido, pero **todavía NO se generó ni se entregó el ZIP final** en esta conversación.

Por lo tanto, un chat nuevo NO debe afirmar que el ZIP ya existe ni inventar un enlace.

## 16.2 Rama y snapshot actuales

Rama activa documental:

`audit/3c9-m17-rev1`

HEAD verificado al momento del corte:

`95dd57eb7f6a9638e561c1ac1597a2bdb164fa8b`

No tocar `main`. No mergear.

## 16.3 Archivos M17 exactos ya creados en GitHub

- `docs/3C9/Reconciliacion_3C9_M17_REV1.md`
  - Git blob SHA: `44d58c5511720efed885a39ee037bbab1dc20a87`

- `docs/3C9/Matriz_Implementacion_3C9_M17_REV1.json`
  - Git blob SHA: `e3a1e8b81c7f1b4642e1a42ea35114be067d4bbe`

- `docs/3C9/PROMPT_AUDITORIA_3C9_M17_REV1_CLAUDE.md`
  - Git blob SHA: `c7b0a7e0f2fcce81f88a9352273e11e80b89a9bc`

- `docs/3C9/fuentes/Fuente_Maestra_T290_M17_EXTRACTO.md`
  - Git blob SHA: `d8d9c7b8e38901bee6b9390939d5c744c8d135ab`

- `docs/3C9/fuentes/Fuente_Maestra_T257_M17_Tecnica_EXTRACTO.md`
  - Git blob SHA: `d66934716fc9e3eb2c608c3c4c089d6e95c5fa50`

- `docs/3C9/fuentes/Fuente_Maestra_T240_Nucleo_M17_EXTRACTO.md`
  - Git blob SHA: `4ea071b52049aff30faba3cccf88be2c1c3cbd66`

Todos fueron recuperados/validados en la conversación antes del corte.

## 16.4 Frontera M16 incluida para la auditoría M17

Archivos exactos disponibles:

- `docs/3C7A/CIERRE_3C7A_M16_REV1.md`
  - Git blob SHA: `44169fddf5696df51b6593cd38478439ac2e8be3`

- `docs/3C7A/Auditoria_3C7A_M16_REV1_CLAUDE.md`
  - Git blob SHA: `683ef81e735af8bffe99e04b1ff98bf92b8b21ec`

M16 está cerrada como:

`3C7A_M16_REV1_CERRADA_DOCUMENTALMENTE_APTA_CON_DECISION_TECNICA_PENDIENTE`

No reabrir M16 salvo contradicción futura real.

## 16.5 Fuentes pesadas ya localizadas/materializadas para el ZIP M17

En el entorno de trabajo de esta conversación se materializaron:

- Fuente Maestra completa:
  - archivo de biblioteca original: `La_Grulla_Blanca_Fuente_Maestra_Fusionada_ver55`
  - file_id: `file_00000000bfec820e96344b87bc3c3bee`
  - tamaño materializado: 11,148,866 bytes

- baseline:
  - `grulla-blanca_ver74.html`
  - file_id: `file_000000006d84820ea82d7204d14ffa5f`
  - tamaño: 1,650,510 bytes
  - SHA-256 canónico: `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

- Auditoría 6 canónica:
  - file_id: `file_00000000de1c81f4aff3a9f5d0aa884b`
  - tamaño materializado: 112,066 bytes

- Auditoría 6 estructurada:
  - `Auditoria_6_Misiones_M01_M18_Estructurada.json`
  - file_id: `file_00000000ed34820ea22c224316fcfcbd`
  - tamaño materializado: 101,815 bytes

Ruta temporal usada en esta conversación:

`/mnt/data/m17_claude_pkg/`

Un chat nuevo no debe depender de que esa ruta temporal siga existiendo; si no existe, rematerializar desde los file_id indicados.

## 16.6 Contenido esperado del ZIP autocontenido M17

El ZIP debe incluir como mínimo:

1. `00_PROMPT_CLAUDE_AUDITORIA_M17.md` o copia exacta/equivalente del prompt GitHub.
2. `README_PRIMERO.md`.
3. `VALIDACION_PAQUETE.md`.
4. `MANIFEST_SHA256.txt`.
5. `docs/3C9/Reconciliacion_3C9_M17_REV1.md`.
6. `docs/3C9/Matriz_Implementacion_3C9_M17_REV1.json`.
7. `docs/3C9/PROMPT_AUDITORIA_3C9_M17_REV1_CLAUDE.md`.
8. `docs/3C9/fuentes/Fuente_Maestra_T290_M17_EXTRACTO.md`.
9. `docs/3C9/fuentes/Fuente_Maestra_T257_M17_Tecnica_EXTRACTO.md`.
10. `docs/3C9/fuentes/Fuente_Maestra_T240_Nucleo_M17_EXTRACTO.md`.
11. Fuente Maestra completa.
12. Auditoría 6 canónica.
13. Auditoría 6 estructurada.
14. `grulla-blanca_ver74.html`.
15. `docs/3C7A/CIERRE_3C7A_M16_REV1.md`.
16. `docs/3C7A/Auditoria_3C7A_M16_REV1_CLAUDE.md`.

Puede incluir archivos adicionales de trazabilidad si ayudan, pero no sustituir las fuentes reales por índices/resúmenes.

## 16.7 Validaciones que faltaban hacer antes de entregar el ZIP

Antes de pasar el ZIP a Claude, el chat nuevo debe:

1. reconstruir/copiar los archivos exactos de GitHub usando el snapshot `95dd57eb7f6a9638e561c1ac1597a2bdb164fa8b`;
2. verificar que la matriz JSON parsea;
3. verificar SHA/blobs de los seis archivos M17 listados arriba;
4. verificar SHA-256 de `grulla-blanca_ver74.html`;
5. generar `MANIFEST_SHA256.txt` con todos los archivos;
6. generar `VALIDACION_PAQUETE.md` distinguiendo:
   - archivos GitHub byte-exact;
   - archivos completos de biblioteca materializados;
7. hacer `zipfile.testzip()` o validación equivalente;
8. calcular SHA-256 final del ZIP;
9. sólo entonces entregar enlace al usuario.

## 16.8 Qué debe auditar Claude en M17

El prompt ya creado exige revisar especialmente:

- M16 HECHA como única precondición;
- `arc1.estado=LIV_CRISIS` y no inventar `LIV_DESCENSO`;
- Consejo no-persuasivo;
- Ji Xueying preside y Qiao Ren autoriza;
- movilidad/anclaje de He Zhen, Lan Meihua y Song Rui;
- permiso `NUCLEO_PROFUNDO`;
- `GATES_329.PASO_PULSO` sin tocar `ROOMS.exits`;
- ruta física profunda room→room;
- R7 antes de R10;
- Centinela combate/protocolo equivalentes;
- legacy `centinela_pluma` de Alturas a sustituir;
- Sala de Relevo obligatoria/segura/no purificadora;
- Cámara de Memoria opcional;
- Comprensión +1 one-shot;
- idempotencia/save-load;
- frontera estricta M17→M18.

Dos puntos deben recibir veredicto explícito:

1. si `nucleo_camara_regulacion` como room candidata del Centinela es compatible o sobreespecificación;
2. si exigir llegada real a `nucleo_umbral_santuario` para cerrar M17 está respaldado por T290 o debe corregirse.

Veredictos permitidos:

`3C9_M17_REV1_APTA_PARA_CONTRATO`

`3C9_M17_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

`3C9_M17_REV1_REQUIERE_CORRECCIONES`

## 16.9 Mensaje sugerido para iniciar el próximo chat

```text
Usá el archivo BACKUP_MAESTRO_CONTINUIDAD_2026-09-25_CORTE_M17.md como estado actual del proyecto La Grulla Blanca.

No mezcles propuestas históricas con canon posterior.
No toques main.
No avances M18.
El frente activo es M17 REV1 en audit/3c9-m17-rev1.

La tarea inmediata es terminar el ZIP autocontenido de auditoría M17 para Claude siguiendo la sección 16 del backup, verificar integridad/hashes y darme el ZIP + el mensaje exacto para Claude.
```

## 16.10 Estado de cierre de esta conversación

```text
M01–M07 documental
→ CERRADO

3C.6 runtime ver75
→ REQUIERE CORRECCIÓN + REAUDITORÍA

M08–M11 REV2
→ falta cierre independiente

M12
→ CERRADA / APTA

M13–M15
→ CERRADAS / APTAS

M16
→ CERRADA / APTA CON DECISIONES TÉCNICAS PENDIENTES

M17 REV1
→ DOCUMENTACIÓN COMPLETA
→ PROMPT CLAUDE COMPLETO
→ ZIP CLAUDE EN PREPARACIÓN
→ ZIP FINAL TODAVÍA NO ENTREGADO

M18+
→ NO INICIADO

Experimentos NPC
→ separados de producción

Implementación global Arc1
→ esperar cierre total M01–última misión y luego paquete global para Codex
```

---

**FIN DEL CORTE CONVERSACIONAL EXACTO — 2026-09-25**
