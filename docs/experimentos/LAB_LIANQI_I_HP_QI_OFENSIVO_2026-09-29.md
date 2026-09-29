# LAB — Cruce HP enemigo × Qi · LianQi I ofensivo

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO ES DUELO COMPLETO**

## Objetivo

Medir cuándo aparece el ataque básico por agotamiento de Qi antes de inventar
daño enemigo o HP del jugador.

Política del subtest:

```text
mientras haya Qi suficiente
→ usar técnica inicial

cuando ya no alcance
→ usar ataque básico
```

El enemigo no actúa.

Por tanto, este test mide sólo la duración ofensiva y la aparición del fallback.

## Configuración

Baseline PHASE A:

- Evasión enemiga 20 PROVISIONAL;
- DEF enemiga 2 PROVISIONAL;
- ataque básico 1d4+4 PROVISIONAL;
- técnicas narrow PROVISIONAL.

Barridos LAB:

- Qi máximo: 24 / 30;
- HP enemigo: 20 / 24 / 28 / 30 / 32 / 36;
- 20.000 combates por raíz y combinación;
- cinco raíces.

Runner:

`experimentos/balance_nuevo/phase_b_hp_qi_offense_lab.py`

## Resumen agregado entre raíces

| Qi | HP enemigo | Turnos medios | Combates que usan básico | Básicos medios | Técnicas medias |
|---:|---:|---:|---:|---:|---:|
| 24 | 20 | 4.08 | 28.3% | 0.54 | 3.53 |
| 24 | 24 | 4.88 | 48.6% | 1.09 | 3.80 |
| 24 | 28 | 5.74 | 68.9% | 1.82 | 3.92 |
| 24 | 30 | 6.23 | 78.2% | 2.27 | 3.96 |
| 24 | 32 | 6.70 | 84.6% | 2.72 | 3.97 |
| 24 | 36 | 7.67 | 92.4% | 3.68 | 3.99 |
| 30 | 20 | 4.00 | 10.8% | 0.19 | 3.81 |
| 30 | 24 | 4.74 | 23.0% | 0.46 | 4.28 |
| 30 | 28 | 5.51 | 40.2% | 0.90 | 4.61 |
| 30 | 30 | 5.94 | 49.7% | 1.20 | 4.74 |
| 30 | 32 | 6.36 | 59.1% | 1.54 | 4.82 |
| 30 | 36 | 7.26 | 75.1% | 2.34 | 4.92 |

## Dos zonas útiles

### Perfil compacto

```text
Qi 24
HP enemigo 20
```

Resultado agregado:

- ~4.08 turnos;
- ~28% de los combates llegan a usar ataque básico;
- ~0.54 acciones básicas de media.

El recurso importa, pero el fallback no domina el combate.

### Perfil extendido

```text
Qi 30
HP enemigo 28
```

Resultado agregado:

- ~5.51 turnos;
- ~40% de los combates llegan a usar ataque básico;
- ~0.90 acciones básicas de media.

Produce peleas algo más largas y hace visible el agotamiento sin convertir el
ataque básico en la acción principal.

## Diferencia entre raíces

El daño directo no es homogéneo, por diseño.

Ejemplo con Qi 30 / HP 28:

| Raíz | Turnos medios | Usa básico | Básicos medios | Técnicas medias |
|---|---:|---:|---:|---:|
| Fuego | 4.32 | 15.0% | 0.28 | 4.04 |
| Metal | 5.23 | 31.3% | 0.60 | 4.63 |
| Agua | 6.47 | 64.2% | 1.57 | 4.90 |
| Tierra | 5.61 | 40.1% | 0.92 | 4.68 |
| Viento | 5.93 | 50.4% | 1.11 | 4.81 |

Esto **no autoriza a subir el daño de Agua**:

- Arrastre todavía no tiene valor en el subtest;
- Agua posee +Control;
- el rasgo de Qi debe valorarse también sobre el catálogo futuro;
- Tierra tampoco está valorando HP/Tenacidad/Peso.

La diferencia sí es una advertencia para PHASE C: el duelo completo debe
comprobar que las utilidades compensan la diferencia de daño bruto sin crear
raíces claramente dominantes.

## Lectura

Qi 24 y Qi 30 siguen siendo candidatos viables, pero no significan lo mismo:

```text
24 Qi
→ fallback aparece antes
→ presión de recurso más fuerte
→ favorece combate corto

30 Qi
→ permite una técnica adicional
→ fallback aparece más gradualmente
→ admite combate de 5–6 turnos
```

Qi 24 contra HP 28+ hace que el básico sea casi obligatorio para la mayoría de
raíces.

Qi 30 contra HP 20–24 hace que el recurso raramente llegue a agotarse.

## Resultado

Todavía no se fija Qi máximo ni HP enemigo.

Quedan dos parejas principales para llevar al duelo completo:

1. **COMPACTA LAB:** Qi 24 / HP enemigo 20.
2. **EXTENDIDA LAB:** Qi 30 / HP enemigo 28.

También puede usarse HP 24 / Qi 30 como control de combate relativamente corto.

## Próximo paso

Para elegir entre COMPACTA y EXTENDIDA necesitamos incorporar la otra mitad del
duelo:

- HP del jugador;
- Precisión enemiga;
- daño enemigo por acción;
- Evasión/DEF base del jugador;
- posteriormente utilidades de Agua/Tierra y defensivas.

No se debe escoger HP/Qi sólo por el TTK ofensivo.
