# Registro universal de estadísticas y propiedades de combate — v0.1

Fecha: 2026-09-28  
Rama: \`experiment/combat-stat-contract-v0.1\`  
Estado: **CONTRATO DE TAXONOMÍA / APROBADO COMO DIRECCIÓN / NO IMPLEMENTAR RUNTIME TODAVÍA**

## 0. Propósito

Este documento fija de una sola vez la taxonomía universal que deberán utilizar:

- estadísticas del jugador;
- estadísticas de NPC/monstruos/jefes;
- técnicas;
- ramas;
- equipo;
- pasivas;
- buffs/debuffs;
- aflicciones;
- Absorción;
- Control;
- Reflect;
- Retaliation;
- curación;
- Robo de Vida;
- Qi;
- Daño Aplazado;
- Concordancias;
- contenido de Arcos futuros.

Objetivo:

> Añadir contenido futuro no debe obligar a inventar una estadística nueva si la mecánica ya puede expresarse mediante una estadística, modificador, propiedad reactiva, parámetro de efecto o recurso interno existente.

Regla adicional:

> Que una propiedad esté registrada NO significa que esté disponible como fuente de poder en Arco 1.

---

# 1. Clases universales

Toda propiedad mecánica debe pertenecer a una de estas categorías.

\`\`\`text
CORE_STAT
MODIFIER_STAT
REACTIVE_PROPERTY
EFFECT_PARAMETER
INTERNAL_RESOURCE
DERIVED_RESULT
SYSTEM_FLAG
\`\`\`

No crear categorías nuevas sin necesidad arquitectónica real.

---

# 2. Estados de disponibilidad

Cada propiedad debe declarar uno de estos estados:

\`\`\`text
ACTIVE_ARC1
PREPARED_ARC1
RESERVED_FUTURE
CONTENT_ONLY
DEPRECATED
FORBIDDEN
\`\`\`

Definiciones:

- \`ACTIVE_ARC1\`: ya utilizada por contenido normal de Arco 1.
- \`PREPARED_ARC1\`: el motor debe soportarla, pero puede no tener fuentes comunes todavía.
- \`RESERVED_FUTURE\`: preparada arquitectónicamente; no debe aparecer como fuente normal en Arco 1.
- \`CONTENT_ONLY\`: parámetro de una técnica/estado concreto; no es stat permanente del actor.
- \`DEPRECATED\`: existe históricamente pero no debe migrarse.
- \`FORBIDDEN\`: concepto explícitamente rechazado como estadística global del nuevo sistema.

---

# 3. CORE_STAT

Son valores persistentes/derivados propios de una entidad y admiten múltiples fuentes compatibles.

## 3.1 Vida

### HP_CURRENT
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- representa Vida actual;
- nunca supera HP_MAX;
- toda pérdida usa DamagePacket o deuda previamente comprometida.

### HP_MAX
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- admite modificadores porcentuales;
- raíz Tierra e injerto pueden modificarla;
- redondeo único al recomputar el máximo.

## 3.2 Qi

### QI_CURRENT
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- recurso gastable;
- no posee regeneración pasiva universal.

### QI_MAX
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- puede crecer mediante cultivo/progresión.

### QI_REWARD
- clase: DERIVED_RESULT / recompensa
- disponibilidad: ACTIVE_ARC1
- no es Qi utilizable en combate;
- no debe confundirse con QI_CURRENT.

## 3.3 Precisión y Evasión

### PRECISION
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- referencia normal: 100;
- puede superar 100 internamente;
- entra en:
  \`clamp(PRECISION_EFFECTIVE - EVASION, 5, 100)\`.

### EVASION
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- no crea segunda tirada;
- puede ser negativa;
- el clamp final de impacto limita el resultado;
- raíz Viento e injerto pueden modificarla.

## 3.4 DEF

### DEF
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- reducción plana universal de daño directo;
- nunca negativa;
- una sola aplicación por impacto.

No existen CORE_STAT separados para DEF física, mágica o elemental.

## 3.5 Penetración

### PERCENT_PENETRATION
- clase: CORE_STAT ofensiva
- disponibilidad: ACTIVE_ARC1
- rango efectivo cerrado: 0–100%;
- se aplica antes de Penetración plana;
- no afecta Absorción;
- no afecta DOT salvo excepción futura explícita.

### FLAT_PENETRATION
- clase: CORE_STAT ofensiva
- disponibilidad: ACTIVE_ARC1
- se aplica después de PERCENT_PENETRATION;
- no puede producir DEF efectiva negativa.

## 3.6 Crítico

### CRIT_CHANCE
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- base normal: 5%;
- rango efectivo: 0–100%;
- un roll por impacto;
- DOT no critica por defecto.

### CRIT_DAMAGE
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- multiplicador base: x1.50;
- bonos se agregan al componente adicional de crítico;
- no tiene aún un techo numérico de balance universal;
- cualquier cap futuro debe ser una decisión explícita.

## 3.7 Control y Tenacidad

### CONTROL
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- entra en:
  \`clamp(CONTROL_EFFECTIVE - TENACITY, 5, 100)\`.

### TENACITY
- clase: CORE_STAT
- disponibilidad: ACTIVE_ARC1
- sólo modifica probabilidad de Control;
- no reduce automáticamente duración o magnitud de debuffs ordinarios.

## 3.8 Robo de Vida

### LIFESTEAL_PERCENT
- clase: CORE_STAT
- disponibilidad: PREPARED_ARC1
- no necesita tener fuentes normales en Arco 1;
- sólo toma daño elegible;
- DOT, Reflect, Retaliation y daño reactivo quedan excluidos por defecto;
- se acumula por acción y liquida una vez en ACTION_END;
- los modificadores normales de curación no lo aumentan ni reducen salvo propiedad explícita \`affects_lifesteal\`.

---

# 4. MODIFIER_STAT

Son modificadores agregables que pueden existir como fuentes de equipo, raíces, estados, ramas o Concordancias.

## 4.1 Daño causado

### DAMAGE_DONE_PERCENT
- disponibilidad: ACTIVE_ARC1
- pool global compatible;
- no es multiplicador final separado.

Subfamilias compatibles por tags:

\`\`\`text
DIRECT_DAMAGE_PERCENT
PHYSICAL_DAMAGE_PERCENT
ELEMENTAL_DAMAGE_PERCENT
FIRE_DAMAGE_PERCENT
METAL_DAMAGE_PERCENT
WATER_DAMAGE_PERCENT
EARTH_DAMAGE_PERCENT
WIND_DAMAGE_PERCENT
TECHNIQUE_DAMAGE_PERCENT
WEAPON_DAMAGE_PERCENT
DOT_DAMAGE_PERCENT
\`\`\`

Cada una afecta sólo porciones/paquetes con tags compatibles.

## 4.2 Daño recibido

### DAMAGE_RECEIVED_PERCENT
- disponibilidad: PREPARED_ARC1
- actúa antes de DEF cuando corresponda al pipeline;
- debe declarar alcance/tags.

### DAMAGE_REDUCTION_PERCENT
- disponibilidad: RESERVED_FUTURE
- no confundir con DEF;
- si se activa en contenido futuro, debe ocupar una capa declarada del pipeline;
- no puede introducirse silenciosamente como "otra DEF".

## 4.3 Curación

### HEALING_DONE_PERCENT
- disponibilidad: PREPARED_ARC1

### HEALING_RECEIVED_PERCENT
- disponibilidad: PREPARED_ARC1

### ANTI_HEAL_PERCENT
- disponibilidad: PREPARED_ARC1
- afecta curación directa/regeneración según tags;
- no afecta LIFESTEAL_PERCENT por defecto.

## 4.4 Coste de Qi

### QI_COST_FLAT
- disponibilidad: ACTIVE_ARC1
- reducción/incremento plano de coste;
- se mantiene como capa separada de QI_COST_PERCENT.

### QI_COST_PERCENT
- disponibilidad: ACTIVE_ARC1
- pool porcentual aditivo compatible;
- raíz Agua e injerto usan esta propiedad;
- piso global exacto sigue pendiente de benchmark.

El orden exacto entre QI_COST_FLAT y QI_COST_PERCENT debe cerrarse antes de serialización runtime.

## 4.5 DEF modificada

### DEF_FLAT_MODIFIER
- disponibilidad: ACTIVE_ARC1

### DEF_PERCENT_MODIFIER
- disponibilidad: ACTIVE_ARC1

Orden:
\`\`\`text
DEF_base
→ DEF_FLAT_MODIFIER
→ DEF_PERCENT_MODIFIER
→ DEF_actual
\`\`\`

## 4.6 Modificadores de estadísticas probabilísticas

Pueden existir modificadores planos en puntos para:

\`\`\`text
PRECISION
EVASION
CRIT_CHANCE
CONTROL
TENACITY
PERCENT_PENETRATION
\`\`\`

Son puntos de la estadística correspondiente, no "bonos planos de daño".

---

# 5. REACTIVE_PROPERTY

Representan comportamiento ligado a eventos. El motor debe soportarlos aunque algunos no estén disponibles en Arco 1.

## 5.1 Reflect

### REFLECT_PERCENT
- disponibilidad: RESERVED_FUTURE
- porcentaje del daño directo recibido según base que se cierre;
- no se activa por DOT;
- evasión impide trigger;
- Absorción no impide el trigger de un impacto directo válido;
- no puede reflejar Reflect ni Retaliation;
- DamagePacket resultante:
  - can_crit=false;
  - can_use_def=true;
  - can_use_absorption=true;
  - can_trigger_lifesteal=false;
  - can_trigger_reflect=false;
  - can_trigger_retaliation=false.

## 5.2 Retaliation / Represalia

### RETALIATION_FLAT
- disponibilidad: RESERVED_FUTURE
- daño plano por impacto directo recibido;
- no se activa por DOT;
- evasión impide trigger;
- Absorción total no impide trigger si hubo impacto válido;
- no recursiva.

## 5.3 Vida al impactar

### LIFE_ON_HIT
- disponibilidad: RESERVED_FUTURE
- recuperación fija o parametrizada por impacto válido;
- distinta de LIFESTEAL_PERCENT;
- no hereda automáticamente modificadores de curación.

## 5.4 Vida al matar

### LIFE_ON_KILL
- disponibilidad: RESERVED_FUTURE
- usa ON_KILL;
- distinta de Robo de Vida.

## 5.5 Qi al impactar

### QI_ON_HIT
- disponibilidad: RESERVED_FUTURE
- preferencia arquitectónica: expresarlo mediante EffectDefinition \`ON_HIT → RESTORE_QI\`;
- el nombre queda registrado como propiedad de contenido, no como CORE_STAT obligatorio.

## 5.6 Qi al matar

### QI_ON_KILL
- disponibilidad: RESERVED_FUTURE
- preferencia: \`ON_KILL → RESTORE_QI\`.

## 5.7 Qi al crítico

### QI_ON_CRIT
- disponibilidad: RESERVED_FUTURE
- preferencia: \`ON_CRIT → RESTORE_QI\`.

## 5.8 Drenaje / Robo de Qi

### QI_DRAIN
- disponibilidad: PREPARED_ARC1
- operación, no CORE_STAT universal;
- transfiere como máximo el Qi realmente disponible;
- no existe por ahora una estadística global \`QI_STEAL_PERCENT\`.

## 5.9 Evasión reactiva

### EVASION_ON_TRIGGER
- disponibilidad: CONTENT_ONLY
- debe expresarse con trigger + MODIFY_STAT_TEMP;
- no necesita convertirse en stat permanente independiente.

## 5.10 Tenacidad reactiva

### TENACITY_ON_TRIGGER
- disponibilidad: CONTENT_ONLY
- trigger + MODIFY_STAT_TEMP.

---

# 6. EFFECT_PARAMETER

Pertenecen a una técnica, estado, aflicción, barrera, zona o instancia. No son stats permanentes del actor.

## 6.1 Daño y aflicciones

\`\`\`text
BASE_DAMAGE
DAMAGE_PORTION
DOT_POTENCY
DOT_DURATION
DOT_STACKS
DOT_MAX_STACKS
AFFLICTION_APPLICATION
AFFLICTION_GRADE
AFFLICTION_FAMILY
PERSISTENCE
INTENSITY
SPREAD
\`\`\`

Disponibilidad:
- ACTIVE_ARC1 o CONTENT_ONLY según técnica.

## 6.2 Control

\`\`\`text
CONTROL_POWER
CONTROL_DURATION
CONTROL_FAMILY
CONTROL_LOCKOUT
ACTION_DENIAL
INTERRUPT
\`\`\`

CONTROL_POWER puede derivar de CONTROL, pero la magnitud propia de una técnica es parámetro de contenido.

## 6.3 Debuffs

\`\`\`text
DEF_SHRED
EVASION_DEBUFF
PRECISION_DEBUFF
STAT_DEBUFF
DEBUFF_DURATION
\`\`\`

No todos usan Control.

## 6.4 Absorción

\`\`\`text
ABSORPTION_AMOUNT
ABSORPTION_MAXIMUM
ABSORPTION_RESTORE
ABSORPTION_DURATION
ABSORPTION_PRIORITY
\`\`\`

No existe una CORE_STAT universal de "Absorción permanente".

## 6.5 Duraciones

\`\`\`text
BUFF_DURATION
DEBUFF_DURATION
DOT_DURATION
CONTROL_DURATION
DEFENSIVE_DURATION
ZONE_DURATION
\`\`\`

Todas deben usar unidades de duración explícitas.

## 6.6 Stacking

\`\`\`text
STACKING_MODE
MAX_STACKS
STACK_VALUE
STACK_DURATION
\`\`\`

Modos:
- UNIQUE_REFRESH
- STACK_REFRESH
- INDEPENDENT

## 6.7 Área / propagación

\`\`\`text
AREA_EFFICIENCY
PROPAGATION
SPREAD
ZONE_RADIUS futuro si se necesita
\`\`\`

AOE normal no declara "número máximo de blancos": afecta a todos los combatientes hostiles válidos.

## 6.8 Ejecución

\`\`\`text
EXECUTION
PREPARED_ACTION
CANCELLABLE
COOLDOWN
RESOURCE_COST
\`\`\`

\`EXECUTION\` es una familia semántica/hook, no una estadística universal de "velocidad".

---

# 7. INTERNAL_RESOURCE

Recursos creados por contenido específico.

Ejemplos ya existentes o preparados:

\`\`\`text
CALOR
ARRAIGO
PLACAS
PESO
RESONANCIA
MARCAS
CARGAS
DEFERRED_DAMAGE_DEBT
\`\`\`

Cada recurso debe declarar:

- owner;
- scope;
- maximum;
- duration;
- gain operations;
- spend operations;
- cleanup rules;
- persistence;
- si puede ser leído por Concordancias.

No convertir automáticamente un INTERNAL_RESOURCE en CORE_STAT.

---

# 8. DERIVED_RESULT

Son valores calculados durante resolución y no deben persistirse como estadísticas base.

\`\`\`text
EFFECTIVE_PRECISION
HIT_CHANCE
EFFECTIVE_DEF
DAMAGE_BEFORE_DEF
DAMAGE_AFTER_DEF
ABSORBED_DAMAGE
LIFE_DAMAGE_COMMITTED
HP_LOSS_IMMEDIATE
ACTUAL_HP_DAMAGE
OVERKILL
CONTROL_CHANCE
HEALING_GENERATED
ACTUAL_HEALING
OVERHEALING
FINAL_QI_COST
\`\`\`

Se calculan desde las fuentes canónicas y se congelan cuando corresponde.

---

# 9. SYSTEM_FLAG

Propiedades booleanas/de permisos de paquetes.

Ejemplos:

\`\`\`text
can_crit
can_use_def
can_use_penetration
can_use_absorption
can_trigger_on_hit
can_trigger_on_damage
can_trigger_lifesteal
can_trigger_reflect
can_trigger_retaliation
can_kill
evadible
affects_lifesteal
persists_out_of_combat
persists_room_change
persists_save
\`\`\`

No son estadísticas y no deben aparecer como números del personaje.

---

# 10. Propiedades preparadas para Arcos futuros

Estas propiedades quedan registradas para evitar refactor estructural posterior.

## 10.1 Reflect / Retaliation
- REFLECT_PERCENT
- RETALIATION_FLAT

## 10.2 Recuperación reactiva
- LIFE_ON_HIT
- LIFE_ON_KILL
- QI_ON_HIT
- QI_ON_KILL
- QI_ON_CRIT

## 10.3 Daño aplazado
- DEFERRED_DAMAGE_PERCENT
- DEFERRED_DAMAGE_AMOUNT
- payment_schedule
- can_kill

Disponibilidad: RESERVED_FUTURE.

## 10.4 Inmunidades temporales

\`\`\`text
IMMUNITY_WINDOW
CONTROL_IMMUNITY_FAMILY
AFFLICTION_IMMUNITY_FAMILY
\`\`\`

No son resistencias porcentuales elementales.

## 10.5 Auras

\`\`\`text
AURA
AURA_RADIUS / scope
AURA_TARGET_FILTER
\`\`\`

Reservadas para contenido futuro.

## 10.6 Posturas

\`\`\`text
STANCE
STANCE_EXCLUSIVITY_GROUP
\`\`\`

## 10.7 Invocaciones

\`\`\`text
SUMMON
SUMMON_OWNER
SUMMON_DURATION
\`\`\`

## 10.8 Zonas / terreno

\`\`\`text
ZONE
ZONE_DURATION
ZONE_TICK
ZONE_OWNER
\`\`\`

Preparado en motor v0.2.

---

# 11. Conceptos que NO deben convertirse en estadísticas globales

Estos conceptos pueden existir como efectos concretos, pero no justifican un CORE_STAT por defecto:

\`\`\`text
QI_ON_CRIT
QI_ON_HIT
QI_ON_KILL
LIFE_ON_CRIT
LIFE_ON_DODGE
DAMAGE_ON_DODGE
DAMAGE_ON_BLOCK
BONUS_VS_BOSS
BONUS_VS_LOW_HP
BONUS_AFTER_CONTROL
BONUS_AFTER_CRIT
BONUS_FIRST_HIT
BONUS_LAST_HIT
\`\`\`

Se expresan como:

\`\`\`text
Trigger
+ Condition
+ Operation
\`\`\`

Esto evita una explosión de estadísticas.

---

# 12. Estadísticas explícitamente FORBIDDEN en el contrato actual

No existen como estadísticas base universales:

\`\`\`text
FIRE_RESISTANCE
METAL_RESISTANCE
WATER_RESISTANCE
EARTH_RESISTANCE
WIND_RESISTANCE

PHYSICAL_DEFENSE separada
MAGIC_DEFENSE separada
ELEMENTAL_DEFENSE separada

ATTACK_SPEED
CAST_SPEED
GLOBAL_SPEED_STAT

PASSIVE_QI_REGEN
QI_REGEN_PER_TURN

GENERIC_ELEMENTAL_ADVANTAGE
ELEMENTAL_ROCK_PAPER_SCISSORS_MULTIPLIER
\`\`\`

Razones:

- DEF ya es defensa universal contra daño directo;
- elementos son tags/interacciones;
- no existe una segunda capa automática de resistencias;
- no se desea una stat universal de Velocidad;
- Qi no se regenera pasivamente por turno;
- Wuxing no da multiplicadores automáticos de daño.

Una futura excepción requeriría un cambio explícito de contrato.

---

# 13. Inmunidades excepcionales

Sí puede existir contenido explícito como:

\`\`\`text
IMMUNE_FIRE
IMMUNE_BURN
IMMUNE_CONTROL_FAMILY(X)
IMMUNE_AFFLICTION_FAMILY(X)
\`\`\`

Son SYSTEM_FLAG/estado excepcional, no stats de resistencia.

Deben ser raros y temáticos.

---

# 14. Relaciones con Concordancias

Una Concordancia sólo puede modificar propiedades registradas.

Cada técnica expone un subconjunto:

\`\`\`text
mechanical_hooks[]
concordance_hooks[]
\`\`\`

Ejemplo:

\`\`\`text
mechanical_hooks:
- DIRECT_DAMAGE
- PRECISION
- CRIT_CHANCE

concordance_hooks:
- DIRECT_DAMAGE
- CRIT_CHANCE
\`\`\`

La existencia interna de PRECISION no obliga a exponerla a Concordancias.

Regla:

> Las Concordancias sólo ven \`concordance_hooks\`, no todas las propiedades mecánicas de la técnica.

Esto evita interacciones accidentales.

---

# 15. Prioridad de resolución de una Concordancia

La relación elemental global declara una lista de hooks compatibles por contexto.

Ejemplo conceptual:

\`\`\`text
FUEGO → VIENTO
OFFENSIVE:
1. CRIT_CHANCE
2. CRIT_DAMAGE
3. PRECISION
4. EXECUTION
5. PROPAGATION
\`\`\`

Si la técnica expone:

\`\`\`text
CRIT_CHANCE
PRECISION
PROPAGATION
\`\`\`

la Concordancia resuelve únicamente:

\`\`\`text
CRIT_CHANCE
\`\`\`

No mejora las tres propiedades simultáneamente salvo que la relación declare explícitamente una transformación compuesta.

Regla global:

> Un Eco produce una sola resolución primaria de Concordancia.

---

# 16. Registro de hooks reconocidos

Catálogo inicial formal:

## Ofensivos

\`\`\`text
DIRECT_DAMAGE
DAMAGE_PORTION
CRIT_CHANCE
CRIT_DAMAGE
PRECISION
PERCENT_PENETRATION
FLAT_PENETRATION
DEF_SHRED
EXECUTION
MULTIHIT
PROPAGATION
AREA_EFFICIENCY
\`\`\`

## Aflicciones

\`\`\`text
AFFLICTION_APPLICATION
DOT_POTENCY
DOT_DURATION
DOT_STACKS
PERSISTENCE
INTENSITY
SPREAD
ANTI_HEAL
\`\`\`

## Control/debuff

\`\`\`text
CONTROL_POWER
CONTROL_DURATION
MOBILITY_REDUCTION
EVASION_DEBUFF
PRECISION_DEBUFF
ACTION_DENIAL
INTERRUPT
STAT_DEBUFF
DEBUFF_DURATION
\`\`\`

## Defensivos

\`\`\`text
DEF_GRANTED
ABSORPTION
ABSORPTION_RESTORE
TENACITY_GRANTED
EVASION_GRANTED
DAMAGE_RECEIVED_MOD
FORTIFICATION
DEFENSIVE_DURATION
REACTIVE_RESPONSE
\`\`\`

## Recuperación/recursos

\`\`\`text
DIRECT_HEAL
REGENERATION
LIFESTEAL
LIFE_ON_HIT
LIFE_ON_KILL
QI_RESTORE
QI_DRAIN
QI_COST
QI_COST_PERCENT
INTERNAL_RESOURCE
\`\`\`

## Estados/estructura

\`\`\`text
STACKABLE_STATE
MARK
CHARGE
AURA
STANCE
SUMMON
ZONE
ZONE_DURATION
DEFERRED_DAMAGE
IMMUNITY_WINDOW
CONTROL_LOCKOUT
\`\`\`

Este catálogo es extensible, pero añadir un hook nuevo debe representar una familia mecánica reutilizable.

---

# 17. Compatibilidad con contenido futuro

El motor debe poder representar sin nueva CORE_STAT:

### "Al esquivar recupera 2 Qi"

\`\`\`text
ON_MISS_RECEIVED
→ RESTORE_QI(2)
\`\`\`

### "Al matar cura 5"

\`\`\`text
ON_KILL
→ HEAL(5, family=LIFE_ON_KILL)
\`\`\`

### "Al romper Absorción gana Evasión"

\`\`\`text
ON_ABSORPTION_BREAK
→ MODIFY_STAT_TEMP(EVASION)
\`\`\`

### "30% del daño se aplaza"

\`\`\`text
DAMAGE_CONVERSION
→ CREATE_DEFERRED_DAMAGE(30%)
\`\`\`

### "Devuelve 20% del daño"

\`\`\`text
ON_VALID_DIRECT_IMPACT_RECEIVED
→ DEAL_DAMAGE(type=REFLECT)
\`\`\`

### "Represalia de 3"

\`\`\`text
ON_VALID_DIRECT_IMPACT_RECEIVED
→ DEAL_DAMAGE(type=RETALIATION, base=3)
\`\`\`

No requieren stats nuevas si se expresan por efectos.

---

# 18. Reglas para añadir una propiedad nueva en el futuro

Antes de registrar una nueva estadística/propiedad:

1. comprobar si ya existe un CORE_STAT equivalente;
2. comprobar si puede ser MODIFIER_STAT;
3. comprobar si es realmente REACTIVE_PROPERTY;
4. comprobar si es un EFFECT_PARAMETER;
5. comprobar si basta Trigger + Condition + Operation;
6. comprobar si es INTERNAL_RESOURCE;
7. sólo crear una nueva propiedad si representa una dimensión mecánica reutilizable.

No crear stats por comodidad de una técnica concreta.

---

# 19. Invariantes

1. Ninguna técnica obliga por sí sola a crear una CORE_STAT.
2. Elemento no implica resistencia elemental.
3. DEF sigue siendo defensa universal de daño directo.
4. Absorción es recurso/pool, no DEF.
5. Control y debuff estadístico siguen separados.
6. Reflect y Retaliation son propiedades reactivas, no pipelines independientes.
7. Qi reactivo se modela preferentemente como efectos, no como docenas de stats.
8. Concordancias sólo modifican hooks expuestos.
9. Un Eco produce una resolución primaria de Concordancia.
10. Propiedades RESERVED_FUTURE no deben aparecer en Arco 1 salvo autorización explícita.
11. FORBIDDEN no puede ser introducida por equipo, técnica o NPC sin cambio de contrato.
12. Toda propiedad nueva debe tener clase y disponibilidad.

---

# 20. Estado inicial de disponibilidad

## ACTIVE_ARC1

\`\`\`text
HP_CURRENT
HP_MAX
QI_CURRENT
QI_MAX
PRECISION
EVASION
DEF
PERCENT_PENETRATION
FLAT_PENETRATION
CRIT_CHANCE
CRIT_DAMAGE
CONTROL
TENACITY
DAMAGE_DONE_PERCENT y subfamilias
QI_COST_FLAT
QI_COST_PERCENT
DEF_FLAT_MODIFIER
DEF_PERCENT_MODIFIER
DOT_POTENCY
DOT_DURATION
DOT_STACKS
ABSORPTION_*
CONTROL_POWER
DEBUFF_*
STACKING_*
INTERNAL_RESOURCE
\`\`\`

## PREPARED_ARC1

\`\`\`text
LIFESTEAL_PERCENT
HEALING_DONE_PERCENT
HEALING_RECEIVED_PERCENT
ANTI_HEAL_PERCENT
DAMAGE_RECEIVED_PERCENT
QI_DRAIN
AFFLICTION_GRADE/FAMILY/PERSISTENCE
ZONE
\`\`\`

## RESERVED_FUTURE

\`\`\`text
REFLECT_PERCENT
RETALIATION_FLAT
LIFE_ON_HIT
LIFE_ON_KILL
QI_ON_HIT
QI_ON_KILL
QI_ON_CRIT
DAMAGE_REDUCTION_PERCENT
DEFERRED_DAMAGE_*
AURA
STANCE
SUMMON
IMMUNITY_WINDOW
\`\`\`

## FORBIDDEN

\`\`\`text
FIRE_RESISTANCE
METAL_RESISTANCE
WATER_RESISTANCE
EARTH_RESISTANCE
WIND_RESISTANCE
PHYSICAL_DEFENSE separada
MAGIC_DEFENSE separada
ELEMENTAL_DEFENSE separada
ATTACK_SPEED
CAST_SPEED
PASSIVE_QI_REGEN
QI_REGEN_PER_TURN
GENERIC_ELEMENTAL_ADVANTAGE
\`\`\`

---

# 21. Próximo uso del registro

Las 20 Concordancias globales deben definirse usando exclusivamente este registro.

Para cada relación:

\`\`\`text
ORIGEN → DESTINO
IDENTIDAD
OFFENSIVE priorities
DEFENSIVE priorities
CONTROL priorities
UTILITY priorities
compatible concordance hooks
transformation rule
fallback = NONE
\`\`\`

Si ningún hook compatible está expuesto:

\`\`\`text
no transformación
no consumo de Eco
\`\`\`

Este registro debe mantenerse como fuente de verdad para nuevas estadísticas y propiedades de combate.


---

# 22. Hook estructural — CONTAINED_TRIGGER

`CONTAINED_TRIGGER` representa un estado encapsulado que espera una interacción futura compatible para liberar su efecto.

- clase: EFFECT_PARAMETER / hook estructural
- disponibilidad: PREPARED_ARC1
- no es una estadística permanente del actor
- debe declarar duración, condición de detonación, regla de consumo y operación de liberación
- puede declarar propagación secundaria si la técnica detonadora lo permite

Manifestación inicial aprobada:

```text
Tierra → Fuego
CONTAINED_TRIGGER
→ Núcleo de Magma
```

El resolver universal procesa el hook y su definición de contenido; no debe hardcodear el nombre de Núcleo de Magma.
