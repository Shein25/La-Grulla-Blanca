# LAB — Perfiles abstractos de enemigo · LianQi I PHASE A

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / NO CANON / SIN CRIATURAS CONCRETAS**

## Objetivo

Encontrar una zona útil de Evasión/DEF para LianQi I sin importar números
legacy y sin adelantar HP, Qi máximo, daño enemigo o equipo.

Se compara:

- ataque básico candidato principal: `1d4+4` (media 6.5, coste 0);
- las cinco técnicas iniciales;
- variantes de dados `narrow` y `wide` actuales;
- raíces CANON;
- cuatro perfiles abstractos de resistencia.

Se excluyen:

- HP/TTK;
- economía total de Qi;
- daño/Precisión enemiga;
- equipo;
- injerto;
- Concordancias;
- Tramos;
- valor extra de Arrastre/Peso.

## Perfiles LAB

| Perfil | Evasión | DEF | Función experimental |
|---|---:|---:|---|
| L1_SOFT | 10 | 1 | enemigo de baja resistencia |
| L1_STANDARD | 20 | 2 | candidato de referencia ordinaria |
| L1_ARMORED | 20 | 4 | cuerpo/armadura resistente |
| L1_EVASIVE | 35 | 2 | enemigo ágil especializado |

Estos valores no representan todavía monstruos reales.

## Método

Monte Carlo reproducible:

- 200.000 acciones por combinación;
- raíces: Fuego / Metal / Agua / Tierra / Viento;
- básico: `1d4+4`;
- técnicas: `narrow` y `wide`;
- pipeline del contrato nuevo;
- semilla base: 20260929.

Runner:

`experimentos/balance_nuevo/phase_a_enemy_profiles_lab.py`

## Resultado principal — técnicas narrow

| Perfil | daño básico medio* | daño técnica medio* | premium medio | rango de premium |
|---|---:|---:|---:|---:|
| L1_SOFT | 5.37 | 7.65 | 1.42x | 1.27–1.55x |
| L1_STANDARD | 3.97 | 6.01 | 1.51x | 1.33–1.64x |
| L1_ARMORED | 2.35 | 4.53 | 1.92x | 1.57–2.32x |
| L1_EVASIVE | 3.24 | 4.91 | 1.51x | 1.34–1.64x |

\* Promedio descriptivo entre raíces, no estadística CANON de personaje.

### L1_STANDARD — E20 / DEF2

| Raíz | Básico | Técnica | Premium |
|---|---:|---:|---:|
| Fuego | 4.65 | 7.65 | 1.64x |
| Metal | 3.98 | 6.14 | 1.55x |
| Agua | 3.74 | 4.98 | 1.33x |
| Tierra | 3.75 | 5.80 | 1.55x |
| Viento | 3.73 | 5.47 | 1.46x |

Tasas de impacto de técnicas:

- raíces sin Precisión extra: ~80%;
- Metal: ~85%;
- Lanza que Parte Nubes: ~85%.

Ninguna técnica narrow produce impactos conectados de daño 0 en este perfil.

### L1_ARMORED — E20 / DEF4

| Raíz | Básico | Técnica | Premium |
|---|---:|---:|---:|
| Fuego | 3.05 | 6.05 | 1.98x |
| Metal | 2.28 | 5.28 | 2.32x |
| Agua | 2.14 | 3.36 | 1.57x |
| Tierra | 2.14 | 4.19 | 1.96x |
| Viento | 2.15 | 3.78 | 1.76x |

El básico `1d4+4` conserva 0% de impactos acertados anulados por DEF4.

La DEF elevada hace que gastar Qi gane valor, especialmente para Metal debido
a su penetración.

## Narrow vs wide

A igual media nominal, `wide` no aporta una mejora sustancial de daño esperado.
Sí incrementa la volatilidad.

Contra L1_ARMORED / DEF4:

- Agua wide: ~7.8% de impactos acertados terminan en 0;
- Tierra wide: ~2.6%;
- Viento wide: ~7.5%;
- las variantes narrow correspondientes: 0%.

Esto no demuestra que `wide` sea incorrecto globalmente, pero sí muestra un
coste importante: una técnica que consume Qi puede acertar y aun así causar
0 daño frente a una DEF que el ataque básico estable todavía atraviesa.

## Lectura de los cuatro perfiles

### L1_SOFT

- ~90% de impacto normal;
- premium medio de técnica ~1.42x;
- útil para enemigos de baja resistencia o tutorial;
- no debería ser la única referencia porque comprime demasiado la diferencia
  entre básico y técnicas de menor daño.

### L1_STANDARD

- ~80% de impacto normal;
- ~85% para técnicas/perfiles con Precisión adicional;
- premium medio ~1.51x;
- no genera impactos de 0 con narrow;
- conserva valor claro para el ataque básico sin hacer gratuitas a las técnicas.

**Es actualmente el candidato LAB más limpio para referencia ordinaria.**

### L1_ARMORED

- mantiene la misma presión de Evasión que STANDARD;
- sube DEF a 4;
- premium medio ~1.92x;
- demuestra claramente el valor de técnicas y penetración;
- funciona bien como perfil resistente/armado o como stress test de PHASE A.

No se propone como enemigo ordinario universal.

### L1_EVASIVE

- ~65% de impacto normal;
- ~70% con Precisión adicional;
- premium de daño similar a STANDARD;
- representa una dificultad distinta: evita daño en vez de absorberlo.

Conviene reservar una Evasión de este orden para enemigos cuya identidad sea
realmente ágil, no para poblar todo LianQi I.

## Hipótesis que emerge

Para continuar PHASE A, la combinación más informativa es:

```text
REFERENCIA ORDINARIA LAB
Evasión 20
DEF 2

ATAQUE BÁSICO LAB
1d4+4

TÉCNICAS
dados narrow como candidato principal
wide conservado como comparación
```

Y conservar:

```text
DEF 4
→ perfil resistente / armadura / stress test

Evasión ~35
→ perfil evasivo especializado
```

Nada de esto queda CANON automáticamente.

## Decisión todavía pendiente

Antes de desbloquear el runner estricto `lianqi1_naked_benchmark.py`, hace falta
una decisión humana explícita sobre:

1. si `E20 / DEF2` pasa de LAB a **PROVISIONAL** como primer enemigo de
   referencia LianQi I;
2. si los dados `narrow` pasan de LAB a **PROVISIONAL** como distribución
   inicial de las cinco técnicas;
3. si `1d4+4` pasa de LAB a **PROVISIONAL** como ataque básico.

Una vez hecho eso, PHASE A puede ejecutarse en el runner estricto y cerrarse
antes de pasar a PHASE B (Qi máximo + piso de coste).
