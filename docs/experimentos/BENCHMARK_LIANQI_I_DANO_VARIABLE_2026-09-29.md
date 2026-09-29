> ⚠️ **HISTÓRICO / NO USAR CIFRAS PARA BALANCE DEL SISTEMA NUEVO.**  
> Este informe fue producido antes de declarar obsoleto el sistema numérico legacy. Puede conservar hallazgos de arquitectura, interacción o metodología, pero cualquier resultado que dependa de HP/Qi/perfiles enemigos/DEF/Evasión/daño derivados o inspirados en `ver74` debe repetirse con el marco `experimentos/balance_nuevo/`. No convertir estadísticas legacy al contrato nuevo.

# Benchmark LianQi I — daño variable y escala base

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LABORATORIO / NO CANÓNICO**

## 0. Objetivo

Fijar LianQi I como metro patrón antes de calcular el crecimiento de LianQi II–IV y ZhuJi.

Este benchmark corrige una simplificación anterior: el daño de las técnicas ofensivas no se modela como un número fijo. Se recupera la distribución variable mediante dados.

Se excluyen:

- equipo;
- injerto;
- Concordancias;
- consumibles;
- ramas de Tramo I–III;
- bonificaciones externas.

Sí se incluyen:

- raíz principal natural;
- crítico universal;
- Precisión/Evasión;
- DEF plana nueva de laboratorio;
- propiedades base propias de la técnica.

---

# 1. Referencia real de LianQi I

Runtime histórico `ver74`:

```text
HP inicial = 16
Qi máximo = 25
Etapa = LianQi I
```

Ascenso histórico posterior:

```text
+4 HP máximo por etapa
+1 Ataque por etapa
Qi máximo: 25 → 45 → 75 → 110
```

El antiguo `Ataque` participaba principalmente en la probabilidad de impacto; no era un +1 plano de daño de técnica.

Por tanto, el crecimiento futuro de daño no debe copiar `+1 Ataque = +1 daño`.

---

# 2. Recuperación de la variabilidad histórica

Valores históricos confirmados:

```text
Palma Ardiente       2d6+2
Filo de Qi Metálico  1d10+3
Látigo de Agua       2d6
```

Las ramas antiguas podían añadir dados como `+1d4`, `+1d6` o `+2d6`.

Para el rediseño se propone usar LianQi I como ancla de las cinco raíces:

| Elemento | Técnica de referencia | Dados LianQi I candidatos | Rango | Media al impactar antes de raíz/DEF |
|---|---|---|---:|---:|
| Fuego | Palma Ardiente | `2d6+2` | 4–14 | 9.0 |
| Metal | Destello de Plata | `1d10+3` | 4–13 | 8.5 |
| Agua | Latigazo de Marea | `2d6` | 2–12 | 7.0 |
| Tierra | Golpe de Montaña | `2d6+1` | 3–13 | 8.0 |
| Viento | Lanza que Parte Nubes | `2d4+3` | 5–11 | 8.0 |

Fuego/Metal/Agua conservan directamente la forma histórica de sus equivalentes. Tierra y Viento son propuestas nuevas de laboratorio.

La distribución de Lanza es deliberadamente más estrecha: menos extremos y más regularidad, coherente con su identidad de precisión.

---

# 3. Conversión de precisión histórica

No se puede conservar los dados históricos y a la vez asumir 100% de impacto.

En `ver74`, con un personaje temprano de referencia:

```text
rata      ≈65% impacto para Fuego
serpiente ≈60%
lobo      ≈60%
```

Metal tenía aproximadamente +5 puntos porcentuales sobre esos valores por su Ataque inicial más alto.

Con el contrato nuevo:

```text
P(impacto) = Precision - Evasion
```

se usa esta escalera de laboratorio:

| Enemigo | HP real | Daño real | Evasión nueva lab | Precisión enemiga lab | DEF plana lab |
|---|---:|---|---:|---:|---:|
| Rata de qi | 9 | 1d4 | 35 | 60 | 0 |
| Serpiente de qi | 13 | 1d4+1 | 40 | 65 | 1 |
| Lobo espiritual | 18 | 1d6+1 | 40 | 70 | 2 |

Esto produce:

```text
Precision 100 → 65% / 60% / 60%
Metal +5 Precision → 70% / 65% / 65%
Lanza +5 Precision → 70% / 65% / 65%
```

La DEF 0/1/2 es únicamente laboratorio. No se deriva de la vieja `defensa`, que tenía otra función.

---

# 4. Raíces incluidas

```text
Fuego  → +10% daño directo · +5 pp crítico
Metal  → +10 pp Penetración % · +5 Precisión
Agua   → −10% coste Qi · +5 Control
Tierra → +10% HP · +5 Tenacidad
Viento → +10 Evasión · +5% daño crítico
```

En Destello se suma su +10 pp Penetración propia: 20 pp en este benchmark.

Latigazo NO recibe todavía valor de Arrastre porque falta `base_control` canónico. Por eso sus resultados ofensivos son un suelo, no su rendimiento completo.

Golpe sí aplica Peso base y mejora la probabilidad de impactos posteriores.

---

# 5. Resultado de técnicas unitarget

Cada personaje empieza con 25 Qi. Con coste efectivo cercano a 6 Qi, una técnica unitarget puede ejecutarse como máximo unas cuatro veces antes de agotar el vaso.

## Rata de qi

| Técnica | victoria antes de agotar Qi/morir | TTK medio si vence |
|---|---:|---:|
| Palma | ~94.1% | ~1.91 acciones |
| Destello | ~95.6% | ~1.97 |
| Latigazo* | ~89.1% | ~2.32 |
| Golpe | ~92.6% | ~2.12 |
| Lanza | ~94.7% | ~2.07 |

