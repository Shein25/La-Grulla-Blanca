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
