# Mapeo canónico de hooks — 12 técnicas de Arco 1

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CANÓNICO PARA RECEPCIÓN DE CONCORDANCIAS / SIN IMPLEMENTACIÓN RUNTIME**

## 0. Autoridad y reglas

Este documento cierra el hueco de `role_primary`, `mechanical_hooks[]` y `concordance_hooks[]` de las 12 técnicas diseñadas hasta Tierra.

Precedencia:

1. `CONTRATO_CONCORDANCIAS_GLOBALES_V0_1.md`
2. `REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md`
3. `CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md`
4. este documento
5. texto narrativo/legacy de `TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md`

Reglas:

- `mechanical_hooks[]` describe capacidades reales de la técnica.
- `concordance_hooks[]` es un subconjunto explícito de capacidades que pueden ser receptoras.
- un hook global del actor no se considera aportación de la técnica;
- un hook condicional sólo existe si la rama que lo crea está activa;
- una aportación inexistente o igual a cero no crea compatibilidad;
- `DIRECT_DAMAGE` no se expone automáticamente;
- un hook STRUCTURAL sólo es compatible si la relación tiene `transformation_rule` registrada;
- un único Eco produce una única resolución primaria por ActionContext;
- `EXECUTION` no se usa como concordance_hook en esta versión.

---

# 1. FUEGO

## 1.1 Palma Ardiente

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, FIRE, UNITARGET]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- CONTAINED_TRIGGER  # capacidad receptora estructural

mechanical_hooks POR RAMA:
- AFFLICTION_APPLICATION
- DOT_POTENCY
- DOT_DURATION
- DOT_STACKS
- CRIT_CHANCE
- CRIT_DAMAGE
- PRECISION
- QI_COST_PERCENT

concordance_hooks BASE:
- DIRECT_DAMAGE
- CONTAINED_TRIGGER

concordance_hooks POR RAMA:
DOT:
- AFFLICTION_APPLICATION
- DOT_POTENCY
- DOT_DURATION
CRIT:
- CRIT_CHANCE
- CRIT_DAMAGE
```

Notas:
- Precisión y coste siguen siendo mecánicos pero ninguna relación entrante de Fuego los necesita actualmente.
- `PERSISTENCE` no se expone: las ramas actuales alargan Quemadura mediante `DOT_DURATION`, no cambian política de persistencia.

## 1.2 Respiración del Cuerpo-Horno

```text
role_primary = DEFENSIVE
tags = [TECHNIQUE, ELEMENTAL, FIRE, DEFENSIVE]

mechanical_hooks BASE:
- ABSORPTION
- DEFENSIVE_DURATION

mechanical_hooks POR RAMA:
- INTERNAL_RESOURCE(CALOR)
- QI_COST_PERCENT

concordance_hooks BASE:
- ABSORPTION
- DEFENSIVE_DURATION

concordance_hooks POR RAMA:
CONVERSION_CALOR:
- INTERNAL_RESOURCE
  scale_target = gain
```

Calor no se vuelve a escalar al liberarse; continúa rigiendo el contrato §38.20 del Motor.

## 1.3 Círculo de las Cien Ascuas

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, FIRE, AOE]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- CONTAINED_TRIGGER

mechanical_hooks POR RAMA:
- AFFLICTION_APPLICATION
- DOT_POTENCY
- DOT_DURATION
- DOT_STACKS
- CRIT_CHANCE
- CRIT_DAMAGE
- PRECISION
- QI_COST_PERCENT

concordance_hooks BASE:
- DIRECT_DAMAGE
- CONTAINED_TRIGGER

concordance_hooks POR RAMA:
DOT:
- AFFLICTION_APPLICATION
- DOT_POTENCY
- DOT_DURATION
CRIT:
- CRIT_CHANCE
- CRIT_DAMAGE
```

Una manifestación CONTAINED_TRIGGER se resuelve una vez por ActionContext y puede aplicarse per_target sólo sobre impactos conectados.

---

# 2. METAL

## 2.1 Destello de Plata

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, METAL, UNITARGET]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PERCENT_PENETRATION

