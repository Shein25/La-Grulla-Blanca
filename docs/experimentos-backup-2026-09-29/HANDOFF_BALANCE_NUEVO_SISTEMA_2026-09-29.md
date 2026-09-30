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


### ETAPA 9B — Estratos Compactos · 2 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA9B_ESTRATOS_COMPACTOS_2_ENEMIGOS_2026-09-29.md`

Runner/checkpoint:
- `experimentos/balance_nuevo/etapa9b_estratos_compactos_2enemigos.py`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 2 enemigos 14+14 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Resultado 200k:
- Piel base: 84.91% win / 40.97% HP / extensión95.90%.
- Piel base + Estratos: 87.30% / 45.01% / extensión91.80%.
- Corteza: 89.41% / 48.55% / extensión78.44%.
- Corteza + Estratos: 89.90% / 49.96% / extensión69.18%.

Efecto Estratos:
- sobre Piel base: +2.39 pp win / +4.03 pp HP.
- sobre Corteza: +0.49 pp win / +1.42 pp HP.

Replicación 4×50k:
- Piel base: +2.386 a +2.510 pp win.
- con Corteza: +0.374 a +0.722 pp win.

Hallazgo:
- retorno decreciente fuerte al combinar Corteza + Estratos;
- no existe DEF permanente adicional;
- usos Estrato ≈1.63 sin Corteza y ≈1.50 con Corteza;
- extensión baja al aumentar mitigación, reforzando autolimitación.

Estado:
- ESTRATO_REACTIVO_2 PASS para continuar;
- sigue LAB;
- NO PROVISIONAL todavía.

Siguiente única etapa:
- ETAPA 9C — Estratos contra 3 enemigos.


### ETAPA 9C — Estratos Compactos · 3 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA9C_ESTRATOS_COMPACTOS_3_ENEMIGOS_2026-09-29.md`

Runner/checkpoint:
- `experimentos/balance_nuevo/etapa9c_estratos_compactos_3enemigos.py`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 3 enemigos 10+9+9 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Resultado 200k:
- Piel base: 57.90% win / 19.50% HP / extensión99.42%.
- Piel base + Estratos: 62.43% / 22.73% / extensión98.82%.
- Corteza: 70.03% / 28.83% / extensión92.34%.
- Corteza + Estratos: 71.71% / 30.53% / extensión88.59%.

Efecto Estratos:
- sobre Piel base: +4.53 pp win / +3.24 pp HP.
- sobre Corteza: +1.68 pp win / +1.71 pp HP.

Usos medios Estrato:
- 3 enemigos: ~1.72 sin Corteza / ~1.74 con Corteza.
- no crecen proporcionalmente a los ataques porque nacen de transiciones de Arraigo.

Replicación 4×50k:
- Piel base: +4.056 a +4.624 pp win.
- con Corteza: +1.546 a +1.904 pp win.

Decisión:
- `ESTRATO_REACTIVO_2` pasa de LAB a **PROVISIONAL** para Estratos Compactos.
- no CANON.
- no runtime/HTML.

Regla PROVISIONAL:
- cuando Arraigo aumente a 2 o 3, gana/refresca 1 Estrato;
- máximo1;
- siguiente impacto directo conectado recibe +2 DEF sólo para ese impacto;
- consume Estrato;
- evasión no consume;
- salto 1->3 genera un solo Estrato;
- funciona con o sin Corteza.

Guardia:
- revalidar contra perfil enemigo autoritativo de LianQi III cuando exista.
- Cuerpo de Roca sigue PENDIENTE y no debe convertirse en otra capa permanente lineal de DEF.


### ETAPA 10A — Cuerpo de Roca · screen estructural 1v1 — CERRADA

Documento:
- `docs/experimentos/ETAPA10A_CUERPO_ROCA_SCREEN_1V1_2026-09-29.md`

Runner/checkpoint:
- `experimentos/balance_nuevo/etapa10a_cuerpo_roca_screen_1v1.py`

Problema:
- Tramo III no debe crear DEF7+ permanente;
- debe funcionar con o sin Corteza/Estratos;
- debe premiar Arraigo máximo sin impedir alcanzarlo.

Descartado:
- activar desde Arraigo>=2: interfiere demasiado con ON_HP_DAMAGE,
  generación de Arraigo y extensión.

Candidato principal LAB:
- `ROCA_GUARD_MAX_3`.
- requiere Piel activa y Arraigo==3.
- primer impacto directo conectado de cada turno del usuario: +3 DEF sólo para
  ese impacto.
- se consume para ese turno y se rearma al siguiente si Piel sigue activa y
  Arraigo sigue en3.
- evasión no consume.
- no aumenta DEF permanente/Tenacidad/duración/máximo Arraigo.

Screen +2/+3/+4:
- +3 seleccionado;
- +4 aporta casi nada adicional sobre la ruta Corteza+Estratos, especialmente
  frente a perfil común;
- +3 conserva más valor ante perfil pesado.

Replicaciones 4×40k de +3:
- Piel base, común: +1.00 a +1.11 pp win; +4.42 a +4.49 pp HP; ~1.22 usos.
- ruta Corteza+Estratos, común: +0.065 a +0.110 pp win; +0.43 a +0.49 pp HP;
  ~0.45 usos.
- Piel base, heavy 1d6+3: +1.77 a +2.13 pp win; +6.32 a +6.60 pp HP; ~1.47 usos.
- ruta completa, heavy: +0.318 a +0.338 pp win; +1.35 a +1.42 pp HP; ~0.80 usos.

Estado:
- candidato principal LAB;
- NO PROVISIONAL;
- no runtime/HTML.

Siguiente única etapa:
- ETAPA 10B — ROCA_GUARD_MAX_3 contra 2 enemigos.


### ETAPA 10B — Cuerpo de Roca · 2 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA10B_CUERPO_ROCA_2_ENEMIGOS_2026-09-29.md`

Runner/checkpoint:
- `experimentos/balance_nuevo/etapa10b_cuerpo_roca_2enemigos.py`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 2 enemigos 14+14 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Candidato:
- `ROCA_GUARD_MAX_3`.
- Piel activa + Arraigo3.
- al inicio de turno del usuario se arma 1 Guardia;
- primer impacto directo conectado del turno recibe +3 DEF;
- evasión no consume;
- alcanzar Arraigo3 durante acciones enemigas no arma retroactivamente.

Resultado 200k:
- Piel base: 84.91% win / 40.97% HP / extensión95.90%.
- Piel + Roca: 89.06% / 47.98% / extensión95.88%.
- Corteza + Estratos: 89.90% / 49.96% / extensión69.18%.
- Corteza + Estratos + Roca: 90.65% / 51.63% / extensión69.14%.

