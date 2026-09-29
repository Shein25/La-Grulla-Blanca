# Contrato global de Concordancias elementales — v0.1

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **MATRIZ CONCEPTUAL COMPLETA / 20 DE 20 RELACIONES APROBADAS / SIN NÚMEROS DE BALANCE**

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
5. si no encuentra hook compatible, no consume Eco por Concordancia; una técnica pura receptora que complete una ejecución válida puede generar después su propio Eco y sustituir el anterior;
6. no existe fallback universal de daño;
7. una relación sólo puede usar `DIRECT_DAMAGE` si su identidad global lo justifica;
8. las magnitudes numéricas se balancean después; primero se cierra identidad, canales y prioridad;
9. la matriz usa exclusivamente propiedades registradas en `REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md`.

10. **Escalado relativo obligatorio:** una Concordancia no añade cantidades absolutas de daño, DEF, curación, Absorción, Precisión, Control, Tenacidad, Penetración ni magnitudes equivalentes. Cuando aumenta una magnitud numérica escalable, lo hace como **porcentaje relativo del hook receptor**.
11. Los modificadores de Concordancia se expresan conceptualmente como `receiver_value × (1 + concordance_scale)`, o una transformación porcentual equivalente declarada por la relación.
12. Las propiedades probabilísticas también se escalan de forma relativa a su magnitud receptora; una Concordancia no concede puntos porcentuales fijos por defecto.
13. Las transformaciones estructurales discretas —por ejemplo impedir un consumo una vez, crear un estado contenido, detonar un estado o cambiar su regla de propagación— pueden existir sin convertirse en una suma numérica fija.
14. Una Concordancia no debe otorgar `+N daño`, `+N DEF`, `+N Precisión`, `+N Control` ni equivalentes como bono de escalado.
15. Si una propiedad discreta no admite escalado porcentual coherente, la relación debe modificar su **potencia, probabilidad, eficiencia o regla estructural**, no añadir una cantidad fija arbitraria.
16. La presencia de `DIRECT_DAMAGE` en `mechanical_hooks[]` no lo expone automáticamente a Concordancias. Sólo puede resolverse sobre daño directo cuando la técnica lo declara expresamente en `concordance_hooks[]`.
17. `EXECUTION` queda retirado temporalmente de las prioridades de la matriz hasta que exista una semántica operacional única y reutilizable.

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
3. DEBUFF_DURATION
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
4. DIRECT_DAMAGE
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
2. ACTION_DENIAL
3. DEBUFF_DURATION
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
4. PROPAGATION
5. DIRECT_DAMAGE
```

Se selecciona sólo el primer hook expuesto compatible.

### DEFENSIVE

```text
1. EVASION_GRANTED
2. REACTIVE_RESPONSE
3. DEFENSIVE_DURATION
```

Esta prioridad representa la intensificación dinámica propia de Fuego sobre defensas de Viento.

### CONTROL

```text
1. INTERRUPT
2. CONTROL_POWER
3. ACTION_DENIAL
```

### UTILITY

```text
1. PROPAGATION
2. ZONE_DURATION
```

---

# 2. Resumen Fuego aprobado

| Relación | Identidad |
|---|---|
| Fuego → Tierra | consolidar / endurecer estructura |
| Fuego → Metal | forjar / templar |
| Fuego → Agua | presurizar / expandir / transformar |
| Fuego → Viento | acelerar / elevar / dinamizar |



---

# 2. METAL como origen — APROBADO

Metal representa dirección, precisión, filo, canalización y refuerzo estructural.

## 2.1 METAL → FUEGO · Chispa de Ignición

**Identidad:** Metal concentra Fuego en un punto de ignición. Favorece prender, concentrar o encontrar un punto crítico; no representa persistencia prolongada.

### OFFENSIVE

\`\`\`text
1. AFFLICTION_APPLICATION
2. DOT_POTENCY
3. INTENSITY
4. CRIT_CHANCE
\`\`\`

Si la técnica Fuego no expone ninguno de esos canales, no consume Eco Metal.

### DEFENSIVE

\`\`\`text
1. REACTIVE_RESPONSE
2. INTERNAL_RESOURCE
3. ABSORPTION
4. FORTIFICATION
\`\`\`

No implica Reflect automáticamente.

### CONTROL

\`\`\`text
1. AFFLICTION_APPLICATION
2. CONTROL_POWER
3. INTERRUPT
4. ACTION_DENIAL
\`\`\`

Sólo cuando la técnica de Fuego fundamenta su control en ignición, explosión, dolor térmico o activación equivalente.

### UTILITY

\`\`\`text
1. AFFLICTION_APPLICATION
2. INTERNAL_RESOURCE
\`\`\`

---

## 2.2 METAL → AGUA · Cauce Tallado

**Identidad:** Metal proporciona un cauce definido al Agua: la dirige, concentra y evita dispersión.

### OFFENSIVE

\`\`\`text
1. PRECISION
2. CONTROL_POWER
3. QI_DRAIN
4. DIRECT_DAMAGE
\`\`\`

\`DIRECT_DAMAGE\` queda al final.

### CONTROL

\`\`\`text
1. CONTROL_POWER
2. PRECISION
3. INTERRUPT
4. ACTION_DENIAL
5. QI_DRAIN
\`\`\`

Metal no crea Control: canaliza mejor uno ya expuesto.

### DEFENSIVE

\`\`\`text
1. QI_COST_PERCENT
2. ABSORPTION_RESTORE
3. DEFENSIVE_DURATION
4. INTERNAL_RESOURCE
\`\`\`

### UTILITY

\`\`\`text
1. QI_COST_PERCENT
2. QI_DRAIN
3. PROPAGATION
4. INTERNAL_RESOURCE
\`\`\`

---

## 2.3 METAL → TIERRA · Anclaje de Hierro

**Identidad:** Metal introduce estructura, refuerzo y puntos de anclaje dentro de Tierra.

### OFFENSIVE

\`\`\`text
1. PERCENT_PENETRATION
2. FLAT_PENETRATION
3. DEF_SHRED
4. CONTROL_POWER
5. DIRECT_DAMAGE
\`\`\`

### DEFENSIVE

\`\`\`text
1. STACKABLE_STATE
2. FORTIFICATION
3. TENACITY_GRANTED
4. ABSORPTION
5. DEF_GRANTED
\`\`\`

\`STACKABLE_STATE\` permite representar casos como Arraigo sin hardcodear su nombre.

### CONTROL

\`\`\`text
1. CONTROL_POWER
2. ACTION_DENIAL
3. DEBUFF_DURATION
\`\`\`

### UTILITY

\`\`\`text
1. STACKABLE_STATE
2. FORTIFICATION
3. INTERNAL_RESOURCE
4. DEFENSIVE_DURATION
\`\`\`

---

## 2.4 METAL → VIENTO · Filo en la Corriente

**Identidad:** Metal da dirección y filo a algo móvil y disperso: precisión de trayectoria y definición del borde.

### OFFENSIVE

\`\`\`text
1. PRECISION
2. PERCENT_PENETRATION
3. FLAT_PENETRATION
4. CRIT_CHANCE
5. DIRECT_DAMAGE
\`\`\`

Se selecciona sólo el primer hook compatible.

### DEFENSIVE

\`\`\`text
1. EVASION_GRANTED
2. QI_COST_PERCENT
3. REACTIVE_RESPONSE
4. DEFENSIVE_DURATION
\`\`\`

### CONTROL

\`\`\`text
1. PRECISION
2. INTERRUPT
3. CONTROL_POWER
\`\`\`

### UTILITY

\`\`\`text
1. QI_COST_PERCENT
2. PRECISION
3. PROPAGATION
\`\`\`

---

# 3. Resumen Metal aprobado

| Relación | Identidad |
|---|---|
| Metal → Fuego | concentración / ignición |
| Metal → Agua | canalización / dirección |
| Metal → Tierra | anclaje / refuerzo |
| Metal → Viento | trayectoria / precisión |


---

# 4. AGUA como origen — APROBADO

Agua representa transformación, adaptación, erosión, templado y difusión.

## 4.1 AGUA → FUEGO · Vapor Súbito

**Identidad:** Agua entra en contacto con Fuego y provoca transformación brusca, choque térmico, expansión y liberación secundaria.

### OFFENSIVE

\`\`\`text
1. DAMAGE_PORTION
2. PROPAGATION
3. INTENSITY
4. AFFLICTION_APPLICATION
5. DIRECT_DAMAGE
\`\`\`

\`DAMAGE_PORTION\` permite crear una porción secundaria compatible sin convertir un porcentaje concreto en la definición universal de la relación.

### DEFENSIVE

\`\`\`text
1. REACTIVE_RESPONSE
2. ABSORPTION_RESTORE
3. INTERNAL_RESOURCE
4. FORTIFICATION
\`\`\`

### CONTROL

\`\`\`text
1. INTERRUPT
2. CONTROL_POWER
3. ACTION_DENIAL
4. AFFLICTION_APPLICATION
\`\`\`

### UTILITY

\`\`\`text
1. PROPAGATION
2. ZONE_DURATION
3. INTERNAL_RESOURCE
4. AFFLICTION_APPLICATION
\`\`\`

---

## 4.2 AGUA → METAL · Temple de Agua

**Identidad:** Agua enfría y templa Metal, fijando su forma y mejorando estabilidad y calidad de ejecución.

### OFFENSIVE

\`\`\`text
1. CRIT_DAMAGE
2. CRIT_CHANCE
3. PRECISION
4. DIRECT_DAMAGE
\`\`\`

### DEFENSIVE

\`\`\`text
1. FORTIFICATION
2. DEF_GRANTED
3. ABSORPTION
4. DEFENSIVE_DURATION
5. TENACITY_GRANTED
\`\`\`

### CONTROL

\`\`\`text
1. CONTROL_DURATION
2. CONTROL_POWER
3. DEBUFF_DURATION
\`\`\`

### UTILITY

\`\`\`text
1. FORTIFICATION
2. DEFENSIVE_DURATION
3. STACKABLE_STATE
4. INTERNAL_RESOURCE
\`\`\`

---

## 4.3 AGUA → TIERRA · Erosión / Sedimentación

**Identidad:** ofensivamente Agua erosiona Tierra; defensivamente la sedimenta y cohesiona.

### OFFENSIVE

\`\`\`text
1. DEF_SHRED
2. EVASION_DEBUFF
3. DEBUFF_DURATION
4. CONTROL_POWER
\`\`\`

### DEFENSIVE

\`\`\`text
1. FORTIFICATION
2. DEFENSIVE_DURATION
3. STACKABLE_STATE
4. ABSORPTION
5. TENACITY_GRANTED
\`\`\`

### CONTROL

\`\`\`text
1. EVASION_DEBUFF
2. CONTROL_POWER
3. DEBUFF_DURATION
4. ACTION_DENIAL
\`\`\`

### UTILITY

\`\`\`text
1. ZONE_DURATION
2. STACKABLE_STATE
3. FORTIFICATION
4. DEBUFF_DURATION
\`\`\`

---

## 4.4 AGUA → VIENTO · Velo de Niebla

**Identidad:** Agua se dispersa dentro de Viento creando humedad, niebla, ocultación y difusión.

### OFFENSIVE

\`\`\`text
1. PRECISION_DEBUFF
2. PROPAGATION
3. DEBUFF_DURATION
4. AREA_EFFICIENCY
5. CONTROL_POWER
\`\`\`

No usa \`DIRECT_DAMAGE\` como fallback.

### DEFENSIVE

\`\`\`text
1. EVASION_GRANTED
2. REACTIVE_RESPONSE
3. DEFENSIVE_DURATION
4. ZONE_DURATION
\`\`\`

### CONTROL

\`\`\`text
1. PRECISION_DEBUFF
2. CONTROL_POWER
3. INTERRUPT
4. DEBUFF_DURATION
\`\`\`

### UTILITY

\`\`\`text
1. ZONE_DURATION
2. PROPAGATION
3. AREA_EFFICIENCY
4. REACTIVE_RESPONSE
\`\`\`

---

# 5. Resumen Agua aprobado

| Relación | Identidad |
|---|---|
| Agua → Fuego | transformación / liberación secundaria |
| Agua → Metal | templado / estabilidad |
| Agua → Tierra | erosión / sedimentación |
| Agua → Viento | difusión / ocultación |


---

# 6. TIERRA como origen — APROBADO

Tierra representa peso, contención, asentamiento, persistencia y materialización.

## 6.1 TIERRA → FUEGO · Corazón de Magma

**Identidad:** Tierra contiene el calor e impide que se disipe. La relación prioriza persistencia real cuando el receptor ya la expone; si no existe ningún canal persistente compatible, puede encapsular el calor como un disparador contenido.

### OFFENSIVE

Prioridad:

\`\`\`text
1. PERSISTENCE
2. DOT_DURATION
3. INTENSITY
4. DOT_POTENCY
5. AFFLICTION_APPLICATION
6. CONTAINED_TRIGGER
\`\`\`

Reglas:

- no existe fallback genérico de \`DIRECT_DAMAGE\`;
- si alguno de los hooks 1–5 está expuesto, se resuelve sobre el primero compatible;
- \`CONTAINED_TRIGGER\` sólo se usa cuando no existe una propiedad persistente más rica;
- un único Eco sigue produciendo una sola resolución primaria.

### Manifestación Fuego de CONTAINED_TRIGGER · Núcleo de Magma

Cuando una técnica ofensiva de Fuego compatible no expone DOT, zona ni otra persistencia aprovechable, \`Tierra→Fuego\` puede crear un estado temporal:

\`\`\`text
NÚCLEO_DE_MAGMA
family = CONTAINED_TRIGGER
element = FIRE
owner = target
source = actor
duration = temporal
unique_per_source_target = true
\`\`\`

El Núcleo:

- no es Quemadura;
- no es DOT;
- no causa daño por turno;
- no modifica retroactivamente el impacto que lo creó;
- espera una nueva interacción ofensiva de Fuego compatible;
- al detonarse se consume.

### Detonación

Una técnica posterior de Fuego que impacte al objetivo marcado puede detonar el Núcleo.

La detonación crea una porción/paquete secundario de Fuego con reglas propias y sin doble escalado.

Si la técnica detonadora es unitarget:
- la detonación afecta al objetivo marcado.

Si la técnica detonadora es AOE:
- la detonación completa se produce sobre el objetivo marcado;
- puede generar una onda secundaria reducida sobre los demás \`VALID_HOSTILE_COMBATANT\` ya incluidos en esa ejecución AOE;
- no añade nuevos objetivos fuera del conjunto válido;
- no incrementa el target cap porque el sistema AOE global no tiene target cap;
- la onda secundaria debe declararse mediante \`PROPAGATION\`/paquete secundario y no como una nueva selección arbitraria de blancos.

La magnitud, duración exacta y porcentaje de propagación quedan pendientes de benchmark.

### DEFENSIVE

\`\`\`text
1. INTERNAL_RESOURCE
2. FORTIFICATION
3. ABSORPTION
4. REACTIVE_RESPONSE
5. DEFENSIVE_DURATION
\`\`\`

### CONTROL

\`\`\`text
1. DEBUFF_DURATION
2. AFFLICTION_APPLICATION
3. CONTROL_DURATION
4. CONTROL_POWER
\`\`\`

### UTILITY

\`\`\`text
1. ZONE_DURATION
2. PERSISTENCE
3. INTERNAL_RESOURCE
4. DEFENSIVE_DURATION
\`\`\`



---

# Regla transversal de escalado de Concordancias — APROBADA 2026-09-28

Las Concordancias están diseñadas para sobrevivir a Arcos futuros y a órdenes de magnitud superiores.

Por tanto:

```text
PROHIBIDO COMO ESCALADO DE CONCORDANCIA:
+3 daño
+5 DEF
+5 Precisión
+10 Control
+2 Absorción
```

Forma correcta:

```text
daño_receptor × (1 + porcentaje_concordancia)
DEF_otorgada × (1 + porcentaje_concordancia)
Absorción_generada × (1 + porcentaje_concordancia)
Precisión_aportada_por_el_hook × (1 + porcentaje_concordancia)
potencia_de_Control_del_hook × (1 + porcentaje_concordancia)
```

La Concordancia escala **la magnitud que ya genera el receptor**, no inyecta una cantidad absoluta desligada de esa magnitud.

Ejemplo estructural:

```text
Placa Fundacional
primer impacto válido:
- la placa no se consume;
- la misma placa queda REFORZADA;

