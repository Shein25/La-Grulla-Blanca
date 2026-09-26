# Resultado — Cerebro de la Grulla · examen final del Arco 1 v0.1

Fecha: 2026-09-26  
Estado: EXPERIMENTAL / NO CANÓNICO  
Rama: experiment/monster-adaptive-survival-lab-v0.1

## 1. Objetivo

La Grulla no debe ser simplemente el enemigo con más HP y daño del Arco 1.

Debe comprobar si el jugador realmente aprendió a:

- leer intenciones;
- administrar qi;
- variar técnicas;
- usar defensa;
- usar control;
- reconocer patrones;
- romper planes;
- llegar al final con recursos.

Se conserva el concepto narrativo de tres fases:

| Fase | Tema | Cerebro | Qué examina |
|---|---|---|---|
| I · El Voto Inmóvil | Obediencia | PROGRAMADA | lectura y disciplina |
| II · Las Alas Recuerdan | Memoria | ADAPTATIVA | variedad y administración |
| III · La Campana sin Dueño | Voluntad | MAESTRA | comprensión integral y contra-juego |

Los números finales de HP, ataque, defensa y daño siguen fuera de alcance.

## 2. Fase I — PROGRAMADA

Ciclo experimental:

1. Golpe de Ala
2. Golpe de Ala
3. Campanada del Pico
4. Pata Inmóvil
5. repetir

El ciclo no cambia por lo que haga el jugador.

La fase comprueba si el jugador entiende telegraphs y ventanas de defensa.

La baja inteligencia es intencional: representa obediencia sin elección.

## 3. Fase II — ADAPTATIVA

Memoria útil: últimas 3–4 acciones observadas.

Kit experimental:

- Golpe de Ala;
- Tormenta de Mil Plumas;
- Cerrar las Alas;
- Recordar el Filo;
- Eco del Meridiano.

Respuestas principales:

- repetir técnica o elemento aumenta Recordar el Filo;
- gastar qi consecutivamente aumenta Eco del Meridiano;
- presión ofensiva fuerte aumenta Cerrar las Alas;
- HP/qi visibles modifican prioridades.

No se crea resistencia elemental arbitraria.

La Grulla responde cambiando conducta.

### Memoria entre fases

Fase II no recibe el historial completo de Fase I.

Recibe sólo un resumen:

- técnica dominante;
- elemento dominante;
- cantidad de ofensivas;
- defensas;
- recuperaciones;
- controles;
- acciones que gastaron qi.

Ese resumen sólo altera pesos iniciales.

## 4. Fase III — MAESTRA

La fase final añade planes de 2 acciones.

Sólo puede existir un plan activo.

### Plan: Romper repetición

Secuencia:

1. detecta repetición;
2. anuncia Silencio entre Campanas;
3. el jugador actúa;
4. si repite, el plan queda armado;
5. turno siguiente: Romper el Ritmo;
6. si varía, el plan se cancela.

El jugador puede engañar a la Grulla.

### Plan: Cazar circulación

Secuencia:

1. detecta gasto continuado de qi;
2. anuncia Buscar el Pulso;
3. el jugador actúa;
4. si vuelve a gastar qi, queda armada Campana sin Dueño;
5. si usa básico, defensa u otra acción sin qi, el plan se cancela.

Ahorrar qi puede ser una decisión táctica.

### Interrupción

Un control válido puede limpiar el plan.

Por tanto control puede tener valor superior a daño cuando el jugador evita un remate.

## 5. Regla de justicia

La Grulla sólo usa información ya observable o resuelta:

- acciones previas;
- técnica y elemento ya usados;
- qi ya gastado;
- banda de daño ya observada;
- HP y qi actuales;
- memoria de fase;
- estado interno de su plan.

No usa:

- próxima acción;
- inventario oculto;
- cooldowns internos del jugador;
- RNG futuro;
- daño futuro;
- crítico futuro.

Orden obligatorio:

Grulla planifica  
→ la UI muestra intención  
→ el jugador actúa  
→ se ejecuta la intención ya comprometida  
→ la Grulla observa  
→ planifica el turno siguiente

La intención actual nunca cambia después de leer la acción del jugador.

## 6. Anti-spam de la propia Grulla

