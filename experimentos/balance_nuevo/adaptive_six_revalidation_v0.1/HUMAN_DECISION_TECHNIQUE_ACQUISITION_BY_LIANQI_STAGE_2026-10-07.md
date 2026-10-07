# Decisión humana — adquisición de tipos de técnica por etapa LianQi

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN_DECISION / AUTORIDAD DE BALANCE PARA LAB

## Regla aprobada

La progresión de técnicas base por etapa queda separada por tipo:

### LianQi I
- acceso a técnicas **unitarget base**;
- puede aprender técnicas unitarget de elementos ajenos según adquisición;
- **sin técnicas defensivas**;
- **sin AOE**;
- **0 Tramos**.

### LianQi II
- conserva las unitarget;
- aparecen las **técnicas defensivas**;
- se desbloquea **Tramo I**;
- economía vigente: +2 puntos de técnica;
- AOE todavía no disponible.

### LianQi III
- conserva unitarget + defensivas;
- aparecen las **técnicas AOE**;
- se desbloquea **Tramo II**;
- economía acumulada vigente: 4 puntos de técnica.

### LianQi IV
- están disponibles unitarget + defensivas + AOE;
- se desbloquea **Tramo III**;
- economía acumulada vigente: 6 puntos de técnica;
- el jugador puede presentar builds maduras con todos los Tramos desbloqueados por etapa, aunque no necesariamente asignados todos simultáneamente.

## Relación con tiers adaptativos T0–T4

Los tiers adaptativos del monstruo NO equivalen a la etapa LianQi del jugador.

- LI nativo: T0–T1 esperado; T2 puede aparecer temporalmente por presión.
- LII: T1–T2 es la banda estructural esperada.
- T3/T4 deben validarse también contra jugadores avanzados que regresan con mejor equipo y acceso a Tramos superiores.
- En gates T3/T4 se deben incluir explícitamente escenarios de jugador avanzado, incluyendo LIII/LIV y, para el stress maduro, builds LIV con Tramo III desbloqueado y equipo EXPECTED/HIGH_ROLL_STRESS.
- No balancear T3/T4 suponiendo que el jugador conserva restricciones de LI/LII.

## Consecuencia para Concordancias

El conjunto receptor crece por etapa:

- LI: sólo hooks BASE de las 5 unitarget.
- LII: se agregan hooks BASE de las 5 defensivas y hooks condicionales que existan realmente por Tramo I según la asignación legal.
- LIII: se agregan las 5 AOE y Tramo II.
- LIV: Tramo III y builds maduras.

Cada etapa requiere su propia regresión de Concordancias, sin recalibrar automáticamente la magnitud fundacional de LI.

## Corrección del gate LI

El plan V01 que usaba las 15 técnicas como envolvente mecánica queda SUPERADO para el benchmark de etapa real.

LI real debe censar únicamente:
- Palma Ardiente;
- Destello de Plata;
- Latigazo de Marea;
- Golpe de Montaña;
- Lanza que Parte Nubes.

Esto produce 20 pares ordenados entre elementos distintos.

Según el mapeo BASE actual:
- 16 pares tienen receptor compatible;
- 4 pares son controles negativos BASE NONE.

No main. No merge. No runtime. No auto-freeze.
