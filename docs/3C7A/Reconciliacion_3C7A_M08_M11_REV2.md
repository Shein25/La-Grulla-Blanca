# Reconciliación detallada 3C.7A — M08–M11 — REV2

**Fecha:** 2026-09-24  
**Estado:** `LISTA_PARA_REAUDITORIA_DOCUMENTAL`  
**Baseline documental/topológico:** `grulla-blanca_ver74.html`  
**SHA-256 ver74:** `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`  
**Predecesor runtime:** resultado aprobado de 3C.6A; no congelar `ver75` hasta terminar su auditoría.

> REV2 conserva REV1 como histórico y corrige únicamente el contrato documental M08–M11. No implementa código.

## 1. Frontera de entrada

La frontera documental de 3C.6A ya está cerrada por `3C6A_REV3_1_APTA_PARA_CONTRATO`:

```text
arc1.estado = LIII_INVESTIGACION
SECTA_INTERIOR = true
M12 = false
ATAJO_ALA_* = false
```

Esto congela el **contrato de entrada**, no el artefacto runtime final. La implementación 3C.7 deberá partir del resultado de 3C.6 que supere su auditoría.

M08, M09 y M10 son paralelas y de orden libre. M11 requiere las tres.

## 2. Modelo de estado corregido

3C.7 extiende el estado existente de 3C.6; no crea un segundo sistema.

```text
this.quests
flags.arc1
├── hitos
├── revelaciones
│   ├── R1
│   ├── R2
│   ├── R3
│   └── R4
├── permisos
│   ├── FORMACIONES_INVESTIGACION
│   ├── ARCHIVO_COMUN
│   └── ARCHIVO_RESTRINGIDO
├── sintesis
│   ├── DOS_ALAS
│   └── SEGUNDA_RAMA
└── anclajePropietario
```

Reglas:

- checkpoints M08–M11 se persisten en `flags.arc1.hitos`;
- estados de misión persisten en `this.quests`;
- `DISPONIBLE/BLOQUEADA` siguen derivados;
- `PARCIAL` sólo pertenece a revelaciones del jugador, nunca a `conocimientoNPC`;
- no se agregan claves top-level;
- `SAVE_SCHEMA_VERSION` permanece 2;
- saves de 3C.6 que ya tienen `flags.arc1` deben enriquecerse de forma idempotente con R2–R4, permisos y síntesis, sin ser tratados como corruptos.

## 3. Resoluciones técnicas

### RT-3C7-01 — M08 / Sala de Mapas de Flujo

Se mantiene:

```text
formaciones_sala_mapas
```

ver74 usa el nombre visible **Sala de Mapas de Flujo** y contiene `mesa_comparacion`.

Clasificación: `ELECCION_TECNICA_RESPALDADA_VER74`.

### RT-3C7-02 — referencias exteriores M08

Se mantienen como elección técnica:

```text
bosque_refugio_patrulla.registro
sauces_casa_comunal.mapa_local
```

Clasificación: `ELECCION_TECNICA_3C7`.

### RT-3C7-03 — M09 independiente de M08

Se preserva la regla maestra: M08/M09/M10 son paralelas. Song Rui puede activar M09 aunque M08 no esté hecha. Si M08 ya terminó, el diálogo puede aludir a sus mediciones; si no, usa inconsistencias del material archivístico/territorial disponible.

Clasificación: `RECONCILIACION_DE_FUENTE`.

### RT-3C7-04 — LEER ESCRITURAS

Se mantiene `leer → estudiar`. 3C.7 extiende `cmd_estudiar()` para scenery documental de misión:

- coste 0;
- no consume objetos;
- no concede Comprensión repetible;
- repetición idempotente.

Clasificación: `CAMBIO_NECESARIO_3C7`.

### RT-3C7-05 — ARCHIVO_COMUN / ARCHIVO_RESTRINGIDO

Corrección de REV1: **no se declara resuelta todavía la semántica de tránsito físico**.

