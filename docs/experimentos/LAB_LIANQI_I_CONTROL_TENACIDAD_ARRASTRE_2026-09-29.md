# LAB — Escala Control/Tenacidad para Arrastre · LianQi I

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON**

## Punto de partida

El test anterior encontró una zona sana para Arrastre:

```text
P(Arrastre efectivo contra enemigo ordinario)
≈ 45–55%

centro LAB
≈ 50%
```

La fórmula CANON es:

```text
P(Control)
=
clamp(
  base_control
  + Control del personaje
  - Tenacidad del objetivo,
  5,
  100
)
```

Agua principal aporta:

```text
+5 Control
```

## Consecuencia matemática

Para obtener aproximadamente 50% contra el enemigo ordinario de referencia:

```text
base_control + 5 - Tenacidad_ref
≈ 50

por tanto:

base_control - Tenacidad_ref
≈ 45
```

Esto es lo que el benchmark realmente identifica.

No identifica por sí solo un valor absoluto único.

Por ejemplo, estas tres parejas son mecánicamente equivalentes contra su
respectiva referencia:

```text
base_control 55 / Tenacidad 10
base_control 65 / Tenacidad 20
base_control 75 / Tenacidad 30
```

Todas producen:

```text
55 + 5 - 10 = 50%
65 + 5 - 20 = 50%
75 + 5 - 30 = 50%
```

## Matriz LAB

Se exploraron:

- `base_control = 55 / 65 / 75`
- `Tenacidad = 10 / 20 / 30 / 40`

Runner:

`experimentos/balance_nuevo/phase_c_control_tenacity_lab.py`

## Candidato de escala

Como ancla LAB, la pareja más legible es:

```text
Arrastre base_control = 65
Tenacidad ordinaria LianQi I = 20
Agua principal = +5 Control

P(Arrastre)
= 65 + 5 - 20
= 50%
```

No se propone porque 65 o 20 sean "números verdaderos"; se propone porque deja
espacio limpio hacia ambos lados de la escala.

Con `base_control 65`:

| Tenacidad objetivo | P(Arrastre) | Win Agua aprox. | Acciones omitidas |
|---:|---:|---:|---:|
| 10 | 60% | 88.14% | 1.56 |
| 20 | 50% | 86.82% | 1.36 |
| 30 | 40% | 85.07% | 1.15 |
| 40 | 30% | 83.19% | 0.91 |

Esto genera una progresión comprensible:

```text
objetivo frágil al Control
Tenacidad 10
→ Arrastre 60%

objetivo ordinario
Tenacidad 20
→ Arrastre 50%

objetivo resistente
Tenacidad 30
→ Arrastre 40%

objetivo muy resistente
Tenacidad 40
→ Arrastre 30%
```

## Relación con ramas futuras

Latigazo ya posee una ruta de Control:

```text
Tramo I   +10 Control
Tramo II  +10 Control
Tramo III +10 Control
```

Con el ancla LAB `65 / Tenacidad 20`:

```text
Base Agua
65 + 5 - 20
= 50%

+ Tramo I
= 60%

+ Tramo II
= 70%

+ Tramo III
= 80%
```

El anti-bloqueo de Arrastre evita que esta progresión se convierta directamente
en un bloqueo permanente.

Este patrón es especialmente atractivo porque cada +10 Control se traduce en
+10 puntos de probabilidad mientras no se alcance el clamp.

## Qué sigue PENDIENTE

No promover aún:

- `base_control 65`;
- Tenacidad ordinaria 20.

Primero deben sobrevivir a:

1. otras técnicas de Control;
2. raíz Tierra (+5 Tenacidad);
3. equipo futuro;
4. jefes / inmunidad temporal / anti-chain;
5. progresión LianQi II–IV.

## Hipótesis de trabajo

Para los siguientes tests de LianQi I puede usarse como **LAB central**:

```text
ARRASTRE
base_control 65

ENEMIGO ORDINARIO
Tenacidad 20

AGUA PRINCIPAL
Control +5

→ 50% efectivo
```

La autoridad numérica continúa siendo LAB.

