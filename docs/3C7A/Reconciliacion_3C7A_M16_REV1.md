# Reconciliación 3C.7A — M16 · Cuando falla el centro — REV1

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_AUDITORIA_DOCUMENTAL`  
**Autoridad principal:** Fuente Maestra ver55, T281 (2026-09-20T07:31:21.863Z).  
**Autoridad histórica complementaria:** T260.  
**Apoyo técnico:** T257 (idempotencia), Auditoría 6, ver74/3C.5 para infraestructura.  
**Alcance:** activación M16, seis frentes, resolución determinista, EMERGENCIA_SECTA, responsables/NPC, consecuencias y cierre M16.  
**Fuera de alcance:** implementación, M17 completo, R7/R10, NUCLEO_PROFUNDO, LIBERAR/CUSTODIAR, balance numérico final.

> T281 es la revisión posterior específica de M16 y prevalece sobre T260 cuando exista diferencia.

## 1. Frontera de entrada

M16 no se activa en el mismo evento que cierra M15.

Frontera heredada:

`M15=HECHA`, `R9=CONFIRMADO`, `arc1.estado=LIV_REVELACION`, `PASO_PULSO=false`, `NUCLEO_PROFUNDO=false`.

M15 deja satisfecha la precondición `M16_EVENTO_INICIO_PENDIENTE_RECONCILIACION`.

## 2. Activación de M16

T281 exige un evento narrativo concreto posterior a M15: señales pequeñas casi simultáneas (Formaciones, caudal, fauna, heridos, Producción) seguidas de la certeza de que el centro está fallando.

Al dispararse una sola vez:

- `M16=ACTIVA`;
- `arc1.estado=LIV_CRISIS`;
- los seis frentes nacen `PENDIENTE`;
- `EMERGENCIA_SECTA=ACTIVA`.

REV1 **no congela todavía el gesto de UI/comando/room exacto que dispara el evento**. Debe cumplir simultáneamente:

- ser posterior y separado del cierre de M15;
- ser explícito/perceptible para el jugador;
- ser alcanzable sin RNG ni reloj;
- ser one-shot e idempotente;
- no depender de `entrarSala()` genérico;
- no depender de tiempo diegético.

Clasificación: `DECISION_TECNICA_PRECONTRATO`.

## 3. Estado único de los seis frentes

REV1 propone una sola fuente de verdad:

`flags.arc1.crisisM16.frentes[ID] = PENDIENTE | ESTABLE | COSTOSO | DAÑADO`.

IDs:

- `MEDICINA`;
- `RUTAS`;
- `FORMACIONES`;
- `RECURSOS`;
- `SAUCES`;
- `JARDINES`.

Los booleanos históricos `crisis_<frente>_resuelta` se derivan de `estado != PENDIENTE`; no se persisten como segunda fuente de verdad.

Clasificación: `RECONCILIACION_ESTRUCTURAL_3C7_AUDITAR`, coherente con estados enumerados e idempotencia.

No existe estado `FALLIDO` para un frente.

## 4. Semántica de resultados

`ESTABLE`: la función esencial se conserva con daños menores.

`COSTOSO`: la función esencial se conserva con pérdida real de reservas, capacidad o infraestructura.

`DAÑADO`: existen consecuencias serias y persistentes para el epílogo, pero la función mínima necesaria para continuar Arc1 queda garantizada.

Invariante absoluto:

`frente=DAÑADO` nunca puede bloquear M17, Fundación/ZhuJi, una receta obligatoria ni una llave de progreso.

No existe resultado perfecto global. Incluso con máxima preparación debe quedar evidencia de crisis: heridos, desgaste, daños menores o interrupciones.

## 5. Resolución determinista

Cada frente consulta factores semánticos:

- `RESPONSABLE`;
- `PREPARACION`;
- `APOYO`;
- `INTERVENCION`.

Puede usar infraestructura/requisiciones/atajos/compañeros como entradas semánticas, pero el macroresultado no depende de RNG.

`resolverFrente(id)` debe fijar el resultado una sola vez. Una segunda llamada devuelve exactamente el estado ya fijado.

Los modificadores entre frentes son de resiliencia, nunca dependencias absolutas. Cada frente puede recibir como máximo uno o dos apoyos externos importantes.

Ejemplos permitidos:

- RECURSOS puede ayudar a MEDICINA o FORMACIONES;
- RUTAS puede ayudar a SAUCES o transporte de RECURSOS;
- FORMACIONES puede aliviar JARDINES/SAUCES.

Prohibido un dominó determinista del tipo `RUTAS DAÑADO => MEDICINA DAÑADO => SAUCES DAÑADO`.

## 6. Intervención del jugador

M16 no muestra seis quests ni un contador visible `2/2`.

`intervencionesJugador` puede existir internamente como conjunto persistente de frentes en los que el jugador completó una intervención principal reconocible.

Entrar a una región no cuenta como intervención.

T281 espera normalmente aproximadamente dos intervenciones principales, en secuencias pequeñas de 2–4 objetivos. REV1 no congela una cardinalidad rígida `exactamente 2` hasta auditoría técnica.

Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`.

