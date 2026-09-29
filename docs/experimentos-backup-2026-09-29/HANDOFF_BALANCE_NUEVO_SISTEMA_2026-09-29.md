# HANDOFF — Balance de combate bajo sistema nuevo

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
HEAD de entrada a este backup: `4da38c1b617a6c4430a3c10d3b228d79f9cd7ce1`

## Guardia

- No tocar `main`.
- No merge automático.
- No implementar todavía en runtime.
- El sistema de estadísticas de `ver74` está **OBSOLETO como fuente numérica de balance**.
- Prohibido convertir ATQ/DEF/HP/Qi/Evasión o probabilidades históricas de `ver74` al contrato nuevo.
- `ver74` sólo puede consultarse como referencia histórica de UX, nomenclatura o mecánicas explícitamente preservadas, nunca para fijar magnitudes nuevas.
- Equipo existente: **desfasado / pendiente de recreación**. No participa en las pruebas actuales.

## Autoridad actual

1. `docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md`
2. `docs/experimentos/REGISTRO_UNIVERSAL_ESTADISTICAS_PROPIEDADES_COMBATE_V0_1.md`
3. `docs/experimentos/CONTRATO_MOTOR_EVENTOS_EFECTOS_V0_1.md`
4. `docs/experimentos/TECNICAS_ARCO1_DISENO_APROBADO_2026-09-28.md`
5. `docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`

## Principio de progresión cerrado

El cultivo puede otorgar automáticamente:

- Vida máxima;
- Qi máximo;
- acceso/puntos de técnica;
- desbloqueos.

El cultivo **NO** otorga universalmente sólo por subir de etapa:

- daño/Ataque;
- DEF;
- Precisión;
- Evasión;
- crítico;
- Penetración;
- Control;
- Tenacidad;
- Absorción.

El crecimiento de esas estadísticas vendrá de técnicas, ramas, equipo nuevo, buffs/debuffs y sistemas explícitos.

## Técnicas y progresión

Dirección aprobada:

- LianQi I: técnica base.
- LianQi II: Tramo I.
- LianQi III: Tramo II.
- LianQi IV: Tramo III.

Los valores actuales de daño/coste/DEF/duraciones son provisionales de benchmark salvo contrato global cerrado.

## Daño variable

El rediseño debe conservar variabilidad de daño. Los números actuales de “daño nominal” NO deben interpretarse como daño fijo final.

El marco de simulación admite:

- dados;
- rango min/max;
- distribución configurable;
- valor nominal/media objetivo.

Todavía no están congelados los dados definitivos de las técnicas.

## Espejo de Luna

Hallazgo cualitativo válido:

> una defensa activa debe justificar el turno que consume.

La propuesta `30% HP` para Espejo fue prometedora, pero los tests numéricos previos usaron perfiles heredados/derivados de datos legacy y deben repetirse bajo perfiles nuevos antes de canonizarla.

## Cuerpo-Horno

Debe balancearse por valor total:

```text
mitigación del turno defensivo
+
valor ofensivo posterior de Calor
```

No se le exige absorber lo mismo que Espejo.

## Tests anteriores

Los Pass 0/1/2/3 y tests de Espejo siguen siendo útiles como pruebas de arquitectura, metodología y detección de interacciones, pero **sus cifras no son autoridad de balance** si dependieron de:

- HP/Qi legacy;
- daño enemigo legacy;
- vieja DEF/ATQ;
- conversiones de vieja DEF a nueva Evasión;
- perfiles COMMON/ELITE/BOSS derivados de `ver74`.

## Marco futuro

Usar `experimentos/balance_nuevo/`:

- motor reutilizable;
- configuración separada;
- escenarios declarativos;
- notebook Colab;
- semilla reproducible;
- resultados exportables CSV;
- ninguna cifra legacy implícita.

El código de simulación no debe reescribirse prueba por prueba. Se modifica la configuración y la matriz de escenarios.

## Orden de trabajo

1. Marcar benchmarks legacy-contaminados como históricos/no válidos numéricamente.
2. Congelar un perfil LianQi I **nuevo**:
   - HP;
   - Qi;
   - Precisión;
   - Evasión/DEF/Tenacidad esperadas de enemigos de etapa;
   - Control de referencia;
   - distribuciones de daño de técnicas;
   - distribuciones de daño enemigas.
3. Simular sólo técnicas base de LianQi I.
4. Ajustar defensivas base.
5. Cerrar LianQi I.
6. Derivar LianQi II desde esa base:
   - sólo HP/Qi garantizados por cultivo;
   - Tramo I como principal crecimiento de build.
7. Repetir III y IV.
8. Recrear equipo bajo contrato nuevo.
9. Recién entonces ejecutar pruebas serias con equipo, builds, Concordancias e injertos en Colab.

## Huecos conocidos

- HP/Qi iniciales nuevos de LianQi I: pendientes.
- crecimiento HP/Qi II–IV: pendiente.
- distribuciones de daño variables nuevas: pendientes.
- DEF/Evasión/Tenacidad de criaturas nuevas por etapa: pendientes.
- `base_control` de Arrastre: pendiente.
- piso global de Qi: pendiente.
- equipo nuevo: pendiente.
- cuatro huecos de ramas mixtas detectados en Pass 3: pendientes de semántica standalone.



---

## Actualización posterior — progresión y equipo

Se amplió el laboratorio para probar hipótesis donde el ascenso de etapa conceda, además de HP/Qi/acceso, estadísticas de combate adicionales. Esto **no modifica el contrato canónico**: se ejecuta como sensibilidad LAB contra el control.

Archivos nuevos:

- `experimentos/balance_nuevo/progression_lab.py`
- `experimentos/balance_nuevo/equipment_lab.py`
- `docs/experimentos/AUDITORIA_EQUIPO_Y_PROGRESION_ARCO1_2026-09-29.md`

