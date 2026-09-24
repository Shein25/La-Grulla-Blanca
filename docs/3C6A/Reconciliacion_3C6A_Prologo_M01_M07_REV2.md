# Reconciliación 3C.6A — Prólogo + M01–M07 — REV2

Fecha: 2026-09-24

## Veredicto

`3C6A_REV2_LISTA_PARA_CONTRATO_IMPLEMENTACION`

REV2 actualiza REV1 al baseline **ver74 / 3C.5 cerrado** e incorpora decisiones humanas aprobadas. Las decisiones humanas se distinguen de los hallazgos documentales; no se reetiquetan como “fuente”.

### Baseline

- `grulla-blanca_ver74.html`
- SHA-256 `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`
- `SAVE_SCHEMA_VERSION = 2`
- 3C.5 NPC: cerrado y auditado

## Decisiones humanas cerradas

### DHP_3C6_01

CONSAGRAR deja de reducir el qi acumulado. LI→LII usa etapa>=2 como evidencia mecánica de haber alcanzado el umbral de 25.

### DHP_3C6_02

servicioTerritorial=COMPLETADO cuando M04 y M05 están HECHAS; M05 se habilita al cerrar M04.

### DHP_3C6_03

evidenciaTerritorial es monotónica: INSUFICIENTE < SUFICIENTE < CONCLUYENTE; gates usan >=SUFICIENTE; campo único informeFronteraAceptado.

### DHP_3C6_04

LI→LII y LII→LIII son transiciones one-shot con presentación visual ceremonial. M07 no abre SECTA_INTERIOR.

### DHP_3C6_05

2→3 requiere qi=45, Píldora de Consolidación, M04+M05, evidencia>=SUFICIENTE e informe aceptado. Se elimina el logro genérico de combate como hard-gate.

### DHP_3C6_06

La raíz se asigna determinísticamente por tres elecciones de diagnóstico; la reacción final ante la Piedra desempata. Sin RNG. Guardia y ayudante quedan como roles genéricos.

### DHP_3C6_07

Madre Wen es la encargada de externos, no la madre biológica. M01 usa registro→sala_jade→patio→patio_cabanas→corredor_cabanas→dormitorio_externos; corredor sólo tránsito.

### DHP_3C6_08

M02 usa la rata de despensa como encuentro tutorial. Tras morir/cerrar M02 no reaparece; no EXTRAER; no bestiario/Atlas/registro; cadáver controlado hasta completar Examen.

### DHP_3C6_09

Condiciones básicas: room sin hostiles vivos y sin combate activo. Piel de Cobre se aprende por primera vez en M03 con Shen Baojun.

### DHP_3C6_10

M04 se asigna/entrega con Jiang Rui en puesto_valle; Gao Shun es checkpoint en puerta; M05 la asigna Duan Shibo desde oficina_logistica y termina con Xu An en Sauces.

### DHP_3C6_11

Evidencia por diversidad: 1 tipo=INSUFICIENTE; 2=INSUFICIENTE/sospecha fuerte; 3=SUFICIENTE; 4=CONCLUYENTE; repetir tipo no suma.

### DHP_3C6_12

M07 se presenta en pabellon_disciplina con Qiao Ren + Jiang Rui; He Zhen recibe copia. Jiang/Qiao R1=CONFIRMADO; He Zhen/Ren Bo/Su Lian R1=SABE.

### DHP_3C6_13

Balance: M02 +1 contrib.; M03 0; M04 +2 contrib. (+1 mérito opcional); M05 +3 contrib. + píldora; M06 +2 contrib. +1 mérito; M07 +4 contrib. +3 mérito +1 Comprensión.

### DHP_3C6_14

QUESTS define P–M07; this.quests persiste activa/hecha; BLOQUEADA/DISPONIBLE derivadas; flags guarda arc1/permisos/evidencia; SAVE_SCHEMA_VERSION sigue en 2.

### DHP_3C6_15

