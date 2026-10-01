# Auditoría — Migración de estadísticas de los 18 monstruos al motor nuevo v0.2

**Fecha:** 2026-09-30  
**Estado:** GUARDIA ACTIVA / MIGRACIÓN PENDIENTE  
**Rama:** `experiment/combat-stat-contract-v0.1`  
**HEAD de autoridad previo a esta migración:** `b218bd60d4983091a9a327164c047bbb5ca8628c`

## Hallazgo

El archivo `experimentos/balance_nuevo/monster_arc1_new_contract_lab.json` no puede seguir tratándose como fuente numérica válida de balance.

Aunque separa `legacy` de `new_contract_lab`, conserva contaminación de ver74:

- HP, daño básico y magnitudes/cadencias de técnicas parten de la ficha legacy;
- Precisión se calculó como `60 + 5*legacy_attack`;
- Evasión se calculó como `5*legacy_defense - 10`;
- DEF plana y Tenacidad fueron hipótesis LAB añadidas alrededor de esa traducción.

Esto contradice la Regla cero de `experimentos/balance_nuevo/README.md`: **no importar estadísticas numéricas de ver74**.

## Decisión

A partir de esta auditoría:

```text
ver74 / MOBS snapshot
        ↓
IDENTIDAD / NOMBRES / ROL / REGIÓN / ELEMENTO / FAMILIA MECÁNICA
        ✓ se pueden preservar

CUALQUIER MAGNITUD NUMÉRICA LEGACY
        ↓
        ✗ NO se convierte
        ✗ NO se hereda
        ✗ NO se usa como baseline

monster_arc1_new_engine_registry_v0_2.json
        ↓
T0 calibrado integralmente en unidades del motor nuevo
        ↓
T1–T4 adaptativos
```

El registro v0.2 usa `null` deliberadamente para estadísticas aún no recalibradas. Una simulación debe **fallar** si intenta usar un perfil pendiente; no debe rellenarlo desde legacy.

## Semántica obligatoria del motor nuevo

- Impacto: `clamp(Precisión efectiva - Evasión objetivo, 5, 100)`.
- DEF: reducción plana universal de daño directo, una vez por impacto.
- DOT: ignora DEF, pero no Absorción.
- Control: `clamp(base_control + Control + buffs - debuffs - Tenacidad, 5, 100)`.
- Crítico base: 5%, x1.50 salvo override explícito del motor nuevo.
- Orden directo: Precisión/Evasión → daño → crítico → DEF/Penetración → Absorción → Vida.

`attack/ataque` legacy **no es Precisión**.  
`defense/defensa` legacy **no es DEF plana**.  
No existe fórmula autorizada para convertir uno en otro.

## Auditoría de los 18 perfiles actualmente traducidos

Los números de esta tabla se muestran **sólo para identificar qué estaba entrando al laboratorio**. Ninguno queda aprobado por esta auditoría.

| Monstruo | Etapa | Rol | HP viejo/anclado | PREC traducida | EVA traducida | DEF LAB | TEN LAB | Daño viejo/anclado | Veredicto |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| rata_qi | LianQi_I | NORMAL | 9 | 65 | 40 | 0 | 20 | 1d4 | REBALANCE REQUIRED |
| serpiente_qi | LianQi_I | NORMAL | 13 | 70 | 45 | 0 | 20 | 1d4+1 | REBALANCE REQUIRED |
| lobo_espiritual | LianQi_I | APEX_BRIDGE | 18 | 75 | 45 | 1 | 25 | 1d6+1 | REBALANCE REQUIRED |
| eco_caido | LianQi_II | ELITE | 34 | 80 | 50 | 1 | 27 | 1d8+2 | REBALANCE REQUIRED |
| pez_lunar | LianQi_III | NORMAL | 26 | 75 | 50 | 1 | 24 | 1d6+2 | REBALANCE REQUIRED |
| sombra_ahogada | LianQi_III | ELITE | 42 | 80 | 55 | 1 | 29 | 2d6 | REBALANCE REQUIRED |
| centinela_pluma | LianQi_IV | BOSS | 48 | 85 | 60 | 4 | 36 | 2d6+2 | REBALANCE REQUIRED |
| devorador_niebla | LianQi_IV | NORMAL | 38 | 80 | 55 | 2 | 26 | 2d6 | REBALANCE REQUIRED |
| avispa_jade | LianQi_I | NORMAL | 10 | 70 | 45 | 0 | 20 | 1d4 | REBALANCE REQUIRED |
| mono_pildoras | LianQi_I | SKIRMISHER | 17 | 75 | 45 | 0 | 20 | 1d6 | REBALANCE REQUIRED |
| sapo_ceniza | LianQi_II | NORMAL | 18 | 70 | 50 | 1 | 22 | 1d6+1 | REBALANCE REQUIRED |
| sapo_caldera | LianQi_II | BOSS | 34 | 80 | 55 | 2 | 32 | 2d6 | REBALANCE REQUIRED |
| escarabajo_hierro | LianQi_II | TANK | 21 | 70 | 65 | 3 | 27 | 1d6+1 | REBALANCE REQUIRED |
| rey_escarabajo | LianQi_II | BOSS | 38 | 80 | 70 | 4 | 32 | 2d6 | REBALANCE REQUIRED |
| anguila_estelar | LianQi_III | SKIRMISHER | 30 | 80 | 55 | 1 | 24 | 1d8+2 | REBALANCE REQUIRED |
| guardian_coral | LianQi_III | BOSS | 52 | 85 | 65 | 3 | 34 | 2d6+1 | REBALANCE REQUIRED |
| halcon_tormenta | LianQi_IV | SKIRMISHER | 31 | 85 | 60 | 1 | 26 | 2d6 | REBALANCE REQUIRED |
| mantis_nube | LianQi_IV | BOSS | 46 | 90 | 65 | 3 | 36 | 2d6+2 | REBALANCE REQUIRED |

