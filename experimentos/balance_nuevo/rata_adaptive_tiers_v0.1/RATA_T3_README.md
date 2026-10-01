# Rata T3 — Species Counter LAB

T0, T1 and T2 are closed.

Frozen chain:

```text
T0: Rata trial 4254
T1: Reflejo de Madriguera +40 EVA / CD5 / REACTIVO_1 / BASE
T2: R2_SHORT — memory 2 / repeat 2 / EFECTIVA / +8
```

T3 is now open for calibration.

The first hypothesis is deliberately narrow:

```text
player repeats an observable pattern
→ T2 recognizes it
→ T1 Reflejo is chosen
→ player attacks into that prediction
→ Reflejo causes a miss
→ T3 may retaliate physically
```

The retaliation uses the canonical Rata basic `2d4` as the initial reference.
This first phase compares **trigger semantics**, not damage scaling.

Candidates:

- `RECOGNIZED_REFLEJO_MISS`: recognition was active and Reflejo caused a miss;
- `CONFIRMED_PATTERN_REFLEJO_MISS`: additionally, the player's actual action
  matched the category T2 predicted;
- `CONFIRMED_PATTERN_ONCE_PER_FIGHT`: same as above but at most once per fight.

This structure preserves counterplay: if the player intentionally breaks the
learned pattern, the confirmed-pattern branches should not retaliate.

No root/build inspection. No QI drain, DOT or Control is introduced. T4 remains
blocked.
