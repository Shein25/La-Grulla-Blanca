# Simulación elemental Pass 1 — sin equipo

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **SIMULACIÓN / NO MODIFICA BALANCE CANÓNICO**

## 0. Alcance

Objetivo: observar cómo se comportan las 15 técnicas por elemento **sin bonificaciones de equipo**.

Se usan dos capas:

1. **técnica pura**: sólo la técnica/rama;
2. **raíz natural**: añade únicamente los rasgos canónicos de la raíz principal correspondiente.

Se excluyen:

- equipo;
- injerto;
- Concordancias;
- consumibles;
- buffs externos;
- bonificaciones de set;
- afinidad elemental automática;
- resistencias elementales.

Las ramas propias de cada técnica sí forman parte de la simulación.

## 0.1 Advertencia sobre el runtime histórico

Los monstruos de `ver74` poseen valores `defensa: 9–16`, pero esa `defensa` histórica participa en la vieja tirada de impacto; **no puede reutilizarse directamente como la nueva DEF plana**.

Por tanto:

- HP y daño de criaturas actuales sirven como referencia aproximada de escala;
- la vieja `defensa` no se usa como DEF del contrato nuevo;
- se usa una escalera sintética de DEF plana: 0 / 3 / 6 / 9 para sensibilidad;
- no se asignan Evasión/Tenacidad nuevas a criaturas que todavía no las declaran.

Datos del runtime actual usados como referencia de escala:

```text
criaturas comunes:
HP mediano ≈ 18
daño medio mediano ≈ 4.5

criaturas únicas:
HP mediano ≈ 42
daño medio mediano ≈ 7
```

Para defensa se usan paquetes directos de prueba:

```text
5  = presión común
8  = presión fuerte/élite
12 = stress test
```

El jugador de LianQi IV sin equipo conserva como referencia histórica 28 Vida máxima. Para Tierra, la raíz natural elevaría aproximadamente esa referencia a 31 por su +10% Vida máxima.

---

# 1. FUEGO

Rasgos de raíz natural incluidos en la segunda capa:

```text
+10% daño directo general
+5 pp crítico
```

## 1.1 Palma Ardiente — ruta directa completa

Daño esperado por lanzamiento:

| DEF | Técnica pura | Con raíz Fuego |
|---:|---:|---:|
| 0 | 16.96 | 18.53 |
| 3 | 13.96 | 15.53 |
| 6 | 10.96 | 12.53 |
| 9 | 7.96 | 9.53 |

Coste de la ruta: 7 Qi.

Lectura:

- la raíz Fuego devuelve a Palma el liderazgo ofensivo esperado;
- Golpe de Montaña deja de ser un outlier evidente cuando se compara raíz contra raíz;
- la ruta directa conserva buen margen frente a DEF creciente.

## 1.2 Palma Ardiente — ruta DOT completa, seis turnos

Supuesto:

- una aplicación por turno;
- 20% nominal × 4 ticks;
- máximo 4 stacks;
- tick al comienzo del turno afectado;
- DOT ignora DEF;
- se contabiliza lo efectivamente realizado dentro de seis turnos y también el daño todavía pendiente.

Con raíz Fuego:

| DEF | Ruta directa · 6t | DOT realizado · 6t | DOT incluyendo ticks pendientes |
|---:|---:|---:|---:|
| 0 | 111.18 | 105.30 | 117.30 |
| 3 | 93.18 | 87.30 | 99.30 |
| 6 | 75.18 | 69.30 | 81.30 |
| 9 | 57.18 | 51.30 | 63.30 |

### Hallazgo F-01

La ruta DOT **no domina durante el combate activo corto**.

Durante seis turnos la ruta directa permanece por encima. La ruta DOT la supera sólo cuando el combate permite cobrar los ticks pendientes.

Esto indica que `20% × 4` no debe nerfearse por la comparación estática de “daño total por aplicación”.