mechanical_hooks POR RAMA:
- FLAT_PENETRATION
- PRECISION
- CRIT_CHANCE
- CRIT_DAMAGE
- QI_COST_PERCENT

concordance_hooks BASE:
- PERCENT_PENETRATION

concordance_hooks POR RAMA:
PENETRATION:
- FLAT_PENETRATION
PRECISION:
- PRECISION
CRITICAL:
- CRIT_CHANCE
- CRIT_DAMAGE
```

`DIRECT_DAMAGE` es mecánico pero **no** se expone a Concordancias en Destello. Esto evita convertir relaciones Metal receptoras en aumento genérico de daño cuando ya existe un canal identitario mejor.

## 2.2 Armadura de Plata

```text
role_primary = DEFENSIVE
tags = [TECHNIQUE, ELEMENTAL, METAL, DEFENSIVE]

mechanical_hooks BASE:
- DEF_GRANTED
- DEFENSIVE_DURATION
- STACKABLE_STATE(PLACAS)
- FORTIFICATION

mechanical_hooks POR RAMA:
- TENACITY_GRANTED
- REACTIVE_RESPONSE

concordance_hooks BASE:
- DEF_GRANTED
- DEFENSIVE_DURATION
- FORTIFICATION

concordance_hooks POR RAMA:
ADAPTATION:
- TENACITY_GRANTED
```

Reglas:
- `FORTIFICATION` es capacidad receptora estructural.
- Tierra→Metal + FORTIFICATION selecciona Placa Fundacional.
- Otras relaciones que no tengan una `transformation_rule` para FORTIFICATION lo omiten y continúan con el siguiente hook compatible.
- `STACKABLE_STATE(PLACAS)` no se expone a Concordancias en esta versión; evita alterar cantidad de Placas con una suma fija.

## 2.3 Lluvia de Filos

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, METAL, AOE]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PERCENT_PENETRATION

mechanical_hooks POR RAMA:
- DEF_SHRED
- PRECISION
- CRIT_CHANCE
- CRIT_DAMAGE
- QI_COST_PERCENT

concordance_hooks BASE:
- PERCENT_PENETRATION

concordance_hooks POR RAMA:
RUPTURE:
- DEF_SHRED
PRECISION:
- PRECISION
CRITICAL:
- CRIT_CHANCE
- CRIT_DAMAGE
```

`DIRECT_DAMAGE` no se expone a Concordancias en Lluvia.

---

# 3. AGUA

## 3.1 Latigazo de Marea

```text
role_primary = CONTROL
tags = [TECHNIQUE, DIRECT, ELEMENTAL, WATER, CONTROL, UNITARGET]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- CONTROL_POWER
- ACTION_DENIAL
- INTERRUPT
- CONTROL_LOCKOUT

mechanical_hooks POR RAMA:
- PRECISION_DEBUFF
- PRECISION
- CRIT_CHANCE
- QI_COST_PERCENT

concordance_hooks BASE:
- CONTROL_POWER
- ACTION_DENIAL
- INTERRUPT
- CONTROL_LOCKOUT

concordance_hooks POR RAMA:
CONTROL_DEBUFF:
- PRECISION_DEBUFF
EFFICIENCY:
- QI_COST_PERCENT
PRECISION:
- PRECISION
```

`DIRECT_DAMAGE` no se expone porque el rol primario de Latigazo es Control.

## 3.2 Espejo de Luna

```text
role_primary = DEFENSIVE
tags = [TECHNIQUE, ELEMENTAL, WATER, DEFENSIVE]

mechanical_hooks BASE:
- ABSORPTION
- ABSORPTION_RESTORE
- DEFENSIVE_DURATION

mechanical_hooks POR RAMA:
- QI_COST_PERCENT
- QI_RESTORE

concordance_hooks BASE:
- ABSORPTION
- ABSORPTION_RESTORE
- DEFENSIVE_DURATION

concordance_hooks POR RAMA:
EFFICIENCY:
- QI_COST_PERCENT
```

Tierra→Agua + `ABSORPTION_RESTORE` selecciona Embalse como manifestación estructural; no aplica simultáneamente un escalado genérico de Reflujo.

