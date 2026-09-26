# Análisis real del arsenal del jugador vs. Evolución I de monstruos v0.1

**Estado:** EXPERIMENTAL / NO CANÓNICO.

## Motivo

Este documento sustituye los escenarios de daño inventados usados como primera prueba de sanidad.

El balance de Evolución I debe partir de lo que el jugador **realmente puede hacer en ver74**.

Fuente de verdad:

`grulla-blanca_ver74.html`

Benchmark reproducible:

`benchmark/player-arsenal-vs-survival-v0.1.mjs`

Script:

```text
npm run benchmark:player-arsenal
```

## Alcance principal: Arco I

El objetivo de balance para Evolución I es el contenido jugable actual:

```text
LianQi IV
+ ramas 1 y 2
+ equipo de ataque disponible
+ afinidad de raíz
+ críticos
+ relación elemental
+ estados ligados al impacto
```

La rama 3 exige ZhuJi.

Las artes Tierra, AOE de rango Tierra y Definitivas también exigen ZhuJi.

Además:

```text
CULTIVO_REINOS.ZhuJi.jugable = false
```

Por eso ZhuJi se considera **stress test futuro**, no referencia para decidir cuánto debe defender una rata de Arco I.

## Ataque efectivo del jugador en LianQi IV

El personaje empieza con:

```text
ataque = 1 + raíz.ataque
```

y gana +1 al consagrar cada etapa hasta LianQi IV.

Raíces:

```text
agua   → ataque base LianQi IV 4
fuego  → 5
metal  → 6
```

Equipo actual puede sumar como máximo +2 simultáneo:

- arma con +1 ataque;
- Amuleto de Colmillo +1 ataque.

Benchmark de presión máxima razonable del Arco I:

```text
agua   6
fuego  7
metal  8
```

antes del bono de precisión propio de la rama.

## Artes ofensivas reales del Arco I

Con afinidad de raíz incluida (+1 daño):

| Arte | Daño base | Media directa con ramas 1–2 | Rango de tirada directa | Bono ATQ máximo | Mejor crítico | Coste afín |
|---|---|---:|---:|---:|---:|---:|
| Palma Ardiente | 2d6+2 | 10,0–12,5 | 5–19 | +7 | 19+ | 5–6 qi |
| Filo de Qi Metálico | 1d10+3 | 9,5–12,0 | 5–18 | +7 | 19+ | 5 qi |
| Látigo de Agua | 2d6 | 8,0–10,5 | 3–17 | +7 | 19+ | 5 qi |

Palma puede añadir además una quemadura de:

```text
1d3 × 2 rondas
media total = 4
```

si se elige esa rama y el golpe final sigue causando daño.

Con `qi_max = 110` en LianQi IV, el qi no impide usar repetidamente estas artes en un duelo normal de Arco I.

## Precisión: hallazgo importante

La fórmula real:

```js
roll + ataque >= defensa + evasionExtra
```

con:

```js
evasionExtra = round((esquiva - 5) / 5)
```

Por tanto:

```text
+20 esquiva ≈ +4 al umbral
+25 esquiva ≈ +5 al umbral
+4 defensa  = +4 al umbral
```

Pero las ramas del jugador pueden sumar +7 ataque ya en LianQi IV.

Resultado:

- ESQUIVA y DEFENSA tienen counters reales;
- una build de precisión puede reducirlas mucho o incluso anular su ventaja contra criaturas de defensa baja;
- los críticos 19–20 son además impactos automáticos bajo la función actual.

Esto es deseable: una defensa aprendida no debe ser una reducción garantizada contra cualquier build.

## Resultado frente a las defensas E1 actuales

El benchmark recorre:

```text
18 monstruos
× 3 artes raíz
× 9 combinaciones de ramas 1–2
= 486 cruces principales
```

con afinidad, precisión, crítico y elemento reales.

| Monstruo | Familia | Daño entrante medio | Evita medio | % del golpe evitado | Evitado / HP propio |
|---|---|---:|---:|---:|---:|
| Rata de qi | Esquiva +25 | 10,06 | 1,77 | 17,5% | 19,7% |
| Serpiente de qi | Esquiva +20 | 9,13 | 1,42 | 15,7% | 10,9% |
| Lobo espiritual | Defensa +3 | 9,81 | 1,06 | 10,9% | 5,9% |
| Eco del Caído | Mitigación 35% | 9,53 | 2,76 | 29,2% | 8,1% |
| Pez lunar | Esquiva +20 | 8,87 | 1,62 | 18,4% | 6,2% |
| Sombra ahogada | Mitigación 35% | 8,55 | 2,45 | 28,8% | 5,8% |
| Centinela | Defensa +4 | 9,36 | 2,12 | 23,0% | 4,4% |
| Devorador | Absorción 3 | 9,82 | 2,54 | 26,9% | 6,7% |
| Avispa de jade | Esquiva +25 | 10,48 | 2,13 | 20,6% | 21,3% |
| Macaco | Esquiva +20 | 9,81 | 1,53 | 15,7% | 9,0% |
| Sapo de ceniza | Mitigación 30% | 9,40 | 2,35 | 25,2% | 13,1% |
| Sapo Caldera | Absorción 4 | 9,05 | 3,39 | 38,6% | 10,0% |
| Escarabajo de hierro | Absorción 4 | 8,86 | 3,04 | 36,0% | 14,5% |
| Rey Escarabajo | Absorción 5 | 8,34 | 3,56 | 44,7% | 9,4% |
| Anguila estelar | Esquiva +20 | 8,55 | 1,76 | 20,9% | 5,9% |
| Guardián Coral | Absorción 5 | 7,71 | 3,78 | 49,9% | 7,3% |
| Halcón | Esquiva +25 | 9,37 | 2,67 | 29,0% | 8,6% |
| Mantis | Defensa +4 | 8,86 | 2,17 | 25,0% | 4,7% |