Sí queda congelado que:

- son permisos narrativos/documentales;
- no modifican `ROOMS.exits`;
- `ARCHIVO_RESTRINGIDO` es necesario para los hallazgos sensibles de M09;
- `ARCHIVO_RESTRINGIDO` expira al cerrar M09;
- `ARCHIVO_COMUN` permanece.

Queda pendiente una decisión humana antes del contrato: si el permiso controla únicamente interacción/lectura o también debe bloquear tránsito físico por el sector restringido sin añadir un nuevo `GATES_329`.

Clasificación: `PENDIENTE_DECISION_HUMANA`.

### RT-3C7-06 — M10 rooms

Se mantienen:

```text
archivo_clinico
sala_anatomica
```

Ambos IDs existen en ver74 y encajan con el contenido de Auditoría 6.

Clasificación: `ELECCION_TECNICA_RESPALDADA_VER74`.

### RT-3C7-07 — M11 sala de síntesis

Se mantiene:

```text
interior_sala_estudio
```

Clasificación: `ELECCION_TECNICA_3C7`.

### RT-3C7-08 — M08 no exige dos nodos

REV1 endurecía el canon al exigir Nodo Oriental **y** Nodo Occidental antes de la comparación.

REV2 corrige:

```text
comparación central
+
confirmación posterior en UN nodo independiente
```

Los dos nodos siguen disponibles, pero el requisito es OR:

```text
M08_NODO_ORIENTAL
OR
M08_NODO_OCCIDENTAL
```

Clasificación: `CORRECCION_CANONICA_REV2`.

### RT-3C7-09 — NPC relevantes omitidos

Se recuperan:

- Wen Tao en M08;
- Yu Shun en M09.

Son relevantes y pueden intervenir en puesta en escena/validación técnica, pero no se convierten en requisitos estructurales sin fuente explícita.

Clasificación: `CORRECCION_DE_COBERTURA`.

### RT-3C7-10 — M10 investigación en orden libre

`M10_REGISTROS_CLINICOS` y `M10_DIAGRAMAS_ANATOMICOS` pueden completarse en cualquier orden. Chen Bo valida cuando ambos existen.

Clasificación: `CORRECCION_CANONICA_REV2`.

### RT-3C7-11 — M11 DISPONIBLE ≠ ACTIVA

Cerrar la tercera de M08/M09/M10 hace que M11 quede **DISPONIBLE derivada**, no activa automáticamente.

Elección técnica propuesta:

```text
HABLAR he_zhen
→ convocar reunión
→ M11=ACTIVA
→ anclar participantes en interior_sala_estudio
```

La convocatoria no otorga revelación ni recompensa por sí sola.

Clasificación: `ELECCION_TECNICA_3C7`.

### RT-3C7-12 — persistencia única de síntesis

Se elimina la inconsistencia de REV1.

Ruta única:

```text
flags.arc1.sintesis.DOS_ALAS
flags.arc1.sintesis.SEGUNDA_RAMA
```

No usar simultáneamente `flags.arc1.DOS_ALAS` o `flags.arc1.SEGUNDA_RAMA`.

Clasificación: `CORRECCION_ESTRUCTURAL_REV2`.

### RT-3C7-13 — baseline documental vs runtime

- ver74 sigue siendo autoridad para rooms, scenery y cierre 3C.5;
- el runtime de 3C.7 será el resultado aprobado de 3C.6;
- no se congela `ver75` mientras siga en auditoría.

Clasificación: `CORRECCION_DE_FRONTERA`.

---

# 4. M08 — Una montaña que no coincide consigo misma

## Requiere

```text
arc1.estado=LIII_INVESTIGACION
SECTA_INTERIOR=true
```

## Activación

```text
HABLAR he_zhen
@ formaciones_sala_control
```

Produce:

```text
flags.arc1.permisos.FORMACIONES_INVESTIGACION=true
flags.arc1.hitos.M08_INSTRUMENTACION_RECIBIDA=true
M08=ACTIVA
```

