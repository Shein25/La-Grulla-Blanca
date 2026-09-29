# Simulación elemental Pass 2 — secuencial y sin equipo

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **SIMULACIÓN DE BALANCE / NO MODIFICA VALORES CANÓNICOS**

## 0. Propósito

Este Pass estudia el comportamiento real por turnos de las 15 técnicas básicas de Arco 1.

Se excluyen completamente:

- equipo;
- bonos de objetos;
- injerto espiritual;
- Concordancias;
- consumibles;
- buffs externos;
- sets;
- ventajas elementales automáticas.

Sí se incluyen:

- la técnica y sus ramas;
- la raíz principal natural de cada elemento;
- las reglas universales ya cerradas;
- crítico, DEF, Absorción, DOT, debuffs y duración cuando corresponden.

No se ha modificado ningún valor de las técnicas a partir de estos resultados.

---

# 1. Protocolo

## 1.1 Personaje de referencia

Referencia de LianQi IV sin equipo:

```text
HP = 28
Qi máximo = 110
```

Tierra recibe su raíz natural:

```text
HP ≈ 31
```

Rasgos incluidos por elemento:

```text
Fuego  → +10% daño directo · +5 pp crítico
Metal  → +10 pp Penetración % · +5 Precisión
Agua   → −10% coste Qi · +5 Control
Tierra → +10% HP · +5 Tenacidad
Viento → +10 Evasión · +5% Daño Crítico
```

## 1.2 Perfiles de prueba

La vieja `defensa: 9–16` de `ver74` pertenece a la tirada histórica de impacto y **no se reutiliza como DEF plana**.

Los HP del runtime sí sirven de referencia.

Perfiles sintéticos:

| Perfil | HP | DEF nueva de prueba | paquete directo recibido |
|---|---:|---:|---:|
| COMMON | 18 | 3 | 5 |
| ELITE | 34 | 6 | 8 |
| BOSS-STRESS | 52 | 9 | 12 |

El paquete recibido es deliberadamente una magnitud post-mitigación previa del personaje: sirve para comparar defensas sin inventar una DEF base nueva del jugador.

## 1.3 Precisión, Evasión y Control

- Precisión normal de referencia: 100.
- Evasión objetivo: 0 salvo prueba de sensibilidad.
- Precisión enemiga normalizada: 100 cuando se evalúan Evasión/debuff de Precisión.
- No se inventa Tenacidad de monstruos.
- No se inventa `base_control` de Arrastre.
- Cuando se prueba Arrastre se informa como **sensibilidad**, no como valor canónico.

## 1.4 Método

- horizonte principal: 6 turnos;
- Monte Carlo: 50.000–100.000 iteraciones según prueba;
- un enemigo realiza una acción ofensiva por turno mientras siga vivo;
- en el stress AOE de 3 enemigos, cada superviviente realiza una acción;
- DOT de Fuego comienza a tickear en el turno del afectado;
- no existe regeneración pasiva de Qi;
- no se usan ataques básicos para rellenar turnos.

---

# 2. FUEGO

## 2.1 Palma Ardiente

Resultados con raíz Fuego.

### COMMON

| Ruta | Kill ≤6 | TTK medio | HP final medio | Qi gastado medio |
|---|---:|---:|---:|---:|
| Directa | 100% | 1.85 | 23.75 | 12.95 |
| DOT | 100% | 2.00 | 23.00 | 12.00 |
| Eficiencia | 100% | 2.81 | 18.95 | 11.24 |

### ELITE

| Ruta | Kill ≤6 | TTK medio | HP final medio | Qi medio |
|---|---:|---:|---:|---:|
| Directa | 100% | 3.59 | 7.27 | 25.14 |
| DOT | 100% | 3.97 | 4.22 | 23.83 |
| Eficiencia | ~0.4% | 4.00 si mata | ~0 | 16.00 |

Lectura:

