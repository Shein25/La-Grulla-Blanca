# Reconciliación 3C.6A — Prólogo + M01–M07 — REV3.1

Fecha: 2026-09-24

## Veredicto

`3C6A_REV3_1_LISTA_PARA_AUDITORIA_FINAL`

REV3.1 es la corrección documental de REV3 posterior a `Auditoria_Cierre_3C6A_REV3_CLAUDE.md`.
Resuelve N-01…N-10 y sincroniza las omisiones D1–D7. No implementa código y no amplía alcance a M08–M18.

### Baseline

- `grulla-blanca_ver74.html`
- SHA-256 `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`
- `SAVE_SCHEMA_VERSION = 2`
- 3C.5 cerrado/auditado
- REV3 auditada: `3C6A_REV3_REQUIERE_CORRECCIONES`

## 1. Invariantes

```text
329 rooms
17 areas
787 directed exits
0 broken reciprocity
0 isolated rooms
1 physical component
```

Además:

- no modificar `ROOMS.exits`;
- no agregar/quitar errantes globales;
- no modificar globalmente 3C.4;
- sin tiempo diegético;
- `SECTA_INTERIOR=false => M12=false => ATAJO_ALA_*=false`;
- `SAVE_SCHEMA_VERSION=2`.

## 2. Modelo de estado

### Narrativo/institucional

```text
flags.arc1.estado
  PROLOGO
  LI_INTEGRACION
  LII_TERRITORIO
  LIII_INVESTIGACION

flags.arc1.estadoAfiliacion
  PENDIENTE_REGISTRO
  ADMITIDO
  MIEMBRO

flags.arc1.rangoInstitucional
  SIN_RANGO
  ASPIRANTE
  DISCIPULO_EXTERNO
```

Los gates narrativos usan `rangoInstitucional`, nunca `rangoFaccion()`.

### Económico

`player.facciones.grulla_blanca` conserva saldo, mérito y rango económico.

Nueva partida:

```text
player.facciones.grulla_blanca.estado = inactivo
```

M03 sincroniza:

```text
estadoAfiliacion = MIEMBRO
player.facciones.grulla_blanca.estado = miembro
```

Si una facción ya está `expulsado`, la normalización nunca la promociona automáticamente.

## 3. Economía REV3.1

```text
otorgarContribucion(n) → sólo saldo
otorgarMerito(n)       → sólo mérito
```

`normalizarFacciones()` deja de:

- forzar `merito >= saldo`;
- convertir un estado explícito `inactivo` en `miembro`.

Ver74 confirma que `otorgarContribucion()` sólo rechaza `expulsado`, por lo que M02 puede otorgar contribución con estado `inactivo`.

Los llamadores existentes a auditar son:

```text
entregarRecompensa()
test de persistencia
otorgarContribucion() (definición)
```

El historial debe distinguir una entrada de contribución de una de mérito.

Totales P–M07:

```text
Contribución: 12
Mérito:       4 sin incidente M04
              5 con incidente M04
Comprensión:  1
Píldora:      1
```

Los servicios económicos de mérito 8/20 no son objetivo alcanzable durante LII en una partida nueva. Es intencional: la Píldora necesaria para LIII proviene de M05.

## 4. Gates

### LI → LII

```text
player.etapa >= 2
rangoInstitucional == DISCIPULO_EXTERNO
primerServicioFormal == true
evaluacionCirculacion == SUPERADA
```

Evaluar en:

- cierre M03;
- CONSAGRAR 1→2;
- carga/migración;
- reconciliación posterior a cierres P–M07.

One-shot: `transicionLILIIHecha`.

### LII → LIII

Partida nueva:

```text
CONSAGRAR 2→3 con qi>=45
+ pildora_consolidacion
+ M04 HECHA
+ M05 HECHA
+ evidencia >= SUFICIENTE
+ informeFronteraAceptado
```

Evaluar/reconciliar tras:

```text
cierres M04/M05/M06/M07
CONSAGRAR 2→3
carga/migración
```

One-shot: `transicionLIILIIIHecha`.

Efecto:

```text
arc1.estado=LIII_INVESTIGACION
SECTA_INTERIOR=true
M12=false
ATAJO_ALA_*=false
presentación ceremonial one-shot
```