segundo impacto válido:
- su DEF propia se multiplica por un porcentaje de fortificación;
- luego la placa se consume.
```

No se define `+N DEF`.

Esto permite que una placa de Arco 1 y una equivalente de Arco futuro utilicen exactamente la misma Concordancia sin quedar obsoletas.

Las operaciones discretas siguen permitidas cuando expresan identidad y no escala numérica, por ejemplo:

- impedir un consumo una vez por activación;
- transformar un estado;
- habilitar detonación;
- cambiar propagación;
- crear un snapshot;
- consumir una marca.

Pero cualquier **aumento de magnitud** producido por la Concordancia debe ser porcentual/relativo.


## 6.2 TIERRA → METAL · Forja Asentada

**Identidad:** Tierra proporciona una base estable al Metal. El Metal se asienta, soporta presión y conserva mejor su estructura sin desviar su fuerza.

### OFFENSIVE

Prioridad:

\`\`\`text
1. CRIT_CHANCE
2. PRECISION
3. PERCENT_PENETRATION
4. FLAT_PENETRATION
\`\`\`

La Concordancia no concede puntos fijos. Cuando mejora una magnitud, la escala porcentualmente sobre el hook receptor expuesto.

Interpretación:

- \`CRIT_CHANCE\`: estabilidad para encontrar un punto decisivo;
- \`EXECUTION\`: sostener el golpe hasta completar una condición de ejecución;
- \`PRECISION\`: reducir dispersión de la trayectoria;
- Penetración queda por debajo porque la identidad principal no es afilar, sino asentar.

### DEFENSIVE

Prioridad:

\`\`\`text
1. FORTIFICATION
2. ABSORPTION
3. DEF_GRANTED
4. STACKABLE_STATE
5. TENACITY_GRANTED
\`\`\`

### Manifestación actual compatible · Placa Fundacional

Cuando una defensa de Metal basada en cargas/placas expone \`FORTIFICATION\`, Tierra→Metal puede crear una transformación estructural:

\`\`\`text
PLACA_FUNDACIONAL
scope = once_per_activation
\`\`\`

Comportamiento:

1. la primera Placa elegible protege un impacto válido con su potencia normal;
2. ese primer impacto **no consume** la Placa;
3. la Placa pasa a estado \`REFORZADA\`;
4. en el siguiente impacto válido, la DEF propia de esa Placa se multiplica por un **porcentaje de fortificación**;
5. después de resolver ese segundo impacto, la Placa se consume normalmente.

Reglas:

- el aumento de DEF nunca es un valor plano fijo;
- escala sobre la DEF propia de la Placa, incluidas mejoras futuras de la build;
- no puede reforzarse repetidamente;
- sólo una Placa por activación recibe esta transformación salvo contenido futuro explícito;
- no crea una Placa adicional: modifica el ciclo de consumo de una existente;
- el porcentaje exacto queda pendiente de benchmark.

Esto permite que la misma Concordancia siga siendo relevante en Arcos futuros aunque las magnitudes defensivas aumenten varios órdenes.

### CONTROL

\`\`\`text
1. CONTROL_DURATION
2. CONTROL_POWER
3. ACTION_DENIAL
4. DEBUFF_DURATION
\`\`\`

La identidad es anclar/fijar una estructura metálica de Control.

### UTILITY

\`\`\`text
1. FORTIFICATION
2. STACKABLE_STATE
3. DEFENSIVE_DURATION
4. INTERNAL_RESOURCE
\`\`\`


---

## Regla transversal — movilidad fuera del sistema

El juego no utiliza una estadística o capa de movilidad en combate.

Las Concordancias no pueden resolver sobre `MOBILITY_REDUCTION`.

Cuando una identidad elemental sugiera peso, lodo, anclaje, arrastre o dificultad de movimiento, debe expresarse mediante hooks reales del sistema, por ejemplo:

```text
EVASION_DEBUFF
CONTROL_POWER
ACTION_DENIAL
INTERRUPT
PRECISION_DEBUFF
DEBUFF_DURATION
```

según lo que la técnica realmente exponga.


## 6.3 TIERRA → AGUA · Cauce Represado

**Identidad:** Tierra contiene el flujo de Agua, evita su dispersión y fuerza a que la energía acuática permanezca dentro de un cauce o reserva.

### OFFENSIVE

Prioridad:

\`\`\`text
1. EVASION_DEBUFF
2. CONTROL_POWER
3. ACTION_DENIAL
4. DEBUFF_DURATION
\`\`\`

No existe hook de movilidad.

La relación no crea daño directo por fallback.

### CONTROL

\`\`\`text
1. CONTROL_POWER
2. ACTION_DENIAL
3. CONTROL_DURATION
4. EVASION_DEBUFF
\`\`\`

Tierra no crea un Control nuevo: refuerza porcentualmente un canal real ya expuesto por la técnica de Agua.

### DEFENSIVE

Prioridad:

\`\`\`text
1. INTERNAL_RESOURCE
2. ABSORPTION_RESTORE
3. ABSORPTION
4. DEFENSIVE_DURATION
5. FORTIFICATION
\`\`\`

### Manifestación actual compatible · Embalse

Una defensa acuática que exponga restauración de Absorción puede convertir parte de la restauración excedente en un recurso temporal contenido:

\`\`\`text
EMBALSE
class = INTERNAL_RESOURCE
source = defensive_effect_instance
scope = activation
\`\`\`

Comportamiento:

1. una restauración de Absorción se calcula normalmente;
2. la parte que cabe entra en el pool;
3. el exceso que normalmente se perdería puede almacenarse en \`EMBALSE\`;
4. cuando el mismo pool pierde Absorción y vuelve a tener espacio, Embalse puede liberar automáticamente parte de su reserva;
5. la liberación restaura el mismo pool, no crea una barrera distinta;
6. no cura Vida;
7. no cuenta como DEF;
8. no genera Robo de Vida ni reacciones ofensivas;
9. la capacidad de Embalse se escala porcentualmente respecto de la magnitud propia de la defensa/reflujo, nunca mediante un valor plano fijo;
10. Embalse desaparece al terminar la activación o al invalidarse el efecto defensivo del que depende.

El porcentaje de almacenamiento y de liberación queda pendiente de benchmark.

### UTILITY

\`\`\`text
1. INTERNAL_RESOURCE
2. ZONE_DURATION
3. DEBUFF_DURATION
4. ABSORPTION_RESTORE
5. CONTROL_LOCKOUT
\`\`\`



## 6.4 TIERRA → VIENTO · Tormenta de Polvo

**Identidad:** Tierra da cuerpo al Viento. La corriente transporta materia, ocupa espacio e interfiere con el entorno.

### OFFENSIVE

Prioridad:

\`\`\`text
1. AREA_EFFICIENCY
2. PROPAGATION
3. PRECISION_DEBUFF
4. ZONE_DURATION
5. DEBUFF_DURATION
\`\`\`

No existe fallback genérico de \`DIRECT_DAMAGE\`.

La relación no aumenta el número de objetivos de una AOE.

### CONTROL

\`\`\`text
1. PRECISION_DEBUFF
2. CONTROL_POWER
3. ACTION_DENIAL
4. INTERRUPT
5. DEBUFF_DURATION
\`\`\`

### DEFENSIVE

\`\`\`text
1. DEFENSIVE_DURATION
2. EVASION_GRANTED
3. REACTIVE_RESPONSE
4. ZONE_DURATION
\`\`\`

La prioridad por duración evita duplicar la identidad de Fuego→Viento, que representa aceleración/magnitud dinámica.

### UTILITY

\`\`\`text
1. ZONE_DURATION
2. PROPAGATION
3. AREA_EFFICIENCY
4. DEBUFF_DURATION
5. REACTIVE_RESPONSE
\`\`\`

### Manifestación compatible · Nube Residual

Una técnica de Viento que exponga \`ZONE\` o \`ZONE_DURATION\` puede dejar después de su ejecución una zona temporal de partículas suspendidas.

La zona:

- no añade objetivos al impacto original;
- no introduce una estadística de movilidad;
- puede aplicar únicamente efectos reales declarados por su contenido, como \`PRECISION_DEBUFF\`;
- su duración y magnitud escalan porcentualmente sobre los hooks receptores;
- no crea daño automático si la técnica no expone un canal de daño apropiado.

---

# 7. Resumen Tierra aprobado

| Relación | Identidad |
|---|---|
| Tierra → Fuego | contención / persistencia / Núcleo de Magma |
| Tierra → Metal | asentamiento / fortificación / Placa Fundacional |
| Tierra → Agua | contención de flujo / Embalse |
| Tierra → Viento | materialización / interferencia / Nube Residual |


---

# 8. VIENTO como origen — APROBADO

Viento representa impulso, aceleración, circulación y ligereza.

No existe una estadística de movilidad; Viento actúa sobre hooks reales del sistema.

## 8.1 VIENTO → FUEGO · Avivamiento

**Identidad:** Viento alimenta la llama y acelera su manifestación inmediata.

### OFFENSIVE

\`\`\`text
1. INTENSITY
2. DIRECT_DAMAGE
3. CRIT_DAMAGE
4. PROPAGATION
\`\`\`

\`DIRECT_DAMAGE\` es válido aquí porque avivar una llama directa pertenece a la identidad de la relación.

Toda mejora de magnitud es porcentual respecto del hook receptor.

### DEFENSIVE

\`\`\`text
1. ABSORPTION
2. INTERNAL_RESOURCE
3. REACTIVE_RESPONSE
4. DEFENSIVE_DURATION
\`\`\`

### CONTROL

\`\`\`text
1. INTERRUPT
2. CONTROL_POWER
3. ACTION_DENIAL
4. DEBUFF_DURATION
\`\`\`

### UTILITY

\`\`\`text
1. INTERNAL_RESOURCE
2. PROPAGATION
3. ZONE_DURATION
\`\`\`

---

## 8.2 VIENTO → METAL · Filo Propulsado

**Identidad:** Viento impulsa al Metal y mejora la trayectoria/ejecución de una propiedad que el receptor ya posee.

### OFFENSIVE

\`\`\`text
1. PRECISION
2. PERCENT_PENETRATION
3. CRIT_CHANCE
4. FLAT_PENETRATION
\`\`\`

Una Concordancia que modifique \`PRECISION\` escala la Precisión aportada por el hook receptor, no toda la Precisión total del actor.

### DEFENSIVE

\`\`\`text
1. QI_COST_PERCENT
2. REACTIVE_RESPONSE
3. DEFENSIVE_DURATION
4. FORTIFICATION
\`\`\`

### CONTROL

\`\`\`text
1. INTERRUPT
2. PRECISION
3. CONTROL_POWER
4. ACTION_DENIAL
\`\`\`

### UTILITY

\`\`\`text
1. QI_COST_PERCENT
2. PRECISION
3. PROPAGATION
\`\`\`

---

## 8.3 VIENTO → AGUA · Corriente Ligera

**Identidad:** Viento facilita la circulación del Agua, reduce resistencia y permite que el flujo ocurra con mayor eficiencia.

### OFFENSIVE

\`\`\`text
1. QI_COST_PERCENT
2. PROPAGATION
3. CONTROL_POWER
4. PRECISION
\`\`\`

### DEFENSIVE

\`\`\`text
1. QI_COST_PERCENT
2. ABSORPTION_RESTORE
3. DEFENSIVE_DURATION
4. INTERNAL_RESOURCE
\`\`\`

### CONTROL

\`\`\`text
1. QI_COST_PERCENT
2. CONTROL_POWER
3. INTERRUPT
4. ACTION_DENIAL
\`\`\`

### UTILITY

\`\`\`text
1. QI_COST_PERCENT
2. PROPAGATION
3. INTERNAL_RESOURCE
\`\`\`

La reducción de coste es porcentual; no resta una cantidad fija de Qi.

---

## 8.4 VIENTO → TIERRA · Golpe del Vendaval

**Identidad:** Viento comunica impulso a la masa de Tierra.

### OFFENSIVE

\`\`\`text
1. CONTROL_POWER
2. DIRECT_DAMAGE
3. PRECISION
4. AREA_EFFICIENCY
\`\`\`

La relación prioriza impacto/control cuando existe. Si no existe, puede aumentar porcentualmente la magnitud directa del golpe.

### DEFENSIVE

\`\`\`text
1. TENACITY_GRANTED
2. FORTIFICATION
3. DEF_GRANTED
4. REACTIVE_RESPONSE
\`\`\`

Cuando modifica \`TENACITY_GRANTED\`, escala porcentualmente la Tenacidad otorgada por el estado/técnica receptora, no añade puntos fijos.

### CONTROL

\`\`\`text
1. CONTROL_POWER
2. ACTION_DENIAL
3. INTERRUPT
4. EVASION_DEBUFF
5. DEBUFF_DURATION
\`\`\`

### UTILITY

\`\`\`text
1. TENACITY_GRANTED
2. FORTIFICATION
3. INTERNAL_RESOURCE
4. AREA_EFFICIENCY
\`\`\`

---

# 9. Matriz conceptual completa — 20/20 APROBADAS

| Origen ↓ / Destino → | Fuego | Metal | Agua | Tierra | Viento |
|---|---|---|---|---|---|
| Fuego | — | Forja Ardiente | Presurización | Cimiento Cocido | Corriente Ascendente |
| Metal | Chispa de Ignición | — | Cauce Tallado | Anclaje de Hierro | Filo en la Corriente |
| Agua | Vapor Súbito | Temple de Agua | — | Erosión / Sedimentación | Velo de Niebla |
| Tierra | Corazón de Magma | Forja Asentada | Cauce Represado | — | Tormenta de Polvo |
| Viento | Avivamiento | Filo Propulsado | Corriente Ligera | Golpe del Vendaval | — |

## 9.1 Estado

Las 20 relaciones dirigidas ya tienen:

- identidad global;
- prioridades por rol/contexto;
- hooks compatibles;
- ausencia de fallback universal;
- escalado relativo/porcentual;
- reglas de interacción con hooks;
- tratamiento explícito cuando no existe receptor compatible.

A partir de este punto no se deben añadir números de balance a la matriz conceptual.

El siguiente trabajo consiste en:

1. mapear cada técnica diseñada contra sus \`mechanical_hooks\`;
2. declarar sus \`concordance_hooks\`;
3. verificar qué relaciones puede recibir realmente cada técnica;
4. detectar relaciones sin cobertura actual;
5. diseñar Viento sin romper la matriz global;
6. recién después asignar magnitudes y hacer benchmark.


---

# 10. Descriptores estructurales canónicos

Regla de precedencia:

> Si una combinación `relation_id + receiver_hook + context` tiene una manifestación estructural registrada, esa manifestación constituye la **única resolución primaria** del Eco. No se aplica además un escalado SCALAR genérico sobre el mismo hook.

Los porcentajes exactos continúan pendientes de benchmark.

## 10.1 Tierra→Fuego + CONTAINED_TRIGGER · Núcleo de Magma

```text
manifestation_id = NUCLEO_DE_MAGMA
relation_id = EARTH_TO_FIRE
receiver_hook = CONTAINED_TRIGGER
hook_class = STRUCTURAL
activation_context = OFFENSIVE
owner = TARGET
source = ACTOR
target_scope = CONNECTED_TARGETS
duration_unit = SOURCE_TURNS
duration_value = PENDING_BENCHMARK
frequency = once_per_target_per_action
scale_rule = RELATIVE_TO_CREATOR_HOOK
scale_target = stored_magnitude
consume_rule = CONSUME_ON_VALID_DETONATION
cleanup_rule = EXPIRE_OR_COMBAT_END
detonator_source_must_match = true
```

Creación:

- sólo se crea sobre un objetivo cuyo impacto conectó;
- si el ataque creador falla contra un objetivo, ese objetivo no recibe Núcleo;
- en una AOE, un único descriptor puede aplicar un Núcleo a cada objetivo conectado del conjunto congelado;
- crear varios Núcleos por una AOE no implica varias resoluciones de Eco: sigue existiendo una única resolución primaria por ActionContext;
- `stored_magnitude` toma como base una magnitud local del hook creador declarada por contenido y queda snapshot;
- la proporción exacta de almacenamiento queda pendiente de benchmark.

Detonación:

```text
trigger = ON_VALID_DIRECT_IMPACT
condition:
- source == manifestation.source
- incoming element == FIRE
- offensive interaction compatible
```

El paquete de detonación usa:

```text
damage_source_type = SECONDARY_REACTIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, FIRE, CONCORDANCE, CONTAINED_TRIGGER]
can_crit = false
can_use_def = true
can_use_penetration = false
can_use_absorption = true
can_trigger_on_hit = false
can_trigger_on_damage = false
can_trigger_lifesteal = false
can_trigger_reflect = false
can_trigger_retaliation = false
aoe_single_target_scalar_applies = false
```

La detonación no vuelve a escalar `stored_magnitude` con pools ofensivos del detonador.

Si el detonador es AOE:

- el objetivo marcado recibe la detonación completa;
- una onda secundaria sólo puede reutilizar los demás objetivos del `target_set` ya congelado;
- la onda usa PROPAGATION declarada por el descriptor;
- no descubre enemigos nuevos.

## 10.2 Tierra→Metal + FORTIFICATION · Placa Fundacional

```text
manifestation_id = PLACA_FUNDACIONAL
relation_id = EARTH_TO_METAL
receiver_hook = FORTIFICATION
hook_class = STRUCTURAL
activation_context = DEFENSIVE
owner = ACTOR
target_scope = SELF
frequency = once_per_activation
scale_rule = RELATIVE_TO_RECEIVER
scale_target = plate_def_value
snapshot_fields = [plate_def_value, concordance_scale]
cleanup_rule = ACTIVATION_END
```

Ciclo:

```text
NORMAL
→ primer ON_VALID_DIRECT_IMPACT_RECEIVED
→ protege con plate_def_value
→ NO consume la Placa
→ estado REFORZADA