Después de la fase de intervención personal, los frentes restantes se resuelven mediante responsables, preparación, apoyo e infraestructura.

## 7. Compañeros

Regla estricta: los compañeros no son unidades asignables por el jugador.

No existe UI `ASIGNAR COMPAÑERO A FRENTE`.

Cada compañero puede adquirir como máximo una asignación de crisis mediante transición narrativa justificada y one-shot.

Asignaciones naturales, no rígidas:

- Lin Yue → RUTAS;
- Han Qiao → RECURSOS;
- Zhao Wen → FORMACIONES;
- Mei Lian → SAUCES o MEDICINA;
- Guo Chen → RECURSOS o RUTAS;
- Luo Yan → FORMACIONES/coordinación.

La trayectoria previa y disponibilidad pueden cambiar la asignación. Afinidad no controla su autonomía básica.

No teletransportación silenciosa: el movimiento exacto queda subordinado a las reglas de movilidad auditadas y a eventos explícitos.

## 8. Responsables y anclajes M16

Responsables canónicos de T281/Auditoría 6:

- MEDICINA: Lan Meihua, con Chen Bo y Yao Fen;
- RUTAS: Jiang Rui, con Ren Bo;
- FORMACIONES: He Zhen, con Wen Tao;
- RECURSOS: Duan Shibo, Ma Qiren y Lu Cheng;
- SAUCES: Xu An + apoyo local;
- JARDINES: Su Lian.

Durante M16 los responsables necesarios quedan anclados a su frente o territorio funcional y no deambulan aleatoriamente.

Las rutas exactas de emergencia y transición de NPC no se congelan en este documento.

## 9. Mapeo de infraestructura ver74

Estas rooms son **anclajes técnicos candidatos**, no checklists obligatorias.

### MEDICINA

`sala_recuperacion`, `sala_tratamientos`, `consultorio_meridianos`, `botica`.

El frente trata circulación irregular, saturación y suministros; no epidemia nueva. Examen/Alquimia pueden abrir opciones, nunca ser requisito obligatorio.

### RUTAS

`puesto_valle`, `patio_puesto_valle`, `bosque_refugio_patrulla` y segmentos existentes de la red territorial.

Puede incluir combate contextual, rescate, mensajería o reapertura de corredor; nunca `mata N criaturas` como objetivo central.

### FORMACIONES

`formaciones_sala_control`, `formaciones_camara_central`, `formaciones_sala_regulacion` y nodos existentes.

El objetivo es aislar/reglar sobrecompensaciones usando conocimiento de Dos Alas/Primera Ala; `DAÑADO` nunca vuelve Núcleo inaccesible.

### RECURSOS

`oficina_logistica`, `almacen_materiales`, `taller_lu_cheng` y dependencias de Producción existentes.

El problema es priorización/distribución bajo escasez relativa, no entregar un número fijo de materiales.

### SAUCES

`sauces_casa_comunal`, `sauces_plaza`, `sauces_canal_bajo`, `sauces_huertos`.

