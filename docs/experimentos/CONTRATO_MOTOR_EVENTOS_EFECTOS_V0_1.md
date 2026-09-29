# Contrato del motor universal de eventos, efectos y Concordancias — v0.2

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **ARQUITECTURA APROBADA / NO IMPLEMENTAR RUNTIME TODAVÍA SIN AUTORIZACIÓN EXPLÍCITA**

## 0. Propósito

Este documento define la arquitectura que debe permitir que técnicas, ramas, estados, aflicciones, equipo, NPC, jefes, Concordancias y sistemas futuros puedan expresarse **sin añadir excepciones al núcleo de combate técnica por técnica**.

Objetivo de aceptación:

> Una mecánica nueva correctamente soportada por el contrato debe poder añadirse principalmente como datos/configuración de efectos y no obligar a modificar el resolver central de combate.

El contrato no reemplaza las fórmulas ya cerradas en `CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md`. Las organiza dentro de un motor genérico.

Registro taxonómico canónico:

- `docs/experimentos/REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md` es la **fuente de verdad para nombres, clase, disponibilidad y hooks universales**. Este contrato define cómo se resuelven; el registro define qué propiedades existen.
- Una propiedad nueva no debe añadirse primero en una técnica ni en el resolver: debe registrarse allí con clase y disponibilidad.

Restricciones de repositorio:

- no tocar `main`;
- no modificar `implement/3c5-npc-ver74`;
- no hacer merge automático;
- no implementar runtime desde este documento sin autorización explícita;
- no cambiar fórmulas cerradas de estadísticas mediante una refactorización arquitectónica;
- toda discrepancia entre este contrato y una regla numérica ya cerrada debe resolverse a favor del contrato numérico anterior hasta revisión explícita.

---

# 1. Principio rector

El motor **no debe conocer nombres de técnicas concretas** para resolver mecánicas generales.

Antipatrón:

```text
if tecnica == "palma_ardiente" ...
if tecnica == "piel_cobre" ...
if tecnica == "espejo_luna" ...
```

Modelo objetivo:

```text
TÉCNICA / ESTADO / EQUIPO
→ declara datos
→ declara tags
→ declara propiedades
→ declara triggers
→ declara condiciones
→ declara operaciones
→ el motor universal resuelve
```

Se permiten handlers especializados sólo para una **primitiva realmente nueva** que no pueda expresarse con operaciones universales existentes. Crear una técnica nueva no es motivo suficiente para crear un handler nuevo.

---

# 2. Capas del sistema

El motor se divide conceptualmente en seis capas:

```text
1. ACTION / intención
2. EVENT BUS / eventos
3. CONTEXT / resultados y metadata
4. EFFECT ENGINE / triggers + condiciones + operaciones
5. STATE ENGINE / buffs, debuffs, aflicciones, recursos y stacking
6. CONCORDANCE RESOLVER / interacción elemental basada en capacidades
```

Las técnicas son contenido que utiliza estas capas; no son una séptima capa de lógica especial.

---

# 3. Identificadores de trazabilidad

Toda acción y todo efecto derivado debe conservar procedencia suficiente para depurar cadenas complejas.

Campos conceptuales mínimos:

```text
combat_id
turn_id
action_id
root_action_id
impact_id
effect_instance_id
source_actor_id
target_actor_id
origin_effect_id
parent_event_id
reaction_depth
```

## 3.1 root_action_id

Todos los resultados derivados de una misma acción original conservan el mismo `root_action_id`.

Ejemplo:

```text
Palma
→ daño directo
→ Reflect
→ pérdida de Vida del atacante
```

Los tres pasos pertenecen a la misma cadena causal aunque sólo el primero sea el daño principal.

## 3.2 parent_event_id

Cada evento derivado identifica el evento que lo produjo.

Esto permite reconstruir:

```text
ACTION
└─ IMPACT
   ├─ LIFESTEAL
   ├─ APPLY_BURN
   └─ REFLECT
```

## 3.3 reaction_depth

Contador de profundidad reactiva usado como protección adicional frente a ciclos accidentales.

Las mecánicas normales deben evitar recursión mediante flags de elegibilidad; `reaction_depth` es una salvaguarda del motor, no el mecanismo primario de balance.

---

# 4. ActionContext

Toda acción debe generar un contexto estable antes de resolver impactos.

Campos conceptuales:

```text
action_id
root_action_id
source
declared_target
resolved_targets[]
technique_id / action_family
role_primary
tags[]
element_tags[]
area_mode
resource_costs
cooldown_data
concordance_context
temporary_modifiers
```

## 4.1 Rol principal

Valores mínimos:

```text
OFFENSIVE
DEFENSIVE
CONTROL
UTILITY
HYBRID
```

El rol principal sirve para prioridades de contenido y Concordancias, pero **no sustituye las capacidades reales**.

Una técnica OFFENSIVE puede exponer CONTROL.  
Una DEFENSIVE puede exponer REACTIVE_RESPONSE.  
Una UTILITY puede generar ABSORPTION.

---

# 5. Tags universales

Los tags describen procedencia, tipo y semántica.

Familias mínimas preparadas:

## 5.1 Procedencia

```text
TECHNIQUE
BASIC_ATTACK
WEAPON
ITEM
EQUIPMENT
STATE
AFFLICTION
ENVIRONMENT
NPC_ABILITY
BOSS_ABILITY
```

## 5.2 Tipo de resolución de daño

```text
DIRECT
DOT
REFLECT
RETALIATION
DELAYED
SELF_RECOIL
SECONDARY_REACTIVE
```

## 5.3 Naturaleza

```text
PHYSICAL
ELEMENTAL
FIRE
METAL
WATER
EARTH
WIND
```

## 5.4 Forma

```text
UNITARGET
AOE
MULTIHIT
PROJECTILE
MELEE
RANGED
```

Los tags futuros pueden añadirse sin cambiar el pipeline siempre que no introduzcan una nueva regla de resolución.

---

# 6. Capacidades / hooks mecánicos

Una técnica o efecto declara **qué propiedades reales expone**. Éstas son los puntos sobre los que pueden actuar ramas, equipo, estados o Concordancias.

Catálogo extensible inicial:

## 6.1 Ofensivos

```text
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
```

## 6.2 Aflicciones / persistencia ofensiva

```text
AFFLICTION_APPLICATION
DOT_POTENCY
DOT_DURATION
DOT_STACKS
PERSISTENCE
INTENSITY
SPREAD
ANTI_HEAL
```

## 6.3 Control / debilitación

```text
CONTROL_POWER
CONTROL_DURATION
EVASION_DEBUFF
PRECISION_DEBUFF
ACTION_DENIAL
INTERRUPT
STAT_DEBUFF
DEBUFF_DURATION
```

## 6.4 Defensivos

```text
DEF_GRANTED
ABSORPTION
ABSORPTION_RESTORE
TENACITY_GRANTED
EVASION_GRANTED
DAMAGE_RECEIVED_MOD
FORTIFICATION
DEFENSIVE_DURATION
REACTIVE_RESPONSE
```

## 6.5 Recuperación / recursos

```text
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
```

## 6.6 Estados estructurales

