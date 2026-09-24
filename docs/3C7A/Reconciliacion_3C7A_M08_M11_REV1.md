# Reconciliación detallada 3C.7A — M08–M11 — REV1

**Fecha:** 2026-09-24  
**Estado:** `LISTA_PARA_AUDITORIA_EXTERNA`  
**Baseline:** `grulla-blanca_ver74.html`  
**SHA-256:** `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

> Este documento no implementa código. Convierte el canon recuperado de Auditoría 6 en un contrato documental concreto para M08–M11, distinguiendo canon de decisiones técnicas de integración con ver74.

## 1. Frontera de entrada

La entrada queda provisional hasta el PASS final de 3C.6A REV3.1:

```text
arc1.estado = LIII_INVESTIGACION
SECTA_INTERIOR = true
M12 = false
ATAJO_ALA_* = false
```

M08, M09 y M10 son paralelas y de orden libre. M11 exige las tres.

## 2. Decisiones técnicas de reconciliación

### RT-3C7-01 — M08 / Sala de Mapas de Flujo

Se propone mapear la antigua “Sala de Mapas de Flujo” a:

```text
formaciones_sala_mapas
```

No se basa sólo en semejanza: ver74 usa exactamente el nombre visible **Sala de Mapas de Flujo** y su `mesa_comparacion` está diseñada para colocar mediciones de campo junto a planos.

Clasificación: `ELECCION_TECNICA_RESPALDADA_VER74`.

### RT-3C7-02 — referencias exteriores de M08

Para que M08 use lugares que el jugador necesariamente conoció en M04/M05, se proponen:

```text
bosque_refugio_patrulla.registro
sauces_casa_comunal.mapa_local
```

No son nuevas rooms ni scenery.

Clasificación: `ELECCION_TECNICA_3C7`.

### RT-3C7-03 — contradicción interna de Auditoría 6 en M09

Auditoría 6 fija simultáneamente:

```text
M08/M09/M10 paralelas y de orden libre
```

y una activación de M09 que menciona “referencias cruzadas usadas durante M08”.

REV1 preserva la dependencia maestra: **M09 no exige M08**.

Song Rui activa M09 en cualquier orden. Si M08 ya fue hecha, su diálogo puede mencionar esas mediciones; si no, señala inconsistencias archivísticas/territoriales ya disponibles. Objetivos, revelación y cierre no cambian.

Clasificación: `RECONCILIACION_DE_FUENTE`.

### RT-3C7-04 — LEER ESCRITURAS

ver74 ya normaliza:

```text
leer → estudiar
```

pero `cmd_estudiar()` sólo sabe usar manuales y devuelve que la enseñanza institucional está pendiente.

3C.7 debe **extender `cmd_estudiar()`**, no crear otro verbo:

```text
LEER <scenery documental>
ESTUDIAR <scenery documental>
```

deben resolver el mismo evento contextual de misión.

Reglas:

- no consume objeto;
- no cuesta recursos;
- no concede +2 Comprensión;
- repetir la lectura no vuelve a otorgar progreso/recompensa.

Clasificación: `CAMBIO_NECESARIO_3C7`.

### RT-3C7-05 — ARCHIVO_COMUN / ARCHIVO_RESTRINGIDO

Se modelan como **permisos documentales**, no como nuevos `GATES_329`.

No se cambia `ROOMS.exits`.

`ARCHIVO_RESTRINGIDO` habilita objetivos sensibles de M09 y expira al cerrar M09. `ARCHIVO_COMUN` permanece.

Clasificación: `ELECCION_TECNICA_3C7`.

### RT-3C7-06 — M10 rooms

Se resuelve el hueco histórico con los IDs reales del baseline:

```text
archivo_clinico
sala_anatomica
```

Chen Bo tiene ambas dentro de su territorio normal.

Clasificación: `ELECCION_TECNICA_RESPALDADA_VER74`.

### RT-3C7-07 — sala de reunión M11

Se propone:

```text
interior_sala_estudio
```

Es una sala de Secta Interior dedicada a lectura, preparación de informes y trabajo compartido. Evita convertir la síntesis en una sesión del Consejo.

Clasificación: `ELECCION_TECNICA_3C7`.

---

# 3. M08 — Una montaña que no coincide consigo misma

## Requiere

```text
arc1.estado=LIII_INVESTIGACION
SECTA_INTERIOR=true
```

No requiere M09 ni M10.

## Activación

```text
HABLAR he_zhen
@ formaciones_sala_control
```

Produce:

```text
FORMACIONES_INVESTIGACION=true
M08_INSTRUMENTACION_RECIBIDA=true
```

He Zhen queda anclado sólo hasta entregar el marco/instrumentación.

## Objetivos

### Referencias exteriores — ambas, orden libre

```text
EXAMINAR registro
@ bosque_refugio_patrulla
→ M08_REF_BOSQUE

