# Prompt de auditoría externa — 3C.7A M12 + gate LIII→LIV REV1

Auditá de forma independiente la reconciliación documental M12 + gate LIII→LIV de `La Grulla Blanca`.

Trabajá en **modo solo lectura**. No modifiques archivos, no crees ramas, no hagas commits, no hagas merge y no implementes 3C.7.

Repositorio: `Shein25/La-Grulla-Blanca`
Rama: `audit/3c7a-fase1-rev2`
HEAD exacto: será suministrado externamente al ejecutar esta auditoría; verificá que trabajás sobre ese HEAD.

## Jerarquía de autoridad

1. decisiones humanas posteriores explícitas;
2. Fuente Maestra ver55, especialmente T288 para M08–M12;
3. T257 sólo como apoyo técnico/idempotencia donde T288 no lo contradiga;
4. Auditoría 6 canónica/estructurada;
5. Fase1 REV2 como recuperación derivada;
6. ver74/3C.5 únicamente para infraestructura real, rooms, scenery, gates, comandos y NPC existentes;
7. topología 329 congelada.

**T288 es posterior a T254 y T257. Si hay una diferencia real, no combines ambas versiones: clasificá qué formulación queda supersedida.**

## Archivos principales

- `docs/3C7A/Reconciliacion_3C7A_M12_Gate_LIII_LIV_REV1.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M12_Gate_LIII_LIV_REV1.json`
- `docs/3C7A/fuentes/Fuente_Maestra_T288_M12_Gate_EXTRACTO.md`
- `docs/3C7A/fuentes/Fuente_Maestra_T257_M12_Tecnica_EXTRACTO.md`
- `docs/3C7A/Auditoria_3C7A_M08_M15_FASE1_REV2.md`
- `docs/3C7A/Matriz_3C7A_M08_M15_FASE1_REV2.json`
- `docs/3C7A/Reconciliacion_3C7A_M08_M11_REV2.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M08_M11_REV2.json`
- `grulla-blanca_ver74.html`

El candidato runtime 3C.6/ver75 está en auditoría/corrección separada. No lo uses como autoridad canónica.

## A. Corregir o confirmar H-08

Comprobá en la fuente primaria si la REV1 resuelve correctamente la aparente contradicción `SUFICIENTE` vs `CONCLUYENTE`.

Verificá específicamente que:
- `SUFICIENTE` sea válido para progreso y para reconstruir el protocolo del Custodio;
- M12 no se marque HECHA sólo por llegar a SUFICIENTE;
- la confirmación definitiva de la red deje `evidenciaPrimeraAla=CONCLUYENTE` antes o en el mismo evento de cierre;
- no haga falta reabrir o continuar una M12 ya HECHA para poder cruzar el gate.

## B. Tres gates

Confirmá que REV1 no mezcle:
- `GATES_329.M12`: entrada oficial Formaciones→Primera Ala;
- gate de cultivo LIII→LIV: transición de etapa 3→4;
- `GATES_329.PASO_MANTENIMIENTO`: acceso físico a M13.

Verificá en ver74 los extremos reales de los gates y que no se modifique `ROOMS.exits`.

## C. Evidencia de Primera Ala

Auditá `evaluarEvidenciaPrimeraAla()` como contrato documental, no como código.

Comprobá que:
- sea semántico, no un contador visible de rooms/ramas;
- preserve la prohibición de exigir 6/6;
- `NUDO_INTERPRETADO` y `DOS_ALAS_ARQUITECTURA` tengan anclajes razonables en scenery existente;
- `PATRON_RAMA` no haya fijado un número de ramas que la fuente no fija;
- `CONEXION_SUPERFICIE` sea corroboración opcional y no exija abrir un atajo;
- una resolución terminal del Custodio pueda actuar como corroboración central sólo si la fuente lo permite;
- cada nueva evidencia actualice el evaluador en el mismo evento, sin depender de cambio de sala/save-load.

Si el umbral propuesto `SUFICIENTE = NUDO + DOS_ALAS + PATRON_RAMA` es demasiado específico para la fuente, no inventes otro: marcá exactamente qué parte debe quedar parametrizable.

## D. Atajos

Confirmá que los seis `ATAJO_ALA_*` son opcionales para M12 y para LIII→LIV, que pueden abrirse individualmente desde Primera Ala y que cerrar M12 no los abre automáticamente.

## E. Custodio de las Dos Alas

