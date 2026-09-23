# Motor NPC Vivo v0.2 — Laboratorio GOAP

Primera iteración experimental posterior a v0.1.1.

## Regla de seguridad

Este directorio sigue aislado del juego de producción.

- no se importa desde `grulla-blanca_ver73.html`;
- no usa los 32 NPC canónicos;
- no usa topología canónica;
- no implementa misiones;
- no modifica el baseline del Arco 1.

Los tres NPC continúan siendo fixtures ficticios heredados del laboratorio v0.1.1.

## Arquitectura

```text
Utility AI
   ↓
selecciona OBJETIVO
   ↓
GOAP
   ↓
construye PLAN mínimo
   ↓
Executor
   ↓
ejecuta un paso
   ↓
verifica precondiciones
   ├─ siguen válidas → continuar
   └─ cambiaron      → REPLAN_REQUIRED
```

### Utility AI

`goal-selector.mjs` ya no selecciona directamente una acción.

Selecciona uno de estos objetivos experimentales:

- HELP_PLAYER
- INVESTIGATE_ANOMALY
- REPORT_SUPERIOR
- FULFILL_DUTY
- RETURN_POST
- WAIT_SAFE

Las personalidades siguen influyendo en la utilidad.

En el mismo mundo base:

- Disciplinado → FULFILL_DUTY
- Leal → HELP_PLAYER
- Curioso → INVESTIGATE_ANOMALY

### GOAP

`goap.mjs` recibe:

- estado inicial;
- condiciones objetivo;
- acciones declarativas;
- costes.

Usa búsqueda de coste uniforme determinista.

El planner:

- respeta precondiciones;
- aplica efectos sobre copias;
- elige el menor coste total;
- desempata de forma determinista;
- evita mutar el mundo;
- puede devolver PLAN_FOUND, NO_PLAN o SEARCH_LIMIT.

### Executor

`executor.mjs` no asume que un plan viejo sigue siendo válido.

Antes de cada paso comprueba las precondiciones reales.

Si cambiaron:

`REPLAN_REQUIRED`

Ejemplo experimental:

```text
Objetivo: informar al superior

plan inicial:
ir_superior → informar_superior

el paso se cierra
        ↓
executor detecta fallo
        ↓
REPLAN_REQUIRED
        ↓
nuevo plan:
enviar_mensajero
```

## Acciones experimentales

Las acciones actuales son deliberadamente pequeñas:

- ayudar_jugador
- cumplir_deber
- enviar_mensajero
- esperar
- informar_superior
- investigar_anomalia
- ir_jugador
- ir_superior
- volver_puesto_desde_jugador
- volver_puesto_desde_superior

No representan todavía la movilidad real de La Grulla Blanca.

## Regresión local inicial

Ejecutado antes de solicitar auditoría externa:

```bash
node tests.mjs
node stress.mjs 10000 1337
```

Resultado:

- **25/25 PASS**
- stress GOAP **10.000/10.000 PASS**
- 0 NO_PLANNABLE_GOAL en ese seed
- distribución del seed 1337:
  - FULFILL_DUTY: 2882
  - RETURN_POST: 2421
  - INVESTIGATE_ANOMALY: 2183
  - HELP_PLAYER: 1181
  - REPORT_SUPERIOR: 865
  - WAIT_SAFE: 468

La distribución no es una meta de balance.

## Qué valida la suite

- coste mínimo real;
- evita retornar el primer goal generado si existe un plan posterior más barato;
- desempate determinista;
- NO_PLAN;
- tres personalidades → tres objetivos;
- generación de planes;
- ruta barata vs mensajero;
- executor completo;
- replanning por cambio del mundo;
- fallback si el objetivo prioritario no tiene plan;
- no mutación;
- RETURN_POST;
- WAIT_SAFE;
- validación de costes/hechos no finitos.

## Límites actuales

- no hay rutas reales;
- no hay puertas/gates canónicos;
- costes fijos;
- no hay duración temporal de acciones;
- no hay concurrencia entre NPC;
- no hay reservas de recursos;
- no hay memoria episódica;
- no hay conocimiento compartido;
- no hay efectos fallidos probabilísticos;
- el stress actual no introduce eventos dinámicos durante la ejecución;
- todavía no hay integración con save/load.

## Próximo paso

Auditoría externa de v0.2.

No mergear esta rama hasta revisar el informe.