## 3.3 Marea de las Ocho Orillas

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, WATER, AOE, DEBUFF]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PRECISION_DEBUFF
- DEBUFF_DURATION

mechanical_hooks POR RAMA:
- PRECISION
- CRIT_CHANCE
- QI_COST_PERCENT
- MARK

concordance_hooks BASE:
- PRECISION_DEBUFF
- DEBUFF_DURATION

concordance_hooks POR RAMA:
PRECISION:
- PRECISION
EFFICIENCY:
- QI_COST_PERCENT
```

`DIRECT_DAMAGE` no se expone a Concordancias en Marea; las relaciones entrantes deben interactuar con su identidad de debilitación/eficiencia cuando exista canal.

---

# 4. TIERRA

## 4.1 Golpe de Montaña

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, EARTH, UNITARGET, DEBUFF]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- EVASION_DEBUFF
- DEBUFF_DURATION
- STACKABLE_STATE(PESO)

mechanical_hooks POR RAMA:
- TENACITY_GRANTED
- DEF_GRANTED
- PRECISION

concordance_hooks BASE:
- DIRECT_DAMAGE
- EVASION_DEBUFF
- DEBUFF_DURATION

concordance_hooks POR RAMA:
PRECISION:
- PRECISION
```

`STACKABLE_STATE(PESO)` no se expone a Concordancias en esta versión; Peso conserva su propia progresión de técnica.

## 4.2 Piel de Cobre

```text
role_primary = DEFENSIVE
tags = [TECHNIQUE, ELEMENTAL, EARTH, DEFENSIVE]

mechanical_hooks BASE:
- DEF_GRANTED
- TENACITY_GRANTED
- DEFENSIVE_DURATION
- STACKABLE_STATE(ARRAIGO)

mechanical_hooks POR RAMA:
- DIRECT_HEAL
- PRECISION

concordance_hooks BASE:
- DEF_GRANTED
- TENACITY_GRANTED
- DEFENSIVE_DURATION

concordance_hooks POR RAMA:
# ninguno adicional necesario en la matriz actual
```

Decisión:
- `STACKABLE_STATE(ARRAIGO)` **no** se expone a Concordancias.
- el antiguo "+1 Arraigo" de Metal→Tierra queda definitivamente legacy;
- esto evita una mejora discreta fija que perdería relevancia con escalado futuro.

## 4.3 Temblor de Montaña

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, EARTH, AOE, DEBUFF]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- EVASION_DEBUFF
- DEBUFF_DURATION

mechanical_hooks POR RAMA:
- MARK(RESONANCIA)
- PRECISION
- CRIT_CHANCE
- CRIT_DAMAGE

concordance_hooks BASE:
- DIRECT_DAMAGE
- EVASION_DEBUFF
- DEBUFF_DURATION

concordance_hooks POR RAMA:
PRECISION:
- PRECISION
```

Los mapeos legacy de Penetración, DEF_SHRED y Evasión adicional quedan sin autoridad.

---

# 5. VIENTO

## 5.1 Lanza que Parte Nubes

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, WIND, UNITARGET]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PRECISION
- CRIT_CHANCE

mechanical_hooks POR RAMA:
- CRIT_DAMAGE
- QI_COST_PERCENT

concordance_hooks BASE:
- PRECISION
- CRIT_CHANCE

concordance_hooks POR RAMA:
CRITICAL:
- CRIT_DAMAGE
```

Decisiones:
- `DIRECT_DAMAGE` es mecánico pero no se expone a Concordancias;
- Fuego→Viento resuelve sobre `CRIT_CHANCE`;
- Metal→Viento resuelve sobre `PRECISION`;
- Agua→Viento y Tierra→Viento no tienen receptor compatible en Lanza;
- la ausencia de receptor no crea fallback ni consume el Eco por Concordancia.

---

# 6. Mini-reauditoría 13 × 4

Esta tabla usa exclusivamente los `concordance_hooks` anteriores y la matriz global actual.