## Serpiente de qi

| Técnica | victoria | TTK |
|---|---:|---:|
| Palma | ~81.2% | ~2.61 |
| Destello | ~78.7% | ~2.82 |
| Latigazo* | ~60.6% | ~3.02 |
| Golpe | ~73.9% | ~2.90 |
| Lanza | ~81.1% | ~2.78 |

## Lobo espiritual

| Técnica | victoria | TTK |
|---|---:|---:|
| Palma | ~57.7% | ~3.06 |
| Destello | ~48.8% | ~3.26 |
| Latigazo* | ~20.3% | ~3.54 |
| Golpe | ~38.2% | ~3.44 |
| Lanza | ~44.2% | ~3.46 |

`*` Latigazo está deliberadamente subestimado porque Arrastre no participa.

### Lectura

- rata = enemigo básico que una técnica puede resolver normalmente en 1–3 ejecuciones;
- serpiente = combate real, ya consume parte importante del vaso;
- lobo = amenaza seria de Etapa I;
- Fuego tiene la presión ofensiva más alta, como corresponde a su raíz;
- Metal compensa parte del daño con precisión/penetración;
- Agua no debe buffearse antes de incluir Control;
- Tierra gana supervivencia y mejora precisión futura mediante Peso;
- Viento combina mejor impacto con Evasión defensiva.

Este perfil es más sano que el test anterior con 100% de impacto, donde el lobo dejaba de ser una amenaza.

---

# 6. Daño efectivo medio por ejecución

Incluye fallos de impacto, crítico, raíz y DEF del perfil.

| Técnica | Rata | Serpiente | Lobo |
|---|---:|---:|---:|
| Palma | ~6.75 | ~5.59 | ~5.06 |
| Destello | ~6.11 | ~5.15 | ~4.62 |
| Latigazo | ~4.66 | ~3.69 | ~3.11 |
| Golpe | ~5.36 | ~4.33 | ~3.73 |
| Lanza | ~5.91 | ~4.84 | ~4.17 |

Esto es daño por **acción declarada**, no daño fijo del golpe.

Un impacto concreto puede estar muy por encima o debajo de la media.

---

# 7. Defensivas base en LianQi I

Stress: lobo espiritual. Se compara atacar desde el primer turno contra gastar primero una acción defensiva y luego usar la ofensiva elemental.

| Elemento | sin defensa: victoria | sin defensa: HP final | con defensa: victoria | con defensa: HP final |
|---|---:|---:|---:|---:|
| Fuego · Horno 15% | ~56.8% | ~9.76 | ~37.9% | ~10.25 |
| Metal · Armadura base | ~48.6% | ~9.21 | ~28.7% | **~12.80** |
| Agua · Espejo 30% | ~19.6% | ~8.57 | ~8.0% | **~11.96** |
| Tierra · Piel base | ~38.3% | ~10.39 | ~18.2% | **~15.53** |
| Viento · Paso +15 | ~43.3% | ~9.64 | ~20.6% | ~9.96 |

Todas pierden tempo porque gastan una acción y Qi antes de atacar. El dato importante es cuánto margen de Vida compran.

### D-01 · Horno

15% sólo mejora marginalmente el HP final. Sensibilidad:

```text
15% → ~10.1 HP final
25% → ~11.2
30% → ~11.8
```

Para que el turno defensivo se sienta de verdad en LianQi I, 25–30% merece una prueba posterior.

### D-02 · Paso

Paso +15 Evasión también compra poco margen en la forma base.

Con la raíz Viento ya existe +10 Evasión; el beneficio real de activar Paso es sólo +15 pp durante dos turnos.

Una magnitud o duración mayor deberá probarse antes de congelar la técnica base.

### D-03 · Espejo

El nuevo 30% funciona mucho mejor que el antiguo 12%. Con 16 HP:

```text
30% HP = 4.8 de reserva
```

Eso ya puede absorber aproximadamente un golpe temprano relevante y habilitar Reflujo.

---

# 8. AOE y artes avanzadas

El runtime histórico bloqueaba Círculo, Lluvia, Marea y otras artes de rango Tierra detrás de ZhuJi.

El rediseño actual aún debe cerrar definitivamente la progresión/desbloqueo de las 15 técnicas.

Por tanto, **no se usará el rendimiento AOE a LianQi I para ajustar su daño canónico**. LianQi I sirve para fijar la unidad de escala; cuando una técnica se desbloquee posteriormente deberá usar la escala correspondiente a esa etapa/reino.

Golpe y Lanza se usan aquí como equivalentes de referencia para Tierra/Viento porque el nuevo sistema contempla cinco raíces; esto no fija todavía su momento exacto de aprendizaje.

---

# 9. Conclusión de Etapa I

Primer ancla candidata:

```text
HP base       = 16
Qi base       = 25
Precisión ref = 100

unitarget al impactar:
media bruta ≈ 7–9
rango típico ≈ 2–14 según técnica

enemigo básico:
~60–70% probabilidad de ser impactado
DEF plana 0–2 en la escalera de laboratorio
```

Objetivo de experiencia:

```text
rata       → 1–3 técnicas
serpiente  → 2–4 técnicas
lobo       → amenaza seria / puede agotar el vaso
```

No se calculan aún las ganancias de LianQi II–IV. El siguiente paso será derivarlas desde esta base en vez de sumar números arbitrarios.

## Variables que todavía deben cerrarse antes de Etapa II

1. `base_control` de Arrastre;
2. daño/valor definitivo de Horno base;
3. magnitud/duración definitiva de Paso base;
4. política final de redondeo de Qi (Agua 7 × 0.90 = 6.3);
5. confirmar qué técnicas se aprenden en cada etapa.
