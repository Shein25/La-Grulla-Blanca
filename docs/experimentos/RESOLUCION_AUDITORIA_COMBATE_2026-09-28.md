# Resolución de auditoría — combate, efectos y Concordancias

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **DECISIONES APROBADAS / NO IMPLEMENTACIÓN RUNTIME**

## 1. Resultado

La auditoría externa identificó tres bloqueantes arquitectónicos y varios huecos altos/medios. El diseñador aprobó las correcciones propuestas.

No se concluyó que el motor requiera una reescritura. Se conserva la arquitectura:

```text
Action
→ Event Bus
→ Context/Packets
→ Effect Engine
→ State Engine
→ Concordance Resolver
```

Las 12 técnicas diseñadas hasta Tierra siguen siendo expresables sin hardcodear IDs en el resolver central.

## 2. Bloqueantes resueltos

### B-01 · TURN_START

Orden cerrado:

```text
restauraciones defensivas
→ DOT/aflicciones
→ regeneración de Vida
→ Control/otros ticks
→ acción disponible
```

Fuente canónica: `CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md` v0.2 §38.1.

### B-02 · Ciclo de Eco

Cerrado:

- un solo slot por actor;
- reemplazo por Eco nuevo;
- consumo sólo con hook compatible;
- consumo al comenzar ejecución tras validación/coste;
- fallo posterior no devuelve Eco;
- consumo y generación no encadenan por defecto en la misma acción;
- híbridas fuera de Concordancias.

Fuente canónica: Motor v0.2 §38.2.

### B-03 · AOE 65%

La capa `AOE_SINGLE_TARGET_SCALAR = 0.65` se aplica antes de DEF y antes del redondeo final.

No reduce automáticamente debuffs, Control, duración ni stacks.

Fuente canónica: Motor v0.2 §38.3 y Contrato de combate v0.3 §27.3.

## 3. Resoluciones altas incorporadas

Se cerraron además:

- roles direccionales `OWNER_AS_SOURCE/TARGET`;
- eventos reactivos recibidos;
- unidades explícitas de duración;
- `max_reaction_depth = 8`;
- flags conservadores para DOT/Reflect/Retaliation/SECONDARY_REACTIVE;
- ventana `DAMAGE_CONVERSION` para Daño Aplazado;
- zonas/terreno como efectos con dueño ROOM/POSITION;
- persistencia de aflicciones y cura por familia/grado;
- múltiples pools de Absorción con prioridad determinista;
- snapshot de Concordancias sobre estados persistentes;
- orden determinista de objetivos AOE;
- disciplina RNG;
- modelo de acciones preparadas;
- recuperación explícita de Qi separada de regeneración pasiva;
- exclusión de injerto del mismo elemento que la raíz principal;
- Calor como porción secundaria sin doble escalado;
- anti-curación de Robo de Vida sólo mediante `affects_lifesteal=true`;
- cobertura de Concordancia medida por relación habilitada, no por todos los roles.

## 4. Correcciones de técnicas

### Armadura de Plata

Las Placas son **cargas secuenciales**, no DEF acumulativa simultánea.

```text
3 placas de +3 DEF
≠ +9 DEF

significa:
3 impactos protegidos
cada uno por +3 DEF
```

La ruta completa de cantidad alcanza 8 Placas mediante la sinergia final declarada.

### Espejo de Luna

Reflujo usa la **reserva máxima de la instancia** como referencia.

### Respiración del Cuerpo-Horno

Calor liberado:

- no vuelve a escalar con pools ofensivos;
- no critica;
- pasa por DEF y Absorción;
- no usa Penetración;
- no genera Robo de Vida.

## 5. Decisiones aún pendientes de balance, no de arquitectura

- valor final del 65% AOE;
- límite numérico de Robo de Vida por acción;
- piso global exacto de coste de Qi;
- orden final entre modificadores planos y porcentuales de coste si no queda fijado antes de serialización;
- caps de estadísticas que dependan de benchmark;
- números de Concordancias;
- economía de puntos de técnicas;
- balance de las 12 técnicas;
- diseño de las 3 técnicas de Viento.

## 6. Próximo paso recomendado

Antes de implementación runtime:

1. cerrar la matriz global de las 20 Concordancias;
2. mapear hooks de las 12 técnicas actuales;
3. diseñar las 3 técnicas de Viento usando la matriz global;
4. realizar una reauditoría corta de contratos;
5. sólo después autorizar implementación.

No tocar todavía `main`, `implement/3c5-npc-ver74` ni el runtime.
