# Auditoría externa — Reactive Routine FSM v0.1

Audita exclusivamente este laboratorio como experimento independiente.

NO modifiques producción.
NO integres NPC canónicos.
NO añadas Utility AI, GOAP, Behavior Trees o pathfinding.
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

Para cada seed verifica:

- digest repetible;
- `nondeterministicMismatches = 0`;
- `inputMutations = 0`;
- `invalidStates = 0`.

## 3. Propiedades obligatorias

Busca contraejemplos para:

- más de una transición física por un único evento;
- target inexistente;
- prioridades empatadas;
- guardas ambiguas;
- orden del array alterando resultados cuando priorities son distintas;
- mutación de machine/runtime/event;
- NaN/Infinity;
- campos heredados;
- getters/setters;
- Proxy hostil / TOCTOU;
- Symbols;
- intents duplicados;
- callbacks escondidos dentro de la definición;
- estados imposibles o loops instantáneos.

## 4. Fixtures

Confirma que las tres máquinas representan sólo patrones sintéticos:

- guardia reactivo;
- trabajador con rutina;
- patrullero reactivo.

No evalúes fidelidad narrativa de NPC canónicos.

## 5. Arquitectura

Evalúa si v0.1 mantiene correctamente esta frontera:

```text
FSM decide estado/intención
        ↓
executor futuro aplica efectos reales
```

La FSM no debe mutar el mundo ni resolver navegación/combate.

## 6. Entregable

Devuelve un informe con:

- entorno;
- HEAD auditado;
- resultados exactos;
- bugs reproducibles;
- riesgos arquitectónicos;
- veredicto final único:

```text
REACTIVE_ROUTINE_FSM_V01_APTO_PARA_ITERAR
REACTIVE_ROUTINE_FSM_V01_REQUIERE_CORRECCIONES
REACTIVE_ROUTINE_FSM_V01_FALLO_CONCEPTUAL
```
