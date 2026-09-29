# Pass 3 — evaluación exhaustiva de combinaciones de ramas

Fecha: 2026-09-29  
Rama: experiment/combat-stat-contract-v0.1  
Estado: **375/405 BUILDS SIMULADAS · SIN CAMBIOS CANÓNICOS**

## 0. Alcance

Cada técnica posee 3 elecciones en cada uno de 3 tramos:

~~~text
3 × 3 × 3 = 27 builds por técnica
15 técnicas = 405 builds teóricas
~~~

Se excluyen equipo, injerto, Concordancias, consumibles y buffs externos. Se incluye únicamente la raíz principal natural y las mecánicas internas de la técnica.

Perfiles principales siguen el Pass 2:

~~~text
COMMON: HP18 · DEF3 · paquete5
ELITE: HP34 · DEF6 · paquete8
Grupo: 3 COMMON simultáneos
~~~

Para pruebas que necesitan Evasión se usa sensibilidad Evasión20; no se declara como valor canónico de criatura.

---

# 1. Cobertura

| Elemento | Builds teóricas | Simuladas | Bloqueadas por especificación |
|---|---:|---:|---:|
| Fuego | 81 | 73 | 8 |
| Metal | 81 | 73 | 8 |
| Agua | 81 | 81 | 0 |
| Tierra | 81 | 67 | 14 |
| Viento | 81 | 81 | 0 |
| **TOTAL** | **405** | **375** | **30** |

Los bloqueos no son fallos del simulador: el documento de técnica no define qué hace la rama en esas combinaciones mixtas.

---

# 2. FUEGO

Detalle completo: SIMULACION_PASS3_COMBINACIONES_FUEGO_2026-09-29.md.

## Palma Ardiente

Contra COMMON, DIR-DIR-DIR conserva el mejor tempo (~1.85 turnos).

Contra ELITE aparecen mezclas superiores:

| Build | TTK | HP final | Qi |
|---|---:|---:|---:|
| DOT-DIR-DIR | ~2.99 | ~12.08 | ~20.93 |
| DOT-DIR-EFF | ~3.00 | ~12.00 | **18.00** |
| DIR-DIR-DIR | ~3.59 | ~7.26 | ~25.15 |

Conclusión: la ruta directa pura no domina universalmente. La combinación de una capa DOT temprana con daño/eficiencia posterior produce builds reales y competitivas.

## Círculo

En el stress de 3 COMMON:

| Build | Clear | Qi medio |
|---|---:|---:|
| DIR-DIR-DIR | **~61.9%** | ~31.2 |
| EFF-DIR-DIR | ~48.2% | ~27.2 |
| DOT-EFF-DIR | ~47.7% | ~22.2 |
| DOT-DOT-DOT | ~47.2% | ~22.2 |

El burst puro conserva un nicho claro porque mata enemigos antes de que actúen.

## Cuerpo-Horno

Mejores mezclas observadas contra ELITE usando Palma Directa después de activar Horno:

| Build | TTK | HP final | Qi |
|---|---:|---:|---:|
| CONV-CONV-EFF | ~3.72 | ~10.24 | ~25.04 |
| CONV-CONV-CONV | ~3.72 | ~10.20 | ~26.07 |
| CONV-CONV-BAR | ~3.73 | **~12.19** | ~26.08 |

Conversión pura no domina: eficiencia o barrera en Tramo III crean intercambios útiles.

### Hueco FUEGO-01

Calor Acumulado (Tramo III) sólo define la ruta CONV-CONV-CONV. Ocho combinaciones con CONV en Tramo III no tienen efecto standalone/mixed definido.

---

# 3. METAL

## Destello de Plata — 27/27

Con ELITE DEF6 y Evasión20 de sensibilidad:

| Build | Kill ≤6 | Lectura |
|---|---:|---|
| PEN-PEN-PRE | **~66.6%** | mejor equilibrio penetración + precisión/crítico |
| PEN-PEN-EFF | ~52.2% | penetración con mejor coste |
| PEN-PEN-PEN | ~52.0% | penetración máxima |
| PRE-PRE-PRE | ~1.2% | pierde demasiado contra DEF6 |

Contra un objetivo más blindado (DEF9, Evasión20), PEN-PEN-PEN vuelve a ser la mejor (~52%).

### M3-DESTELLO-01

El Pass 3 matiza el hallazgo del +7 plano:

- sigue siendo muy potente;
- pero la ruta completa PEN no domina todo;
- PEN-PEN-PRE gana contra defensa media con Evasión;
- PEN-PEN-PEN conserva su nicho contra defensa alta.

Por tanto, el +7 plano permanece candidato a ajuste, pero ya no debe reducirse antes de explorar una nueva escala canónica de DEF.