REFORZADA
→ siguiente ON_VALID_DIRECT_IMPACT_RECEIVED
→ protege con plate_def_value × (1 + concordance_scale)
→ termina la transformación Fundacional
→ la Placa vuelve a las reglas ordinarias de consumo
```

Reglas:

- Evasión y DOT no cuentan como impacto válido;
- un impacto directo válido cuenta aunque DEF reduzca su daño a 0;
- al segundo impacto, el modificador Fundacional termina siempre;
- si otra regla legítima de Armadura evita consumir la Placa en ese segundo impacto, la Placa puede sobrevivir, pero vuelve a estado NORMAL y no conserva el refuerzo;
- no puede entrar otra vez en REFORZADA durante la misma activación por esta manifestación;
- no crea una carga extra.

## 10.3 Tierra→Agua + ABSORPTION_RESTORE · Embalse

```text
manifestation_id = EMBALSE
relation_id = EARTH_TO_WATER
receiver_hook = ABSORPTION_RESTORE
hook_class = STRUCTURAL
activation_context = DEFENSIVE
owner = ACTOR
source = defensive_effect_instance
target_scope = SELF
resource_family = EMBALSE
scale_rule = RELATIVE_TO_RECEIVER
scale_target = overflow_storage_capacity
frequency = per_restore_event
cleanup_rule = SOURCE_EFFECT_INSTANCE_END
```

Captura:

```text
ON_ABSORPTION_RESTORE_RESOLVED
if overflow_restore > 0
→ STORE_RESOURCE(EMBALSE, amount derived from overflow_restore)
```

Liberación:

```text
ON_ABSORPTION_LOSS_RESOLVED
if same pool_instance_id remains valid
and reserve_after < reserve_max
and EMBALSE > 0
→ RESTORE_ABSORPTION from EMBALSE
```

Reglas:

- no es una segunda barrera;
- no cura Vida;
- no retroabsorbe el paquete que produjo la pérdida;
- no genera triggers ofensivos;
- capacidad y liberación escalan relativamente;
- si el pool/effect instance se rompe y queda invalidado, Embalse se limpia;
- una reconstrucción crea nueva instancia y no hereda Embalse de la instancia rota salvo futura regla explícita.

## 10.4 Tierra→Viento + ZONE/ZONE_DURATION · Nube Residual

```text
manifestation_id = NUBE_RESIDUAL
relation_id = EARTH_TO_WIND
receiver_hook = ZONE | ZONE_DURATION
hook_class = STRUCTURAL/PARAMETRIC
activation_context = OFFENSIVE | UTILITY
owner = ROOM
source = ACTOR
target_scope = FROZEN_ACTION_TARGET_SET
duration_unit = SOURCE_TURNS
duration_value = PENDING_BENCHMARK
scale_rule = RELATIVE_TO_RECEIVER
scale_target = zone_duration | declared_zone_effect_magnitude
cleanup_rule = DURATION_END_OR_COMBAT_END
```

Reglas:

- no requiere posiciones internas;
- pertenencia significa presencia en el mismo espacio de combate/sala;
- por defecto sólo puede afectar a entidades del `target_set` congelado de la acción creadora;
- enemigos que entren después no se añaden automáticamente;
- no introduce movilidad;
- sólo aplica efectos explícitos del descriptor, por ejemplo `PRECISION_DEBUFF`;
- no causa daño si no existe un canal de daño declarado;
- si la técnica expone un hook compatible de mayor prioridad que ZONE/ZONE_DURATION, ese hook gana y Nube Residual no se crea.

---

# 11. Regla AOE transversal para Concordancias

Para cualquier Concordancia aplicada a una AOE:

1. el Eco se resuelve una vez por ActionContext;
2. el descriptor resultante puede operar `per_target`, pero no vuelve a resolver la relación;
3. `PROPAGATION` no equivale a AOE;
4. `AREA_EFFICIENCY` no equivale a PROPAGATION;
5. ningún hook descubre blancos fuera del conjunto congelado salvo futura excepción global explícita;
6. un debuff escalado por Concordancia se aplica con la misma regla a cada objetivo al que la técnica ya habría aplicado ese debuff;
7. efectos `once_per_action` siguen siendo uno por ejecución, no por objetivo.
