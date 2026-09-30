# ETAPA 15B — Piel de Cobre completa

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CERRADA / 27 RUTAS SCREEN PASS / PIEL COMPLETA PROVISIONAL CON WATCH MULTIIMPACTO**

## Alcance

Se completó el benchmark integral de Piel de Cobre:

- base DEF_CAP2;
- Fortificación I–III;
- Estabilidad I–III;
- Aguante I–III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 enemigos;
- 3 enemigos;
- stress LAB de Control;
- curación;
- duración;
- sinergias entre familias.

Runner:

`experimentos/balance_nuevo/etapa15b_piel_cobre_completa.py`

No se modifica runtime/HTML.

---

# 1. Notación

En este documento:

```text
F = Fortificación
S = Estabilidad
A = Aguante
```

Cada ruta tiene tres letras:

```text
T1 / T2 / T3
```

Ejemplos:

```text
FFF
Corteza / Estratos / Cuerpo de Roca

SSS
Centro Firme / Raíz Profunda / Inamovible

AAA
Tierra Persistente / Suelo que Sostiene / Montaña Persistente

AAF
Tierra Persistente / Suelo que Sostiene / Cuerpo de Roca
```

---

# 2. Fortificación

No se reabre.

Permanece PROVISIONAL según Etapas 8–10:

## T1 — Corteza Endurecida

```text
contribución Arraigo DEF:
2 / 3 / 3

con +2 DEF inmediata:
Piel aporta +4 / +5 / +5 DEF
```

## T2 — Estratos Compactos

```text
al aumentar Arraigo a 2 o 3:
gana/refresca 1 Estrato

máximo1

siguiente impacto directo conectado:
+2 DEF sólo para ese impacto
```

## T3 — Cuerpo de Roca

```text
Arraigo3
+
TURN_START
→ arma 1 Guardia

primer impacto directo conectado del turno:
+3 DEF sólo para ese impacto
```

Los tres mecanismos siguen mostrando retornos decrecientes al combinarse.

---

# 3. Estabilidad — validación completa

Los valores existentes no necesitaron recalibración.

## T1 — Centro Firme

```text
cada Arraigo:
+5 Tenacidad
en vez de +3
```

## T2 — Raíz Profunda

```text
con 2+ Arraigos:
+5 Tenacidad adicional
```

Si existe Centro Firme:

```text
primera vez por activación
que un Control falla:
+1 turno de duración restante
```

## T3 — Inamovible

```text
con al menos 1 Arraigo:
+5 Tenacidad
```

Primera vez por activación que el usuario resiste Control a Arraigo máximo:

```text
siguiente Golpe de Montaña:
+10 Precisión
```

No genera acción adicional.

---

# 4. Tenacidad de la ruta SSS

Incluyendo raíz Tierra CANON +5 Tenacidad:

## Piel base sin Estabilidad

```text
Arraigo1: 8 Tenacidad total
Arraigo2: 11
Arraigo3: 14
```

Con Control efectivo65:

```text
P(Control):
57%
54%
51%
```

## SSS

```text
Arraigo1:
raíz5 + Centro5 + Inamovible5
= 15

Arraigo2:
raíz5 + Centro10 + Raíz Profunda5 + Inamovible5
= 25

Arraigo3:
raíz5 + Centro15 + Raíz Profunda5 + Inamovible5
= 30
```

Con Control efectivo65:

```text
P(Control):
50%
40%
35%
```

La progresión es fuerte pero acotada.

No existe inmunidad automática.

---

# 5. Stress LAB de Control

Este escenario NO define un enemigo canónico.

Configuración:

```text
enemigo COMMON
+
Control efectivo65
+
intento de SKIP_ACTION tras impacto directo conectado
```

En este runner el intento se resuelve después de ON_HP_DAMAGE/Arraigo para
aislar la respuesta reactiva de Piel.

Promedio de cuatro semillas × 12.000 combates:

| Ruta | Win | P(Control) agregada | Acciones perdidas |
|---|---:|---:|---:|
| FFF | 88.72% | 53.64% | 1.51 |
| SSS | 91.91% | **37.43%** | 1.49 |
| AAA | 91.19% | 52.06% | 2.14 |
| AAF | 92.78% | 52.05% | 2.14 |
| SSA | **93.22%** | 41.81% | 2.01 |

La tasa agregada no coincide exactamente con los valores por estado porque:

- Piel cambia de Arraigo durante el combate;
- no todos los intentos ocurren a Arraigo3;
- la ventana defensiva puede expirar.

En SSS:

- la extensión de Raíz Profunda + Centro se activa en ~92.1% del stress;
- la respuesta de Inamovible para +10 Precisión se prepara en ~78.9%.

Por tanto Estabilidad tiene identidad mecánica real.

**Estabilidad I–III → PROVISIONAL.**

---

# 6. Aguante — problema detectado

