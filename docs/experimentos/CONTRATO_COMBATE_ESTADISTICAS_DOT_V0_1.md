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

## 1.1 Técnicas AOE — contrato global CERRADO

Las técnicas marcadas como AOE no eligen un número máximo de blancos.

```text
AOE
→ alcanza a todos los NPC hostiles presentes en la sala
→ incorpora inmediatamente al combate a los hostiles alcanzados
→ cada objetivo resuelve su propio impacto
```

Reglas:

- No existe un límite base de 3, 4 o 6 objetivos para una AOE.
- Las ramas de una técnica AOE no aumentan el número de objetivos: el alcance total de la sala ya pertenece al contrato base.
- El daño no se divide entre enemigos.
- Con **2 o más objetivos válidos**, la técnica conserva el 100% de su daño calculado.
- Con **un único objetivo válido**, la técnica conserva provisionalmente el **65% de su daño calculado**, reproduciendo la regla de duelo ya existente en `ver74`.
- Ese 65% es una regla global de AOE, no una propiedad individual de cada técnica.
- El valor queda sujeto a benchmark final junto al resto del balance numérico de técnicas de Arco 1.
- Si una Concordancia modifica una AOE, debe declarar expresamente qué propiedad modifica. En el rediseño de Arco 1 se prioriza que una Concordancia válida afecte coherentemente a toda la ejecución, salvo excepción documentada.

Consecuencia de diseño:

```text
unitarget
→ mejor herramienta de duelo

AOE
→ herramienta de grupo
→ pierde eficiencia de daño cuando se fuerza contra un solo enemigo
```

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

# 25. Progresión por cultivo y raíces — CERRADO

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

## Valores de raíces principales — CERRADO

Las cinco raíces principales quedan cerradas con dos rasgos porcentuales/probabilísticos cada una. No se usan bonos planos de daño, DEF, Vida, Qi, Precisión, Control o Tenacidad que se diluyan con la progresión.

| Raíz | Rasgo principal | Rasgo secundario |
|---|---|---|
| Fuego | +10% daño directo general | +5% probabilidad crítica |
| Metal | +10% Penetración porcentual general | +5% Precisión |
| Agua | −10% coste de Qi de todas las técnicas | +5% Control |
| Tierra | +10% Vida máxima | +5% Tenacidad |
| Viento | 10% Evasión base / probabilidad innata de esquivar | +5% Daño crítico |

Reglas de alcance:
- **Fuego**: el +10% afecta todo daño directo propio, incluidos ataques normales y técnicas; no aumenta DOT, Reflect ni Retaliation.
- **Metal**: el +10% de Penetración porcentual afecta todo daño directo que pase por DEF, incluidos ataques normales y técnicas; no afecta DOT ni Absorción.
- **Agua**: el −10% se aplica al coste de Qi de todas las técnicas, sin importar elemento; no genera Qi.
- **Tierra**: el +10% modifica la Vida máxima derivada y escala con el crecimiento futuro del personaje.
- **Viento**: el 10% se expresa mediante la estadística universal Evasión; no crea una segunda tirada de esquiva.

Los rasgos secundarios del 5% forman parte de la identidad de la raíz. Su interacción exacta con otras fuentes del mismo tipo seguirá las reglas globales de cada estadística y sus pools compatibles.

Los injertos todavía no están incluidos en este cierre: debe definirse por separado qué parte de estos rasgos transmite una raíz secundaria.

### Fuego — CERRADO

La raíz principal de Fuego representa potencia ofensiva directa general.

Rasgo:

```text
DAÑO_DIRECTO
= daño calculado × 1.10
```

Reglas:
- aumenta **10% el daño directo general** causado por el personaje;
- afecta ataques normales y técnicas;
- afecta componentes físicos, elementales e híbridos que formen parte de un impacto directo;
- no aumenta DOT/aflicciones como Quemadura o Hemorragia;
- no aumenta Reflect, Retaliation ni otras fuentes reactivas;
- se integra en el pool porcentual ofensivo normal compatible, no como multiplicador final separado;
- conserva precisión decimal y sigue la política global de redondeo.

