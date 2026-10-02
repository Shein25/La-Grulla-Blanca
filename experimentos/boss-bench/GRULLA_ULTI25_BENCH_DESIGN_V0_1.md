# BENCH GRULLA 25/25 — Diseño V0.1

Fecha: 2026-10-02

Estado: **DISEÑO LAB / NO CANON / NO RUNTIME / NO MERGE / NO PUSH**

## Pregunta central

> Cuando el jugador preparó correctamente su carta y encuentra la oportunidad, ¿la Definitiva cambia realmente el destino de una pelea difícil sin convertir la Fase III en una fase inexistente?

La Grulla se usa como **objetivo de estrés prolongado**, no como objetivo para el cual se rediseñan las Ultis.

## Autoridades

1. Contrato cerrado de combate/estadísticas/eventos de Ultis.
2. Catálogo y runner validados de las 25 Definitivas.
3. Diseño real de la Grulla F1 → F2 → F3.
4. `GRULLA_F3_PACTO_ULTIMO_VUELO_2026-10-02.md`.

No se debe simplificar la Grulla a un saco de HP.

## Diseño causal: paired seeds

Cada semilla genera un encuentro base.

Para la misma semilla se ejecutan ramas hermanas:

- `BASELINE_NO_ULTI`;
- cada Ulti bajo una política de activación definida.

La rama con Ulti y la rama baseline deben compartir:

- estado inicial;
- RNG previo al checkpoint;
- política normal del jugador;
- IA real de la Grulla;
- inventario/equipo;
- técnicas normales;
- reglas del motor.

Esto permite medir **Δ destino** con menos ruido.

## Unidad experimental

Una unidad = una pelea completa F1 → F2 → F3 o muerte del jugador.

Se registran checkpoints exactos de entrada a F2 y F3.

## Brazos de activación

Para cada una de las 25 Ultis:

### W1 · F1_EARLY
Primera oportunidad legal después de que la Grulla haya resuelto su primera intención F1.

Objetivo: medir valor de tempo y supervivencia temprana.

### W2 · F2_ENTRY
Primera oportunidad legal del jugador después de entrar F2.

Objetivo: medir aceleración de fase media y preservación de recursos.

### W3 · F3_ENTRY
Primera oportunidad legal al entrar F3, antes de la primera intención real F3 de la Grulla.

Objetivo principal:
- medir potencial de borrado de F3;
- activar telemetría del Pacto;
- cuantificar cuánto overkill habría producido la Ulti sin el death-gate.

### W4 · PREPARED_OPPORTUNITY
La Ulti se usa sólo cuando se cumple su propia condición de oportunidad/preparación.

No existe un trigger genérico.

Ejemplos de clase, no de números:
- recursos/stacks suficientes;
- ventana de reacción válida;
- Qi por debajo del gate correcto;
- objetivo con heridas/estados pertinentes;
- condición defensiva/hostil propia de la técnica.

La implementación de cada trigger debe venir del catálogo autoritativo de esa Ulti, no de una heurística nueva.

## Perfiles del jugador

Primera matriz propuesta:

- `FULL`: preparado y saludable;
- `BALANCED`: estado medio plausible;
- `DISADVANTAGE`: recursos/vida desfavorables;
- `NEAR_DEATH`: pelea casi perdida.

Estos perfiles deben fijarse con stats/técnicas reales del personaje, no inventados por el benchmark. Si todavía no existe una autoridad cerrada del personaje, el runner debe marcar `BLOCKED_PLAYER_FIXTURE` en vez de fabricar valores.

## Baseline y Δ destino

Para cada seed y perfil:

`delta_win = win_with_ulti - win_baseline`

Más útil que daño bruto:

- `loss_to_win_flip`: baseline pierde, Ulti gana;
- `win_to_loss_flip`: baseline gana, Ulti pierde;
- fase alcanzada baseline vs Ulti;
- turnos ahorrados;
- HP/Qi conservados;
- acciones hostiles evitadas;
- cambio en probabilidad de alcanzar F3;
- cambio en probabilidad de superar F3.

## Métricas por fase

### F1
- turnos jugador / Grulla;
- daño a Vida;
- daño absorbido;
- HP/Qi de salida;
- estados persistentes;
- Ulti usada/no usada.

### F2
- todo lo anterior;
- memoria/adaptación real de la Grulla;
- número de intenciones observadas;
- tiempo hasta transición F3.

