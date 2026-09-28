# Contrato global de Concordancias elementales — v0.1

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **EN CONSTRUCCIÓN / FUEGO COMO ORIGEN APROBADO**

## 0. Principio

Las Concordancias pertenecen a relaciones dirigidas `ORIGEN → DESTINO`.

La técnica receptora declara:

```text
role_primary
mechanical_hooks[]
concordance_hooks[]
```

El resolver sólo inspecciona `concordance_hooks[]`.

Reglas universales:

1. un Eco produce una sola resolución primaria de Concordancia;
2. el resolver recorre prioridades por contexto;
3. toma el primer hook compatible expuesto;
4. no aplica múltiples bonificaciones por un mismo Eco salvo transformación compuesta explícita;
5. si no encuentra hook compatible, no consume Eco;
6. no existe fallback universal de daño;
7. una relación sólo puede usar `DIRECT_DAMAGE` si su identidad global lo justifica;
8. las magnitudes numéricas se balancean después; primero se cierra identidad, canales y prioridad;
9. la matriz usa exclusivamente propiedades registradas en `REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md`.

---

# 1. FUEGO como origen — APROBADO

Fuego representa energía, excitación, transformación térmica y aceleración.

## 1.1 FUEGO → TIERRA · Cimiento Cocido

**Identidad:** Fuego consolida, endurece y densifica aquello que Tierra ya está formando.

### OFFENSIVE

Prioridad:

```text
1. DIRECT_DAMAGE
2. CONTROL_POWER
3. DEF_SHRED
4. PERCENT_PENETRATION
5. FLAT_PENETRATION
```

Condición semántica: el hook debe representar impacto, masa, presión o ruptura estructural.

### DEFENSIVE

```text
1. DEF_GRANTED
2. ABSORPTION
3. FORTIFICATION
4. TENACITY_GRANTED
5. DEFENSIVE_DURATION
```

### CONTROL

```text
1. CONTROL_POWER
2. ACTION_DENIAL
3. MOBILITY_REDUCTION
4. DEBUFF_DURATION
```

Sólo si el control representa peso, presión, encierro, impacto o inmovilización estructural.

### UTILITY

```text
1. FORTIFICATION
2. DEFENSIVE_DURATION
3. STACKABLE_STATE
```

### No prioritarios/incompatibles por identidad

```text
CRIT_CHANCE
CRIT_DAMAGE
QI_COST_PERCENT
PRECISION
EVASION_GRANTED
DIRECT_HEAL
DOT_POTENCY
```

---

## 1.2 FUEGO → METAL · Forja Ardiente

**Identidad:** Fuego transforma Metal mediante forja y templado.

### OFFENSIVE

```text
1. PERCENT_PENETRATION
2. FLAT_PENETRATION
3. DEF_SHRED
4. EXECUTION
5. DIRECT_DAMAGE
```

`DIRECT_DAMAGE` queda deliberadamente al final: primero se intenta expresar forja/filo/ruptura.

### DEFENSIVE

```text
1. FORTIFICATION
2. DEF_GRANTED
3. ABSORPTION
4. DEFENSIVE_DURATION
5. TENACITY_GRANTED
```

### CONTROL

```text
1. CONTROL_POWER
2. MOBILITY_REDUCTION
3. ACTION_DENIAL
4. DEBUFF_DURATION
```

Sólo si el control deriva de una estructura metálica coherente: cadena, jaula, grillete, anclaje o equivalente.

### UTILITY

```text
1. FORTIFICATION
2. DEBUFF_DURATION / DEFENSIVE_DURATION según el efecto
3. STACKABLE_STATE estructural
```

No usa `QI_COST_PERCENT` por defecto.

---

## 1.3 FUEGO → AGUA · Presurización

**Identidad:** Fuego aporta energía al flujo de Agua y lo transforma en presión, expansión o cambio de fase.

`Vapor Súbito` puede ser una manifestación concreta de esta relación, no su definición universal.

### OFFENSIVE

```text
1. PROPAGATION
2. DIRECT_DAMAGE
3. CONTROL_POWER
4. PRECISION_DEBUFF
5. DEBUFF_DURATION
```

### CONTROL

```text
1. CONTROL_POWER
2. INTERRUPT
3. ACTION_DENIAL
4. PRECISION_DEBUFF
5. MOBILITY_REDUCTION
```

Fuego no crea Control de la nada: presuriza una propiedad ya expuesta.

### DEFENSIVE

```text
1. REACTIVE_RESPONSE
2. ABSORPTION_RESTORE
3. ABSORPTION
4. DEFENSIVE_DURATION
```

`REACTIVE_RESPONSE` no implica automáticamente Reflect; puede materializarse como debuff, Control, restauración, expulsión, zona u otra reacción declarada.

### UTILITY

```text
1. PROPAGATION
2. ZONE_DURATION
3. REACTIVE_RESPONSE
4. DEBUFF_DURATION
```

No usa `QI_COST_PERCENT` por defecto.

---

## 1.4 FUEGO → VIENTO · Corriente Ascendente

**Identidad:** Fuego acelera el movimiento del aire y potencia propiedades dinámicas de Viento.

### OFFENSIVE

```text
1. CRIT_CHANCE
2. CRIT_DAMAGE
3. PRECISION
4. EXECUTION
5. PROPAGATION
6. DIRECT_DAMAGE
```

Se selecciona sólo el primer hook expuesto compatible.

### DEFENSIVE

```text
1. EVASION_GRANTED
2. REACTIVE_RESPONSE
3. DEFENSIVE_DURATION
```

### CONTROL

```text
1. INTERRUPT
2. CONTROL_POWER
3. MOBILITY_REDUCTION
4. ACTION_DENIAL
```

### UTILITY

```text
1. EXECUTION
2. PROPAGATION
3. ZONE_DURATION
```

---

# 2. Resumen Fuego aprobado

| Relación | Identidad |
|---|---|
| Fuego → Tierra | consolidar / endurecer estructura |
| Fuego → Metal | forjar / templar |
| Fuego → Agua | presurizar / expandir / transformar |
| Fuego → Viento | acelerar / elevar / dinamizar |