Esta propiedad pertenece a la **raíz principal Fuego**. La transmisión mediante injerto todavía no está definida.

---

### Metal — CERRADO

La raíz principal de Metal representa ruptura de defensas en todo combate directo.

Rasgo:

```text
PENETRACIÓN_PORCENTUAL_GENERAL += 10%
```

Reglas:
- concede **10% de Penetración porcentual general** a todo daño directo que pase por DEF;
- se aplica a ataques normales, técnicas físicas, elementales e híbridas;
- no afecta DOT/aflicciones;
- no afecta Reflect, Retaliation ni otras fuentes reactivas;
- no afecta Absorción;
- se suma de forma aditiva con otras fuentes normales de Penetración porcentual compatibles;
- se resuelve dentro del orden universal ya cerrado: DEF real → reducción/shred → Penetración % → Penetración plana → DEF efectiva.

Esta propiedad pertenece a la **raíz principal Metal**. La transmisión mediante injerto todavía no está definida.

---

### Tierra — CERRADO

La raíz principal de Tierra representa resistencia estructural del cuerpo.

Rasgo:

```text
VIDA_MÁXIMA_FINAL
= Vida máxima calculada × 1.10
```

Reglas:
- aumenta **10% la Vida máxima**;
- se aplica de forma porcentual para conservar relevancia a futuro;
- no concede DEF plana;
- no concede Absorción permanente;
- no concede Tenacidad plana;
- puede coexistir con otras fuentes porcentuales de Vida máxima;
- los porcentajes normales compatibles de Vida máxima se combinan de forma aditiva antes de aplicar el resultado;
- el valor final respeta la política global de redondeo para máximos derivados.

Esta propiedad pertenece a la **raíz principal Tierra**. La transmisión mediante injerto todavía no está definida.

---

### Viento — CERRADO

La raíz principal de Viento representa evasión innata.

Rasgo:

```text
EVASIÓN_BASE += 10 puntos porcentuales
```

Interpretación:
- equivale a una **probabilidad innata de esquivar** dentro del sistema universal Precisión ↔ Evasión;
- no crea una segunda tirada de esquiva ni una capa multiplicativa posterior;
- contra Precisión 100 y sin otras fuentes de Evasión, produce 90% de impacto / 10% de evasión;
- otras fuentes de Evasión pueden sumarse normalmente a la Evasión total;
- sigue respetando el clamp universal de impacto 5%–100%;
- no afecta impactos marcados como `evadible:false`;
- no afecta DOT ya aplicados, Control puro ni daño reactivo.

Aunque el valor sea fijo en puntos porcentuales, pertenece a una estadística probabilística acotada y conserva relevancia a futuro; no es un bono plano de daño/DEF/recursos que se diluya al escalar los números del juego.

Esta propiedad pertenece a la **raíz principal Viento**. La transmisión mediante injerto todavía no está definida.

---

### Agua — CERRADO

La raíz principal de Agua representa eficiencia general en la circulación de Qi.

Rasgo:

```text
COSTE_FINAL_DE_TÉCNICA
= coste calculado × 0.90
```

Reglas:
- reduce **10% el coste de Qi de todas las técnicas**, no sólo las de Agua;
- no genera Qi y no cuenta como regeneración;
- no modifica el coste de acciones que no sean técnicas;
- se aplica de forma porcentual para conservar relevancia a futuro;
- el resultado conserva precisión decimal durante el cálculo y se redondea únicamente al convertir el coste en Qi realmente gastado, siguiendo la política global de redondeo;
- esta reducción usa el sistema general de **reducción de coste de Qi** y puede coexistir con otras fuentes futuras.

### Reducción de coste de Qi — sistema general

Pueden existir múltiples fuentes compatibles, por ejemplo:
- raíz principal;
- equipo u objetos;
- ramas de técnicas;
- buffs/estados temporales;
- efectos especiales.

