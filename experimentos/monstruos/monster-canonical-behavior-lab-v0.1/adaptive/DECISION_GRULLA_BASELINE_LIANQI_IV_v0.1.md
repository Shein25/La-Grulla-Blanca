# Decisión — Baseline mínimo de victoria contra la Grulla v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / REQUISITO DE DISEÑO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## Hallazgo de ver74

Las tres raíces iniciales garantizan una única técnica ofensiva preparada:

```text
Fuego → Palma Ardiente
Metal → Filo de Qi Metálico
Agua  → Látigo de Agua
```

Los manuales de:

- Paso de Nube;
- Piel de Cobre;
- Filamento de Agua;

existen en `ITEMS`, pero actualmente:

```text
CATALOGO = []
COMPRAR = pendiente de implementación 3C
TIENDA  = pendiente de implementación 3C
```

y no tienen una referencia directa de quest/room/drop en ver74.

Por tanto no pueden tratarse todavía como herramientas garantizadas al llegar al jefe.

## Regla

La Grulla debe ser vencible, con ejecución competente, usando como mínimo:

```text
técnica raíz inicial
+
ataque básico
+
DEFENDER
+
recursos/consumibles que la progresión normal entregue
```

Las técnicas adicionales pueden:

- facilitar ciertos counters;
- abrir mejores ventanas;
- ahorrar recursos;
- permitir rutas tácticas más elegantes;

pero **no deben ser llaves obligatorias de victoria**.

## Consecuencia para el anti-spam

La regla:

> 100% de la misma skill = 0% victoria

no significa:

> necesitas aprender una segunda skill para poder terminar el juego.

Un jugador con una sola técnica puede demostrar variedad mediante:

```text
Palma
→ ataque básico
→ defender
→ Palma
→ ataque básico
```

El ataque básico cuenta como variación táctica real.

DEFENDER o curarse por sí solos no hacen olvidar a la Grulla una técnica ya comprendida.

## Invariante de accesibilidad sistémica

Cada una de las tres raíces iniciales debe tener una ruta válida:

```text
Fuego / Palma + básico
Metal / Filo + básico
Agua / Látigo + básico
```

sin necesitar:

- Paso de Nube;
- Piel de Cobre;
- Filamento;
- una raíz secundaria;
- una técnica de ZhuJi;
- un manual opcional específico.

Esto deberá demostrarse en la simulación completa posterior.

## Test dirigido

Se añadió al laboratorio de cerebro una prueba que recorre las tres raíces iniciales y verifica que:

- alternar técnica raíz + básico evita entrar a Fase II con counter duro;
- la misma alternancia en Fase II no consolida el lock de esa técnica.

Esto sólo valida el contrato cognitivo, no todavía la tasa real de victoria.