Efecto Roca:
- sobre Piel base: +4.15 pp win / +7.00 pp HP.
- sobre ruta Corteza+Estratos: +0.75 pp win / +1.66 pp HP.

Replicación 4×50k:
- Piel base: +4.114 a +4.238 pp win.
- ruta completa previa: +0.640 a +0.786 pp win.

Usos Guardia:
- ~2.15 por combate sobre Piel base.
- ~1.19 sobre Corteza+Estratos.

Hallazgo:
- casi no altera Arraigo máximo ni extensión;
- una Guardia por turno evita activación por enemigo;
- fuerte retorno decreciente al apilar con ramas previas.

Estado:
- PASS para continuar;
- sigue LAB;
- NO PROVISIONAL todavía.

Siguiente única etapa:
- ETAPA 10C — Cuerpo de Roca contra 3 enemigos.


### ETAPA 10C — Cuerpo de Roca · 3 enemigos — CERRADA

Documento:
- `docs/experimentos/ETAPA10C_CUERPO_ROCA_3_ENEMIGOS_2026-09-29.md`

Runner/checkpoint:
- `experimentos/balance_nuevo/etapa10c_cuerpo_roca_3enemigos.py`

Escenario:
- Tierra HP33 / Qi31 / DEF1 / EVA5;
- 3 enemigos 10+9+9 HP;
- PREC90 / EVA20 / DEF2 / ataque 2d4+1.

Resultado 200k:
- Piel base: 57.90% win / 19.50% HP / extensión99.42%.
- Piel + Roca: 66.35% / 25.67% / extensión99.43%.
- Corteza + Estratos: 71.71% / 30.53% / extensión88.59%.
- Corteza + Estratos + Roca: 73.87% / 32.89% / extensión88.52%.

Efecto Roca:
- sobre Piel base: +8.45 pp win / +6.18 pp HP.
- sobre ruta Corteza+Estratos: +2.16 pp win / +2.36 pp HP.

Replicación 4×50k:
- Piel base: +8.098 a +8.506 pp win.
- ruta completa previa: +2.088 a +2.562 pp win.

Usos Guardia:
- ~2.65 por combate sobre Piel base.
- ~1.87 sobre Corteza+Estratos.

Hallazgo:
- no escala linealmente con atacantes porque sólo puede armarse 1 Guardia por turno;
- Arraigo máximo y extensión permanecen prácticamente sin cambios;
- fuerte retorno decreciente al apilar con las ramas previas.

Decisión:
- `ROCA_GUARD_MAX_3` pasa de LAB a **PROVISIONAL** para Cuerpo de Roca.
- no CANON.
- no runtime/HTML.

Regla PROVISIONAL:
- Piel activa + Arraigo3;
- al inicio del turno del usuario, arma 1 Guardia;
- primer impacto directo conectado del turno: +3 DEF sólo para ese impacto;
- evasión no consume;
- alcanzar Arraigo3 durante acciones enemigas no arma retroactivamente.

Estado ruta fortificación:
- Piel base PROVISIONAL.
- Corteza Endurecida PROVISIONAL.
- Estratos Compactos PROVISIONAL.
- Cuerpo de Roca PROVISIONAL.

Guardia:
- revalidar Tramos I–III contra perfiles enemigos autoritativos LianQi II–IV cuando existan.


### ETAPA 11 — Respiración del Cuerpo-Horno completa — CERRADA

Documento:
- `docs/experimentos/ETAPA11_CUERPO_HORNO_COMPLETO_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa11_cuerpo_horno_completo.py`

Alcance:
- base;
- Tramos I–III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 y 3 enemigos;
- lattice de economía Qi.

Base:
- antiguo 15% descartado como magnitud principal;
- **25% HP Absorción / 2t / coste7 → PROVISIONAL**.
- no Calor base.

Repetición 4×25k, 25% vs 15%:
- COMMON: +1.71 a +2.02 pp win; +7.33 a +7.42 pp HP.
- 2 enemigos: +8.16 a +9.12 pp win; +5.93 a +6.71 pp HP.
- 3 enemigos: +5.59 a +7.02 pp win; +2.21 a +2.90 pp HP.

Barrera — PROVISIONAL:
- Cámara: +5 pp; base25 ->30%.
- Crisol: +5 pp; con Cámara +5 pp sinergia; BB=40%.
- Muro: +5 pp; BBB=45% /2t/7Qi.
- BBB promedio 4×25k: COMMON ~97.12%; 3 enemigos ~41.06%.

Conversión:
- problema antiguo: cap5% HP =1.5 con HP30; contra DEF2 el paquete temprano de Calor daba 0 daño efectivo.
- valores antiguos de Conversión reemplazados.

Conversión — PROVISIONAL recalibrada:
- Horno Latente T1: 40% absorbido -> Calor; cap10% HP.
- Corazón T2 solo: 50% / cap10%.
- Corazón con Horno: 60% / cap15%.
- Calor Acumulado T3 sin C previa: 50% / cap10%.
- con exactamente 1 C previa: 70% / cap15%.
- con 2 C previas: 80% / cap20%.
- CCC promedio 4×25k: COMMON ~96.67%; 3 enemigos ~49.59%.

Semántica LAB usada para Calor:
- recurso consumido por técnica ofensiva de Fuego posterior;
- comparte hit/miss de técnica portadora;
- no tirada propia;
- flags de DamagePacket siguen Motor §38.20.
- momento exacto de consumo frente a hit/miss sigue pendiente de cierre de Motor; no implementar desde la suposición LAB.

Eficiencia — PROVISIONAL con guardia:
- Respiración Mesurada 7->6 Qi.
- Circuito -10%; con Mesurada duración3.
- Horno Continuo -10%; ruta completa duración4 +5pp Absorción.
- bajo redondeo LAB EEE queda coste5 / duración4 / Absorción30%.
- Qi31 oculta parte del beneficio porque coste7/6/5 permiten 4 Palmas.
- umbrales donde cambia economía: Qi29/30/35/36/41/42/etc.
- revalidar obligatoriamente cuando se fije Qi máximo LianQi II–IV.

Screen 27/27:
- COMMON win ~95.86–97.23%.
- 2 enemigos ~68.76–80.05%.
- 3 enemigos ~30.03–50.18%.
- sin escalado ilimitado.
- Barrera = supervivencia bruta.
- Conversión = tempo ofensivo.
- Eficiencia = economía/duración dependiente de Qi.

Estado final:
- base PROVISIONAL.
- Barrera I–III PROVISIONAL.
- Conversión I–III PROVISIONAL recalibrada.
- Eficiencia I–III PROVISIONAL condicionada a Qi futuro.
- runtime/HTML SIN CAMBIOS.


### ETAPA 12 — Espejo de Luna completo — CERRADA