Cada fuente debe declarar su alcance, por ejemplo:
- GLOBAL: todas las técnicas;
- ELEMENTO: sólo técnicas de un elemento;
- TÉCNICA/FAMILIA: sólo una técnica o grupo concreto.

Las reducciones porcentuales normales compatibles se suman en un mismo pool:

```text
REDUCCIÓN_TOTAL_QI =
suma de reducciones compatibles

COSTE_QI_CALCULADO =
coste base × (1 - REDUCCIÓN_TOTAL_QI)
```

No se redondean reducciones intermedias.

Debe existir un **piso global de coste** para impedir técnicas prácticamente gratuitas. El valor numérico exacto del piso se balanceará por separado antes de implementar.

Esta propiedad pertenece a la **raíz principal Agua**. La transmisión mediante injerto todavía no está definida.

---

## Injerto espiritual — CERRADO

El personaje puede incorporar una única raíz secundaria permanente.

La raíz secundaria transmite:

```text
AFINIDAD ELEMENTAL
→ 100%

RASGOS NUMÉRICOS DE LA RAÍZ
→ 80%

APRENDIZAJE DE TÉCNICAS AFINES
→ 90%
```

La afinidad elemental no se reduce: el injerto cuenta plenamente como afinidad para requisitos, ramas, técnicas e híbridas.

Los rasgos numéricos sí se expresan al 80% de su valor de raíz principal.

Valores derivados:

| Injerto | Rasgos heredados |
|---|---|
| Fuego | +8% daño directo general · +4% probabilidad crítica |
| Metal | +8% Penetración porcentual general · +4% Precisión |
| Agua | −8% coste de Qi de todas las técnicas · +4% Control |
| Tierra | +8% Vida máxima · +4% Tenacidad |
| Viento | 8% Evasión base · +4% Daño crítico |

Reglas:
- la raíz principal conserva el 100% de sus rasgos;
- el injerto no sustituye ni reduce los rasgos de la raíz principal;
- los rasgos compatibles de raíz principal, injerto, equipo, ramas y buffs se combinan según las reglas globales de cada estadística;
- el injerto concede 100% de afinidad elemental para activar requisitos y combinaciones;
- las técnicas de la raíz secundaria progresan al 90% de ritmo de aprendizaje;
- sólo puede existir un injerto espiritual permanente por personaje;
- compatibilidades, conflictos e interacciones entre afinidades pueden diseñarse por separado, pero **las raíces no determinan si una combinación es ofensiva, defensiva, de control o utilitaria**; esa función pertenece a cada técnica concreta.

---

## Concordancias por rama elemental — EN DEFINICIÓN

### Rama Fuego — CERRADA CONCEPTUALMENTE

Una técnica pura de Fuego deja un **Eco de Fuego**. Si la siguiente técnica compatible consume ese eco, la concordancia depende del elemento receptor.

No existe un bono universal de Concordancia.

```text
FUEGO → TIERRA
Cimiento cocido
Identidad: consolidación.
- ofensiva: potencia la magnitud ofensiva principal de la técnica Tierra;
- defensiva: potencia la DEF o Absorción generada por la técnica Tierra.
```

```text
FUEGO → METAL
Forja / templado
Identidad: ruptura o endurecimiento.
- ofensiva: mejora Penetración;
- defensiva: mejora la magnitud defensiva propia de la técnica Metal.
```

```text
FUEGO → AGUA
Presurización / vapor
Identidad: presión y transformación.
- ofensiva/control: potencia Control o debilitación compatible;
- defensiva: habilita una respuesta reactiva propia de la técnica Agua.
```

```text
FUEGO → VIENTO
Corriente ascendente / aceleración
Identidad: aceleración.
- ofensiva: mejora una propiedad crítica compatible;
- defensiva: mejora la Evasión generada por la técnica Viento.
```

Las magnitudes numéricas quedan pendientes hasta probar estas identidades sobre técnicas reales.

---

