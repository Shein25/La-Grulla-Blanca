# Contrato de combate y aflicciones — checkpoint v0.2

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Base: `snapshot/handoff-2026-09-27-astra-a04`

## Propósito

Checkpoint documental del rediseño del combate de Arco 1. Este archivo **no implementa todavía cambios en el runtime**: congela decisiones de diseño ya cerradas para evitar pérdidas de estado entre iteraciones y para que la implementación posterior no tenga ambigüedades.

## Restricciones de repositorio

- No tocar `main`.
- No modificar `implement/3c5-npc-ver74`; esa rama sigue reservada para NPC 3C.5.
- No hacer merge automático.
- No modificar `ROOMS.exits`.
- No modificar `GATES_329`.
- No migrar valores antiguos de DEF/ATQ directamente al modelo nuevo.
- El equipo viejo queda pendiente de recreación luego del cierre del contrato de estadísticas.

---

# 1. Jerarquía de combate

```text
ACCIÓN
 └─ 1..N IMPACTOS
     └─ 1..N PORCIONES / COMPONENTES DE DAÑO
```

En Arco 1, una acción usa normalmente un solo impacto. El multigolpe queda preparado arquitectónicamente para arcos futuros.

Una porción conserva etiquetas de **tipo** y **origen**, por ejemplo:

```text
4 físico [DIRECTO][TÉCNICA][FÍSICO]
4 físico [DIRECTO][TÉCNICA][ARMA][FÍSICO]
6 fuego  [DIRECTO][TÉCNICA][FUEGO][ELEMENTAL]
```

Un impacto híbrido sigue siendo un solo impacto para Precisión, Crítico, DEF y Absorción.

---

# 2. Estadísticas nucleares

- Vida / Vida máxima
- Qi / Qi máximo
- Ataque como paraguas de modificadores de daño, no como precisión
- Precisión
- Evasión
- Defensa
- Penetración de armadura
- Probabilidad crítica
- Daño crítico
- Control
- Tenacidad
- Absorción
- Subsistema de aflicciones/DOT

Sistemas como comprensión, impurezas, heridas meridianas, cultivo, contribución, profesiones y maestrías no son estadísticas nucleares de combate.

---

# 3. Precisión y Evasión

```text
Precisión efectiva =
Precisión del personaje
+ modificador de la acción
+ buffs
- debuffs

Probabilidad de impacto =
clamp(Precisión efectiva - Evasión objetivo, 5, 100)
```

- Precisión normal de referencia: 100.
- Puede superar 100 internamente para contrarrestar Evasión.
- Evasión evita por completo un impacto.
- Un impacto evadido no hace daño ni consume Absorción.
- Los ticks de DOT ya aplicados no vuelven a tirar Precisión.
- `evadible:false` será una excepción explícita.
- Crítico no concede impacto automático.

---

# 4. Modificadores ofensivos

Cada porción de daño recibe los modificadores compatibles con sus etiquetas.

## 4.1 Bonos planos

Los bonos planos se aplican una sola vez y sólo a la porción compatible.

Ejemplos:
- +3 físico → sólo porciones [FÍSICO].
- +3 fuego → sólo porciones [FUEGO].
- +3 global plano → una sola aportación al impacto; nunca se duplica por tener varias porciones.

Los bonos planos aplicables se incorporan antes de los porcentajes.

## 4.2 Bonos porcentuales

Los porcentajes ofensivos compatibles con una misma porción **se suman entre sí**.

```text
Daño modificado =
daño base modificado
× (1 + suma de porcentajes aplicables)
```

Ejemplos de etiquetas compatibles:
- GLOBAL
- DIRECTO
- TÉCNICA
- ATAQUE_COMÚN
- ARMA
- FÍSICO
- ELEMENTAL
- FUEGO / AGUA / METAL / TIERRA / VIENTO

No se multiplican entre sí los bonos normales de +X%.

Una porción [TÉCNICA][ARMA][FÍSICO] puede recibir simultáneamente bonos de global, técnica, arma y físico.

El bono de arma sólo afecta la porción procedente realmente del arma. El bono de técnica puede afectar también esa porción si el arma participa dentro de una técnica.

El multiplicador ofensivo nunca baja de 0.

---

# 5. Crítico

Base conceptual:

```text
Probabilidad crítica base: 5%
Daño crítico base: x1.50
```

Los bonos de daño crítico se suman al multiplicador:
```text
x1.50 + 20% = x1.70
```

- Un crítico se tira por impacto.
- Todos los componentes de un impacto híbrido comparten el mismo resultado crítico.
- Crítico se resuelve después de los modificadores ofensivos y antes de DEF.
- Crítico es una capa multiplicativa separada de los +X% normales.
- DOT no critica por defecto.
- Ramas específicas podrán permitir crítico de DOT.
- Si un DOT puede criticar, sus ticks tiran crítico independientemente.
- El crítico del golpe inicial no vuelve automáticamente crítico al DOT ni aumenta su potencia.

---

# 6. Modificadores de daño recibido

