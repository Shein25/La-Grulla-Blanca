# Resultado — Grulla · benchmark integral de tres fases v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / CALIBRACIÓN, NO CANÓNICO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Objetivo

Medir por primera vez el cerebro completo de la Grulla atravesando consecutivamente:

```text
I   EL VOTO INMÓVIL      — PROGRAMADA
II  LAS ALAS RECUERDAN   — ADAPTATIVA
III LA CAMPANA SIN DUEÑO — MAESTRA
```

contra las variantes reales de meridianos disponibles a LianQi IV.

No se buscó todavía fijar el balance numérico definitivo.

---

## 2. Jugadores simulados

Se probaron las tres raíces iniciales:

- Fuego / Palma;
- Metal / Filo;
- Agua / Látigo.

Cada técnica se prueba con:

```text
3 opciones de tramo 1
×
3 opciones de tramo 2
=
9 builds por raíz
```

Total:

```text
27 builds LianQi IV
```

Se usa maestría 2, que es el techo de LianQi en ver74.

La afinidad principal replica `statsTecnica()`:

- coste −1 con suelo de 70%;
- daño +1.

Loadout preparado de referencia:

```text
+2 Ataque
+7 Defensa
ataque básico 1d8
```

Las técnicas opcionales Paso/Piel/Filamento NO participan.

---

## 3. Stats de la Grulla usados

Se reutilizó únicamente como punto de calibración el viejo candidato:

| Fase | HP | ATQ | DEF | Base |
|---|---:|---:|---:|---|
| I | 45 | 3 | 13 | 1d6+1 |
| II | 35 | 4 | 13 | 1d6+2 |
| III | 25 | 5 | 12 | 1d8+2 |

Total:

```text
105 HP
```

Estos números **no se declaran canónicos**.

---

## 4. Efectos provisionales del cerebro

Para poder medir el encuentro completo se asignaron efectos de laboratorio utilizando sólo conceptos que `Combate` ya soporta:

- ataque;
- precisión;
- Defensa;
- Esquiva;
- Guardia/reserva;
- drenaje de qi;
- preparación.

No se añadió silencio ni bloqueo general de técnicas.

Los efectos numéricos concretos siguen siendo provisionales.

---

## 5. Estrategias evaluadas

### PURE_SINGLE_SKILL

La única herramienta ofensiva utilizada es siempre la técnica raíz.

No utiliza ataque básico.

### SINGLE_SKILL_WITH_DEFENSE

La única skill ofensiva sigue siendo la misma.

Puede usar DEFENDER frente a telegraphs peligrosos.

Esto comprueba que DEFENDER no sea un exploit para hacer olvidar el patrón.

### MINIMAL_ALTERNATE

Sólo utiliza herramientas garantizadas:

```text
técnica raíz
+
ataque básico
+
una curación
```

Alterna técnica y básico, pero no interpreta profundamente la intención enemiga.

### MINIMAL_READER

También utiliza únicamente el toolkit mínimo:

```text
técnica raíz
ataque básico
DEFENDER
una curación
```

pero además:

- rompe preparaciones con BASIC;
- no repite una técnica que ya fue comprendida;
- DEFENDER se reserva para remates o situaciones de vida comprometida;
- conserva qi;
- responde a los planes de Fase III.

No requiere Paso, Piel ni Filamento.

---

## 6. Agujero detectado en el primer barrido

La primera ejecución detectó una excepción extremadamente rara:

```text
SINGLE_SKILL_WITH_DEFENSE
Fuego
→ ~0,02% de victoria
```

Causa:

una Palma excepcionalmente fuerte podía permitir superar Fase I con sólo dos usos de la técnica.

La memoria de transición exigía tres.

Esto violaba el contrato:

> 100% una sola skill = 0% victoria.

### Corrección

Fase I funciona como una fase completa de observación.

Ahora:

```text
2+ ejecuciones de una única skill
+
ningún BASIC
+
ninguna técnica alternativa
→ Fase II la recuerda ya comprendida
```

Dentro de Fase II y III se mantiene la regla normal:

```text
3 usos consecutivos
→ counter aprendido
```

Además se corrigió el benchmark para limpiar al cambiar de fase los estados aplicados a la manifestación anterior de la Grulla, como Quemadura/debilitamiento.

