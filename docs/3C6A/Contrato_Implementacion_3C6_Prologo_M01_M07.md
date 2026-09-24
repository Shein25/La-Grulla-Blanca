# Contrato de Implementación — 3C.6 — Prólogo + M01–M07

**Proyecto:** La Grulla Blanca  
**Estado del contrato:** `LISTO_PARA_IMPLEMENTACION`  
**Fecha:** 2026-09-24

## 0. Autoridad y fuente de verdad

Implementar únicamente contra:

1. `docs/3C6A/CIERRE_3C6A_REV3_1.md`
2. `docs/3C6A/Reconciliacion_3C6A_Prologo_M01_M07_REV3_1.md`
3. `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3_1.json`
4. `docs/3C6A/Auditoria_Final_3C6A_REV3_1_CLAUDE.md`
5. baseline `grulla-blanca_ver74.html`
6. `Informe_Implementacion_3C5_ver74.md`

Si una propuesta histórica contradice estas fuentes, ignorarla.

El JSON canónico es el del repositorio auditado, SHA-256:

`96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881`

Baseline HTML:

`grulla-blanca_ver74.html`

SHA-256:

`8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

## 1. Regla de rama

La implementación debe realizarse en una rama exclusiva de producción para 3C.6.

No trabajar en:

- `main`
- ramas `audit/*`
- ramas `experiment/*`
- ramas anteriores de 3C.5

No hacer merge durante la implementación.

Antes de tocar código, verificar:

- rama correcta;
- HEAD base;
- hash del baseline;
- que `grulla-blanca_ver74.html` sea el archivo de trabajo.

## 2. Alcance

Implementar:

- Prólogo P;
- M01;
- M02;
- M03;
- M04;
- M05;
- M06;
- M07;
- transición PROLOGO→LI;
- transición LI→LII;
- transición LII→LIII;
- migración de saves ver74;
- persistencia necesaria;
- economía Contribución/Mérito desacoplada;
- anclajes NPC de misión;
- plumbing de misiones P–M07;
- tests y regresión del alcance.

No implementar:

- M08–M18;
- epílogo;
- scheduler NPC nuevo;
- GOAP/Utility AI;
- cambios globales de 3C.4;
- cambios de topología;
- modularización del monolito.

## 3. Invariantes obligatorios

La implementación debe mantener exactamente:

- 329 rooms;
- 17 áreas;
- 787 exits dirigidos;
- 0 reciprocidades rotas;
- 0 rooms aisladas;
- 1 componente físico;
- `SAVE_SCHEMA_VERSION = 2`;
- `ROOMS.exits` sin cambios;
- identidad/cantidad global de errantes sin cambios;
- `SECTA_INTERIOR=false => M12=false => ATAJO_ALA_*=false`;
- sin tiempo diegético.

## 4. Modelo de estado

### 4.1 Estado narrativo

Persistir dentro de `flags.arc1`:

```text
estado:
  PROLOGO
  LI_INTEGRACION
  LII_TERRITORIO
  LIII_INVESTIGACION

estadoAfiliacion:
  PENDIENTE_REGISTRO
  ADMITIDO
  MIEMBRO

rangoInstitucional:
  SIN_RANGO
  ASPIRANTE
  DISCIPULO_EXTERNO
```

Gates narrativos consultan `rangoInstitucional`, no `rangoFaccion()`.

### 4.2 Facción económica

`player.facciones.grulla_blanca` sigue siendo economía/servicios.

Nueva partida:

```js
estado = "inactivo"
```

M03:

```js
estado = "miembro"
```

No auto-promover `expulsado`.

## 5. Economía

Modificar semántica:

```text
otorgarContribucion(n)
  -> aumenta sólo saldo

otorgarMerito(n)
  -> aumenta sólo mérito
```

`normalizarFacciones()` debe dejar de:

- defaultar un registro explícitamente inactivo a miembro;
- forzar `merito >= saldo`.

Historial económico debe distinguir contribución de mérito.

Auditar callers legacy de `otorgarContribucion()`, incluyendo `entregarRecompensa()` y tests.

Recompensas canónicas:

| Misión | Contribución | Mérito | Comprensión | Otro |
|---|---:|---:|---:|---|
| M02 | 1 | 0 | 0 | — |
| M03 | 0 | 0 | 0 | — |
| M04 | 2 | 0 | 0 | +1 mérito opcional one-shot |
| M05 | 3 | 0 | 0 | 1 Píldora |
| M06 | 2 | 1 | 0 | — |
| M07 | 4 | 3 | 1 | — |

Totales:

- contribución 12;
- mérito 4 normal;
- mérito 5 con incidente M04;
- comprensión 1;
- píldora 1.

## 6. QUESTS y estados

Agregar P, M01–M07 al catálogo `QUESTS`.

Estados persistidos usados por este tramo:

- `activa`
- `hecha`

`BLOQUEADA` y `DISPONIBLE` son derivados y no se persisten.

El motor puede conservar compatibilidad con `rumor`/`fallida`, pero P–M07 no dependen de ellos.

Actualizar cualquier test histórico que exigía `QUESTS={}`.

## 7. normalizarArc1() y reconciliarProgresionArc1()

Implementar ambos como piezas centrales.

### 7.1 normalizarArc1()

Debe:

- discriminar legacy válido por ausencia de `flags.arc1`;
- fallar cerrado si `flags.arc1` existe pero es inválido;
- sanear quests desconocidas a no-hecha/ausente, nunca promover;
- degradar quest downstream HECHA si su prerequisito no está HECHO;
- derivar evidencia `nivel` y `sospechaFuerte` desde `tipos`;
- derivar `informeFronteraAceptado` desde M07=HECHA;
- reconciliar owners/anclajes;
- impedir que `arc1.estado` supere lo sostenido por datos válidos.

### 7.2 reconciliarProgresionArc1()

Debe ser idempotente y ejecutarse:

- tras cierres P–M07;
- tras CONSAGRAR;
- tras load/migración;
- **inmediatamente al registrar por primera vez un nuevo tipo de evidencia territorial**.

No repetir presentaciones/recompensas one-shot.

## 8. Migración saves ver74

Trigger:

```text
schema 2 válido
+ flags.arc1 ausente
```

Preservar:

- raíz;
- origen;
- stats;
- inventario;
- técnicas;
- posición;
- visitadas;
- gates;
- NPC;
- saldo/mérito existentes.

Migrar:

```text
P   = hecha
M01 = hecha
M02 = hecha
M03 = hecha
```

One-shots P–M03:

```text
raizDiagnosticada=true
equipoInicialEntregado=true
REGISTRO_INICIAL_COMPLETADO=true
NOMBRE_INSCRITO=true
ALOJAMIENTO_CONFIRMADO=true
SERVICIO_DESPENSA_VALIDADO=true
EXAMEN_ESPIRITUAL_APRENDIDO=true
M03_PIEL_COBRE_INSTRUIDA=true
M03_PRACTICA_MUNECO_COMPLETADA=true
EVALUACION_CIRCULACION_SUPERADA=true
M03_PROMOCION_FORMALIZADA=true
TECNICA_PIEL_COBRE_APRENDIDA=true
```

Además:

- desbloquear Examen si falta;
- conceder Piel de Cobre si falta;
- `dormitorio_externos` conocido/visitado;
- no rediagnosticar raíz;
- no recalcular ni reducir economía.

Etapas legacy:

```text
etapa 1 -> LI_INTEGRACION; transicionLILIIHecha=false
etapa 2 -> LII_TERRITORIO; transicionLILIIHecha=true
etapa>=3 -> LII_TERRITORIO; transicionLILIIHecha=true; cultivoLIIIPreexistente=true
```

Si un legacy trae `SECTA_INTERIOR=true`:

- guardar `legacySectaInteriorPrevia=true` diagnóstico;
- normalizar `SECTA_INTERIOR=false`;
- `M12=false`;
- todos `ATAJO_ALA_*=false`;
- no exigir píldora retroactiva para etapa>=3;
- M04–M07 se juegan.

## 9. CONSAGRAR y gates

### 9.1 Regla qi

CONSAGRAR **no resta** el vaso anterior al qi.

Ejemplo:

```text
25/25 etapa 1 -> etapa 2 con 25/45
```

### 9.2 LI→LII

Condición:

```text
player.etapa >= 2
rangoInstitucional == DISCIPULO_EXTERNO
primerServicioFormal == true
evaluacionCirculacion == SUPERADA
```

One-shot:

`flags.arc1.transicionLILIIHecha`

Efecto:

- `arc1.estado=LII_TERRITORIO`;
- presentación ceremonial una sola vez.

### 9.3 LII→LIII

Partida nueva:

```text
qi >= 45
+ pildora_consolidacion
+ M04 HECHA
+ M05 HECHA
+ evidenciaTerritorial >= SUFICIENTE
+ informeFronteraAceptado=true
```

`servicioTerritorial` es derivado: M04 && M05.

Al CONSAGRAR 2→3:

- validar todos los requisitos antes de consumir recursos;
- consumir 1 píldora;
- no restar qi;
- ejecutar reconciliación.

One-shot:

`flags.arc1.transicionLIILIIIHecha`

Efecto:

- `arc1.estado=LIII_INVESTIGACION`;
- `SECTA_INTERIOR=true`;
- `M12=false`;
- `ATAJO_ALA_*=false`;
- presentación ceremonial one-shot.

`compruebaPuerta()` debe ser fail-closed: requisito desconocido bloquea y reporta **antes** de cualquier consumo.

## 10. Anclajes NPC de misión

Conservar forma de 3C.5:

```js
posicionNPC[id].anclaje = { room, hasta }
```

Agregar owner persistente:

```js
flags.arc1.anclajePropietario[npcId] = ownerId
```

Un anclaje con owner de misión no puede ser preemptado por escena social/ambiental/crisis.

Tabla:

| NPC | Owner | Room | Hasta | Liberación |
|---|---|---|---|---|
| Tao Ming | P | registro | REGISTRO_INICIAL_COMPLETADO | transferir a M01 |
| Tao Ming | M01 | registro | NOMBRE_INSCRITO | mover a oficina_servicios fuera de vista |
| Madre Wen | M01 | patio_cabanas | ALOJAMIENTO_CONFIRMADO | limpiar |
| Tao Ming | M02 | oficina_servicios | SERVICIO_DESPENSA_VALIDADO | limpiar |
| Chen Bo | M02 | sala_anatomica | EXAMEN_ESPIRITUAL_APRENDIDO | limpiar |
| Shen Baojun | M03 | sala_formas | M03_PIEL_COBRE_INSTRUIDA | limpiar |
| Qiao Ren | M03 | pabellon_disciplina | M03_PROMOCION_FORMALIZADA | limpiar |
| Jiang Rui | M04 | puesto_valle | M04_RETORNO_INFORMADO | limpiar |
| Gao Shun | M04 | puerta | M04_CONTROL_PUERTA | tras salir, mover a casa_guardia fuera de vista |
| Jiang Rui | M07 | pabellon_disciplina | INFORME_ACEPTADO | al cerrar, mover a puesto_valle |

`hasta` es simbólico, nunca tiempo diegético.

## 11. Prólogo P

Nueva partida:

- visible como Aspirante;
- `estadoAfiliacion=PENDIENTE_REGISTRO`;
- `rangoInstitucional=SIN_RANGO`;
- facción económica Grulla `inactivo`;
- quitar entrega automática legacy de uniforme/espada.

Diagnóstico raíz:

- tres decisiones;
- score Fuego/Metal/Agua;
- empate resuelto por reacción final de la Piedra;
- sin RNG;
- conservar formato actual `player.raiz`.

Equipamiento en `descansillo`, one-shot `equipoInicialEntregado`.

Preservar beneficios de origen.

Ruta principal:

```text
patio_raices
descansillo
mirador_niebla
patio_practica
sendero_pinos
camino
puerta
registro
```

Cierre:

`REGISTRO_INICIAL_COMPLETADO`

Produce:

- P HECHA;
- `estadoAfiliacion=ADMITIDO`;
- `arc1.estado=LI_INTEGRACION`.

## 12. M01

Ruta:

```text
registro
sala_jade
patio
patio_cabanas
corredor_cabanas
dormitorio_externos
```

Eventos:

- Tao Ming activa;
- `NOMBRE_INSCRITO`;
- Madre Wen asigna alojamiento;
- player entra físicamente a `dormitorio_externos`.

Cierre:

`ALOJAMIENTO_CONFIRMADO`

Produce:

- `rangoInstitucional=ASPIRANTE`;
- `SECTA_EXTERIOR_BASE=true`;
- dormitorio conocido/visitado.

## 13. M02

Secuencia:

1. HABLAR Tao Ming en `oficina_servicios`;
2. ir a `deposito_comun`;
3. resolver `rata_despensa` con M02 activa;
4. fijar cadáver tutorial;
5. aprender Examen con Chen Bo en `sala_anatomica`;
6. volver y OBSERVAR/EXAMINAR cadáver;
7. HABLAR Tao Ming.

Wrapper local:

- reutilizar errante `rata_despensa` / mob `rata_qi`;
- retiro permanente sólo si muere con M02 activa;
- no respawn posterior;
- EXTRAER bloqueado localmente;
- no Atlas/bestiario/familiaridad;
- cadáver controlado;
- si falta y el paso sigue pendiente, recrear **una vez** sin loot;
- no cambiar 3C.4 global.

Cierre:

`SERVICIO_DESPENSA_VALIDADO`

Produce:

- `primerServicioFormal=true`;
- Examen aprendido/desbloqueado.

## 14. M03

### Enseñanza

Shen Baojun @ `sala_formas`.

Piel de Cobre se concede idempotentemente.

`manual_piel` no puede enseñar Piel de Cobre antes de M03. Después, si ya es conocida, no consumirlo ni inventar maestría.

### Muñeco

En `patio_marcial`, crear instancia derivada mientras:

`M03_PRACTICA_MUNECO_COMPLETADA=false`

Completar sólo cuando el jugador usa con éxito `piel_cobre` durante ese encuentro.

Si desaparece/muere/load con paso pendiente, recrear.

No agregar mob permanente a ROOMS.

### Evaluación

En `patio_respiracion`:

el hook de `cmd_meditar` debe disparar `EVALUACION_CIRCULACION_SUPERADA`:

- después de comprobar sin combate y sin hostiles vivos;
- antes de la rama `qi>=qi_max` / CONSAGRAR;
- aunque no se gane qi.

### Promoción

Qiao Ren @ `pabellon_disciplina`.

Produce:

- M03 HECHA;
- `rangoInstitucional=DISCIPULO_EXTERNO`;
- `estadoAfiliacion=MIEMBRO`;
- facción económica `miembro`;
- evaluación superada.

## 15. M04

Activación: HABLAR Jiang Rui @ `puesto_valle`.

Checkpoints one-shot:

```text
M04_ASIGNADA
  HABLAR jiang_rui @ puesto_valle

M04_CONTROL_PUERTA
  HABLAR gao_shun @ puerta

M04_REFUGIO_ALCANZADO
  ENTER bosque_refugio_patrulla con M04 activa

M04_RETORNO_INFORMADO
  HABLAR jiang_rui @ puesto_valle
```

No usar `visitadas`.

Incidente opcional:

- EXAMINAR `bosque_puesto_marcas.tablillas`;
- o EXAMINAR `bosque_refugio_patrulla.registro`;
- sólo M04 activa;
- primer disparo fija flag y luego +1 mérito;
- nunca recomputar en cierre.

Cierre:

`PRIMERA_PATRULLA_VALIDADA`

Produce:

- `PATRULLA_TERRITORIAL=true`;
- refugio conocido.

## 16. M05

Duan Shibo activa @ `oficina_logistica`.

Checkpoints sólo posteriores a activación:

```text
M05_VALLE_LOGISTICA_REVISADA
  ENTER mercado_valle OR granero_valle

M05_XU_AN_CONTACTADO
  HABLAR xu_an @ sauces_casa_comunal OR sauces_plaza

M05_CIRCUITO_REGISTRADO
  EXAMINAR registros @ sauces_casa_comunal
  requiere M05_XU_AN_CONTACTADO

M05_HOSPEDAJE_VISITADO
  ENTER sauces_casa_huespedes
```

Cierre cuando los cuatro estén completos.

Produce:

- `reconocimientoSauces=HUESPED`;
- alojamiento conocido;
- `PILDORA_CONSOLIDACION_OTORGADA=true`;
- una Píldora.

### Protección

Mientras:

```text
PILDORA_CONSOLIDACION_OTORGADA
&& etapa < 3
&& !transicionLIILIIIHecha
```

bloquear cualquier remoción/transferencia excepto consumidor autorizado CONSAGRAR 2→3.

Reemisión:

- sólo si falta;
- sólo con `PILDORA_REEMITIDA=false`;
- fijar flag **antes** de agregar;
- máximo una reemisión;
- no acumular duplicados.

## 17. M06

Tipos:

```text
DESPLAZAMIENTO_FAUNA
ALTERACION_VEGETAL
ALTERACION_HIDRICA
PATRON_TERRITORIAL
```

Conjunto persistente sin duplicados.

Evaluador:

```text
1 -> INSUFICIENTE, sospechaFuerte=false
2 -> INSUFICIENTE, sospechaFuerte=true
3 -> SUFICIENTE, sospechaFuerte=true
4 -> CONCLUYENTE, sospechaFuerte=true
```

Ordinal:

```text
INSUFICIENTE=0
SUFICIENTE=1
CONCLUYENTE=2
```

Tabla externa verificada contra ver74 completo:

| Tipo | Fuente 1 | Fuente 2 |
|---|---|---|
| DESPLAZAMIENTO_FAUNA | bosque_collado_alto.huellas | aguas_poza_profunda.marcas |
| ALTERACION_VEGETAL | aguas_senda_bosque.vegetacion | terraza_cantera.vegetacion |
| ALTERACION_HIDRICA | aguas_cauce_alto.corriente | aguas_paso_piedras.corriente |
| PATRON_TERRITORIAL | bosque_puesto_marcas.tablillas | bosque_refugio_patrulla.registro |

Hooks externos a `ROOMS`.

Cada nuevo tipo registrado dispara inmediatamente `reconciliarProgresionArc1()`.

Activación M06:

```text
M04 HECHA
&& M05 HECHA
&& tipos.size >= 1
&& M06 no activa/hecha
```

Cierre state-based con nivel >= SUFICIENTE.

Produce:

`arc1.revelaciones.R1=PARCIAL`

El cuarto tipo puede registrarse hasta cerrar M07. CONCLUYENTE sólo modifica contexto/diálogo.

## 18. M07

Activar:

```text
HABLAR qiao_ren @ pabellon_disciplina
M06 HECHA
evidencia >= SUFICIENTE
```

Al activar, anclar Jiang Rui.

Formulación:

```text
CAUTA + SUFICIENTE/CONCLUYENTE
 -> final CAUTA, corregida=false

FUERTE + CONCLUYENTE
 -> final FUERTE, corregida=false

FUERTE + SUFICIENTE
 -> corrección institucional automática
 -> final CAUTA, corregida=true
```

No hay rama de rechazo ni penalización.

Persistir:

- `formulacionFinal`;
- `corregida`.

Cierre:

`INFORME_ACEPTADO`

Produce:

- `informeFronteraAceptado=true`;
- player R1 CONFIRMADO;
- Jiang Rui R1 CONFIRMADO;
- Qiao Ren R1 CONFIRMADO;
- He Zhen R1 SABE;
- Ren Bo R1 SABE;
- Su Lian R1 SABE;
- +1 Comprensión one-shot.

Usar escritura NPC directa y monotónica. No implementar propagación automática.

## 19. Conocimiento player vs NPC

No mezclar dominios.

Player:

```text
flags.arc1.revelaciones.R1
PARCIAL
CONFIRMADO
```

NPC:

```text
conocimientoNPC[npc].R1
DESCONOCIDO
SOSPECHA
SABE
CONFIRMADO
```

Nunca escribir PARCIAL en `conocimientoNPC`.

Implementar helper monotónico de elevación.

## 20. UI y presentación

Transiciones LI→LII y LII→LIII pueden usar popup/presentación ceremonial one-shot, coherente con UI de aprendizaje de técnica.

No introducir:

- fechas;
- horas;
- amanecer/noche;
- estaciones;
- calendarios diegéticos.

## 21. Tests mínimos obligatorios

### 21.1 Regresión mundial

Debe seguir pasando:

- 329 rooms;
- 17 áreas;
- 787 exits;
- 0 rotas;
- 0 aisladas;
- 1 componente;
- invariantes de gates.

### 21.2 Save/load

Probar:

- nueva partida;
- save a mitad de P;
- save a mitad de cada M01–M07;
- legacy etapa 1;
- legacy etapa 2;
- legacy etapa>=3;
- legacy con SECTA_INTERIOR=true;
- flags.arc1 inválido;
- quest estado desconocido;
- downstream HECHA sin prerequisito;
- owner/anclaje corruptos;
- evidencia nivel corrupto vs tipos.

### 21.3 Idempotencia

Probar doble ejecución de:

- equipamiento P;
- raíz;
- Examen;
- Piel de Cobre;
- práctica muñeco;
- evaluación M03;
- incidente M04;
- recompensas M02–M07;
- píldora M05;
- conocimiento M07;
- transiciones LI/LII/LIII.

### 21.4 Soft-locks

Probar:

- consagrar antes de M03;
- cerrar M03 ya etapa 2;
- vaso lleno antes de evaluación M03;
- rata muerta antes de aprender Examen;
- cadáver perdido;
- M04/M05 visitadas históricamente;
- M05 píldora faltante;
- carga repetida después de reemisión;
- M04+M05 con cero evidencia, luego primera evidencia;
- 3/4 evidencias antes de activar M06;
- M07 con cada combinación válida;
- etapa>=3 legacy + M04–M07.

### 21.5 Economía

Probar:

- contribución no aumenta mérito;
- mérito no aumenta saldo;
- M02 paga estando facción inactiva;
- expulsado no recibe;
- historial distingue tipos;
- totals 12/4 o 12/5;
- servicios 8/20 siguen requiriendo mérito real.

## 22. Prohibiciones

No:

- cambiar topología;
- modificar `ROOMS.exits`;
- agregar/quitar errantes globales;
- cambiar 3C.4 global;
- subir schema;
- reintroducir quests legacy;
- usar RNG para raíz;
- usar RNG para incidente M04;
- usar afinidad social como gate;
- abrir M12;
- abrir atajos;
- implementar M08+;
- modularizar el HTML.

## 23. Entregable de implementación

Al terminar, entregar:

1. archivo HTML resultante con nombre de versión nueva;
2. SHA-256;
3. rama y HEAD;
4. lista exacta de archivos modificados;
5. informe:
   `Informe_Implementacion_3C6_Prologo_M01_M07.md`;
6. resultados Node;
7. resultados browser/Chromium si están disponibles;
8. conteo total de tests;
9. lista de cambios técnicos;
10. lista de cualquier desviación del contrato.

No declarar PASS si browser no pudo ejecutarse; distinguir claramente Node PASS de browser NO_VERIFICADO.

## 24. Criterio de aceptación

3C.6 sólo podrá cerrarse después de:

- implementación terminada;
- tests reproducibles;
- auditoría externa independiente;
- revisión de informe;
- ausencia de regresiones;
- confirmación de hashes;
- merge posterior autorizado explícitamente.

**Este contrato no autoriza merge.**