Los modificadores del objetivo se calculan por porción antes de sumar el impacto.

Ejemplo:
```text
10 físico + 10 fuego
objetivo: +20% daño de Fuego recibido

→ 10 físico + 12 fuego
→ total 22
```

Los porcentajes compatibles de daño recibido también se suman entre sí, en lugar de multiplicarse.

Esta capa es distinta de los modificadores ofensivos del atacante.

---

# 7. Defensa

DEF es reducción plana universal de daño directo.

Después de terminar las porciones y modificadores de daño recibido:

```text
sumar porciones del impacto
→ DEF efectiva
→ Absorción
→ Vida
```

- Puede reducir daño directo hasta 0.
- Se aplica una vez por impacto.
- Un impacto híbrido aplica DEF una sola vez sobre el total.
- DOT ignora DEF.
- En futuro multigolpe, DEF se aplica a cada impacto por separado.

---

# 8. Penetración de armadura

Universal para todo daño directo.

Orden:

```text
DEF real del objetivo
→ reducción/shred de DEF
→ penetración porcentual
→ penetración plana
→ DEF efectiva, mínimo 0
```

- No afecta DOT.
- No afecta Absorción.
- La reducción de DEF cambia la DEF real del objetivo para todos.
- La penetración pertenece al atacante y sólo modifica su cálculo.

---

# 9. Absorción

Absorción es una reserva protectora temporal.

Datos básicos:
```text
reserva
duración
```

Flujo directo:
```text
daño directo
→ DEF
→ Absorción
→ Vida
```

Flujo DOT:
```text
DOT
→ Absorción
→ Vida
```

La Absorción desaparece únicamente por:
1. reserva agotada;
2. duración expirada.

El daño no reduce duración y el paso del tiempo no reduce reserva.

Excepción futura:
```text
ignora_absorcion:true
```

Ese daño salta la burbuja sin consumirla ni destruirla.

---

# 10. Resultado de impacto y eventos

Cada impacto debe producir un resultado estable:

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

Donde:
- `hp_damage` = daño que habría llegado a Vida tras Absorción.
- `actual_hp_damage` = daño realmente perdido por el objetivo, limitado por la Vida que tenía antes del golpe; no cuenta overkill.

Eventos directos:

```text
ON_HIT
impacto directo conectado.

ON_DAMAGE
impacto directo conectado
y damage_after_def > 0.

ON_HP_DAMAGE
impacto directo conectado
y actual_hp_damage > 0.

ON_CRIT
impacto directo conectado
y resultado crítico.
```

Los triggers pueden combinarse.

Los efectos disparados por un impacto se resuelven a partir del resultado ya cerrado y **no modifican retroactivamente ese mismo impacto**.

DOT, Reflect y Retaliation no generan los eventos normales de impacto directo; tendrán eventos propios para evitar recursiones.

En multigolpe futuro, los eventos se evalúan por impacto. Los efectos podrán declarar `once_per_impact` o `once_per_action`.

---

# 11. Pipeline universal de daño directo

```text
VALIDAR ACCIÓN
↓
PAGAR COSTES
↓
PRECISIÓN vs EVASIÓN
↓
CONSTRUIR PORCIONES DE DAÑO
↓
APLICAR BONOS PLANOS A SU PORCIÓN
↓
SUMAR % OFENSIVOS APLICABLES
↓
ESCALAR CADA PORCIÓN
↓
CRÍTICO DEL IMPACTO
↓
MODIFICADORES DE DAÑO RECIBIDO POR PORCIÓN
↓
SUMAR TODAS LAS PORCIONES
↓
DEF ACTUAL
↓
PENETRACIÓN %
↓
PENETRACIÓN PLANA
↓
RESTAR DEF UNA SOLA VEZ
↓
ABSORCIÓN
↓
VIDA
↓
CONGELAR RESULTADO DEL IMPACTO
↓
DISPARAR EFECTOS POSTERIORES
```

---

# 12. Control y Tenacidad

```text
Control ↔ Tenacidad
```

```text
Control efectivo =
potencia base del efecto
+ Control del personaje
+ buffs
- debuffs

Probabilidad de control =
clamp(Control efectivo - Tenacidad, 5, 100)
```

- Tenacidad es resistencia universal a estados de control.
- No reduce duración: sólo modifica probabilidad de aplicación.
- Debuffs estadísticos normales no son Control.
- Crítico y Penetración no afectan Control.
- `inmune_control:true` y `control_garantizado:true` son excepciones explícitas.
- El anti-chain fuerte y la inmunidad temporal de jefes quedan como capa posterior de balance.

---

# 13. Robo de Vida — CERRADO

Robo de Vida será **universal respecto del origen/tipo del daño directo**.

No se discrimina entre:
- físico;
- elemental;
- arma;
- técnica;
- ataque común;
- impacto híbrido.

Si el daño directo llegó realmente a la Vida del objetivo, es elegible.

Base:

```text
VIDA_ROBADA_POTENCIAL =
actual_hp_damage
× porcentaje_robo_de_vida
```

