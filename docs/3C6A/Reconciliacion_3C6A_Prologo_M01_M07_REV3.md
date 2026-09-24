# Reconciliación 3C.6A — Prólogo + M01–M07 — REV3

Fecha: 2026-09-24

## Veredicto

`3C6A_REV3_LISTA_PARA_AUDITORIA_DE_CIERRE`

REV3 corrige REV2 a partir de la auditoría externa de Claude y de las resoluciones técnicas posteriores.
No implementa código. No amplía el alcance a M08–M18.

### Baseline

- `grulla-blanca_ver74.html`
- SHA-256 `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`
- `SAVE_SCHEMA_VERSION = 2`
- 3C.5 NPC: cerrado y auditado
- Auditoría de REV2: `Auditoria_3C6A_REV2_Prologo_M01_M07_CLAUDE.md` → `3C6A_REV2_REQUIERE_CORRECCIONES`

## 1. Principios congelados

- No modificar `ROOMS.exits`.
- No modificar globalmente 3C.4 ni la cantidad/identidad de errantes.
- `SECTA_INTERIOR=false => M12=false => ATAJO_ALA_*=false`.
- No introducir tiempo diegético.
- No subir `SAVE_SCHEMA_VERSION`.
- `arc1.revelaciones.R1` y `conocimientoNPC[npc].R1` son dominios distintos.
- Toda transición y recompensa debe ser idempotente y fail-closed.

## 2. Resoluciones post-auditoría REV2

### R3_01 — Afiliación, rango institucional y rango económico

REV3 separa tres dominios:

```text
flags.arc1.estadoAfiliacion
  PENDIENTE_REGISTRO
  ADMITIDO
  MIEMBRO

flags.arc1.rangoInstitucional
  SIN_RANGO
  ASPIRANTE
  DISCIPULO_EXTERNO

player.facciones.grulla_blanca
  estado de acceso económico/servicios
  saldo
  mérito
  rangoFaccion() derivado del mérito
```

`rangoInstitucional` es la fuente de verdad para gates narrativos. `rangoFaccion()` no lo sustituye.
`player.facciones.grulla_blanca.estado` comienza `inactivo` y pasa a `miembro` en M03.

### R3_02 — Evaluación central de gates

Se define `reconciliarProgresionArc1()` como operación idempotente y fail-closed.
Se invoca después de cierres P–M07, después de CONSAGRAR y después de cargar/migrar.

One-shots:

```text
flags.arc1.transicionLILIIHecha
flags.arc1.transicionLIILIIIHecha
```

### R3_03 — Saves ver74 existentes

Un save schema 2 válido sin `flags.arc1` **no repite P–M03**.

Se preservan raíz, origen, stats, inventario, técnicas, posición, visitadas, gates, NPC y valores económicos existentes.

La migración fija:

```text
P    = hecha
M01  = hecha
M02  = hecha
M03  = hecha

estadoAfiliacion       = MIEMBRO
rangoInstitucional     = DISCIPULO_EXTERNO
primerServicioFormal   = true
evaluacionCirculacion  = SUPERADA
EXAMEN_ESPIRITUAL_APRENDIDO = true
SECTA_EXTERIOR_BASE    = true
```

Si faltan, se desbloquea Examen y se concede Piel de Cobre sin consumir manual.
La raíz se conserva; nunca se vuelve a diagnosticar.

- etapa 1 → `LI_INTEGRACION`, todavía debe consagrar.
- etapa 2 → `LII_TERRITORIO`.
- etapa ≥3 → `LII_TERRITORIO` + `cultivoLIIIPreexistente=true`; no se exige una píldora retroactiva. M04–M07 sí deben jugarse y `SECTA_INTERIOR` sigue cerrada hasta M07 + reconciliación.

### R3_04 — Evidencia territorial

Único enum de nivel:

```text
INSUFICIENTE < SUFICIENTE < CONCLUYENTE
```

Dos tipos distintos siguen siendo `INSUFICIENTE`, con `sospechaFuerte=true`.

Persistencia:

```text
flags.arc1.evidenciaTerritorial.tipos
flags.arc1.evidenciaTerritorial.nivel
flags.arc1.evidenciaTerritorial.sospechaFuerte
```

Tipos:

```text
DESPLAZAMIENTO_FAUNA
ALTERACION_VEGETAL
ALTERACION_HIDRICA
PATRON_TERRITORIAL
```

Comparador ordinal obligatorio:

```text
INSUFICIENTE = 0
SUFICIENTE   = 1
CONCLUYENTE  = 2
```

La evidencia puede registrarse desde que `PATRULLA_TERRITORIAL=true` y hasta cerrar M07.
`CONCLUYENTE` mejora diálogo/contexto; no cambia gates ni recompensas.

### R3_05 — Contribución y Mérito

REV3 congela canales realmente separados:

```text
otorgarContribucion(n) → sólo saldo
otorgarMerito(n)       → sólo mérito
```

`normalizarFacciones` deja de imponer `merito >= saldo`. Los rangos económicos continúan derivados sólo del mérito.

Totales P–M07:

```text
Contribución: 12
Mérito sin incidente M04: 4
Mérito con incidente M04: 5
Comprensión: 1
Píldora: 1
```

Los saves existentes conservan sus números actuales; la migración no recalcula saldo ni mérito.

## 3. Gates reconciliados

### PROLOGO → LI

`REGISTRO_INICIAL_COMPLETADO` produce `PROLOGO=HECHO` y `arc1.estado=LI_INTEGRACION`.

### LI → LII

```text
player.etapa >= 2
+ flags.arc1.rangoInstitucional == DISCIPULO_EXTERNO
+ primerServicioFormal == true
+ evaluacionCirculacion == SUPERADA
```

Evaluar en:

```text
cierre de M03
CONSAGRAR 1→2
carga/migración
reconciliación posterior a cierres P–M07
```

One-shot: `transicionLILIIHecha`.

Efecto: presentación ceremonial + `arc1.estado=LII_TERRITORIO`.

### LII → LIII

Para una partida nueva, CONSAGRAR 2→3 exige:

```text
qi >= 45
+ Píldora de Consolidación
+ M04 HECHA
+ M05 HECHA
+ evidenciaTerritorial >= SUFICIENTE
+ informeFronteraAceptado == true
```

`servicioTerritorial=COMPLETADO` es **derivado**: `M04=HECHA && M05=HECHA`.

Tras la consagración exitosa, `reconciliarProgresionArc1()` ejecuta una vez:

```text
arc1.estado = LIII_INVESTIGACION
SECTA_INTERIOR = true
transicionLIILIIIHecha = true
```

`M12` y `ATAJO_ALA_*` permanecen false.

Para un save ver74 migrado con etapa ≥3, el componente de cultivo se considera ya satisfecho; no se consume píldora retroactivamente. La transición espera M04–M07.

**Regla de seguridad:** `compruebaPuerta()` debe ser fail-closed. Un requisito desconocido bloquea o produce error; nunca se ignora silenciosamente.

## 4. Misiones reconciliadas

### P — La Piedra y la Puerta · `PROLOGO`

- Activación: flujo de nueva partida.
- Rooms: `patio_raices`, `descansillo`, `mirador_niebla`, `patio_practica`, `sendero_pinos`, `camino`, `puerta`, `registro`.
- La raíz se resuelve **antes de `crearPersonaje`** mediante tres elecciones + reacción final de desempate, sin RNG.
- En `descansillo` se entrega una sola vez el uniforme y el arma inicial; `equipoInicialEntregado` evita duplicación.
- El origen callejero conserva `cuchillo_hueso` conforme a su beneficio de origen y no debe duplicar una espada si el origen la sustituye.
- Guardia/ayudante son roles genéricos; no se agregan NPC a `NPC_DEF`.
- Herboristería permanece mecánicamente desbloqueada por compatibilidad durante 3C.6, sin presentarla como recompensa narrativa de P.
- Cierre: `REGISTRO_INICIAL_COMPLETADO`.
- Produce: `estadoAfiliacion=ADMITIDO`, `PROLOGO=HECHO`, `arc1.estado=LI_INTEGRACION`.
- Abre M01.
- Recompensa: 0.