El primer sparring encontró un problema real:

una Utility demasiado agresiva podía seleccionar repetidamente el gran ataque contra jugadores prudentes.

Eso sería dificultad falsa.

Se añadió penalización/cooldown cognitivo a acciones recientes, incluyendo:

- Tormenta de Mil Plumas;
- Recordar el Filo;
- Eco del Meridiano;
- Cerrar las Alas;
- Campana sin Dueño;
- Ala Vacía;
- Pata Inmóvil;
- preparaciones de plan.

Ahora la Grulla puede insistir sobre una debilidad sin repetir siempre la misma acción.

## 7. Suite dirigida

Archivo:

tests/grulla-boss-brain.test.mjs

Resultado local:

PASS: 10  
FAIL: 0

La suite comprueba:

1. Fase I conserva ciclo fijo.
2. Fase II reconoce spam de técnica.
3. Fase II distingue spam de gasto de qi.
4. Fase II hereda sólo resumen de Fase I.
5. Fase III puede preparar anti-repetición.
6. Variar rompe ese plan.
7. Repetir arma y completa el plan.
8. Una acción sin qi rompe el plan de circulación.
9. Una interrupción elimina el plan.
10. Información futura/oculta no altera la decisión.

## 8. Sparring por arquetipos

Benchmark:

benchmark/grulla-brain-capability-benchmark-v0.1.mjs

Este benchmark prueba el cerebro, no el daño completo.

### SPAMMER

Repite la misma técnica y elemento.

Fase II, 12 turnos:

- 9 respuestas tácticas/counters;
- 5 intenciones distintas.

Fase III, 16 turnos:

- 7 planes armados;
- 7 completados;
- 0 rotos.

La repetición constante alimenta la capacidad de contra-juego del boss.

### QI_BURNER

Varía técnica, pero gasta qi casi todos los turnos.

Fase III:

- 4 planes de circulación armados;
- 4 completados.

La Grulla no confunde gasto de qi con spam elemental.

### VARIED

Mezcla básicos, técnicas, control, defensa y recuperación.

Fase III:

- 0 planes completados;
- 2 planes rotos;
- 5 intenciones distintas.

La variedad reduce la posibilidad de convertir observación en remate.

### GOOD_READER

Lee intenciones y cambia deliberadamente su respuesta.

Fase III:

- 0 planes completados;
- 1 plan roto explícitamente;
- variedad de ataques y defensas conservada.

Romper planes no trivializa el combate: sólo evita que la Grulla convierta el hábito del jugador en una ventaja automática.

## 9. Las siete capacidades que examina

### C1 — Leer

Reconocer telegraphs y distinguir preparación de ejecución.

### C2 — Conservar

No gastar qi por inercia.

### C3 — Variar

No resolver todo con una sola técnica o elemento.

### C4 — Defender

Usar defensa, guardia o esquiva en ventanas apropiadas.

### C5 — Controlar

Interrumpir cuando romper un plan vale más que hacer daño.

### C6 — Engañar

Mostrar un patrón y abandonarlo cuando la Grulla intenta explotarlo.

### C7 — Adaptarse

Cambiar estrategia entre fases y llegar a la tercera con recursos.

El boss no exige que todas las builds tengan exactamente la misma herramienta.

Debe exigir que cada jugador use correctamente las herramientas que eligió.

## 10. Trabajo pendiente

Antes de convertirlo en boss jugable falta:

- conectar estas intenciones con Combat Ability Contract/executor;
- asignar efectos reales;
- probar todas las raíces y builds de LianQi IV;
- probar consumibles;
- probar control y Tenacidad reales;
- probar concordancias;
- probar afinidades elementales;
- fijar HP/ATQ/DEF/daño;
- simular las tres fases consecutivas;
- definir tasa de victoria objetivo.

## 11. Criterio de éxito

Una derrota justa debería poder explicarse con una causa legible:

- no leí la intención;
- repetí demasiado;
- vacié mi qi;
- no rompí el plan;
- defendí en la ventana equivocada;
- llegué sin recursos a Fase III.

Una victoria correcta debería sentirse así:

No superé una barra de vida. Entendí lo que la Grulla intentaba hacer y conseguí obligarla a equivocarse.
