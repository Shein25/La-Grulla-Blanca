# Auditoría externa — Behavior Tree v0.1

Audita exclusivamente este laboratorio como experimento independiente.

NO modifiques producción.
NO integres NPC canónicos.
NO añadas Utility AI, GOAP, HTN o pathfinding.
NO hagas merge.

## 1. Suite oficial

```bash
node tests.mjs
```

Reporta PASS, FAIL y exit code reales.

## 2. Stress determinista

```bash
node stress.mjs 100000 1337
node stress.mjs 100000 1
node stress.mjs 100000 42
node stress.mjs 100000 999
node stress.mjs 100000 20260925
```

Digests esperados:

- 1337: `a1a4e7d1e67815751f86e7743e471eb4c31311d67a8de15ca0a664700541d50d`
- 1: `0e6d9ebc1adf385fc50924b62dbc0a74cbb5c3b41b697aa619835f693c12607a`
- 42: `f4f317efdae05ea016a4e4e37b3f6735ec89b63a45b39c0d869ee3014cc7afb1`
- 999: `e3374685a39252364258c598f9a5e40b94eaf772213a29fbc6bddd7793eefbbe`
- 20260925: `9c69171c22e18e8baaee55bc2206de7de9d3a9f6c3ba83ae6d81c414ca4a969f`

Exige:

- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidRuntime = 0`;
- `multiEmit = 0`.

## 3. Ataques adversariales obligatorios

Busca contraejemplos para:

- más de un intent por tick;
- acción RUNNING reemitida incorrectamente;
- resultado de acción aplicado a una acción distinta;
- preempción incorrecta o no determinista;
- selector/sequence con semántica rota;
- prioridades alteradas por orden mutable o aliasing;
- IDs duplicados;
- ciclos de referencias;
- profundidad/número de nodos/hijos fuera de límites;
- arrays sparse, propiedades extra, accessors y Symbols;
- facts con objetos, NaN o Infinity;
- Proxy revocado y traps reflectivos hostiles;
- overflow de `runtime.tick`;
- mutación de tree/runtime/tick;
- contaminación de prototipo;
- `-0` frente a `0`;
- comportamiento de fact ausente con `EQ/NEQ/IN`.

## 4. Propiedad arquitectónica principal

Confirma que el árbol:

```text
reevalúa prioridades
→ selecciona como máximo una acción
→ emite intención
→ executor externo resuelve
```

y que no ejecuta movimiento, combate ni efectos del mundo.

## 5. Fixtures

Son patrones sintéticos, no NPC canónicos:

- guardia reactivo;
- trabajador interrumpible;
- supervisor con prioridades.

No evalúes fidelidad narrativa.

## 6. Entregable

Informe Markdown con entorno, HEAD exacto, integridad, resultados, pruebas independientes, bugs reproducibles y veredicto único:

```text
BEHAVIOR_TREE_V01_APTO_PARA_ITERAR
BEHAVIOR_TREE_V01_REQUIERE_CORRECCIONES
BEHAVIOR_TREE_V01_FALLO_CONCEPTUAL
```