### M01 — Un nombre entre miles · `LI_INTEGRACION`

Ruta:

```text
registro
→ sala_jade
→ patio
→ patio_cabanas
→ corredor_cabanas
→ dormitorio_externos
```

- Tao Ming activa mediante anclaje temporal en `registro`.
- `NOMBRE_INSCRITO` ocurre en `sala_jade`.
- Madre Wen asigna alojamiento en `patio_cabanas`.
- El jugador debe entrar físicamente en `dormitorio_externos`.
- `corredor_cabanas` es tránsito narrativo, no gate.
- Cierre: `ALOJAMIENTO_CONFIRMADO`.
- Produce: `rangoInstitucional=ASPIRANTE`, `SECTA_EXTERIOR_BASE=true`, alojamiento conocido/visitado.
- Recompensa: 0.

### M02 — Trabajo que alguien debe hacer · `LI_INTEGRACION`

Tao Ming asigna y valida desde `oficina_servicios`.

Secuencia:

```text
1. aceptar servicio
2. investigar deposito_comun
3. matar rata_despensa con M02 activa
4. fijar cadáver tutorial
5. aprender Examen con Chen Bo en sala_anatomica
6. volver y OBSERVAR/EXAMINAR cadáver
7. informar a Tao Ming
```

Reglas de `rata_despensa` durante M02:

- se reutiliza el errante existente; no se crea otro;
- el retiro permanente comienza sólo si muere con M02 activa;
- no reaparece después;
- `EXTRAER` está prohibido;
- no escribe Atlas/bestiario/registro/familiaridad;
- el cadáver se mantiene hasta obtener la información o cerrar M02;
- si el cadáver tutorial falta después de la muerte y el Examen sigue pendiente, se recrea una vez **sin loot nuevo**;
- todo es un wrapper local y no cambia la semántica global de 3C.4.

Cierre: `SERVICIO_DESPENSA_VALIDADO`.

Produce: `primerServicioFormal=true`, Examen aprendido/desbloqueado.

Recompensa: +1 Contribución, 0 Mérito.

### M03 — Aprender a permanecer · `LI_INTEGRACION`

1. **`sala_formas`** — Shen Baojun enseña Piel de Cobre (`M03_PIEL_COBRE_INSTRUIDA`).
2. **`patio_marcial`** — encuentro de misión con `muneco_practica`. Se completa con al menos una respuesta defensiva válida; no exige derrotarlo.
3. **`patio_respiracion`** — `MEDITAR` con éxito, sin combate activo y sin hostiles vivos; no exige llenar 25/25. Produce `EVALUACION_CIRCULACION_SUPERADA`.
4. **`pabellon_disciplina`** — Qiao Ren formaliza la promoción y produce `M03_PROMOCION_FORMALIZADA`.

M03 se cierra con `M03_PROMOCION_FORMALIZADA`.

Produce:

```text
rangoInstitucional = DISCIPULO_EXTERNO
estadoAfiliacion = MIEMBRO
player.facciones.grulla_blanca.estado = miembro
evaluacionCirculacion = SUPERADA
TECNICA_PIEL_COBRE_APRENDIDA = true
```

`manual_piel` no puede enseñar Piel de Cobre antes de M03. Después, si la técnica ya es conocida, no se consume ni añade una nueva mecánica de maestría.

Recompensa: 0.

### M04 — Más allá de la Puerta Roja · `LII_TERRITORIO`

Obligatorios:

```text
puesto_valle          → asignación Jiang Rui
puerta                → control Gao Shun
bosque_refugio_patrulla → destino
puesto_valle          → regreso/informe
```

`bosque_senda_patrulla` queda como tránsito/contexto.

Incidente opcional determinista:

```text
evento: M04_INCIDENTE_FAUNA_DOCUMENTADO
flag:   M04_INCIDENTE_FAUNA_DOCUMENTADO

se dispara una sola vez por:
EXAMINAR tablillas en bosque_puesto_marcas
o
EXAMINAR registro en bosque_refugio_patrulla
durante M04
```

