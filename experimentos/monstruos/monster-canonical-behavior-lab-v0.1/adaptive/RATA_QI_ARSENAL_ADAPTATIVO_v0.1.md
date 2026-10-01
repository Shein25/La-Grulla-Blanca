# Rata de Qi — Arsenal adaptativo T0–T4 v0.1

**Estado:** EXPERIMENTAL / NO CANÓNICO.  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`  
**Objetivo:** registrar la candidata T4 para que no quede fuera de la futura simulación integral T1–T4.

## Base recuperada

La Rata de Qi ya tiene en el laboratorio de Survival Evolution:

```text
T1 → Reflejo de Madriguera
EVADE_NEXT +25
1 acción
cooldown 2
```

Además, material histórico de diseño contenía el concepto `Mordisco frenético`, con tendencia a aparecer cuando la rata estaba herida. Ese concepto se recupera aquí como punto de partida, pero su ubicación en T4 y su contrato mecánico son **nueva propuesta LAB**.

## Regla de identidad

La Rata sigue siendo una criatura `INSTINTIVO / COLONIA`. T4 representa una población extremadamente presionada, no una rata convertida en artista marcial.

Por eso `Mordisco Frenético` NO recibe:

- penetración de DEF;
- ignorar absorción;
- drenaje de Qi;
- DOT;
- control;
- lectura de acciones futuras;
- cambio automático de cognitiveProfile.

## T4 — Mordisco Frenético

Telegraph:

> La rata encorva el lomo; el qi robado chisporrotea entre sus incisivos antes de lanzarse en una ráfaga de mordiscos.

Contrato LAB:

```text
categoría         OFENSIVA / MULTIIMPACTO / INSTINTIVO
unlock            effectiveAdaptiveTier >= T4
ventana           SELF_LOW_HP o SURVIVAL_EVADE_SUCCEEDED
impactos          2
potencia          0,75 × ataque básico por impacto
hit rolls         independientes
DEF               se aplica normalmente a cada impacto
absorción         se aplica normalmente a cada impacto
penetración       ninguna
Qi drain          0
DOT               ninguno
control           ninguno
cooldown          3 rondas
```

La potencia total bruta máxima de referencia es 1,50× un ataque básico si ambos impactos conectan, pero la DEF plana se aplica a cada impacto. El valor `0,75` y el cooldown `3` son **parámetros de laboratorio** y deben ser recalibrados después de cerrar T0 y al simular la progresión ofensiva T1–T4.

## Sinergia con T1

`Reflejo de Madriguera` enseña a salir de la línea del golpe. En T4, si esa evasión fue efectiva, `Mordisco Frenético` puede entrar en su ventana de elegibilidad en la siguiente decisión.

La lectura buscada es instintiva:

```text
escapa del golpe
→ queda junto al atacante
→ responde mordiendo de forma frenética
```

No requiere plan de varios turnos ni lectura del futuro.

## Progresión registrada

```text
T0 → ataque básico / balance natural
T1 → + Reflejo de Madriguera
T2 → reconocimiento persistente + defensa anticipatoria
      PENDIENTE: habilidad activa propia si se adopta “1 skill nueva por Tier”
T3 → counter específico de especie
      PENDIENTE: concretar habilidad activa de Rata
T4 → + Mordisco Frenético
```

Las habilidades son acumulativas mientras el Tier efectivo las sostenga. Si una población que alcanzó T4 decae a T3, `Mordisco Frenético` sale del `effectiveKit`, coherente con la regla vigente de que T4 es una adaptación extrema reversible.

## Integración futura obligatoria

Cuando se construya el laboratorio integral T1–T4:

1. incluir `rata_qi__mordisco_frenetico_t4` en el catálogo de abilities;
2. desbloquearla sólo en `effectiveAdaptiveTier >= 4`;
3. registrar usos, impactos, daño por impacto y activaciones tras `Reflejo de Madriguera`;
4. probarla contra todas las raíces/builds legales de la etapa correspondiente;
5. mantener Definitivas fuera del balance de monstruos;
6. no congelar `0,75`, cooldown `3` ni la ventana de elegibilidad sin simulación integral.
