# Resultado benchmark — Monster Behavior Benchmark v0.1

## Corrida reproducida

### Smoke — 18 combatientes

```text
runs por mob            1.000
mobs                       18
decisiones primarias    18.000
seed                     1337
digest       29c77e4b3ae654d6
```

En los 18:

```text
cadenceViolations = 0
invalidSelections = 0
```

Cambios observables destacados:

- serpiente_qi — memoria: 12,60%
- sapo_caldera — memoria: 14,60%
- sombra_ahogada — memoria: 13,60%
- guardian_coral — memoria: 10,80%
- lobo_espiritual — social: 11,70%
- mono_pildoras — memoria: 14,20%; social: 15,00%; combinado vs neutral: 20,70%

Los perfiles INSTINTIVO mantienen 0 cambios por memoria, como exige el contrato.

## Barridos densos

### guardian_coral

```text
10.000 decisiones
seed 6
digest 50c2faace22ef189

memoryChangedDecision = 1.129
memoryChanged         = 11,29%
cadenceViolations     = 0
invalidSelections     = 0
```

### lobo_espiritual

```text
10.000 decisiones
seed 7
digest 39396ac4a5bb9a23

socialChangedDecision = 1.150
socialChanged         = 11,50%
cadenceViolations     = 0
invalidSelections     = 0
```

### mono_pildoras

```text
10.000 decisiones
seed 8
digest 89e5f87c0c300189

memoryChangedDecision      = 1.243
socialChangedDecision      = 1.632
combinedChangedVsNeutral   = 2.047

memoryChanged              = 12,43%
socialChanged              = 16,32%
combinedChangedVsNeutral   = 20,47%

cadenceViolations          = 0
invalidSelections          = 0
```

## Interpretación

El benchmark confirma que la adaptividad no es decorativa:

- memoria cambia decisiones en perfiles que la usan;
- social cambia decisiones en perfiles sociales compatibles;
- perfiles INSTINTIVO ignoran memoria;
- `CADENCE_COMPAT` sigue mandando sobre la ejecución productiva.

Las tasas no asignan calidad ni balance final. Sirven para localizar superficies de decisión que luego deben revisarse contra diseño narrativo y combate real.

## Estado

`MONSTER_BEHAVIOR_BENCHMARK_V01: SIGNAL_CONFIRMED`