Reglas:
- Trigger conceptual: `ON_HP_DAMAGE`.
- Usa `actual_hp_damage`, por lo que no cuenta overkill.
- DEF reduce indirectamente el robo porque reduce daño a Vida.
- Absorción reduce indirectamente el robo porque impide daño a Vida.
- El crítico puede aumentar el robo únicamente porque aumenta el daño; la recuperación no critica.
- Los modificadores normales de curación no aumentan Robo de Vida.
- Sobrecuración se pierde.
- No almacena recuperación sobrante.
- Todos los impactos de una acción aportan a una reserva potencial y el límite se aplica al total de la acción.
- En AOE se suman los aportes válidos de todos los objetivos, sujetos al mismo límite por acción.
- El valor exacto del límite por acción se balanceará posteriormente; la semántica del sistema queda cerrada.

Por defecto NO son elegibles:
- DOT;
- Reflect;
- Retaliation;
- daño reactivo/secundario.

Una técnica futura puede romper esta regla explícitamente, pero eso será una propiedad especial y no el Robo de Vida universal normal.

Sistemas distintos:
```text
VIDA AL IMPACTAR ≠ ROBO DE VIDA
VIDA AL MATAR    ≠ ROBO DE VIDA
```

Vida al impactar es una recuperación plana por evento válido.
Vida al matar depende de `ON_KILL`.
Ninguna de las dos escala por el porcentaje universal de Robo de Vida.

---

# 14. Daño Aplazado — RESERVADO / post Arco 1

Mecánica futura de suavizado temporal del daño. **No forma parte del balance activo de Arco 1**, pero queda reconocida por el contrato para no perderla ni confundirla posteriormente con un DOT.

## Identidad

Aplazamiento no reduce necesariamente el daño total: cambia **cuándo** se pierde la Vida.

```text
daño directo
→ DEF
→ Absorción
→ daño comprometido a Vida
→ Aplazamiento
   ├─ pérdida inmediata
   └─ deuda futura
```

## Reglas reservadas

- Sólo actúa sobre daño que ya atravesó DEF y Absorción.
- No es DOT.
- No vuelve a tirar Precisión/Evasión.
- No vuelve a aplicar Crítico.
- La deuda no vuelve a pasar por DEF.
- La deuda no vuelve a pasar por Penetración.
- La deuda no vuelve a pasar por Absorción.
- La deuda no recibe modificadores de daño DOT.
- Puede matar por defecto.
- La deuda se cobra en pagos futuros, preferentemente al final de turnos para conservar una ventana real de reacción.
- Cada aplicación crea un paquete independiente; recibir daño nuevo no prolonga indefinidamente deuda antigua.
- Técnicas, ramas o equipo futuros podrán purgar, reducir, convertir o manipular deuda explícitamente.

## Variables futuras sugeridas

Cuando se implemente Aplazamiento, el resultado de impacto deberá distinguir:

```text
life_damage_committed
hp_loss_immediate
deferred_loss_created
```

cumpliendo:

```text
life_damage_committed =
hp_loss_immediate + deferred_loss_created
```

El Aplazamiento no se considera mitigación adicional: sólo modifica el calendario de pérdida de Vida.

## Interacción futura con Robo de Vida

Si se implementa, Robo de Vida deberá usar el daño real comprometido por el golpe antes de dividirlo entre pérdida inmediata y deuda aplazada, sin contar overkill. El objetivo es que aplazar daño no reduzca artificialmente el daño que realmente consiguió atravesar DEF y Absorción.

## Estado

**RESERVADO. No implementar ni balancear todavía en Arco 1.**


# 15. Reflect / Retaliation — post Arco 1

Preparados arquitectónicamente pero no activos en Arco 1.

- Reflect = porcentaje del daño directo recibido.
- Retaliation = valor plano por impacto directo recibido.
- DOT no los dispara.
- Evasión impide el trigger.
- Absorción no impide el trigger si existió impacto válido.
- Nunca generan recursión entre sí.

---

# 16. DOT / aflicciones — reglas universales cerradas

Las familias DOT comparten:
- ignoran DEF;
- no usan Penetración;
- pasan por Absorción;
- no vuelven a tirar Precisión después de aplicarse;
- no critican por defecto;
- pueden tener reglas propias de acumulación;
- las interacciones avanzadas deben venir de ramas/efectos explícitos.

El motor debe permitir familias con:
- potencia;
- duración expresada según la semántica propia;
- cargas;
- máximo de cargas;
- fuente;
- etiquetas;
- posible elemento;
- capacidad crítica opcional;
- capacidad de ignorar Absorción opcional.

No todos los estados persistentes deben comportarse igual.

---

# 17. HEMORRAGIA — contrato base CERRADO

## Naturaleza
Aflicción física persistente producida por determinadas acciones cortantes.

## Aplicación

Sólo una acción que lo declare explícitamente puede aplicar Hemorragia. Llevar una espada no basta.

La Hemorragia física normal requiere:

```text
ON_HP_DAMAGE
```

Es decir, una Absorción que detuvo por completo el golpe también impide abrir la herida física.

Orden:
```text
1. Precisión vs Evasión
2. Impacto válido
3. Resolver daño directo
4. Comprobar ON_HP_DAMAGE
5. Aplicar Hemorragia
```

Una técnica futura puede usar otro trigger explícito, pero será una excepción declarada.

## Estructura de cada carga

```text
potencia
activaciones_restantes
fuente
```

Las cargas son independientes.

La UI puede agregarlas:
```text
HEMORRAGIA ×3
Daño al actuar: 7
```

## Activación

Se activa cuando el afectado realiza una **acción voluntaria de combate**.

Activa con:
- ataque;
- técnica;
- defender;
- uso voluntario de objeto en combate.

No activa con:
- perder turno por Control;
- incapacidad;
- ausencia de acción.

## Momento

```text
decide actuar
→ Hemorragia
→ Absorción
→ Vida
→ si sigue vivo, ejecuta la acción
```

Puede matar al objetivo antes de que complete su acción.

## Mitigación

```text
Hemorragia
→ ignora DEF
→ no usa Penetración
→ Absorción
→ Vida
```

## Crítico

- No critica por defecto.
- El crítico del golpe inicial no modifica automáticamente potencia o duración.
- Cualquier interacción con crítico debe venir de una rama o efecto explícito.

## Escalado

```text
Potencia =
(base propia
 + bono plano DOT
 + bono plano Hemorragia)

×
(1
 + % daño global aplicable
 + % DOT
 + % físico
 + % Hemorragia)
```

No afectan automáticamente:
- daño de ataque común;
- daño de arma;
- daño directo;
- Penetración.

## Acumulación

- Cargas independientes.
- Máximo bajo y legible.
- Parámetro inicial de laboratorio: **4 cargas**.
- Al superar el máximo, la nueva carga reemplaza la más antigua.

## Duración

Se expresa como:
```text
activaciones_restantes
```

Cada acción voluntaria:
- activa el daño;
- reduce `activaciones_restantes` en 1.

Si el objetivo no actúa por Control, no hace daño ni consume duración.

## Fuera del núcleo base

Hemorragia NO concede por sí misma:
- vulnerabilidad a cortante;
- detonación;
- consumo de cargas;
- reducción de DEF;
- cargas extra por crítico;
- crítico propio;
- máximo adicional;
- extensión;
- recuperación de Qi;
- propagación.

Todo eso pertenece a ramas, nodos, técnicas, equipo o efectos explícitos.

---

# 18. Quemadura — candidato avanzado, aún no congelado

Dirección actual:
- DOT elemental de Fuego;
- aplicación sólo por acciones que lo declaren;
- tick automático al comienzo del turno del afectado;
- cargas independientes;
- máximo base a testear: 3;
- al superar máximo, reemplaza la más antigua;
- potencia propia;
- ignora DEF y pasa por Absorción;
- no critica por defecto;
- detonación, propagación, extensión y vulnerabilidad al Fuego no pertenecen al núcleo base.

---

# 19. Veneno — pendiente

Dirección actual:
- más stacks;
- desgaste sostenido;
- duración mayor;
- debe diferenciarse de Quemadura;
- posible especialización futura en mantenimiento, anti-curación o acumulación.

---

# 20. Orden posterior al impacto — CERRADO

Una vez congelado `IMPACT_RESULT`, el daño principal no puede modificarse retroactivamente.

Orden:

```text
CONGELAR IMPACT_RESULT
↓
GENERAR FLAGS
  ON_HIT
  ON_DAMAGE
  ON_HP_DAMAGE
  ON_CRIT
  LETHAL_HIT
↓
EFECTOS SOBRE LA FUENTE
  Robo de Vida / Qi / buffs / recursos
↓
SI EL OBJETIVO SOBREVIVE
  DOT / debuffs / Control / estados persistentes
↓
REACCIONES DEL OBJETIVO
  Reflect / Retaliation / contraefectos futuros
↓
RESOLVER MUERTE
↓
ON_DEATH
↓
ON_KILL
```

Reglas:
- Un golpe letal puede generar recuperación de la fuente y reacciones provocadas por ese mismo impacto.
- No se aplican nuevos estados persistentes normales a un objetivo ya muerto por el daño principal.
- `ON_DEATH` pertenece al objetivo muerto.
- `ON_KILL` pertenece a la fuente responsable.
- DOT puede causar muerte y debe conservar la fuente para atribuir `ON_KILL`.
- Debe conservarse metadata `kill_source` con actor, acción/familia de daño y etiquetas relevantes.
- Vida al matar usa `ON_KILL` y es independiente de Robo de Vida.

---

# 21. Buffs / Debuffs / stacking — CERRADO

## Principio general

Los buffs y debuffs normales deben usar pocas reglas universales. Las excepciones de acumulación se declaran explícitamente en los datos del efecto.