Documento:
- `docs/experimentos/ETAPA12_ESPEJO_LUNA_COMPLETO_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa12_espejo_luna_completo.py`

Alcance:
- base;
- Tramos I–III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 y 3 enemigos;
- economía Qi;
- Reflujo/reconstrucción;
- Arrastre con anti-lock correcto por objetivo.

Base:
- 12% descartado.
- **24% HP Absorción / Reflujo25% / duración3 / coste base7 / efectivo Agua6 → PROVISIONAL**.

Base24 vs12, repetición 4×25k:
- COMMON: +7.58 a +8.24 pp win; +11.94 a +12.51 pp HP.
- PRECISE: +9.88 a +10.30 pp win.
- HEAVY: +8.71 a +9.30 pp win.
- DANGEROUS: +11.19 a +11.86 pp win.
- 2 enemigos: +10.32 a +11.58 pp win.
- 3 enemigos: +2.30 a +2.60 pp win.

Base24 vs ofensiva pura:
- mejora 1v1;
- queda peor en 2/3 enemigos porque el pool puede romperse antes del siguiente TURN_START;
- se conserva como debilidad identitaria de barrera regenerativa.

Reserva — PROVISIONAL:
- T1 Marea Profunda: +5 pp =>29%.
- T2 Marea Alta: +5 pp; con Marea Profunda +3 pp sinergia => RR37%.
- T3 Mar Interior: +5 pp.
- RRR = 42% reserva / Reflujo25 / dur3 / coste6.
- RRR promedio 4×15k: COMMON92.62%; 2 enemigos59.60%; 3 enemigos12.38%.

Reflujo — PROVISIONAL:
- T1 Agua Renovada: Reflujo35%.
- T2 Corriente Retorno: +10 pp; con G1 reconstrucción40% una vez.
- T3 Marea Eterna: +10 pp con tope50%; reconstrucción40->50 si ya existe.
- GGG = reserva24 / Reflujo50 / reconstrucción50 una vez / dur3 / coste6.
- GGG promedio: COMMON91.76%; 2 enemigos49.92%; 3 enemigos8.19%.
- reconstrucción: ~24% common / ~88% 2en / ~99% 3en.
- no convierte Reflujo en defensa anti-burst; diferencia intencional frente a Reserva.

Eficiencia — PROVISIONAL recalibrada:
- problema: −10% aislado + raíz Agua seguía redondeando coste efectivo6 => nodo nulo.
- T1 Circulación Serena: nominal7->6; efectivo Agua5.
- T2 Flujo Ligero: **−15%**; standalone efectivo6->5; con T1 duración4.
- T3 Corriente Ininterrumpida: **−15%**; al expirar naturalmente con reserva +1 Qi explícito; funciona standalone.
- EEE = reserva24 / Reflujo25 / duración5 / coste efectivo4 / refund1.
- EEE promedio: COMMON90.65%; 2 enemigos39.72%; 3 enemigos4.72%.
- Qi31 no cruza nuevos umbrales de cantidad de ofensivas; revalidar obligatoriamente en Qi II–IV.

Screen 27/27, 8k/celda:
- COMMON win 89.74–92.84%.
- PRECISE 85.09–89.70%.
- HEAVY 84.43–89.31%.
- DANGEROUS 78.86–85.15%.
- 2 enemigos 40.33–59.28%.
- 3 enemigos 4.60–12.44%.
- ninguna ruta fuera de escala.

Estado:
- base PROVISIONAL.
- Reserva I–III PROVISIONAL.
- Reflujo I–III PROVISIONAL.
- Eficiencia I–III PROVISIONAL recalibrada y condicionada a Qi futuro.
- runtime/HTML SIN CAMBIOS.

Guardias:
- revalidar con perfiles enemigos II–IV autoritativos;
- revalidar economía al fijar Qi II–IV;
- TURN_START mantiene Reflujo antes de DOT;
- +1 Qi de Corriente Ininterrumpida es fuente explícita, no regen universal.


### ETAPA 13 — Paso de Nube Ligera completo — CERRADA

Documento:
- `docs/experimentos/ETAPA13_PASO_NUBE_COMPLETO_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa13_paso_nube_completo.py`

Alcance:
- base antigua vs nueva;
- Tramos I–III;
- 27/27 combinaciones mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 y 3 enemigos;
- CORRIENTE_CLARA;
- economía Qi/duración.

Base:
- antiguo +15 EVA /2t descartado.
- **+35 EVA /4t /coste7 → PROVISIONAL**.

Base nueva vs antigua, 4×25k:
- COMMON: +11.55 pp win promedio.
- PRECISE: +14.68 pp.
- HEAVY: +14.78 pp.
- DANGEROUS: +17.37 pp.
- 2 enemigos: +28.86 pp.
- 3 enemigos: +23.65 pp.

Base nueva vs ofensiva pura:
- COMMON +1.53 pp.
- PRECISE +0.12 pp.
- HEAVY +2.25 pp.
- DANGEROUS +0.77 pp.
- 2 enemigos +9.66 pp.
- 3 enemigos +13.22 pp.
- confirma identidad natural de Evasión multiimpacto sin dominar PREC100.

Evasión — PROVISIONAL:
- T1 Nube Velada +5 => Paso40.
- T2 Cuerpo de Nube +5 => con T1 Paso45.
- T3 Nube Inalcanzable +5 => VVV Paso50.
- con EVA base5 + raíz10: EVA total65.
- VVV promedio 4×15k:
  COMMON93.77 / PRECISE88.48 / HEAVY90.67 / DANGEROUS83.45 /
  2EN78.18 / 3EN51.38.
- no inmunidad: hit25% vs PREC90,35% vs PREC100.

Respuesta — PROVISIONAL recalibrada por conteo:
- primera evasión válida durante Paso crea CORRIENTE_CLARA una vez/activación.
- 1 nodo R: siguiente técnica pura Viento +5 Precisión.
- 2 nodos R: +10 Precisión.
- 3 nodos R: +15 Precisión +5 pp crítico.
- ataque básico no consume.
- trigger ~94–100% según perfil.
- RRR promedio:
  COMMON91.72 / PRECISE85.69 / HEAVY87.67 / DANGEROUS80.04 /
  2EN68.03 / 3EN34.72.

Eficiencia — PROVISIONAL recalibrada:
- T1 Respiración Ligera: coste7->6.
- T2 Circulación: -10%; con E previa +1 duración.
- T3 Aliento: -10%; con cualquier E previa +1 duración.
- EEE = coste5 / duración6 / +35 EVA.
- conserva techo histórico de coste: 6*.9*.9=4.86->5.
- EEE promedio:
  COMMON93.42 / PRECISE88.22 / HEAVY90.38 / DANGEROUS83.61 /
  2EN72.80 / 3EN41.88.
