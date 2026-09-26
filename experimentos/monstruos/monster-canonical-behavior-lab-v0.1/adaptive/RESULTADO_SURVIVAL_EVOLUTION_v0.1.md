# Resultado — Monster Adaptive Survival v0.1

## Estado

`EXPERIMENTAL_NON_CANONICAL_SURVIVAL_V01`

Rama:

`experiment/monster-adaptive-survival-lab-v0.1`

Base:

`e97add771e0f9ee8d00de21b6c8dc3ca2b7fa237`

No toca `main`, PR #17 ni PR #18.

## Hipótesis

La primera evolución debe enseñar **supervivencia**, no añadir HP, daño ni otra técnica ofensiva.

```text
más encuentros
→ experiencia adaptativa
→ Evolución I
→ +1 paso cognitivo máximo
→ +1 acción defensiva propia de la especie
```

## Balance elegido

Umbral experimental:

- comunes: 6 XP;
- únicos: 4 XP;
- encuentro real: +1 XP;
- encuentro con HP bajo o golpe fuerte observado: +1 XP adicional;
- máximo 2 XP por encuentro.

Esto produce:

- común: 3 encuentros duros o 6 ordinarios;
- único: 2 encuentros duros o 4 ordinarios.

## Política de supervivencia

La defensa se calibra contra la preferencia ofensiva ya existente del monstruo.

Barrido dirigido sobre 18 combatientes:

```text
sano                              0.0 % defensa
HP bajo                          49.5 % defensa
golpe fuerte, pero HP sano        0.0 % defensa
HP bajo + golpe fuerte          100.0 % defensa
defensa en cooldown               0.0 % defensa
violaciones CADENCE_COMPAT           0
```

El 100% del caso crítico no implica spam: la acción defensiva consume turno y propone 2 rondas de cooldown.

## Inteligencia y riesgo

Cuando ambos lados están bajos de vida, sin golpe fuerte reciente, el perfil evolucionado decide progresivamente asumir más riesgo:

```text
REACTIVO_1  — rata_qi          22.125 % defensa
CAZADOR_2   — serpiente_qi     12.725 % defensa
TACTICO_3   — lobo_espiritual   5.475 % defensa
MASTER_4    — guardian_coral    0.000 % defensa
```

Interpretación experimental:

- perfiles simples aún dudan entre sobrevivir y rematar;
- perfiles más inteligentes reconocen mejor la ventana de ejecución;
- si reciben además un golpe fuerte estando bajos, todos vuelven a supervivencia prioritaria.

Así, “más inteligencia” no equivale a “más defensa”.

## Fuerza de las acciones defensivas

Stage I queda limitada deliberadamente:

### EVADE_NEXT

- +20 a +25 esquiva;
- una acción;
- cooldown propuesto: 2 rondas.

En el cálculo actual de ver74, cada +5 de esquiva añade aproximadamente un escalón de d20 al requisito de impacto, por lo que +20/+25 representa una defensa perceptible pero temporal.

### MITIGATE_NEXT

- reduce 30–40% del próximo golpe;
- un golpe;
- cooldown propuesto: 2 rondas.

No se permiten en v0.1:

- curación gratuita;
- aumento permanente de defensa;
- contraataque automático;
- daño añadido a la defensa;
- invulnerabilidad;
- defensa y ataque en la misma acción.

## Ataque-only

Los dos combatientes que actualmente no poseen técnica canónica evolucionan así:

```text
rata_qi
BASIC_ATTACK
→ Reflejo de Madriguera
→ EVADE_NEXT (+25 esquiva)

eco_caido
BASIC_ATTACK
→ Guardia del Último Ensayo
→ MITIGATE_NEXT (-35% próximo golpe)
```

No se inventó una técnica ofensiva para hacerlos “más fuertes”.

## Cobertura

Suite dirigida:

```text
15/15 PASS
```

Comprueba:

- 18/18 políticas presentes;
- muñeco de práctica fuera;
- XP sólo por encuentro real;
- umbrales 6/4;
- stage 0 conserva kit;
- stage 1 suma defensa;
- cognición avanza máximo un escalón;
- 0 defensa estando sano;
- decisión ~50/50 con HP bajo;
- supervivencia fuerte en estado crítico;
- cooldown impide spam;
- CADENCE_COMPAT sigue autoritativo;
- Rata/Eco no reciben ofensiva inventada;
- gradiente de riesgo por inteligencia;
- efectos defensivos dentro de caps conservadores.

## Gaps reales antes de producción

### 1. Persistencia adaptativa

Todavía no existe un store productivo de:

`survivalXp / evolutionStage`

Debe decidirse la identidad:

- comunes: probablemente aprendizaje por especie;
- únicos: aprendizaje por individuo.

No se ha añadido esto al save.

### 2. Executor de intents defensivos

Monster Combat AI puede **decidir**:

- `EVADE_NEXT`;
- `MITIGATE_NEXT`.

ver74 todavía no tiene un bridge/executor de monstruos que aplique esos efectos.

Esto es un gap de capacidad, no debe resolverse fingiendo un ataque canónico.

## Resultado

La hipótesis “primero aprender a sobrevivir” queda balanceada como base de Evolución I.

El siguiente trabajo no requiere otra arquitectura de IA: requiere persistencia adaptativa + executor defensivo, reutilizando el Monster Combat AI auditado.
