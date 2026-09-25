# Prompt de auditoría externa — 3C.9 M17 REV1

Auditá de forma independiente la reconciliación documental de **M17 · Descender**.

Modo **solo lectura**. No modifiques archivos, no implementes, no crees ramas, no hagas merge y no avances M18.

## Jerarquía de autoridad

1. decisiones humanas posteriores explícitas;
2. Fuente Maestra ver55 **T290**, bloque M17, como autoridad principal;
3. T257 para transición/idempotencia;
4. T240 para topología y función de las 13 rooms del Núcleo;
5. T254/T222 para matriz narrativa/revelaciones;
6. Auditoría 6 canónica/estructurada;
7. ver74/3C.5 para infraestructura física, gates, NPC y legacy;
8. cierre documental de M16 como frontera previa.

Importante: T290 está marcado PARCIAL a nivel de turno completo porque contiene M17+M18, pero el bloque M17 recuperado es continuo hasta el encabezado de M18. No rellenes material faltante de M18.

## Archivos principales

- `docs/3C9/Reconciliacion_3C9_M17_REV1.md`
- `docs/3C9/Matriz_Implementacion_3C9_M17_REV1.json`
- `docs/3C9/fuentes/Fuente_Maestra_T290_M17_EXTRACTO.md`
- `docs/3C9/fuentes/Fuente_Maestra_T257_M17_Tecnica_EXTRACTO.md`
- `docs/3C9/fuentes/Fuente_Maestra_T240_Nucleo_M17_EXTRACTO.md`
- Fuente Maestra completa si está en el paquete;
- Auditoría 6;
- `grulla-blanca_ver74.html`;
- `docs/3C7A/CIERRE_3C7A_M16_REV1.md`.

## A. Frontera M16 → M17

Confirmá:
- `M16=HECHA` es la precondición;
- M17 comienza con `arc1.estado=LIV_CRISIS`;
- REV1 no inventa un nuevo macroestado `LIV_DESCENSO`;
- `EMERGENCIA_SECTA` ya está expirada y no abre Núcleo Profundo.

Si Auditoría 6 usa 'LIV_CRISIS/LIV_DESCENSO', determiná si debe leerse como etapa descriptiva y no como nuevo valor persistente, a la luz de T257 y de la máquina global de estados.

## B. Consejo y autorización

Auditá que la comparecencia:
- no sea juicio/persuasión;
- tenga a Ji Xueying presidiendo;
- Qiao Ren autorice la excepción;
- use R6/R8/R9 + M16 resuelta como contexto ya adquirido;
- produzca una sola vez `NUCLEO_PROFUNDO_AUTORIZADO`.

REV1 deja el gesto exacto de activación como `DECISION_TECNICA_3C9_AUDITAR`. Determiná si T290 obliga a un comando/room/evento más concreto.

Contrastá `interior_sala_consejo` con ver74.

### Movilidad

Revisá especialmente la presencia de He Zhen, Lan Meihua y Song Rui en la escena: T290 los hace relevantes, pero 3C.5 no fija su posición M17. Decidí si `DEPENDENCIA_MOVILIDAD_3C9_AUDITAR` es suficiente o si REV1 debe congelar una solución.

## C. Permiso y gate

Confirmá que `NUCLEO_PROFUNDO` sólo habilita:

`nucleo_archivo_promesa ↔ nucleo_descenso_pulso`

mediante `GATES_329.PASO_PULSO`, sin modificar `ROOMS.exits`.

Debe NO:
- abrir todos los sellos;
- dar autoridad total sobre el Núcleo;
- reactivar EMERGENCIA_SECTA;
- iniciar M18.

Auditá la compatibilidad con el modelo uniforme de permisos todavía pendiente.

## D. Ruta física

Verificá contra ver74, room por room:

`nucleo_archivo_promesa → nucleo_descenso_pulso → nucleo_galeria_pulso → nucleo_camara_regulacion → nucleo_sala_relevo → nucleo_exterior_ancla → nucleo_umbral_santuario`

y la rama opcional:

`nucleo_exterior_ancla ↔ nucleo_camara_memoria`.

Confirmá que `nucleo_santuario_vinculo` queda fuera de M17 y pertenece a M18.

## E. R7 antes de R10

Ésta debe ser una regla congelada.

Auditá que:
- R7 = dependencia de entidad viva;
- NO significa todavía 'la Grulla está viva';
- se garantiza por Galería/Cámara de Regulación;
- la fuente primaria de lógica es conocimiento real y R7 es auditoría narrativa;
- no depende de contenido opcional.

Después auditá R10:
- ocurre después de R7;
- se confirma en Exterior del Ancla;
- demuestra que es la misma Grulla del pacto original;
- no descendiente, sucesora, copia, eco ni representación;
- tampoco depende de Cámara de la Memoria.

