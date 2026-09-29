# ETAPA 1 — Piel CURRENT vs DEF_CAP2 · 1v1 común

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / NO PROMOCIÓN**

## Pregunta única

¿Reducir la DEF máxima de Piel de Cobre de 6 a 5 mediante `DEF_CAP2`
rompe su rendimiento normal en duelo 1v1?

No se testean todavía:

- enemigos pesados;
- enemigos precisos;
- grupos de 2;
- grupos de 3;
- Control enemigo;
- otras defensivas.

## Baseline

Jugador Tierra:

- HP base 30;
- +10% raíz Tierra → 33 HP;
- Qi31 LAB;
- DEF base1;
- EVA5;
- Golpe de Montaña narrow;
- Peso PROVISIONAL STACK_REFRESH.

Enemigo común LAB:

- HP28;
- PREC90;
- EVA20;
- DEF2;
- ataque 2d4+1.

Piel se usa como apertura.

## Variantes

### CURRENT

- +2 DEF inmediata;
- 1 Arraigo al activar;
- cada Arraigo añade +1 DEF;
- máximo 3;
- DEF total posible: 6;
- extensión al alcanzar 3 Arraigos conservada.

### DEF_CAP2

- +2 DEF inmediata;
- 1 Arraigo al activar;
- Arraigo1 → +1 DEF;
- Arraigo2 → +2 DEF acumulada;
- Arraigo3 → sigue +2 DEF acumulada;
- DEF total posible: 5;
- tercera carga conserva Tenacidad y extensión.

## Resultado principal

Simulación de 200.000 duelos:

| Métrica | CURRENT | DEF_CAP2 |
|---|---:|---:|
| Win rate | 96.21% | 95.60% |
| Turnos medios | 6.61 | 6.60 |
| HP restante medio | 60.68% | 58.39% |
| Usa ataque básico | 67.17% | 67.17% |
| Arraigo máximo medio | 2.72 | 2.72 |
| Impactos enemigos medios | 4.80 | 4.80 |
| Daño recibido medio | 13.05 | 13.82 |

Diferencia principal:

```text
Win rate:
DEF_CAP2 ≈ -0.61 pp

HP restante:
DEF_CAP2 ≈ -2.29 pp
```

## Repetición por semillas

Se repitió con cuatro semillas independientes de 100.000 duelos.

Delta de win DEF_CAP2 frente a CURRENT:

- −0.666 pp;
- −0.521 pp;
- −0.518 pp;
- −0.555 pp.

La dirección del efecto es estable.

## Conclusión de Etapa 1

**PASS para continuar testeando DEF_CAP2.**

No significa que DEF_CAP2 quede aprobado.

Significa únicamente:

> reducir la DEF máxima de Piel de 6 a 5 no destruye su funcionamiento básico
> contra un enemigo ordinario 1v1.

Piel sigue siendo una defensiva fuerte en ambas variantes.

La pequeña pérdida de rendimiento es coherente con el objetivo del ajuste:
recortar escalado extremo sin volver mediocre la técnica en duelo normal.

## Próxima etapa

**ETAPA 2 — CURRENT vs DEF_CAP2 contra enemigo pesado 1v1.**

No avanzar a precisión ni grupos antes de cerrar esa comparación.
