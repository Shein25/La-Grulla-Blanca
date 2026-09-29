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
