# Resultado — Grulla Fase III · opcionales y stress final v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / VALIDACIÓN FINAL PASADA  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Baseline previo

```text
FASE I       CERRADA
FASE II      CERRADA / CHAIN_A
FASE III HP  50

Perfil FIII  M_A
Política     MASTER_READER
```

M_A:

```text
ATQ 4 / DEF 13
Picotazo Blanco       +1 ATQ / 1d4+1
Campana sin Dueño     +1 ATQ / 1d6+2 / drain 2
Ala Vacía             +10 EVA
Pata Inmóvil          +3 DEF
Romper Ritmo          +2 ATQ / 1d6+2
```

MASTER_READER ya había confirmado:

```text
llega FIII           20,22%
FIII condicional     35,17%
I+II+III              8,33%
```

## 2. Stress cero-qi — FIII standalone

Entrada forzada:

```text
HP       28
qi        0
poción    0
```

10.000 duelos por build.

| Raíz | Victoria media | Mín | Máx |
|---|---:|---:|---:|
| Fuego | 86,42% | 85,80% | 87,02% |
| Metal | 89,63% | 89,15% | 90,31% |
| Agua | 92,30% | 91,72% | 92,82% |
| **Global** | **89,45%** | **85,80%** | **92,82%** |

Conclusión: M_A no necesita qi para ser resoluble desde estado fresco; BASIC conserva una ruta robusta.

## 3. Stress cero-qi — cadena real

Fase I + Fase II se ejecutan normalmente. Sólo al entrar a FIII se fuerza:

```text
qi       0
poción   0
HP       heredado real
```

10.000 cadenas por build.

| Raíz | Llega FIII | FIII condicional | I+II+III |
|---|---:|---:|---:|
| Fuego | 21,86% | 16,46% | 3,93% |
| Metal | 20,62% | 19,71% | 4,31% |
| Agua | 18,56% | 19,03% | 4,21% |
| **Global** | **20,35%** | **18,40%** | **4,15%** |

Entrada media HP a FIII: **10,29**.

Rango condicional entre builds:

```text
9,70% .. 33,06%
```

Conclusión: no existe soft-lock de recursos. Incluso con qi y poción en cero, la cadena conserva rutas reales.

## 4. Opcionales en cadena completa I -> II -> III

Se reutilizan exactamente las políticas cerradas de Fase I/Fase II:

```text
Paso óptimo
Piel G345_D1 final
Filamento óptimo
```

En FIII la opcional sólo sustituye DEFENDER ante Campana sin Dueño o Romper Ritmo cuando HP <= 10. No se usa como rotación principal.

Se conservan:

- Silencio entre Campanas -> BASIC;
- Buscar Pulso -> acción sin qi;
- aprendizaje y supresión por repetición;
- BASIC u otra técnica rompe lock;
- Tenacidad/cooldown de Filamento;
- ausencia de lectura de RNG futuro.

## 5. Confirmación opcionales — 15.000 por build

Volumen por corrida:

```text
3 herramientas
× 27 builds
× 15.000
=
1.215.000 cadenas
```

Se ejecutaron dos corridas con las mismas entradas: opcional activa en FIII y opcional desactivada sólo dentro de FIII.

### Con opcional activa en FIII

| Herramienta | Llega FII | Llega FIII | FIII condicional | I+II+III | HP entrada | qi entrada |
|---|---:|---:|---:|---:|---:|---:|
| Paso | 66,21% | **13,28%** | **16,11%** | **2,45%** | 8,70 | 1,15 |
| Piel | 75,07% | **21,45%** | **21,48%** | **5,22%** | 9,80 | 1,22 |
| Filamento | 75,76% | **17,58%** | **17,16%** | **3,40%** | 8,87 | 1,37 |

### Diferencia por reutilizar la opcional dentro de FIII

```text
Paso       -0,0345 pp
Piel       +0,0037 pp
Filamento  -0,0018 pp
```

Resultado: reutilizar la herramienta dentro de FIII es prácticamente neutro. El factor dominante es el desgaste heredado y la lectura de la fase maestra.

Uso medio de la opcional por FIII alcanzada:

```text
Paso       0,030
Piel       0,031
Filamento  0,0001
```

MASTER_READER rara vez necesita recurrir a ellas.

## 6. Opcionales por raíz

### Paso

| Raíz | Llega FIII | FIII condicional | Total |
|---|---:|---:|---:|
| Fuego | 10,49% | 12,86% | 1,53% |
| Metal | 14,05% | 16,40% | 2,71% |
| Agua | 15,30% | 19,07% | 3,11% |

### Piel

| Raíz | Llega FIII | FIII condicional | Total |
|---|---:|---:|---:|
| Fuego | 20,02% | 18,41% | 4,16% |
| Metal | 24,90% | 23,74% | 6,72% |
| Agua | 19,42% | 22,29% | 4,78% |

### Filamento

| Raíz | Llega FIII | FIII condicional | Total |
|---|---:|---:|---:|
| Fuego | 15,67% | 13,96% | 2,43% |
| Metal | 21,17% | 18,20% | 4,45% |
| Agua | 15,90% | 19,33% | 3,32% |

Las tres raíces conservan rutas.

## 7. Counterplay maestro

La evidencia previa permanece válida:

```text
PURE SPAM            0% victoria global
SPAM + DEFENDER      0% victoria global
```

MASTER_READER frente a GREEDY:

```text
GREEDY
FIII condicional 34,11%
total             8,05%

MASTER_READER
FIII condicional 35,17%
total             8,33%
```

MASTER supera al codicioso porque permite hasta dos técnicas seguidas, rompe Silencio con BASIC, responde a Buscar Pulso sin qi y defiende sólo bajo amenaza real.

## 8. Decisión

No existe evidencia para endurecer M_A.

No existe evidencia para hacer obligatoria ninguna opcional.

No existe soft-lock con qi cero.

No existe una ruta de spam viable.

Por tanto:

```text
M_A             VALIDADO
MASTER_READER   VALIDADO
HP 50           VALIDADO
OPCIONALES      VALIDADAS
ZERO-QI         VALIDADO
ANTI-SPAM       VALIDADO
```

Fase III queda lista para cierre experimental.

## 9. Scripts

- `benchmark/colab/grulla-phase123-chain-ma-v0.1.py`
- `benchmark/colab/grulla-phase123-optionals-v0.1.py`