Inicio: título Aspirante, afiliación PENDIENTE_REGISTRO y sin rango. Fin P: ADMITIDO. M01: ASPIRANTE. M03: DISCIPULO_EXTERNO + MIEMBRO. Uniforme/espada se reciben en descansillo.

### DHP_3C6_16

dormitorio_externos se asigna en M01 y queda conocido+visitado. SECTA_EXTERIOR_BASE y PATRULLA_TERRITORIAL son permisos institucionales, no gates físicos.

### DHP_3C6_17

Subsistema social opcional paralelo. Afinidad no bloquea progreso. Prioridad CRISIS > misión principal > personal > ambiental. Máximo una escena social importante por entrada. Géneros: Lin F, Han M, Zhao M, Mei F, Guo M, Luo M.

## Gates reconciliados

### PROLOGO → LI

- `REGISTRO_INICIAL_COMPLETADO` → `PROLOGO=HECHO` + `arc1.estado=LI_INTEGRACION`.

### LI → LII

```text
player.etapa >= 2
+ rango == DISCIPULO_EXTERNO
+ primerServicioFormal == true
+ evaluacionCirculacion == SUPERADA
```

Al cumplirse: transición visual one-shot y `arc1.estado=LII_TERRITORIO`.

### LII → LIII

```text
player.qi >= 45
+ Píldora de Consolidación
+ M04 HECHA
+ M05 HECHA
+ evidenciaTerritorial >= SUFICIENTE
+ informeFronteraAceptado == true
```

`servicioTerritorial=COMPLETADO` equivale a M04+M05. La píldora se consume al CONSAGRAR 2→3. `SECTA_INTERIOR` sólo se abre en la transición oficial a LIII.

## Misiones reconciliadas

### P — La Piedra y la Puerta · `PROLOGO`

- **REQUIERE:** nueva_partida_valida
- **Activación:** automática al crear personaje
- **Rooms:** patio_raices, descansillo, mirador_niebla, patio_practica, sendero_pinos, camino, puerta, registro
- **Objetivos:** diagnóstico de raíz sin RNG; recibir uniforme y espada de madera en descansillo; recorrer acceso hasta registro; REGISTRO_INICIAL_COMPLETADO con Tao Ming
- **Cierre:** `REGISTRO_INICIAL_COMPLETADO`
- **PRODUCE:** estadoAfiliacion=ADMITIDO; PROLOGO=HECHO; arc1.estado=LI_INTEGRACION; raiz persistente
- **ABRE:** M01
- **Recompensas:** `{"contribucion": 0, "merito": 0, "comprension": 0}`

### M01 — Un nombre entre miles · `LI_INTEGRACION`

- **REQUIERE:** PROLOGO=HECHO, arc1.estado=LI_INTEGRACION
- **Activación:** Tao Ming en registro
- **Rooms:** registro, sala_jade, patio, patio_cabanas, corredor_cabanas, dormitorio_externos
- **Objetivos:** NOMBRE_INSCRITO; recibir alojamiento de Madre Wen; llegar a dormitorio_externos
- **Cierre:** `ALOJAMIENTO_CONFIRMADO`
- **PRODUCE:** rango=ASPIRANTE; SECTA_EXTERIOR_BASE; alojamiento dormitorio_externos conocido+visitado
- **ABRE:** M02
- **Recompensas:** `{"contribucion": 0, "merito": 0, "comprension": 0}`

### M02 — Trabajo que alguien debe hacer · `LI_INTEGRACION`

- **REQUIERE:** M01=HECHA
- **Activación:** aceptar servicio de despensa/depósito
- **Rooms:** oficina_servicios, deposito_comun, sala_anatomica
- **Objetivos:** resolver rata tutorial de la despensa; obtener información del cadáver tutorial; aprender Examen Espiritual con Chen Bo
- **Cierre:** `SERVICIO_DESPENSA_VALIDADO`
- **PRODUCE:** primerServicioFormal=true; EXAMEN_ESPIRITUAL_APRENDIDO; profesiones.examen.desbloqueada=true
- **ABRE:** M03
- **Recompensas:** `{"contribucion": 1, "merito": 0, "comprension": 0}`
- **Reglas tutorial:** no respawn tras cierre; no EXTRAER; no bestiario/Atlas/registro; no familiaridad profesional; recuperación controlada del cadáver