- contra DANGEROUS EEE queda ligeramente sobre VVV, por lo que VVV no domina todo.

Screen 27/27, 8k/celda:
- COMMON 90.31–93.45%.
- PRECISE 83.73–88.60%.
- HEAVY 86.61–91.34%.
- DANGEROUS 77.86–83.81%.
- 2 enemigos 65.35–78.30%.
- 3 enemigos 31.24–50.33%.
- ninguna ruta fuera de escala.

Estado:
- base PROVISIONAL.
- Evasión I–III PROVISIONAL.
- Respuesta I–III PROVISIONAL por conteo de nodos.
- Eficiencia I–III PROVISIONAL con nueva duración.
- runtime/HTML SIN CAMBIOS.

Guardias:
- revalidar Qi II–IV;
- revalidar perfiles enemigos II–IV;
- CORRIENTE una vez/activación;
- no movimiento/Velocidad/segunda esquiva.


### ETAPA 14 — Armadura de Plata completa — CERRADA

Documento:
- `docs/experimentos/ETAPA14_ARMADURA_PLATA_COMPLETA_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa14_armadura_plata_completa.py`

Alcance:
- base;
- Tramos I–III;
- 27/27 rutas mixables;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2 y 3 enemigos;
- consumo/no-consumo de Placas;
- stress LAB de Control para Adaptación.

Base — PROVISIONAL:
- coste7 / duración4.
- 3 Placas.
- +3 DEF por Placa contra impacto directo actual.
- Placas secuenciales; no suman DEF entre sí.
- impacto conectado consume1.
- evasión/DOT no consumen.

Base vs ofensiva pura, promedio 4×25k:
- COMMON +2.19 pp win.
- PRECISE +2.26.
- HEAVY +2.19.
- DANGEROUS +1.82.
- 2 enemigos −6.15.
- 3 enemigos −6.83.
Lectura: buena 1v1, débil a multiimpacto por consumo rápido; identidad válida.

Ramas se formalizan por cantidad de nodos para 27 rutas.

Resistencia — PROVISIONAL:
- 0R +3 DEF/Placa.
- 1R +4.
- 2R +6.
- 3R +8.
- RRR = 3 Placas +8 / dur4 / coste7.
- promedio 4×15k:
  COMMON97.76 / PRECISE96.08 / HEAVY96.63 / DANG93.96 /
  2EN70.26 / 3EN16.78.
- impacto conectado sigue consumiendo Placa aunque daño0, salvo Adaptación2+.

Cantidad — PROVISIONAL:
- 0Q 3 Placas.
- 1Q 4.
- 2Q 6.
- 3Q 8.
- QQQ = 8 Placas +3 / dur4 / coste7.
- promedio:
  COMMON94.81 / PRECISE92.24 / HEAVY90.94 / DANG87.39 /
  2EN76.36 / 3EN33.09.
- duración4 limita uso de cargas en 1v1.

Adaptación — PROVISIONAL:
- 1A: +5 Tenacidad tras romper Placa hasta próximo turno usuario.
- 2A: +10; si DEF deja impacto conectado en0, Placa no se consume.
- 3A: +15; conserva no-consumo; primer Control fallido/activación recupera 1 Placa rota, cap máximo inicial.
- chequeo daño0 es post-DEF y antes de Absorción externa.
- AAA daño puro promedio:
  COMMON93.59 / PRECISE90.02 / HEAVY88.89 / DANG83.99 /
  2EN57.01 / 3EN10.97.
- no se buffea por escenarios sin Control.

Stress Control LAB ilustrativo:
- Control efectivo65, intento tras impacto conectado.
- matemáticamente justo tras ruptura: A0 65%, A1 60, A2 55, A3 50.
- agregado 4×20k:
  A0 65.01% / A1 62.95 / A2 61.39 / A3 59.11.
- AAA recuperación ~96.98% en este stress deliberadamente cargado.
- NO perfil enemigo canónico.

Screen 27/27, 8k/celda:
- COMMON 93.19–98.55%.
- PRECISE 90.26–97.76%.
- HEAVY 88.48–97.14%.
- DANGEROUS 83.84–95.99%.
- 2 enemigos 56.94–83.20%.
- 3 enemigos 11.38–34.03%.
- sin escalado ilimitado.
- mezclas RRQ fuertes 1v1; RQQ/QRQ fuertes multiimpacto.

Estado:
- base PROVISIONAL.
- Resistencia I–III PROVISIONAL.
- Adaptación I–III PROVISIONAL.
- Cantidad I–III PROVISIONAL.
- runtime/HTML SIN CAMBIOS.

Guardias:
- revalidar II–IV contra perfiles autoritativos;
- Adaptación con enemigos reales de Control;
- multihit puede consumir varias Placas por impactos separados;
- no-consumo por daño0 depende de DEF, no Absorción;
- nunca sumar DEF de varias Placas.


### ETAPA 15A — Screen conjunto de defensivas BASE — CERRADA

Documento:
- `docs/experimentos/ETAPA15A_SCREEN_CONJUNTO_DEFENSIVAS_BASE_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa15a_screen_conjunto_defensivas_base.py`

Metodología:
- único runner para las cinco raíces;
- reglas CANON de raíz + ofensivas PROVISIONAL actuales;
- bases defensivas recalibradas actuales;
- Piel usa DEF_CAP2;
- 4 semillas × 10k por celda en la repetición principal;
- COMMON / PRECISE / HEAVY / DANGEROUS / 2EN / 3EN.

COMMON, defensa vs ofensiva propia:
- Fuego 95.85% vs95.66% => +0.19pp; HP +5.80pp.
- Metal 93.05 vs90.66 => +2.40pp; HP +9.75pp.
- Agua 88.76 vs86.79 => +1.96pp; HP +5.32pp.
- Tierra 95.72 vs91.66 => +4.06pp; HP +15.46pp.
- Viento 89.19 vs87.76 => +1.44pp; HP +7.20pp.

PRECISE delta win:
- Fuego +0.18pp.
- Metal +2.06.
- Agua +2.38.
- Tierra +5.46.
- Viento +0.17.

HEAVY:
- Fuego −0.05pp, HP +4.81pp.
- Metal +1.86.
- Agua +1.56.
- Tierra +5.01.
- Viento +1.64.

DANGEROUS:
- Fuego −0.58pp, HP +4.06pp.
- Metal +0.87.
- Agua +0.66.
- Tierra +6.69.
- Viento +1.41.

2EN delta win:
- Fuego −6.43pp.
- Metal −6.16.
- Agua −7.99.
- Tierra +23.55.
- Viento +9.97.

3EN delta win:
- Fuego −14.31pp.
- Metal −6.64.
- Agua −7.09.
- Tierra +40.66.
- Viento +13.26.