---

## 7. Confirmación final

Se ejecutaron:

```text
27 builds
× 4 estrategias
× 1.000 duelos
=
108.000 duelos
```

### Invariantes

```text
PURE_SINGLE_SKILL             → 0% victoria en las 27 builds
SINGLE_SKILL_WITH_DEFENSE     → 0% victoria en las 27 builds
las tres raíces tienen ruta de victoria mínima
Paso/Piel/Filamento no son necesarios
```

Todos los invariantes del benchmark final se cumplen.

---

## 8. Resultados — estrategia mínima sin lectura avanzada

### MINIMAL_ALTERNATE

| Raíz | Promedio | Peor build | Mejor build |
|---|---:|---:|---:|
| Fuego | 52,7% | 45,4% | 64,9% |
| Metal | 47,4% | 34,1% | 57,2% |
| Agua | 50,3% | 41,3% | 66,8% |

Interpretación:

> variar ya evita el hard-counter, pero no garantiza dominar el encuentro.

---

## 9. Resultados — jugador que lee a la Grulla

### MINIMAL_READER

| Raíz | Promedio | Peor build | Mejor build |
|---|---:|---:|---:|
| Fuego | 59,5% | 47,6% | 74,6% |
| Metal | 53,5% | 39,4% | 66,0% |
| Agua | 53,8% | 37,7% | 74,1% |

El lector mejora sobre el simple alternador, especialmente en Fuego y Metal.

Esto demuestra que el telegraph y los planes tienen valor mecánico real.

---

## 10. Builds extremas observadas

### Fuego

Peor lector:

```text
Tramo 1 opción 3 — Chispa perseguidora
Tramo 2 opción 1 — Respiración frugal
47,6%
```

Mejor lector:

```text
Tramo 1 opción 2 — Palma compacta
Tramo 2 opción 2 — Pulso certero
74,6%
```

### Metal

Peor lector:

```text
Tramo 1 opción 3 — Filo oportunista
Tramo 2 opción 1 — Corte del vacío
39,4%
```

Mejor lector:

```text
Tramo 1 opción 2 — Filo pesado
Tramo 2 opción 2 — Corte dirigido
66,0%
```

### Agua

Peor lector:

```text
Tramo 1 opción 1 — Onda desgarradora
Tramo 2 opción 1 — Cauce continuo
37,7%
```

Mejor lector:

```text
Tramo 1 opción 2 — Azote profundo
Tramo 2 opción 2 — Curva imprevisible
74,1%
```

La dispersión entre ramas no se atribuye automáticamente al jefe.

Algunas combinaciones priorizan economía, crítico o debilitamiento frente a daño/precisión directa.

Debe revisarse después junto al balance general de meridianos.

---

## 11. Hallazgo principal

El viejo total provisional de 105 HP ya no puede evaluarse como una simple bolsa de vida.

Con el cerebro nuevo produce aproximadamente:

```text
spam absoluto          → 0%
variedad mínima        → ~47–53% promedio según raíz
lectura competente     → ~54–59% promedio según raíz
```

Por tanto la dificultad empieza a provenir del comportamiento, no exclusivamente de los stats.

No se recomienda subir HP/daño antes de probar las técnicas opcionales y el executor real.

---

## 12. Comprobación dirigida adicional

Después de corregir el agujero de transición se verificó directamente:

1. dos usos exclusivos en Fase I + DEFENDER → counter heredado;
2. la técnica heredada queda bloqueada;
3. RECOVER no borra el conocimiento;
4. BASIC rompe el counter.

Resultado:

```text
4/4 PASS
```

---

## 13. Próximo trabajo

El siguiente paso válido es incorporar al benchmark, una por una:

- Paso de Nube;
- Piel de Cobre;
- Filamento de Agua;

no como requisitos, sino para comprobar que:

1. ofrecen ventajas tácticas reales;
2. la Grulla aprende su abuso por tipo;
3. ninguna trivializa el boss;
4. ninguna se vuelve inútil por tener counter;
5. el toolkit mínimo sigue siendo viable.

Después de eso se podrá fijar una primera candidata real de HP/ATQ/DEF/daño.
