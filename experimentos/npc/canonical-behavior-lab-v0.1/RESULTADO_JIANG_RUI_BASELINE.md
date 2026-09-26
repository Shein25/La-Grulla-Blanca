# Resultado baseline — Jiang Rui / LAB v0.1

## Alcance

Tercer ensayo de comportamiento sobre un NPC canónico, sin integración con producción.

Canon usado: `NPC_DEF.jiang_rui` de `grulla-blanca_ver74.html`.

Motores:

- Reactive Routine FSM v0.1 REV2 — snapshot auditado.
- Behavior Tree v0.1 REV2 — snapshot auditado.
- Utility AI v0.1.1 — fuente exacta del merge de PR #1, commit `404411f09c0e110f02c92689ffeb1a3c69a213ab`, blob `8d567625be09a4272c33b939b9b1bd94b68f18e7`.

## Canon relevante

- rol: Capitán de patrulla;
- sala inicial: `puesto_valle`;
- rutas:
  - `puesto_valle ↔ valle_explanada`;
  - `puesto_valle ↔ patio_puesto_valle`;
- sin tránsito técnico;
- LI: Puerta/Puesto;
- LII: rutas completas;
- LIII: territorio + investigación;
- M16: responsable principal, junto a Ren Bo, del frente RUTAS;
- R1 inicial: SOSPECHA.

## Perfil Utility

Los traits numéricos y la relación con el jugador NO existen en el canon.

El laboratorio usa un perfil de calibración explícitamente:

`EXPERIMENTAL_NON_CANONICAL`

Su única función es permitir probar el comportamiento del motor Utility. No debe copiarse a producción como personalidad canónica de Jiang Rui.

## Verificación

```text
PASS: 44
FAIL: 0
```

## Resultados por escenario

### 1. Patrulla ordinaria

Los tres convergen:

```text
FSM            PATROL_ROUTE
Behavior Tree  PATROL_ROUTE
Utility        PATROL_ROUTE   score 52.95
```

### 2. Anomalía leve, superior no alcanzable

```text
FSM            INVESTIGATE_ROUTE_ANOMALY
Behavior Tree  INVESTIGATE_ROUTE_ANOMALY
Utility        PATROL_ROUTE
```

Ranking Utility:

```text
patrullar    54.90
investigar   52.60
esperar      26.20
```

La diferencia es pequeña: Utility conserva el deber de patrulla ante una anomalía leve con este perfil de calibración.

### 3. Anomalía de riesgo alto, superior no alcanzable

Los tres convergen en investigar.

Utility:

```text
investigar   63.50
patrullar    62.05
esperar      21.00
```

El aumento de peligro/urgencia cruza el punto donde investigar supera patrullar.

### 4. Anomalía leve, superior alcanzable

```text
FSM            INVESTIGATE_ROUTE_ANOMALY
Behavior Tree  INVESTIGATE_ROUTE_ANOMALY
Utility        REPORT_SUPERIOR
```

Utility:

```text
informar_superior  67.30
patrullar          54.90
investigar         52.60
```

Con el perfil experimental prudente/disciplinado, la disponibilidad de un superior cambia la decisión.

### 5. Fuera del puesto, sin amenaza

Los tres convergen:

```text
RETURN_POST
```

Utility asigna `regresar_puesto` un score de 89.95.

### 6. Crisis de rutas M16

Los tres convergen:

```text
REPORT_SUPERIOR
```

Utility:

```text
informar_superior  86.20
investigar         63.35
patrullar          60.75
```

## Observación técnica

Jiang Rui es el primer baseline donde Utility AI muestra una propiedad que FSM/BT no expresan naturalmente con la misma configuración: **un cambio gradual de decisión por magnitud y contexto**.

La política fija del baseline FSM/BT dice, simplificando:

```text
anomalía -> investigar
alto riesgo + superior -> informar
```

Utility puede producir:

```text
anomalía leve + sin superior -> seguir patrullando
anomalía leve + superior     -> informar
anomalía grave + sin superior -> investigar
```

Esto NO demuestra que Utility sea mejor para Jiang Rui. El resultado depende de traits experimentales no canónicos. Sí demuestra que existe una diferencia medible que merece barrido de parámetros y escenarios en Colab.

No se asigna todavía arquitectura definitiva.
