# LI Monster T1 Survival Lab — V01

## Base
T0 LI está congelado en esta rama desde commit `f53edd00dd894cb3534df0b8544543dc074f6acb`.

Review exhaustivo T0:
`77337e8ee77dfcd53ca1e679998d158cf5d2f8de8b6f744fc5e4c426bb3bf542`

## T1
Se calibra una sola habilidad de supervivencia por especie para las cinco raíces:

- rata_qi — Reflejo de Madriguera — EVADE_NEXT
- serpiente_qi — Muda del Cauce — EVADE_NEXT
- avispa_jade — Quiebro de Jade — EVADE_NEXT
- mono_pildoras — Salto del Ladrón — EVADE_NEXT
- lobo_espiritual — Paso de la Cola Vigilante — DEFENSE_UP

Sólo varían magnitud y cooldown. Los triggers quedan fijos:
- low HP: 30%;
- heavy hit: 20% max HP.

La habilidad defensiva consume el turno del monstruo.

## Campaña Kaggle preparada
- paquete: `KAGGLE_LI_MONSTER_T1_SURVIVAL_GENERAL_V01.zip`
- package SHA-256: `bfd6c7e0b0d516fbbe2631d88d8519ad79929a96c65a052169e908855e25dd8d`
- notebook SHA-256: `42b053687829aa39a6b1c6044a63a2c627e93e938a580e0fb5204968d6a7e9c2`
- runner SHA-256: `187ea823a8ad9424f193340c5478e840143e1ee8cc77a90cb3cd312f2eb09e8d`
- technique catalog SHA-256: `912b7824eff9149909ca21b9ad6290c6c82b1e1ea31867da1185c32df383d187`
- CRN epoch: `13b6c488bfd3cf516b76cdea1ff22a38f981dbe5f565d6fa435378ee720050c8`

## Authority
Adaptive branch head after ceiling correction:
`6fc4b376c723954f835572f82660b79478c1e2ca`

Ceiling:
- LI → T1
- LII → T2
- LIII → T2
- LIV → T3/T4 mediante presión nueva.

T2–T4 permanecen numéricamente bloqueados hasta cerrar secuencialmente T1.

## Gate
`T1_GENERAL_SEARCH_READY_FOR_KAGGLE`
