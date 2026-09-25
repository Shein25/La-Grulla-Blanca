# Canonical NPC Behavior Lab v0.1

Laboratorio para observar cómo se comportan NPC canónicos sobre motores ya auditados antes de integrarlos al juego.

## Regla principal

Se mantienen separadas dos capas:

### CANON

Datos copiados literalmente de la definición canónica del NPC: identidad, rol, rooms, movilidad, rutas, anclajes y conocimiento.

### POLÍTICA EXPERIMENTAL

Reacciones que todavía estamos probando: patrullar, observar, advertir, bloquear paso, volver al puesto, etc.

Una política experimental **no se convierte en canon** por estar en este laboratorio.

## Primer sujeto

`gao_shun` — Guardia de la Puerta Roja.

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
