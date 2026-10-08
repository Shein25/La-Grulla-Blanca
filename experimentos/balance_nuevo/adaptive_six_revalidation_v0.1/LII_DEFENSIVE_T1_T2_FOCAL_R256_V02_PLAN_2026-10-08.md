# LII Defensive T1/T2 Focal R256 V02 — Gate

Fecha: 2026-10-08.
Estado: **PLAN DE VERIFICACIÓN / NO_AUTO_FREEZE**.

Autoridad de partida: `LII_DEFENSIVE_T1_T2_CAUSAL_SCREEN_V01_AUDIT_2026-10-08.md`.
Source exacto: `9a6baa41bd6fc505a755a474cd4f64a2522ba0b9`. 
Base runner V01 SHA: `fc14ff185419d694160121ad9684539bfd324ea171fda8fe8ef8261566510fa9`.
Focal runner SHA: `f92ba535b606ef5063f57839b4dece6962a53b6f8bc3ddcbe66d9be1a452f6f5`.

## Matriz confirmatoria
- 11 estratos root/gear/monstruo/tier (Fuego 4; Tierra 2; Viento 2; Metal 1; Agua 2).
- Siete builds por estrato: BASE_0, OFF_T1_0, OFF_T1_1, DEF_T1_0, DEF_T1_1, DEF_T1_2, OFF_1_DEF_0.
- Cuatro políticas OFFENSE_ONLY/DEFENSE_OPEN/DEFENSE_DUE/DEFENSE_GUARD.
- R256, semillas distintas de V01 y compartidas entre todas las builds/políticas de un mismo estrato.
- Total 11 × 7 × 4 × 256 = **78.848 combates**.
- 2 workers, 11 checkpoints, widget persistente, Source Lock/manifest/hashes.

## Gates
1. Revalidar contratos freeze T0/T1/T2 y 10 pruebas de eventos.
2. Compilar y verificar coste base y Tramo I de las cinco defensivas, registrar breakpoint de Qi de Agua.
3. Reexaminar consecuencias negativas de política en R256 sin categorizar automáticamente una mala apertura como bug.
4. Contrastes pareados por política y variantes Tramo I; no atribuir independencia artificial a builds que comparten RNG.
5. Exportar semillas individuales, CI95 y casos materialmente negativos. Humano decide si hace falta cambio o sólo educar al jugador para timing.
6. Ningún cambio de monstruo, raí­ces, equipo, habilidades, ni restricciones de progresión.

## No confundirse con cierre global
Este gate focal NO valida mutantes, adquisiciones multielementales ni Concordancias nuevas. Esas pruebas vienen después, leyendo primero el contrato real `MUTANT_SUFFIX_CONTRACT_V1`; no inventar mutantes. Sin runtime/HTML; Astra integra luego.