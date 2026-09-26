# Decisión — Herramientas opcionales contra la Grulla v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / REQUISITO DE DISEÑO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Principio

Paso de Nube, Piel de Cobre y Filamento de Agua pueden mejorar mucho la calidad táctica del jugador, pero **ninguna debe ser requisito de victoria**.

El toolkit mínimo garantizado sigue siendo:

```text
técnica raíz
+
ATACAR
+
DEFENDER
+
recursos normales
```

## Paso de Nube — herramienta de lectura

Rol: `EVADE`.

Debe ser especialmente valioso frente a Campanada del Pico, Tormenta de Mil Plumas, Campana sin Dueño y Romper el Ritmo.

No reemplaza el counterplay universal `DEFENDER`.

Si el jugador abusa de Paso y la Grulla lo comprende, `PULSO FIJADO` anula la Esquiva de **esa activación concreta**. No concede inmunidad universal a Esquiva.

## Piel de Cobre — herramienta de absorción

Rol: `GUARD`.

Debe ofrecer una ruta eficiente frente a golpes fuertes y cadenas de daño, preservando HP mejor que una respuesta tardía.

No reemplaza `DEFENDER`.

Si la Grulla comprende Piel, `RESONANCIA INTERNA` impide que esa activación genere su burbuja de Guardia. No rompe DEFENDER ni otras defensas.

## Filamento de Agua — herramienta de interrupción

Rol: `CONTROL`.

Su valor principal contra la Grulla no es aumentar daño: es **interrumpir una intención peligrosa o romper una preparación de plan**.

En especial puede ser útil contra Silencio entre Campanas, Buscar el Pulso y golpes fuertes telegráficos.

Sigue sometido a las reglas reales de jefe:

```text
máximo 1 acción perdida
+
Tenacidad 2
```

Por tanto no puede encadenar control infinito.

Si la Grulla aprende Filamento, `ANCLA DEL VOTO` hace fallar esa ejecución concreta. No obtiene inmunidad universal al control.

## Fases

### Fase I

Las herramientas opcionales pueden ayudar a sobrevivir, pero la fase sigue teniendo una respuesta universal legible. No deben permitir ignorar completamente el ciclo programado.

### Fase II

La Grulla empieza a observar cómo se usan. El jugador obtiene ventaja si sabe cuándo usarlas y pierde eficiencia si las convierte en automatismo.

### Fase III

Las tres ganan valor estratégico:

```text
Paso      → evitar un remate que se dejó preparar
Piel      → absorber una ventana de presión
Filamento → cancelar una preparación o turno crítico
```

Pero el mismo problema siempre tiene al menos una respuesta del toolkit básico.

## Invariante de diseño

Para toda intención de la Grulla existe al menos una respuesta universal.

No puede existir:

```text
"si no compraste/encontraste el manual X, pierdes"
```

## Implementación de laboratorio

Matriz: `adaptive/grulla-counterplay-matrix-v0.1.mjs`

Test: `tests/grulla-counterplay-matrix.test.mjs`

La matriz diferencia:

```text
UNIVERSAL
BASIC
DEFEND

OPTIONAL
EVADE   → paso_nube
GUARD   → piel_cobre
CONTROL → filamento
```

## Próximo paso

La siguiente calibración numérica debe medir cuánto aumenta la victoria un buen uso de cada técnica, si alguna trivializa el encuentro, si abusarla activa correctamente su counter y si el toolkit mínimo conserva sus tasas originales.

Hasta completar esa medición, no se suben HP/ATQ/DEF de la Grulla.
