# Matriz experimental — Evolución de Supervivencia v0.1

**Estado:** EXPERIMENTAL / NO CANÓNICO.

## Principio

La primera evolución enseña a **sobrevivir**, pero no todos los monstruos sobreviven de la misma manera.

```text
anatomía + comportamiento + elemento + rol
→ familia defensiva coherente
→ habilidad propia de especie
→ Monster Combat AI existente decide cuándo usarla
```

No se aumenta HP, daño ni ataque en Evolución I.

## Cuatro familias

### EVADE_NEXT — esquiva
Evita que el golpe conecte elevando temporalmente la esquiva.

Uso natural: criaturas pequeñas, aéreas, serpentinas, acuáticas rápidas u oportunistas.

### DEFENSE_UP — defensa plana
Aumenta temporalmente `defensa`. En ver74 eso eleva el umbral necesario para impactar; **no resta daño después de acertar**.

Uso natural: postura, parada, placas articuladas, guardia técnica.

### ABSORB_RESERVE — absorción
Usa el modelo de reserva que ya existe en ver74: tope absorbible por golpe + reserva total.

Uso natural: caparazón, masa espiritual, coral, niebla condensada, cuerpos que pueden recibir y consumir impacto.

### MITIGATE_NEXT — mitigación
El golpe entra, pero el siguiente impacto pierde un porcentaje de daño.

Uso natural: disipación, amortiguación, cuerpo incorpóreo, piel que distribuye impacto.

## XP provisional

- común: `6 XP`;
- único: `4 XP`;
- encuentro con al menos una ronda: `+1 XP`;
- si llegó a HP bajo **o** sufrió un golpe fuerte observado: `+1 XP`;
- máximo: `2 XP` por encuentro.

Resultado aproximado:

- común: 3 encuentros duros o 6 ordinarios;
- único: 2 encuentros duros o 4 ordinarios.

## Matriz por monstruo

| Monstruo | Cognición base → E1 | Defensa aprendida | Familia | Efecto candidato | Por qué encaja |
|---|---|---|---|---|---|
| Rata de qi | INSTINTIVO → REACTIVO_1 | **Reflejo de Madriguera** | ESQUIVA | +25 esquiva · 1 acción | sobrevive huyendo del ángulo del golpe, no bloqueándolo |
| Serpiente de qi | REACTIVO_1 → CAZADOR_2 | **Muda del Cauce** | ESQUIVA | +20 esquiva · 1 acción | cuerpo flexible y afinidad agua; cambia la línea del ataque |
| Lobo espiritual | CAZADOR_2 → TACTICO_3 | **Paso de la Cola Vigilante** | DEFENSA | +3 defensa · 1 acción | sus tres colas ya vigilan direcciones; aprende una postura de cobertura |
| Eco del Caído | REACTIVO_1 → CAZADOR_2 | **Guardia del Último Ensayo** | MITIGACIÓN | −40% próximo golpe | memoria de entrenamiento: recibe mejor el impacto, no crea armadura |
| Pez lunar | CAZADOR_2 → TACTICO_3 | **Giro de Corriente Ciega** | ESQUIVA | +25 esquiva · 1 acción | caza por pulsos de qi y puede salir de la trayectoria antes del contacto |
| Sombra ahogada | TACTICO_3 → MASTER_4 | **Disolverse en Marea** | MITIGACIÓN | −40% próximo golpe | cuerpo de sombra/agua que dispersa parte del impacto |
| Centinela de plumas | REACTIVO_1 → CAZADOR_2 | **Cierre de Plumas Pétreas** | DEFENSA | +5 defensa · 1 acción | placas/pétalos pétreos forman una guardia física, sin absorber energía |
| Devorador de niebla | TACTICO_3 → MASTER_4 | **Cuerpo de Bruma Replegada** | ABSORCIÓN | 4 por golpe · reserva 8 | cuerpo condensado consume parte del golpe hasta dispersarse |
| Avispa de jade | INSTINTIVO → REACTIVO_1 | **Quiebro de Jade** | ESQUIVA | +25 esquiva · 1 acción | criatura diminuta y aérea; bloquear sería poco coherente |
| Macaco ladrón | CAZADOR_2 → TACTICO_3 | **Salto del Ladrón** | ESQUIVA | +20 esquiva · 1 acción | oportunista móvil que ya roba y se reposiciona |
| Sapo de ceniza | INSTINTIVO → REACTIVO_1 | **Piel de Brasa Muerta** | MITIGACIÓN | −35% próximo golpe | la piel caliente amortigua el impacto sin volverlo difícil de acertar |
| Sapo Caldera | REACTIVO_1 → CAZADOR_2 | **Cierre de las Tres Gargantas** | ABSORCIÓN | 4 por golpe · reserva 8 | masa corporal y cámaras internas permiten “tragarse” parte del impacto |
| Escarabajo de hierro | INSTINTIVO → REACTIVO_1 | **Cierre de Caparazón** | ABSORCIÓN | 4 por golpe · reserva 8 | su identidad ya es el caparazón metálico; la reserva representa desgaste |
| Rey Escarabajo | CAZADOR_2 → TACTICO_3 | **Diagrama de Placas** | ABSORCIÓN | 5 por golpe · reserva 10 | versión avanzada del caparazón, coherente con su diagrama defensivo canónico |
| Anguila estelar | REACTIVO_1 → CAZADOR_2 | **Desliz de Meridiano** | ESQUIVA | +25 esquiva · 1 acción | cuerpo lineal y acuático; desvía su trayectoria siguiendo el qi |
| Guardián de coral | TACTICO_3 → MASTER_4 | **Arrecife Replegado** | ABSORCIÓN | 5 por golpe · reserva 10 | el coral se erosiona por capas y puede consumir varios impactos pequeños |
| Halcón de tormenta | CAZADOR_2 → TACTICO_3 | **Ascenso Contraviento** | ESQUIVA | +30 esquiva · 1 acción | usa altura y corriente para abandonar la línea del golpe |
| Mantis de nube | MASTER_4 → MASTER_4 | **Guardia de las Dos Hojas** | DEFENSA | +5 defensa · 1 acción | precisión extrema: no huye, intercepta/paraliza la línea del ataque |

