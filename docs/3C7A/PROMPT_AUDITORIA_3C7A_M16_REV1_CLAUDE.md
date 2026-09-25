# Prompt de auditoría externa — 3C.7A M16 REV1

Auditá de forma independiente la reconciliación documental de **M16 · Cuando falla el centro**.

Trabajá en modo **solo lectura**. No modifiques archivos, no implementes, no crees ramas, no hagas commits y no avances M17.

## Jerarquía de autoridad

1. decisiones humanas posteriores explícitas;
2. Fuente Maestra ver55 **T281** como autoridad principal específica de M16;
3. T260 como versión histórica complementaria; T281 prevalece si difiere;
4. T257 para idempotencia/estructura;
5. Auditoría 6 canónica/estructurada;
6. ver74/3C.5 para infraestructura física y NPC;
7. topología 329 congelada.

## Archivos principales

- `docs/3C7A/Reconciliacion_3C7A_M16_REV1.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M16_REV1.json`
- `docs/3C7A/fuentes/Fuente_Maestra_T281_M16_EXTRACTO.md`
- Fuente Maestra ver55 completa, T281 y T260;
- `docs/3C7A/fuentes/Auditoria_6_Misiones_M01_M18_CANONICA.md`;
- `docs/3C7A/fuentes/Auditoria_6_Misiones_M01_M18_Estructurada.json`;
- `grulla-blanca_ver74.html`;
- cierres M15 REV2 como frontera previa.

## A. Activación M16

Comprobá que REV1 respete:
- M15 se cierra antes;
- M16 NO se activa en el mismo evento;
- el inicio consiste en señales casi simultáneas + certeza del fallo central;
- al activarse: `M16=ACTIVA`, `arc1.estado=LIV_CRISIS`, seis frentes PENDIENTE y `EMERGENCIA_SECTA=ACTIVA`;
- no usa tiempo diegético, RNG, `setTimeout` narrativo ni `entrarSala()` genérico.

REV1 deja el disparador exacto como `DECISION_TECNICA_PRECONTRATO`. Determiná si es una pendiente aceptable o si T281 ya obliga a un gesto concreto.

## B. Fuente única de verdad de los frentes

REV1 reemplaza la persistencia paralela de seis booleanos `crisis_<frente>_resuelta` por:

`flags.arc1.crisisM16.frentes[ID] = PENDIENTE | ESTABLE | COSTOSO | DAÑADO`

y deriva `resuelta` de `estado != PENDIENTE`.

Auditá si esta reconciliación estructural:
- preserva completamente T281/Auditoría 6;
- evita duplicación;
- respeta la regla de estados enumerados;
- mantiene el invariante `M16 HECHA => ningún frente PENDIENTE`.

Clasificala como `RESPALDADA`, `ELECCION_TECNICA_COMPATIBLE`, `DECISION_HUMANA_REQUERIDA` o `CONTRADICCION`.

## C. Seis frentes

Auditá por separado MEDICINA, RUTAS, FORMACIONES, RECURSOS, SAUCES y JARDINES.

Para cada uno verificá:
- problema concreto;
- responsable/NPC;
- preparación/apoyo;
- rooms candidatas reales en ver74;
- que esas rooms no se hayan convertido en checklist obligatoria;
- consecuencias ESTABLE/COSTOSO/DAÑADO;
- ausencia de soft-lock.

Confirmá especialmente:
- Medicina no exige Alquimia/Examen;
- Rutas no se reduce a matar mobs;
- Formaciones DAÑADO no bloquea Núcleo/M17;
- Recursos no es una fetch quest fija;
- Sauces nunca desaparece ni se vuelve zona de combate aleatorio;
- Jardines no puede eliminar ingredientes obligatorios de progresión.

## D. Resolución determinista

Comprobá el modelo semántico:
`RESPONSABLE + PREPARACION + APOYO + INTERVENCION`.

El macroresultado no usa RNG.

`resolverFrente()` es one-shot e idempotente.