NPC relevantes: He Zhen, Wen Tao.

## Fase A — referencias exteriores

Ambas, orden libre:

```text
EXAMINAR registro
@ bosque_refugio_patrulla
→ hitos.M08_REF_BOSQUE

EXAMINAR mapa_local
@ sauces_casa_comunal
→ hitos.M08_REF_SAUCES
```

## Fase B — calibración / trabajo de campo

```text
EXAMINAR placas_referencia
o EXAMINAR instrumentos
@ formaciones_patio_medicion
→ hitos.M08_CALIBRACION
```

## Fase C — comparación central

```text
EXAMINAR mesa_comparacion
@ formaciones_sala_mapas
```

Requiere:

```text
M08_REF_BOSQUE
M08_REF_SAUCES
M08_CALIBRACION
```

Produce:

```text
hitos.M08_COMPARACION_MAPAS=true
```

## Fase D — confirmación independiente

Después de la comparación:

```text
EXAMINAR agujas
@ formaciones_nodo_oriental
→ hitos.M08_NODO_ORIENTAL
```

o:

```text
EXAMINAR lecturas
@ formaciones_nodo_occidental
→ hitos.M08_NODO_OCCIDENTAL
```

Cierre requiere:

```text
M08_COMPARACION_MAPAS
AND
(M08_NODO_ORIENTAL OR M08_NODO_OCCIDENTAL)
```

Produce:

```text
M08=HECHA
flags.arc1.revelaciones.R2=CONFIRMADO
FORMACIONES_INVESTIGACION permanece true
```

Recompensas canónicas cualitativas:

- Comprensión: 0;
- Mérito: moderado;
- Contribución: sí;
- valores numéricos: `PENDIENTE_BALANCE_3C7`.

---

# 5. M09 — Los nombres que faltan

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
M09=ACTIVA
flags.arc1.permisos.ARCHIVO_COMUN=true
```

NPC relevantes: Song Rui, Zhao Wen, Qiao Ren, Luo Yan, Yu Shun.

## Fase común

```text
LEER/ESTUDIAR huecos
@ archivos_galeria_registros
→ hitos.M09_REFERENCIA_AUSENTE

LEER/ESTUDIAR terminos
@ archivos_sala_estelas
→ hitos.M09_NOMBRES_DIVERGENTES
```

Con ambos:

```text
hitos.M09_SOLICITAR_RESTRINGIDO=true
```

## Autorización

```text
HABLAR qiao_ren
@ pabellon_disciplina
```

Produce:

```text
flags.arc1.permisos.ARCHIVO_RESTRINGIDO=true
hitos.M09_ARCHIVO_RESTRINGIDO_AUTORIZADO=true
```

## Fase restringida

Requiere `ARCHIVO_RESTRINGIDO=true` para registrar progreso:

```text
LEER/ESTUDIAR variantes
@ archivos_camara_copias
→ hitos.M09_COPIA_MODIFICADA

LEER/ESTUDIAR referencias
@ archivos_sala_indices
→ hitos.M09_DOS_ALAS_MENCIONADO
```

El término **Dos Alas** aparece, pero no queda definido.

## Cierre

Requiere los cuatro hallazgos.

Produce:

```text
M09=HECHA
flags.arc1.revelaciones.R3=PARCIAL
flags.arc1.permisos.ARCHIVO_RESTRINGIDO=false
flags.arc1.permisos.ARCHIVO_COMUN=true
```

Recompensas canónicas cualitativas:

- Comprensión: 0;
- Mérito: sí si produce hallazgo reconocido;
- Contribución: posible;
- valores numéricos: `PENDIENTE_BALANCE_3C7`.

---

# 6. M10 — El cuerpo recuerda

## Requiere

```text
arc1.estado=LIII_INVESTIGACION
```

## Activación

```text
HABLAR lan_meihua
@ archivo_clinico
→ M10=ACTIVA
→ hitos.M10_CASOS_ABIERTOS
```

## Investigación — orden libre

```text
LEER/ESTUDIAR formatos_antiguos
@ archivo_clinico
→ hitos.M10_REGISTROS_CLINICOS

