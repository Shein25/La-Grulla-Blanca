# Cambios v0.1 → v0.1.1

Fuente de cambios: auditoría externa de `Informe_Test_Motor_NPC_Vivo_v0.1.md`.

## Correcciones de alta prioridad

### B1
Antes: campos ausentes en `traits` o `relationPlayer` se convertían de facto en cero.

Ahora: schema estricto y error antes de puntuar.

### B2
Antes: `nextNpc` compartía objetos internos con el estado anterior.

Ahora: `structuredClone()` y prueba explícita de independencia profunda.

## Riesgos de diseño tratados

### Clamp a 100
Antes: dos acciones clampadas a 100 se resolvían sólo por orden fijo.

Ahora: `raw` desempata antes de `ACTION_ORDER`.

### Inercia
Antes: `lastAction` daba +6 indefinidamente.

Ahora: `behaviorState` lleva racha y el bono decae 6 → 4 → 2 → 0.

### Trabajar / esperar
Antes: `trabajar` y `esperar` eran casi inaccesibles en el stress.

Ahora: el mundo declara el deber existente mediante `dutyMode`. Se añadieron escenarios de aceptación donde `trabajar` y `esperar` deben ganar por razones semánticas, no por uniformar frecuencias.

## Decisión arquitectónica nueva

`dutyMode` funciona como una primera precondición explícita.

No es GOAP, pero evita que acciones conceptualmente imposibles compitan sólo porque sus pesos existen.
