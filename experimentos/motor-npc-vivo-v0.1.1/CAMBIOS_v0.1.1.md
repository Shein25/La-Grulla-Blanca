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


## Segundo retest — propiedades heredadas

El retest externo sobre el commit `946fd177fa443601233a1be767a4bbaed71bdfc0` detectó que tres usos semánticos de pertenencia podían aceptar propiedades heredadas de JavaScript.

Casos demostrados:

- `knowledge.R1 = "toString"`;
- `relevantKnowledge = "constructor"`;
- `topicId = "toString"`;
- contextos creados con `Object.create(BASE_CONTEXT)`.

Corrección aplicada en la candidata posterior:

1. lista cerrada `KNOWLEDGE_STATES`;
2. `Object.hasOwn()` para campos obligatorios y topic IDs;
3. `isPlainObject()` restringido a prototipo `Object.prototype` o `null`;
4. validación de propiedades propias en contexto de diálogo;
5. pruebas negativas de `toString`, `constructor`, `__proto__`, `R99` e inputs heredados;
6. preflight adversarial añadido a cada stress run.

No se modificaron pesos, personalidad, dutyMode, inercia, raw tie-break ni comportamiento canónico del juego.


## Tercer candidato — getters/setters

El segundo retest demostró un caso TOCTOU: una propiedad propia implementada como getter podía devolver un valor válido durante la validación y otro inválido durante el cálculo.

Política elegida: **rechazo**, no snapshot implícito.

El contrato experimental define NPC y contextos como registros de datos. Los campos consumidos por el motor deben ser propiedades propias de datos.

Cambios:

1. helper `readOwnData()` basado en `Object.getOwnPropertyDescriptor()`;
2. ningún getter se ejecuta para validar;
3. accessors rechazados en estructura NPC, traits, vínculos, knowledge y behaviorState;
4. accessors rechazados en contexto de acción y diálogo;
5. pruebas negativas con getters que intentarían cambiar a `toString`, `constructor` o `NaN`;
6. stress preflight verifica que esos getters se rechacen y que el contador de lecturas permanezca en 0.

No se cambió el cálculo de utilidad.