EXAMINAR laminas
@ sala_anatomica
→ hitos.M10_DIAGRAMAS_ANATOMICOS
```

Ambos son obligatorios, pero ninguno depende del otro.

Después:

```text
HABLAR chen_bo
@ sala_anatomica
```

requiere ambos y produce:

```text
hitos.M10_CHEN_BO_CONSULTADO=true
M10=HECHA
flags.arc1.revelaciones.R4=CONFIRMADO
```

Restricciones:

- no habilitar injerto;
- no mostrar `ESTUDIAR INJERTO`;
- no afirmar `Segunda Rama == Dos Alas`;
- `LEER APENDICE` futuro fuera de 3C.7A.

Recompensas canónicas cualitativas:

- Comprensión: 0;
- Mérito: sí por investigación importante;
- Contribución: posible;
- valores numéricos: `PENDIENTE_BALANCE_3C7`.

---

# 7. M11 — Las Dos Alas

## Disponibilidad

Derivada cuando:

```text
M08=HECHA
M09=HECHA
M10=HECHA
```

No persistir `DISPONIBLE`.

## Activación propuesta

```text
HABLAR he_zhen
```

cuando M11 está disponible.

Produce:

```text
M11=ACTIVA
hitos.M11_REUNION_CONVOCADA=true
```

Entonces se anclan temporalmente:

```text
He Zhen
Song Rui
Lan Meihua
@ interior_sala_estudio
```

## Síntesis

En `interior_sala_estudio`:

```text
HABLAR he_zhen
```

integra:

```text
mediciones M08
+ textos M09
+ casos corporales M10
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
flags.arc1.revelaciones.R3=CONFIRMADO
flags.arc1.sintesis.DOS_ALAS=PRINCIPIO
flags.arc1.sintesis.SEGUNDA_RAMA=APLICACION_CORPORAL
hitos.ARC1_M11_DOS_ALAS=true
Comprensión +1
hitos.M11_SELLO_ANTIGUO_RECONOCIDO=true
M12 queda disponible de forma derivada
```

Recompensas canónicas cualitativas:

- Comprensión: +1 one-shot;
- Mérito: sí;
- Contribución: secundaria;
- valores numéricos de Mérito/Contribución: `PENDIENTE_BALANCE_3C7`.

Al cerrar, liberar los tres NPC y reubicarlos fuera de vista en posiciones válidas.

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

Wen Tao y Yu Shun se recuperan como NPC relevantes, pero REV2 no inventa un anclaje obligatorio para ellos.

## 9. Requisitos técnicos para futuro contrato

Antes de implementar:

1. extender `ARC1_IDS` a M08–M11 antes de usar esos IDs como owner de anclaje;
2. ampliar `crearArc1()/validarArc1()/normalizarArc1()` para R2–R4, permisos y síntesis;
3. migrar/enriquecer saves 3C.6 existentes de forma idempotente;
4. no cambiar `ROOMS.exits`;
5. conservar 329 rooms / 17 áreas / topología congelada;
6. mantener `SAVE_SCHEMA_VERSION=2` salvo que una auditoría de implementación demuestre que no es viable;
7. separar revelación del jugador de `conocimientoNPC`;
8. todos los hitos/recompensas deben ser one-shot.

## 10. Pendientes bloqueantes antes del contrato

- decidir semántica de **tránsito físico** de `ARCHIVO_RESTRINGIDO`;
- terminar auditoría de implementación 3C.6 y congelar el predecesor runtime;
- balance numérico de Mérito/Contribución M08–M11;
- reauditar la activación propuesta de M11 por `HABLAR he_zhen`.

## Estado

`3C7A_M08_M11_REV2_LISTA_PARA_REAUDITORIA_DOCUMENTAL`

**No implementar todavía.**
