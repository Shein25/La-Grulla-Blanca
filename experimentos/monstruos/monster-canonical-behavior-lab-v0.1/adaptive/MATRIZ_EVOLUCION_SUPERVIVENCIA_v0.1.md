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
| Eco del Caído | REACTIVO_1 → CAZADOR_2 | **Guardia del Último Ensayo** | MITIGACIÓN | −35% próximo golpe | memoria de entrenamiento: recibe mejor el impacto, no crea armadura |
| Pez lunar | CAZADOR_2 → TACTICO_3 | **Giro de Corriente Ciega** | ESQUIVA | +20 esquiva · 1 acción | caza por pulsos de qi y puede salir de la trayectoria antes del contacto |
| Sombra ahogada | TACTICO_3 → MASTER_4 | **Disolverse en Marea** | MITIGACIÓN | −35% próximo golpe | cuerpo de sombra/agua que dispersa parte del impacto |
| Centinela de plumas | REACTIVO_1 → CAZADOR_2 | **Cierre de Plumas Pétreas** | DEFENSA | +4 defensa · 1 acción | placas/pétalos pétreos forman una guardia física, sin absorber energía |
| Devorador de niebla | TACTICO_3 → MASTER_4 | **Cuerpo de Bruma Replegada** | ABSORCIÓN | 3 por golpe · reserva 6 | cuerpo condensado consume parte del golpe hasta dispersarse |
| Avispa de jade | INSTINTIVO → REACTIVO_1 | **Quiebro de Jade** | ESQUIVA | +25 esquiva · 1 acción | criatura diminuta y aérea; bloquear sería poco coherente |
| Macaco ladrón | CAZADOR_2 → TACTICO_3 | **Salto del Ladrón** | ESQUIVA | +20 esquiva · 1 acción | oportunista móvil que ya roba y se reposiciona |
| Sapo de ceniza | INSTINTIVO → REACTIVO_1 | **Piel de Brasa Muerta** | MITIGACIÓN | −30% próximo golpe | la piel caliente amortigua el impacto sin volverlo difícil de acertar |
| Sapo Caldera | REACTIVO_1 → CAZADOR_2 | **Cierre de las Tres Gargantas** | ABSORCIÓN | 4 por golpe · reserva 8 | masa corporal y cámaras internas permiten “tragarse” parte del impacto |
| Escarabajo de hierro | INSTINTIVO → REACTIVO_1 | **Cierre de Caparazón** | ABSORCIÓN | 4 por golpe · reserva 8 | su identidad ya es el caparazón metálico; la reserva representa desgaste |
| Rey Escarabajo | CAZADOR_2 → TACTICO_3 | **Diagrama de Placas** | ABSORCIÓN | 5 por golpe · reserva 10 | versión avanzada del caparazón, coherente con su diagrama defensivo canónico |
| Anguila estelar | REACTIVO_1 → CAZADOR_2 | **Desliz de Meridiano** | ESQUIVA | +20 esquiva · 1 acción | cuerpo lineal y acuático; desvía su trayectoria siguiendo el qi |
| Guardián de coral | TACTICO_3 → MASTER_4 | **Arrecife Replegado** | ABSORCIÓN | 5 por golpe · reserva 10 | el coral se erosiona por capas y puede consumir varios impactos pequeños |
| Halcón de tormenta | CAZADOR_2 → TACTICO_3 | **Ascenso Contraviento** | ESQUIVA | +25 esquiva · 1 acción | usa altura y corriente para abandonar la línea del golpe |
| Mantis de nube | MASTER_4 → MASTER_4 | **Guardia de las Dos Hojas** | DEFENSA | +4 defensa · 1 acción | precisión extrema: no huye, intercepta/paraliza la línea del ataque |

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

## Nichos mecánicos comprobados

Se usó la matemática de impacto actual de ver74.

Daño esperado evitado en el siguiente ataque, usando representantes:

| Escenario | Esquiva Rata +25 | Defensa Centinela +4 | Mitigación Eco 35% | Absorción Guardián 5 |
|---|---:|---:|---:|---:|
| golpe grande e impreciso | **5.00** | 4.00 | 4.55 | 3.25 |
| golpe medio equilibrado | 2.50 | 2.00 | 2.25 | **3.75** |
| golpe pequeño y preciso | 1.00 | 0.80 | 0.95 | **3.80** |
| golpe grande y preciso | 5.00 | 4.00 | **6.65** | 4.75 |

Lectura:

- **Esquiva:** mejor contra un impacto grande que todavía puede fallar.
- **Defensa plana:** función parecida a una esquiva moderada, pero representa postura/armadura/parada.
- **Absorción:** excelente contra impactos pequeños/medios que conectan con frecuencia.
- **Mitigación:** escala mejor frente a golpes grandes y precisos.

Además, en la fórmula actual:

```text
+20 esquiva ≈ +4 al umbral efectivo de impacto
+4 defensa  = +4 al umbral efectivo de impacto
```

Eso permite balance similar sin borrar la diferencia conceptual.

## Frontera pendiente

Esta matriz sólo define y balancea intents.

```text
Monster Combat AI
→ decide SURVIVAL_EVOLUTION_1
→ [GAP] executor defensivo de monstruos
→ aplicar EVADE / DEFENSE / ABSORB / MITIGATE
```

El executor todavía no existe y no se simula fingiendo otra acción canónica.