Estado: **SIN AJUSTE POR AHORA**.

## 1.3 Cuerpo-Horno

Referencia HP = 28.

```text
Base:
15% HP → 4 Absorción aprox.

Ruta barrera completa:
35% HP → 10 Absorción aprox.
```

Daño total evitado contra una secuencia de hasta cuatro impactos:

| Paquete enemigo | Base | Ruta barrera |
|---:|---:|---:|
| 5 | 4 | 10 |
| 8 | 4 | 10 |
| 12 | 4 | 10 |

La reserva base se rompe ante un impacto común de 5, por lo que su duración de 2 turnos rara vez importa contra paquetes de ese tamaño.

La ruta barrera, en cambio, absorbe aproximadamente dos ataques comunes.

### Hallazgo F-02

Base Cuerpo-Horno puede ser demasiado frágil si la escala futura de paquetes directos ronda 5+.

No modificar hasta cerrar la nueva escala de daño de enemigos.

## 1.4 Círculo de las Cien Ascuas

Ruta directa completa con raíz Fuego.

Daño esperado por objetivo:

| DEF | Grupo · sin 0.65 | Duelo · 0.65 |
|---:|---:|---:|
| 0 | 12.21 aprox. | 7.94 |
| 3 | 9.21 aprox. | 4.94 |
| 6 | 6.21 aprox. | 1.94 |
| 9 | 3.21 aprox. | 0.40 |

En 3 objetivos con DEF 3:

```text
≈ 27.6 daño total
≈ 2.30 daño/Qi
```

Estado: buen comportamiento grupal; el problema sigue siendo el 0.65 + DEF plana en duelo.

---

# 2. METAL

Rasgos de raíz natural:

```text
+10 pp Penetración %
+5 Precisión
```

## 2.1 Destello de Plata — penetración vs crítico/precisión

Ruta de penetración completa:

```text
técnica: +25 pp Penetración % propia
técnica: +7 Penetración plana según texto de ruta completa
raíz: +10 pp Penetración %
total benchmark: 35% + 7 plana
```

Daño esperado:

| DEF | Penetración | Crítico/Precisión |
|---:|---:|---:|
| 0 | 9.23 | 9.95 |
| 3 | 9.23 | 7.25 |
| 6 | 9.23 | 4.55 |
| 9 | 9.23 | 1.85 |
| 12 | 8.43 | 0.68 |
| 16 | 5.83 | 0.14 |

### Hallazgo M-01 — ALTO

La Penetración plana `+7` es enorme respecto de una técnica cuyo daño nominal es 9.

La ruta de penetración:

- pierde levemente contra DEF 0;
- supera a la ruta crítica desde aproximadamente DEF 1;
- neutraliza casi por completo una escalera DEF 3–9.

Esto puede hacer que la decisión de ruta deje de ser una elección real.

**CANDIDATO PRINCIPAL A AJUSTE NUMÉRICO.**

No se modifica todavía.

## 2.2 Lluvia de Filos

Con raíz Metal.

Ruta de daño vs ruta de ruptura:

| DEF | Daño · por objetivo | Ruptura · primer impacto | Ruptura · impactos posteriores con −3 DEF |
|---:|---:|---:|---:|
| 0 | 9.54 | 6.15 | 6.15 |
| 3 | 7.14 | 4.20 | 6.15 |
| 6 | 4.74 | 2.25 | 4.20 |
| 9 | 2.34 | 0.30 | 2.25 |
| 12 | 0.48 | 0.06 | 0.30 |

La ruta de ruptura no compite en daño personal inmediato; su valor real es bajar DEF para impactos posteriores y para otros actores.

Estado: **coherente si su función es apoyo de ruptura**, pero deberá probarse en combate grupal real.

## 2.3 Armadura de Plata

Daño evitado en cuatro impactos:

| Paquete | Base 3×+3 | Resistencia 3×+8 | Cantidad 8×+3 |
|---:|---:|---:|---:|
| 5 | 9 | 15 | 12* |
| 8 | 9 | 24 | 12* |
| 12 | 9 | 24 | 12* |

`*` sólo se simulan cuatro impactos; la ruta cantidad conserva cuatro Placas adicionales.

Lectura:

- resistencia domina contra pocos golpes fuertes;
- cantidad domina en encuentros largos/multigolpe;
- ambas convergen a un techo teórico de 24 mitigación si todos los impactos son suficientemente grandes y se consumen todas las Placas.

Estado: **MUY BUENA DIFERENCIACIÓN DE RUTAS**.

---

# 3. AGUA

Rasgos de raíz natural:

```text
−10% coste de Qi
+5 Control
```

No se asigna una probabilidad absoluta a Arrastre en este Pass porque el `base_control` de la técnica y la Tenacidad nueva de los enemigos todavía no tienen valores canónicos.

## 3.1 Latigazo de Marea — ruta daño

Con raíz Agua, coste 7 × 0.90 → aproximadamente 6 Qi al pago discreto.

| DEF | Daño esperado | Daño/Qi |
|---:|---:|---:|
| 0 | 13.86 | 2.31 |
| 3 | 10.86 | 1.81 |
| 6 | 7.86 | 1.31 |
| 9 | 4.86 | 0.81 |

Además conserva Arrastre base.

### Hallazgo A-01

La ruta de daño no parece excesiva una vez entra DEF, pero el valor total de Latigazo depende muchísimo de la probabilidad real de Arrastre.

Pendiente obligatorio:

```text
definir base_control de Arrastre
definir Tenacidad de perfiles enemigos
```

antes de balance final.

## 3.2 Espejo de Luna

HP de referencia = 28.

### Base

```text
12% HP → 3 Absorción aprox.
Reflujo = 25%
duración = 3
```

Contra paquetes 5/8/12:

```text
se rompe en el primer impacto
daño evitado ≈ 3
Reflujo no llega a operar
```

### Ruta reserva completa

```text
30% HP → 8 Absorción aprox.
Reflujo base 25%
duración base 3
```

Daño evitado:

| Paquete | Mitigación aproximada |
|---:|---:|
| 5 | 10 |
| 8 | 8 |
| 12 | 8 |

### Ruta regeneración completa

Con reserva base de sólo 12%, incluso Reflujo 50% + reconstrucción 50% produce aproximadamente:

```text
5 daño evitado
```

frente a cuatro paquetes de 5–12.

### Hallazgo A-02 — ALTO

Las rutas de Espejo dependen demasiado de la reserva inicial.

Si un único impacto rompe la reserva:

- Reflujo pierde valor;
- duración pierde valor;
- la ruta regeneración puede ser claramente inferior a reserva.

Esto merece ajuste tras fijar escala de daño entrante.

## 3.3 Marea de las Ocho Orillas

Ruta daño con raíz Agua.

Coste aproximado: 9 Qi tras rasgo de raíz.

En duelo:

| DEF | Daño esperado | Daño/Qi |
|---:|---:|---:|
| 0 | 6.14 | 0.68 |
| 3 | 3.14 | 0.35 |
| 6 | 0.28 | 0.03 |
| 9 | 0.00 | 0.00 |

En grupo sigue aportando Desbalance a cada impacto conectado y la eficiencia total crece por número de enemigos.

Estado: el problema no parece Marea en particular, sino la interacción global **AOE 0.65 + DEF plana**.

---

# 4. TIERRA

Rasgos de raíz natural:

```text
+10% Vida máxima
+5 Tenacidad
```

No aumentan directamente el daño.

## 4.1 Golpe de Montaña — seis turnos

Ruta de daño completa:

- primeros golpes: +65%;
- una vez Peso está al máximo: +80% total provisional;
- coste 6 Qi.