### Lectura correcta de la absorción

El porcentaje del golpe aislado puede engañar.

Ejemplo:

```text
Guardián Coral
absorbe ~49,9% del golpe medio protegido
pero ese ahorro representa ~7,3% de sus 52 HP
```

Mientras:

```text
Avispa
esquiva evita ~20,6% del golpe medio
pero equivale a ~21,3% de sus 10 HP
```

Por tanto el balance no debe igualar "% de golpe evitado" entre especies.

## Reserva completa de ABSORB_RESERVE

La absorción no expira por ronda en ver74: consume una reserva.

Capacidad máxima actual por activación:

```text
Devorador       6 / 38 HP = 15,8% HP
Sapo Caldera    8 / 34 HP = 23,5% HP
Escarabajo      8 / 21 HP = 38,1% HP
Rey Escarabajo 10 / 38 HP = 26,3% HP
Guardián Coral 10 / 52 HP = 19,2% HP
```

Este dato es más importante que el porcentaje del primer golpe.

El Escarabajo de Hierro es el caso que merece mayor vigilancia: su reserva completa representa una fracción grande de su HP.

## Ancla: defensas reales del jugador

No hace falta inventar una escala defensiva externa.

### Paso de Nube Ligera

Base:

```text
+15 esquiva
2 rondas
```

Con ramas 1–2 puede alcanzar:

```text
+32 esquiva durante 2 rondas
```

o aumentar duración hasta 4 rondas.

### Piel de Cobre

Base:

```text
absorbe 3 por golpe
reserva 6
```

Con ramas 1–2 puede alcanzar combinaciones de hasta:

```text
absorbe 10 por golpe / reserva 20
```

o:

```text
absorbe 7 por golpe / reserva 21
```

### DEFENDER

Sin técnica especial, el jugador ya obtiene:

```text
primer golpe  → 35–50% reducción
segundo golpe → 25–40% reducción
```

y la acción consume su turno.

Esto pone en contexto las defensas E1 de monstruos:

- +20/+25 esquiva por una acción es menor que una especialización alta de Paso;
- absorción 3–5 con reserva 6–10 está por debajo de Piel de Cobre especializada;
- mitigación 30–35% de un golpe está por debajo de la protección completa que puede ofrecer DEFENDER durante dos impactos.

## Conclusiones de balance

### No hay razón para bajar todas las defensas

El análisis real no confirma que todos los valores anteriores estuvieran altos.

La mayoría cae en un rango razonable cuando se considera:

- daño real;
- precisión;
- HP del monstruo;
- coste de gastar una acción defensiva;
- counters de build.

### ESQUIVA / DEFENSA

No necesitan nerf global.

La precisión del jugador ya es su counter natural.

En algunos cruces su ahorro cae a 0%.

### MITIGACIÓN

30–35% de un golpe se comporta de forma estable.

Además queda por debajo de la acción básica DEFENDER del jugador.

No hay evidencia actual para cambiarla.

### ABSORCIÓN

Debe evaluarse por **reserva / HP**, no sólo por "% del golpe".

Los valores 3/6 a 5/10 están dentro de la escala de Piel de Cobre, pero:

```text
Escarabajo de Hierro: reserva 8 = 38,1% de su HP
```

es el caso más agresivo y debe entrar en la siguiente simulación de combate completo antes de congelarse.

## Hallazgo de diseño: monstruos frágiles

Rata y Avispa pueden recibir golpes LianQi IV cuyo daño medio ronda o supera su HP total.

Si su IA sólo aprende:

```text
"estoy bajo de HP → defender"
```

pueden morir antes de tener oportunidad de aplicar lo aprendido.

Esto refuerza el concepto original de aprendizaje:

```text
encuentros repetidos
→ recuerda cómo abre el jugador
→ anticipa una técnica peligrosa
→ puede defender ANTES del golpe
```

No debe implementarse fingiendo una señal. Requiere que la persistencia adaptativa entregue una señal real de patrón aprendido.

## Lo que aún NO queda cerrado

Los valores E1 siguen siendo **candidatos**, no balance final.

Falta un benchmark de combate completo que incluya:

- cuándo se activa realmente la defensa;
- coste de perder el ataque del monstruo por defender;
- consumo completo de reservas de absorción;
- prohibición de refrescar una absorción mientras siga activa;
- duración real del duelo;
- frecuencia de reactivación tras cooldown.

Hasta cerrar eso, no se deben subir ni bajar números sólo por intuición.

## Stress test ZhuJi

Las artes de ZhuJi y Definitivas no son el objetivo del balance E1 del Arco I.

Se usarán después para responder otra pregunta:

> ¿Una criatura vieja sigue beneficiándose de lo aprendido sin impedir que el jugador de un reino superior la supere claramente?

Ese test debe preservar progresión, no igualar monstruos del Arco I con un cultivador ZhuJi.