El diseño anterior permitía acumular:

- +1 turno desde Tierra Persistente;
- +1 turno adicional por sinergia de Suelo que Sostiene;
- +1 turno desde Montaña Persistente;

mientras el texto también declaraba una ruta completa de aproximadamente 3→5.

Además Piel ya posee:

```text
al alcanzar Arraigo3:
+1 turno restante
una vez/activación
```

En presión multiimpacto, cada turno extra multiplica la cantidad de impactos
beneficiados por DEF plana.

El screen confirmó que permitir dos turnos base adicionales desde Aguante
volvía a abrir el mismo tipo de escalado que DEF_CAP2 intentó corregir.

---

# 7. Recalibración de Aguante — AGUANTE_DUR_CAP1

Se introduce la regla PROVISIONAL:

```text
Aguante puede aportar
como máximo +1 turno
a la duración base de Piel.
```

No limita la extensión propia de Arraigo máximo ni la extensión de Estabilidad
por Control: limita únicamente los bonos base de la familia Aguante.

## T1 — Tierra Persistente — PROVISIONAL

Se conserva:

```text
+1 turno de duración desde la activación
```

Base:

```text
3 → 4
```

## T2 — Suelo que Sostiene — PROVISIONAL recalibrada

Se conserva:

```text
primera vez que alcanza Arraigo3:
cura 5% Vida máxima
```

Se elimina la antigua sinergia de otro +1 turno con Tierra Persistente.

Motivo:

- era la principal fuente del escalado excesivo de duración;
- el nodo sigue siendo útil por sí mismo mediante curación;
- no necesita duplicar la función de T1/T3.

## T3 — Montaña Persistente — PROVISIONAL recalibrada

Concede:

```text
+1 turno base
si Aguante todavía no concedió uno
```

Por tanto:

```text
T3 sola:
3 → 4

T1 + T3:
sigue en 4
no 5
```

Además conserva:

```text
al alcanzar Arraigo3:
cura 5% Vida máxima

una vez/activación,
si Vida <30% con Piel activa:
cura otro 5%
```

Con Suelo + Montaña:

```text
al alcanzar Arraigo3:
hasta 10% Vida máxima total
```

Ruta AAA completa:

```text
duración base4

+
extensión propia de Arraigo3:
puede llegar a5

curación:
5% Suelo
+5% Montaña al máximo
+5% Montaña bajo30%
máximo teórico15% por activación
```

La curación real nunca supera Vida faltante.

---

# 8. Efecto de AGUANTE_DUR_CAP1

Comparación pareada con cuatro semillas × 10.000.

## AA- · Tierra Persistente + Suelo

| Perfil | Duración antigua | CAP1 | Delta win |
|---|---:|---:|---:|
| COMMON | 99.07% | 98.14% | -0.94 pp |
| 2 enemigos | 95.15% | 92.38% | -2.77 pp |
| 3 enemigos | 81.91% | 74.64% | **-7.27 pp** |

## AAA

| Perfil | Antigua | CAP1 | Delta win |
|---|---:|---:|---:|
| COMMON | 99.34% | 98.60% | -0.74 pp |
| 2 enemigos | 96.13% | 93.65% | -2.48 pp |
| 3 enemigos | 84.42% | 77.16% | **-7.25 pp** |

## AAF

| Perfil | Antigua | CAP1 | Delta win |
|---|---:|---:|---:|
| COMMON | 99.53% | 98.88% | -0.65 pp |
| 2 enemigos | 97.80% | 95.43% | -2.37 pp |
| 3 enemigos | 89.61% | 82.00% | **-7.62 pp** |

Lectura:

> CAP1 reduce principalmente el exceso multiimpacto y casi no altera el duelo.

Éste es exactamente el patrón buscado.

**Aguante I–III → PROVISIONAL recalibrado.**

---

# 9. Rutas puras finales

Promedio de cuatro semillas × 15.000.

## FFF — Fortificación completa

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 96.44% | 62.06% |
| PRECISE | 95.00% | 58.94% |
| HEAVY | 94.92% | 59.92% |
| DANGEROUS | 93.13% | 57.02% |
| 2 enemigos | 90.35% | 51.38% |
| 3 enemigos | 73.80% | 32.80% |

## SSS — Estabilidad completa

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 95.71% | 58.51% |
| PRECISE | 93.94% | 55.13% |
| HEAVY | 92.98% | 53.05% |
| DANGEROUS | 90.17% | 49.00% |
| 2 enemigos | 84.77% | 40.83% |
| 3 enemigos | 57.56% | 19.46% |

Sin Control enemigo es correcto que SSS sea la ruta más débil de daño puro.

## AAA — Aguante completo con CAP1