`BASE NONE` significa que el Eco no se consume por Concordancia; si la técnica pura completa una ejecución válida puede generar su Eco propio y sustituir el anterior.

| Técnica | Eco entrante | Primer hook compatible | Resultado | Estado |
|---|---|---|---|---|
| Palma | Metal→Fuego | BASE NONE; rama DOT: AFFLICTION_APPLICATION; rama crítica: CRIT_CHANCE | Ignición sólo con canal real | PASS |
| Palma | Agua→Fuego | DIRECT_DAMAGE | escala daño propio | PASS |
| Palma | Tierra→Fuego | CONTAINED_TRIGGER; con DOT: DOT_DURATION | Núcleo o duración DOT, nunca ambos | PASS |
| Palma | Viento→Fuego | DIRECT_DAMAGE | Avivamiento directo | PASS |
| Cuerpo-Horno | Metal→Fuego | ABSORPTION; con Calor: INTERNAL_RESOURCE | barrera o ganancia de Calor | PASS |
| Cuerpo-Horno | Agua→Fuego | BASE NONE; con Calor: INTERNAL_RESOURCE | sin fallback en base | PASS |
| Cuerpo-Horno | Tierra→Fuego | ABSORPTION; con Calor: INTERNAL_RESOURCE | contención | PASS |
| Cuerpo-Horno | Viento→Fuego | ABSORPTION | magnitud inmediata | PASS |
| Círculo | Metal→Fuego | BASE NONE; con DOT: AFFLICTION_APPLICATION | ignición por rama | PASS |
| Círculo | Agua→Fuego | DIRECT_DAMAGE | escala magnitud de la AOE | PASS |
| Círculo | Tierra→Fuego | CONTAINED_TRIGGER; con DOT: DOT_DURATION | Núcleo per_target o DOT | PASS |
| Círculo | Viento→Fuego | DIRECT_DAMAGE | Avivamiento AOE | PASS |
| Destello | Fuego→Metal | PERCENT_PENETRATION | Forja sobre Pen propia | PASS |
| Destello | Agua→Metal | BASE NONE; con rama crítica/precisión: CRIT_DAMAGE/CRIT_CHANCE/PRECISION | Temple requiere propiedad real | PASS |
| Destello | Tierra→Metal | PERCENT_PENETRATION; CRIT_CHANCE si rama | asentamiento | PASS |
| Destello | Viento→Metal | PERCENT_PENETRATION; PRECISION si rama | propulsión/precisión | PASS |
| Armadura | Fuego→Metal | DEF_GRANTED | escala DEF de Placa | PASS |
| Armadura | Agua→Metal | DEF_GRANTED | escala DEF de Placa | PASS con convergencia |
| Armadura | Tierra→Metal | FORTIFICATION | Placa Fundacional | PASS |
| Armadura | Viento→Metal | DEFENSIVE_DURATION | duración escalada | PASS |
| Lluvia | Fuego→Metal | PERCENT_PENETRATION | Forja sobre Pen | PASS |
| Lluvia | Agua→Metal | BASE NONE; rama crítica/precisión habilita receptor | Temple condicional | PASS |
| Lluvia | Tierra→Metal | PERCENT_PENETRATION; CRIT_CHANCE si rama | asentamiento | PASS |
| Lluvia | Viento→Metal | PERCENT_PENETRATION; PRECISION si rama | propulsión | PASS |
| Latigazo | Fuego→Agua | CONTROL_POWER | Presurización de Arrastre | PASS |
| Latigazo | Metal→Agua | CONTROL_POWER | Cauce de Arrastre | PASS con convergencia |
| Latigazo | Tierra→Agua | CONTROL_POWER | flujo contenido | PASS |
| Latigazo | Viento→Agua | CONTROL_POWER; QI_COST_PERCENT si rama | control o eficiencia PRE_COST | PASS |
| Espejo | Fuego→Agua | ABSORPTION_RESTORE | Reflujo escalado | PASS |
| Espejo | Metal→Agua | ABSORPTION_RESTORE; QI_COST_PERCENT si rama | Reflujo/coste | PASS |
| Espejo | Tierra→Agua | ABSORPTION_RESTORE | Embalse | PASS |
| Espejo | Viento→Agua | ABSORPTION_RESTORE; QI_COST_PERCENT si rama | Reflujo/coste | PASS con convergencia |
| Marea | Fuego→Agua | PRECISION_DEBUFF | Presurización sobre Desbalance | PASS |
| Marea | Metal→Agua | BASE NONE; PRECISION si rama | canalización condicional | PASS |
| Marea | Tierra→Agua | DEBUFF_DURATION | prolonga Desbalance porcentualmente | PASS |
| Marea | Viento→Agua | BASE NONE; QI_COST_PERCENT/PRECISION por rama | eficiencia condicional | PASS |
| Golpe | Fuego→Tierra | DIRECT_DAMAGE | Cimiento | PASS |
| Golpe | Metal→Tierra | DIRECT_DAMAGE | Anclaje cae a daño | PASS con convergencia |
| Golpe | Agua→Tierra | EVASION_DEBUFF | Erosión de Peso | PASS |
| Golpe | Viento→Tierra | DIRECT_DAMAGE | impulso | PASS con convergencia |
| Piel | Fuego→Tierra | DEF_GRANTED | DEF propia escalada | PASS |
| Piel | Metal→Tierra | TENACITY_GRANTED | estabilidad relativa, sin +1 Arraigo | PASS |
| Piel | Agua→Tierra | DEFENSIVE_DURATION | duración porcentual + snapshot | PASS |
| Piel | Viento→Tierra | TENACITY_GRANTED | Tenacidad propia escalada | PASS con convergencia |
| Temblor | Fuego→Tierra | DIRECT_DAMAGE | Cimiento AOE | PASS |
| Temblor | Metal→Tierra | DIRECT_DAMAGE | Anclaje cae a daño | PASS con convergencia |
| Temblor | Agua→Tierra | EVASION_DEBUFF | Suelo Inestable escalado | PASS |
| Temblor | Viento→Tierra | DIRECT_DAMAGE | impulso AOE | PASS con convergencia |
| Lanza | Fuego→Viento | CRIT_CHANCE | Corriente Ascendente escala la probabilidad crítica propia | PASS |
| Lanza | Metal→Viento | PRECISION | Filo en la Corriente escala la Precisión propia | PASS |
| Lanza | Agua→Viento | NONE | Sin resolución; sin fallback | PASS |
| Lanza | Tierra→Viento | NONE | Sin resolución; sin fallback | PASS |