El notebook Colab fue ampliado con bloques para:

- políticas de ascenso;
- acumulación LianQi I–IV;
- disponibilidad de equipo por etapa;
- futuras matrices NAKED / EXPECTED / HIGH_ROLL.

### Auditoría de equipo actual

Actualmente obtenibles desde el ecosistema inicial:

- espada de madera — inventario inicial;
- uniforme externo — inventario inicial;
- cuchillo de hueso — sólo origen callejero;
- anillo herrumbroso — Camino de la Montaña;
- amuleto de colmillo — drop del lobo espiritual en zona inicialmente accesible.

Definidos pero sin fuente jugable activa:

- espada de hierro;
- túnica reforzada;
- bandana de cuero;
- sandalias de viento;
- uniforme interno.

Razón: `CATALOGO=[]`, comercio pendiente y `QUESTS={}`.

Consecuencia:

> El equipo actual no posee una progresión real LianQi I → IV. Antes de asignar estadísticas nuevas hay que distribuir fuentes/etapas de obtención.

### Regla de test futuro

Separar siempre:

1. crecimiento por cultivo;
2. crecimiento por rama;
3. crecimiento por equipo;
4. interacción de las tres capas.

No balancear sólo el personaje final completamente equipado.


---

## Actualización posterior — arquitectura futura de slots de equipo

Se registró una ampliación de arquitectura de equipamiento para implementar
**después de cerrar los tests actuales de LianQi I NAKED**.

No se modificó runtime/HTML y no se asignaron estadísticas nuevas.

### Arquitectura objetivo

**13 slots totales**

Equipo marcial:
- Arma
- Tocado
- Vestidura
- Brazales
- Fajín
- Piernas
- Calzado

Accesorios:
- Amuleto
- Pulsera
- Anillo I
- Anillo II

Tesoros espirituales:
- Tesoro Espiritual I
- Tesoro Espiritual II

### Reglas registradas

- Pulsera y Brazales son slots distintos.
- Piernas y Calzado son slots distintos.
- `mano` deberá normalizarse a Arma.
- `torso` deberá normalizarse a Vestidura.
- `cabeza` deberá presentarse como Tocado.
- `cuello` deberá normalizarse a Amuleto.
- `dedo` deberá pasar a dos slots independientes: Anillo I / Anillo II.
- Las Sandalias de viento deberán ocupar Calzado cuando se haga la migración.
- Los dos slots de Tesoro Espiritual existen como capacidad estructural y
  **no se bloquean por etapa**.
- Un slot de Tesoro vacío simplemente significa que el jugador aún no posee
  un objeto compatible.
- La obtención/rareza/contenido del mundo controla cuándo aparecen tesoros;
  no una barrera artificial de etapa.
- Tener dos slots NO implica entregar dos tesoros en el Arco 1. Pueden
  introducirse tesoros adicionales en arcos posteriores.

### Guardia

Antes de implementar esta arquitectura:

1. cerrar LianQi I NAKED;
2. cerrar sus parámetros de combate relevantes;
3. mantener todo el equipo fuera de los benchmarks NAKED;
4. después diseñar fuentes, etapas y stats nuevos;
5. validar NAKED / MINIMAL / EXPECTED / HIGH_ROLL.

No tocar runtime por esta decisión durante el bloque actual.


---

## Pendiente agendado — hotfix narrativo de Concordancias post-A07

Se registró un hotfix narrativo para ejecutar **después de cerrar e integrar los
diálogos NPC de A07**.

Documento de trabajo:

- `docs/experimentos/PENDIENTE_HOTFIX_CONCORDANCIAS_NARRATIVA_ARCO1_2026-09-29.md`

Objetivo:

- fijar Concordancia como enseñanza característica/básica de la Grulla Blanca;
- no añadir bonus ni sistema nuevo;
- auditar Prólogo → M18 + Epílogo;
- revisar siembra, spoilers, terminología, doctrina, conocimiento NPC y
  compatibilidad con flags/gates;
- aplicar el hotfix sólo después de la auditoría y de congelar los diálogos.

Guardia: no tocar runtime, quests ni diálogos actuales por este pendiente hasta
cerrar A07.


---

## Actualización posterior — PHASE A perfiles abstractos LianQi I

Se añadió:

- `experimentos/balance_nuevo/phase_a_enemy_profiles_lab.py`
- `docs/experimentos/LAB_PERFILES_ENEMIGO_LIANQI_I_PHASE_A_2026-09-29.md`

Todo sigue en **LAB**.

Perfiles evaluados:

- L1_SOFT = Evasión 10 / DEF 1
- L1_STANDARD = Evasión 20 / DEF 2
- L1_ARMORED = Evasión 20 / DEF 4
- L1_EVASIVE = Evasión 35 / DEF 2

Con ataque básico `1d4+4` y técnicas `narrow`, el perfil STANDARD produce
aprox. 80% de impacto normal (85% con Precisión adicional) y un premium medio
de técnica de ~1.51x. El perfil ARMORED eleva el premium medio a ~1.92x.

Hallazgo adicional: a igual media, las variantes `wide` empiezan a producir
impactos acertados de 0 contra DEF 4 en Agua/Tierra/Viento, mientras las
variantes `narrow` no.

Hipótesis principal para continuar, todavía NO canonizada:

- referencia ordinaria: E20 / DEF2;
- ataque básico: 1d4+4;
- técnicas: narrow;
- DEF4 como perfil resistente/stress;
- Evasión ~35 como perfil evasivo especializado.

Antes de desbloquear el runner estricto de PHASE A se requiere decisión humana
para promover esos candidatos de LAB a PROVISIONAL.


---

## Actualización posterior — inicio de testeos estrictos LianQi I

### PHASE A

**PASS PROVISIONAL**

Promovidos a PROVISIONAL:

- enemigo de referencia: Evasión 20 / DEF 2;
- ataque básico: 1d4+4;
- técnicas iniciales: variantes narrow.

Validación:

- 300.000 acciones por acción/raíz;
- cross-check determinístico por enumeración exacta;
- desviación máxima Monte Carlo vs exacto <0.25%;
- 0% impactos conectados anulados por DEF en el baseline.

Documento:

- `docs/experimentos/TEST_LIANQI_I_NAKED_PHASE_A_2026-09-29.md`

### PHASE B — presupuesto Qi

Barrido LAB:

- Qi máximo 18/24/30/36/42;
- pisos de coste 1/3/5/6.

Hallazgo:

- las cinco técnicas iniciales cuestan efectivamente 6 Qi en su raíz principal;
- Agua: 7 × 0.90 = 6.3 -> ROUND_HALF_UP = 6;
- pisos 1–6 son indistinguibles en este subtest y el piso global sigue PENDIENTE;
- banda principal de Qi para pruebas siguientes: 24–30 LAB.

Documento:

- `docs/experimentos/LAB_LIANQI_I_NAKED_PHASE_B_QI_2026-09-29.md`

### Cruce ofensivo HP × Qi

Se simularon 20.000 combates por raíz/combinación sin respuesta enemiga.

Dos parejas principales LAB:

1. COMPACTA: Qi 24 / HP enemigo 20
   - ~4.08 turnos medios;
   - ~28% de combates usan ataque básico.

2. EXTENDIDA: Qi 30 / HP enemigo 28
   - ~5.51 turnos medios;
   - ~40% de combates usan ataque básico.

No fijar todavía Qi máximo ni HP enemigo. Falta incorporar presión enemiga,
HP/DEF/Evasión del jugador y valor real de utilidades/defensivas.

Documento:

- `docs/experimentos/LAB_LIANQI_I_HP_QI_OFENSIVO_2026-09-29.md`

Runners nuevos:

- `experimentos/balance_nuevo/phase_a_exact_check.py`
- `experimentos/balance_nuevo/phase_b_qi_budget_lab.py`
- `experimentos/balance_nuevo/phase_b_hp_qi_offense_lab.py`


---

## Actualización posterior — PHASE C presión enemiga

Se añadió:

- `experimentos/balance_nuevo/phase_c_pressure_lab.py`
- `docs/experimentos/LAB_LIANQI_I_PHASE_C_PRESION_2026-09-29.md`

Primer duelo bidireccional LAB:

- jugador actúa primero;
- usa técnica mientras tenga Qi;
- luego ataque básico;
- enemigo responde con ataque directo si sigue vivo.

Se compararon COMPACTA y EXTENDIDA, perfiles de HP/DEF/Evasión del jugador,
Precisión enemiga 90/100 y daño enemigo 1d4+3 / 2d4+1 / 1d6+3.

Confirmaciones de 100.000 duelos por raíz:

COMPACTA P24/D1/E0, enemigo Precisión100 + 2d4+1:
- win medio 86.36%;
- 3.83 turnos;
- 39.87% HP restante;
- 23.56% usa básico.

EXTENDIDA P30/D1/E5, enemigo Precisión100 + 2d4+1:
- win medio 82.68%;
- 5.16 turnos;
- 33.36% HP restante;
- 36.02% usa básico.

Shortlist LAB para continuar:
- jugador HP30 / Qi30 / DEF1 / EVA5;
- enemigo HP28 / PREC100 / EVA20 / DEF2 / ataque 2d4+1;
- jugador primero.

No promover todavía: Agua queda en 65.22% win porque Arrastre/Control aún no
están valorados. Fuego queda en 93.85%. La diferencia exige probar utilidad
antes de ajustar daño.

PHASE C sigue NO PASS.


---

## Actualización posterior — A/B Precisión/Evasión cap95 vs cap100

Se añadió:

- `experimentos/balance_nuevo/phase_c_accuracy_cap_lab.py`
- `docs/experimentos/LAB_PRECISION_EVASION_CAP95_VS_100_2026-09-29.md`

Comparación:

- contrato actual: `clamp(Precisión - Evasión, 5, 100)`;
- variante: `clamp(Precisión - Evasión, 5, 95)`.

Hallazgos:

1. Con EVA base 5 y PREC enemigo <=100, ambos caps son prácticamente
   equivalentes; cap95 no interviene.
2. Con EVA 0 / PREC100, cap95 regala 5% de fallo a raíces sin Evasión.
3. Cap95 comprime la ventaja efectiva de Viento cerca del techo:
   - PREC100 / EVA0: Viento pasa de ventaja de 10 pp (cap100) a 5 pp (cap95).
   - PREC105 / EVA0: cap95 puede anular completamente la ventaja de +10 EVA.
4. Mantener cap100 y variar la Precisión propia de cada monstruo preserva mejor
   la relación transparente Precisión/Evasión.

Resultado LAB:

- **cap100 permanece como candidato principal**;
- el problema estaba en usar PREC100 como enemigo ordinario universal;
- usar PREC90 como centro LAB del próximo enemigo ordinario;
- banda LAB sugerida: común 85–90, competente 90–95, entrenado 95–100,
  especialista >100.

No se modifica el contrato CANON todavía; la decisión se sostiene como
resultado de benchmark para los tests siguientes.


---

## Actualización posterior — Arrastre + Peso en PHASE C

Se añadió:

- `experimentos/balance_nuevo/phase_c_arrastre_peso_lab.py`
- `docs/experimentos/LAB_LIANQI_I_PHASE_C_ARRASTRE_PESO_2026-09-29.md`

Resultado principal con PREC enemiga 90:

- Agua sin Arrastre: ~74.4% win.
- Arrastre 45% efectivo: ~86.2%.
- Arrastre 55% efectivo: ~87.6%.
- Arrastre 65% efectivo: ~88.8%.