Auditá el contrato:
- estados únicos `NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`;
- COMBATE y PROTOCOLO equivalentes para cerrar misión;
- PROTOCOLO requiere M11 + evidencia suficiente, no 6 atajos/14 secretos/único/Afinidad alta;
- perder, huir o morir no resuelve; debe poder reintentarse;
- no hay llave/reliquia ni mejor premio exclusivo por combate;
- `ala_camara_dos_alas` como localización es elección técnica a auditar, no canon automático.

Las fuentes históricas mencionan controles laterales, pero la topología congelada no contiene `ala_control_este/oeste`. **No propongas crear rooms nuevas.** Verificá si el protocolo puede expresarse mediante scenery/acciones contextuales en la Cámara actual o si necesita decisión humana/técnica posterior.

## F. Cierre de M12

Comprobá el contrato:
`evidenciaPrimeraAla=CONCLUYENTE + Custodio terminal` → M12 HECHA, R5 CONFIRMADO, +1 Comprensión one-shot `ARC1_M12_RED_PRIMERA_ALA`, Primera Ala confirmada, umbral de Mantenimiento conocido.

Confirmá que `PASO_MANTENIMIENTO` permanezca cerrado hasta M13.

## G. Autorización institucional

REV1 reconcilia T257 `autorizacionInvestigacionProfunda` con la autorización institucional requerida por T288 y propone conceder `AUTORIZACION_INVESTIGACION_PROFUNDA` al cierre formal de M12.

Determiná si esta reconciliación es:
- `RESPALDADA_POR_FUENTE`;
- `ELECCION_TECNICA_COMPATIBLE`;
- `DECISION_HUMANA_REQUERIDA`;
- o `CONTRADICCION`.

No inventes un NPC emisor si la fuente no lo congela.

## H. Dos Alas

REV1 no crea un nuevo estado persistente `COMPRENDIDAS`. Verificá si es correcto derivar «Dos Alas comprendidas» de M11 HECHA + R3 CONFIRMADO + `sintesis.DOS_ALAS=PRINCIPIO`, dado que T288 expresa el gate posterior mediante M11/R3.

Si una fuente posterior obliga a un valor persistente distinto, citála y explicá por qué.

## I. Gate LIII→LIV

Auditá la fórmula de autoridad más reciente recuperada de T288:
`qi>=75 + M11=HECHA + M12=HECHA + R3=CONFIRMADO + R5=CONFIRMADO + autorización institucional correspondiente`.

Comprobá además los invariantes derivados de estados válidos y que no se esté duplicando información innecesariamente.

Contrastá con el legacy real de ver74: `PUERTAS[4] = 2 píldoras + comprensión:6`. Clasificá su sustitución como deuda esperada o contradicción según las fuentes.

La futura 3C.7 no debe dejar una doble puerta ni consumir las dos píldoras legacy al pasar 3→4.

## J. Persistencia y permisos

Auditá que el estado propuesto permanezca bajo `flags.arc1` y `this.quests`, sin claves top-level.

El modelo uniforme de permisos (boolean + metadatos o objeto estructurado) está marcado como pendiente antes de contrato. No lo penalices como fallo si realmente puede permanecer abierto en esta etapa documental; sí señalá cualquier incompatibilidad con saves/schema 2.

## K. Canon negativo

Confirmá que M12 no vuelva a depender de:
- `reliquias_verticales`;
- Sombra/Centinela como llaves;
- 6/6 atajos;
- únicos ecológicos;
- Afinidad alta;
- todos los secretos;
- todas las rooms;
- acceso prematuro a Mantenimiento/M13.

## Entrega

Entregá un informe conceptualmente llamado `Auditoria_Cierre_3C7A_M12_Gate_REV1_CLAUDE.md` con:

1. hallazgos por gravedad: BLOQUEANTE / ALTA / MEDIA / BAJA;
2. tabla de requisitos de M12 con PASS / FAIL / DECISION_HUMANA_REQUERIDA / NO_VERIFICADO;
3. tabla específica del evaluador de evidencia;
4. tabla específica del Custodio COMBATE/PROTOCOLO;
5. tabla del gate LIII→LIV;
6. compatibilidad con topología/gates ver74;
7. persistencia, idempotencia y riesgos de soft-lock;
8. lista de cualquier canon inventado o de cualquier decisión técnica correctamente etiquetada;
9. lista exacta y mínima de correcciones, sólo si son necesarias.

Usá exactamente uno de estos veredictos:

`3C7A_M12_GATE_REV1_APTA_PARA_CONTRATO`

`3C7A_M12_GATE_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

`3C7A_M12_GATE_REV1_REQUIERE_CORRECCIONES`

No implementes las correcciones. No avances M13.
