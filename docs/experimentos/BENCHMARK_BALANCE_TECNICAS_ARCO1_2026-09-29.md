# Benchmark de balance — 15 técnicas de Arco 1

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **PASS 0 / LÍNEA BASE NORMALIZADA / SIN CAMBIOS NUMÉRICOS APLICADOS**

## 0. Objetivo

Comparar las 15 técnicas sobre una base común antes de modificar daño, coste, AOE, DOT o valores defensivos.

Este documento no cambia identidades, hooks, Concordancias ni runtime.

---

# 1. Supuestos de Pass 0

Para aislar el valor propio de la técnica:

- sin raíz principal;
- sin injerto;
- sin equipo;
- sin Concordancia;
- sin buffs externos;
- sin Robo de Vida;
- impacto conectado;
- DEF = 0 salvo en la prueba de sensibilidad;
- crítico universal base = 5%;
- daño crítico base = x1.50;
- DOT no critica;
- ramas comparadas por ruta completa coherente;
- AOE en grupo usa magnitud completa;
- AOE en duelo usa 0.65 antes de DEF según contrato actual.

El objetivo de este Pass 0 no es declarar ganador, sino detectar outliers.

---

# 2. Unitarget — base sin ramas

| Técnica | Base | Qi | Daño base/Qi | Utilidad incorporada |
|---|---:|---:|---:|---|
| Palma Ardiente | 10 | 6 | 1.67 | ninguna de base |
| Destello de Plata | 9 | 6 | 1.50 | +10 pp Penetración % |
| Latigazo de Marea | 8 | 7 | 1.14 | Arrastre / Control |
| Golpe de Montaña | 9 | 6 | 1.50 | Peso / −Evasión |
| Lanza que Parte Nubes | 8 | 6 | 1.33 | +5 Precisión / +5 pp crítico |

Lectura:

- Palma puede liderar daño base porque no trae utilidad adicional.
- Destello sacrifica daño relativo por Penetración.
- Latigazo sacrifica daño por un Control fuerte.
- Lanza sacrifica daño por fiabilidad/crítico.
- Golpe combina daño 9/6 con Peso; debe vigilarse porque comparte eficiencia base con Destello pero posee una utilidad distinta que no depende de DEF.

---

# 3. Unitarget — ruta ofensiva completa

Estimación de daño esperado antes de DEF, incorporando sólo el crítico propio de la ruta.

| Técnica | Daño bruto de ruta | Coste de ruta | Daño esperado | Esperado/Qi |
|---|---:|---:|---:|---:|
| Palma directa | 16.00 | 7 | 16.96 | 2.42 |
| Destello penetración | 9.00 | 6 | 9.23 | 1.54 |
| Latigazo daño | 13.20 | 7 | 13.86 | 1.98 |
| Golpe daño | 14.85 | 6 | 15.22 | **2.54** |
| Lanza impacto | 12.80 | 7 | 13.44 | 1.92 |

Notas:

- Destello no posee ruta de daño puro; su ruta de Penetración debe medirse contra DEF.
- Golpe todavía no incluye en esta tabla el +15% condicional contra Peso máximo.
- Por tanto su pico real puede superar el 2.54/Qi mostrado.

## Hallazgo U-01 — Golpe de Montaña

Golpe presenta la mayor eficiencia ofensiva directa del grupo aun antes de sumar:

- Peso;
- reducción de Evasión;
- bonificación contra Peso máximo;
- utilidades defensivas de otras rutas.

Se marca como **CANDIDATO A AJUSTE**.

Opciones futuras de corrección:

1. añadir +1 Qi a Impacto Profundo;
2. reducir la suma de la ruta directa;
3. reducir el bono condicional de Peso máximo;
4. combinación moderada de 1 + 3.

No se aplica todavía ninguna.

---

# 4. Fuego DOT — prueba de daño total

## Palma Ardiente — ruta DOT completa

Directo base esperado:

```text
10 × crítico base esperado
≈ 10.25
```

Quemadura completa por aplicación:

```text
20% × daño nominal 10 × 4 ticks
= 8 daño diferido
```

Total teórico si todos los ticks ocurren:

```text
≈ 18.25 por lanzamiento
coste = 6 Qi
≈ 3.04 daño total/Qi
```

Esto supera claramente la ruta directa en daño total/Qi, pero:

- es diferido;
- pasa por Absorción;
- puede perder valor si el enemigo muere antes;
- requiere tiempo para completar ticks;
- la comparación real necesita simulación de 3/4/5/6 turnos;
- múltiples aplicaciones pueden coexistir hasta el máximo declarado.

## Hallazgo F-01

La ruta DOT de Palma es **CANDIDATO A TEST DE SOBRERENDIMIENTO**, no a nerf automático.

Debe simularse acumulación de stacks y duración de combate antes de modificar 20% × 4.

## Círculo — ruta DOT completa

Por objetivo:

```text
directo esperado ≈ 7.175
DOT = 20% × 7 × 3 = 4.2
total ≈ 11.375
coste = 9
≈ 1.26 por Qi por objetivo
```

No presenta por sí sola el mismo outlier que Palma porque depende del número de blancos y del coste AOE.

---

# 5. AOE — ruta ofensiva completa

Daño esperado por objetivo antes de DEF:

| Técnica | Esperado/objetivo | Coste | 1 objetivo con 0.65 / Qi | 2 objetivos / Qi | 3 objetivos / Qi |
|---|---:|---:|---:|---:|---:|
| Círculo | 11.13 | 12 | 0.60 | 1.86 | 2.78 |
| Lluvia | 9.54 | 11 | 0.56 | 1.73 | 2.60 |
| Marea | 9.45 | 10 | 0.61 | 1.89 | 2.84 |
| Temblor | 9.54 | 11 | 0.56 | 1.73 | 2.60 |
| Tijera | 9.81 | 10 | 0.64 | 1.96 | 2.94 |

Lectura:

- con 2 objetivos las AOE ya se acercan a una eficiencia unitarget razonable;
- con 3+ objetivos pasan naturalmente a ser la herramienta correcta de grupo;
- las diferencias internas se justifican parcialmente por Penetración/debuffs/interferencia;
- Tijera es la más eficiente de las AOE directas actuales, pero la diferencia no es todavía extrema;
- Círculo paga el coste más alto debido a base 7 y ruta de daño más agresiva.

---

# 6. Sensibilidad del 0.65 frente a DEF

Se evaluó la ruta directa completa contra DEF 0/3/6/9.

## Duelo con AOE_SINGLE_TARGET_SCALAR = 0.65

Daño esperado aproximado:

| Técnica AOE | DEF 0 | DEF 3 | DEF 6 | DEF 9 |
|---|---:|---:|---:|---:|
| Círculo | 7.23 | 4.23 | 1.23 | 0.19 |
| Lluvia | 6.20 | 3.50 | 0.80 | 0.13 |
| Marea | 6.14 | 3.14 | 0.28 | 0.00 |
| Temblor | 6.20 | 3.20 | 0.34 | 0.04 |
| Tijera | 6.38 | 3.38 | 0.50 | 0.05 |

Lluvia conserva su Penetración base de Metal en esta aproximación.

## Hallazgo A-01

El 0.65 **antes de DEF** funciona como penalización moderada con DEF baja, pero con DEF media/alta se combina con la reducción plana y puede llevar varias AOE casi a cero.

Esto puede ser intencional si AOE debe ser muy mala en duelo, pero no debe cerrarse sin conocer la DEF real de:

- enemigos comunes de Arco 1;
- élites;
- mini-jefes;
- Grulla.

No cambiar todavía 0.65.

---

# 7. Primer rango objetivo de balance

No es una regla rígida; sirve para detectar outliers.

## Unitarget ofensiva completa

Objetivo preliminar sin utilidad extrema:

```text
~1.9 a 2.4 daño esperado/Qi antes de DEF
```

Una técnica con Control, Penetración o debuff fuerte puede estar por debajo.

## AOE ofensiva completa

Con 2 objetivos:

```text
~1.7 a 2.0 daño esperado total/Qi
```

Con 3 objetivos:

```text
~2.5 a 3.0
```

Esto coincide razonablemente con las cinco AOE actuales.

---

# 8. Candidatos para Pass 1

## Prioridad ALTA

### B-01 · Golpe de Montaña

Probar primero:

```text
Impacto Profundo:
+1 Qi
```

Esto lleva la ruta directa completa de coste 6 a coste 7 sin alterar su identidad ni daño visible.

Después reevaluar el +15% contra Peso máximo.

### B-02 · Palma DOT

Simular combates de 3–6 turnos con:

- aplicación cada turno;
- máximo 4 stacks;
- ticks al inicio de turno;
- DEF ignorada;
- Absorción activa/inactiva;
- muerte antes de completar ticks.

No modificar todavía el 20% × 4.

### B-03 · AOE 0.65

No modificar hasta fijar una escalera representativa de DEF del contenido.

## Prioridad MEDIA

- comprobar si Latigazo requiere +1 Qi en su ruta directa por combinar +65% con Arrastre base;
- comprobar si la base de Lanza 8 sigue suficiente cuando se incorpora precisión real y crítico;
- comprobar Destello en DEF alta antes de considerar cualquier buff de daño;
- comparar Tijera con Marea cuando Turbulencia/Desbalance entren en una simulación probabilística.

---

# 9. Siguiente benchmark

Pass 1 debe introducir perfiles de objetivo:

```text
COMMON
ELITE
BOSS
```

con al menos:

```text
HP
DEF
EVASION
TENACITY
ABSORPTION si corresponde
duración esperada de combate
```

Sin esos perfiles no conviene modificar simultáneamente daño y DEF.