- Directa = mejor tempo.
- DOT = casi el mismo número de acciones, menor coste, daño más tardío y mejor relación con DEF.
- Eficiencia = excelente conservación de Qi, pero pierde demasiado tempo bajo presión fuerte.

### BOSS-STRESS

Ninguna ruta de Palma desnuda de equipo/defensas es autosuficiente contra el paquete 12.

No es un defecto de Palma: el personaje recibe suficiente presión para morir antes de completar el daño.

## 2.2 Palma DOT — revisión de la sospecha anterior

En seis turnos la ruta DOT completa **no supera automáticamente** a la directa.

La directa mata antes; DOT se vuelve más eficiente si el combate dura lo suficiente para cobrar ticks pendientes.

Conclusión:

> No hay evidencia para nerfear `20% × 4` en este momento.

Estado: **MANTENER / REVISAR SÓLO CON DURACIONES REALES DE JEFES**.

---

## 2.3 Cuerpo-Horno + Palma Directa

Se activa Cuerpo-Horno en turno 1 y después se usa Palma directa.

### ELITE

| Ruta de Horno | Kill ≤6 | TTK | HP final | Qi medio |
|---|---:|---:|---:|---:|
| Barrera | 100% | 4.59 | 9.29 | 32.12 |
| Conversión | 100% | **3.72** | **10.23** | 26.05 |
| Eficiencia | 100% | 4.59 | 5.26 | 30.15 |

Comparación sin Horno:

```text
Palma directa sola
TTK ≈ 3.59
HP final ≈ 7.27
```

### Hallazgo F-02

**Conversión funciona muy bien.**

Pierde muy poco tempo respecto de atacar inmediatamente:

```text
3.59 → 3.72 turnos
```

pero mejora la supervivencia:

```text
7.27 → 10.23 HP
```

La interacción Absorción → Calor → siguiente técnica Fuego sí cumple su objetivo.

### Hallazgo F-03

La ruta de eficiencia de Cuerpo-Horno es débil bajo paquetes de 8:

- la reserva pequeña se rompe antes de aprovechar los 4 turnos;
- gastar un turno defensivo provoca un ataque adicional;
- termina con menos Vida que Palma directa sin Horno.

No tocar todavía: primero se comparará con builds mixtas.

---

## 2.4 Círculo — tres COMMON simultáneos

Stress test: 3 enemigos de 18 HP, DEF 3, paquete 5 cada uno.

Sin defensa previa:

| Ruta | Limpia grupo | Turnos al limpiar | HP final medio si se considera toda la población |
|---|---:|---:|---:|
| Directa | ~62.3% | 2.97 | 2.92 |
| DOT | ~46.8% | 2.99 | 1.91 |
| Eficiencia | ~0.2% | ~3.1 | ~0 |

Con paquete enemigo 4 en lugar de 5:

- Directa: 100% de clears;
- DOT: 100%;
- Eficiencia: ~3%.

Con paquete 3:

- las tres limpian;
- Eficiencia tarda aproximadamente 4 turnos.

### Lectura

La ruta de Eficiencia sufre un **survival cliff**:

```text
ahorra mucho Qi
pero necesita una acción adicional
→ el grupo obtiene otra ronda completa de ataques
```

Esto puede ser aceptable como identidad de economía, pero debe compararse con builds mixtas antes de modificarla.

---

## 2.5 AOE 0.65 y DOT

El contrato dice que `AOE_SINGLE_TARGET_SCALAR` reduce magnitud ofensiva derivada del daño, pero no enumera explícitamente `DOT_POTENCY`.

Para este Pass principal se interpretó:

```text
DOT_POTENCY creado por una AOE
→ snapshot afectado por 0.65 en duelo
```

Sensibilidad de Círculo DOT vs COMMON:

```text
DOT escalado por 0.65:
TTK ≈ 4.63

DOT sin 0.65:
TTK ≈ 3.97
```

Debe cerrarse expresamente antes del benchmark final.

---

