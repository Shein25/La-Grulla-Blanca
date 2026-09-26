# Canonical NPC Behavior Lab v0.1

Laboratorio para observar cómo se comportan NPC canónicos sobre motores ya auditados antes de integrarlos al juego.

## Regla principal

Se mantienen separadas dos capas:

### CANON

Datos copiados literalmente de la definición canónica del NPC: identidad, rol, rooms, movilidad, rutas, anclajes y conocimiento.

### POLÍTICA EXPERIMENTAL

Reacciones que todavía estamos probando: patrullar, observar, advertir, bloquear paso, volver al puesto, etc.

Una política experimental **no se convierte en canon** por estar en este laboratorio.

## Sujetos actuales

1. `gao_shun` — Guardia de la Puerta Roja.
2. `pei_luo` — Responsable de Cocina/Comedor.
3. `jiang_rui` — Capitán de patrulla.
4. `qiao_ren` — Disciplina y Administración.
5. `lin_yue` — Aspirante, enlace territorial/rutas.
6. `han_qiao` — Aspirante, recursos/contactos y logística.
7. `zhao_wen` — Aspirante, piezas documentales / análisis.
8. `mei_lian` — Aspirante, saber médico/local y puente Secta-Sauces.
9. `guo_chen` — Aspirante, trabajo material/persistencia.
10. `luo_yan` — Aspirante, protocolo/historia oficial.
11. `wei_jian` — Autoridad marcial / Pabellón Marcial.
12. `song_rui` — Responsable de Archivos.
13. `lan_meihua` — Medicina / Alquimia.
14. `duan_shibo` — Recursos / Producción.
15. `he_zhen` — Formaciones / Territorio.
16. `ji_xueying` — Maestra de Secta, anclada en Consejo.

Motivo: es funcional, tiene movilidad `RUTA`, territorio y ruta documentados, y permite comparar limpiamente FSM contra Behavior Tree.

## Motores congelados usados

- `vendor/fsm-engine.mjs`
  - fuente: `snapshot/npc-reactive-routine-fsm-v0.1-rev2-audited`
  - blob fuente: `91bb6a67188fd9613d9519658f283ff036d491f4`
- `vendor/bt-engine.mjs`
  - fuente: `snapshot/npc-behavior-tree-v0.1-rev2-audited`
  - blob fuente: `94f452866dc566af15dde0dac66f12f13c0cf5fe`

Las copias no deben editarse dentro del laboratorio.

## Escenarios Gao Shun

1. rutina/patrulla;
2. escalada sospecha → advertencia → hostilidad;
3. patrulla interrumpida por amenaza.

## Qué medimos

- cumplimiento del perfil canónico;
- intents fuera de whitelist;
- latencia de reacción;
- secuencia temporal;
- preempción;
- recuperación a rutina;
- mutación accidental del perfil canónico.

No se evalúan todavía diálogo, combate real, pathfinding ni movimiento físico por rooms.

## Ejecutar

```bash
node tests/gao-shun.test.mjs
node run-gao-shun.mjs
```

## Estado

`LAB_STATUS: GAO_SHUN_BASELINE_CREATED`


## Escenarios Pei Luo

1. rutina experimental cocina → comedor → cocina;
2. crisis M16 durante servicio;
3. crisis M16 durante preparación.

Resultado baseline: `21 PASS / 0 FAIL`.

Hallazgo provisional:

- en rutina normal FSM y Behavior Tree producen la misma secuencia observable;
- en crisis la FSM representa un estado `CRISIS` explícito;
- el Behavior Tree preempta inmediatamente la acción normal activa.

No se ha elegido todavía arquitectura definitiva para Pei Luo.


## Escenarios Jiang Rui

Motores comparados: FSM, Behavior Tree y Utility AI v0.1.1.

1. patrulla ordinaria;
2. anomalía leve sin superior;
3. anomalía grave sin superior;
4. anomalía leve con superior alcanzable;
5. fuera del puesto;
6. crisis de rutas M16.

Resultado baseline: `44 PASS / 0 FAIL`.

Hallazgo provisional:

- FSM y Behavior Tree aplican una política categórica de este laboratorio;
- Utility varía la decisión según magnitud/contexto;
- con el perfil experimental actual, una anomalía leve sin superior no basta para abandonar patrulla;
- una anomalía leve con superior disponible induce `informar_superior`;
- una anomalía grave sin superior induce `investigar`.

Los traits de Utility son de calibración y NO son canon de Jiang Rui.


## Qiao Ren — baseline avanzado

Stack probado:

```text
Scheduler → Memory/Relations → Utility → GOAP → Execution Session
```

Resultado: `13 PASS / 0 FAIL`.

Confirmado:

- deber institucional → `FULFILL_DUTY` → `cumplir_deber`;
- coordinación M16 con evidencia → `REPORT_SUPERIOR` → `ir_superior → informar_superior`;
- fuera del puesto → `RETURN_POST`;
- M17 exige autorización de `NUCLEO_PROFUNDO`, capacidad que GOAP actual no representa.

