# Variabilidad intraespecie de monstruos — v0.4

**Fecha de rebase:** 2026-10-06  
**Estado:** HUMAN_RATIFIED_REBASED_T0_T1_COMPAT_PENDING

## Objetivo

Mantener un único `species_id` por criatura y permitir variabilidad individual defensiva y ofensiva sin inflar el catálogo.

La autoridad actual es:

- T0 LI congelado: `T0_LI_EXHAUSTIVE_PASS_2026-10-06`;
- T1 LI congelado: `T1_LI_FINAL_FREEZE_2026-10-06`.

El T0 congelado es el **piso natural absoluto**. Ninguna instancia normal ni Mutante puede aparecer por debajo de él.

## Rebase 2026-10-06

La v0.3 fue validada antes del rebalance final de T0/T1 y contenía pisos antiguos. La v0.4 aplica esta regla sin inventar valores:

1. el nuevo T0 congelado reemplaza el piso histórico de cada eje;
2. un techo histórico se conserva sólo si todavía es >= al nuevo piso;
3. si el viejo techo quedó por debajo del nuevo T0, ese eje queda colapsado al T0 hasta que exista nueva evidencia;
4. en escaleras ofensivas se eliminan expresiones por debajo del ataque T0 congelado;
5. cadencia, QI_DRAIN y demás mecánicas identitarias se sincronizan con el T0 congelado.

Esto conserva únicamente evidencia experimental ya existente.

## Aclaración semántica ratificada — individuos normales

El perfil T0 congelado **no representa un monstruo normal con estadísticas fijas**.

Representa el piso natural y la referencia mínima de la especie. Cada spawn repetible se instancia con sus propias tiradas independientes `q_axis ∈ [0,1]` sobre todos los ejes variables disponibles.

Por tanto:

```text
especie
→ T0 floor
→ tiradas q_axis individuales
→ individuo normal concreto
→ evaluación de conjunción excepcional
→ posible Mutante / subtipo
→ tier adaptativo T0/T1/...
```

Un Mutante no recibe un paquete arbitrario de estadísticas. Es el resultado emergente de una **conjunción excepcional de las mismas características aleatorias que ya diferencian a todos los individuos normales**.

Los futuros sufijos especializados deben derivarse de esa configuración de `q_axis`; no deben sortearse independientemente ni reemplazar la variabilidad natural.

## Distribución

Cada eje realmente variable recibe una tirada independiente `q_axis ∈ [0,1]` una vez al crear la instancia.

```text
stat_instance = round(T0_floor + q_axis * (measured_ceiling - T0_floor))
```

La distribución sigue siendo `UNIFORM_0_1`.

Ejes físicos posibles:

```text
HP / DEF / EVA / PREC / TEN
```

Ejes ofensivos posibles:

```text
daño básico
daño directo de técnica
daño DOT
ticks de DOT cuando exista evidencia
```

Un eje cuyo techo haya colapsado al T0 deja temporalmente de contar como eje variable.

## Mutante

```text
individual_power_score
= media de q de todos los ejes que realmente varían
```

El umbral depende del número efectivo de ejes y mantiene una cola teórica cercana a 0,75%, con guardia <1%.

Al superar el umbral:

```text
suffix = "Mutante"
loot_multiplier = 1.5
xp_multiplier = 1.5
```

No se crea otro `species_id`.

## Criterio de dificultad ratificado

Un Mutante es contenido raro y excepcional.

**No existe un piso mínimo de probabilidad de victoria del jugador frente a Mutantes.**

Que la probabilidad de victoria caiga mucho respecto del individuo normal o T0/T1 es esperable y no constituye por sí mismo un fallo de balance.

El gate de compatibilidad debe fallar por problemas mecánicos, no por ser difícil:

- valores inválidos o por debajo de T0;
- identidad mecánica alterada;
- NaN/Inf;
- loops, timeouts o soft-locks;
- procs imposibles/inconsistentes;
- Mutantes sistemáticamente más fáciles por un bug;
- tier adaptativo concedido por la condición Mutante;
- modificación del registro canónico.

## Identidad fija

Nunca se sortea:

- `resource_model`;
- Control base;
- crítico/multiplicador base;
- nombre y tipo de técnica;
- mecánicas de técnica;
- cadencia;
- QI_DRAIN;
- probabilidad de control;
- cognición/social AI;
- reglas T1–T4.

Ser Mutante no concede T1/T2/T3/T4 ni modifica `maxTierReached`.

## Envolventes rebased

### Rata Qi

T0: HP45 / DEF2 / EVA0 / PRE84 / TEN0 / básico `2d4+3`.

- HP y DEF: colapsados al T0.
- básico: colapsado a `2d4+3`; todas las expresiones históricas eran inferiores al nuevo T0.
- EVA: techo medido 19.
- PRE: techo medido 104.
- TEN: techo medido 1.

### Serpiente Qi

T0: HP57 / DEF0 / EVA11 / PRE94 / TEN5.

- HP: colapsado a 57.
- DEF/EVA/PRE/TEN: conservan techos medidos 3/30/106/32.
- básico fijo `1d2+2`.
- veneno conserva escalera medida desde `1d2+2` hasta candidatos superiores y ticks 3→4.
- cadencia 2 fija.

### Avispa Jade

T0: HP42 / DEF2 / EVA22 / PRE102 / TEN7.

- HP/DEF: colapsados al T0.
- EVA/PRE/TEN: techos 55/103/8.
- básico, veneno y ticks conservan escaleras medidas que parten del T0 actual.
- cadencia 2 fija.

### Mono Píldoras

T0: HP59 / DEF2 / EVA28 / PRE91 / TEN12.

- HP/TEN: colapsados al T0.
- DEF/EVA/PRE: techos 3/44/111.
- básico y daño directo conservan escaleras medidas.
- `QI_DRAIN=6` fijo.
- cadencia 2 fija.

### Lobo Espiritual

T0: HP53 / DEF1 / EVA12 / PRE100 / TEN20.

- EVA/PRE/TEN: colapsados al T0 donde el techo histórico no lo superaba.
- HP/DEF: techos 57/5.
- básico y daño de Emboscada conservan escaleras medidas.
- cadencia de Emboscada = **4**, fija.

## Orden de aplicación

```text
species T0 READY
→ tiradas individuales
→ posible Mutante
→ perfil individual
→ tier adaptativo T0/T1/...
→ combate
```

El T1 congelado se aplica **después** de resolver la instancia individual.

## Guardia previa a runtime

Antes de activar esta v0.4:

1. selfcheck de incidencia y envelopes;
2. incidencia Mutante <1%;
3. ningún eje/ataque por debajo del T0 congelado;
4. normales y Mutantes probados con T1 congelado;
5. cero timeouts/NaN/soft-lock;
6. mecánicas identitarias intactas;
7. no se exige una probabilidad mínima de victoria contra Mutantes;
8. no escribir ni mutar el registro canónico.

Hasta que pase ese gate, la configuración permanece `T1_COMPAT_PENDING`.
