# Rata de Qi — arsenal adaptativo v0.2

**Estado:** IDENTIDAD APROBADA PARA LAB / NÚMEROS PENDIENTES

## T0

La Rata de Qi parte de su perfil T0 del motor nuevo. No hereda daño, HP, precisión, evasión ni defensa de ninguna ficha anterior.

Su T0 no recibe una técnica nueva por compatibilidad. Si el balance integral demuestra que su ataque físico natural basta, permanece sin técnica T0.

## T1

`Reflejo de Madriguera` conserva la identidad de una respuesta evasiva instintiva.

```text
kind = EVADE_NEXT
paramsStatus = PENDING_T0_T4_REBALANCE
```

No existe un bono de Evasión autorizado todavía.

## T2

Reconocimiento persistente y anticipación elegible. La habilidad activa concreta sigue pendiente.

## T3

Counter específico de especie. La habilidad activa concreta sigue pendiente.

## T4

`Mordisco Frenético` conserva esta identidad:

- ofensiva física;
- instintiva;
- basada en el ataque básico T0 nuevo;
- multimpacto como familia mecánica candidata.

Parámetros pendientes:

- número de impactos;
- escalar por impacto;
- precisión;
- cooldown;
- interacción final con crítico;
- cualquier otro modificador de daño.

No se conserva ningún valor numérico previo.

## Regla

```text
Rata T0 READY
→ calibrar T1
→ calibrar T2
→ calibrar T3
→ calibrar T4
```

Definitivas del jugador permanecen fuera del balance de monstruos.
