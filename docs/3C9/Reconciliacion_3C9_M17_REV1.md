# Reconciliación 3C.9 — M17 · Descender — REV1

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_AUDITORIA_DOCUMENTAL`  
**Autoridad principal:** Fuente Maestra ver55 T290, bloque recuperado de M17.  
**Apoyo técnico:** T257 (transiciones/idempotencia), T240 (Núcleo/topología), T254/T222 (matriz narrativa), Auditoría 6, ver74/3C.5.  
**Frontera previa:** M16 REV1 cerrada documentalmente.  
**Alcance:** M17 desde Consejo hasta Umbral del Santuario.  
**Fuera de alcance:** combate de la Grulla, LIBERAR/CUSTODIAR, M18, Gran Perfección, epílogo, balance final del Centinela.

> T290 está marcado como parcial a nivel de turno completo, pero el bloque recuperado de M17 llega de forma continua desde su encabezado hasta el inicio de M18. No se rellenan huecos posteriores de M18.

## 1. Precondición y estado macro

M17 queda disponible cuando:

`M16=HECHA`.

Al iniciar M17:

- `arc1.estado` permanece `LIV_CRISIS`;
- NO se crea un nuevo estado macro `LIV_DESCENSO`;
- `EMERGENCIA_SECTA` ya está expirada y no sirve como llave.

T257 permite expresamente que M17 comience dentro de `LIV_CRISIS` y recomienda no añadir otro estado macro.

## 2. Estructura obligatoria

Orden congelado:

`CONSEJO → AUTORIZACIÓN → DESCENSO → R7 DEPENDENCIA VIVA → CENTINELA → SALA DE RELEVO → R10 IDENTIDAD → UMBRAL → M17 HECHA`.

R7 debe ocurrir **antes** que R10.

M17 no inicia M18.

## 3. Consejo después de M16

La comparecencia no es un juicio ni un minijuego de persuasión.

Los hechos ya existen:

- R6 confirmado;
- R8 confirmado;
- R9 confirmado;
- M16 resuelta.

Ji Xueying preside.

Qiao Ren autoriza la excepción institucional.

He Zhen aporta la lectura de dependencia central.

Lan Meihua puede contextualizar los efectos orgánicos de M16.

Song Rui aporta la memoria documental del relevo.

### 3.1 Sala

La infraestructura canónica de ver74 contiene `interior_sala_consejo`; Ji Xueying está anclada allí y Qiao Ren dispone de ruta válida hasta esa sala.

### 3.2 Activación exacta

REV1 no congela si la comparecencia se activa mediante `HABLAR`, evento de convocatoria aceptado u otra interacción explícita.

Debe cumplir:

- M16 HECHA;
- ser perceptible y explícita;
- no dispararse por `entrarSala()` durante load;
- ser one-shot;
- no exigir persuasión ni afinidad.

Clasificación: `DECISION_TECNICA_3C9_AUDITAR`.

### 3.3 NPC relevantes vs. anclajes

Ji Xueying y Qiao Ren tienen soporte de movilidad/posición en ver74.

He Zhen, Lan Meihua y Song Rui son participantes/relevantes de la escena según T290, pero sus posiciones M17 no están cerradas en 3C.5. El contrato futuro debe resolver su presencia mediante anclaje temporal explícito, tránsito válido o representación por informe, sin teletransportación silenciosa.

Clasificación: `DEPENDENCIA_MOVILIDAD_3C9_AUDITAR`.

## 4. Autorización NUCLEO_PROFUNDO

El Consejo concede exactamente una vez:

`NUCLEO_PROFUNDO_AUTORIZADO`.

Semántica del permiso:

`NUCLEO_PROFUNDO { fuente=ORDEN, origen=M17, activa=true }`.

El shape exacto depende del modelo uniforme global de permisos aún pendiente.

Efecto físico asociado:

`GATES_329.PASO_PULSO = true`.

`PASO_PULSO` conecta exclusivamente:

`nucleo_archivo_promesa ↔ nucleo_descenso_pulso`.

El permiso NO:

- abre todos los sellos;
- concede autoridad general sobre el Núcleo;
- reactiva `EMERGENCIA_SECTA`;
- abre el Santuario por una llave independiente;
- cambia `ROOMS.exits`.

## 5. Ruta física del Núcleo profundo

Topología verificada en ver74/T240:

`nucleo_archivo_promesa`
`↓`
`nucleo_descenso_pulso`
`↓`
`nucleo_galeria_pulso`
`→ nucleo_camara_regulacion`
`→ nucleo_sala_relevo`
`→ nucleo_exterior_ancla`

Desde `nucleo_exterior_ancla`:

- oeste → `nucleo_camara_memoria` (opcional);
- norte → `nucleo_umbral_santuario`;
- norte desde el Umbral → `nucleo_santuario_vinculo` (M18).

No se modifica ninguna conexión.

## 6. Descenso del Pulso

`nucleo_descenso_pulso` introduce ritmo, vibración, presión, luz/resonancia y respuesta central.

No confirma R7 por sí solo.

No usa la palabra 'corazón' como explicación mecánica literal.

Su función es preparar la transición de infraestructura histórica a actividad presente.

## 7. R7 — dependencia viva

Orden narrativo obligatorio:

`R7 antes de R10`.

Fuente primaria de lógica:

`conocimiento.nucleo.dependenciaViva = CONFIRMADO`.

Auditoría narrativa asociada:

`R7 = CONFIRMADO`.

R7 debe quedar garantizado por la ruta principal en `nucleo_galeria_pulso` / `nucleo_camara_regulacion`.

La prueba debe demostrar:

- respuesta no puramente mecánica;
- regulación dinámica;
- recuperación/variación compatible con actividad viva;
- la red recibe/amplifica una respuesta orgánica en vez de generar toda la regulación por sí sola.

El trigger exacto de evidencias/EXAMINAR no se congela en REV1.

Clasificación: `ELECCION_TECNICA_3C9_AUDITAR`.

R7 NO puede depender de Cámara de la Memoria, secretos, atajos, únicos opcionales ni skill opcional.

## 8. Centinela de Plumas Petrificadas

Debe ocurrir después de R7 y antes de alcanzar la Sala de Relevo.

Identidad técnica reutilizable:

`centinela_pluma`.

Resoluciones equivalentes:

- COMBATE;
- PROTOCOLO basado en conocimiento principal de M14–M15.

No exige:

- secretos opcionales;
- seis atajos;
- afinidad;
- loot previo.

Al resolverlo:

- no produce reliquia;
- no produce cadáver/restos examinables;
- no produce Pluma Celeste;
- no abre historia por loot.

### 8.1 Estado propuesto

`flags.arc1.centinelaPluma = NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`.

Clasificación: `ELECCION_TECNICA_3C9_AUDITAR`.

### 8.2 Ubicación exacta

T290 congela su posición narrativa como transición entre infraestructura profunda y sector de relevo, pero no proporciona room_id literal.

REV1 propone como candidato:

`nucleo_camara_regulacion` bloqueando el avance norte hacia `nucleo_sala_relevo` mientras siga `NO_RESUELTO`.

Clasificación: `ELECCION_TECNICA_RESPALDADA_POR_TOPOLOGIA_A_AUDITAR`.

No crear una room nueva ni modificar `ROOMS.exits`.

### 8.3 Legacy ver74 a sustituir

ver74 todavía contiene:

- `centinela_pluma` en `alturas_mirador_grulla`;
- perfil de combate legacy;
- loot normal;
- tratamiento posterior como `restos` examinables;
- lógica histórica que puede conceder `reliquia_pluma` al derrotarlo.

Todo ese uso como llave/material del final es:

`LEGACY_A_REEMPLAZAR_3C9`.

El contrato de implementación deberá reutilizar o migrar la identidad sin mantener dos Centinelas únicos simultáneos.

## 9. Sala de Relevo del Ancla

`nucleo_sala_relevo` es obligatoria antes de M18.

ver74 ya la contiene como uno de los 13 alojamientos.

Contrato:

- `seguro=true`;
- `purifica=false`;
- conocida automáticamente al alcanzarla mediante movimiento real;
- permite descanso/preparación según sistema de alojamiento;
- permanece último refugio estable antes del tramo final.

Save/load no debe marcarla conocida por materialización artificial de sala.

La Sala cuenta historia del relevo, pero NO concede una nueva R obligatoria.

## 10. R10 — misma Grulla original

R10 ocurre después de R7.

Room principal:

`nucleo_exterior_ancla`.

Fuente primaria de lógica:

`conocimiento.nucleo.grullaViva = CONFIRMADO`.

Auditoría narrativa:

`R10 = CONFIRMADO`.

Debe quedar inequívoco que la entidad viva actual es la misma Grulla que participó en el pacto original:

- no descendiente;
- no sucesora;
- no copia;
- no eco;
- no representación.

La confirmación puede integrar firma/patrón/memoria del sistema, pero la ruta principal debe garantizarla sin exigir la Cámara de la Memoria.

## 11. Cámara de la Memoria

`nucleo_camara_memoria` es opcional.

Puede aportar contexto, recuerdos fragmentarios y humanidad al pacto.

Prohibido usarla como única fuente de:

- R7;
- R10;
- LIBERAR/CUSTODIAR;
- acceso a M18.

No debe declarar cuál decisión final es 'correcta'.

## 12. Comprensión M17

Recompensa one-shot:

`Comprensión +1`

`fuente = ARC1_M17_DEPENDENCIA_VIVA`.

Se concede cuando R7 y R10 quedan integrados, no +1 por cada revelación.

No se repaga al repetir EXAMINAR, volver a Exterior, entrar al Umbral o cargar partida.

Mérito/reconocimiento numérico queda `PENDIENTE_BALANCE_3C9`; Auditoría 6 lo describe cualitativamente como enorme y permite que parte del reconocimiento espere.

## 13. Cierre de M17

Condiciones mínimas:

- `M16=HECHA`;
- `NUCLEO_PROFUNDO_AUTORIZADO`;
- `R7=CONFIRMADO` por conocimiento real;
- Centinela terminal;
- `nucleo_sala_relevo` conocida;
- `R10=CONFIRMADO` por conocimiento real;
- llegada real a `nucleo_umbral_santuario`.

Al cerrar one-shot:

- `M17=HECHA`;
- M18 queda `DISPONIBLE` derivada;
- `arc1.estado` permanece `LIV_CRISIS`;
- Santuario queda como siguiente espacio narrativo;
- no se inicia combate;
- no se exige volver al Consejo.

La llegada al Umbral como condición de cierre sigue la formulación de T290: 'cuando el jugador llega a la última antesala y R10 queda confirmado'.

## 14. Frontera con M18

`nucleo_santuario_vinculo` pertenece a M18.

M17 NO:

- inicia combate al entrar;
- ejecuta `INTERVENIR`;
- produce `VINCULO_CEDIDO`;
- ofrece LIBERAR/CUSTODIAR;
- cambia a EPILOGO;
- concede Gran Perfección.

El primer ingreso al Santuario sólo puede ocurrir después de M17 HECHA y abre la escena de M18, no combate automático.

## 15. Compañeros

Los seis compañeros no descienden como party.

Pueden participar en preparación, Consejo, superficie o soporte.

El descenso profundo es principalmente del jugador por haber conectado personalmente la investigación, no porque sea 'el elegido'.

No crear asignación de party ni bonus obligatorio por afinidad.

## 16. Idempotencia/save-load

One-shot obligatorio:

- `NUCLEO_PROFUNDO_AUTORIZADO`;
- R7 primera confirmación;
- resolución Centinela;
- primer conocimiento real de Sala de Relevo;
- R10 primera confirmación;
- recompensa `ARC1_M17_DEPENDENCIA_VIVA`;
- `M17 → HECHA`.

Save/load no debe:

- convocar Consejo;
- conceder autorización;
- abrir PASO_PULSO;
- confirmar R7/R10;
- resolver Centinela;
- marcar Sala de Relevo conocida;
- cerrar M17;
- iniciar M18.

## 17. Tests obligatorios futuros

1. M16 no HECHA → M17 indisponible.
2. M16 HECHA → comparecencia disponible sin cambiar estado macro.
3. EMERGENCIA_SECTA no abre PASO_PULSO.
4. autorización abre sólo PASO_PULSO.
5. R10 no puede confirmarse antes de R7.
6. R7 no depende de contenido opcional.
7. protocolo del Centinela funciona sin secretos/atajos.
8. combate y protocolo producen mismo progreso narrativo.
9. Centinela no deja cadáver, restos, reliquia ni Pluma Celeste.
10. no existen dos Centinelas únicos simultáneos.
11. Sala de Relevo conocida antes de M17 HECHA.
12. Cámara de Memoria omitida → M17 sigue completable.
13. M17 HECHA → R7 y R10 confirmados.
14. llegar al Umbral no inicia M18/combate.
15. save/load en Consejo, antes/después R7, antes/después Centinela, Sala de Relevo, Exterior y Umbral no cambia progreso.
16. ROOMS.exits y 329/17/787 permanecen intactos.

## 18. Pendientes antes de contrato

1. gesto exacto de activación de la comparecencia;
2. tratamiento de He Zhen/Lan Meihua/Song Rui en la escena de Consejo compatible con movilidad;
3. evidencia/acciones exactas que confirman R7;
4. estado persistente exacto del Centinela;
5. room exacta del Centinela;
6. interfaz/comandos del PROTOCOLO;
7. regla técnica para bloquear el paso mientras Centinela no sea terminal sin alterar ROOMS.exits;
8. modelo uniforme de permisos;
9. balance del Centinela y recompensas M17;
10. sustitución completa del legacy `centinela_pluma` de Alturas;
11. runtime predecesor aprobado de 3C.6 y contratos anteriores.

## Estado final

`3C9_M17_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`

**NO IMPLEMENTAR. NO AVANZAR M18.**