No depende de RNG ni de la presencia real de un errante.

Cierre: `PRIMERA_PATRULLA_VALIDADA`.

Produce: `PATRULLA_TERRITORIAL=true`, refugio conocido.

Recompensa: +2 Contribución; +1 Mérito sólo si ocurrió el incidente opcional.

### M05 — Los caminos de la Grulla · `LII_TERRITORIO`

Duan Shibo asigna en `oficina_logistica`.

No existe ruta cardinal rígida ni checklist de siete rooms.

Requisitos:

```text
1. revisar mercado_valle O granero_valle
2. contactar Xu An en sauces_casa_comunal O sauces_plaza
3. después del contacto, registrar el circuito en sauces_casa_comunal
4. visitar sauces_casa_huespedes
```

`puesto_valle` y `sauces_plaza` pueden funcionar como tránsito/contexto.

Cierre: `RUTA_SAUCES_VALIDADA`.

Produce: `reconocimientoSauces=HUESPED`, casa de huéspedes conocida y `PILDORA_CONSOLIDACION_OTORGADA=true`.

Recompensa: +3 Contribución + Píldora de Consolidación.

Protección anti-soft-lock:

```text
mientras:
PILDORA_CONSOLIDACION_OTORGADA
&& player.etapa < 3
&& !transicionLIILIIIHecha

→ no permitir SOLTAR pildora_consolidacion
→ si falta al cargar/reconciliar, reemitir una sola
```

### M06 — Lo que no debería estar aquí · `LII_TERRITORIO`

Requiere M04 y M05 HECHAS y al menos una observación territorial.

Tipos:

```text
DESPLAZAMIENTO_FAUNA
ALTERACION_VEGETAL
ALTERACION_HIDRICA
PATRON_TERRITORIAL
```

Evaluador:

```text
1 tipo → INSUFICIENTE / sospechaFuerte=false
2 tipos → INSUFICIENTE / sospechaFuerte=true
3 tipos → SUFICIENTE
4 tipos → CONCLUYENTE
```

Repetir el mismo tipo no suma.

Las fuentes se definen mediante tabla externa `(room, scenery) -> tipo` usando scenery ya existente. No se modifican `ROOMS` ni 3C.4.

La evidencia se puede registrar desde que `PATRULLA_TERRITORIAL=true`. `listo()` es state-based: si ya existen tres tipos al activar M06, puede cerrarse sin esperar un nuevo evento.

Cierre: `EVIDENCIA_TERRITORIAL_SUFICIENTE`.

Produce: `arc1.revelaciones.R1=PARCIAL`.

Recompensa: +2 Contribución +1 Mérito.

El cuarto tipo puede seguir registrándose hasta cerrar M07. `CONCLUYENTE` sólo mejora contexto/diálogo.

### M07 — Informe de frontera · `LII_TERRITORIO`

Room: `pabellon_disciplina`.

Participantes:

```text
Qiao Ren  → presencia física
Jiang Rui → presencia física mediante anclaje temporal owner=M07
He Zhen   → no requiere presencia; escritura directa
Ren Bo    → no requiere presencia; escritura directa
Su Lian   → no requiere presencia; escritura directa
```

Al liberar a Jiang Rui se lo reubica atómicamente a `puesto_valle`, fuera de la vista del jugador.

Formulación:

```text
CAUTA
FUERTE
```

Con evidencia `SUFICIENTE`, una formulación FUERTE puede ser cuestionada y corregida sin penalización.
Con `CONCLUYENTE`, ambas son aceptables.

Se persisten:

```text
flags.arc1.informe.formulacion
flags.arc1.informe.corregida
```

No cambian recompensa ni gate.

Cierre: `INFORME_ACEPTADO`.

Produce:

```text
informeFronteraAceptado=true
arc1.revelaciones.R1=CONFIRMADO

Jiang Rui R1=CONFIRMADO
Qiao Ren   R1=CONFIRMADO
He Zhen    R1=SABE
Ren Bo     R1=SABE
Su Lian    R1=SABE

Comprensión +1 one-shot
```

