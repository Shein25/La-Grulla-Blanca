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

# 22. Daño elemental y resistencias — SIGUIENTE BLOQUE

Pendiente de cerrar:
- qué significa una etiqueta elemental;
- si existe resistencia elemental como estadística universal o sólo como propiedad explícita;
- ventajas/debilidades entre elementos;
- interacción con impactos híbridos;
- relación con DEF universal;
- límites para evitar duplicar capas defensivas.

---

# 23. Siguientes bloques prioritarios

1. Cerrar orden de efectos posteriores al impacto.
2. Definir buffs/debuffs y reducción de DEF.
3. Cerrar Quemadura.
4. Cerrar Veneno.
5. Definir elementos/resistencias.
6. Definir curación/recuperación/Qi.
7. Fijar política global de redondeo.
8. Reinterpretar progresión por cultivo y raíces.
9. Rehacer técnicas.
10. Recrear equipo.
11. Benchmarks de jugador.
12. Rebalance de monstruos/jefes.