```text
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
CONTAINED_TRIGGER
```

Una técnica no tiene obligación de exponer todas las capacidades asociadas a su rol.

---

# 7. Event Bus universal

Los efectos se disparan mediante eventos normalizados.

Catálogo inicial:

## 7.1 Acción

```text
ACTION_DECLARE
ACTION_VALIDATE
ACTION_START
BEFORE_COST
COST_PAID
BEFORE_TARGET_RESOLUTION
ACTION_END
```

## 7.2 Impacto

```text
BEFORE_HIT
ON_MISS
ON_HIT
ON_CRIT
BEFORE_DAMAGE_BUILD
AFTER_DAMAGE_BUILD
AFTER_DEF
ON_ABSORB
ON_ABSORPTION_BREAK
ON_HP_DAMAGE
IMPACT_RESOLVED
```

## 7.3 Control

```text
CONTROL_ATTEMPT
CONTROL_SUCCESS
CONTROL_FAIL
CONTROL_EXPIRE
```

## 7.4 Estados

```text
EFFECT_APPLY_ATTEMPT
ON_EFFECT_APPLY
ON_EFFECT_REFRESH
ON_EFFECT_STACK
ON_EFFECT_REMOVE
ON_EFFECT_EXPIRE
ON_MAX_STACK
```

## 7.5 Turno / combate

```text
TURN_START
TURN_END
COMBAT_START
COMBAT_END
ENTER_COMBAT
LEAVE_COMBAT
```

## 7.6 Recursos y recuperación

```text
BEFORE_HEAL
ON_HEAL
ON_OVERHEAL
ON_QI_SPEND
ON_QI_GAIN
ON_QI_DRAIN
```

## 7.7 Fuentes especiales de daño

```text
ON_DOT_TICK
ON_REFLECT
ON_RETALIATION
ON_DELAYED_DAMAGE
ON_SELF_RECOIL
```

## 7.8 Muerte

```text
LETHAL_HIT
ON_DEATH
ON_KILL
```

No todos los eventos se emiten en Arco 1; el contrato reserva sus nombres y semántica para no introducir incompatibilidades futuras.

---

# 8. Ventanas de mutación y fases de resolución

No todos los eventos pueden modificar lo mismo.

Fases:

```text
PRE_ACTION
↓
COST
↓
PRE_HIT
↓
HIT_RESOLUTION
↓
DAMAGE_BUILD
↓
MITIGATION
↓
ABSORPTION
↓
HP_COMMIT
↓
FREEZE_IMPACT_RESULT
↓
POST_HIT_SOURCE
↓
POST_HIT_TARGET
↓
REACTIONS
↓
DEATH_RESOLUTION
↓
POST_ACTION
```

## 8.1 Antes del freeze

Los modificadores autorizados pueden cambiar la ejecución aún abierta:

- coste;
- Precisión;
- porciones;
- magnitud compatible;
- crítico;
- Penetración;
- modificadores recibidos;
- parámetros previos de Absorción si una regla explícita actúa antes del impacto.

## 8.2 Después del freeze

Una vez congelado `IMPACT_RESULT`:

> ningún efecto posterior puede recalcular retroactivamente ese impacto.

Puede:

- curar;
- recuperar Qi;
- aplicar estados;
- generar DOT;
- Reflect;
- Retaliation;
- crear daño secundario;
- modificar estadísticas futuras;
- crear recursos internos;
- resolver muerte.

No puede:

- añadir daño al impacto ya cerrado;
- volver a tirar crítico de ese impacto;
- cambiar la DEF usada;
- modificar la Absorción ya consumida retroactivamente.

---

# 9. ImpactResult canónico

Se conserva el contrato ya cerrado y se prepara su extensión futura.

Campos actuales:

```text
hit
critical
damage_before_def
effective_def
damage_after_def
absorbed_damage
hp_damage
actual_hp_damage
target_killed
```

Campos preparados para daño aplazado:

```text
life_damage_committed
hp_loss_immediate
deferred_loss_created
```

Debe existir relación:

```text
life_damage_committed
=
hp_loss_immediate
+
deferred_loss_created
```

El resultado congelado es inmutable.

---

# 10. DamagePacket universal

Toda pérdida de Vida debe provenir de un paquete explícito.

Campos conceptuales:

```text
source
target
base_amount
damage_source_type
tags[]
element_tags[]
can_crit
can_use_def
can_use_penetration
can_use_absorption
can_trigger_lifesteal
can_trigger_reflect
can_trigger_retaliation
can_trigger_on_hit
can_trigger_on_damage
can_kill
provenance
```

## 10.1 Daño directo

Valores normales:

```text
can_crit = true según acción
can_use_def = true
can_use_penetration = true
can_use_absorption = true
can_trigger_lifesteal = true por defecto
can_trigger_reflect = true
can_trigger_retaliation = true
```

## 10.2 DOT

Contrato actual:

```text
can_crit = false por defecto
can_use_def = false
can_use_penetration = false
can_use_absorption = true
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false
```

Las excepciones requieren propiedad explícita.

## 10.3 Reflect

```text
damage_source_type = REFLECT
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false
```

No puede generar ciclo de Reflect.

## 10.4 Retaliation

```text
damage_source_type = RETALIATION
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false
```

## 10.5 Daño aplazado

```text
damage_source_type = DELAYED
can_use_def = false
can_use_penetration = false
can_use_absorption = false
can_crit = false
```

Representa una deuda ya comprometida, no un ataque nuevo.

## 10.6 Retroceso espiritual

```text
damage_source_type = SELF_RECOIL
can_use_def = false
can_use_penetration = false
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false
```

Su interacción exacta con Absorción y muerte permanece pendiente donde el contrato anterior ya la dejó pendiente.

---

# 11. HealPacket universal

Toda recuperación de Vida debe distinguir su familia.

```text
DIRECT_HEAL
REGENERATION
LIFESTEAL
LIFE_ON_HIT
LIFE_ON_KILL
```

Campos:

```text
source
target
healing_family
base_amount
tags[]
affected_by_healing_done
affected_by_healing_received
can_crit
provenance
```

## 11.1 Curación directa

Respeta:

```text
healing_generated
actual_healing
overhealing
```

y modificadores de curación realizada/recibida.

## 11.2 Regeneración

Periódica; puede usar los modificadores normales de curación según contrato existente.

## 11.3 Robo de Vida

- usa daño directo elegible;
- usa `actual_hp_damage` actualmente;
- cuando exista Aplazamiento, deberá usar daño comprometido real según contrato reservado;
- no recibe modificadores normales de curación;
- no critica;
- límite agregado por acción.

## 11.4 Vida al impactar / matar

Son familias independientes y no escalan con Robo de Vida.

---

# 12. ResourcePacket universal

Debe soportar al menos:

```text
QI_SPEND
QI_RESTORE
QI_DRAIN
INTERNAL_RESOURCE_GAIN
INTERNAL_RESOURCE_SPEND
STACK_GAIN
STACK_SPEND
```

Qi sigue las reglas cerradas:

- no regeneración pasiva por turno;
- meditación;
- consumibles;
- piedras espirituales;
- drenaje/robo explícito;
- otras fuentes sólo si están declaradas.