Todas consumen la acción del monstruo y proponen **2 rondas de cooldown**.

## Distribución

```text
ESQUIVA       7
DEFENSA       3
MITIGACIÓN    3
ABSORCIÓN     5
TOTAL        18
```

La distribución no busca igualdad numérica sino coherencia con las criaturas existentes.

## Política de decisión

La elección de defender sigue calibrada contra la preferencia ofensiva original.

```text
sano                         → 0% defensa
HP bajo                      → ~50% defensa
golpe fuerte, HP sano        → 0% defensa
HP bajo + golpe fuerte       → supervivencia prioritaria
defensa en cooldown          → atacar
ronda técnica canónica       → CADENCE_COMPAT manda
```

## Balance contra arsenal real

Los escenarios sintéticos usados durante el primer smoke test ya **no son evidencia de balance**.

La referencia vigente es:

`adaptive/ANALISIS_ARSENAL_JUGADOR_DEFENSAS_E1_v0.1.md`

y su benchmark:

`benchmark/player-arsenal-vs-survival-v0.1.mjs`

El benchmark usa directamente ver74 y cruza:

```text
LianQi IV
× Palma / Filo / Látigo
× ramas 1–2
× equipo actual
× afinidad
× crítico
× relación elemental
× los 18 monstruos
```

Conclusión provisional:

- esquiva y defensa conservan counters de precisión reales;
- mitigación 35–40% queda dentro de la escala de DEFENDER del jugador;
- absorción debe compararse por reserva total / HP del monstruo;
- el Escarabajo de Hierro (reserva 8 sobre 21 HP) es el caso que requiere más vigilancia;
- los valores quedaron fijados como **candidato final experimental** tras medir combate completo, uso de defensa y coste de oportunidad de perder el ataque.

## Frontera pendiente

Esta matriz sólo define y balancea intents.

```text
Monster Combat AI
→ decide SURVIVAL_EVOLUTION_1
→ [GAP] executor defensivo de monstruos
→ aplicar EVADE / DEFENSE / ABSORB / MITIGATE
```

El executor todavía no existe y no se simula fingiendo otra acción canónica.
