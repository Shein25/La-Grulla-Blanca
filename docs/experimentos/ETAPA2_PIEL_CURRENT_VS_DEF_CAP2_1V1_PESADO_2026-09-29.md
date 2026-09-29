# ETAPA 2 — Piel CURRENT vs DEF_CAP2 · 1v1 pesado

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA COMO TEST / NO PROMOCIÓN**

## Pregunta única

¿Reducir la DEF máxima de Piel de Cobre de 6 a 5 mediante `DEF_CAP2`
degrada demasiado su rendimiento contra un enemigo pesado 1v1?

No se testean todavía:

- enemigos precisos;
- grupos de 2;
- grupos de 3;
- Control enemigo;
- otras defensivas.

## Baseline

Se conserva exactamente la Etapa 1 salvo una única variable:

```text
ataque enemigo
2d4+1 → 1d6+3
```

Jugador Tierra:

- HP efectivo 33;
- Qi31 LAB;
- DEF1;
- EVA5;
- Piel como apertura;
- Golpe de Montaña narrow;
- Peso PROVISIONAL STACK_REFRESH.

Enemigo pesado LAB:

- HP28;
- PREC90;
- EVA20;
- DEF2;
- ataque `1d6+3`.

## Resultado principal

Simulación de 200.000 duelos:

| Métrica | CURRENT | DEF_CAP2 |
|---|---:|---:|
| Win rate | 93.91% | 92.96% |
| Turnos medios | 6.56 | 6.53 |
| HP restante medio | 55.92% | 53.15% |
| Usa ataque básico | 67.28% | 67.17% |
| Arraigo máximo medio | 2.80 | 2.80 |
| Impactos enemigos medios | 4.78 | 4.76 |
| Daño recibido medio | 14.69 | 15.63 |

Diferencias:

```text
Win rate:
DEF_CAP2 ≈ -0.95 pp

HP restante:
DEF_CAP2 ≈ -2.78 pp
```

## Repetición por semillas

Cuatro semillas independientes de 100.000 duelos:

- −0.898 pp;
- −0.895 pp;
- −1.013 pp;
- −1.013 pp.

Delta de HP restante:

- −2.76 pp;
- −2.85 pp;
- −2.87 pp;
- −2.79 pp.

La dirección del efecto es estable.

## Lectura

El enemigo pesado amplifica la diferencia respecto de Etapa 1, como era
esperable: cada unidad de DEF plana vale más cuando hay más daño atravesando
Piel.

Pero el ajuste sigue siendo moderado:

- Piel conserva >92% de victoria;
- la duración prácticamente no cambia;
- la frecuencia de fallback permanece igual;
- Arraigo sigue alcanzando máximos con la misma frecuencia;
- DEF_CAP2 reduce supervivencia sin cambiar la identidad de la técnica.

## Conclusión de Etapa 2

**PASS para continuar testeando DEF_CAP2.**

Esto no aprueba DEF_CAP2 todavía.

Significa únicamente:

> contra un enemigo pesado 1v1, bajar la DEF máxima de 6 a 5 produce una
> pérdida medible pero no destruye la función defensiva de Piel.

## Próxima etapa

**ETAPA 3 — CURRENT vs DEF_CAP2 contra enemigo preciso 1v1.**

No avanzar todavía a grupos.