Los recursos internos, como Calor, no deben confundirse con Qi.

---

# 13. ControlAttempt universal

Un control no debe programar su fórmula por técnica.

Campos:

```text
source
target
control_family
base_control
effective_control
target_tenacity
application_chance
duration
tags[]
lockout_family
provenance
```

Resolución base:

```text
P(Control)
=
clamp(Control efectivo - Tenacidad objetivo, 5, 100)
```

Familias preparadas:

```text
SKIP_ACTION
STUN
INTERRUPT
SILENCE
DISARM
FEAR
FORCED_TARGET
```

No todas están activas en Arco 1.

Un debuff estadístico ordinario no se convierte automáticamente en Control.

---

# 14. EffectDefinition

Todo buff, debuff, estado, pasiva, rama o reacción debe poder representarse mediante una definición común.

Campos mínimos:

```text
effect_id
stack_group
owner
source
polarity
tags[]
duration
duration_unit
stacking_mode
max_stacks
modifiers[]
triggers[]
operations[]
frequency_rules[]
removal_rules[]
provenance
```

Se conservan modos ya cerrados:

```text
UNIQUE_REFRESH
STACK_REFRESH
INDEPENDENT
```

No debe inferirse automáticamente qué efecto multidimensional es "más fuerte" si varios comparten grupo; el contenido debe declarar prioridad.

---

# 15. Trigger + Condition + Operation

Ésta es la unidad compositiva principal.

## 15.1 Trigger

Ejemplo:

```text
ON_HP_DAMAGE
```

## 15.2 Conditions

Lista declarativa:

```text
source_is_owner
damage_source_is(DIRECT)
actual_hp_damage > 0
target_hp_percent < 30
has_tag(FIRE)
not_has_tag(DOT)
critical == true
has_effect(X)
stacks(X) >= 3
```

Las condiciones consultan contexto; no deben mutarlo.

## 15.3 Operation

La operación produce el cambio.

Primitivas iniciales:

```text
DEAL_DAMAGE
HEAL
RESTORE_QI
SPEND_QI
DRAIN_QI

APPLY_EFFECT
REMOVE_EFFECT
REFRESH_EFFECT
EXTEND_DURATION

ADD_STACK
REMOVE_STACK
SET_STACKS

ADD_ABSORPTION
RESTORE_ABSORPTION
REMOVE_ABSORPTION

MODIFY_STAT_TEMP
MODIFY_NEXT_ACTION
MODIFY_NEXT_IMPACT

ATTEMPT_CONTROL
SKIP_ACTION
CANCEL_PREPARED_ACTION

STORE_RESOURCE
CONSUME_RESOURCE

CREATE_MARK
CONSUME_MARK

CREATE_DEFERRED_DAMAGE
REDUCE_DEFERRED_DAMAGE
PURGE_DEFERRED_DAMAGE
```

Primitivas futuras pueden añadirse sin cambiar el modelo Trigger/Condition/Operation.

---

# 16. Frecuencia universal

Todo trigger debe poder limitarse mediante scopes estándar.

```text
once_per_impact
once_per_target_per_action
once_per_action
once_per_turn
once_per_activation
once_per_combat
unlimited
```

El motor debe mantener claves de consumo por `effect_instance_id + scope`.

Ejemplos:

## 16.1 Piel de Cobre

```text
ON_HP_DAMAGE_RECEIVED
→ ADD_STACK(ARRAIGO)
→ once_per_action
```

## 16.2 Reflect

```text
ON_VALID_DIRECT_IMPACT_RECEIVED
→ DEAL_DAMAGE(REFLECT)
→ once_per_impact
```

## 16.3 Pasiva futura

```text
ON_CRIT
→ RESTORE_QI(1)
→ once_per_turn
```

No debe existir lógica ad hoc de "ya ocurrió" distinta para cada técnica.

---

# 17. Orden determinista de efectos simultáneos

Cuando varios efectos escuchan el mismo evento, el resultado debe ser determinista.

Cada trigger puede declarar:

```text
priority
```

Orden conceptual:

```text
1. reglas globales obligatorias
2. efectos de la acción
3. efectos de la fuente
4. efectos del objetivo
5. equipo / pasivas según prioridad declarada
6. reacciones secundarias
```

Para misma prioridad se usa un criterio estable documentado, nunca orden incidental de arrays/DOM.

La prioridad no debe usarse como parche frecuente; sólo cuando el orden tenga significado mecánico real.

---

# 18. Reacciones y prevención de recursión

Reflect, Retaliation, daño reactivo y futuras contraacciones deben generar paquetes con flags explícitos.

Regla:

> Una reacción nunca hereda automáticamente todos los permisos del evento que la originó.

Debe declarar qué puede volver a disparar.

Ejemplo Reflect:

```text
source_type = REFLECT

can_trigger_reflect = false
can_trigger_retaliation = false
can_trigger_lifesteal = false
can_trigger_on_hit = false
```

El motor debe contar además con:

```text
reaction_depth
max_reaction_depth
```

como cinturón de seguridad ante una configuración errónea.

Al alcanzar el límite se aborta la nueva reacción, se registra diagnóstico y no se continúa silenciosamente.

---

# 19. Absorción como recurso universal

Una barrera no debe pertenecer al código de una técnica.

Estructura conceptual:

```text
absorption_pool_id
source
current
maximum
duration
tags[]
priority
restore_rules
break_rules
```

Debe permitir:

- consumir reserva;
- restaurar reserva;
- máximo;
- duración;
- ruptura;
- eventos `ON_ABSORB`;
- `ON_ABSORPTION_BREAK`;
- múltiples pools si alguna mecánica futura lo exige;
- prioridad explícita entre pools múltiples.

Espejo de Luna:

```text
TURN_START
→ RESTORE_ABSORPTION(% maximum)
```

Cuerpo-Horno:

```text
ON_ABSORB
→ STORE_RESOURCE(CALOR)
```

No requieren resolver especial por nombre.

---

# 20. Aflicciones como familia de EffectDefinition

Una aflicción declara:

```text
family
source
potency
duration
stacks
max_stacks
stacking_mode
tick_event
damage_packet_template
tags
```

El motor permite, sin asumir que todas sean iguales:

- Quemadura;
- Hemorragia;
- Veneno;
- futuras aflicciones;
- daño sin DEF;
- capacidad crítica opcional;
- ignorar Absorción opcional;
- stacking independiente;
- stacking compartido;
- duración propia.

Las reglas particulares pertenecen a la familia, no a un `if tecnica`.

---

# 21. Reflect y Retaliation preparados desde ahora

Aunque post-Arco 1, el modelo debe admitirlos sin refactor estructural posterior.

## 21.1 Reflect

Semántica cerrada:

- porcentaje del daño directo recibido;
- DOT no activa;
- evasión impide trigger;
- Absorción no impide trigger si hubo impacto directo válido;
- no genera recursión.

Debe poder elegir explícitamente cuál magnitud del `ImpactResult` usa como base cuando se cierre el balance final, sin cambiar el tipo de operación.

## 21.2 Retaliation