El frente es hídrico/comunitario. Sauces no desaparece y no se transforma en zona de combate aleatorio.

### JARDINES

`patio_jardineros`, `bancal_central`, `canal_principal`, `estanque_riego`, `conducto_antiguo_jardines`.

Herboristería y el atajo de Jardines pueden ayudar, pero no ser requisito. Ningún resultado elimina ingredientes indispensables para progresión.

## 10. Atajos de Primera Ala

Los seis atajos pueden aportar resiliencia o movilidad a uno o dos frentes.

Ningún frente exige un atajo específico.

6/6 atajos no produce crisis perfecta ni todos los frentes ESTABLE.

## 11. EMERGENCIA_SECTA

Permiso temporal activado al comenzar M16 y expirado al cerrarla.

Solo puede autorizar conexiones que declaren explícitamente aceptar emergencia.

No sustituye ni concede:

- `ARCHIVO_RESTRINGIDO`;
- `PRIMERA_ALA_INVESTIGACION`;
- `NUCLEO_PROFUNDO`;
- ni abre barreras físicas por sí misma.

El modelo persistente exacto debe alinearse con la decisión global de permisos de 3C.7.

## 12. Presentación y prioridad de eventos

La crisis se comunica mediante mundo, mensajes, NPC y variantes de rooms; no mediante tablero de porcentajes.

Prioridad conceptual durante M16:

`CRISIS > MISION_PRINCIPAL > PERSONAL_NO_URGENTE > AMBIENTAL`.

Escenas personales directamente ligadas a la crisis permanecen; escenas tranquilas no urgentes se posponen.

## 13. HISTORY y recompensas

M16 no concede Comprensión.

Recompensa cualitativa:

- Mérito extraordinario/importante por la misión completa;
- Contribución posible y secundaria;
- Prestigio sectorial según acciones conocidas.

No atender un frente no penaliza Prestigio automáticamente.

Registrar como HISTORY al menos la primera prioridad personal (`M16_PRIORIDAD_PRIMERA` o forma semántica equivalente). La segunda intervención puede registrarse como historia general sin convertir los seis frentes en puntuación.

Valores numéricos: `PENDIENTE_BALANCE_3C7`.

## 14. Cierre M16

Condición única:

`todos los frentes != PENDIENTE`.

Al cerrar one-shot:

- `M16=HECHA`;
- `EMERGENCIA_SECTA=EXPIRADA`;
- estabilización provisional registrada;
- `M17=DISPONIBLE` derivada;
- `arc1.estado` permanece `LIV_CRISIS` hasta la transición propia de M17.

Invariante de test:

`M16=HECHA => ningún frente=PENDIENTE`.

M16 no abre `NUCLEO_PROFUNDO`, no abre `PASO_PULSO`, no confirma R7 ni R10 y no decide LIBERAR/CUSTODIAR.

## 15. Idempotencia y save/load

Save/load no debe:

- disparar el evento inicial;
- cambiar una asignación de compañero ya fijada;
- resolver un frente;
- recalcular un resultado terminal;
- volver a activar EMERGENCIA_SECTA tras M16 HECHA;
- volver a pagar recompensas;
- activar M17 más allá de la disponibilidad derivada.

Los resultados terminales de cada frente deben preservarse exactamente.

## 16. Pendientes antes de contrato

1. definir el disparador concreto posterior a M15 que activa M16;
2. auditar cardinalidad/fases exactas de intervención personal sin contador visible;
3. fijar evaluadores semánticos concretos por frente sin convertirlos en sumas secretas;
4. fijar qué conexiones aceptan `EMERGENCIA_SECTA`;
5. reconciliar el modelo uniforme global de permisos;
6. auditar anclajes y rutas de emergencia contra movilidad vigente;
7. balance numérico de Mérito/Contribución/Prestigio;
8. congelar runtime predecesor sólo después del PASS de 3C.6 y contratos previos.

## Estado final

`3C7A_M16_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`

**NO IMPLEMENTAR TODAVÍA. NO AVANZAR M17.**
