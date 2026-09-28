# Contrato de combate y aflicciones — checkpoint v0.1

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

Modelo lógico:

```text
ACCIÓN
 └─ 1..N IMPACTOS
     └─ 1..N COMPONENTES DE DAÑO
```

En Arco 1, una acción usa normalmente un solo impacto. El multigolpe queda preparado arquitectónicamente para arcos futuros.

Un impacto puede contener varios componentes, por ejemplo:

```text
6 físico + 8 fuego
```

Sigue siendo **un solo impacto** para DEF, crítico y absorción.

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

# 4. Crítico

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
- Crítico se resuelve después de modificadores ofensivos y antes de DEF.
- DOT no critica por defecto.
- Ramas específicas podrán permitir crítico de DOT.
- Si un DOT puede criticar, sus ticks tiran crítico independientemente.
- El crítico del golpe inicial no vuelve automáticamente crítico al DOT ni aumenta su potencia.

---

# 5. Defensa

DEF es reducción plana universal de daño directo.

```text
daño directo del impacto
→ DEF efectiva
→ Absorción
→ Vida
```

- Puede reducir daño directo hasta 0.
- Se aplica una vez por impacto.
- Un impacto híbrido suma sus componentes y luego aplica DEF una sola vez.
- DOT ignora DEF.
- En futuro multigolpe, DEF se aplica a cada impacto por separado.

---

# 6. Penetración de armadura

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

# 7. Absorción

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

# 8. Control y Tenacidad

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

# 9. Reflect / Retaliation — post Arco 1

Preparados arquitectónicamente pero no activos en Arco 1.

- Reflect = porcentaje del daño directo recibido.
- Retaliation = valor plano por impacto directo recibido.
- DOT no los dispara.
- Evasión impide el trigger.
- Absorción no impide el trigger si existió impacto válido.
- Nunca generan recursión entre sí.

---

# 10. DOT / aflicciones — reglas universales cerradas

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

# 11. HEMORRAGIA — contrato base CERRADO

## Naturaleza

Aflicción física persistente producida por determinadas acciones cortantes.

## Aplicación

Sólo una acción que lo declare explícitamente puede aplicar Hemorragia.

Llevar una espada no basta.

Orden:

```text
1. Precisión vs Evasión
2. Impacto válido
3. Resolver daño directo
4. Aplicar Hemorragia
```

La nueva carga nunca beneficia al golpe que acaba de crearla.

## Estructura de cada carga

Cada carga conserva:

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

aunque internamente tengan potencias/duraciones distintas.

## Activación

Hemorragia no usa tick automático por turno.

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

Se resuelve antes de ejecutar la acción elegida:

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
- El crítico del golpe inicial no modifica automáticamente su potencia o duración.
- Cualquier interacción con crítico debe venir de una rama o efecto explícito.

## Escalado

La Hemorragia posee potencia propia y **no se calcula como porcentaje del daño final del golpe**.

Modelo conceptual:

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

Afectan:
- daño global aplicable;
- daño DOT;
- daño físico;
- daño Hemorragia.

No afectan automáticamente:
- daño de ataque común;
- daño de arma;
- daño directo;
- Penetración.

## Acumulación

- Cargas independientes.
- Máximo bajo y legible.
- Parámetro inicial de laboratorio: **4 cargas**.
- El 4 no queda congelado como valor final de balance.

Al superar el máximo:

```text
la nueva carga reemplaza la más antigua
```

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

Todo esto pertenece a ramas, nodos, técnicas, equipo o efectos explícitos.

Ejemplos de especialización futura:

```text
HERIDAS EXPUESTAS
Cada carga aumenta el daño CORTANTE recibido.
```

```text
DESGARRO
Consume cargas para un efecto inmediato.
```

```text
FILO SANGRIENTO
Los críticos cortantes pueden aplicar una carga adicional.
```

## Identidad

> Hemorragia recompensa abrir heridas mediante acciones cortantes y mantener al enemigo combatiendo. Su núcleo es daño persistente condicionado a actuar; sus interacciones ofensivas adicionales se distribuyen entre ramas de técnicas.

---

# 12. Familias en estudio

## Quemadura — SIGUIENTE BLOQUE

Pendiente de cerrar:
- identidad base;
- tick;
- máximo de cargas;
- duración;
- acumulación;
- reaplicación;
- potencia;
- relación con elemento Fuego;
- reglas de detonación/consumo;
- separación entre núcleo base y ramas.

Dirección de diseño ya acordada:
- pocos stacks;
- intensidad rápida;
- adecuada para detonación;
- no convertir la detonación en bucle rígido A→B;
- varias técnicas deben poder leer/transformar/consumir cargas mediante etiquetas generales.

## Veneno — pendiente

Dirección actual:
- más stacks;
- desgaste sostenido;
- duración mayor;
- debe diferenciarse de Quemadura;
- posible especialización futura en mantenimiento, anti-curación o acumulación.

---

# 13. Siguiente paso

Cerrar **QUEMADURA** con el mismo nivel de precisión usado para Hemorragia antes de rehacer las técnicas.

Cuando todas las familias y estadísticas estén cerradas:
1. reetiquetar/recrear técnicas;
2. recrear equipo;
3. construir baseline del jugador;
4. ejecutar benchmarks;
5. recién después rebalancear monstruos/jefes.
