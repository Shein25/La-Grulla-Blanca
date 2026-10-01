# Rata T1 — Reflejo de Madriguera

Este laboratorio parte del T0 READY seleccionado en Heavy:

```text
HP 21 / PREC 80 / EVA 0 / DEF 0 / TEN 0 / CTRL 0 / crit 5% / x1.50 / basic 2d4
resource_model = NONE
```

No rediseña Monster Combat AI. Sólo calibra la magnitud del efecto T1 aprobado:

```text
Reflejo de Madriguera
kind = EVADE_NEXT
```

## Por qué grilla exhaustiva

Sólo hay dos magnitudes pendientes en esta capa:

- bono de Evasión al próximo ataque: +5 a +50, paso 5;
- cooldown: 1 a 5 rondas.

Son 50 combinaciones; una búsqueda exhaustiva es más transparente que Optuna.

## Sensibilidad de señales

Los umbrales del `LabSignalBridge` nunca fueron CANON. Se prueban tres brazos:

- EARLY: SELF_LOW_HP 40%, TOOK_HEAVY_HIT 15%;
- BASE: 30% / 20%;
- LATE: 20% / 25%.

Esto permite comprobar que la selección no dependa de un único umbral LAB.

## Comparación

T0 y T1 usan common random numbers. Las métricas centrales son:

- evades adicionales por pelea frente a T0;
- extensión de rondas frente a T0;
- presupuesto adaptativo normalizado.

Win rate, presión HP y retención de daño se reportan de forma descriptiva y no
se convierten en un target de win rate.

## Preset heavy

- 50 configuraciones;
- 3 brazos de señal;
- 1000 peleas/contexto durante grilla;
- 10 contextos;
- hasta 7 representantes Pareto;
- 20000 peleas/contexto high precision;
- 3 brazos de señal.

No se guardan peleas individuales.

Salida final:

`RESULTADOS_RATA_T1_REFLEJO_HEAVY.zip`

T2–T4 permanecen prohibidos.