### Rama Metal — CERRADA CONCEPTUALMENTE

Una técnica pura de Metal deja un **Eco de Metal**. La concordancia depende del elemento receptor.

```text
METAL → FUEGO
Chispa / ignición
Identidad: punto de ignición.
- ofensiva: potencia la aplicación o potencia de Quemadura compatible;
- defensiva: habilita una respuesta térmica/reactiva compatible.
```

```text
METAL → AGUA
Cauce tallado / canalización
Identidad: flujo dirigido.
- ofensiva/control: potencia Control o precisión del efecto compatible;
- defensiva/utilitaria: mejora la eficiencia de Qi de esa ejecución.
```

```text
METAL → TIERRA
Anclaje de hierro
Identidad: refuerzo estructural.
- ofensiva: mejora una propiedad de ruptura/penetración compatible;
- defensiva: potencia Absorción, Tenacidad u otra magnitud defensiva propia de la técnica Tierra.
```

```text
METAL → VIENTO
Filo en la corriente
Identidad: precisión y aprovechamiento de aperturas.
- ofensiva: mejora Precisión u otra propiedad de ejecución compatible;
- defensiva: puede potenciar la Evasión generada por una técnica Viento, sujeto a validación con técnicas reales.
```

Las magnitudes numéricas quedan pendientes hasta probar estas identidades sobre técnicas reales.

---

### Rama Agua — CERRADA CONCEPTUALMENTE

Una técnica pura de Agua deja un **Eco de Agua**. La concordancia depende del elemento receptor.

```text
AGUA → FUEGO
Vapor súbito
Identidad: transformación por presión.
- ofensiva: potencia una propiedad compatible de Quemadura, expansión o presión del efecto;
- defensiva: habilita una respuesta térmica/reactiva compatible.
```

```text
AGUA → METAL
Templar el filo
Identidad: templado y calidad del golpe.
- ofensiva: favorece Daño Crítico u otra propiedad crítica compatible;
- defensiva: potencia estabilidad/fortificación propia de la técnica Metal.
```

```text
AGUA → TIERRA
Erosión / sedimentación
Identidad: desgaste o cohesión.
- ofensiva: puede aplicar reducción de DEF para impactos posteriores;
- defensiva: potencia estabilidad/cohesión de una técnica Tierra compatible.
```

```text
AGUA → VIENTO
Velo de niebla
Identidad: desorientación y ocultación.
- ofensiva: reduce Precisión u otra capacidad ofensiva compatible del objetivo;
- defensiva: potencia la Evasión generada por la técnica Viento.
```

Las magnitudes numéricas quedan pendientes hasta probar estas identidades sobre técnicas reales.

---

### Rama Tierra — CERRADA CONCEPTUALMENTE

Una técnica pura de Tierra deja un **Eco de Tierra**. La concordancia depende del elemento receptor.

```text
TIERRA → FUEGO
Corazón de magma
Identidad: contención y persistencia del calor.
- ofensiva: potencia persistencia/intensidad de una aflicción de Fuego compatible;
- defensiva: mejora la capacidad de contener o aprovechar daño recibido mediante la técnica Fuego.
```

```text
TIERRA → METAL
Forja asentada
Identidad: asentamiento y calidad estructural.
- ofensiva: favorece Probabilidad Crítica;
- defensiva: potencia estabilidad de DEF, Absorción o fortificación propia de la técnica Metal.
```

```text
TIERRA → AGUA
Cauce represado
Identidad: peso y contención del flujo.
- ofensiva/control: reduce Evasión u otra movilidad compatible del objetivo;
- defensiva/utilitaria: puede aumentar duración de un efecto Agua compatible en lugar de su magnitud.
```

```text
TIERRA → VIENTO
Tormenta de polvo
Identidad: dispersión material y persistencia del movimiento.
- ofensiva: favorece área/propagación o eficiencia contra múltiples objetivos;
- defensiva: puede aumentar duración de la Evasión generada por la técnica Viento.
```