---

# 7. Resultado

## Cerrado

- las 13 técnicas diseñadas poseen `role_primary`;
- 13/13 poseen `mechanical_hooks[]`;
- 13/13 poseen `concordance_hooks[]`;
- hooks de ramas son condicionales;
- DIRECT_DAMAGE deja de exponerse automáticamente;
- Latigazo queda como CONTROL;
- Piel no expone STACKABLE_STATE a Concordancias;
- Armadura expone FORTIFICATION para Placa Fundacional;
- Espejo expone ABSORPTION_RESTORE para Embalse;
- Palma/Círculo exponen CONTAINED_TRIGGER para Núcleo;
- las 52 combinaciones de las 13 técnicas diseñadas tienen resultado determinista bajo la matriz actual.

## Riesgos no bloqueantes detectados

Persisten convergencias mecánicas en técnicas concretas:

- Fuego→Metal y Agua→Metal sobre Armadura pueden terminar en DEF_GRANTED;
- Fuego/Metal/Viento→Tierra sobre Golpe/Temblor pueden converger en DIRECT_DAMAGE;
- Fuego/Metal/Tierra→Agua sobre Latigazo convergen en CONTROL_POWER;
- varios Ecos sobre Espejo pueden escalar ABSORPTION_RESTORE.

Esto no viola el resolver ni produce doble resolución, pero debe considerarse al diseñar Viento y durante benchmark.

## Pendiente

- las 3 técnicas de Viento;
- porcentajes finales de Concordancia;
- benchmark de 0.65 AOE;
- valores de manifestaciones;
- benchmark de cobertura/identidad tras añadir Viento.