Cada efecto debe poder declarar:
- `effect_id`
- `stack_group` (por defecto igual a `effect_id`)
- fuente
- polaridad (buff/debuff)
- duración
- modo de stacking
- modificadores
- máximo de stacks cuando corresponda

## Duración

Por defecto, la duración se mide en turnos completos de la entidad afectada.

- El turno en el que se aplica el efecto no consume inmediatamente una unidad de duración.
- El efecto permanece activo durante los siguientes N turnos de su propietario.
- La duración se reduce al final de esos turnos.
- Reaplicar/refrescar nunca debe acortar una duración ya superior.
- Extender duración es una operación distinta de refrescar.

## Modos de stacking

### UNIQUE_REFRESH — modo por defecto

Un `stack_group` normal mantiene una sola instancia.

- Reaplicación equivalente: refresca duración.
- Reaplicación más fuerte: reemplaza la magnitud y usa su duración.
- Reaplicación más débil: no reemplaza ni refresca por defecto.
- Si distintos `effect_id` comparten `stack_group`, el diseñador debe declarar prioridad/potencia explícita; el motor no intenta inferir qué efecto multidimensional es “más fuerte”.

### STACK_REFRESH — acumulación explícita

Para efectos diseñados para acumular intensidad:
- cada aplicación añade 1 stack hasta `max_stacks`;
- todos los stacks comparten una sola duración;
- reaplicar refresca la duración;
- al máximo, una nueva aplicación no añade stacks pero sí refresca;
- la magnitud total normalmente es `valor_por_stack × stacks`.

Ejemplo:
```text
ARMOR_SHRED
-2 DEF por stack
max_stacks = 3
duración = 2 turnos
```

Resultado máximo:
```text
-6 DEF
```

### INDEPENDENT — excepcional

Instancias separadas con magnitud/duración propia. Reservado para DOT/aflicciones u otros sistemas que realmente lo necesiten; no es el modo normal de buffs/debuffs estadísticos.

## Combinación entre efectos distintos

Efectos de grupos diferentes pueden coexistir.

Todos los modificadores planos de una misma estadística se suman en su capa.
Todos los porcentajes normales de una misma estadística se suman en su capa.

Los efectos positivos y negativos se compensan algebraicamente.

## DEF actual del objetivo

Candidato de fórmula:

```text
DEF_actual =
max(
  0,
  (DEF_base + suma_modificadores_planos_DEF)
  × max(0, 1 + suma_modificadores_porcentuales_DEF)
)
```

Los debuffs de reducción de DEF forman parte de esta DEF real del objetivo y afectan a todos los atacantes.

Después, para un atacante concreto:

```text
DEF_efectiva =
max(
  0,
  DEF_actual × (1 - penetración_porcentual)
  - penetración_plana
)
```

Orden:
```text
DEF base
→ buffs/debuffs planos
→ buffs/debuffs porcentuales
→ DEF actual
→ penetración %
→ penetración plana
→ DEF efectiva
```

La DEF nunca es negativa.

## Relación con triggers

La técnica/equipo decide cuándo se aplica un buff/debuff:
- ON_HIT
- ON_DAMAGE
- ON_HP_DAMAGE
- ON_CRIT
- ON_KILL
- u otro evento explícito.

Un debuff aplicado por un impacto afecta sólo cálculos futuros; no recalcula el impacto que lo generó.

## Tenacidad

Los debuffs estadísticos ordinarios no son Control y Tenacidad no reduce automáticamente su duración ni su magnitud. Si un efecto necesita probabilidad de aplicación propia, debe declararla explícitamente.

---

# 22. Daño elemental — CERRADO

## Principio

Los elementos son **etiquetas ofensivas y de interacción**, no una segunda familia defensiva.

No existen como estadísticas base:
- Resistencia Fuego;
- Resistencia Agua;
- Resistencia Metal;
- Resistencia Tierra;
- Resistencia Viento;
- ni buffs genéricos de resistencia para cada elemento.

La defensa universal contra daño directo sigue siendo **DEF**.

## Componentes elementales

Una porción puede declarar etiquetas como:

```text
[FUEGO][ELEMENTAL]
[AGUA][ELEMENTAL]
[METAL][ELEMENTAL]
```

Estas etiquetas permiten:
- bonos de daño elemental;
- bonos de un elemento específico;
- requisitos e interacciones de técnicas;
- aflicciones;
- ramas;
- combos futuros.

No añaden una capa defensiva adicional.

## Impactos híbridos

Una acción puede contener varias porciones:

```text
8 físico + 6 fuego
```

Cada porción conserva sus etiquetas durante el cálculo ofensivo. Después se suman y la **DEF universal se aplica una sola vez por impacto**.

## Inmunidades excepcionales

Una criatura o efecto futuro puede poseer una inmunidad explícita y excepcional, por ejemplo:

```text
inmune_fuego: true
```

Esto no crea una estadística de resistencia ni obliga a diseñar buffs de resistencia elemental. Las inmunidades deben ser raras, temáticas y declaradas explícitamente.

