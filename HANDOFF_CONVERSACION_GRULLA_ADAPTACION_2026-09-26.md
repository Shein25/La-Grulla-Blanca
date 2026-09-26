# Handoff de conversación — Grulla + adaptación poblacional
**Fecha:** 2026-09-26  
**Backup branch:** `docs/experimentos-backup-2026-09-25`

## 1. Rama activa real

Trabajo experimental activo:

```text
experiment/monster-adaptive-survival-lab-v0.1
```

HEAD verificado al crear este backup:

```text
94e925aa5b7f380898ea57a10125fc9b3e772634
```

Últimos commits relevantes:

```text
94e925a chore: expose Grulla phase I Paso benchmark
0e3d373 docs: close Grulla phase I Paso isolation
78ad239 benchmark: add Grulla phase I Paso isolation grid
dd46170 docs: supersede 45 35 25 Grulla benchmark
220b961 chore: expose Grulla phase I root-grid benchmark
7ce227a docs: record Grulla phase I 150 HP root-grid results
ea013c1 benchmark: add Colab-ready Grulla phase I root grid
7df2d2e docs: checkpoint Grulla phase I at 150 HP
d2cb31f docs: invalidate 105 HP Grulla balance result
2b504a9 fix: restore Grulla 150-100-50 phase baseline
```

Guardas:

- no tocar `main`;
- no hacer merge;
- no mezclar este trabajo con otras ramas;
- conservar `CADENCE_COMPAT` como autoridad hasta decisión explícita;
- no repetir suites/cálculos cerrados salvo invalidación concreta;
- documentar + commit después de cada bloque pesado.

---

# 2. Adaptación poblacional — decisión cerrada

Modelo elegido:

```text
C — FINAL_E1_ADAPTIVE_LEARNING_STATS
variante C_STAGGERED
```

A queda sólo como baseline/control histórico.

B queda sólo como comparación histórica.

## Tiers

### T0
```text
stats canónicos
sin adaptación aprendida
```

### T1
```text
E1 de supervivencia
HP x1.025
daño x1.025
```

### T2
```text
memoria persistente / reconocimiento
HP x1.05
daño x1.05
HIT +1
```

### T3
```text
contraadaptación de especie
HP x1.075
daño x1.075
HIT +1
EVA +5
```

### T4
```text
segunda adaptación compatible
HP x1.10
daño x1.10
HIT +1
EVA +5
CRIT 5% -> 10%
```

Referencia de calibración:

```text
T1 ~10 muertes efectivas
T2 ~25
T3 ~50
T4 ~90
```

Thresholds de presión:

```text
T0 = 0-19
T1 = 20-44
T2 = 45-69
T3 = 70-89
T4 = 90-100
```

---

# 3. Decay — pisos irreversibles

Regla seleccionada:

```text
máximo histórico T0 -> piso T0
máximo histórico T1 -> piso T1
máximo histórico T2 -> piso T1
máximo histórico T3 -> piso T2
máximo histórico T4 -> piso T3
```

En palabras:

- alcanzó T1 -> nunca vuelve a T0;
- alcanzó T2 -> puede bajar a T1;
- alcanzó T3 -> puede bajar a T2;
- alcanzó T4 -> puede bajar a T3.

Campo histórico previsto:

```text
maxTierReached
```

No persistir `floorTier` ni `effectiveTier`; se derivan.

Archivo principal:

`adaptive/adaptive-ecology-milestone-floor-v0.2.mjs`

---

# 4. Ceiling — decisión posterior a auditoría de Claude

Claude auditó el sistema y concluyó:

```text
APTO PARA CONTINUAR
```

No encontró bugs críticos del modelo C.

Se cerró una ambigüedad importante:

```text
adaptiveCapabilityCeiling
= techo de APRENDIZAJE REAL
no sólo de manifestación
```

Caps de presión:

```text
ceiling T0 -> pressure max 19
ceiling T1 -> pressure max 44
ceiling T2 -> pressure max 69
ceiling T3 -> pressure max 89
ceiling T4 -> pressure max 100
```

Ejemplo:

```text
Rata + jugador LianQi I
ceiling T1
-> aunque farmee de forma obsesiva, no precarga T2/T3/T4

jugador sube a LianQi II
-> población sigue T1
-> necesita NUEVA presión para cruzar a T2
```

Archivos:

- `adaptive/adaptive-learning-ceiling-v0.2.mjs`
- `adaptive/DECISION_TECHO_APRENDIZAJE_ADAPTATIVO_v0.2.md`
- `tests/adaptive-learning-ceiling.test.mjs`

También se corrigió `npm test` para incluir suites adaptativas + Grulla.

Documentos A/B antiguos quedaron marcados como históricos/superseded.

---

# 5. Grulla — objetivo de diseño

La Grulla debe sentirse como el jefe final del Arco 1 y medir si el jugador aprendió a jugar.

Tres cerebros:

```text
Fase I  — EL VOTO INMÓVIL       — PROGRAMADA
Fase II — LAS ALAS RECUERDAN    — ADAPTATIVA
Fase III— LA CAMPANA SIN DUEÑO  — MAESTRA
```

Examina:

```text
leer telegraphs
administrar qi
variar herramientas
defender
controlar
romper planes
adaptarse
```

No debe ganar sólo por HP/daño.

---

# 6. Regla dura anti-spam

Contrato:

> Un jugador que intente resolver TODO el boss usando exclusivamente la misma skill ofensiva debe tener 0% de victoria.

La Grulla no hace future-read.

En Fase II/III:

```text
misma skill
misma skill
misma skill
-> técnica comprendida
```

La tercera todavía resuelve.

La siguiente repetición queda anulada.

En transición Fase I -> II:

```text
2+ usos de una única skill
+ ningún ataque básico
+ ninguna técnica alternativa real
-> Fase II empieza recordándola
```

DEFENDER, curarse o esperar NO hacen olvidar una técnica.

Rompen el patrón:

- otra técnica;
- otro control;
- ataque básico.

IMPORTANTE:

```text
"básico" = comando ATACAR normal
sin técnica
sin qi
```

Ejemplo válido:

```text
Palma
ATACAR
Palma
ATACAR
```

---

# 7. Counters por tipo de skill

```text
ofensiva       -> TRAZO VACÍO
esquiva        -> PULSO FIJADO
guardia        -> RESONANCIA INTERNA
control        -> ANCLA DEL VOTO
fortificación  -> CAMPANA INVERSA
```

Counter sólo a la técnica aprendida; nunca inmunidad universal.

Ejemplo:

```text
comprender Palma
!= inmunidad al fuego
```

---

# 8. Toolkit mínimo y herramientas opcionales

Toolkit universal que debe permitir ganar:

```text
técnica raíz
ATACAR básico
DEFENDER
recursos normales
```

Técnicas opcionales:

```text
Paso de Nube
Piel de Cobre
Filamento de Agua
```

Nunca pueden ser llaves obligatorias.

Matriz de counterplay ya existe:

- `adaptive/grulla-counterplay-matrix-v0.1.mjs`
- `tests/grulla-counterplay-matrix.test.mjs`

---

# 9. Corrección crítica del baseline de HP de la Grulla

El baseline correcto recuperado es:

```text
Fase I   150 HP
Fase II  100 HP
Fase III  50 HP
TOTAL    300 HP
```

El benchmark `45 / 35 / 25` quedó invalidado/superseded como base de balance.

NO volver a usar `45/35/25` para balancear la Grulla.

Checkpoint:

`adaptive/CHECKPOINT_GRULLA_FASE1_150HP_v0.1.md`

---

# 10. Regla de trabajo para evitar timeouts

Usuario pidió explícitamente evitar intentar todo junto por riesgo de:

```text
ChatGPT stream recovery polling timed out
```

Procedimiento obligatorio:

1. trabajar una sola fase/bloque;
2. usar script reproducible, preferentemente Colab-ready para Monte Carlo pesado;
3. guardar resultado;
4. commit;
5. sólo entonces pasar al siguiente bloque.

No intentar Fase I+II+III en una sola respuesta.

---

# 11. Fase I — baseline y estado

Sólo se trabaja:

```text
FASE I — EL VOTO INMÓVIL
```

Stats actuales de sensibilidad:

```text
HP = 150
ATQ = 4
daño básico = 1d6+2
Campanada = 2d6+2
ciclo = Golpe -> Golpe -> Campanada -> Pata Inmóvil
Pata Inmóvil = +3 DEF sobre siguiente ofensiva (aún provisional)
```

Se comparan:

```text
DEF 13
DEF 14
```

Todavía NO seleccionar una.

Jugador preparado de referencia:

```text
LianQi IV
28 HP
110 qi
+3 ATQ por consagraciones
gear de sensibilidad +2 ATQ / +7 DEF
básico 1d8
1 poción
```