# 3. METAL

## 3.1 Destello de Plata

Con raíz Metal.

### COMMON

| Ruta | TTK | HP final | Qi |
|---|---:|---:|---:|
| Penetración | **2.00** | 23.00 | 12.00 |
| Crítico/Precisión | 2.72 | 19.39 | 16.34 |
| Eficiencia | 2.90 | 18.49 | 11.61 |

### ELITE

| Ruta | Kill ≤6 | TTK | HP final |
|---|---:|---:|---:|
| Penetración | **100%** | 3.99 | 4.06 |
| Crítico/Precisión | ~1.2% | 4.0 si mata | ~0 |
| Eficiencia | 0% | — | 0 |

Ruta completa de Penetración:

```text
35% Penetración porcentual total en benchmark
+7 Penetración plana
```

### Hallazgo M-01 — CONFIRMADO

`+7 Penetración plana` es demasiado grande respecto de:

```text
daño nominal de Destello = 9
DEF de prueba = 3–9
```

La ruta de Penetración deja de ser una especialización contra objetivos blindados y se convierte en la mejor ruta casi universal.

Estado: **PRIMER CANDIDATO REAL A AJUSTE**.

No se cambia aún.

---

## 3.2 Armadura de Plata

Contra impactos directos consecutivos:

```text
Resistencia:
3 Placas × +8 DEF

Cantidad:
8 Placas × +3 DEF
```

Resultado conceptual confirmado:

- Resistencia domina pocos golpes grandes.
- Cantidad domina muchos impactos.
- Adaptación depende de Control/impactos anulados y necesita otra simulación.

### Armadura Resistencia → Destello Penetración vs ELITE

```text
Kill = 100%
TTK ≈ 4.99
HP final ≈ 20.06
```

Sin Armadura:

```text
TTK ≈ 3.99
HP final ≈ 4.06
```

El turno defensivo sí produce una decisión real:

```text
+1 turno
a cambio de
~+16 HP de margen
```

Estado: **SANO**.

---

## 3.3 Lluvia de Filos — tres COMMON

| Ruta | Clear |
|---|---:|
| Ruptura | ~0% en este stress |
| Directa | ~46.7% |
| Eficiencia | ~0% |

La ruta Ruptura tarda en pagar porque:

1. el primer impacto aplica el shred sólo hacia el futuro;
2. tres enemigos atacan antes de que los impactos posteriores exploten la reducción.

No implica que Ruptura sea mala: puede ser una ruta de apoyo para grupo o para un combate largo.

Estado: **PROBAR BUILDS MIXTAS Y COMBATE CON ALIADOS**.

---

# 4. AGUA

## 4.1 Latigazo de Marea sin atribuir Control inventado

Si se ignora temporalmente Arrastre para medir sólo la parte ofensiva:

### COMMON

| Ruta | TTK | HP | Qi |
|---|---:|---:|---:|
| Control | 3.85 | 13.73 | 23.12 |
| Daño | **2.00** | 23.00 | 12.00 |
| Eficiencia | 3.86 | 13.72 | 15.42 |

### ELITE

Ruta Daño:

```text
Kill ≤6 ≈ 34.6%
```

Control/Eficiencia no alcanzan a matar en seis turnos si se elimina artificialmente Arrastre.

Esto demuestra que **no se puede balancear Latigazo sólo por daño**.

## 4.2 Sensibilidad de Arrastre

Ruta Control, sin fijar un valor canónico:

| Probabilidad supuesta de Arrastre | supervivencia vs ELITE |
|---:|---:|
| 30% | ~8% |
| 60% | ~47.6% |
| 90% | ~94.7% |

La rama Control no aumenta DPS: transforma acciones enemigas en acciones perdidas.

Pendiente obligatorio:

```text
base_control de Arrastre
Tenacidad COMMON
Tenacidad ELITE
Tenacidad BOSS
```

---

## 4.3 Espejo de Luna