- daño plano por impacto directo recibido;
- DOT no activa;
- evasión impide;
- Absorción no impide trigger si hubo impacto válido;
- no recursión.

Reflect y Retaliation son dos configuraciones del sistema reactivo, no dos pipelines independientes.

---

# 22. Daño aplazado preparado desde ahora

El motor debe reservar:

```text
CREATE_DEFERRED_DAMAGE
REDUCE_DEFERRED_DAMAGE
PURGE_DEFERRED_DAMAGE
ON_DELAYED_DAMAGE
```

Una deuda debe conservar:

```text
source
amount_remaining
payment_schedule
can_kill
tags
provenance
```

No es DOT y no reutiliza flags de DOT por conveniencia.

---

# 23. Estados internos y recursos de técnica

El motor debe soportar recursos distintos de HP/Qi:

```text
CALOR
ARRAIGO
PLACAS
PESO
RESONANCIA
MARCAS
CARGAS
otros futuros
```

No todos son iguales:

- algunos pertenecen al actor;
- otros al objetivo;
- algunos a una instancia de técnica;
- otros son estados persistentes;
- algunos tienen máximo;
- otros duración;
- algunos se consumen;
- otros sólo representan stacks.

La definición de cada recurso declara alcance y ciclo de vida.

---

# 24. Concordancias: arquitectura global

## 24.1 Principio

Las Concordancias pertenecen a la relación elemental:

```text
ORIGEN → DESTINO
```

No pertenecen a una técnica concreta.

La técnica receptora sólo declara:

```text
rol
capacidades/hooks compatibles
```

El resolver:

```text
Eco existente
↓
identificar ORIGEN
↓
elemento de técnica receptora = DESTINO
↓
consultar contrato ORIGEN→DESTINO
↓
consultar role_primary + concordance_hooks[] de receptora
↓
encontrar canal compatible según prioridad
↓
producir modificador/transformation descriptor
↓
si hubo resolución válida: consumir Eco
↓
si no hubo propiedad compatible: no consumir Eco; la generación posterior de un Eco nuevo puede sustituirlo según §38.2
```

## 24.2 No fallback genérico

Prohibido:

```text
"si no tiene la mecánica principal, darle +15% daño"
```

salvo que el contrato global de esa relación elemental incluya realmente `DIRECT_DAMAGE` como canal compatible.

## 24.3 Técnica futura

Una técnica futura puede introducir una propiedad nueva y volverse receptora de una Concordancia existente sin cambiar el contrato elemental si esa propiedad cae dentro de un canal ya definido.

Ejemplo:

```text
TIERRA → FUEGO
identidad = persistencia / contención / intensidad sostenida
```

Puede actuar sobre:

- duración de Quemadura;
- zona ígnea persistente;
- carga de calor;
- sello térmico;
- invocación temporal compatible;

sin que el motor tenga que conocer ninguno de esos nombres.

## 24.4 Roles y prioridades

Una relación elemental puede tener prioridades distintas según contexto:

```text
OFFENSIVE
DEFENSIVE
CONTROL
UTILITY
```

Pero las prioridades buscan **capacidades**, no IDs de técnicas.

Ejemplo conceptual:

```text
FUEGO → TIERRA

OFFENSIVE:
1. DIRECT_DAMAGE
2. CONTROL_POWER
3. DEF_SHRED
4. PERCENT_PENETRATION
5. FLAT_PENETRATION

DEFENSIVE:
1. DEF_GRANTED
2. ABSORPTION
3. FORTIFICATION
4. TENACITY_GRANTED
5. DEFENSIVE_DURATION
```

Las 20 relaciones dirigidas deberán recibir este tratamiento antes de cerrar Concordancias numéricas.

---

# 25. Eco elemental como estado

Los Ecos deben modelarse mediante State Engine.

Campos conceptuales:

```text
echo_element
source
created_by_action
duration / expiry rule
consumable
eligible_receivers
```

Una acción pura compatible puede producir Eco según contrato.

Definitivas híbridas:

- no generan Eco;
- no consumen Eco;
- no reciben Concordancias;
- no activan Concordancias.

---

# 26. Ramas como modificadores de datos

Una rama no debería reescribir una técnica.

Debe poder:

- añadir capacidad;
- modificar magnitud;
- cambiar máximo de stacks;
- añadir trigger;
- añadir operación;
- modificar duración;
- modificar coste;
- modificar flags del paquete;
- añadir condición;
- añadir una sinergia condicional con otra rama.

Ejemplo conceptual:

```text
Palma base:
hooks = [DIRECT_DAMAGE]

Ascua:
+ AFFLICTION_APPLICATION
+ DOT_POTENCY
+ PERSISTENCE
```

Una Concordancia que requiere PERSISTENCE pasa a poder resolver Palma después de adquirir esa rama **sin que el resolver conozca el nombre Ascua**.

---

# 27. AOE en el motor genérico

Contrato global existente:

```text
AOE
→ todos los NPC hostiles de la sala
→ incorporación inmediata al combate
→ impacto independiente por objetivo
```

El resolver debe tratar:

- `action_id` común;
- `impact_id` distinto por objetivo;
- efectos `once_per_action` compartidos;
- efectos `once_per_target_per_action` separados;
- Robo de Vida agregado y limitado por acción;
- Concordancia aplicada a la ejecución según su descriptor;
- 65% provisional de daño al existir un solo objetivo válido.

Ningún contenido AOE define cantidad máxima de enemigos salvo futura excepción explícita distinta de la regla AOE normal.

---

# 28. Muerte y atribución

Debe conservarse:

```text
kill_source
killer_actor
root_action_id
damage_source_type
action / effect family
tags
```

Orden existente:

```text
impacto congelado
→ efectos de fuente
→ estados del objetivo si sobrevive
→ reacciones
→ resolver muerte
→ ON_DEATH
→ ON_KILL
```

Un DOT conserva su fuente original para atribución.

Un paquete reactivo conserva su provenance.

---

# 29. Redondeo

Este motor no modifica la política ya cerrada:

> nunca redondear cálculos intermedios.

Los paquetes conservan decimal mientras están en construcción y redondean una sola vez cuando se convierten en modificación discreta del recurso correspondiente.

No debe haber operaciones que redondeen internamente y luego vuelvan a entrar al pipeline como si fueran valores base salvo regla explícita.

---

# 30. Registro y diagnóstico

Para permitir benchmark y auditoría, el resolver debe poder registrar en modo debug:

```text
ACTION_START
targets
cost
echo_before
concordance_resolution

por impacto:
precision
hit/miss
crit
damage portions
modifiers
effective DEF
absorbed
HP damage

post-impact triggers
effects applied
reactions
death

echo_after
resources_after
```

Además debe registrar:

- efecto ignorado por condición;
- trigger bloqueado por frecuencia;
- Concordancia sin hook compatible;
- reacción bloqueada por guardia antirrecursión;
- intento de mutar un ImpactResult congelado;
- referencia a primitive/op desconocida.

No son mensajes normales al jugador; son diagnóstico.

---

# 31. Validación de contenido

Antes de cargar una técnica/estado, el motor o una herramienta de auditoría debería comprobar:

- event name válido;
- operation válida;
- tags válidos;
- stacking válido;
- frequency scope válido;
- hooks declarados coherentes;
- valores requeridos presentes;
- una operación no intenta modificar una fase ya cerrada;
- un Reflect/Retaliation no tiene permisos recursivos por accidente;
- una Concordancia no consume Eco si no resuelve un hook;
- un DOT no activa flags directos salvo excepción explícita;
- una Definitiva híbrida no entra a Concordancias;
- ningún efecto de Qi crea regeneración pasiva automática;
- un debuff estadístico no usa Tenacidad salvo que sea Control real.

---

# 32. Invariantes del núcleo

Estas reglas deben mantenerse en cualquier implementación:

1. **No hardcode de técnicas en el resolver central.**
2. **ImpactResult inmutable después de freeze.**
3. **Toda pérdida de Vida usa DamagePacket o deuda previamente creada.**
4. **Toda curación usa HealPacket.**
5. **Todo cambio de Qi/recurso usa ResourcePacket/operación registrada.**
6. **Todo Control usa ControlAttempt salvo excepción explícita de guion fuera del combate normal.**
7. **Todo buff/debuff/aflicción usa State Engine.**
8. **Toda reacción conserva provenance.**
9. **Toda reacción declara permisos de retrigger.**
10. **No recursión Reflect↔Reflect, Retaliation↔Retaliation ni Reflect↔Retaliation.**
11. **DOT no se convierte accidentalmente en impacto directo.**
12. **Una Concordancia sólo consume Eco si produjo una transformación válida.**
13. **Las ramas pueden añadir hooks; el motor no pregunta por nombres de ramas.**
14. **No existe regeneración pasiva universal de Qi.**
15. **El orden de efectos simultáneos es determinista.**
16. **Las reglas de frecuencia pertenecen al motor, no a flags manuales por técnica.**
17. **Las fórmulas cerradas de estadísticas siguen siendo fuente de verdad matemática.**

---

# 33. Prueba de extensibilidad

La arquitectura se considera insuficiente si alguno de estos ejemplos requiere modificar el resolver central.

## Caso A — Manto del Escorpión

```text
duración 3 turnos
+5 Tenacidad
al recibir impacto directo:
  aplica Veneno al atacante
si atacante ya estaba envenenado:
  recupera 2 Qi
máximo una vez por turno
```

Debe componerse con:

```text
MODIFY_STAT_TEMP
ON_HIT_RECEIVED
condition: has_effect(effect_family)
APPLY_EFFECT
RESTORE_QI
once_per_turn
```

## Caso B — Espina de Jade

```text
20% Reflect
+3 Retaliation
```

Debe usar dos triggers configurados y guardas antirrecursión sin nuevo pipeline.

## Caso C — Sello del Deudor

```text
30% del daño comprometido a Vida
se aplaza durante 2 pagos
```

Debe usar `CREATE_DEFERRED_DAMAGE`.

## Caso D — Técnica que roba Qi al crítico

```text
ON_CRIT
→ DRAIN_QI(3)
→ once_per_target_per_action
```

## Caso E — Técnica futura con Concordancia

Una técnica Fuego nueva expone:

```text
PERSISTENCE
ZONE_DURATION
```

Tierra→Fuego debe poder encontrar un canal compatible sin registrar el ID de esa técnica.

---

# 34. Pruebas mínimas obligatorias antes de implementación real

## Pipeline

- fallo por Evasión;
- impacto normal;
- crítico;
- DEF reduce a 0;
- Absorción parcial;
- Absorción total;
- impacto letal;
- AOE con varios objetivos;
- AOE con un objetivo.

## Eventos

- once_per_impact;
- once_per_action;
- once_per_turn;
- once_per_activation;
- múltiples triggers simultáneos con prioridad.

## Estados

- refresh;
- stack;
- independiente;
- expiración;
- remover;
- máximo de stacks.

## Reacciones

- Reflect;
- Retaliation;
- Reflect + Absorción total;
- evasión impide ambos;
- DOT no activa;
- no recursión.

## Recuperación

- Robo de Vida;
- Vida al impactar;
- Vida al matar;
- curación directa;
- sobrecuración;
- Qi drain con objetivo sin suficiente Qi.

## Control

- éxito;
- fallo;
- límites 5/100;
- lockout;
- debuff ordinario ignorando Tenacidad.

## Concordancias

- hook compatible;
- sin hook compatible → no consume Eco;
- rama añade hook;
- defensiva y ofensiva del mismo elemento resuelven propiedades diferentes;
- AOE aplica descriptor a toda la ejecución según contrato;
- híbrida ignora completamente Eco.

---

# 35. Criterio de aceptación para una técnica nueva

Antes de aceptar contenido nuevo, responder:

```text
¿puede expresarse con:
- tags
- hooks
- triggers
- condiciones
- operaciones
- estados
- frecuencias
- prioridades?
```

Si SÍ:

> no modificar el núcleo.

Si NO:

1. determinar si falta una **primitiva universal** real;
2. comprobar que la nueva primitiva serviría a múltiples contenidos futuros;
3. añadirla al contrato;
4. testearla aisladamente;
5. recién después permitir que una técnica la utilice.

Nunca crear una primitiva universal sólo para disfrazar hardcode de una técnica.

---

# 36. Pendientes antes de implementar

1. Definir las prioridades/hook families y reglas de escala de las 20 Concordancias dirigidas.
2. Definir schema concreto de serialización en JS.
3. Cerrar la base numérica exacta de Reflect si existieran varias magnitudes candidatas.
4. Cerrar el límite numérico universal de Robo de Vida por acción.
5. Cerrar el piso numérico global de reducción de coste de Qi.
6. Cerrar el orden exacto entre reducción plana y reducción porcentual de coste de Qi.
7. Cerrar el techo/piso de estadísticas que siguen sujetas a benchmark cuando corresponda.
8. Auditar numéricamente las 12 técnicas tras cerrar Concordancias y economía de puntos.
9. Diseñar y auditar las 3 técnicas de Viento.

Los bloqueantes arquitectónicos detectados por la auditoría externa del 2026-09-28 se consideran resueltos por la sección 38.

---

# 37. Estado

**ARQUITECTURA APROBADA POR EL DISEÑADOR.**

No autoriza todavía implementación runtime. Las cifras marcadas como provisionales siguen sujetas a benchmark.

Este archivo propone la arquitectura universal sobre la que deberían apoyarse:

- estadísticas;
- técnicas;
- ramas;
- Concordancias;
- buffs/debuffs;
- DOT/aflicciones;
- Absorción;
- Control;
- curación;
- Robo de Vida;
- Qi;
- Reflect;
- Retaliation;
- daño aplazado;
- recursos internos;
- equipo;
- pasivas;
- NPC;
- jefes;
- contenido futuro.


---

# 38. Resoluciones post-auditoría — CERRADO 2026-09-28

Esta sección resuelve los bloqueantes y huecos arquitectónicos detectados en la auditoría externa posterior a v0.1. Cuando una cláusula anterior sea menos específica, esta sección prevalece.

## 38.1 Orden total de TURN_START

El comienzo del turno se divide en categorías deterministas:

```text
TURN_START
1. START_TURN_DEFENSIVE_RESTORE
2. START_TURN_AFFLICTION_TICKS
3. START_TURN_HP_REGENERATION
4. START_TURN_CONTROL_AND_OTHER_TICKS
5. START_TURN_ACTION_READY
```

Reglas:

- Reflujo y otras restauraciones de Absorción ocurren en `START_TURN_DEFENSIVE_RESTORE`.
- Quemadura, Veneno y otros DOT con tick de inicio ocurren en `START_TURN_AFFLICTION_TICKS`.
- Regeneración de Vida ocurre después de los DOT de inicio.
- Una aflicción puede matar antes de que el actor llegue a `START_TURN_ACTION_READY`.
- Una familia futura puede declarar otra fase sólo mediante extensión explícita del catálogo, no mediante una prioridad ad hoc.
- Dentro de la misma categoría se usa prioridad declarada y después un desempate estable por `effect_instance_id`.

## 38.2 Ciclo de vida del Eco elemental

Existe **un único slot de Eco por actor**.

```text
actor.echo_slot =
  null
  o
  {
    element,
    source_action_id,
    created_turn_id
  }
```

Reglas:

1. Un Eco nuevo sustituye al Eco anterior del mismo actor.
2. El Eco pertenece al actor que lo generó; no queda ligado al objetivo.
3. Sólo técnicas puras elegibles generan Eco.
4. Definitivas híbridas no generan, consumen ni reciben Ecos.
5. Al declarar una técnica pura receptora:
   - el resolver inspecciona el Eco existente;
   - busca una relación ORIGEN→DESTINO;
   - busca un hook compatible.
6. Si no existe hook compatible, la acción continúa y el Eco **no se consume por Concordancia**. Esto no impide que, al finalizar una ejecución válida, la propia técnica genere un Eco nuevo y sustituya el anterior conforme a las reglas 1 y 10.
7. Si existe hook compatible y la acción pasa validación/coste, el Eco queda comprometido y se consume al comenzar la ejecución.
8. Si posteriormente el impacto falla por Evasión, el Eco sigue gastado: la energía ya fue canalizada.
9. Una acción que consumió un Eco **no genera otro Eco al finalizar esa misma acción** por defecto.
10. Una técnica pura que no consumió Eco puede generar su propio Eco al completar una ejecución válida.
11. Para técnicas ofensivas, "ejecución válida" exige al menos un impacto conectado; para técnicas defensivas/utilitarias elegibles, basta una activación válida.
12. Una excepción futura capaz de encadenar consumo→generación deberá declararlo explícitamente como propiedad especial del contenido.
13. El Eco no se conserva indefinidamente fuera de combate: al terminar el combate se elimina salvo futura regla explícita.
14. Acciones no técnicas no crean ni consumen Eco. No borran el Eco por defecto bajo el contrato nuevo.

## 38.3 Capa AOE contra un único objetivo

Se crea la capa global:

```text
AOE_SINGLE_TARGET_SCALAR = 0.65
```

Se aplica **a la magnitud ofensiva de la ejecución antes de DEF y antes del redondeo final**.

Orden relevante:

```text
porciones
→ planos
→ pool porcentual ofensivo
→ crítico
→ modificadores de daño recibido
→ AOE_SINGLE_TARGET_SCALAR si hay 1 objetivo válido
→ sumar porciones
→ DEF/Penetración
→ redondeo
→ Absorción
→ Vida
```

Reglas:

- afecta el daño directo originado por la técnica AOE;
- afecta la potencia base de DOT/aflicción cuyo daño derive expresamente de la magnitud ofensiva de esa AOE;
- no reduce magnitud de debuffs estadísticos, Control, duración, stacks ni otros estados que no escalen con daño;
- no modifica el número de objetivos;
- el valor 0.65 sigue siendo provisional para benchmark, pero su **posición en el pipeline queda cerrada**.

## 38.4 Roles direccionales de eventos

Todo trigger puede declarar el papel del propietario del efecto:

```text
OWNER_AS_SOURCE
OWNER_AS_TARGET
OWNER_AS_EITHER
```

Condiciones universales mínimas:

```text
source_is_owner
target_is_owner
source_is_not_owner
target_is_not_owner
```

Los eventos canónicos incluyen además:

```text
ON_DAMAGE
ON_HIT_RECEIVED
ON_DAMAGE_RECEIVED
ON_HP_DAMAGE_RECEIVED
ON_VALID_DIRECT_IMPACT_RECEIVED
ON_ABSORPTION_RESTORE_RESOLVED
ON_ABSORPTION_LOSS_RESOLVED
ON_ACTION_ATTEMPT
ON_ACTION_COMPLETED
```

Los eventos `*_RECEIVED` son vistas direccionales del mismo evento causal; no duplican el evento ni permiten doble trigger automático.

Hemorragia puede escuchar `ON_ACTION_ATTEMPT` del afectado antes de ejecutar la acción voluntaria.

## 38.5 Unidades de duración

`duration_unit` debe ser una enumeración explícita:

```text
OWNER_TURNS
SOURCE_TURNS
GLOBAL_ROUNDS
UNTIL_OWNER_TURN_START
UNTIL_OWNER_TURN_END
UNTIL_SOURCE_TURN_START
UNTIL_ACTION_COMPLETED
UNTIL_NEXT_VALID_HIT
UNTIL_COMBAT_END
EVENT_COUNT
```

Reglas:

- "1 turno" no se interpreta por contexto; el contenido debe declarar la unidad.
- `once_per_turn` debe declarar `OWNER_TURN`, `SOURCE_TURN` o `GLOBAL_ROUND`.
- `once_per_activation` usa la identidad de la instancia activa del efecto.
- Los efectos aplicados durante el turno enemigo no expiran accidentalmente por una convención implícita.

## 38.6 Prevención de recursión

Flags son la defensa principal. `reaction_depth` es una salvaguarda adicional.

```text
max_reaction_depth = 8
```

Reglas:

- toda reacción que produzca otro evento reactivo incrementa `reaction_depth + 1`;
- al superar 8, la nueva reacción se cancela y se registra diagnóstico;
- un `DamagePacket` generado por `DEAL_DAMAGE` debe declarar explícitamente su `damage_source_type` y permisos;
- ausencia de un permiso se interpreta de forma conservadora como `false` para retriggers reactivos.

Defaults:

```text
DOT:
can_trigger_on_hit = false
can_trigger_on_damage = false
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false

REFLECT:
can_crit = false
can_use_def = true
can_use_absorption = true
can_trigger_on_hit = false
can_trigger_on_damage = false
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false

RETALIATION:
can_crit = false
can_use_def = true
can_use_absorption = true
can_trigger_on_hit = false
can_trigger_on_damage = false
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false

SECONDARY_REACTIVE:
todos los retriggers reactivos = false por defecto
```

Las excepciones futuras deben declararse explícitamente y superar validación de contenido.

## 38.7 Daño Aplazado y HP_COMMIT

Se introduce la ventana:

```text
HP_COMMIT
→ LIFE_DAMAGE_COMMITTED
→ DAMAGE_CONVERSION
   ├─ hp_loss_immediate
   └─ deferred_loss_created
→ HP_WRITE
→ FREEZE
```

