# Checkpoint — Grulla Fase I · baseline 150 HP v0.1

**Fecha:** 2026-09-26  
**Estado:** CHECKPOINT DE TRABAJO / NO CANÓNICO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Corrección de baseline

Se recupera como referencia histórica de la Grulla:

```text
Fase I   150 HP
Fase II  100 HP
Fase III  50 HP
TOTAL    300 HP
```

El benchmark reciente que reutilizó:

```text
45 / 35 / 25
```

se considera una sensibilidad antigua de reducción y **no debe usarse como baseline de la Grulla**.

## Alcance de este checkpoint

Se estudia únicamente:

```text
FASE I — EL VOTO INMÓVIL
```

No se calculan Fase II ni Fase III hasta cerrar y documentar Fase I.

## Stats históricos a barrer

Fijos:

```text
HP  = 150
ATQ = 4
daño básico = 1d6+2
Campanada cada 4 rondas
Campanada = 2d6+2
```

Sensibilidad:

```text
DEF 13
DEF 14
```

No se fija todavía cuál de las dos DEF será definitiva.

## Jugador LianQi IV

Ver74 concede:

```text
4 puntos de técnica totales
```

Por tanto cualquier combinación de meridianos usada en los cálculos debe respetar ese presupuesto.

Toolkit universal:

```text
ATACAR básico
DEFENDER
técnica raíz
```

Opcionales:

```text
Paso de Nube
Piel de Cobre
Filamento de Agua
```

## Orden de cálculo para evitar trabajo perdido

### Fase I-A

Barrido completo de las 27 formas raíz:

```text
3 raíces
× 3 opciones tramo 1
× 3 opciones tramo 2
= 27
```

con DEF 13 y DEF 14.

### Fase I-B

Añadir Paso / Piel / Filamento de forma aislada y medir su ventaja real.

### Fase I-C

Sólo después, cruzar combinaciones múltiples de técnicas opcionales respetando:

```text
máximo 4 PT
```

y deduplicar configuraciones equivalentes antes de Monte Carlo.

## Regla de seguridad de trabajo

Cada sub-barrido debe:

1. guardar script reproducible;
2. guardar resultado resumido;
3. hacer commit;
4. recién entonces avanzar al siguiente bloque.

Esto evita perder el estado del análisis ante una interrupción o timeout.