Lectura:
- no igualar win entre raíces;
- pools/cargas finitas pierden contra presión múltiple;
- Viento escala por oportunidades de evasión;
- Tierra sigue outlier multiimpacto.
- Piel queda PROVISIONAL + WATCH multiimpacto; no nerf automático desde stress unitarget.

Hallazgo de auditoría:
- Fuego/Metal/Agua/Viento tienen benchmark integral 27/27.
- Tierra NO está completa todavía.
- Cerrados Tierra: base + Fortificación (Corteza/Estratos/Cuerpo de Roca).
- PENDIENTES de benchmark integral:
  Estabilidad = Centro Firme / Raíz Profunda / Inamovible.
  Aguante = Tierra Persistente / Suelo que Sostiene / Montaña Persistente.

Estado:
- ETAPA15A PASS como screen conjunto BASE.
- no cambios numéricos.
- runtime/HTML SIN CAMBIOS.

Siguiente única etapa:
- ETAPA15B — Piel de Cobre completa: Estabilidad + Aguante + 27 rutas.
- luego screen conjunto final real de las cinco técnicas completas.


### ETAPA 15B — Piel de Cobre completa — CERRADA

Documento:
- `docs/experimentos/ETAPA15B_PIEL_COBRE_COMPLETA_2026-09-29.md`

Runner:
- `experimentos/balance_nuevo/etapa15b_piel_cobre_completa.py`

Alcance:
- base DEF_CAP2;
- Fortificación I–III;
- Estabilidad I–III;
- Aguante I–III;
- 27/27 combinaciones F/S/A;
- COMMON / PRECISE / HEAVY / DANGEROUS;
- 2/3 enemigos;
- stress LAB Control efectivo65;
- curación/duración.

Fortificación:
- no se reabre.
- Corteza / Estratos / Cuerpo de Roca permanecen PROVISIONAL.

Estabilidad — PROVISIONAL:
- Centro Firme: +5 Tenacidad por Arraigo en vez de +3.
- Raíz Profunda: +5 Tenacidad con2+; con Centro, primer fallo de Control/activación +1 duración restante.
- Inamovible: +5 Tenacidad con1+; primer Control resistido a Arraigo3 prepara siguiente Golpe +10 Precisión.
- SSS a Arraigo3: Piel aporta +25 Tenacidad; con raíz Tierra total actor30.
- Stress Control 4×12k:
  FFF P(Control) agregada ~53.64%;
  SSS ~37.43%;
  SSS win ~91.91% vs FFF ~88.72%;
  extensión Centro+Raíz ~92.1%;
  trigger Inamovible ~78.9%.

Aguante — PROVISIONAL recalibrado:
- problema detectado: sumar >1 turno base amplificaba demasiado DEF plana multiimpacto.
- nueva regla **AGUANTE_DUR_CAP1**: Aguante aporta máximo +1 turno a duración base.
- Tierra Persistente: +1 turno desde activación.
- Suelo que Sostiene: cura5% al primer Arraigo3; se elimina antigua sinergia de otro +1 turno.
- Montaña Persistente: +1 turno sólo si Aguante aún no lo dio; cura5% al Arraigo3 + otro5% una vez si HP<30%.
- AAA: base duration4; extensión propia de Arraigo3 puede llevar a5; curación teórica máxima15%/activación.

CAP1 vs duración antigua, 4×10k pareado:
- AA- 3EN: 81.91% -> 74.64% (-7.27pp); COMMON -0.94pp.
- AAA 3EN: 84.42% -> 77.16% (-7.25pp); COMMON -0.74pp.
- AAF 3EN: 89.61% -> 82.00% (-7.62pp); COMMON -0.65pp.
=> corrige exceso multiimpacto sin destruir duelo.

Rutas puras finales, promedio 4×15k:
- FFF COMMON96.44 / 2EN90.35 / 3EN73.80.
- SSS COMMON95.71 / 2EN84.77 / 3EN57.56.
- AAA COMMON98.61 / 2EN93.54 / 3EN77.36.
- AAF mixed: COMMON98.89 / 2EN95.31 / 3EN82.14.
- FAA mixed: 2EN~96.10 / 3EN~86.18; WATCH F+A.

Screen 27/27 final, 8k/celda:
- COMMON 95.71–99.11%.
- PRECISE 94.19–98.39%.
- HEAVY 92.43–98.01%.
- DANGEROUS 90.38–97.38%.
- 2EN 84.84–96.16%.
- 3EN 59.06–87.01%.

Estado:
- Piel BASE PROVISIONAL.
- Fortificación I–III PROVISIONAL.
- Estabilidad I–III PROVISIONAL.
- Aguante I–III PROVISIONAL recalibrado.
- 27/27 PASS.
- runtime/HTML SIN CAMBIOS.

WATCH:
1. Piel sigue outlier multiimpacto global.
2. mezclas Fortificación+Aguante son prioridad al existir perfiles enemigos II–IV.
3. Estabilidad debe revalidarse con enemigos reales de Control.

Siguiente bloque correcto:
- screen conjunto final real de las cinco defensivas completas.


### ETAPA 15C — Screen conjunto final de las cinco defensivas completas — CERRADA

Documento:
- docs/experimentos/ETAPA15C_SCREEN_FINAL_DEFENSIVAS_COMPLETAS_2026-09-29.md

Runner agregador:
- experimentos/balance_nuevo/etapa15c_screen_final_defensivas_completas.py

Metodología:
- no vuelve a simular todo en un único motor;
- agrega los benchmarks autoritativos ya cerrados de ETAPA11/12/13/14/15B;
- criterio = integridad estructural + nicho, no igualación de win rate;
- técnicas avanzadas siguen probadas contra perfiles LianQi I, por lo que no
  representan balance final II–IV.

Rangos 27/27 COMMON:
- Fuego 95.86–97.23%.
- Metal 93.19–98.55%.
- Agua 89.74–92.84%.
- Tierra 95.71–99.11%.
- Viento 90.31–93.45%.

Rangos 27/27 2EN:
- Fuego 68.76–80.05%.
- Metal 56.94–83.20%.
- Agua 40.33–59.28%.
- Tierra 84.84–96.16%.
- Viento 65.35–78.30%.

Rangos 27/27 3EN:
- Fuego 30.03–50.18%.
- Metal 11.38–34.03%.
- Agua 4.60–12.44%.
- Tierra 59.06–87.01%.
- Viento 31.24–50.33%.

Lectura global:
- no hay una defensiva globalmente equivalente por win rate y no se busca eso;
- Tierra sigue WATCH multiimpacto, sin nerf adicional;
- Agua queda WATCH burst múltiple, pero el set actual no incluye su perfil
  favorable de presión espaciada/Reflujo;