Con ~55% efectivo Agua queda cerca de Viento sin tocar su daño y evita ~1.46
acciones enemigas por combate, respetando el lockout.

Peso:
- baseline Tierra ~89.6% win;
- con Peso conservador (~1 acción futura): ~91%;
- con interpretación de 2 acciones futuras: ~92.2–92.5%;
- STACK_REFRESH vs INDEPENDENT cambia poco en este duelo;
- la semántica exacta de stacking/duración sigue PENDIENTE.

Con utilidades activas y PREC enemigo 90:
- Fuego ~95.7%;
- Metal ~90.5%;
- Agua ~87.7%;
- Tierra ~92.6%;
- Viento ~88.1%;
- promedio ~90.9%.

Conclusión LAB:
- no subir daño de Agua por ahora;
- PREC90 sigue como centro LAB de criatura común;
- PREC95 como referencia más exigente;
- resolver stacking/duración de Peso y Tenacidad/base_control antes de PASS de
  PHASE C.


---

## Actualización posterior — Arrastre, Peso y escala Control/Tenacidad

Se añadieron:

- `experimentos/balance_nuevo/phase_c_water_earth_utility_lab.py`
- `experimentos/balance_nuevo/phase_c_control_tenacity_lab.py`
- `docs/experimentos/LAB_LIANQI_I_ARRASTRE_PESO_PHASE_C_2026-09-29.md`
- `docs/experimentos/LAB_LIANQI_I_CONTROL_TENACIDAD_ARRASTRE_2026-09-29.md`

Duelo central LAB:
- jugador HP30 / Qi30 / DEF1 / EVA5;
- enemigo HP28 / PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- cap de impacto 100.

Arrastre:
- anti-bloqueo preservado;
- banda efectiva prometedora: 45–55%;
- centro LAB: ~50%;
- con ~50% Agua pasa de ~74.1% win sin Arrastre a ~86.8%;
- evita ~1.36 acciones enemigas por duelo;
- no subir daño de Latigazo por ahora.

Relación identificada:
`base_control - Tenacidad_referencia ≈ 45` para Agua principal (+5 Control).

Ancla LAB conveniente, NO PROVISIONAL:
- Arrastre base_control 65;
- Tenacidad ordinaria 20;
- Agua +5 Control;
- probabilidad efectiva 50%.

Con base_control65:
- Tenacidad10 -> 60%;
- Tenacidad20 -> 50%;
- Tenacidad30 -> 40%;
- Tenacidad40 -> 30%.

Peso:
- -3 EVA/carga, duración2, max2 sigue sano;
- sin Peso Tierra ~89.6% win;
- STACK_REFRESH ~91.9%;
- INDEPENDENT ~91.1%;
- STACK_REFRESH queda como candidato semántico principal LAB por coherencia con
  un estado único con cargas y duración, pero falta decisión de contenido.

Comparación con utilidades centrales:
- Fuego ~95.7%;
- Tierra+Peso(refresh) ~91.9%;
- Metal ~90.6%;
- Viento ~88.0%;
- Agua+Arrastre50 ~86.8%.

PHASE C sigue NO PASS. Siguiente bloque recomendado: primeras defensivas base,
empezando por Piel de Cobre y Espejo de Luna, sin elevar todavía estos números
a CANON.


---

## Actualización posterior — semántica de Peso

Se añadió:

- `docs/experimentos/LAB_LIANQI_I_PESO_SEMANTICA_2026-09-29.md`

Resultado LAB:

- `STACK_REFRESH` es el candidato principal para Peso;
- razón principal: la progresión habla de un único estado Peso con máximo de
  cargas y duración compartida (2 -> 3 al máximo), lo que encaja mejor que
  cargas independientes;
- candidato de duración:
  - owner = objetivo afectado;
  - duration_unit = TARGET_TURN;
  - duration = 2;
  - decay en TURN_END del objetivo;
  - cada aplicación válida añade una carga y refresca la duración completa;
  - al llegar a 0 expiran todas las cargas.

A/B 200k duelos:
- sin Peso ~89.65% win;
- STACK_REFRESH ~91.80%;
- INDEPENDENT ~91.11%;
- una variante que garantiza dos acciones futuras completas sube sólo a ~92.4%
  pero es semánticamente menos natural para un debuff del objetivo.

No se modifica todavía el documento autoritativo ni runtime.


---

## Decisión aprobada — Arrastre / Tenacidad / Peso pasan a PROVISIONAL

Aprobación humana registrada el 2026-09-29.

Se promueven para los siguientes benchmarks, **no a CANON**:

### Arrastre
- `base_control = 65` PROVISIONAL.
- Tenacidad de referencia ordinaria LianQi I = `20` PROVISIONAL.
- Agua principal aporta +5 Control CANON.
- Resultado de referencia: `65 + 5 - 20 = 50%` de Arrastre.
- Anti-bloqueo se conserva.

### Peso
- `-3 EVA/carga`, máximo 2, duración 2.
- `stacking_mode = STACK_REFRESH` PROVISIONAL.
- owner = objetivo afectado.
- `duration_unit = TARGET_TURN`.
- decremento en `TURN_END` del objetivo.
- cada aplicación válida añade una carga y refresca la duración completa.
- al expirar se eliminan todas las cargas.

Guardia:
- sin cambio de runtime/HTML;
- sin elevar a CANON;
- rebenchmark obligatorio con defensivas y posteriores capas del sistema.

### Siguiente bloque activo
**PHASE C — defensivas base**:
1. Piel de Cobre;
2. Espejo de Luna;
3. después comparar las cinco defensivas base antes de cerrar LianQi I.


---

## Actualización posterior — defensivas base + economía mixta de Qi

Se añadieron:

- `experimentos/balance_nuevo/phase_c_defensives_lab.py`
- `experimentos/balance_nuevo/phase_b_mixed_qi_lab.py`
- `experimentos/balance_nuevo/phase_c_all_defensives_lab.py`
- `docs/experimentos/LAB_LIANQI_I_DEFENSIVAS_PHASE_C_2026-09-29.md`
- `docs/experimentos/LAB_LIANQI_I_QI_MIXTO_2026-09-29.md`
- `docs/experimentos/LAB_LIANQI_I_CINCO_DEFENSIVAS_PHASE_C_2026-09-29.md`

### Espejo y Piel

Espejo 12%:
- FAIL LAB;
- suele romperse en un impacto;
- Reflujo casi no participa;
- apertura reduce win de Agua respecto de ofensiva pura.
- banda siguiente prometedora: 22–25% HP de Absorción.

Piel:
- magnitud defensiva base PASS LAB;
- con Qi30/coste7 sufría un acantilado de recurso;
- con economía que permite una ofensiva adicional se vuelve fuerte.

### Economía mixta

Todas las defensivas base actuales cuestan 7 Qi.
Agua las convierte en 6 efectivos por raíz.

Qi30:
- 5 ofensivas6;
- pero defensiva7 + sólo 3 ofensivas6;
- sobran 5 Qi.

Qi31:
- 5 ofensivas6;
- defensiva7 + 4 ofensivas6;
- defensiva6 + 4 ofensivas6.

Por ello `Qi máximo = 31` emerge como candidato estructural LAB para comparar
cargas mixtas. NO PROVISIONAL todavía.

### Screen cinco defensivas con Qi31

120k duelos por estrategia:

- Fuego sólo ofensiva ~95.76%; Cuerpo-Horno15 ~94.12%.
- Metal sólo ofensiva ~90.71%; Armadura ~92.79%.
- Agua ofensiva+Arrastre ~86.75%; Espejo12 ~81.33%.
- Tierra ofensiva+Peso ~91.75%; Piel ~96.28%.
- Viento sólo ofensiva ~87.98%; Paso +15 EVA/2t ~77.81%.

Lectura:
- Metal = PASS inicial.
- Tierra = PASS fuerte; vigilar sobrepotencia bajo muchos impactos.
- Fuego15 = FAIL marginal; siguiente banda Absorción 22–25%.
- Agua12 = FAIL claro; siguiente banda Absorción 22–25%.
- Viento +15 EVA/2t = FAIL claro; necesita revisar magnitud/duración/función,
  no sólo +5 EVA.

Stress COMMON/PRECISE/HEAVY/DANGEROUS confirmó que Fuego/Agua/Viento no se
rescatan simplemente aumentando la presión del enemigo; Metal y Tierra sí
mantienen valor positivo.

PHASE C sigue NO PASS.


---

## Actualización posterior — recalibración defensiva, Qi31 y stress multi-enemigo

Se añadieron:

- experimentos/balance_nuevo/phase_c_defensive_recalibration_lab.py
- experimentos/balance_nuevo/phase_c_multi_enemy_defensive_stress_lab.py
- experimentos/balance_nuevo/phase_c_piel_scaling_lab.py
- docs/experimentos/LAB_LIANQI_I_RECALIBRACION_DEFENSIVAS_2026-09-29.md
- docs/experimentos/LAB_LIANQI_I_QI31_VALIDACION_DEFENSIVAS_2026-09-29.md
- docs/experimentos/LAB_LIANQI_I_STRESS_MULTI_ENEMIGO_DEFENSIVAS_2026-09-29.md
- docs/experimentos/LAB_LIANQI_I_PIEL_ESCALADO_MULTIIMPACTO_2026-09-29.md

### Recalibración defensiva — candidatos LAB

Fuego / Cuerpo-Horno:
- 15% sigue FAIL;
- banda 22–25% probada;
- candidato LAB principal: 25% HP Absorción / 2 turnos / coste7;
- queda aproximadamente en paridad de win con ofensiva pura, pero conserva
  ~5–6 pp más HP;
- no añadir Calor a la base.

Agua / Espejo:
- 12% sigue FAIL;
- candidato LAB principal: 24% HP Absorción / Reflujo25% / 3 turnos;
- mejora win ~2 pp y HP restante ~5–6 pp frente a ofensiva+Arrastre;
- no modificar Reflujo todavía.

Viento / Paso:
- +15 EVA /2t FAIL;
- mejoras pequeñas no alcanzan;
- candidato puramente numérico LAB: +35 EVA /4t;
- conserva hooks base EVASION_GRANTED + DEFENSIVE_DURATION;
- no mueve CORRIENTE_CLARA/REACTIVE_RESPONSE a la base;
- si se adopta, los números de ramas I–III deben recalibrarse porque la
  escalera provisional actual +15→+30 / duración2→4 queda superada.

### Qi31

Qi31 continúa como candidato estructural LAB fuerte:
- cinco ofensivas de coste6;
- o defensiva7 + cuatro ofensivas6;
- o defensiva Agua efectiva6 + cuatro ofensivas6.

Qi30 favorece Agua por acantilado de coste.
Qi32–35 no añaden acciones respecto de31.
Qi36 crea otro desfase; Qi37 sería el siguiente escalón completo pero aumenta
demasiado el presupuesto base para resolver este problema.

No promover Qi31 todavía.

### Stress multi-enemigo real

Se usaron enemigos con HP propio, manteniendo HP total ~28:
- 2 enemigos = 14+14;
- 3 enemigos = 10+9+9.

Hallazgo:
- Piel actual escala de forma extrema con múltiples acciones.
- Aproximado:
  - 2 enemigos: Tierra ofensiva ~61% vs Piel ~89%;
  - 3 enemigos: Tierra ofensiva ~18% vs Piel ~68%.