**Resultado: 18/18 requieren perfil T0 nuevo.**

Esto no significa que todos sus valores deban necesariamente cambiar. Significa que, si un valor coincide finalmente con el anterior, deberá ser porque el benchmark del motor nuevo lo justificó, no porque fue heredado o convertido.

## Qué sí se conserva

Por monstruo pueden conservarse como identidad de contenido:

- ID y nombre;
- etapa nativa;
- rol ecológico;
- región;
- elemento;
- condición de único;
- nombre de técnica;
- familia mecánica cualitativa: daño directo, Veneno, Quemadura, drenaje de Qi, etc.;
- perfiles de IA/adaptación ya seleccionados, sujetos a integración.

Los **números** de esas técnicas se recalibran: daño, precisión propia, cadencia, DOT, duración, drenaje y cualquier otro parámetro cuantitativo.

## Relación con Adaptive Ecology

La adaptación no puede corregir un T0 contaminado.

Regla obligatoria:

```text
NEW_ENGINE_T0
→ profile completo y validado
→ adaptive C_STAGGERED / abilities T1–T4
→ effectiveKit
→ Monster Combat AI
→ resolver del motor nuevo
```

Nunca:

```text
ver74 stats
→ fórmula de traducción
→ T1–T4
```

Los multiplicadores/bonos adaptativos existentes también deberán revalidarse una vez cerrado el nuevo T0. La estructura del modelo C puede mantenerse; sus cifras no se usan para justificar T0.

## Efecto sobre experimentos anteriores

Todo resultado que dependa de `monster_arc1_new_contract_lab.json` conserva valor como:

- diagnóstico de arquitectura;
- sensibilidad;
- prueba de pipeline;
- evidencia de que el perfil legacy traducido estaba desescalado/desalineado.

No puede elevarse a **balance CANON/PROVISIONAL de monstruos**.

En particular, los laboratorios Stage I v0.1/v0.2/v0.3 que consumieron ese contrato deben tratarse como **PRE-MIGRATION / DIAGNOSTIC ONLY**. Sus hallazgos metodológicos siguen siendo útiles; sus números no congelan stats.

## Próximo orden correcto

1. Construir T0 integral de los cinco monstruos LianQi I con el registro v0.2.
2. Simular cuerpo + ataque físico + técnicas + estados + IA natural contra el jugador completo.
3. Congelar perfiles T0 nuevos.
4. Repetir por bandas LianQi II, III y IV.
5. Sólo entonces recalibrar T1–T4, incluida la evolución de daños/skills.
6. Mantener Definitivas fuera de todo balance de monstruos.

## Invariante de aceptación

Un perfil de monstruo sólo puede entrar a un benchmark de balance si:

```text
stats_status != PENDING
numeric_source == NEW_ENGINE_ONLY
legacy_numeric_values_allowed == false
legacy_formula_translation_allowed == false
```

Si no cumple, el runner debe abortar.