Las magnitudes numéricas quedan pendientes hasta probar estas identidades sobre técnicas reales.

---

### Rama Viento — CERRADA CONCEPTUALMENTE

Una técnica pura de Viento deja un **Eco de Viento**. La concordancia depende del elemento receptor.

```text
VIENTO → FUEGO
Avivar las brasas
Identidad: intensificación inmediata.
- ofensiva: potencia el daño directo de la técnica Fuego receptora;
- defensiva: potencia la magnitud inmediata del efecto defensivo generado por la técnica Fuego.
```

```text
VIENTO → METAL
Filo impulsado
Identidad: aceleración y precisión.
- ofensiva: mejora Precisión de la técnica Metal;
- defensiva: puede mejorar su eficiencia de ejecución, incluyendo reducción de coste de Qi cuando la técnica lo admita.
```

```text
VIENTO → AGUA
Corriente ligera
Identidad: circulación eficiente.
- cualquier técnica compatible: reduce porcentualmente el coste de Qi de la ejecución receptora;
- esta reducción entra en el pool general de reducción de coste de Qi y respeta el piso global del sistema.
```

```text
VIENTO → TIERRA
Impacto de vendaval
Identidad: impulso aplicado a masa y estructura.
- ofensiva/control: potencia Control u otra propiedad de impacto compatible;
- defensiva: potencia Tenacidad generada cuando la técnica Tierra posea esa propiedad.
```

Las magnitudes numéricas quedan pendientes hasta probar estas identidades sobre técnicas reales.

---

## Regla de cobertura técnica de Concordancias — CERRADA

Toda Concordancia habilitada en una etapa del juego debe tener una aplicación mecánica real sobre al menos una técnica receptora disponible en esa misma etapa.

```text
CONCORDANCIA DISPONIBLE
→ debe existir técnica receptora compatible
→ debe existir propiedad real que pueda potenciar/modificar
→ el efecto debe ser visible y resolverse en runtime
```

No se admite una Concordancia meramente nominal que se active sin producir un efecto aplicable.

Consecuencias de diseño:

- las técnicas se auditan y, cuando corresponda, se ajustan después de cerrar las Concordancias;
- cada técnica debe declarar qué propiedades de Concordancia acepta;
- una técnica no necesita aceptar todas las Concordancias posibles de su elemento;
- si una Concordancia no tiene receptor compatible en una etapa, no debe introducirse todavía en esa etapa;
- no se inventa un bono genérico de emergencia para evitar una Concordancia vacía;
- cuando una técnica tenga varias propiedades potenciales, la Concordancia debe indicar de forma explícita cuál modifica;
- las Concordancias pueden añadir una propiedad nueva sólo cuando esa interacción esté diseñada expresamente para esa técnica o familia.

La cobertura se valida por contenido real, no sólo por la matriz teórica de 20 relaciones dirigidas.

---

## Reconstrucción del catálogo de técnicas de Arco 1 — CERRADO COMO DIRECCIÓN

Las técnicas comunes de Arco 1 se **recrearán desde cero** sobre el nuevo contrato de combate.

El catálogo de `ver74` queda como **referencia histórica**, no como base mecánica a migrar automáticamente.

Principios:

- no se conservan automáticamente daño, coste de Qi, duración, DEF, Guardia, Evasión, Control, ramas ni requisitos del catálogo anterior;
- los nombres, fantasía y conceptos de técnicas antiguas pueden reutilizarse sólo si siguen encajando con el nuevo diseño;
- cada técnica nueva debe definirse contra las estadísticas, pipeline, Concordancias, DOT, Control, DEF, Absorción y reglas de afinidad ya cerradas;
- cada técnica debe declarar con claridad su elemento, rol, efecto principal, coste, requisitos y compatibilidades de Concordancia;
- no se mantiene una técnica sólo por continuidad histórica si genera contradicciones con el nuevo sistema;
- el balance numérico se hará después de cerrar primero la identidad y función de cada técnica;
- las Definitivas híbridas se tratan por separado del catálogo común y permanecen fuera de Concordancias;
- las **cinco técnicas iniciales**, una por cada elemento canónico, serán **ofensivas**;
- el prólogo debe presentar una opción ofensiva inicial para Fuego, Metal, Agua, Tierra y Viento;
- la diferenciación hacia defensa, control, aflicciones, apoyo o utilidad aparecerá después mediante nuevas técnicas, ramas y progresión;
- las cinco técnicas iniciales no necesitan compartir la misma mecánica ofensiva: pueden diferenciarse por daño directo, precisión, control asociado, preparación de estados u otras propiedades compatibles, siempre que su función principal siga siendo ofensiva;