- Viento gana valor naturalmente al aumentar las acciones entrantes.
- Placas de Metal se consumen rápidamente y no se buffean por este stress.
- Horno/Espejo comparten reserva finita y no son defensas de enjambre por
  defecto.

### Piel — variantes LAB

La causa dominante no es la frecuencia del trigger por acción, sino alcanzar
DEF plana muy alta + extensión.

CURRENT:
- DEF total con Piel: 4→5→6.

Candidato LAB principal DEF_CAP2:
- Arraigo1 → DEF4;
- Arraigo2 → DEF5;
- Arraigo3 → sigue DEF5;
- tercera carga conserva Tenacidad y activa extensión;
- mantiene trigger por acción;
- mantiene 3 Arraigos;
- reduce escalado multiimpacto sin rediseñar toda la técnica.

Resultados aproximados DEF_CAP2:
- 1 enemigo ~96%;
- 2 enemigos ~85%;
- 3 enemigos ~58%.

No promover ni modificar Piel autoritativa todavía.

### Estado

PHASE A = PASS PROVISIONAL.
PHASE B = PARCIAL; Qi31 es el candidato LAB actual.
PHASE C = NO PASS.

Bloque pendiente antes de promoción:
1. validar Piel CURRENT vs DEF_CAP2 contra varios perfiles;
2. volver a ejecutar las cinco defensivas con candidato de Piel elegido;
3. revisar ramas I–III de Horno/Espejo/Paso si sus nuevos valores base
   sobreviven;
4. recién entonces promover cifras de PHASE B/C.


---

## Metodología por etapas — Piel de Cobre

A partir de este punto, la comparación CURRENT vs DEF_CAP2 se hará de una sola
variable/escenario por etapa, evitando mezclar perfiles y conclusiones.

### ETAPA 1 — 1v1 enemigo común — CERRADA

Documento:
- `docs/experimentos/ETAPA1_PIEL_CURRENT_VS_DEF_CAP2_1V1_COMUN_2026-09-29.md`

Baseline:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- enemigo HP28 / PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- Piel de apertura;
- Peso PROVISIONAL STACK_REFRESH.

200.000 duelos:
- CURRENT: 96.21% win / 60.68% HP restante.
- DEF_CAP2: 95.60% win / 58.39% HP restante.
- delta win ≈ -0.61 pp.
- delta HP restante ≈ -2.29 pp.

Repetición 4×100k:
- delta win: -0.666 / -0.521 / -0.518 / -0.555 pp.

Conclusión:
- DEF_CAP2 **PASS para continuar testeando**;
- no rompe Piel en 1v1 común;
- no se promueve todavía.

Siguiente única etapa:
- ETAPA 2 — CURRENT vs DEF_CAP2 contra enemigo pesado 1v1.


### ETAPA 2 — 1v1 enemigo pesado — CERRADA

Documento:
- `docs/experimentos/ETAPA2_PIEL_CURRENT_VS_DEF_CAP2_1V1_PESADO_2026-09-29.md`

Único cambio respecto de Etapa 1:
- daño enemigo `2d4+1 -> 1d6+3`.

200.000 duelos:
- CURRENT: 93.91% win / 55.92% HP restante.
- DEF_CAP2: 92.96% win / 53.15% HP restante.
- delta win ≈ -0.95 pp.
- delta HP restante ≈ -2.78 pp.

Repetición 4×100k:
- delta win: -0.898 / -0.895 / -1.013 / -1.013 pp.

Conclusión:
- DEF_CAP2 PASS para continuar;
- pérdida medible pero moderada;
- Piel conserva función defensiva fuerte contra daño alto;
- no se promueve todavía.

Siguiente única etapa:
- ETAPA 3 — CURRENT vs DEF_CAP2 contra enemigo preciso 1v1.


### ETAPA 3 — 1v1 enemigo preciso — CERRADA

Documento:
- `docs/experimentos/ETAPA3_PIEL_CURRENT_VS_DEF_CAP2_1V1_PRECISO_2026-09-29.md`

Único cambio respecto de Etapa 1:
- Precisión enemiga `90 -> 100`.
- daño se mantiene en `2d4+1`.

200.000 duelos:
- CURRENT: 94.70% win / 57.76% HP restante.
- DEF_CAP2: 93.87% win / 54.93% HP restante.
- delta win ≈ -0.83 pp.
- delta HP restante ≈ -2.83 pp.

Repetición 4×100k:
- delta win: -0.853 / -0.818 / -0.792 / -0.810 pp.

Conclusión:
- DEF_CAP2 PASS para continuar;
- la mayor precisión no cambia cualitativamente la comparación;
- no se promueve todavía.

Siguiente única etapa:
- ETAPA 4 — CURRENT vs DEF_CAP2 contra 2 enemigos.


### ETAPA 4 — 2 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA4_PIEL_CURRENT_VS_DEF_CAP2_2_ENEMIGOS_2026-09-29.md`

Escenario:
- 2 enemigos reales de 14 HP;
- HP total ~28;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- una acción por enemigo vivo y ronda.

200.000 combates:
- CURRENT: 88.83% win / 46.52% HP restante.
- DEF_CAP2: 84.91% win / 40.97% HP restante.
- delta win ≈ -3.92 pp.
- delta HP restante ≈ -5.54 pp.

Repetición 4×100k:
- delta win: -4.040 / -3.947 / -3.766 / -3.882 pp.

Hallazgo:
- primera etapa donde DEF_CAP2 deja de ser casi equivalente a CURRENT;
- ambas variantes alcanzan Arraigo máximo ~2.96;
- ambas activan extensión ~96%;
- el recorte proviene específicamente de limitar DEF máxima 6 -> 5;
- DEF_CAP2 sigue siendo viable, pero entra en zona de decisión.

Siguiente única etapa:
- ETAPA 5 — CURRENT vs DEF_CAP2 contra 3 enemigos.