### M03 — Aprender a permanecer · `LI_INTEGRACION`

- **REQUIERE:** M01=HECHA, M02=HECHA, room_sin_hostiles_vivos, sin_combate_activo
- **Activación:** Shen Baojun inicia formación
- **Rooms:** patio_marcial, sala_formas, patio_respiracion, pabellon_disciplina
- **Objetivos:** aprender Piel de Cobre; practicar contra muñeco; superar evaluación de circulación
- **Cierre:** `EVALUACION_CIRCULACION_SUPERADA`
- **PRODUCE:** rango=DISCIPULO_EXTERNO; estadoAfiliacion=MIEMBRO; evaluacionCirculacion=SUPERADA; TECNICA_PIEL_COBRE_APRENDIDA
- **ABRE:** gate LI→LII
- **Recompensas:** `{"contribucion": 0, "merito": 0, "comprension": 0}`

### M04 — Más allá de la Puerta Roja · `LII_TERRITORIO`

- **REQUIERE:** arc1.estado=LII_TERRITORIO, rango=DISCIPULO_EXTERNO
- **Activación:** Jiang Rui en puesto_valle
- **Checkpoints:** puesto_valle, puerta, bosque_senda_patrulla, bosque_refugio_patrulla
- **Objetivos:** revisar tramo de patrulla; alcanzar refugio; volver a puesto_valle; dar informe breve
- **Cierre:** `PRIMERA_PATRULLA_VALIDADA`
- **PRODUCE:** PATRULLA_TERRITORIAL; bosque_refugio_patrulla conocido
- **ABRE:** M05
- **Recompensas:** `{"contribucion": 2, "merito_base": 0, "merito_incidente_opcional": 1, "comprension": 0}`

### M05 — Los caminos de la Grulla · `LII_TERRITORIO`

- **REQUIERE:** M04=HECHA
- **Activación:** Duan Shibo en oficina_logistica
- **Checkpoints:** oficina_logistica, puesto_valle, mercado_valle, granero_valle, sauces_plaza, sauces_casa_comunal, sauces_casa_huespedes
- **Objetivos:** paso por Valle/intercambio; llegar a Sauces; hablar con Xu An; registrar modificación del circuito
- **Cierre:** `RUTA_SAUCES_VALIDADA`
- **PRODUCE:** reconocimientoSauces=HUESPED; sauces_casa_huespedes conocido; PILDORA_CONSOLIDACION_OTORGADA
- **ABRE:** M06
- **Recompensas:** `{"contribucion": 3, "merito": 0, "comprension": 0, "item": "pildora_consolidacion"}`

### M06 — Lo que no debería estar aquí · `LII_TERRITORIO`

- **REQUIERE:** M04=HECHA, M05=HECHA, alguna_observacion_anomala
- **Activación:** primer incidente reconocido como anómalo
- **Áreas:** bosques, aguas_barrancos, cantera_vetas
- **Objetivos:** obtener al menos 3 tipos distintos de evidencia
- **Cierre:** `EVIDENCIA_TERRITORIAL_SUFICIENTE`
- **PRODUCE:** evidenciaTerritorial>=SUFICIENTE; arc1.revelaciones.R1=PARCIAL; conocimiento.anomaliasTerritoriales=SOSPECHA_FUERTE
- **ABRE:** M07
- **Recompensas:** `{"contribucion": 2, "merito": 1, "comprension": 0}`
- **Evidencia:** 1 tipo→INSUFICIENTE; 2→INSUFICIENTE/sospecha fuerte; 3→SUFICIENTE; 4→CONCLUYENTE; repetir tipo no suma.

### M07 — Informe de frontera · `LII_TERRITORIO`