## Wuxing

Los ciclos de generación/control no producen multiplicadores automáticos tipo piedra-papel-tijera.

Se reservan para:
- interacciones entre técnicas;
- transformación/consumo de estados;
- combos;
- ramas;
- efectos especiales.

Ejemplo conceptual:

```text
estado de Madera
→ técnica de Fuego
→ interacción especial
```

No:

```text
Fuego siempre hace +X% a Metal
```

## Separación de conceptos

Elemento ≠ tipo físico.

```text
CORTANTE / CONTUNDENTE / PERFORANTE
```

describen la forma del daño físico.

```text
FUEGO / AGUA / METAL / etc.
```

describen naturaleza elemental.

Ambas dimensiones pueden coexistir dentro de una acción sin crear defensas separadas.

## Regla final

> Todo daño directo, físico o elemental, se mitiga con la misma DEF. Los elementos existen para construcción ofensiva, aflicciones e interacciones, no para multiplicar estadísticas defensivas ni exigir una técnica defensiva específica por elemento.

---

# 23. Curación, recuperación y Qi — CERRADO

## Recuperación de Vida

```text
RECUPERACIÓN DE VIDA
├─ Curación directa
├─ Regeneración de Vida
├─ Robo de Vida
├─ Vida al impactar
└─ Vida al matar
```

### Curación directa

```text
CURACIÓN_GENERADA =
(base + bonos planos de curación)
× (1 + suma de % curación realizada)
```

Luego:

```text
CURACIÓN_RECIBIDA =
CURACIÓN_GENERADA
× max(0, 1 + suma de % curación recibida)
```

Y:

```text
CURACIÓN_REAL =
min(curación_recibida, Vida máxima - Vida actual)
```

- La sobrecuración se pierde.
- No genera Absorción salvo efecto explícito.
- No critica por defecto.
- Una prohibición total de curación debe ser una propiedad explícita, no un porcentaje negativo extremo.

### Regeneración de Vida

- Es periódica y distinta de la curación instantánea.
- Puede existir como buff/efecto.
- Los modificadores normales de curación pueden afectar curación directa y regeneración de Vida.
- No afectan Robo de Vida, Vida al impactar ni Vida al matar.
- El orden exacto entre regeneración y DOT al inicio de turno se decidirá al cerrar el ciclo completo del turno.

### Resultado de curación

Debe poder distinguirse:

```text
healing_generated
actual_healing
overhealing
```

---

## Qi — recurso de combate

Separar definitivamente:

```text
qi_actual
qi_max
qi_recompensa
```

`qi_recompensa` no es Qi utilizable en combate.

## Fuentes válidas de recuperación de Qi

**No existe regeneración pasiva de Qi por turno.**

Qi sólo puede recuperarse mediante:

1. **Meditación**.
2. **Píldoras u otros consumibles explícitos de Qi**.
3. **Robo/drenaje de Qi** mediante técnicas o efectos.
4. **Piedras espirituales**.
5. Otras fuentes futuras sólo si se declaran explícitamente como acciones/consumos; nunca como regeneración automática por turno.

No existirán objetos que otorguen:

```text
+X Qi por turno
```

ni estadísticas base de regeneración pasiva de Qi.

## Meditación

Meditación es la fuente normal y sistémica de recuperación de Qi.

Puede seguir dependiendo de:
- raíz espiritual;
- método de cultivo;
- vena/condición espiritual de la sala;
- saturación;
- heridas meridianas;
- otros modificadores explícitos.

Los antiguos conceptos `qi_med` y `hp_med` deben reinterpretarse como parámetros de recuperación **mediante meditación**, no como regeneración general de combate.

### Equipo y meditación

Sí pueden existir objetos que aumenten la cantidad de Qi obtenida al meditar.

Ejemplo conceptual:

```text
+2 Qi obtenido al meditar
```

o:

```text
+X% Qi obtenido mediante meditación
```

Esto mejora la eficiencia de la acción de meditar, pero **no produce Qi automáticamente**.

## Píldoras

Una píldora puede restaurar Qi instantáneamente:

```text
qi_actual =
min(qi_max, qi_actual + recuperación)
```

El exceso se pierde salvo futura mecánica explícita.

## Piedras espirituales

Las piedras espirituales pueden actuar como recurso consumible para recuperar Qi.

Su uso debe ser explícito y consumir la piedra o la cantidad correspondiente. No equivalen a regeneración pasiva.

## Robo / drenaje de Qi

Queda reservado como efecto de técnicas/equipo.

Ejemplo:

```text
robar 3 Qi
```

transfiere como máximo el Qi realmente disponible en el objetivo.

No se crea por ahora una estadística universal de `% Robo de Qi`; se diseña por efecto/técnica para proteger el balance del recurso.

## Separación de sistemas

```text
+% curación
```

no afecta Qi.

```text
+% Qi al meditar
```

no afecta curación de Vida.

Curación no elimina Daño Aplazado; sólo aumenta la Vida disponible para soportar sus pagos. Purgar deuda aplazada requiere un efecto específico.

