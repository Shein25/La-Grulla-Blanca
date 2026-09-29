# LAB — LianQi I NAKED · PHASE B presupuesto de Qi

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / PARCIAL / NO CANON**

## Objetivo

Explorar el presupuesto inicial de Qi sin adelantar todavía HP, TTK ni daño
enemigo.

Se barre:

- Qi máximo: 18 / 24 / 30 / 36 / 42;
- piso global de coste: 1 / 3 / 5 / 6;
- las cinco técnicas iniciales PROVISIONAL.

No existe regeneración pasiva universal.

## Regla CANON relevante

Agua:

```text
COSTE_QI_CALCULADO
= coste base × 0.90
```

El cálculo conserva decimales y sólo redondea al convertir el coste en Qi
realmente gastado.

Por tanto:

```text
Latigazo de Marea
7 × 0.90
= 6.3
ROUND_HALF_UP
= 6 Qi
```

## Resultado de costes iniciales

| Raíz | Técnica | Coste base | Tras rasgo | Coste final |
|---|---|---:|---:|---:|
| Fuego | Palma Ardiente | 6 | 6.0 | 6 |
| Metal | Destello de Plata | 6 | 6.0 | 6 |
| Agua | Latigazo de Marea | 7 | 6.3 | 6 |
| Tierra | Golpe de Montaña | 6 | 6.0 | 6 |
| Viento | Lanza que Parte Nubes | 6 | 6.0 | 6 |

En el loadout inicial NAKED, las cinco raíces terminan gastando **6 Qi por
técnica**.

## Hallazgo sobre Agua

El -10% de Agua no concede todavía una técnica extra respecto de las otras
raíces en su técnica inicial.

Su función actual es compensar que Latigazo de Marea posee coste base 7.

Esto no invalida el rasgo:

- se aplica a todas las técnicas;
- puede producir diferencias reales en técnicas futuras con otros costes;
- puede importar si el personaje aprende técnicas ajenas;
- seguirá interactuando con futuras reducciones compatibles.

Pero en el benchmark inicial raíz+técnica propia, la economía queda igualada.

## Barrido de Qi máximo

Como el coste efectivo actual es 6 para las cinco raíces:

| Qi máximo LAB | Técnicas completas desde lleno | Qi restante |
|---:|---:|---:|
| 18 | 3 | 0 |
| 24 | 4 | 0 |
| 30 | 5 | 0 |
| 36 | 6 | 0 |
| 42 | 7 | 0 |

El resultado es idéntico para las cinco raíces en este subtest.

## Piso global de coste

Se probaron:

`1 / 3 / 5 / 6`

Todos producen exactamente el mismo resultado en LianQi I inicial porque
ningún coste calculado cae por debajo de 6.

Conclusión:

> **PHASE B inicial no contiene información suficiente para identificar el
> valor correcto del piso global de coste.**

El piso debe seguir **PENDIENTE** y probarse más adelante contra:

- reducciones acumuladas;
- equipo;
- ramas;
- Concordancias de reducción de coste;
- injerto de Agua;
- técnicas de coste bajo.

No se debe elegir un piso arbitrario sólo para desbloquear el runner.

## Lectura de Qi máximo

Sin HP/TTK todavía no puede cerrarse un único Qi máximo.

El rango útil para el siguiente duelo es:

```text
24 Qi → 4 técnicas
30 Qi → 5 técnicas
36 Qi → 6 técnicas
```

18 Qi deja sólo tres técnicas y se conserva como control bajo.

42 Qi permite siete técnicas seguidas y se conserva como control alto.

### Banda principal propuesta para PHASE C

**24–30 Qi**.

Motivo experimental:

- hace que el recurso pueda agotarse dentro de un combate significativo;
- permite que el ataque básico de coste 0 tenga función real;
- evita decidir todavía que un jugador pueda encadenar 6–7 técnicas antes
  de usar fallback;
- podrá compararse directamente contra HP/TTK del enemigo de referencia.

Esto es una hipótesis LAB, no una promoción a PROVISIONAL.

## Runner

`experimentos/balance_nuevo/phase_b_qi_budget_lab.py`

## Estado de PHASE B

```text
costes efectivos iniciales
→ resueltos bajo reglas actuales

Qi máximo
→ banda LAB 24–30 para siguiente prueba

piso global de coste
→ PENDIENTE; no identificable con técnicas iniciales
```

PHASE B no se marca todavía PASS.

## Próximo paso

Construir el primer esqueleto de duelo sin fijar aún estadísticas enemigas
completas:

1. barrer HP de enemigo de referencia;
2. medir TTK esperado con técnicas y ataque básico;
3. cruzar HP con Qi 24 y 30;
4. observar con qué combinación el jugador normalmente empieza a necesitar el
   ataque básico sin convertir cada combate en una pelea de desgaste;
5. sólo después elegir Qi máximo PROVISIONAL.