- **REQUIERE:** M06=HECHA, evidenciaTerritorial>=SUFICIENTE
- **Activación:** decisión explícita de presentar informe
- **Rooms:** pabellon_disciplina
- **Objetivos:** preparar informe; elegir grado de certeza; aceptar corrección sin penalización
- **Cierre:** `INFORME_ACEPTADO`
- **PRODUCE:** informeFronteraAceptado=true; arc1.revelaciones.R1=CONFIRMADO; jiang_rui.R1=CONFIRMADO; qiao_ren.R1=CONFIRMADO; he_zhen.R1=SABE; ren_bo.R1=SABE; su_lian.R1=SABE; Comprension +1 one-shot
- **ABRE:** gate LII→LIII
- **Recompensas:** `{"contribucion": 4, "merito": 3, "comprension": 1}`

## Balance de recompensas

```text
M02  +1 Contribución
M03   0
M04  +2 Contribución (+1 Mérito sólo por incidente opcional)
M05  +3 Contribución + Píldora de Consolidación
M06  +2 Contribución +1 Mérito
M07  +4 Contribución +3 Mérito +1 Comprensión
```

Total con incidente opcional de M04: **12 Contribución, 4 Mérito, 1 Comprensión y 1 Píldora de Consolidación**. Contribución y Mérito deben otorgarse por canales separados.

## Persistencia

```text
QUESTS          → catálogo P–M07
this.quests     → activa / hecha
flags           → arc1 / afiliación / rango / permisos / evidencia / one-shots
player          → qi / inventario / stats / recursos
conocimientoNPC → R1–R10 individuales
```

`BLOQUEADA` y `DISPONIBLE` son derivados. `SAVE_SCHEMA_VERSION` permanece en 2.

## R1: jugador ≠ NPC

```text
arc1.revelaciones.R1
  M06 → PARCIAL
  M07 → CONFIRMADO

conocimientoNPC[npc].R1
  DESCONOCIDO / SOSPECHA / SABE / CONFIRMADO
```

`PARCIAL` nunca se escribe en `conocimientoNPC`.

## Compañeros

- Subsistema social opcional paralelo.
- Afinidad no bloquea progreso estructural.
- Prioridad: `CRISIS > MISIÓN PRINCIPAL > PERSONAL > AMBIENTAL`.
- Máximo una escena social importante por entrada.
- La posición real 3C.5 es fuente de verdad; misión puede anclar temporalmente.
- 3C.6 sólo incorpora escenas LI/LII que intersecten P–M07.

Géneros cerrados: Lin Yue mujer; Han Qiao hombre; Zhao Wen hombre; Mei Lian mujer; Guo Chen hombre; Luo Yan hombre.

## Estado de salida tras M07

- P y M01–M07 HECHAS.
- `arc1.estado=LII_TERRITORIO` hasta satisfacer y ejecutar el gate LII→LIII.
- `rango=DISCIPULO_EXTERNO`, `estadoAfiliacion=MIEMBRO`.
- `primerServicioFormal=true`, `evaluacionCirculacion=SUPERADA`, Examen aprendido.
- `PATRULLA_TERRITORIAL`, reconocimiento Sauces HUESPED.
- `evidenciaTerritorial>=SUFICIENTE`, `informeFronteraAceptado=true`.
- `arc1.revelaciones.R1=CONFIRMADO`.
- Jiang Rui/Qiao Ren R1 CONFIRMADO; He Zhen/Ren Bo/Su Lian SABE.
- `SECTA_INTERIOR=false` hasta la transición oficial a LIII.

## Pendientes no bloqueantes

- prosa final de la leyenda pública del Prólogo;
- texto exacto de las tres preguntas del diagnóstico de raíz;
- microprosa/diálogos de escenas sociales LI/LII;
- limpieza legacy no-quest que corresponda a M2.

## Siguiente paso

Auditar esta REV2. Si no aparecen contradicciones, redactar `Contrato_Implementacion_3C6_Prologo_M01_M07.md` sin ampliar alcance a M08–M18.