HP de referencia = 28.

Valores aproximados tras redondeo:

```text
Base / Reflujo / Eficiencia:
12% HP → 3 Absorción

Ruta Reserva:
30% HP → 8 Absorción
```

Daño total absorbido durante una activación:

| paquete | Reserva | Reflujo completo | Eficiencia |
|---:|---:|---:|---:|
| 3 | 9 | 5 | 3 |
| 5 | **10** | 5 | 3 |
| 8 | **8** | 5 | 3 |
| 12 | **8** | 5 | 3 |

### Hallazgo A-02 — CONFIRMADO

La reserva inicial de 12% es tan pequeña que:

- Reflujo suele no tener tiempo de operar;
- duración extra suele no importar;
- la ruta de Eficiencia puede romperse en el primer golpe.

La ruta Reserva es funcional; las otras dos dependen de que el paquete entrante sea muy pequeño.

Estado: **CANDIDATO REAL A AJUSTE**, pero no necesariamente mediante daño.

---

## 4.4 Marea — tres COMMON

Modelo normalizado:

```text
Precisión enemiga = 100
Evasión del jugador Agua = 0
```

| Ruta | Clear |
|---|---:|
| Debuff | ~0% |
| Daño | ~18.9% |
| Eficiencia | ~0% |

La ruta de Debuff reduce a −12 Precisión, pero su daño bajo permite demasiadas acciones enemigas antes de limpiar.

No es todavía un veredicto porque Agua debe combinar Marea con Control/defensa.

---

## 4.5 Kit Agua contra ELITE

```text
Espejo Reserva
→ Latigazo Daño
```

Si se fuerza Arrastre = 0:

```text
Kill/supervivencia ≈ 34.5%
```

Sensibilidad si Latigazo conserva una probabilidad base real de Arrastre:

| P(Arrastre) | Kill/supervivencia |
|---:|---:|
| 30% | ~84.2% |
| 50% | ~95.8% |
| 70% | ~99.5% |

### Conclusión Agua

**No aumentar daño de Agua antes de cerrar Arrastre.**

Una probabilidad moderada de Control cambia completamente su rendimiento real.

---

# 5. TIERRA

## 5.1 Golpe de Montaña

Con raíz Tierra, HP = 31.

### COMMON

| Ruta | TTK | HP final |
|---|---:|---:|
| Presión | 3.00 | 21.01 |
| Daño | **1.95** | 26.25 |
| Estabilidad | 3.00 | 21.01 |

### ELITE

Ruta Daño:

```text
Kill = 100%
TTK ≈ 3.86
HP ≈ 8.15
```

Presión/Estabilidad no matan dentro del horizonte si se elimina de la simulación el valor de Evasión/Tenacidad que precisamente deberían explotar.

### Hallazgo T-01 — REVISADO

La sospecha anterior de nerf inmediato de Golpe queda retirada.

Comparado raíz contra raíz:

- Palma mantiene mayor presión ofensiva.
- Golpe sacrifica parte de ese daño por Peso y estabilidad.

Estado: **MANTENER**.

---

## 5.2 Piel de Cobre — secuencia de seis impactos

Raíz Tierra: HP ≈31.

### Ruta Fortificación

DEF según Arraigo bajo lectura actual:

```text
1 → 5 DEF
2 → 8 DEF
3 → 12 DEF
```

Daño evitado efectivo en seis paquetes:

| paquete | evitado |
|---:|---:|
| 5 | 15 |
| 8 | 21 |
| 12 | 41 |

Importante:

- contra paquete 5, bloquea todo pero no gana Arraigo;
- contra 8 puede quedarse en 2 Arraigos;
- contra 12 salta a máximo y bloquea fuertemente la ráfaga, pero expira después.

### Ruta Estabilidad

DEF sigue la progresión base:

```text
3 → 4 → 5
```

Su valor verdadero está en Tenacidad; sin Control enemigo sólo se mide una fracción de la ruta.

