# Contrato del motor universal de eventos, efectos y Concordancias — v0.1

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CONTRATO ARQUITECTÓNICO / NO IMPLEMENTAR TODAVÍA SIN AUTORIZACIÓN EXPLÍCITA**

## 0. Propósito

Este documento define la arquitectura que debe permitir que técnicas, ramas, estados, aflicciones, equipo, NPC, jefes, Concordancias y sistemas futuros puedan expresarse **sin añadir excepciones al núcleo de combate técnica por técnica**.

Objetivo de aceptación:

> Una mecánica nueva correctamente soportada por el contrato debe poder añadirse principalmente como datos/configuración de efectos y no obligar a modificar el resolver central de combate.

El contrato no reemplaza las fórmulas ya cerradas en `CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md`. Las organiza dentro de un motor genérico.

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
MOBILITY_REDUCTION
EVASION_DEBUFF
PRECISION_DEBUFF
ACTION_DENIAL
INTERRUPT
STAT_DEBUFF
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
DEFERRED_DAMAGE
IMMUNITY_WINDOW
CONTROL_LOCKOUT
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
ROOT
INTERRUPT
SILENCE
DISARM
FEAR
FORCED_TARGET
MOVEMENT_DENIAL
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
can_trigger_normal_on_hit = false
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
consultar rol + hooks reales de receptora
↓
encontrar canal compatible según prioridad
↓
producir modificador/transformation descriptor
↓
si hubo resolución válida: consumir Eco
↓
si no hubo propiedad compatible: conservar Eco
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
1. STRUCTURAL_MAGNITUDE
2. IMPACT
3. compatible rupture property

DEFENSIVE:
1. DEF_GRANTED
2. ABSORPTION
3. FORTIFICATION
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
MODIFY_STAT
ON_HIT_RECEIVED
CHECK_EFFECT
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

# 36. Pendientes de cierre antes de implementar

1. Definir las prioridades/hook families de las 20 Concordancias dirigidas.
2. Definir schema concreto de serialización en JS.
3. Cerrar orden TURN_START entre DOT, regeneración y otros ticks.
4. Cerrar base exacta de Reflect si existieran varias magnitudes candidatas.
5. Cerrar límite numérico universal de Robo de Vida por acción.
6. Cerrar piso de reducción de coste de Qi.
7. Definir política de múltiples pools de Absorción si se permiten.
8. Definir `max_reaction_depth` de seguridad.
9. Auditar las 12 técnicas ya diseñadas contra este contrato.
10. Auditar estadísticas y fórmulas actuales para verificar que cada una tiene una única capa de resolución.

---

# 37. Estado

**APROBACIÓN PENDIENTE DEL USUARIO.**

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