| DEF | Antes de Peso máx. | Con Peso máx. | Daño 6 turnos | Daño/Qi |
|---:|---:|---:|---:|---:|
| 0 | 15.22 | 16.61 | 96.86 | 2.69 |
| 3 | 12.22 | 13.61 | 78.86 | 2.19 |
| 6 | 9.22 | 10.61 | 60.86 | 1.69 |
| 9 | 6.22 | 7.61 | 42.86 | 1.19 |

Comparación importante:

Con raíz natural, Palma directa produce en seis turnos:

```text
DEF 3 → 93.18
DEF 6 → 75.18
```

Golpe produce:

```text
DEF 3 → 78.86
DEF 6 → 60.86
```

### Hallazgo T-01

El Pass 0 había marcado Golpe como posible outlier porque comparaba técnicas sin sus raíces naturales.

Con la raíz elemental incluida, Golpe ya no supera a Fuego en presión directa.

**Se retira por ahora la propuesta automática de +1 Qi a Impacto Profundo.**

Peso sigue aportando utilidad, por lo que se mantiene en observación, pero no hay evidencia suficiente para nerf inmediato.

## 4.2 Piel de Cobre

Raíz Tierra:

```text
HP benchmark ≈ 31
umbral de 10% ≈ 3.1 HP
```

### Base

Mitigación incremental en cuatro impactos:

| Paquete | Daño evitado total |
|---:|---:|
| 5 | 17 |
| 8 | 18 |
| 12 | 18 |

### Ruta fortificación completa — lectura literal provisional

La combinación actual puede producir aproximadamente:

```text
1 Arraigo → +5 DEF
2 Arraigos → +8 DEF
3 Arraigos → hasta +12 DEF
```

Contra cuatro impactos:

| Paquete | Daño evitado |
|---:|---:|
| 5 | 20/20 |
| 8 | 29/32 |
| 12 | 41/48 |

Un golpe de 8–12 que atraviese la DEF inicial puede activar el umbral del 10%, llevar Arraigo rápidamente al máximo y hacer que los siguientes impactos directos queden casi o totalmente anulados.

### Hallazgo T-02 — ALTO

La ruta completa de fortificación de Piel parece **demasiado fuerte para la escala actual**.

El problema no es la identidad de Arraigo, sino la suma simultánea de:

- +2 DEF inmediata;
- +2 DEF por Arraigo;
- Estratos Compactos;
- sinergia adicional al máximo;
- Cuerpo de Roca.

Debe revisarse numéricamente.

## 4.3 Temblor de Montaña

Ruta de daño en duelo:

| DEF | Daño esperado |
|---:|---:|
| 0 | 6.20 |
| 3 | 3.20 |
| 6 | 0.34 |
| 9 | 0.04 |

En grupo de 3 contra DEF 3:

```text
≈ 19.62 daño total
≈ 1.78 daño/Qi
```

más Suelo Inestable según la rama elegida.

Estado: coherente en grupo; penalización de duelo vuelve a ser el punto a revisar globalmente.

---

# 5. VIENTO

Rasgos de raíz natural:

```text
+10 Evasión
+5% Daño Crítico
```

## 5.1 Lanza que Parte Nubes

Se comparan dos especializaciones contra DEF 3.

### Ruta impacto

```text
+60% directo
Precisión propia base de Lanza: +5
crítico efectivo: 10%
Daño Crítico con raíz Viento: ×1.55
coste: 7
```

### Ruta precisión/crítico

Lectura provisional de ruta completa:

```text
Precisión propia total aprox.: +20
crítico efectivo: 20%
Daño Crítico con raíz: ×1.65
coste: 6
```

Sensibilidad a Evasión objetivo:

| Evasión | Impacto: daño esperado | Precisión: daño esperado |
|---:|---:|---:|
| 0 | 10.50 | 6.04 |
| 10 | 9.98 | 6.04 |
| 20 | 8.93 | 6.04 |
| 30 | 7.88 | 5.44 |
| 40 | 6.83 | 4.83 |
| 60 | 4.73 | 3.62 |
| 80 | 2.63 | 2.42 |
| 90 | 1.58 | 1.81 |