### Ruta Aguante

Con duración completa y curación:

| paquete | prevención efectiva en 6 turnos |
|---:|---:|
| 5 | ~29 |
| 8 | ~30 |
| 12 | ~32 |

### Hallazgo T-02 — REVISADO

La lectura estática hacía parecer Fortificación excesiva.

La simulación temporal muestra:

- Fortificación = mejor contra ráfaga;
- Aguante = mejor contra presión prolongada;
- Estabilidad = no evaluable sin Control real.

**No nerfear Piel automáticamente.**

---

## 5.3 Temblor — tres COMMON

Ruta Daño:

```text
Clear = 100%
TTK = 3 turnos
HP final medio ≈ 1.16
```

El resultado está muy influido por la raíz Tierra:

```text
28 HP → ~31 HP
```

Esos 3 HP adicionales permiten sobrevivir a la segunda ronda completa y lanzar el tercer Temblor.

Debuff y Resonancia no limpian por sí solas bajo este stress; deben evaluarse por la utilidad que producen para la acción Tierra posterior.

---

# 6. VIENTO

## 6.1 Lanza que Parte Nubes — ELITE

Se varió Evasión del objetivo porque es la razón de existir de la ruta de Precisión.

### Evasión 0

| Ruta | Kill ≤6 |
|---|---:|
| Precisión/Crítico | ~0% |
| Impacto | **~56.6%** |
| Eficiencia | 0% |

### Evasión 20

| Ruta | Kill ≤6 |
|---|---:|
| Precisión/Crítico | ~0% |
| Impacto | **~34.3%** |
| Eficiencia | 0% |

### Evasión 40

| Ruta | Kill ≤6 |
|---|---:|
| Precisión/Crítico | ~0% |
| Impacto | **~14.4%** |
| Eficiencia | 0% |

Incluso sobre COMMON con Evasión 80–90, Impacto continúa compitiendo o ganando en la mayoría de simulaciones.

### Hallazgo V-01 — CONFIRMADO

La ruta:

```text
+60% daño directo
```

está demasiado separada de la ruta:

```text
+Precisión
+Crítico
+Daño Crítico
```

La rama de Precisión sólo empieza a acercarse bajo Evasión extrema.

Estado: **CANDIDATO REAL A AJUSTE**.

---

## 6.2 Paso de Nube Ligera

Con raíz Viento:

```text
Evasión completa:
40 Evasión durante 2 turnos

Respuesta:
25 Evasión durante 2 turnos

Eficiencia:
25 Evasión durante 4 turnos
```

Contra Precisión enemiga 100:

- ruta Evasión: 40% de evitar cada impacto mientras dura;
- Respuesta: 25%;
- Eficiencia: 25% durante el doble de tiempo.

Probabilidad de que Respuesta consiga al menos una Evasión en dos ataques:

```text
≈ 43.75%
```

y entonces prepara:

```text
+15 Precisión
+5 pp crítico
```

para la siguiente técnica de Viento.

### Conclusión Paso

La diferenciación es saludable:

- Evasión = protección intensa;
- Respuesta = defensa + preparación ofensiva;
- Eficiencia = cobertura prolongada.

Estado: **MANTENER**.

---

## 6.3 Tijera — tres COMMON

La raíz Viento (+10 Evasión) y Turbulencia modifican la presión enemiga.

| Ruta | Clear |
|---|---:|
| Interferencia | ~0.1% |
| Tempestad | **~83.4%** |
| Corriente | ~0% |

Tempestad:

```text
TTK ≈ 2.97
HP final medio ≈ 5.82
```

La ruta Interferencia reduce mucho más la Precisión rival pero no mata antes de acumular demasiadas acciones enemigas.

Debe probarse en builds mixtas.

---

# 7. Stress transversal — defensa primero, ofensiva después

Este bloque **no es un ranking de elementos**. Sólo pregunta:

> ¿qué ocurre si el jugador gasta el turno 1 en su defensa especializada y luego usa su ofensiva principal?

Contra ELITE:

| Elemento | apertura | Kill/supervivencia | TTK | HP final |
|---|---|---:|---:|---:|
| Fuego | Horno Conversión → Palma Directa | 100% | 3.72 | 10.23 |
| Metal | Armadura Resistencia → Destello Pen | 100% | 4.99 | 20.06 |
| Agua | Espejo Reserva → Latigazo Daño, forzando Arrastre=0 | 34.5% | 4.92 si mata | 1.60 |
| Tierra | Piel Fortificación → Golpe Daño | 100% | 4.86 | 21.14 |
| Viento | Paso Evasión → Lanza Impacto | ~44.8% | 5.38 si mata | 3.06 |

Agua cambia drásticamente cuando se habilita Arrastre:

```text
P=30% → ~84%
P=50% → ~96%
P=70% → ~99.5%
```

Por eso no debe compararse su daño bruto con Fuego/Tierra como si fuese un atacante puro.

---

# 8. Stress AOE — tres COMMON

Sin apertura defensiva, usando la ruta de daño/burst:

| Elemento | técnica | clear aproximado |
|---|---|---:|
| Fuego | Círculo Directo | 62% |
| Metal | Lluvia Directa | 47% |
| Agua | Marea Daño | 19% |
| Tierra | Temblor Daño | 100% |
| Viento | Tijera Tempestad | 83% |

Factores que explican diferencias:

- Fuego mata antes;
- Metal paga por Penetración, que vale menos contra DEF 3;
- Agua invierte parte del presupuesto en debuff/Control y ahorro de Qi;
- Tierra posee ~3 HP adicionales y sobrevive justo a la ronda necesaria;
- Viento recibe menos golpes por raíz + Turbulencia.

Este stress **no debe usarse solo para igualar daño base**.

---

# 9. Hallazgos que sobreviven al Pass 2

## AJUSTE NUMÉRICO PROBABLE

### M-01 · Destello de Plata
`+7 Penetración plana` es demasiado dominante en la escala actual.

### A-02 · Espejo de Luna
La reserva base de 12% deja sin espacio real a Reflujo y a la ruta de duración.

### V-01 · Lanza que Parte Nubes
+60% directo crea demasiada distancia respecto de Precisión/Crítico.

## NO TOCAR TODAVÍA

- Palma DOT;
- Golpe de Montaña;
- Piel de Cobre;
- Armadura de Plata;
- Paso de Nube Ligera.

## NECESITAN BUILDS MIXTAS 3×3×3

- Círculo;
- Lluvia;
- Marea;
- Temblor;
- Tijera;
- rutas de eficiencia de unitarget.

Las rutas puras son extremos. El jugador puede mezclar las tres elecciones entre Tramos I–III, por lo que el siguiente Pass debe enumerar las **27 combinaciones por técnica** antes de nerfear/buffear las AOE.

---

# 10. Huecos de contrato/balance todavía abiertos

1. `base_control` de Arrastre;
2. Tenacidad por perfil de enemigo;
3. Evasión por perfil de enemigo;
4. nueva escala de DEF plana de criaturas;
5. relación exacta entre progresión de Ataque y `BASE_DAMAGE`;
6. si `AOE_SINGLE_TARGET_SCALAR` modifica explícitamente el snapshot de `DOT_POTENCY`;
7. piso global de Qi.

No se rellenarán con valores heredados de `ver74` si cumplen una función mecánica distinta.

---

# 11. Próximo Pass

Enumerar las 27 combinaciones de ramas por técnica ofensiva/defensiva y buscar:

- mejor build por COMMON;
- mejor build por ELITE;
- mejor build por grupo;
- builds dominadas que nunca son racionales;
- puntos de quiebre de supervivencia;
- coste Qi por victoria;
- dependencia de DEF/Evasión/Control.

Sólo después se modificarán números canónicos.