EXAMINAR mapa_local
@ sauces_casa_comunal
→ M08_REF_SAUCES
```

### Calibración

```text
EXAMINAR placas_referencia
o EXAMINAR instrumentos
@ formaciones_patio_medicion
→ M08_CALIBRACION
```

### Nodos independientes — ambos, orden libre

```text
EXAMINAR agujas
@ formaciones_nodo_oriental
→ M08_NODO_ORIENTAL

EXAMINAR lecturas
@ formaciones_nodo_occidental
→ M08_NODO_OCCIDENTAL
```

### Comparación final

```text
EXAMINAR mesa_comparacion
@ formaciones_sala_mapas
```

requiere los cinco flags anteriores.

Produce:

```text
M08_COMPARACION_MAPAS=true
M08=HECHA
arc1.revelaciones.R2=CONFIRMADO
```

`FORMACIONES_INVESTIGACION` permanece.

### Recompensa

- Comprensión: 0, canónico.
- Contribución/Mérito: `PENDIENTE_BALANCE_3C7`; Auditoría 6 sólo los deja cualitativos.

---

# 4. M09 — Los nombres que faltan

## Requiere

```text
arc1.estado=LIII_INVESTIGACION
```

No requiere M08.

## Activación

```text
HABLAR song_rui
@ archivos_sala_consulta
```

Produce:

```text
ARCHIVO_COMUN=true
M09=ACTIVA
```

## Mecánica LEER ESCRITURAS

Se usa `LEER`/`ESTUDIAR` contextual sobre scenery documental.

### Fase común

```text
LEER huecos
@ archivos_galeria_registros
→ M09_REFERENCIA_AUSENTE
→ tipo REFERENCIA_AUSENTE

LEER terminos
@ archivos_sala_estelas
→ M09_NOMBRES_DIVERGENTES
→ tipo NOMBRES_PRESENTES_AUSENTES
```

Con ambos:

```text
M09_SOLICITAR_RESTRINGIDO=true
```

## Autorización de Qiao Ren

```text
HABLAR qiao_ren
@ pabellon_disciplina
```

requiere `M09_SOLICITAR_RESTRINGIDO`.

Produce:

```text
ARCHIVO_RESTRINGIDO=true
M09_ARCHIVO_RESTRINGIDO_AUTORIZADO=true
```

## Fase restringida

```text
LEER variantes
@ archivos_camara_copias
→ M09_COPIA_MODIFICADA
→ tipo COPIA_MODIFICADA