### F3
Además:
- `f3_skip_attempted`;
- `f3_lethal_preventions`;
- `f3_prevented_lethal_damage`;
- `f3_max_single_overkill_prevented`;
- fuente del letal prevenido;
- si fue DIRECT/DOT/Hemorragia/derivado;
- primera intención real F3 resuelta;
- turnos de Grulla en F3;
- acciones del jugador después de liberar el Pacto hasta matar;
- HP de Grulla inmediatamente después de liberar el Pacto.

## Métricas de cada Ulti

- activación legal;
- activación fallida y motivo;
- climax alcanzado;
- stacks/recursos construidos;
- daño directo;
- daño derivado;
- daño absorbido;
- Control intentado/logrado/resistido;
- acciones negadas;
- Qi gastado/restaurado/ahorrado;
- curación;
- Absorción creada/restaurada;
- supervivencia del jugador;
- tasa de muerte antes de poder usar la Ulti.

## Diagnóstico anti-"guardar todo para F3"

No se nerfea automáticamente una Ulti si tiene alto `f3_skip_attempted`.

Se analiza:

1. cuánto aumenta la victoria en W3;
2. cuánto aporta en W1/W2/W4;
3. cuántas veces deja a la Grulla en 1 HP;
4. cuánto tarda en morir después de la primera acción real F3;
5. si W3 domina de forma sistemática a la ventana preparada.

Señal de riesgo de diseño:
- si guardar la Ulti para W3 domina consistentemente su uso preparado y comprime F3 a "una acción obligatoria + remate", hay un problema de encuentro/meta que estudiar.

No se decide de antemano si la solución es tocar la Grulla o la Ulti.

## Comparación intrafamilia

Cada Ulti se compara con sus cuatro hermanas en:

- Δ victoria;
- fase donde más cambia el resultado;
- supervivencia;
- tempo;
- control;
- eficiencia de Qi;
- dependencia de preparación;
- potencial de skip F3;
- tiempo posterior al Pacto.

Objetivo: detectar solapamientos o una hermana que haga lo mismo mejor en todos los ejes.

## Escala inicial propuesta

### Smoke
- 25 Ultis × 4 ventanas × 4 perfiles × 20 seeds
- + baseline pareado
- objetivo: contratos, transitions, death-gate, logging.

### Pilot
- 25 × 4 × 4 × 200 seeds = 80.000 encuentros con Ulti
- baseline se calcula una vez por seed/perfil y se reutiliza.
- objetivo: estimar duración, varianza y coste Kaggle.

### Mass
No fijar todavía el N final.

Después del Pilot:
- calcular intervalos de confianza de win-flip y métricas F3;
- elegir N suficiente;
- evitar millones innecesarios de peleas largas.

## Invariantes de fallo duro

El bench debe abortar si ocurre cualquiera:

- `F3_KILL_BEFORE_FIRST_REAL_ACTION > 0`;
- el Pacto se libera por una acción impedida;
- un segundo hit de la misma acción salta el death-gate;
- una Ulti usa una implementación distinta de la autoridad cerrada;
- la IA real de la Grulla es sustituida por flags abstractos;
- una técnica auxiliar real es reemplazada por un booleano;
- RNG no pareado entre baseline y rama Ulti;
- se inventan stats del jugador o de la Grulla.

## Entregables del Pilot

- `run_manifest.json`;
- `self_check.json`;
- `baseline_summary.csv`;
- `ulti_summary.csv`;
- `paired_delta_summary.csv`;
- `f3_skip_pressure.csv`;
- `family_comparison.csv`;
- `phase_metrics.csv`;
- `issues.json`;
- ZIP único para auditoría.

## Estado actual

Ya existen en esta rama:

- contrato `PACTO_ULTIMO_VUELO`;
- helper contractual LAB;
- prototipo visual/funcional `BOSS_UI_B13_GRULLA_PACTO_ULTIMO_VUELO.html`, derivado del B12 recuperado;
- spec machine-readable del bench;
- scaffold `grulla_ulti25_bench_runner_v01.py` con seeds pareadas y streams RNG por dominio.

B12/B13 son prototipos **SIN MOTOR**. Por eso el diseño del bench sigue abierto para ejecución real.

Bloqueantes antes del runner masivo:

1. source ejecutable real de la IA/combate de la Grulla F1–F3;
2. fixture autoritativo del personaje/equipo/técnicas con el que se enfrentará al jefe;
3. definir exactamente cómo se construye el trigger `PREPARED_OPPORTUNITY` para las 25 Ultis desde su catálogo existente.

No se deben inventar esos tres componentes.