## Regla final

> Qi es un recurso deliberadamente limitado. No se regenera pasivamente durante el combate. Recuperarlo exige meditar, consumir recursos, drenar/robar Qi o usar piedras espirituales. El equipo puede mejorar la eficiencia de la meditación, pero no crear regeneración automática de Qi por turno.

---

# 24. Política global de precisión y redondeo — CERRADO

## Principio general

**Nunca redondear cálculos intermedios.**

Todas las operaciones de daño, modificadores porcentuales, crítico, DEF, penetración, curación y recuperación conservan precisión decimal mientras el cálculo siga abierto.

El redondeo ocurre únicamente cuando un resultado se convierte en una cantidad discreta que va a modificar un recurso del juego.

## Daño directo

Orden conceptual:

```text
porciones base
→ planos
→ porcentajes ofensivos
→ crítico
→ modificadores recibidos
→ sumar porciones
→ DEF / penetración
→ daño_post_DEF_decimal
→ REDONDEO ÚNICO
→ paquete de daño entero
→ Absorción
→ Vida
```

No se redondea:
- cada componente;
- cada bono;
- el crítico;
- la DEF actual;
- la penetración;
- cada multiplicador.

Se redondea **una sola vez** después de obtener el daño final post-DEF y antes de consumir Absorción/Vida.

## Método de redondeo

Candidato:

```text
ROUND_NEAREST
0.5 o más → entero superior
menos de 0.5 → entero inferior
```

Para cantidades no negativas equivale al comportamiento de `Math.round`.

Ejemplos:

```text
7.49 → 7
7.50 → 8
0.49 → 0
0.50 → 1
```

No existe daño mínimo obligatorio de 1.

## DOT / aflicciones

Cada activación/tick calcula toda su potencia con precisión decimal y redondea **una sola vez al crear el paquete de daño de ese tick**.

Las cargas no se redondean individualmente antes de sumarse si comparten la misma activación; primero se obtiene el total de la activación y luego se redondea una vez.

## Curación

```text
curación base
→ modificadores
→ curación decimal
→ REDONDEO ÚNICO
→ aplicar a Vida
```

La sobrecuración se calcula después del redondeo del paquete de curación.

## Robo de Vida

- Se calcula usando `actual_hp_damage`.
- En multigolpe/AOE futuro se acumula el robo potencial decimal de toda la acción.
- Se aplica el límite por acción.
- Se redondea **una sola vez al finalizar la acción**.
- No se redondea por impacto.

Esto evita que muchos impactos pequeños generen recuperación artificialmente mayor o menor sólo por redondeos repetidos.

## Qi

Píldoras, meditación, piedras espirituales y otros efectos calculan su recuperación completa y redondean una sola vez cuando se modifica `qi_actual`.

No existe regeneración pasiva de Qi.

## DEF y Penetración

DEF actual y DEF efectiva pueden conservar decimales internamente.

Ejemplo:

```text
DEF = 13
-15% DEF
→ 11.05

25% penetración
→ 8.2875
```

No se convierte prematuramente en 11 u 8.

La DEF decimal participa completa en el cálculo del daño y el resultado del daño se redondea al final.

## Probabilidades

Precisión/Evasión, Crítico, Control/Tenacidad y probabilidades de aplicación pueden conservar decimales.

Ejemplo:

```text
73.6% de impacto
```

se compara como 73.6%, no como 74%.

El redondeo visual de la UI no altera el valor mecánico interno.

## Duraciones y stacks

Son cantidades discretas:
- turnos;
- ticks;
- activaciones;
- stacks.

No admiten fracciones salvo que una mecánica futura lo declare explícitamente.

## Vida máxima y Qi máximo

Si en el futuro modificadores porcentuales producen valores fraccionarios de máximos, se calcula todo el valor derivado y se redondea una sola vez al recomputar el máximo.

## Regla final

> Mantener precisión completa durante el cálculo y redondear una única vez en la frontera donde el resultado se convierte en una modificación real y discreta de un recurso. Nunca redondear por componente ni entre capas de la fórmula.

---

# 25. Progresión por cultivo y raíces — CANDIDATO

## Principio general

La progresión de cultivo debe aumentar la capacidad estructural del personaje sin inflar automáticamente todas las estadísticas de combate.

Separar:

```text
PROGRESIÓN GARANTIZADA
→ recursos / acceso / capacidad

PROGRESIÓN DE BUILD
→ daño / DEF / crítico / precisión / penetración / etc.
```

## Qué puede crecer automáticamente con cultivo

El reino/etapa puede otorgar:
- Vida máxima;
- Qi máximo;
- puntos de técnica / acceso a nuevas ramas;
- desbloqueo de técnicas, equipo o sistemas;
- parámetros de cultivo/meditación cuando corresponda.

Los valores numéricos exactos se balancearán posteriormente.

## Qué NO debe crecer automáticamente sólo por subir de etapa