El gap M17 se registra como límite del motor, no se rellena con conducta inventada.


## Lin Yue — baseline de compañero

Stack probado:

```text
Memory → Relations → Utility → GOAP → Execution Session
```

Resultado: `15 PASS / 0 FAIL`.

Caso central:

```text
sin memoria
→ hablar_jugador
→ sin plan GOAP

PLAYER_HELPED_ME
→ afinidad/confianza/deuda derivadas aumentan
→ ayudar_jugador
→ HELP_PLAYER
→ ir_jugador
→ ayudar_jugador
→ GOAL_REACHED
```

Las relaciones base permanecen inmutables.

Gap detectado:

- M16 exige que Lin Yue vaya a RUTAS por iniciativa propia;
- el stack avanzado actual no implementa navegación física por rooms;
- se registra como gap de capacidad, no se simula falsamente.


## Han Qiao — baseline de logística

Resultado: `14 PASS / 0 FAIL`.

Contraste confirmado:

```text
deber bajo + jugador pide ayuda
→ ayudar_jugador

M16 Recursos + deber alto
→ trabajar
→ FULFILL_DUTY
→ cumplir_deber
```

Gap detectado:

- el GOAP actual sólo representa `dutySatisfied`;
- no hay cantidades, inventario, carros, destinos ni reparto de recursos;
- `RESOURCE_ALLOCATION_AND_LOGISTICS` queda como capacidad de dominio pendiente.


## Zhao Wen — baseline de conocimiento

Resultado: `15 PASS / 0 FAIL`.

Invariante confirmado:

```text
conocimiento = DESCONOCIDO
→ NO_SABE
→ disclosure = 0
```

Ni confianza, afinidad, deuda, respeto ni rango alto del jugador pueden revelar conocimiento inexistente.

Gap detectado:

- M09 requiere `ARCHIVO_RESTRINGIDO` concedido por Qiao Ren;
- el stack GOAP actual no representa ese permiso;
- queda como capacidad institucional pendiente.


## Mei Lian — baseline de frente condicional

Resultado: `13 PASS / 0 FAIL`.

Canon M16:

`SAUCES o MEDICINA según estado y responsables disponibles`.

Resultado del stack actual:

```text
SAUCES   → trabajar → FULFILL_DUTY
MEDICINA → trabajar → FULFILL_DUTY
```

La identidad del frente se pierde.

Gap confirmado:

`M16_FRONT_ASSIGNMENT_SAUCES_OR_MEDICINA`

Hace falta una capa de dominio para frente, estado, responsables, asignación y navegación.


## Guo Chen — baseline de decisión irreversible

Resultado: `14 PASS / 0 FAIL`.

Hallazgo:

```text
trabajo material M16
→ FULFILL_DUTY

Segunda Rama mal codificada como duty
→ FULFILL_DUTY
```

El stack genérico no puede distinguir ambas semánticas.

Guardia obligatoria:

`EXECUTE_SECOND_BRANCH_GRAFT`

no debe poder entrar por `FULFILL_DUTY`.


## Luo Yan — baseline de conocimiento y epílogo

Resultado: `14 PASS / 0 FAIL`.

Gaps confirmados:

```text
R5 = SABE
→ no cabe en knowledge R1-R3
→ KNOWLEDGE_SCHEMA_R1_TO_R10 pendiente
```

y:

```text
LIBERAR / CUSTODIAR
→ no existe como outcome de dominio
→ LIBERAR_CUSTODIAR_DOMAIN_OUTCOME pendiente
```

R1 sí se representa correctamente como SOSPECHA sin fabricar certeza.


## Wei Jian — baseline marcial reactivo

Resultado: `17 PASS / 0 FAIL`.

Behavior Tree experimental:

```text
highThreat   → RESPOND_SECURITY
suspicious   → INVESTIGATE_MARTIAL_ANOMALY
trainingDue  → SUPERVISE_TRAINING
```

La amenaza preempta entrenamiento activo y, al finalizar, la rutina puede reanudarse.

Gaps preservados:

- combate físico;
- navegación por rooms;
- gate `SECTA_INTERIOR`.


## Autoridades — bloque completo

Los siete NPC de categoría `autoridad` ya tienen baseline:

```text
Qiao Ren     13/13
Wei Jian     17/17
Song Rui     13/13
Lan Meihua   11/11
Duan Shibo   10/10
He Zhen      11/11
Ji Xueying   13/13
TOTAL        88/88 PASS
```

Hallazgos transversales:

- un NPC anclado como Ji Xueying no necesita una arquitectura compleja para presencia básica;
- Behavior Tree encaja bien como hipótesis reactiva para Wei Jian;
- dominios Archivo, Medicina, Recursos y Formaciones requieren estado de mundo específico antes de que `FULFILL_DUTY` deje de ser una abstracción booleana;
- el esquema de conocimiento R1-R3 es insuficiente para varios NPC de autoridad.