### Recordatorio de prólogo / selección inicial — PENDIENTE

La selección del prólogo debe revisarse para que pueda representar correctamente los **cinco elementos canónicos**:

- Fuego
- Metal
- Agua
- Tierra
- Viento

El prólogo actual no debe quedar limitado al antiguo conjunto inicial de tres raíces/técnicas.

Queda pendiente decidir durante el rediseño del prólogo:

- si se añade una técnica inicial común por cada uno de los cinco elementos;
- si la estructura de preguntas actual alcanza para distinguir las cinco opciones;
- si conviene añadir **una o dos preguntas adicionales** para mejorar la selección;
- cómo evitar que la elección de prólogo determine de forma excesivamente rígida la build futura.

No se modifica todavía el runtime del prólogo.

---

## Técnicas híbridas / Definitivas — PRINCIPIO CERRADO

Las técnicas híbridas representan la **Definitiva del personaje**: la expresión más poderosa de dos disciplinas elementales combinadas.

No forman parte de la rotación ordinaria ni deben poder utilizarse de manera repetitiva sin planificación.

Principios:

- una híbrida combina exactamente dos elementos y sigue siendo una sola técnica/acción;
- su función concreta depende de la técnica: puede ser ofensiva, defensiva, de control u otra función diseñada;
- por jerarquía, debe ser una de las herramientas más poderosas del kit del personaje;
- su potencia se compensa mediante un coste estratégico alto;
- el coste principal debe combinar **alto consumo de Qi** y **enfriamiento (cooldown) elevado**;
- su uso debe plantear una decisión real sobre el momento de activación;
- no debe ser eficiente utilizarla apenas está disponible sin considerar el estado del combate;
- no se fijan todavía valores numéricos de Qi ni cooldown: se balancearán después sobre técnicas concretas;
- una Definitiva híbrida **no se entrega como recompensa común ni se desbloquea automáticamente por progresión básica**;
- su obtención debe constituir un hito relevante y deliberado de progresión, ligado al desarrollo real de ambas disciplinas y a contenido específico;
- el método concreto de adquisición (maestro, manual, prueba, evento, legado, misión u otro) se diseña por contenido y no se universaliza todavía;
- poseer afinidad o incluso dos raíces compatibles no concede por sí solo la Definitiva;
- la obtención de una Definitiva híbrida es **independiente de la raíz principal y del injerto** del personaje;
- un personaje puede obtener una Definitiva cuyos dos elementos sean ajenos a sus afinidades actuales;
- obtenerla no obliga al jugador a incorporarla a su build: debe evaluar si su dominio, coste de Qi, cooldown, requisitos y sinergias justifican utilizarla;
- la afinidad influirá en qué tan natural/eficiente resulte desarrollar y aprovechar la técnica, pero no constituye por sí sola un bloqueo universal de uso;
- las penalizaciones o eficiencias exactas para híbridas con confluencia, afinidad parcial o afinidad ajena se definirán por separado antes del balance final;
- una Definitiva híbrida que no sea afín a la raíz principal y/o injerto puede sufrir penalidades reales de uso;
- dichas penalidades no impiden necesariamente la activación: convierten el uso de una Definitiva ajena en una decisión de coste/beneficio;
- los ejes candidatos de penalización son coste de Qi, eficiencia/potencia, estabilidad de ejecución y/o requisitos de dominio; no se fijan todavía magnitudes ni se aplican todos los ejes simultáneamente por defecto;
- la confluencia completa debe representar el uso más natural de la Definitiva, la afinidad parcial una situación intermedia y la afinidad ajena la situación con mayor fricción;
- **RETROCESO ESPIRITUAL — CERRADO COMO PRINCIPIO:** una Definitiva híbrida ejecutada con afinidad insuficiente puede provocar un retroceso interno tras la ejecución;
- el retroceso representa una circulación forzada de Qi por meridianos no adaptados a esa combinación elemental; no es daño infligido por el enemigo ni daño normal de la propia técnica;
- confluencia completa: sin retroceso espiritual;
- afinidad parcial: retroceso espiritual leve;
- afinidad ajena: retroceso espiritual mayor;
- el retroceso puede expresarse como una pequeña pérdida de Vida proporcional a la Vida máxima; los porcentajes exactos se balancearán después;
- el retroceso no usa Precisión, Crítico, DEF, Penetración ni Life Leech;
- no se considera DOT ni activa eventos ofensivos normales;
- **HERIDA MERIDIANA:** una Definitiva ajena puede, bajo condiciones o probabilidad explícita, causar una Herida Meridiana además del retroceso; esta consecuencia debe ser poco frecuente y más seria que la pérdida de Vida;
- la Herida Meridiana no es obligatoria en cada uso ajeno: debe preservar la posibilidad estratégica de emplear una Definitiva incompatible sin convertirla en una opción irracional;
- **DESVIACIÓN DE QI:** queda reservada para eventos excepcionales de incompatibilidad extrema, abuso, fallo grave o contenido narrativo/especial; no se usa como penalidad ordinaria por emplear una Definitiva ajena;
- valores exactos del retroceso, probabilidad/condiciones de Herida Meridiana, interacción con Absorción y posibilidad de muerte por retroceso quedan pendientes de prueba y cierre numérico;
- las Definitivas híbridas quedan **fuera del sistema de Concordancias**;
- no consumen Ecos elementales;
- no generan Ecos elementales;
- no reciben mejoras de Concordancia;
- no activan Concordancias por contener dos elementos;
- esta exclusión es intencional: su potencia, coste de Qi y cooldown ya constituyen una capa superior de poder y decisión táctica;
- las técnicas híbridas actuales combinan exactamente **dos elementos**;
- cualquier técnica de tres elementos queda reservada como posibilidad futura y requerirá un contrato propio antes de implementarse;
- cualquier interacción entre Concordancias y Definitivas híbridas debe diseñarse de forma explícita para evitar amplificaciones descontroladas.