Definiciones:

- `life_damage_committed`: daño real que atravesó DEF/Absorción y quedó comprometido contra Vida, limitado por la Vida disponible para evitar overkill artificial.
- `hp_loss_immediate`: pérdida de Vida aplicada ahora.
- `deferred_loss_created`: deuda creada.
- `actual_hp_damage`: pérdida inmediata real de Vida en esta escritura.

Semántica:

- `ON_HP_DAMAGE` usa `actual_hp_damage > 0`.
- Robo de Vida, cuando exista Aplazamiento, usa `life_damage_committed` elegible.
- Hemorragia normal que exige daño físico a Vida usa `life_damage_committed > 0`, porque la herida fue comprometida aunque parte se aplace.
- La deuda posterior no vuelve a generar Robo de Vida por el mismo daño.

## 38.8 Zonas, terreno y efectos con dueño no actor

`EffectDefinition.owner` puede ser:

```text
ACTOR
ROOM
POSITION
SUMMON
OBJECT
```

Se añaden:

```text
ZONE
ZONE_DURATION
ON_ZONE_TICK
ON_ENTER_ZONE
ON_LEAVE_ZONE
```

Una zona persistente, trampa, niebla, fuego ambiental o formación puede existir sin handler específico de técnica.

## 38.9 Persistencia de aflicciones

Una aflicción puede declarar:

```text
family
grade
persists_out_of_combat
persists_room_change
persists_save
out_of_combat_lethality
cure_tags[]
```

Defaults para aflicciones persistentes de Arco 1 cuando el contenido lo declare:

- pueden sobrevivir a fin de combate y cambio de sala;
- pueden persistir en guardado;
- la cura puede filtrar por familia/tipo y grado máximo;
- fuera de combate no reducen al personaje por debajo de 1 HP salvo regla excepcional explícita.

Las reglas nuevas de stacking de Hemorragia/Quemadura prevalecen sobre el comportamiento histórico de `ver74`; el runtime histórico es referencia, no contrato.

## 38.10 Qi: recuperación explícita vs regeneración pasiva

Se permite recuperar Qi mediante efectos explícitos de técnicas, ramas, estados, equipo o eventos.

Ejemplos válidos:

```text
ON_CRIT → RESTORE_QI(1)
ON_EFFECT_EXPIRE → RESTORE_QI(1)
ON_KILL → RESTORE_QI(X)
```

Continúa prohibido:

```text
TURN_START → RESTORE_QI(X)
```

cuando sea incondicional y permanente como regeneración automática general.

Regla:

> "No regeneración pasiva" significa que no existe una estadística o proceso universal automático de Qi por turno. No prohíbe recompensas explícitas condicionadas a una mecánica.

## 38.11 Múltiples pools de Absorción

Se permiten múltiples pools.

Cada uno declara:

```text
priority
created_order
```

Resolución:

1. mayor prioridad primero;
2. a igual prioridad, pool más antiguo primero.

Restaurar un pool no cambia su orden de creación.

Una reconstrucción después de llegar a 0 crea un pool nuevo con el mismo `absorption_pool_id` lógico y una nueva instancia/orden de creación.

## 38.12 Concordancias persistentes: snapshot

Cuando una Concordancia modifica un estado persistente:

- la resolución de Concordancia ocurre al crear/activar el estado;
- sus parámetros quedan **snapshot** en esa instancia;
- no se vuelve a consultar el Eco ni las estadísticas de la Concordancia en cada tick/trigger;
- reactivar/reemplazar el estado crea un nuevo snapshot.

## 38.13 Concordancias globales y magnitudes

La identidad y canal pertenecen a la relación global `ORIGEN→DESTINO`.

La técnica receptora declara:

- hooks disponibles;
- magnitud base de la propiedad;
- restricciones específicas de contenido.

No debe existir una definición arbitraria y completamente distinta de la misma relación en cada técnica.

La tabla global futura de las 20 relaciones debe declarar:

```text
relation_id
identity
role/context priorities
compatible_hook_families
transformation_rule / scale_rule
```

La técnica sólo aporta el hook y los datos sobre los que operar.

## 38.14 Condiciones de build/contenido

Se añaden condiciones de sólo lectura:

```text
has_branch(option_id)
has_all_branches([...])
action_has_hook(hook)
action_applies_effect(effect_family)
action_generates_resource(resource_family)
target_has_effect(effect_family)
resource_stacks(resource_family)
```

Estas condiciones viven en configuración de contenido; su existencia no autoriza hardcodear IDs en el resolver.

## 38.15 Combatiente hostil válido

Para AOE y selección automática:

```text
VALID_HOSTILE_COMBATANT
=
entidad viva
+ atacable
+ hostil al actor
+ presente en el espacio de combate
+ no excluida explícitamente por reglas de la acción
```

"NPC hostil" en documentos anteriores debe leerse como `VALID_HOSTILE_COMBATANT`.

NPC sociales no entran en una AOE sólo por compartir sala.

## 38.16 Orden determinista de objetivos AOE

Los objetivos AOE se congelan al iniciar la resolución de blancos.

Orden estable:

1. orden de incorporación al contexto de combate;
2. desempate por ID estable de entidad.

Cada objetivo conserva su propio `impact_id`.

La muerte o reacción de un objetivo no reordena los impactos restantes de esa acción.

## 38.17 Disciplina RNG

Cada impacto consume sorteos en orden fijo cuando corresponda:

```text
1. HIT
2. CRIT
3. controles/estados disparados por ese impacto en prioridad estable
```

Un sorteo que no corresponde no se consume.

El RNG debe ser sembrable/reproducible para diagnóstico.

## 38.18 Acción preparada/anunciada

`ActionContext` puede declarar:

```text
prepared_action_id
prepare_state
prepare_source
intended_targets
execution_window
cancellable
```

Estados mínimos:

```text
DECLARED
PREPARED
EXECUTING
RESOLVED
CANCELLED
```

`CANCEL_PREPARED_ACTION` sólo actúa sobre una acción `PREPARED` y `cancellable=true`.

## 38.19 Injerto espiritual

El injerto permanente **no puede compartir elemento con la raíz principal**.

Su propósito es aportar una segunda afinidad real; no duplicar el mismo paquete de rasgos.

## 38.20 Calor de Cuerpo-Horno

El Calor consumido por una técnica ofensiva de Fuego genera una porción secundaria con:

```text
damage_source_type = DIRECT
tags = [TECHNIQUE, DIRECT, ELEMENTAL, FIRE, STORED_RESOURCE]
amount = recurso consumido ya fijado
can_crit = false
can_use_def = true
can_use_penetration = false
can_use_absorption = true
can_trigger_lifesteal = false
```

La cantidad almacenada **no vuelve a recibir pools ofensivos** al liberarse. Esto evita doble escalado.

## 38.21 Robo de Vida y anti-curación

Los modificadores normales de curación realizada/recibida no modifican Robo de Vida.

Un efecto de anti-curación sólo afecta Robo de Vida si declara explícitamente:

```text
affects_lifesteal = true
```