## F. Centinela de Plumas Petrificadas

Confirmá el contrato narrativo:
- después de R7;
- antes de Sala de Relevo;
- combate o protocolo equivalentes;
- protocolo usa conocimiento principal M14–M15;
- sin secretos/6 atajos/afinidad/loot previo;
- sin reliquia;
- sin Pluma Celeste;
- sin cadáver/restos examinables.

### Dos decisiones técnicas a auditar

1. REV1 propone un enum:
`NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`.

Clasificalo como `RESPALDADA`, `ELECCION_TECNICA_COMPATIBLE`, `DECISION_HUMANA_REQUERIDA` o `CONTRADICCION`.

2. T290 no da room_id literal. REV1 propone `nucleo_camara_regulacion` como ubicación candidata, bloqueando el avance hacia Sala de Relevo.

Auditá si esa room es la mejor lectura de topología/fuente o si es sobreespecificación. No inventes una room alternativa si la fuente no la fija.

### Legacy ver74

Verificá expresamente que ver74 todavía coloca `centinela_pluma` en `alturas_mirador_grulla`, con loot/tratamiento de restos y lógica histórica de `reliquia_pluma`.

Determiná si marcar todo esto `LEGACY_A_REEMPLAZAR_3C9` es correcto y si existe algún otro punto legacy que la REV1 haya omitido.

Debe quedar prohibido que existan dos Centinelas únicos simultáneamente.

## G. Sala de Relevo

Confirmá:
- room real `nucleo_sala_relevo`;
- alojamiento existente en ver74;
- obligatoria antes de M18;
- segura;
- no purifica;
- se conoce al entrar mediante movimiento real;
- load no puede simular ese descubrimiento;
- no concede una nueva revelación obligatoria.

## H. Cámara de la Memoria

Debe ser opcional.

Confirmá que no sea fuente exclusiva de R7, R10, acceso M18 ni de la respuesta LIBERAR/CUSTODIAR.

## I. Comprensión

Confirmá:
`Comprensión +1`, fuente `ARC1_M17_DEPENDENCIA_VIVA`, una sola vez cuando R7+R10 quedan integrados.

Auditá que no pueda cobrarse dos veces por dos revelaciones o por repetir EXAMINAR/load.

## J. Cierre M17 — punto crítico de auditoría

REV1 exige:
- autorización;
- R7;
- Centinela terminal;
- Sala de Relevo conocida;
- R10;
- llegada real a `nucleo_umbral_santuario`.

T290 dice: 'cuando el jugador llega a la última antesala y R10 queda confirmado: M17=HECHA / M18=DISPONIBLE'.

Determiná expresamente si exigir `nucleo_umbral_santuario` como última antesala es:
`RESPALDADO_POR_T290`, `ELECCION_TECNICA_COMPATIBLE`, o `SOBREESPECIFICACION_A_CORREGIR`.

Este punto no debe quedar implícito.

Al cerrar:
- M17 HECHA;
- M18 disponible derivada;
- `arc1.estado=LIV_CRISIS`;
- NO volver al Consejo;
- NO entrar al Santuario automáticamente;
- NO iniciar combate;
- NO VINCULO_CEDIDO;
- NO LIBERAR/CUSTODIAR;
- NO EPILOGO/Gran Perfección.

## K. Compañeros

Confirmá que los seis compañeros NO bajen como party y que M17 no introduzca bonus obligatorios por Afinidad.

## L. Idempotencia/save-load

Auditá one-shot de:
- autorización;
- R7;
- Centinela;
- conocimiento real de Relevo;
- R10;
- Comprensión;
- cierre M17.

Y confirmá que cargar partida no pueda provocar ninguno de esos efectos.

Relacioná esto con el bug conocido de 3C.6 `deserializar()/entrarSala()` sólo como riesgo de implementación futuro; no lo uses para invalidar el documento si el contrato M17 lo prohíbe correctamente.

## M. Entrega

Entregá:
1. hallazgos `BLOQUEANTE / ALTA / MEDIA / BAJA`;
2. tabla de secuencia M17;
3. tabla R7/R10;
4. tabla Centinela canon vs legacy;
5. tabla gates/permisos;
6. tabla rooms/topología;
7. persistencia/idempotencia;
8. decisiones técnicas compatibles vs sobreespecificaciones;
9. riesgos de soft-lock;
10. correcciones mínimas.

Usá exactamente uno de estos veredictos:

`3C9_M17_REV1_APTA_PARA_CONTRATO`

`3C9_M17_REV1_APTA_CON_DECISION_TECNICA_PENDIENTE`

`3C9_M17_REV1_REQUIERE_CORRECCIONES`

No implementes. No avances M18.