### ETAPA 5 — 3 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA5_PIEL_CURRENT_VS_DEF_CAP2_3_ENEMIGOS_2026-09-29.md`

Escenario:
- 3 enemigos reales 10 + 9 + 9 HP;
- HP total 28;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1;
- una acción por enemigo vivo y ronda.

200.000 combates:
- CURRENT: 68.04% win / 26.72% HP restante.
- DEF_CAP2: 57.90% win / 19.50% HP restante.
- delta win ≈ -10.14 pp.
- delta HP restante ≈ -7.22 pp.

Repetición 4×100k:
- delta win: -10.212 / -10.050 / -10.181 / -9.903 pp.

Contexto:
- Tierra sin Piel en el mismo escenario ≈17.34% win.
- DEF_CAP2 sigue siendo una defensiva muy fuerte (~58% win) y conserva
  Arraigo/extension prácticamente intactos.

Conclusión:
- CURRENT amplifica demasiado la tercera unidad de DEF bajo múltiples impactos.
- DEF_CAP2 logra el patrón buscado: casi no altera 1v1, recorta progresivamente
  al crecer la cantidad de impactos.
- DEF_CAP2 pasa a ser candidato principal LAB frente a CURRENT.
- todavía NO PROVISIONAL.

Siguiente única etapa:
- ETAPA 6 — valorar la tercera carga de DEF_CAP2 contra Control enemigo
  (Tenacidad + extensión), sin abrir otras defensivas.


### ETAPA 6 — tercer Arraigo frente a Control — CERRADA

Documento:
- `docs/experimentos/ETAPA6_PIEL_TERCER_ARRAIGO_CONTROL_2026-09-29.md`

Pregunta:
- si DEF_CAP2 elimina la tercera unidad incremental de DEF, ¿la tercera carga
  sigue teniendo valor por Tenacidad + extensión?

Resultado determinístico bajo fórmula CANON:
- Tierra sola: Tenacidad5.
- 2 Arraigos: Tenacidad11.
- 3 Arraigos: Tenacidad14.
- tercer Arraigo = +3 Tenacidad = -3 pp de P(Control) por intento en rango
  lineal.
- al alcanzar 3 Arraigos se activa +1 turno de duración; ese turno conserva
  +9 Tenacidad de Piel frente a Piel expirada.

Ejemplo ilustrativo con Control efectivo65, no canónico:
- Tierra sola: 60% Control.
- 2 Arraigos: 54%.
- 3 Arraigos: 51%.
- horizonte 3 intentos:
  - 2 Arraigos y luego expiración: 1.68 aplicaciones esperadas;
  - 3 Arraigos + extensión: 1.53;
  - +3.30 pp de probabilidad de resistir los tres.

Conclusión:
- PASS;
- la tercera carga de DEF_CAP2 no queda decorativa;
- CURRENT y DEF_CAP2 conservan igual Tenacidad y extensión;
- la única diferencia sigue siendo la unidad adicional de DEF de CURRENT.

Estado DEF_CAP2:
- Etapas1–3 PASS 1v1.
- Etapa4 recorte visible con2 enemigos.
- Etapa5 candidato principal LAB con3 enemigos.
- Etapa6 PASS frente al eje Control/Tenacidad.

Siguiente única etapa:
- revisión conjunta Etapas1–6 para decidir si DEF_CAP2 pasa de LAB a
  PROVISIONAL como base de Piel.


### ETAPA 7 — cierre de Piel base — CERRADA

Documento:
- `docs/experimentos/ETAPA7_CIERRE_PIEL_DEF_CAP2_PROVISIONAL_2026-09-29.md`

Decisión:
- `DEF_CAP2` pasa de LAB a **PROVISIONAL** para Piel de Cobre base.
- No pasa a CANON.

Curva PROVISIONAL:

```text
Piel aporta:
1 Arraigo -> +3 DEF / +3 Tenacidad
2 Arraigos -> +4 DEF / +6 Tenacidad
3 Arraigos -> +4 DEF / +9 Tenacidad
```

Con DEF base1 del benchmark:
- DEF total 4 -> 5 -> 5.

Se conserva:
- coste7;
- duración3;
- +2 DEF inmediata;
- 1 Arraigo inicial;
- máximo3;
- +3 Tenacidad por Arraigo;
- trigger reactivo;
- trigger fuerte;
- extensión al máximo;
- Eco de Tierra.

Motivo:
- 1v1: impacto mínimo (~0.6–1.0 pp de win).
- 2 enemigos: recorte ~3.9 pp.
- 3 enemigos: recorte ~10.1 pp, pero DEF_CAP2 conserva ~58% win frente a
  ~17% sin Piel.
- tercer Arraigo conserva valor por +3 Tenacidad y extensión.

Documento autoritativo de técnicas actualizado.

Guardia:
- ramas de fortificación Corteza Endurecida / Estratos Compactos /
  Cuerpo de Roca quedan PENDIENTES DE REBENCHMARK porque sus números dependían
  de la antigua curva 4->5->6.
- sin runtime/HTML.


### ETAPA 8A — Corteza Endurecida · 1v1 común — CERRADA

Documento:
- `docs/experimentos/ETAPA8A_CORTEZA_ENDURECIDA_1V1_2026-09-29.md`

Se compararon cuatro curvas sobre Piel DEF_CAP2:
- BASE: 1/2/2.
- PLUS1_CAP: 2/3/3.
- DOUBLE_CAP: 2/4/4.
- PROGRESSIVE: 2/3/4.

Hallazgo:
- más DEF reduce ON_HP_DAMAGE y, por tanto, reduce generación de Arraigo y
  frecuencia de extensión;
- DOUBLE_CAP erosiona demasiado la mecánica reactiva para la ganancia extra;
- PROGRESSIVE reabre crecimiento de DEF en el tercer Arraigo, justo el problema
  corregido por DEF_CAP2.