## Armadura de Plata — 27/27

Paquete 8:

~~~text
3 impactos: RES-RES-RES evita 24/24
4 impactos: RES-RES-RES y RES-RES-QTY evitan 24
8 impactos: RES-RES-RES, RES-RES-QTY, QTY-QTY-RES y QTY-QTY-QTY convergen en ~24 evitado, pero con distribución temporal distinta
~~~

Lectura:

- resistencia domina ráfaga corta;
- cantidad domina cobertura sostenida;
- mezclas resistencia/cantidad ocupan puntos intermedios;
- adaptación no puede juzgarse sin Control real.

Estado: estructura de ramas saludable.

## Lluvia de Filos

En 3 COMMON, entre builds con semántica cerrada:

| Build | Clear |
|---|---:|
| DIR-DIR-DIR | **~45.8%** |
| DIR-DIR-EFF | ~2.9% |
| RUP-DIR-DIR | ~0.8% |

Ruptura no paga su inversión dentro de un combate grupal tan corto; su valor debe probarse con aliados o enemigos de mayor HP.

### Hueco METAL-01

Defensa Quebrada (Tramo III) declara -1 DEF sola y -3 DEF durante 3 turnos para la ruta completa, pero no define duración para las combinaciones mixtas que la seleccionan sin RUP-RUP.

Ocho builds quedan bloqueadas.

---

# 4. AGUA

## Latigazo — 27/27 con sensibilidad de Control

No existe base_control canónico, por lo que se probaron dos escenarios de sensibilidad antes de sumar raíz/rama.

Con baseline30:

| Build | Kill ≤6 | skips medios |
|---|---:|---:|
| DIR-DIR-DIR | ~88.0% | ~1.01 |
| DIR-DIR-CTL | ~74.1% | ~1.49 |
| CTL-DIR-DIR | ~68.2% | ~1.54 |
| DIR-DIR-EFF | ~60.6% | ~1.21 |

Con baseline50:

| Build | Kill ≤6 | skips medios |
|---|---:|---:|
| DIR-DIR-DIR | ~97.2% | ~1.41 |
| DIR-DIR-CTL | ~92.1% | ~1.94 |
| CTL-DIR-DIR | ~90.0% | ~2.04 |

Lectura: las mezclas de Control intercambian daño por más acciones enemigas anuladas. El árbol responde bien, pero no puede cerrarse numéricamente hasta fijar base_control/Tenacidad.

## Espejo de Luna — 27/27

Contra paquetes 5–8, las mezclas con Reserva siguen dominando el valor inmediato.

Ejemplos de Absorción total aproximada en la activación:

| Build | paquete5 | paquete8 |
|---|---:|---:|
| RES-RES-RES | ~10 | ~8 |
| REG-REG-RES | ~7 | ~7 |
| REG-REG-REG | ~5 | ~5 |
| EFF-EFF-EFF | ~3 | ~3 |

### A3-ESPEJO-01

La mejor versión de Regeneración no corrige el problema de una reserva máxima demasiado pequeña: si el primer impacto rompe el pool, Reflujo tiene poco espacio operativo.

REG-REG-RES muestra una pista útil: añadir una sola rama de Reserva hace mucho más viable la idea de reconstrucción.

## Marea — 27/27

En 3 COMMON del stress actual:

| Build | Clear |
|---|---:|
| DIR-DIR-DIR | ~19.1% |
| DIR-DIR-DEB | ~2.6% |
| DIR-DIR-EFF | ~1.1% |

Las ramas de debilitación reducen presión enemiga, pero no compensan una ronda adicional de ataques en este escenario.

No buffear daño todavía: Marea debe probarse como apertura de Latigazo/Control, no sólo como herramienta de limpieza.

---

# 5. TIERRA

## Golpe de Montaña

Con ELITE DEF6/Evasión20:

| Build | Kill ≤6 |
|---|---:|
| DIR-DIR-DIR | **~53.9%** |
| PRS-DIR-DIR | ~9.9% |
| DIR-DIR-STB | ~9.7% |

La ruta directa sigue siendo la mejor para un duelo corto, pero Presión requiere un objetivo con suficiente Evasión/HP para recuperar la inversión.

### Hueco TIERRA-01

Anclaje de Montaña (Tramo III Presión) sólo define el resultado de la ruta PRS-PRS-PRS. Ocho builds mixtas con esa elección no tienen magnitud standalone declarada.

## Piel de Cobre — 27/27 bajo presión directa

Contra seis paquetes 8:

| Build | HP final aproximado | daño evitado |
|---|---:|---:|
| FOR-END-END | **21** | ~36 |
| FOR-FOR-END | 19 | ~36 |
| END-END-FOR | 19 | ~34 |
| END-FOR-END | 16 | ~33 |
| FOR-FOR-FOR | 4 | ~21 |
| END-END-END | 13 | ~28 + curación |

### T3-PIEL-01

El mejor resultado no es una ruta pura sino FOR-END-END: fortificación temprana + persistencia posterior.

Esto confirma que Piel no debe nerfearse mirando únicamente su DEF máxima. La duración es parte decisiva de su valor.

## Temblor de Montaña

Con Evasión20 sintética y 3 COMMON:

| Build | Clear |
|---|---:|
| DIR-DIR-DIR | **~14.5%** |
| DIR-DIR-PRE | ~0.6% |
| DIR-DIR-DEB | ~0.4% |

El stress con Evasión20 reduce drásticamente el 100% observado anteriormente con Evasión0, demostrando que los perfiles de Evasión enemigos son críticos para el balance de Tierra.

### Hueco TIERRA-02

Eco de la Falla (Tramo II Preparación) dice que funciona sin Tramo I generando una “versión menor”, pero no declara cuánta Precisión concede esa versión.

Seis builds que eligen PRE en Tramo II sin PRE en Tramo I quedan bloqueadas.

---

# 6. VIENTO

## Lanza que Parte Nubes — 27/27

ELITE DEF6/Evasión20:

| Build | Kill ≤6 |
|---|---:|
| DIR-DIR-DIR | **~34.7%** |
| DIR-DIR-PRE | ~20.0% |
| DIR-DIR-EFF | ~11.6% |
| DIR-PRE-DIR | ~6.3% |
| PRE-DIR-DIR | ~3.9% |

### V3-LANZA-01

El exhaustivo confirma el problema de Lanza: incluso la mejor mezcla Precisión/Crítico sigue por detrás de mantener daño directo en los tres tramos.

El siguiente ajuste debe actuar aquí; no hace falta esperar al equipo.

## Paso de Nube Ligera — 27/27

Cuatro ataques de paquete8, Precisión enemiga100:

| Build | daño evitado | prob. de preparar respuesta |
|---|---:|---:|
| EFF-EFF-EFF | **~8.0** | — |
| EFF-EFF-EVA | ~7.2 | — |
| EVA-EVA-EVA | ~6.4 | — |
| EFF-EFF-RSP | ~6.0 | ~57.7% |
| EVA-EVA-RSP | ~5.6 | ~58.0% |

Lectura:

- duración/eficiencia gana valor acumulado;
- evasión pura gana intensidad por turno;
- respuesta mezcla defensa con preparación de la siguiente técnica.

Estado: árbol saludable; no requiere ajuste inmediato.

## Tijera del Vendaval Partido — 27/27

3 COMMON con Evasión20:

| Build | Clear |
|---|---:|
| DIR-DIR-DIR | **~34.7%** |
| DIR-DIR-INT | ~2.6% |
| DIR-DIR-FLOW | ~1.7% |

La ruta Tempestad completa sigue muy por encima en limpieza directa. Interferencia/Flujo deben medirse como apertura o soporte, no como burst.

---

# 7. Resultado del Pass 3

## Hallazgos numéricos que siguen vivos

1. **Lanza**: diferencia excesiva entre ruta de daño y Precisión/Crítico.
2. **Espejo**: reserva inicial demasiado pequeña para que Reflujo/duración compitan de forma consistente.
3. **Destello**: +7 Penetración plana sigue siendo muy agresivo, pero el exhaustivo muestra que la ruta completa sólo domina claramente contra DEF alta.

## Hallazgos retirados o debilitados

- Golpe de Montaña: no hay evidencia de nerf inmediato.
- Piel de Cobre: no hay evidencia de nerf global; las builds mixtas revelan tradeoffs reales.
- Palma DOT: no hay evidencia de nerf inmediato.
- Armadura de Plata: resistencia/cantidad mantienen nichos distintos.
- Paso de Nube Ligera: árbol sano.

## Problema estructural nuevo

30/405 builds no tienen semántica completa por documentación insuficiente. Antes del Pass 4 deben cerrarse:

~~~text
FUEGO · Cuerpo-Horno · T3 Conversión · efecto standalone/mixed
METAL · Lluvia · T3 Ruptura · duración standalone/mixed
TIERRA · Golpe · T3 Presión · efecto standalone/mixed
TIERRA · Temblor · T2 Preparación · magnitud de versión menor
~~~

## Próxima operación

1. cerrar esos cuatro huecos sin cambiar identidad;
2. repetir únicamente las 30 builds bloqueadas;
3. después simular kits mixtos entre las tres técnicas de cada elemento;
4. sólo entonces aplicar los primeros cambios numéricos canónicos.