LianQi IV dispone de:

```text
4 PT totales
```

Toda combinación de técnicas debe respetar ese presupuesto.

---

# 12. Fase I-A — CERRADA

Grid:

```text
3 raíces
x 3 opciones tramo 1
x 3 opciones tramo 2
= 27 builds
```

Estrategias:

- SPAM
- ALTERNATE
- READER

Volumen:

```text
27 builds
x 2 DEF
x 3 estrategias
x 20.000 duelos
= 3.240.000 duelos
```

Script:

`benchmark/colab/grulla-phase1-root-grid-v0.1.py`

Resultado READER:

```text
DEF 13:
Fuego 61,5%
Metal 59,5%
Agua 61,8%
global 60,9%

DEF 14:
Fuego 55,2%
Metal 53,9%
Agua 55,0%
global 54,7%
```

Valor de leer Fase I:

```text
DEF 13:
ALTERNATE 38,3% -> READER 60,9%
+22,6 pp

DEF 14:
ALTERNATE 33,0% -> READER 54,7%
+21,7 pp
```

Documento:

`adaptive/RESULTADO_GRULLA_FASE1_150HP_ROOT_GRID_v0.1.md`

Fase I-A NO repetir.

---

# 13. Fase I-B / Paso de Nube — CERRADO

Sólo Paso, sin Piel ni Filamento.

Presupuesto:

```text
raíz = 2 PT
Paso = 0,1,2 PT
máximo total = 4 PT
```

Se probaron 16 configuraciones de Paso:

```text
base                1
sólo tramo 1        3
sólo tramo 2        3
tramo 1 + tramo 2   9
---------------------
16
```

Barrido:

```text
27 formas raíz
x 16 configuraciones Paso
x 2 DEF
x 5.000
= 4.320.000 duelos
```

Finalistas confirmados:

```text
27 formas raíz
x 3 finalistas
x 2 DEF
x 20.000
= 3.240.000 duelos
```

Mejor Paso:

```text
T1-1 Paso prolongado
+
T2-2 Paso velado

coste 5
Esquiva +25%
duración 3
```

Resultado:

```text
DEF 13 = 66,25%
DEF 14 = 59,39%
```

Comparado con READER universal:

```text
DEF 13:
60,9 -> 66,25
+5,35 pp

DEF 14:
54,7 -> 59,39
+4,69 pp
```

Paso base sin PT:

```text
DEF 13 = 39,60%
DEF 14 = 33,40%
```

Conclusión:

- encontrar manual NO equivale a botón de victoria;
- Paso bien especializado da ventaja real;
- no trivializa Fase I;
- no nerfear Paso por este resultado;
- no subir stats de Grulla por este resultado.

Script:

`benchmark/colab/grulla-phase1-paso-v0.1.py`

Documento:

`adaptive/RESULTADO_GRULLA_FASE1_PASO_v0.1.md`

Volumen útil nuevo Paso:

```text
7.560.000 duelos
```

Fase I-B/Paso NO repetir.

---

# 14. ESTADO EXACTO PARA RETOMAR

```text
FASE I-A            -> CERRADA
FASE I-B / PASO     -> CERRADO
FASE I-B / PIEL     -> PENDIENTE  <-- RETOMAR AQUÍ
FASE I-B / FILAMENTO-> PENDIENTE
FASE I-C            -> NO INICIAR TODAVÍA
FASE II             -> NO TOCAR TODAVÍA
FASE III            -> NO TOCAR TODAVÍA
```

Próximo trabajo permitido:

> Fase I-B — Piel de Cobre aislada.

Debe seguir la misma metodología de Paso:

1. respetar 4 PT total;
2. raíz conserva 2 PT;
3. Piel puede usar 0/1/2 PT;
4. generar grid legal;
5. 5.000 duelos por escenario para selección;
6. elegir finalistas;
7. 20.000 duelos por finalista;
8. comparar DEF13 vs DEF14;
9. comparar contra READER universal;
10. documentar;
11. commit;
12. detenerse.

NO pasar a Filamento en la misma respuesta.

---

# 15. Prompt de reanudación recomendado

Copiar el bloque que se entrega al usuario junto con este handoff.

La nueva conversación debe:

- leer este handoff primero;
- verificar HEAD activo;
- no rehacer Fase I-A ni Paso;
- continuar exclusivamente con Piel de Cobre;
- documentar y hacer commit antes de terminar;
- evitar cálculos multi-fase.