El límite numérico por acción continúa pendiente de benchmark.

## 38.22 Cobertura de Concordancias

La cobertura mínima se mide por **relación elemental habilitada en una etapa**, no por cada rol posible.

Si una relación tiene al menos un receptor real y compatible en la etapa puede existir.

Una técnica concreta que no expone ningún hook compatible:

- no recibe transformación;
- no consume Eco.

No es obligatorio que cada relación tenga simultáneamente receptor ofensivo, defensivo, Control y utilidad.


## 38.23 Previsualización de Concordancia y coste de Qi

Para cualquier Concordancia capaz de modificar el coste de la acción se introduce una fase de **previsualización sin consumo**:

```text
DECLARE_ACTION
→ CONCORDANCE_PREVIEW
→ CALCULATE_FINAL_COST
→ VALIDATE_COST
→ PAY_COST
→ COMMIT_CONCORDANCE
→ EXECUTING
```

Reglas:

- `CONCORDANCE_PREVIEW` puede leer el Eco y resolver qué transformación sería aplicable;
- esta fase no consume ni sustituye el Eco;
- sólo las propiedades declaradas como `PRE_COST` pueden modificar el coste;
- si la acción no supera validación o pago, el Eco permanece sin consumir;
- si la acción supera validación y existe una Concordancia válida, el Eco se compromete y se consume al comenzar `EXECUTING`;
- las Concordancias que no afectan coste pueden resolverse en preview pero sus cambios no se materializan hasta el compromiso;
- `QI_COST_PERCENT` de Concordancia se aplica como capa local de esa ejecución y no como modificación permanente del pool global del actor.

Forma conceptual:

```text
coste_tras_modificadores_normales
× (1 - concordance_cost_scale)
→ piso_global_de_coste
→ redondeo_final
```

El porcentaje exacto queda pendiente de benchmark.


## 38.24 Schema universal de manifestación estructural

Una Concordancia STRUCTURAL o PARAMETRIC compleja no se implementa mediante condiciones por ID de técnica.

Debe producir un descriptor de datos:

```text
ConcordanceManifestation {
  manifestation_id
  relation_id
  receiver_hook
  hook_class
  activation_context
  owner
  source
  target_scope
  duration_value
  duration_unit
  trigger
  conditions[]
  frequency
  scale_rule
  scale_target
  transformation_rule
  consume_rule
  operations[]
  packet_flags
  cleanup_rule
  snapshot_fields[]
}
```

Reglas:

1. `manifestation_id` identifica contenido, no autoriza un `if manifestation_id` en el resolver.
2. `relation_id` identifica la relación ORIGEN→DESTINO.
3. `receiver_hook` debe estar presente en `concordance_hooks[]` de la técnica/estado receptor.
4. `hook_class` usa `SCALAR | PARAMETRIC | STRUCTURAL`.
5. `target_scope` nunca puede ampliar silenciosamente el conjunto congelado de blancos de una ejecución.
6. Toda duración temporal debe declarar `duration_value + duration_unit`.
7. Toda operación que produzca DamagePacket debe declarar flags explícitos.
8. `snapshot_fields[]` declara qué valores quedan congelados al crear la instancia.
9. `cleanup_rule` define expiración, consumo, ruptura o fin de combate.
10. La transformación se selecciona por relación + hook + contexto, no por nombre de técnica.

Manifestaciones iniciales:

```text
Tierra→Fuego + CONTAINED_TRIGGER → NUCLEO_DE_MAGMA
Tierra→Metal + FORTIFICATION   → PLACA_FUNDACIONAL
Tierra→Agua + ABSORPTION_RESTORE/INTERNAL_RESOURCE → EMBALSE
Tierra→Viento + ZONE/ZONE_DURATION → NUBE_RESIDUAL
```

Los detalles específicos viven en datos de contenido compatibles con este schema.

## 38.25 Descriptor de Concordancia por ejecución AOE

Una Concordancia se resuelve **una vez por ActionContext**, no una vez por objetivo, salvo que la transformación declarada produzca efectos por objetivo.

Flujo:

```text
ActionContext
→ resolver Concordancia una vez
→ crear ConcordanceDescriptor
→ congelar target_set
→ resolver impactos por objetivo
→ aplicar el descriptor según scope
```

Reglas:

- un único Eco no puede producir varias resoluciones primarias por tener múltiples objetivos;
- `PROPAGATION`, `AREA_EFFICIENCY`, zonas y paquetes secundarios no descubren nuevos enemigos fuera de `target_set`;
- un descriptor puede declarar `per_target` para aplicar la misma transformación a cada objetivo ya válido;
- un descriptor puede declarar `marked_target_only` para una manifestación individual;
- paquetes secundarios que reutilicen `target_set` conservan el orden determinista;
- el `AOE_SINGLE_TARGET_SCALAR` sólo se aplica a paquetes que declaren explícitamente pertenecer a la magnitud ofensiva de la AOE. Un paquete secundario independiente debe declarar su propia relación con esa capa.

## 38.26 Roles funcionales y composición elemental

`role_primary` sólo puede ser:

```text
OFFENSIVE
DEFENSIVE
CONTROL
UTILITY
```

Una técnica puede tener capacidades secundarias, pero debe elegir un único rol primario para seleccionar la tabla de prioridades de Concordancia.

`HYBRID` no es un rol funcional. Describe composición elemental.

Las Definitivas híbridas continúan fuera del sistema de Ecos/Concordancias por regla propia, no por `role_primary`.

## 38.27 Eco del mismo elemento

La diagonal elemental no tiene Concordancia:

```text
FUEGO→FUEGO
METAL→METAL
AGUA→AGUA
TIERRA→TIERRA
VIENTO→VIENTO
= NONE
```

Si una técnica pura del mismo elemento encuentra un Eco previo:

- no existe resolución de Concordancia;
- el Eco previo no se consume;
- si la técnica completa una ejecución válida y genera un Eco nuevo, éste sustituye al anterior conforme a §38.2.


## 38.28 Resultados de restauración y pérdida de Absorción

Toda operación `RESTORE_ABSORPTION` produce un resultado congelado:

```text
AbsorptionRestoreResult {
  absorption_pool_id
  pool_instance_id
  requested_restore
  actual_restore
  overflow_restore
  reserve_before
  reserve_after
  reserve_max
}
```

donde:

```text
overflow_restore
=
max(0, requested_restore - actual_restore)
```

Después de escribir el nuevo valor del pool se emite:

```text
ON_ABSORPTION_RESTORE_RESOLVED
```

Cuando un DamagePacket u otra operación reduce una reserva, después de resolver esa reducción para el paquete actual se emite:

```text
ON_ABSORPTION_LOSS_RESOLVED
```

con al menos:

```text
absorption_pool_id
pool_instance_id
loss_amount
reserve_before
reserve_after
reserve_max
root_action_id
```

Una reacción a `ON_ABSORPTION_LOSS_RESOLVED` puede restaurar reserva para **paquetes futuros**, pero nunca vuelve atrás para absorber daño del paquete que ya produjo el evento.

Esto permite recursos como Embalse sin crear una segunda barrera ni reabrir el DamagePacket actual.
