# Parallel Arc 1 balance work

This package exists so work can continue while the Rata T1 Kaggle run is executing.

## Blocks

1. `mono_qi_drain_ablation.py`
   - paired A/B test with common random numbers;
   - A = candidate's real QI_DRAIN;
   - B = identical candidate with qi_drain=0;
   - isolates the causal contribution of Manotazo al Dantian.

2. `directed_t0_revalidation.py`
   - revalidates the five high-precision candidates already found for:
     Avispa de Jade, Serpiente de Qi and Lobo Espiritual;
   - no new broad Optuna search;
   - common random numbers and root/loadout breakdown.

3. `monster_extrapolation_matrix.json`
   - transfers methodology and search priors to the remaining 13 Arc 1 monsters;
   - never transfers final numbers.

4. `RATA_T2_T4_STRUCTURAL_AUDIT.md`
   - prepares dependencies/telemetry only;
   - T2-T4 execution remains blocked until T1 is human-selected and closed.

## Shared guards

- no main;
- no merge;
- no automatic CANON promotion;
- no target win-rate objective;
- no Definitives;
- no old monster numeric baselines;
- all heavy simulations are intended for Kaggle/Colab, not CI.
