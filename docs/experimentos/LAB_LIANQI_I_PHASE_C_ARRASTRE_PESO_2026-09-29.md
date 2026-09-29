# LAB — Arrastre y Peso en PHASE C · LianQi I

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON**

## Objetivo

Valorar por primera vez la utilidad real de las técnicas iniciales de Agua y
Tierra sin corregir artificialmente su daño directo.

Se mantiene:

- hit cap = 100;
- jugador LAB: HP 30 / Qi 30 / DEF 1 / EVA 5;
- enemigo: HP 28 / EVA 20 / DEF 2;
- daño enemigo: `2d4+1`;
- jugador actúa primero;
- técnicas narrow;
- ataque básico `1d4+4`.

Se barre Precisión enemiga 85 / 90 / 95 / 100.

## Reglas recuperadas

### Latigazo de Marea — Arrastre

Base aprobada:

- al impactar intenta aplicar Arrastre mediante Control vs Tenacidad;
- Arrastre hace perder la próxima acción;
- puede cortar una acción anunciada;
- anti-bloqueo: después de sufrir Arrastre, el objetivo debe completar una
  acción normal antes de poder sufrir Arrastre otra vez.

La potencia base de Control sigue **PENDIENTE**.

### Golpe de Montaña — Peso

Base aprobada:

- al impactar aplica Peso;
- −3 Evasión por carga;
- duración 2 turnos;
- máximo 2 cargas;
- no es Control.

Hueco detectado:

> el diseño todavía no declara explícitamente `STACKING_MODE` ni la unidad
> exacta de consumo de esos "2 turnos".

El Registro universal admite `STACK_REFRESH` e `INDEPENDENT`, por lo que
ambos se testean y no se canoniza ninguno todavía.

## Baseline sin Arrastre/Peso · PREC enemiga 90

Confirmación de 100.000 duelos por raíz:

| Raíz | Win rate | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|
| Fuego | ~95.6% | ~4.25 | ~52.2% | ~13.7% |
| Metal | ~90.7% | ~5.05 | ~40.0% | ~28.5% |
| Agua | ~74.4% | ~5.93 | ~26.1% | ~59.1% |
| Tierra | ~89.6% | ~5.42 | ~40.4% | ~40.0% |
| Viento | ~87.9% | ~5.69 | ~38.8% | ~48.0% |

La desventaja aparente de Agua sigue siendo artificial porque todavía no usa
su control.

## Arrastre — sensibilidad de Control

Para separar potencia propia de técnica y Tenacidad enemiga, se mide la
**probabilidad efectiva**:

```text
chance = base_control + Control jugador - Tenacidad enemigo
```

Agua aporta +5 Control por raíz.

Con PREC enemiga 90:

| Chance efectiva de Arrastre | Win Agua | HP restante | Acciones enemigas saltadas |
|---:|---:|---:|---:|
| 45% | ~86.2% | ~41.5% | ~1.26 |
| 55% | ~87.6% | ~44.2% | ~1.46 |
| 65% | ~88.8% | ~46.6% | ~1.65 |

La banda 55–65% ya corrige casi toda la desventaja de Agua sin tocar su daño.

### Lectura

Con ~55% efectivo:

- Agua pasa de ~74% a ~88% de victorias;
- queda muy cerca de Viento;
- sigue por debajo de Fuego;
- evita aproximadamente 1.5 acciones enemigas por combate;
- el anti-bloqueo impide encadenar control indefinidamente.

Esto es un resultado saludable.

No se fija todavía `base_control`, porque depende de la Tenacidad que
terminemos asignando al enemigo ordinario.

Ejemplo puramente LAB:

```text
base_control 60
+ Control de raíz Agua 5
- Tenacidad enemiga 10
= 55% efectivo
```

## Peso — sensibilidad de stacking/duración

Baseline Tierra sin Peso:

- win rate ~89.6%;
- ~5.42 turnos;
- ~40.4% HP restante.

### Interpretación conservadora
Peso beneficia aproximadamente una acción futura:

| Modo | Win Tierra | Turnos | HP restante |
|---|---:|---:|---:|
| STACK_REFRESH | ~91.2% | ~5.31 | ~42.1% |
| INDEPENDENT | ~91.0% | ~5.32 | ~42.0% |

### Interpretación literal de dos acciones futuras

| Modo | Win Tierra | Turnos | HP restante |
|---|---:|---:|---:|
| STACK_REFRESH | ~92.5% | ~5.21 | ~43.4% |
| INDEPENDENT | ~92.2% | ~5.22 | ~43.3% |

La diferencia entre `STACK_REFRESH` e `INDEPENDENT` es pequeña en estos
duelos porque Golpe de Montaña se usa repetidamente.

La duración, en cambio, sí importa.

### Lectura

Peso funciona como utilidad moderada:

- mejora consistencia del propio Golpe y del básico posterior;
- reduce el fallback;
- acorta ligeramente el combate;
- no altera la presión enemiga directamente;
- no produce una explosión de poder.

Esto encaja con la identidad de Tierra.

## Comparación con utilidades activas

Usando como referencia:

- Agua con Arrastre efectivo ~55%;
- Tierra con Peso de 2 acciones futuras / STACK_REFRESH;
- Fuego, Metal y Viento sin cambios;

el duelo queda aproximadamente así:

| PREC enemigo | Fuego | Metal | Agua | Tierra | Viento | Promedio |
|---:|---:|---:|---:|---:|---:|---:|
| 85 | 96.7% | 92.3% | 89.7% | 94.0% | 90.2% | 92.6% |
| 90 | 95.7% | 90.5% | 87.7% | 92.6% | 88.1% | 90.9% |
| 95 | 94.9% | 88.7% | 85.4% | 91.0% | 85.2% | 89.0% |
| 100 | 93.8% | 86.7% | 83.5% | 89.4% | 82.1% | 87.1% |

## Hallazgo principal

Una vez valoradas las utilidades:

> **Agua deja de necesitar un aumento de daño.**

La brecha extrema anterior era consecuencia de simular una técnica de Control
como si sólo fuera daño.

Tierra también obtiene valor real de Peso, pero de magnitud moderada.

## Precisión enemiga

El test refuerza que Precisión debe variar por criatura.

Para un enemigo ordinario de referencia:

- PREC 85 resulta muy indulgente;
- PREC 90 produce ~91% de victoria agregada con utilidades;
- PREC 95 produce ~89%;
- PREC 100 queda como presión más alta, no como valor universal.

Por ahora se conserva:

```text
PREC 90
→ centro LAB de criatura común

PREC 95
→ criatura competente / más exigente

PREC 100
→ entrenada / muy precisa
```

No se promueve todavía a tabla CANON.

## Decisiones NO tomadas

Aún no se fija:

- base_control definitivo de Arrastre;
- Tenacidad normal de LianQi I;
- stacking mode de Peso;
- unidad exacta de duración de Peso;
- Precisión universal por categoría;
- HP/DEF/EVA del jugador como CANON.

## Próximo paso recomendado

1. resolver semántica de Peso:
   - `STACK_REFRESH` vs `INDEPENDENT`;
   - qué significa exactamente "2 turnos";
2. elegir un perfil LAB de Tenacidad ordinaria;
3. fijar una potencia base LAB de Arrastre que produzca ~55% efectivo contra
   ese perfil;
4. reejecutar PHASE C con esas semánticas cerradas;
5. después introducir las técnicas defensivas base.