No otorgar de forma universal:
- daño/Ataque;
- DEF;
- Precisión;
- Evasión;
- Probabilidad crítica;
- Daño crítico;
- Penetración;
- Control;
- Tenacidad;
- Robo de Vida;
- Absorción.

Estas estadísticas deben provenir de:
- equipo;
- técnicas;
- ramas;
- buffs/debuffs;
- efectos específicos;
- sistemas especializados.

Una escuela corporal futura puede otorgar DEF/Absorción, por ejemplo, pero no por el mero hecho de avanzar de cultivo.

## Consecraciones / avances internos

El modelo antiguo que sumaba automáticamente ATQ por consagración no debe migrarse.

Las consagraciones pueden aumentar capacidad estructural —principalmente Vida/Qi y desbloqueos— sin introducir un multiplicador ofensivo universal.

## Raíces espirituales

El conjunto canónico de elementos del juego es exactamente:

```text
FUEGO
METAL
AGUA
TIERRA
VIENTO
```

No introducir Madera ni otros elementos nuevos dentro de este contrato.

Las raíces no deben convertirse en paquetes de estadísticas universales del tipo:

```text
Fuego = +ATQ
Metal = +ATQ
Agua = +DEF
```

Los antiguos bonos de ATQ/DEF deben reinterpretarse.

La raíz debe funcionar principalmente como:
- afinidad/etiqueta espiritual;
- relación con técnicas y ramas;
- identidad de cultivo;
- modificador de meditación/eficiencia de Qi cuando corresponda;
- requisito o habilitador de interacciones específicas.

No debe existir una raíz que sea universalmente “la mejor de daño” o “la mejor de defensa” por un bono plano permanente.

## Identidad preliminar de las cinco raíces canónicas

Estas identidades son dirección de diseño, no paquetes gratuitos de estadísticas:

```text
FUEGO
→ intensidad, Quemadura, combustión y transformación de daño/estados

METAL
→ corte, Hemorragia, ruptura y explotación de heridas

AGUA
→ flujo, Control, manipulación de Qi y adaptación

TIERRA
→ estabilidad corporal, Absorción, fortificación y resistencia al Control

VIENTO
→ movilidad, Evasión, reposicionamiento y precisión/ritmo de ataque sin crear una estadística de Velocidad
```

Estas direcciones se apoyan en técnicas ya existentes:
- Fuego: Palma Ardiente, Círculo de las Cien Ascuas, Respiración del Cuerpo-Horno.
- Metal: Filo de Qi Metálico, Lluvia de los Mil Filos.
- Agua: Látigo de Agua, Filamento de Agua, Espejo de Luna, Marea que Barre las Ocho Orillas.
- Tierra: Sello de la Montaña Oprimida, Piel de Cobre.
- Viento: Paso de Nube Ligera, Lanza que Parte Nubes, Tijera del Vendaval Partido.

## Afinidad y técnicas

Una raíz puede interactuar con una técnica sin modificar todo el daño del personaje.

Ejemplos conceptuales futuros:

```text
Raíz Fuego
→ habilita/mejora una rama de Quemadura
```

```text
Raíz Metal
→ habilita interacciones con técnicas de espada/corte y Hemorragia
```

```text
Raíz Agua
→ habilita interacciones de flujo, Control o manipulación de Qi
```

```text
Raíz Tierra
→ habilita fortificación, Absorción o Tenacidad mediante ramas concretas
```

```text
Raíz Viento
→ habilita interacciones de Evasión, reposicionamiento o precisión mediante ramas concretas
```

La forma exacta se definirá al rehacer técnicas; no se hardcodean todavía bonificaciones universales.

## Meditación

Las raíces pueden conservar perfiles distintos de eficiencia al meditar.

Esto puede expresarse mediante:
- Qi base obtenido al meditar;
- modificadores de método;
- afinidad con condiciones espirituales;
- interacción con piedras/venas/objetos.

Esto NO equivale a regeneración pasiva de Qi.

## Crecimiento de poder

La mayor potencia ofensiva al avanzar debe provenir principalmente de:
- técnicas nuevas;
- coeficientes/ramas mejores;
- mayor disponibilidad de Qi;
- mejor equipo;
- sinergias;
- especialización.

No de una suma automática de +ATQ por nivel/etapa.

## Regla final

> Cultivar aumenta primero la capacidad del personaje y abre nuevas herramientas. Las estadísticas de combate especializadas pertenecen a la build, no al simple hecho de subir de etapa.

---

# 26. Siguientes bloques prioritarios

1. Cerrar orden de efectos posteriores al impacto.
2. Definir buffs/debuffs y reducción de DEF.
3. Cerrar Quemadura.
4. Cerrar Veneno.
5. Definir elementos/resistencias.
6. Curación/recuperación/Qi — CERRADO.
7. Política global de redondeo — CERRADO.
8. Progresión por cultivo y raíces — CANDIDATO.
9. Rehacer técnicas.
10. Recrear equipo.
11. Benchmarks de jugador.
12. Rebalance de monstruos/jefes.