`compruebaPuerta` es fail-closed: requisito desconocido **bloquea y reporta antes de cualquier consumo**.

## 5. Migración de saves ver74

Discriminante:

```text
flags.arc1 AUSENTE
  → save schema2 legacy válido: migrar

flags.arc1 PRESENTE Y VÁLIDO
  → no migrar; normalizar + reconciliar

flags.arc1 PRESENTE PERO INVÁLIDO
  → fallar cerrado; no tratarlo como legacy
```

P–M03 quedan `hecha`; M04–M07 deben jugarse.

One-shots fijados en migración:

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

También se marca `dormitorio_externos` conocido/visitado.

Etapa:

```text
1   → LI_INTEGRACION; transicionLILIIHecha=false
2   → LII_TERRITORIO; transicionLILIIHecha=true
>=3 → LII_TERRITORIO; transicionLILIIHecha=true; cultivoLIIIPreexistente=true
```

Si un save legacy trae `SECTA_INTERIOR=true`, REV3.1 guarda `legacySectaInteriorPrevia=true` sólo para diagnóstico y normaliza:

```text
SECTA_INTERIOR=false
M12=false
ATAJO_ALA_*=false
```

hasta completar M04–M07 y la transición oficial. No hay consumo retroactivo de píldora en etapa≥3.

## 6. Anclajes de misión

`hasta` es un identificador simbólico de evento/condición, nunca una fecha/hora/turno diegético.

| NPC | Owner | Room | Hasta | Liberación |
|---|---|---|---|---|
| Tao Ming | P | `registro` | `REGISTRO_INICIAL_COMPLETADO` | transferir owner a M01 sin mover |
| Tao Ming | M01 | `registro` | `NOMBRE_INSCRITO` | reubicar a `oficina_servicios` fuera de vista |
| Madre Wen | M01 | `patio_cabanas` | `ALOJAMIENTO_CONFIRMADO` | limpiar anclaje; ya es posición válida |
| Tao Ming | M02 | `oficina_servicios` | `SERVICIO_DESPENSA_VALIDADO` | limpiar anclaje |
| Chen Bo | M02 | `sala_anatomica` | `EXAMEN_ESPIRITUAL_APRENDIDO` | limpiar anclaje |
| Shen Baojun | M03 | `sala_formas` | `M03_PIEL_COBRE_INSTRUIDA` | limpiar anclaje |
| Qiao Ren | M03 | `pabellon_disciplina` | `M03_PROMOCION_FORMALIZADA` | limpiar anclaje |
| Jiang Rui | M04 | `puesto_valle` | `M04_RETORNO_INFORMADO` | limpiar al cierre |
| Gao Shun | M04 | `puerta` | `M04_CONTROL_PUERTA` | tras salir de `puerta`, reubicar a `casa_guardia` fuera de vista |
| Jiang Rui | M07 | `pabellon_disciplina` | `INFORME_ACEPTADO` | al cerrar, escena de salida + reubicación a `puesto_valle` |

Reglas:

- un owner de misión activo no puede ser preemptado por CRISIS/PERSONAL/AMBIENTAL;
- `CRISIS > MISIÓN > PERSONAL > AMBIENTAL` sólo ordena escenas físicamente elegibles;
- owner sin anclaje al cargar → descartar owner;
- anclaje sin owner de misión → el subsistema social no lo libera;
- owner cuya misión ya no está activa → reconciliar/liberar según la tabla;
- anclar/liberar/reubicar es una mutación síncrona.

## 7. P y M01

P mantiene la REV3:

- diagnóstico de raíz determinista;
- equipo one-shot en `descansillo`;
- guardia/ayudante genéricos;
- Tao Ming en `registro`.

M01:

```text
registro → sala_jade → patio → patio_cabanas → corredor_cabanas → dormitorio_externos
```

`NOMBRE_INSCRITO` libera a Tao Ming hacia `oficina_servicios`; así queda disponible para M02.

## 8. M02

Secuencia robusta:

