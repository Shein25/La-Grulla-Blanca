# Continuar laboratorio de experimentos — La Grulla Blanca

Quiero continuar exclusivamente el trabajo del laboratorio experimental de La Grulla Blanca.

Repositorio:

`https://github.com/Shein25/La-Grulla-Blanca`

Antes de responder o modificar nada:

1. leé íntegramente:
   `experimentos/backups/HANDOFF_MAESTRO_EXPERIMENTOS_2026-09-24.md`;
2. prestá especial atención a las secciones de actualización 2026-09-25;
3. verificá el HEAD real de cualquier rama implicada;
4. no asumas que una candidata local existe en GitHub;
5. no mergees nada sin orden explícita.

## Reglas permanentes

- no trabajar sobre producción;
- no tocar `main` salvo pedido explícito;
- no convertir fixtures experimentales en canon;
- no mezclar ramas experimentales entre sí;
- toda auditoría externa debe identificar agente/modelo/HEAD cuando exista HEAD;
- un PASS externo no sustituye auditoría independiente;
- toda decisión arquitectónica importante, nueva versión, corrección relevante o implementación próxima debe registrarse en el backup maestro.

## Frentes actuales

### Monster Combat AI v0.1

Objetivo:

`Deterministic Decision Kernel`

Rama futura:

`experiment/monster-combat-ai-v0.1`

La candidata recibida fue LOCAL; todavía no existe rama real ni PR.

Estado independiente actual:

`MONSTER_COMBAT_AI_V01_REQUIERE_CORRECCIONES`

REV2 pendiente por:

1. reorder invariance con jitter;
2. cooldowns estrictamente booleanos;
3. métricas de stress que midan realmente lo que nombran.

No integrar Adaptive Ecology dentro de esta REV2.

### Adaptive Ecology v0.1

Estado:

```text
ESPECIFICACIÓN EN REVISIÓN
NO IMPLEMENTAR TODAVÍA
```

Rama futura:

`experiment/monster-ecology-adaptation-v0.1`

Responsabilidad:

```text
Population State
→ Pressure Resolver
→ Adaptation Resolver
→ activeAdaptations
→ effectiveKit
→ FIN v0.1
```

Claude debe revisar conceptualmente la especificación antes de implementación.

## Separación

```text
Adaptive Ecology
→ effectiveKit
→ Monster Decision Kernel
```

Adaptive Ecology no decide acciones.
Monster AI no conoce pressure/kills/tier/decay.

## Continuidad

Si aparece nueva evidencia, una nueva REV, un veredicto o una decisión arquitectónica importante:

1. verificarla;
2. actualizar el backup maestro;
3. recién después avanzar al siguiente hito cuando corresponda.