LEER referencias
@ archivos_sala_indices
→ M09_DOS_ALAS_MENCIONADO
```

La segunda lectura deja aparecer el término **Dos Alas**, pero no lo define.

## Cierre

Requiere:

```text
M09_REFERENCIA_AUSENTE
M09_NOMBRES_DIVERGENTES
M09_COPIA_MODIFICADA
M09_DOS_ALAS_MENCIONADO
```

Produce:

```text
M09=HECHA
arc1.revelaciones.R3=PARCIAL
ARCHIVO_RESTRINGIDO=false
ARCHIVO_COMUN=true
```

No se escribe `PARCIAL` en `conocimientoNPC`.

### Compañeros

Zhao Wen y Luo Yan conservan hooks sociales documentados de M09, pero son opcionales y no cierran objetivos.

---

# 5. M10 — El cuerpo recuerda

## Requiere

```text
arc1.estado=LIII_INVESTIGACION
```

No requiere M08 ni M09.

## Activación

```text
HABLAR lan_meihua
@ archivo_clinico
→ M10_CASOS_ABIERTOS
```

## Investigación

```text
LEER formatos_antiguos
@ archivo_clinico
→ M10_REGISTROS_CLINICOS
```

Esto permite identificar el conjunto histórico llamado **Segunda Rama**, pero no lo equipara a Dos Alas.

Después:

```text
EXAMINAR laminas
@ sala_anatomica
→ M10_DIAGRAMAS_ANATOMICOS
```

Con ambos:

```text
HABLAR chen_bo
@ sala_anatomica
→ M10_CHEN_BO_CONSULTADO
```

## Cierre

Produce:

```text
M10=HECHA
arc1.revelaciones.R4=CONFIRMADO
```

Restricciones:

- no habilita injerto;
- no usa `ESTUDIAR INJERTO`;
- no afirma `Segunda Rama == Dos Alas`;
- `LEER APENDICE` futuro queda fuera de 3C.7A.

### Compañeros

Mei Lian, Guo Chen y Luo Yan pueden tener escenas opcionales ya documentadas. Ninguna puede cerrar M10 ni habilitar injerto.

---

# 6. M11 — Las Dos Alas

## Requiere

```text
M08=HECHA
M09=HECHA
M10=HECHA
```

Cuando se cierra la tercera misión:

```text
M11=ACTIVA
M11_REUNION_CONVOCADA=true
```

Se anclan temporalmente:

```text
He Zhen
Song Rui
Lan Meihua
```

en:

```text
interior_sala_estudio
```

## Síntesis

El jugador entra y usa:

```text
HABLAR he_zhen
```

La escena integra:

```text
mediciones de M08
+ textos de M09
+ casos corporales de M10
```

No es una nueva expedición.

## Cierre

Evento:

```text
M11_SINTESIS_DOS_ALAS
```

Produce atómicamente:

```text
M11=HECHA

arc1.revelaciones.R3=CONFIRMADO

DOS_ALAS=PRINCIPIO
SEGUNDA_RAMA=APLICACION_CORPORAL

Comprensión +1
one-shot ARC1_M11_DOS_ALAS

M11_SELLO_ANTIGUO_RECONOCIDO=true
M12 disponible
```

He Zhen reconoce el sello antiguo bajo Formaciones como consecuencia de la síntesis.

Los tres NPC se liberan y vuelven fuera de vista a posiciones válidas de sus territorios.

---

# 7. Persistencia e idempotencia

Todo nuevo estado vive en:

```text
this.quests
flags.arc1
```

No se agrega clave top-level.

Reglas:

- `DISPONIBLE/BLOQUEADA` siguen derivados.
- Sets/flags de M08–M10 no cuentan dos veces.
- `ARCHIVO_RESTRINGIDO` persiste durante M09 si se guarda, y expira una vez al cerrar.
- La Comprensión de M11 usa `ARC1_M11_DOS_ALAS` y no puede repetirse.
- Cargar una misión a mitad conserva los flags ya registrados.
- `conocimientoNPC` no recibe estados PARCIAL.

---

# 8. Anclajes

| NPC | Owner | Room | Hasta |
|---|---|---|---|
| He Zhen | M08_ACTIVACION | `formaciones_sala_control` | instrumentación entregada |
| Song Rui | M09_ACTIVACION | `archivos_sala_consulta` | M09 activa |
| Qiao Ren | M09_AUTORIZACION | `pabellon_disciplina` | permiso restringido concedido |
| Lan Meihua | M10_ACTIVACION | `archivo_clinico` | casos abiertos |
| Chen Bo | M10_VALIDACION | `sala_anatomica` | M10 cerrada |
| He Zhen | M11 | `interior_sala_estudio` | síntesis cerrada |
| Song Rui | M11 | `interior_sala_estudio` | síntesis cerrada |
| Lan Meihua | M11 | `interior_sala_estudio` | síntesis cerrada |

Los anclajes de misión prevalecen sobre escenas sociales mientras estén activos.

---

# 9. Pendientes antes de contrato

1. PASS final de 3C.6A para congelar la frontera LIII.
2. Resultado de la auditoría externa de 3C.7A Fase 1.
3. Auditoría específica de RT-3C7-03 (orden libre M09 vs texto de activación histórico).
4. Auditoría de `ARCHIVO_RESTRINGIDO` como permiso documental y no gate topológico.
5. Balance numérico de Contribución/Mérito para M08–M11.
6. Confirmar técnicamente `interior_sala_estudio` como staging de M11.
7. Después: M12 + gate LIII→LIV.

## Estado

`3C7A_M08_M11_REV1_LISTA_PARA_AUDITORIA`

No implementar todavía.