La interdependencia entre frentes debe ser moderada: máximo uno o dos modificadores externos importantes por frente y nunca dominó obligatorio de resultados DAÑADO.

Decidí si REV1 endurece o flexibiliza indebidamente T281.

## E. Intervención personal

T281 habla de aproximadamente dos intervenciones principales y secuencias de 2–4 objetivos, sin contador visible.

REV1 persiste un set de frentes intervenidos pero NO congela `exactamente 2`.

Auditá si esta decisión es fiel a T281 y si puede evitar:
- que el jugador resuelva seis frentes corriendo;
- un contador visible 2/2;
- soft-lock por cantidad rígida mal alcanzada.

## F. Compañeros

Confirmá que:
- no son unidades asignables por el jugador;
- Afinidad no controla su autonomía básica;
- su asignación de crisis es one-shot;
- la trayectoria previa puede cambiar destino;
- no existe teletransportación silenciosa;
- las asignaciones Lin/Rutas, Han/Recursos, Zhao/Formaciones, Mei/Sauces-Medicina, Guo/Recursos-Rutas, Luo/Formaciones-coordinación están correctamente tratadas como naturales/no rígidas.

Contrastá con la infraestructura/NPC de ver74 y, si corresponde, con fuentes de compañeros/movilidad sin expandir el alcance de M16.

## G. EMERGENCIA_SECTA

Auditá que sea permiso temporal y no llave universal.

Debe:
- activarse con M16;
- expirar al cerrar M16;
- funcionar sólo en conexiones que explícitamente acepten emergencia;
- no sustituir ARCHIVO_RESTRINGIDO;
- no sustituir PRIMERA_ALA_INVESTIGACION;
- no conceder NUCLEO_PROFUNDO;
- no abrir una barrera física por sí sola.

El modelo exacto de permisos puede quedar pendiente si está bien marcado.

## H. Atajos/opcionales

Confirmá que:
- los atajos pueden mejorar resiliencia/movilidad;
- ningún atajo es requisito;
- 6/6 no produce todos ESTABLE;
- únicos ecológicos, afinidad alta, requisiciones opcionales o habilidades opcionales no se vuelven puertas ocultas.

## I. Presentación, HISTORY y recompensas

Confirmá:
- no tablero porcentual de seis frentes;
- prioridad `CRISIS > misión principal > personal no urgente > ambiental` como regla técnica compatible;
- Comprensión M16 = 0;
- Mérito por misión, no +premio por cada frente estable;
- no atender un frente no penaliza Prestigio automáticamente;
- HISTORY puede registrar prioridad personal sin convertirla en puntuación moral.

## J. Cierre y frontera M17

M16 sólo puede quedar HECHA cuando todos los frentes sean terminales.

Al cerrar:
- EMERGENCIA_SECTA expira;
- M17 queda disponible;
- `arc1.estado` permanece `LIV_CRISIS` hasta M17;
- `PASO_PULSO=false`;
- `NUCLEO_PROFUNDO=false`;
- R7 y R10 no se confirman;
- no se decide LIBERAR/CUSTODIAR.

Verificá que ningún estado DAÑADO bloquee M17.

## K. Save/load e idempotencia

Comprobá que load no pueda:
- disparar M16;
- reasignar compañeros;
- resolver/recalcular frentes;
- reactivar EMERGENCIA tras cierre;
- repagar recompensas;
- activar M17 indebidamente.

## Entrega

Entregá:
1. hallazgos por gravedad `BLOQUEANTE / ALTA / MEDIA / BAJA`;
2. tabla por frente;
3. tabla de activación/fases/cierre;
4. tabla de persistencia/idempotencia;
5. tabla de compañeros/responsables;
6. decisiones técnicas compatibles vs canon inventado;
7. riesgos de soft-lock;
8. correcciones mínimas si son necesarias.

Usá exactamente uno de estos veredictos:

`3C7A_M16_REV1_APTA_PARA_CONTRATO`

`3C7A_M16_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

`3C7A_M16_REV1_REQUIERE_CORRECCIONES`

No implementes. No avances M17.