| Perfil | Win | HP restante |
|---|---:|---:|
| COMMON | 98.61% | 74.38% |
| PRECISE | 97.92% | 71.51% |
| HEAVY | 97.40% | 68.97% |
| DANGEROUS | 96.09% | 65.46% |
| 2 enemigos | 93.54% | 56.63% |
| 3 enemigos | 77.36% | 33.81% |

Curación media aproximada:

- ~8.3% HP en COMMON;
- ~9.3% en DANGEROUS;
- ~9.6% en 3 enemigos.

El máximo15% no se alcanza sistemáticamente porque:

- algunas curas producen overheal;
- el trigger de <30% no siempre ocurre;
- el personaje puede morir o acabar el combate antes.

---

# 10. Sinergias mixtas

Las 27 rutas muestran sinergias reales.

## AAF

```text
Tierra Persistente
Suelo que Sostiene
Cuerpo de Roca
```

Promedio:

| Perfil | Win |
|---|---:|
| COMMON | 98.89% |
| PRECISE | 98.45% |
| HEAVY | 98.19% |
| DANGEROUS | 97.33% |
| 2 enemigos | 95.31% |
| 3 enemigos | 82.14% |

Cuerpo de Roca obtiene más oportunidades porque Aguante prolonga Piel, pero
CAP1 evita que esa sinergia siga creciendo con múltiples turnos base extra.

## FAA

```text
Corteza
Suelo
Montaña
```

Es una de las rutas más fuertes de daño puro:

- 2 enemigos: ~96.10%;
- 3 enemigos: ~86.18%.

No suma DEF permanentemente más allá de Corteza: su potencia procede de
fortificación + curación.

Se mantiene como **WATCH de sinergia F+A**, no como motivo de nerf inmediato.

---

# 11. Screen 27/27 final

8.000 combates por celda.

Rangos:

| Perfil | Win mínimo | Win máximo | HP mínimo | HP máximo |
|---|---:|---:|---:|---:|
| COMMON | 95.71% | 99.11% | 58.58% | 77.50% |
| PRECISE | 94.19% | 98.39% | 55.31% | 75.69% |
| HEAVY | 92.43% | 98.01% | 52.84% | 73.71% |
| DANGEROUS | 90.38% | 97.38% | 49.44% | 71.96% |
| 2 enemigos | 84.84% | 96.16% | 40.99% | 65.70% |
| 3 enemigos | 59.06% | 87.01% | 19.77% | 48.24% |

No aparece:

- crecimiento infinito de duración;
- curación repetible sin límite;
- DEF permanente adicional no autorizada;
- generación infinita de Estratos;
- múltiples Guardias de Roca por turno;
- inmunidad automática a Control.

---

# 12. Lectura de identidades

## Fortificación

```text
más mitigación por impacto
+
ventanas defensivas
```

Especialización de daño directo.

## Estabilidad

```text
más Tenacidad
+
reacción al fallo de Control
+
respuesta ofensiva al resistir
```

Especialización anti-Control.

## Aguante

```text
+1 turno base máximo
+
curación limitada por activación
```

Especialización de supervivencia prolongada.

Las tres familias ya no intentan resolver el mismo problema mediante más DEF.

---

# 13. Estado final de Piel de Cobre

```text
BASE                   PROVISIONAL
FORTIFICACIÓN I–III    PROVISIONAL
ESTABILIDAD I–III      PROVISIONAL
AGUANTE I–III          PROVISIONAL recalibrado

27/27 rutas            SCREEN PASS

runtime                SIN CAMBIOS
HTML                   SIN CAMBIOS
```

---

# 14. WATCH obligatorios

## WATCH 1 — Piel multiimpacto

Piel continúa siendo la defensiva base con mayor escalado frente a múltiples
acciones enemigas.

DEF_CAP2 y AGUANTE_DUR_CAP1 reducen dos fuentes distintas de amplificación, pero
no eliminan deliberadamente su identidad de Tierra.

No nerfear otra vez sin encuentros reales.

## WATCH 2 — mezclas Fortificación + Aguante

Rutas como FAA/AAF son muy fuertes bajo presión.

No se declaran rotas porque este benchmark usa enemigos LianQi I para nodos
LianQi IV.

Deben ser prioridad cuando existan perfiles enemigos II–IV.

## WATCH 3 — Estabilidad

Revalidar con enemigos reales que posean:

- Control;
- Tenacidad propia si corresponde;
- frecuencia real de intentos;
- inmunidades/lockout de jefes.

El Control efectivo65 usado aquí es sólo LAB.

---

# 15. Decisión

**Piel de Cobre queda completa en estado PROVISIONAL.**

Con este cierre ya existen benchmarks integrales para las cinco defensivas:

- Cuerpo-Horno;
- Armadura de Plata;
- Espejo de Luna;
- Piel de Cobre;
- Paso de Nube Ligera.

El siguiente bloque correcto es el **screen conjunto final de las cinco
defensivas completas**, ya sin el hueco documental de Tierra.