Candidato LAB seleccionado:
- `CORTEZA_PLUS1_CAP`.

Curva:
- contribución DEF de Arraigo con Corteza = 2 / 3 / 3;
- Piel aporta total = +4 / +5 / +5 DEF;
- con DEF base1 del benchmark = DEF total 5 -> 6 -> 6.

Vs Piel base en 1v1 común:
- +0.54 a +0.76 pp de win según semilla;
- ~+3.0 pp de HP restante;
- mantiene mejora clara sin reabrir la tercera unidad incremental de DEF.

Estado:
- PASS para continuar;
- todavía NO PROVISIONAL.

Siguiente única etapa:
- ETAPA 8B — CORTEZA_PLUS1_CAP contra 2 enemigos.


### ETAPA 8B — Corteza Endurecida · 2 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA8B_CORTEZA_ENDURECIDA_2_ENEMIGOS_2026-09-29.md`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 2 enemigos reales de 14 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Comparación:
- Piel base PROVISIONAL: DEF total 4 -> 5 -> 5.
- Piel + Corteza candidata: DEF total 5 -> 6 -> 6.

200.000 combates:
- base: 84.91% win / 40.97% HP restante.
- Corteza: 89.41% win / 48.55% HP restante.
- delta win ≈ +4.50 pp.
- delta HP ≈ +7.58 pp.
- extensión: 95.90% -> 78.44%.

Repetición 4×100k:
- delta win: +4.611 / +4.592 / +4.531 / +4.562 pp.
- delta HP: +7.54 / +7.61 / +7.49 / +7.58 pp.
- delta extensión: alrededor de -17.4 pp.

Lectura:
- Corteza fortalece de forma clara y estable.
- no devuelve crecimiento de DEF al tercer Arraigo;
- más DEF reduce ON_HP_DAMAGE, por lo que baja generación de Arraigo y
  extensión: existe autolimitación sistémica;
- contra 2 enemigos no hay evidencia suficiente de sobreescalado.

Estado:
- PASS para continuar;
- CORTEZA_PLUS1_CAP sigue candidato principal LAB;
- todavía NO PROVISIONAL.

Siguiente única etapa:
- ETAPA 8C — Corteza candidata contra 3 enemigos.


### ETAPA 8C — Corteza Endurecida · 3 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA8C_CORTEZA_ENDURECIDA_3_ENEMIGOS_2026-09-29.md`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 3 enemigos reales 10+9+9 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Comparación:
- Piel base PROVISIONAL: DEF total 4 -> 5 -> 5.
- Piel + Corteza: DEF total 5 -> 6 -> 6.

200.000 combates:
- base: 57.90% win / 19.50% HP restante.
- Corteza: 70.03% win / 28.83% HP restante.
- delta win ≈ +12.13 pp.
- delta HP ≈ +9.33 pp.
- extensión: 99.42% -> 92.34%.

Repetición 4×100k:
- delta win: +12.239 / +12.117 / +11.862 / +11.947 pp.
- delta HP: +9.40 / +9.05 / +9.03 / +9.09 pp.

Lectura:
- fortificación escala fuerte con múltiples impactos, como se esperaba;
- aun así, Corteza requiere inversión de Tramo I y no devuelve crecimiento de
  DEF en el tercer Arraigo;
- Piel+Corteza (~70%) queda apenas por encima de la antigua Piel base
  CURRENT (~68%) en 3 enemigos;
- mayor DEF reduce ON_HP_DAMAGE y autolimita Arraigo/extensión.

Decisión:
- `CORTEZA_PLUS1_CAP` pasa de LAB a **PROVISIONAL**.
- curva de contribución Arraigo: 2 / 3 / 3;
- Piel+Corteza aporta +4 / +5 / +5 DEF;
- con DEF base1: DEF total 5 -> 6 -> 6.

Guardia para Tramos II/III:
- no continuar con escalera lineal de +1 DEF permanente;
- Estratos Compactos y Cuerpo de Roca siguen PENDIENTES DE REBENCHMARK;
- explorar retornos decrecientes, condiciones o ventanas defensivas.


### ETAPA 9A — Estratos Compactos · screen estructural 1v1 — CERRADA

Documento:
- docs/experimentos/ETAPA9A_ESTRATOS_COMPACTOS_SCREEN_1V1_2026-09-29.md

Runner/checkpoint:
- experimentos/balance_nuevo/etapa9a_estratos_compactos_screen.py

Problema:
- no continuar escalera permanente de DEF hacia 7+;
- Estratos debe funcionar incluso sin Corteza.

Candidato principal LAB:
- ESTRATO_REACTIVO_2.
- al aumentar Arraigo y alcanzar 2 o 3: gana/refresca 1 Estrato;
- máximo 1;
- siguiente impacto directo conectado: +2 DEF sólo para ese impacto;
- se consume al conectar;
- evasión no consume;
- salto 1->3 genera un solo Estrato;
- ascenso gradual puede proteger hasta dos impactos por activación.

Screen 50k, seed 20260929:
- común 2d4+1, Piel base: 95.60% -> 96.10% win; HP +2.14 pp.
- común, Piel+Corteza: 96.37% -> 96.31%; HP +0.08 pp.
- heavy 1d6+3, Piel base: 92.99% -> 93.92%; HP +3.10 pp.
- heavy, Piel+Corteza: 94.31% -> 94.55%; HP +1.20 pp.

Lectura:
- funciona sin Corteza;
- con Corteza muestra retornos decrecientes en enemigo común;
- gana valor frente a impactos pesados;
- evita DEF7 permanente y limita usos por transiciones de Arraigo.

Estado:
- candidato principal LAB;
- NO PROVISIONAL todavía;
- no runtime/HTML.

Siguiente única etapa:
- ETAPA 9B — ESTRATO_REACTIVO_2 contra 2 enemigos.
