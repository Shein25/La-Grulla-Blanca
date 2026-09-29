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

