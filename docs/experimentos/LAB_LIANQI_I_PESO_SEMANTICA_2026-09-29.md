# LAB — Semántica exacta de Peso · LianQi I

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / CANDIDATO SEMÁNTICO / NO CANON**

## Problema

Golpe de Montaña tiene actualmente:

```text
Peso
-3 Evasión por carga
máximo 2 cargas
duración 2 turnos
no es Control
```

El diseño no había cerrado dos detalles:

1. `STACK_REFRESH` vs `INDEPENDENT`;
2. qué significa exactamente `duración 2 turnos`.

## Evidencia estructural

La progresión de Golpe de Montaña habla de:

```text
máximo Peso 2 -> 3
al máximo, duración 2 -> 3
```

y posteriormente:

```text
ruta completa:
3 cargas
-5 Evasión por carga
duración 3 turnos
```

Esta redacción describe de forma más natural **un único estado Peso con intensidad
acumulable y una duración compartida**.

Con cargas independientes, "al máximo, duración 2 -> 3" requeriría decidir qué
carga se alarga o si se alteran todas, introduciendo una semántica que el diseño
no necesita.

Por ello `STACK_REFRESH` es el candidato estructural principal.

## A/B de stacking

Duelo central LAB:

- jugador Tierra: HP efectivo 33 / Qi 30 / DEF 1 / EVA 5;
- enemigo: HP 28 / PREC 90 / EVA 20 / DEF 2;
- ataque enemigo: 2d4+1;
- 200.000 duelos.

| Variante | Win Tierra | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|
| Sin Peso | 89.65% | 5.43 | 40.48% | 39.92% |
| STACK_REFRESH | 91.80% | 5.24 | 43.10% | 33.53% |
| INDEPENDENT | 91.11% | 5.31 | 42.14% | 35.96% |

Ambos modelos son balanceables. La diferencia de potencia es pequeña; la razón
principal para elegir `STACK_REFRESH` es claridad sistémica y coherencia con
la progresión futura.

## A/B de duración

Se compararon dos lecturas.

### A. Dos turnos del afectado

```text
al aplicar Peso:
duration = 2

cada TURN_END del afectado:
duration -= 1

si una nueva carga entra:
+1 stack hasta máximo
duration vuelve a 2
```

En duelo uno contra uno, la carga recién aplicada no altera el impacto que la
creó. Beneficia el siguiente ataque del jugador y, si Golpe vuelve a conectar,
la intensidad aumenta/refresca.

Resultado:

- win ~91.8%;
- utilidad moderada;
- permite alcanzar 2 cargas con ataques consecutivos;
- un fallo deja una ventana real para que Peso expire.

### B. Dos acciones futuras completas del atacante

La carga garantiza dos futuras ventanas ofensivas antes de expirar.

Resultado:

- win ~92.4%;
- duración media ~5.21;
- HP restante ~43.5%;
- fallback ~32.7%.

La diferencia numérica es pequeña (~0.6 pp de win), pero esta interpretación
requiere una duración anclada al atacante y es menos natural para un debuff que
pertenece al objetivo.

## Candidato semántico

La opción más limpia es:

```text
PESO

owner:
objetivo afectado

stacking_mode:
STACK_REFRESH

max_stacks:
2

stack_value:
-3 Evasión

duration:
2

duration_unit:
TARGET_TURN

tick/decay:
TURN_END del objetivo

on valid application:
+1 carga
refrescar duración completa

expiration:
al llegar duration a 0 se eliminan todas las cargas
```

Consecuencia en duelo:

```text
Golpe 1 conecta
→ Peso x1

enemigo completa turno
→ queda 1 turno de duración

Golpe 2 se beneficia de -3 EVA
si conecta:
→ Peso x2
→ duración vuelve a 2

si el jugador falla y no refresca:
→ Peso puede expirar
```

Esto crea exactamente la identidad buscada:

> cada impacto asienta al enemigo y hace más probable el siguiente, pero el
> jugador debe mantener la presión para conservar el máximo.

## Relación con Tramos

La semántica escala limpiamente:

### Base
- máximo 2;
- -3 EVA/carga;
- duración 2.

### Tramo II
- máximo 3;
- al máximo, duración 2 -> 3.

### Tramo III
- máximo 3;
- -5 EVA/carga;
- duración 3.

No requiere lógica especial por carga.

## Resultado

**Candidato principal LAB:**

```text
STACK_REFRESH
+
duration_unit = TARGET_TURN
+
decay en TURN_END del objetivo
```

No se modifica aún el documento autoritativo de técnicas ni runtime.

La magnitud `-3 EVA / carga, máximo 2` sigue superando los tests sin señal de
sobrepotencia.
