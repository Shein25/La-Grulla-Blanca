# Regla humana de balance — Expectativa y progresión del equipamiento

**Fecha de ratificación humana:** 2026-10-09  
**Estado:** DECISIÓN DE DISEÑO RATIFICADA POR EL USUARIO.  
**Alcance:** equipo de todas las etapas, pruebas de balance, propuestas numéricas y handoffs para integración.

## Principio rector

> El equipo que un jugador consigue debe cumplir las expectativas creadas por su etapa, especialización y esfuerzo de obtención. Una recompensa superior debe sentirse superior en el papel que ocupa, sin que eso implique invulnerabilidad ni victorias automáticas.

No declarar una pieza «rota» ni recomendar nerf **solo porque aumenta considerablemente el win rate**. Antes de proponer modificarla, identificar:

1. **Posición real en la progresión:** etapa mínima, momento efectivo de adquisición y si es pieza inicial, intermedia, superior o final de su categoría.
2. **Función y fantasía de equipo:** pesada/protectora, ligera/evasiva, ofensiva, recurso, híbrida, etc. Comparar principalmente alternativas del mismo slot y etapa, preservando diferencias reconocibles.
3. **Esfuerzo o dificultad de obtención:** permisos, progreso, misión, materiales, enemigos y restricciones de acceso, **sin reabrir ni alterar los precios ratificados**.
4. **Valor percibido:** diferencia significativa respecto del equipo anterior, mejoras relevantes y oportunidades donde brilla su especialización.
5. **Encuentros y contrapartidas:** dificultad por monstruo, tier, etapa, configuración de técnicas y otras formas de daño; no exigir que una pieza defensiva pierda toda su ventaja por ser buena contra golpes físicos.
6. **Alternativas viables y no dominación:** una opción debe conservar su identidad (por ejemplo, la vestidura pesada por DEF y la ligera por EVA); detectar nerfs que vuelven dominante otra pieza, o que destruyen la recompensa por progresar.
7. **Criterios de nerf:** demostrar una distorsión real para su momento de adquisición y rol, y buscar primero el ajuste mínimo que preserve expectativas. Un win rate alto por sí solo **NO** es prueba suficiente.

## Ejemplo concreto LianQi II — Sobretúnica de patrulla

En `equipment_arc1_catalog.json`, `sobretunica_patrulla` es la vestidura **de mayor DEF de LianQi II**: **DEF +2, HP +2**, fuente M04, rol `MEDIUM_PATROL`. La alternativa ligera `tunica_ruta_sauces` es **DEF +1, EVA +3, HP +1**, fuente M05. Vestiduras pesadas con más DEF llegan en etapas posteriores (por ejemplo, LianQi III).

Los benchmarks V20–V31 documentaron un fuerte breakpoint de DEF plana y propusieron como candidato bajar la Sobretúnica a DEF +1. **La recomendación de aplicarlo queda SUSPENDIDA** hasta evaluar el rol de mejor vestidura defensiva de LianQi II, la expectativa del jugador y su relación con la alternativa de evasión y la progresión de la etapa. **Mantener DEF +2, HP +2 como baseline vigente; DEF +1 únicamente como brazo experimental.** No se modificó la pieza canónica ni se ratificó el nerf.

## Guardias y comunicación entre agentes

- Prioridad de esta decisión humana sobre recomendaciones antiguas de laboratorio cuando conflijan.
- Conservar la evidencia numérica histórica V20–V31 sin borrarla ni reinterpretar resultados como aprobaciones.
- Incorporar este criterio a nuevos dictámenes y al futuro handoff para Astra.
- No tocar `main`, no merge, no HTML, no `ROOMS.exits`, no equipo productivo, ni economía/comercio ratificados.

**Esta decisión establece un criterio de evaluación; no ratifica stats nuevas ni altera otras autoridades.**