- Metal conserva dispersión legítima por Resistencia/Adaptación/Cantidad;
- Fuego conserva identidad de reserva finita + Conversión a tempo ofensivo;
- Viento conserva escalado natural por múltiples intentos, limitado por clamp,
  una sola CORRIENTE y ausencia de segunda esquiva.

Guardias globales:
- Fuego pool/cap Calor finitos y sin escalado recursivo.
- Metal Placas secuenciales, nunca sumadas.
- Agua Reflujo requiere pool vivo y reconstrucción una vez.
- Tierra DEF_CAP2 + Estrato max1 + Roca max1/turno + AGUANTE_DUR_CAP1 + curas once.
- Viento clamp hit + CORRIENTE once + sin Velocidad/movimiento.

Estado:
- 5/5 defensivas completas.
- 5/5 bases PROVISIONAL.
- 15/15 familias de progresión cerradas estructuralmente.
- 135/135 rutas conceptuales cubiertas (27×5).
- no cambios numéricos en ETAPA15C.
- runtime/HTML SIN CAMBIOS.

WATCH:
- Tierra multiimpacto y mezclas F+A.
- Agua burst simultáneo / falta presión espaciada.
- Metal Control real / multihit.
- Fuego consumo exacto de Calor hit/miss y Qi futuro.
- Viento Precisión enemiga II–IV y Qi futuro.

Siguiente única etapa:
- ETAPA16 — validación final de Qi31 para decidir LAB -> PROVISIONAL.


### ETAPA 16 — Validación final de Qi31 — CERRADA

Documento:
- docs/experimentos/ETAPA16_QI31_VALIDACION_FINAL_2026-09-29.md

Runner:
- experimentos/balance_nuevo/etapa16_qi31_validacion_final.py

Decisión:
- LianQi I Qi máximo = **31 PROVISIONAL**.
- pasa de LAB -> PROVISIONAL.
- no CANON.

Razón estructural:
- ofensivas base efectivas: 6 Qi.
- defensivas Fuego/Metal/Tierra/Viento: 7 Qi.
- defensiva Agua efectiva: 6 Qi.
- Qi30: ofensiva pura5; Agua def+4; resto def+3 => asimetría.
- Qi31: ofensiva pura5; Agua def+4; resto def+4 => primera frontera limpia.
- Qi32–35: misma cantidad de acciones que31; sólo residuo.
- Qi36: ofensiva pura6 / Agua def+5 / resto def+4 => reaparece acantilado.
- Qi37: restaura paridad pero sube presupuesto general a seis ofensivas.

Relaciones:
- 5*6 = 30.
- 7 + 4*6 = 31.
- 6 + 4*6 = 30.

Evidencia de promoción ya satisfecha:
- bases ofensivas cerradas;
- Arrastre/Peso cerrados PROVISIONAL;
- cinco defensivas completas;
- stress 2/3 enemigos;
- screen conjunto ETAPA15C;
- enemigo ordinario LianQi I usado como marco LAB.

Configs actualizadas:
- config_lianqi1_naked.py: PLAYER_BASE.qi_max = 31 PROVISIONAL.
- config_arc1_provisional.py: STAGES["LianQi_I"]["qi"] = 31.

No fija:
- Qi II/III/IV;
- regeneración pasiva;
- piso global de coste.

runtime/HTML SIN CAMBIOS.

Siguiente bloque sugerido:
- formalizar baseline desnudo LianQi I restante: HP30 / DEF1 / EVA5 y perfil enemigo ordinario completo.


### ETAPA 17 — Progresión personaje LianQi I–IV — CERRADA

Documento:
- docs/experimentos/ETAPA17_PROGRESION_PERSONAJE_LIANQI_I_IV_2026-09-29.md

Runner:
- experimentos/balance_nuevo/etapa17_progresion_lianqi_i_iv.py

Decisiones estructurales PROVISIONALES:

Stats iniciales:
- fijos, NO aleatorios;
- HP30;
- Qi31;
- Prec100 CANON;
- EVA5;
- DEF1;
- Control0;
- Tenacidad0;
- crit5% CANON;
- crit damage x1.50 CANON.
- raíz se aplica después del baseline.

Progresión:
- LianQi I Percepción: HP30 / Qi31 / 0 pts / BASE.
- LianQi II Circulación: HP36 / Qi37 / +2 pts / Tramo I.
- LianQi III Consolidación: HP42 / Qi43 / +2 pts / Tramo II.
- LianQi IV Refinamiento: HP48 / Qi49 / +2 pts / Tramo III.

Regla por avance:
- +6 HP.
- +6 Qi.
- +2 puntos de técnica.
- nuevo techo de Tramo.
- NO daño/DEF/Prec/EVA/crit/pen/control/tenacity automáticos.

Qi:
- 31/37/43/49 conserva paridad entre ofensiva6 y defensiva7/Agua6;
- base6 pura: 5/6/7/8 usos;
- def7 + base6: 1+4 /1+5 /1+6 /1+7;
- secuencias con AOE9 también ganan ~1 acción mixta por etapa;
- eficiencia puede cruzar umbrales adicionales como premio de build.

Puntos:
- 2 por avance II/III/IV;
- total6 a LianQi IV;
- 3 técnicas ×3 Tramos =9 slots posibles;
- obliga a elegir entre especializar y repartir;
- 1 nodo =1 punto;
- T2 requiere cualquier T1 previo en la misma técnica;
- T3 requiere cualquier T2;
- identidad de rama puede cambiar;
- puntos se pueden guardar.

Afectación de habilidades:
- NO stage_multiplier global.
- stage abre Tramos y puntos.
- más Qi permite más usos.
- efectos %HP/%Qi se recomputan naturalmente con nuevo máximo.
- valores planos siguen planos salvo rama/equipo/Concordancia/buff explícito.

Ejemplos HP30→36→42→48:
- Horno25%: 7.5→9→10.5→12.
- Horno45%: 13.5→16.2→18.9→21.6.
- Espejo24%: 7.2→8.64→10.08→11.52.
- Espejo42%: 12.6→15.12→17.64→20.16.
- curas Piel5%: 1.5→1.8→2.1→2.4.

Configs/docs sincronizados:
- config_lianqi1_naked.py baseline HP/EVA/DEF/Control/Tenacity.
- config_arc1_provisional.py STAGES HP/Qi/puntos/acceso.
- TECNICAS_ARCO1... economía de puntos.
- CONTRATO_COMBATE... progresión provisional.

Guardia:
- valores II–IV son PROVISIONALES estructurales;
- no afirmar balance final hasta crear perfiles enemigos II–IV.

Siguiente bloque:
- perfiles enemigos LianQi II/III/IV y revalidación por Tramo.


### ETAPA 17B — Reserva jugable de Qi — CERRADA