Las escrituras NPC son directas y monotónicas; no existe propagación automática.

Recompensa: +4 Contribución +3 Mérito +1 Comprensión.

## 5. Persistencia

```text
QUESTS
  catálogo P–M07

this.quests
  P–M07 usan activa/hecha
  rumor/fallida permanecen compatibles con el motor si otra definición futura los usa

BLOQUEADA/DISPONIBLE
  derivados; no persistidos

flags.arc1
  estado
  estadoAfiliacion
  rangoInstitucional
  permisos
  evidencia
  informe
  one-shots
  propietario de anclajes

player
  qi/inventario/stats
  facción económica
  recursos

conocimientoNPC
  R1–R10
```

`normalizarArc1()` sanea la estructura conocida de `flags.arc1` y los estados de quests al cargar.
Luego se ejecuta `reconciliarProgresionArc1()`.

No se agrega clave top-level y `SAVE_SCHEMA_VERSION` permanece en 2.

## 6. Compañeros

- Subsistema social opcional paralelo.
- Afinidad no bloquea progreso estructural.
- Prioridad `CRISIS > MISIÓN PRINCIPAL > PERSONAL > AMBIENTAL`.
- Máximo una escena social importante por entrada.
- `posicionNPC` es fuente de verdad.
- `flags.arc1.anclajePropietario[npcId]` impide que una escena social pise un anclaje de misión.
- Liberar un anclaje reubica a una room válida fuera de vista.
- 3C.6 sólo incorpora escenas LI/LII que intersectan P–M07.
- Géneros: Lin F, Han M, Zhao M, Mei F, Guo M, Luo M.

## 7. Estado de salida

Tras cerrar M07 y antes de ejecutar LII→LIII:

```text
P y M01–M07 = HECHAS
arc1.estado = LII_TERRITORIO
rangoInstitucional = DISCIPULO_EXTERNO
estadoAfiliacion = MIEMBRO
player.facciones.grulla_blanca.estado = miembro
primerServicioFormal = true
evaluacionCirculacion = SUPERADA
EXAMEN_ESPIRITUAL_APRENDIDO = true
PATRULLA_TERRITORIAL = true
reconocimientoSauces = HUESPED
evidenciaTerritorial >= SUFICIENTE
informeFronteraAceptado = true
arc1.revelaciones.R1 = CONFIRMADO
SECTA_INTERIOR = false
```

Al ejecutar la transición oficial:

```text
arc1.estado = LIII_INVESTIGACION
transicionLIILIIIHecha = true
SECTA_INTERIOR = true
M12 = false
ATAJO_ALA_* = false
```

## 8. Cambios técnicos obligatorios para el futuro contrato

1. `compruebaPuerta` fail-closed.
2. CONSAGRAR no resta `vasoAnterior` al qi.
3. `otorgarContribucion` y `otorgarMerito` separados; quitar acoplamiento `merito>=saldo`.
4. API de anclaje/liberación atómica + owner en flags.
5. `elevarConocimientoNPC` monotónico.
6. Wrapper local de `rata_despensa`.
7. Tabla externa de evidencia por scenery.
8. `normalizarArc1()` + `reconciliarProgresionArc1()` al cargar.
9. Actualizar tests que asumían `QUESTS={}` o `merito>=saldo`.
10. No modificar `ROOMS.exits` ni número/identidad global de errantes.
11. Mantener `SAVE_SCHEMA_VERSION=2`.

## 9. Pendientes editoriales no bloqueantes

- prosa final de la leyenda pública del Prólogo;
- texto exacto de las tres preguntas del diagnóstico de raíz;
- microprosa/diálogos de escenas sociales LI/LII.

## 10. Siguiente paso

Auditoría corta de cierre de REV3. Si MD y JSON coinciden, no hay soft-locks documentales y no aparece una contradicción nueva con ver74, el siguiente entregable será:

`Contrato_Implementacion_3C6_Prologo_M01_M07.md`