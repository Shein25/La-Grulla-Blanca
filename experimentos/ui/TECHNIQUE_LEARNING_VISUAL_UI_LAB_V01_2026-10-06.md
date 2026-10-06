# TECHNIQUE LEARNING VISUAL UI LAB V01

**Fecha:** 2026-10-06  
**Estado:** ACTIVO / SOLO UI VISUAL / CHAT SEPARADO

## Corrección de alcance

Este documento **supersede** cualquier interpretación previa que haya planteado un laboratorio visual AOE como respuesta a esta idea.

La decisión humana correcta es:

> Cuando el personaje aprende una técnica, la UI debe mostrar durante unos segundos una secuencia visual que simule que realmente la está entrenando/practicando, usando una barra de progreso animada.

## Objetivo

Diseñar y prototipar únicamente la **presentación visual del aprendizaje de una técnica**.

Ejemplo conceptual:

```text
ENTRENAMIENTO

Palma Ardiente

██████████████░░░░░░░░  63%

Repites la circulación una vez más...
El qi comienza a estabilizarse.
```

La barra no representa un nuevo sistema mecánico. Es una representación narrativa/visual de un aprendizaje que el motor ya resolvió.

## Semántica dura

- El motor decide si la técnica fue aprendida/desbloqueada.
- La UI sólo representa visualmente ese evento.
- No crear una segunda progresión.
- No agregar XP.
- No agregar probabilidades.
- No modificar requisitos.
- No modificar maestría real.
- No bloquear el aprendizaje por el resultado de la animación.
- No agregar reloj sistémico ni timers persistentes.
- La duración de la secuencia es sólo presentación local.
- No tocar balance.
- No tocar combate.
- No tocar T0–T4.
- No tocar Ultis.
- No main.
- No merge.

## Sensación buscada

La animación debe transmitir que el personaje está **practicando de verdad**:

1. inicio del entrenamiento;
2. primeros intentos;
3. pequeñas dificultades/correcciones;
4. progreso irregular, no una carga lineal perfecta;
5. comprensión final;
6. revelación de la técnica aprendida.

Ejemplo de progresión visual:

`8 → 21 → 35 → 42 → 42 → 47 → 66 → 81 → 100`

Puede existir una pausa breve o un pequeño retroceso puramente visual para representar dificultad, pero el resultado final no cambia porque el aprendizaje ya fue resuelto por el motor.

## Textos dinámicos posibles

Deben depender del contexto de aprendizaje cuando esa información exista.

### Maestro
- Observas la postura.
- Repites el movimiento.
- Corriges la respiración.
- El instructor vuelve a mostrarte el flujo.
- Finalmente comprendes la intención.

### Manual
- Estudias el diagrama.
- Repites la circulación indicada.
- Algo no encaja.
- Relees el pasaje.
- El patrón finalmente cobra sentido.

### Comprensión propia
- Recuerdas el movimiento.
- Intentas reproducir la sensación.
- El qi se dispersa.
- Ajustas el flujo.
- Una comprensión repentina atraviesa tu mente.

### Legado / transmisión
Puede tener una presentación más excepcional, pero sigue siendo únicamente UI.

## Resultado visual esperado

Al 100%:

```text
████████████████████████████ 100%

        ✦ COMPRENSIÓN ALCANZADA ✦

             PALMA ARDIENTE

        Has aprendido la técnica.
```

## Diseño

Debe adaptarse al estilo xianxia/UI existente de La Grulla Blanca.

Preferencias:
- panel modal o panel de foco;
- barra claramente visible;
- color ligado a rama/elemento cuando sea apropiado;
- texto narrativo breve que cambia con el progreso;
- animación suave;
- evitar aspecto de instalador/software moderno;
- debe sentirse como entrenamiento/cultivación.

## Duración

La duración se estudia sólo como UX.

Objetivo inicial de prototipo:
- técnica normal: ~3–5 s;
- evento excepcional: podría durar un poco más.

No usar esto como tiempo real de aprendizaje del sistema.

## Prototipos solicitados

Explorar 2–3 variantes visuales:

A. **Entrenamiento físico**
- barra + frases de repetición/corrección.

B. **Circulación de Qi**
- barra + estados de flujo/meridianos/comprensión.

C. **Comprensión xianxia**
- barra irregular + breve bloqueo narrativo + salto final de comprensión.

## Entregable

El chat visual separado debe producir:
1. propuesta visual;
2. 2–3 variantes;
3. mockup/prototipo aislado;
4. recomendación;
5. opcionalmente HTML/CSS/JS independiente para probar el efecto.

No implementar todavía en el HTML productivo.