```text
HABLAR Tao Ming en oficina_servicios
→ investigar deposito_comun
→ resolver rata_despensa durante M02
→ fijar cadáver tutorial
→ aprender Examen con Chen Bo
→ OBSERVAR/EXAMINAR cadáver
→ HABLAR Tao Ming
```

Si Examen ya estaba aprendido por un save/migración válida, no se obliga a repetir la enseñanza.

La rata:

- es el errante existente `rata_despensa`;
- sólo queda retirada permanentemente si muere con M02 activa;
- no EXTRAER;
- no Atlas/bestiario/familiaridad;
- cadáver persistente mientras se necesite;
- recuperación una vez sin loot si faltara;
- sin alterar 3C.4 global.

## 9. M03

### Enseñanza

Shen Baojun enseña Piel de Cobre en `sala_formas`.

### Práctica

En `patio_marcial`, mientras `M03_PRACTICA_MUNECO_COMPLETADA=false`, se deriva una instancia de `muneco_practica`.

Se completa **exactamente** cuando:

```text
el jugador usa con éxito piel_cobre
durante el encuentro contra muneco_practica
```

No exige derrotarlo ni recibir daño.

Si el muñeco muere/desaparece antes, o se carga una partida con el paso pendiente, se recrea. No se agrega a `ROOMS`, no da loot de misión.

### Evaluación

En `patio_respiracion`, `cmd_meditar` marca `EVALUACION_CIRCULACION_SUPERADA`:

```text
después de comprobar:
- sin combate activo
- sin hostiles vivos

pero antes de:
- comprobar qi>=qi_max
- intentar CONSAGRAR
```

Por lo tanto un vaso lleno no puede bloquear M03. Cuenta aunque la acción no gane qi.

Qiao Ren cierra M03 en `pabellon_disciplina`.

## 10. M04

Checkpoints:

```text
M04_ASIGNADA
  HABLAR jiang_rui @ puesto_valle

M04_CONTROL_PUERTA
  HABLAR gao_shun @ puerta
  (evento; nunca visitadas)

M04_REFUGIO_ALCANZADO
  ENTER bosque_refugio_patrulla con M04 activa

M04_RETORNO_INFORMADO
  HABLAR jiang_rui @ puesto_valle
```

Incidente opcional:

```text
EXAMINAR tablillas @ bosque_puesto_marcas
O
EXAMINAR registro @ bosque_refugio_patrulla
```

Ambos scenery existen en ver74.

El primer disparo:

1. fija `M04_INCIDENTE_FAUNA_DOCUMENTADO=true`;
2. otorga +1 Mérito;
3. nunca vuelve a otorgarlo.

El cierre de M04 no recomputa ese mérito.

## 11. M05

Todos los checkpoints cuentan sólo **después de activar M05**; `visitadas` históricas no sirven.

```text
M05_VALLE_LOGISTICA_REVISADA
  ENTER mercado_valle O granero_valle

M05_XU_AN_CONTACTADO
  HABLAR xu_an @ sauces_casa_comunal O sauces_plaza

M05_CIRCUITO_REGISTRADO
  EXAMINAR registros @ sauces_casa_comunal
  requiere M05_XU_AN_CONTACTADO

M05_HOSPEDAJE_VISITADO
  ENTER sauces_casa_huespedes
```

`registros` existe como scenery de `sauces_casa_comunal`.

M05 cierra cuando están los cuatro flags.

### Píldora anti-soft-lock/anti-exploit

Mientras:

```text
PILDORA_CONSOLIDACION_OTORGADA
&& etapa < 3
&& !transicionLIILIIIHecha
```

cualquier remoción/transferencia de `pildora_consolidacion` se rechaza, salvo el consumidor autorizado `CONSAGRAR_2_3`.

La guarda cubre SOLTAR y cualquier VENDER/DEPOSITAR/ENTREGAR/TRANSFERIR/limpieza de muerte presente o futura.

Reemisión:

```text
si falta
&& PILDORA_REEMITIDA=false
→ fijar PILDORA_REEMITIDA=true
→ agregar exactamente una

PILDORA_REEMITIDA=true
→ nunca reemitir otra
```

## 12. M06

Activación state-based en `reconciliarProgresionArc1()`:

```text
M04=HECHA
&& M05=HECHA
&& evidenciaTerritorial.tipos.size >= 1
&& M06 no activa/hecha
→ activar M06
```