Documento:
- docs/experimentos/ETAPA17B_RESERVA_QI_JUGABLE_2026-09-29.md

Motivo:
- Qi31 era la frontera matemática mínima, pero demasiado austera como reserva
  jugable para combates duros y podía empujar a meditar demasiado seguido.

Decisión:
- LianQi I Qi37.
- LianQi II Qi43.
- LianQi III Qi49.
- LianQi IV Qi55.
- progresión continúa +6 Qi por etapa.
- HP permanece 30/36/42/48.
- puntos de técnica permanecen +2 por avance, total6.
- stats iniciales siguen fijos, no aleatorios.

Comparación LianQi I:
- Qi31: 5 ofensivas6 / def7+4 / 3 AOE9.
- Qi37: 6 ofensivas6 / def7+5 / 4 AOE9.
- Qi43: 7 ofensivas6 / def7+6 / 4 AOE9.
- se elige37: +1 técnica base (+20%) sin adelantar dos escalones de economía.

Interpretación ETAPA16:
- Qi31 = mínimo matemático limpio.
- Qi37 = baseline jugable elegido.

Curva vigente:
- 37 -> 43 -> 49 -> 55.

Economía:
- ofensivas6 puras: 6 / 7 / 8 / 9.
- def7 + ofensivas6: 1+5 / 1+6 / 1+7 / 1+8.
- Agua def6 mantiene igual total de acciones.
- AOE9 + ofensivas6: 5 / 6 / 7 / 8 acciones totales.
- def7 + AOE9 + ofensivas6: 5 / 6 / 7 / 8.

Guardia:
- no se introduce regen pasiva universal.
- la cadencia real de meditación sigue PENDIENTE y debe diseñarse aparte.
- ramas de Eficiencia y resultados dependientes de fallback Qi deben revalidarse
  bajo el nuevo baseline.

Archivos sincronizados:
- config_lianqi1_naked.py.
- config_arc1_provisional.py.
- etapa17_progresion_lianqi_i_iv.py.
- ETAPA17_PROGRESION_PERSONAJE_LIANQI_I_IV...
- CONTRATO_COMBATE_ESTADISTICAS_DOT...
- ETAPA16 marcada como frontera matemática, no baseline vigente.

runtime/HTML SIN CAMBIOS.


### ETAPA 17C — Potencia intrínseca de cultivo + equipo — CERRADA

Documento:
- docs/experimentos/ETAPA17C_POTENCIA_INTRINSECA_CULTIVO_EQUIPO_2026-09-29.md

Decisión PROVISIONAL:
- ascender de reino sí aumenta poder intrínseco ofensivo de forma moderada;
- el resto del crecimiento cuantitativo queda principalmente en equipo/build.

Golpe básico:
- LianQi I: 1d4+4, media6.5.
- LianQi II: 1d4+5, media7.5.
- LianQi III: 1d4+6, media8.5.
- LianQi IV: 1d4+7, media9.5.

Potencia de daño DIRECTO base de técnicas:
- I x1.00.
- II x1.08.
- III x1.16.
- IV x1.24.

Aplicación:
- magnitud base directa de técnica -> scalar cultivo -> planos -> % ofensivos -> crítico -> DEF/Absorción.
- una sola vez.
- no es stat ATQ.

Excluidos del scalar:
- Golpe básico (ya escala por dado).
- DOT.
- Reflect/Retaliation.
- Calor almacenado.
- Robo de Vida.
- curaciones.
- Absorción.
- DEF/EVA/Precisión/Control/Tenacidad.
- duración/cargas/recursos internos.
- daño secundario no_offensive_rescale.

%HP/%Qi:
- no doble escalar; ya crecen con el recurso máximo.

Papel del equipo:
- principal segunda capa de progresión cuantitativa;
- podrá aportar daño, DEF, precisión, evasión, crítico, penetración,
  Control/Tenacidad, HP/Qi y propiedades especiales;
- no usar equipo para reparar baseline roto.

Curva vigente:
- HP 30/36/42/48.
- Qi 37/43/49/55.
- básico 1d4+4/+5/+6/+7.
- tech directa x1.00/1.08/1.16/1.24.
- puntos 0/2/4/6.

Guardia:
- PROVISIONAL hasta validar contra enemigos LianQi II–IV.
- runtime/HTML SIN CAMBIOS.


### ETAPA 18 — Equipo Arco 1 LianQi I–IV — DISEÑO COMPLETO

Documento:
- docs/experimentos/ETAPA18_EQUIPO_ARCO1_DISENO_COMPLETO_2026-09-29.md

Catálogo:
- experimentos/balance_nuevo/equipment_arc1_catalog.json
- experimentos/balance_nuevo/equipment_arc1_catalog.py

Estado:
- PROVISIONAL / listo para benchmark; NO runtime.

Arquitectura:
- 13 slots: Arma, Tocado, Vestidura, Brazales, Fajín, Piernas, Calzado,
  Amuleto, Pulsera, 2 Anillos, 2 Tesoros.
- no bloqueo artificial de slots de tesoro.
- no full-set bonus, rareza MMO, refuerzo +1/+10 ni durabilidad.

Catálogo:
- 58 piezas.
- LI 12.
- LII 18.
- LIII 16.
- LIV 12.
- 11 armas / 6 tocados / 6 vestiduras / 5 brazales / 4 fajines /
  4 piernas / 5 calzados / 5 amuletos / 4 pulseras / 7 anillos /
  1 Tesoro Espiritual.

Fuentes:
- dotación inicial / origen;
- exploración única;
- piedras en mercado/Sauces;
- Lu Cheng (armas/metal);
- Ning Cai (textil/cuero/accesorios);
- Jiang Rui (patrulla);
- Chen Bo/Lan Meihua (médico);
- Wen Tao/He Zhen (formaciones);
- Song Rui (archivo);
- Qiao Ren (institucional);
- Duan Shibo (logística);
- Ji Xueying (Núcleo);
- canjes desbloqueados por misión.

Economía:
- M02–M07 mantiene CANON contribución total12.
- propuesta LIII para equipo: M08 4 / M09 2 / M10 3 / M11 3 / M12 6 =18.
- propuesta LIV: M13 4 / M14 3 / M15 1 / M16 6 / M17 5 / M18 0 =19.
- valores LIII/LIV NO se sincronizan todavía a misiones: primero simular economía.
- 10 requisiciones definidas; objetivo 5–8 activas por partida, 1–3 contribución c/u.
- Mérito no se gasta.
- piedras y Contribución siguen economías separadas.

Dotación garantizada propuesta:
- P: espada madera + uniforme.
- M03: fajín discípulo externo.
- M11: fajín Dos Alas.
- M17: fajín Núcleo Profundo.
- M18: NO loot/equipo legendario.

