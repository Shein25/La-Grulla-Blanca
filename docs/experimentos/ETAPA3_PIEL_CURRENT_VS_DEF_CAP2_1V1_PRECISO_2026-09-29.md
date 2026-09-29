# ETAPA 3 — Piel CURRENT vs DEF_CAP2 · 1v1 preciso

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / NO PROMOCIÓN**

## Pregunta única

¿Reducir la DEF máxima de Piel de Cobre de 6 a 5 mediante `DEF_CAP2`
degrada demasiado su rendimiento contra un enemigo preciso 1v1?

No se testean todavía:

- grupos de 2;
- grupos de 3;
- Control enemigo;
- otras defensivas.

## Baseline

Se conserva la Etapa 1 salvo una sola variable:

```text
Precisión enemiga
90 → 100
```

El daño vuelve al baseline normal:

```text
2d4+1
```

Jugador Tierra:

- HP efectivo 33;
- Qi31 LAB;
- DEF1;
- EVA5;
- Piel como apertura;
- Golpe de Montaña narrow;
- Peso PROVISIONAL STACK_REFRESH.

Enemigo preciso LAB:

- HP28;
- PREC100;
- EVA20;
- DEF2;
- ataque `2d4+1`.

## Resultado principal

Simulación de 200.000 duelos:

| Métrica | CURRENT | DEF_CAP2 |
|---|---:|---:|
| Win rate | 94.70% | 93.87% |
| Turnos medios | 6.58 | 6.56 |
| HP restante medio | 57.76% | 54.93% |
| Usa ataque básico | 67.28% | 67.40% |
| Arraigo máximo medio | 2.81 | 2.81 |
| Impactos enemigos medios | 5.35 | 5.34 |
| Daño recibido medio | 14.05 | 15.00 |

Diferencias:

```text
Win rate:
DEF_CAP2 ≈ -0.83 pp

HP restante:
DEF_CAP2 ≈ -2.83 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 duelos:

- −0.853 pp;
- −0.818 pp;
- −0.792 pp;
- −0.810 pp.

Delta de HP restante:

- −2.81 pp;
- −2.78 pp;
- −2.77 pp;
- −2.79 pp.

La dirección del efecto es estable.

## Lectura

Subir Precisión enemiga de 90 a 100 aumenta el número de impactos recibidos,
pero no cambia cualitativamente la comparación entre las dos versiones de Piel.

DEF_CAP2:

- sigue manteniendo >93% de victoria;
- conserva prácticamente la misma duración;
- conserva el mismo patrón de Arraigo;
- no altera la frecuencia de fallback de forma material;
- reduce supervivencia de forma medible, pero contenida.

## Conclusión de Etapa 3

**PASS para continuar testeando DEF_CAP2.**

Esto todavía no aprueba DEF_CAP2.

Significa únicamente:

> contra un enemigo preciso 1v1, limitar la contribución máxima de DEF de
> Arraigo mantiene la función defensiva de Piel sin introducir una caída
> desproporcionada.

## Próxima etapa

**ETAPA 4 — CURRENT vs DEF_CAP2 contra 2 enemigos.**

No avanzar todavía a 3 enemigos.