Por tanto, reunir evidencia antes de cerrar M05 no puede bloquear la misión.

Evaluador:

```text
1 tipo → INSUFICIENTE, sospechaFuerte=false
2 tipos → INSUFICIENTE, sospechaFuerte=true
3 tipos → SUFICIENTE, sospechaFuerte=true
4 tipos → CONCLUYENTE, sospechaFuerte=true
```

`nivel` y `sospechaFuerte` son derivados de `tipos` al cargar/reconciliar.

Tabla concreta `(room, scenery) → tipo`:

| Tipo | Fuente 1 | Fuente 2 |
|---|---|---|
| DESPLAZAMIENTO_FAUNA | `bosque_collado_alto.huellas` | `aguas_poza_profunda.marcas` |
| ALTERACION_VEGETAL | `aguas_senda_bosque.vegetacion` | `terraza_cantera.vegetacion` |
| ALTERACION_HIDRICA | `aguas_cauce_alto.corriente` | `aguas_paso_piedras.corriente` |
| PATRON_TERRITORIAL | `bosque_puesto_marcas.tablillas` | `bosque_refugio_patrulla.registro` |

La tabla vive fuera de `ROOMS`. Cada tipo tiene dos fuentes independientes.

## 13. M07

Activación:

```text
HABLAR qiao_ren @ pabellon_disciplina
con M06=HECHA y evidencia>=SUFICIENTE
```

Al activar se ancla Jiang Rui con owner `M07`.

Formulación determinista:

```text
CAUTA + SUFICIENTE/CONCLUYENTE
→ final=CAUTA, corregida=false, cerrar

FUERTE + CONCLUYENTE
→ final=FUERTE, corregida=false, cerrar

FUERTE + SUFICIENTE
→ corrección institucional automática
→ final=CAUTA, corregida=true
→ cerrar sin penalización
```

No existe rama de rechazo que pueda bloquear M07.

Persistencia:

```text
flags.arc1.informe.formulacionFinal
flags.arc1.informe.corregida
```

Jiang Rui se libera sólo al cerrar.

## 14. Normalización al cargar

- quest desconocida → descartar/no-hecha; nunca promover;
- downstream HECHA con requisito previo no HECHO → degradar fail-closed;
- `nivel` y `sospechaFuerte` → recalcular desde tipos;
- `informeFronteraAceptado` → derivar de M07=HECHA;
- `arc1.estado` → no puede superar lo sostenido por etapa + quests + flags válidos;
- owner/anclaje → reconciliar según tabla;
- luego ejecutar `reconciliarProgresionArc1()`.

## 15. Requisitos técnicos del futuro contrato

1. `compruebaPuerta` bloquea y reporta requisitos desconocidos antes de consumo.
2. CONSAGRAR no resta el vaso anterior.
3. Separar contribución/mérito y sus historiales.
4. Inicializar facción como `inactivo`; M03 pasa a `miembro`.
5. Auditar todos los callers de `otorgarContribucion`.
6. Anclajes atómicos con owner y `hasta` simbólico.
7. Anclajes de misión no preemptibles.
8. `elevarConocimientoNPC` monotónico.
9. Wrapper local de rata M02.
10. Instancia recreable del muñeco M03.
11. Hook de MEDITAR antes de vaso lleno.
12. Eventos M04/M05, no `visitadas` históricas.
13. Guardia central de píldora + máximo una reemisión.
14. Tabla externa de evidencia de 8 fuentes.
15. M06 activa/cierra state-based.
16. `normalizarArc1` + migración discriminada + reconciliación.
17. Reemplazar stub `gestionarMisionesNpc`.
18. Actualizar tests `QUESTS={}` y `merito>=saldo`.
19. No tocar `ROOMS.exits` ni identidad/cantidad global de errantes.
20. Mantener schema 2.

## 16. Siguiente paso

Auditoría final corta de REV3.1. Si no quedan soft-locks documentales ni divergencias MD↔JSON:

`3C6A_REV3_1_APTA_PARA_CONTRATO`

y se redacta `Contrato_Implementacion_3C6_Prologo_M01_M07.md`.