La potencia de una Definitiva no significa necesariamente daño directo: una híbrida defensiva puede constituir la herramienta defensiva más poderosa del personaje, una híbrida de control su mayor herramienta de control, etc.

---

## Combinaciones dobles ya confirmadas

El juego ya contiene cuatro Definitivas híbridas que muestran cómo una misma combinación elemental puede expresarse mediante una técnica concreta. **La orientación ofensiva, defensiva, de control o utilitaria pertenece a la técnica, no a la pareja de raíces.**

### Ofensivas

```text
FUEGO + VIENTO
→ Brasa del Vendaval
→ ofensiva
```

```text
AGUA + VIENTO
→ Aguja del Río de Plata
→ ofensiva
```

```text
AGUA + FUEGO
→ Loto de Vapor Concordante
→ ofensiva
```

### Defensiva

```text
METAL + TIERRA
→ Coraza del Crisol Sereno
→ guardia / Absorción
```

Estas cuatro técnicas quedan como anclas existentes del diseño.

Las otras seis parejas posibles entre los cinco elementos no necesitan una orientación ofensiva/defensiva propia: una misma pareja puede sostener técnicas de funciones distintas si el diseño de esas técnicas lo justifica.

La función de combate se define **por técnica**, no por raíz ni por combinación de raíces.

---

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