Balance:
- power budget por pieza diagnóstico:
  LI<=1.5, LII<=2.5, LIII<=3.5, LIV<=4.0.
- DEF de equipo deliberadamente limitada; máximo teórico catálogo +1.
- no gear Qi cost % en Arc1 para no pisar ramas de Eficiencia.
- piezas no root-locked.
- builds soportadas: precisión, agresión/crítico, penetración, evasión,
  HP/Tenacidad, Control, Qi/continuidad, balanceada.

Tesoros:
- Espejo de Pulso Velado solamente.
- 2 slots arquitectónicos, 1 tesoro obtenible en Arc1.
- segundo slot vacío por diseño.

Simulación preparada:
- MANDATORY_ENTRY.
- EXPECTED_STAGE.
- HIGH_ROLL_STRESS.
- loader/validator permite aggregate_stats, effects, tags y export CSV.

Validación catálogo:
- 62 IDs únicos;
- cero overflow perfiles;
- cero pieza sobre ceiling;
- fuentes/precios obligatorios completos.

Guardias:
- balancear monstruos contra MANDATORY_ENTRY, revisar EXPECTED, HIGH_ROLL sólo stress.
- equipo no repara baseline roto; amplifica/especializa.
- Uniforme Discípulo Interno sigue Arc2.
- Lu Cheng/Ning Cai servicios, no profesiones.
- recuperación/meditación pendiente afecta valor de +Qi y Anillo Herrumbroso.

Siguiente etapa:
- ETAPA18B — benchmark equipo por etapa/arquetipo en Colab/Monte Carlo.


### ETAPA18 — CORRECCIÓN TESORO ÚNICO + DAÑO DE TÉCNICAS

Decisión:
- 2 slots arquitectónicos de Tesoro Espiritual;
- sólo **1 tesoro obtenible en Arc1**;
- segundo slot vacío todo Arc1;
- tesoros deben ser poderosos/raros/difíciles, no accesorios normales.

Único Arc1:
- Espejo de Pulso Velado;
- LianQi III+, oculto Primera Ala / M12;
- no compra/canje/recompensa automática;
- +5 EVA;
- +3 Tenacidad;
- 1/combat al caer primero a <=35% HP -> Absorción20% HPmax.
- no necesario para balance ni progreso principal.

Catálogo:
- 58 piezas total.
- LI12 / LII18 / LIII16 / LIV12.
- TESORO_ESPIRITUAL=1.

Ofensiva de equipo:
- stat renombrado `technique_direct_damage_percent`.
- sólo escala daño directo compatible de TÉCNICAS.
- no básico, DOT, Reflect, Retaliation, Calor, curación, Absorción ni secondary no_offensive_rescale.
- piezas actuales: Amuleto Colmillo +3%, Sable Anillo Gris +2%, Hoja Seis Corrientes +3%, Anillo Relevo +3%.
- máximo teórico LIV especializado ~+9% (arma + amuleto + anillo), no baseline.


### ETAPA18A — AMPLIACIÓN, PRÓLOGO Y DESCRIPCIONES — CERRADA

Documento:
- docs/experimentos/ETAPA18A_AMPLIACION_CATALOGO_PROLOGO_DESCRIPCIONES_2026-09-29.md

Catálogo vigente:
- 68 piezas.
- LI14 / LII21 / LIII19 / LIV14.
- 1 único Tesoro Espiritual Arc1.
- 68/68 tienen description examinable.
- cero placeholders.

Confirmación ver74:
- ITEMS usaba campo desc para descripciones examinables.
- nuevaPartida legacy arrancaba con pocion + uniforme + espada_madera.
- callejero añadía cuchillo_hueso.
- contrato 3C6 ya quitó auto-entrega de uniforme/espada en creación y trasladó
  la entrega al descansillo, one-shot equipoInicialEntregado.

Prólogo nuevo:
- antes de descansillo: ningún equipo de secta.
- descansillo, una sola vez:
  1) uniforme_gris_aspirante (HP+2, auto-equip);
  2) espada_madera_entrenamiento.
- campesino/escolar: espada auto-equip.
- callejero: conserva cuchillo_hueso_callejero, recibe también espada y puede
  elegir arma activa; conserva ambas.
- consumibles fuera de este pase: no modificar pociones aquí.

Reemplazo legacy:
- todo EQUIPO nuevo reemplaza equipo legacy; coexistencia prohibida.
- mapa previsto:
  espada_madera -> espada_madera_entrenamiento
  uniforme -> uniforme_gris_aspirante
  cuchillo_hueso -> cuchillo_hueso_callejero
  anillo_herrumbroso -> anillo_hierro_oxidado
  espada_hierro -> espada_hierro_equilibrada
  tunica_reforzada -> tunica_reforzada_trama_cobre
  bandana -> bandana_cuero_reforzada
  sandalias_viento -> sandalias_corriente_ligera
  amuleto_colmillo -> amuleto_colmillo_montado
- runtime/migración todavía DEFER.

10 piezas agregadas:
- LI: Cinta patio aspirante; Anillo cobre sin sello.
- LII: Pulsera tensión meridiana; Calzas guardia externa; Anillo reserva menor.
- LIII: Fajín respiración larga; Brazales aguja plata; Amuleto flujo contenido.
- LIV: Vestidura Ala Cerrada; Pulsera meridiano profundo.

Daño directo de técnicas por equipo:
- stat explícito technique_direct_damage_percent.
- máximo teórico por slots:
  LI0 / LII5 / LIII7 / LIV11%.
- no afecta básico, DOT, secondary no_offensive_rescale, Calor, curación ni Absorción.

Diferido por decisión:
- auditoría integral de adquisiciones;
- reconciliación final de precios/fuentes;
- registro/Monte Carlo masivo en Colab;
- runtime.

Validador actualizado:
- description obligatoria;
- legacy ID no reutilizable;
- exactamente1 tesoro;
- IDs de prólogo deben existir;
- export CSV incluye description.


### ETAPA18A — CORRECCIÓN STATS PLANOS ENTEROS

Regla:
- todo stat plano de equipo debe ser entero;
- porcentajes/pp sólo mediante campos explícitos;
- prohibida DEF fraccionaria.

Correcciones:
- uniforme aspirante: HP+2, DEF0.
- sobretúnica patrulla: HP+3, Ten+2.
- brazales cuero cruzado: HP+2, Ten+2.
- túnica reforzada trama cobre: DEF+1, HP+2.
- manto mantenimiento: DEF+1, Ten+3, Qi+2.
- brazales relevo: HP+4, Ten+3.
- vestidura Ala Cerrada: HP+5, Ten+4.

DEF equipo máxima:
- LI0 / LII0 / LIII+1 / LIV+1.