Por eficiencia de Qi, la ruta precisión recién alcanza a la ruta impacto aproximadamente en Evasión 75+.

### Hallazgo V-01 — ALTO

La ruta precisión/crítico de Lanza necesita enemigos con Evasión extremadamente alta para competir con +60% daño.

Eso pone en riesgo la elección de build.

Candidatos para Pass 2:

- reducir el +60% total de la ruta impacto;
- añadir algo de daño directo moderado a la ruta precisión;
- aumentar el valor crítico de la ruta precisión;
- combinación moderada.

No aplicar todavía.

## 5.2 Paso de Nube Ligera

Contra enemigo de Precisión 100:

```text
raíz Viento = +10 Evasión
Paso base = +15
total base = 25 Evasión
```

Probabilidad de impacto enemiga aproximada:

```text
75%
```

Ruta evasión completa:

```text
+30 Evasión de Paso
+10 raíz
= 40 Evasión
→ enemigo Precision 100 impacta 60%
```

Ruta duración:

```text
25 Evasión total
duración 4
```

Daño esperado evitado en paquetes repetidos:

| Paquete | Evasión completa · 2 turnos | Duración · 4 turnos |
|---:|---:|---:|
| 5 | 4.0 | 5.0 |
| 8 | 6.4 | 8.0 |
| 12 | 9.6 | 12.0 |

### Hallazgo V-02

La ruta duración puede evitar más daño total que la ruta de Evasión máxima si recibe un ataque por turno.

Esto no es necesariamente malo:

- evasión = protección más intensa e inmediata;
- duración = protección menor pero sostenida.

Estado: **diferenciación saludable**.

## 5.3 Tijera del Vendaval Partido

Ruta Tempestad con raíz Viento.

Duelo:

| DEF | Daño esperado |
|---:|---:|
| 0 | 6.42 |
| 3 | 3.42 |
| 6 | 0.55 |
| 9 | 0.10 |

Grupo de 3 contra DEF 3:

```text
≈ 20.63 daño total
≈ 2.06 daño/Qi
```

más Turbulencia si se usa la ruta de interferencia en lugar de Tempestad.

Estado: buen rendimiento grupal; mismo problema global de AOE en duelo.

---

# 6. Hallazgos consolidados del Pass 1

## Sin evidencia de nerf inmediato

- Palma directa;
- Palma DOT;
- Círculo en grupo;
- Lluvia en grupo;
- Armadura de Plata;
- Latigazo en daño puro;
- Golpe de Montaña;
- Temblor en grupo;
- Paso de Nube Ligera;
- Tijera en grupo.

## Requieren nueva simulación antes de tocar números

### ALTO · M-01
Destello: +7 Penetración plana puede ser demasiado grande para daño base 9.

### ALTO · A-02
Espejo: reserva base 12% hace que Reflujo/regeneración no lleguen a funcionar contra paquetes comunes de 5+.

### ALTO · T-02
Piel: fortificación completa puede alcanzar una DEF otorgada demasiado alta demasiado rápido.

### ALTO · V-01
Lanza: ruta de precisión/crítico pierde contra ruta de impacto salvo Evasión extraordinariamente alta.

### GLOBAL · G-01
AOE 0.65 antes de DEF produce daño casi nulo en duelo con DEF media.

## Huecos que impiden simulación completa

1. nueva escala canónica de DEF de monstruos;
2. Evasión de monstruos;
3. Tenacidad de monstruos;
4. `base_control` de Arrastre;
5. fórmula de progresión de daño base/Ataque en el contrato nuevo.

Estos huecos deben cerrarse como parte del balance de entidades, no rellenarse usando silenciosamente la vieja `defensa` de ver74.
