# GRULLA BENCH — Técnicas solas y consumibles

Fecha: 2026-10-02

## Decisión

El banco debe permitir aislar tres capas causales:

1. **ULTIS_EQUIPMENT**
   - Ultis sí
   - equipo sí
   - técnicas normales no

2. **TECHNIQUES_EQUIPMENT**
   - técnicas normales sí
   - equipo sí
   - Ultis no

3. **FULL_LOADOUT**
   - técnicas sí
   - Ultis sí
   - equipo sí

Así se puede medir por separado la contribución de técnicas y de Ultis antes de estudiar sus sinergias.

## Pociones

Los análisis anteriores del nuevo bench habían dejado consumibles fuera para aislamiento.

Eso cambia parcialmente tras revisar la autoridad del 01/10.

### Ratificado

HP:

`ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json`

Estado:

`READY_HUMAN_RATIFIED`

LIV Condensada:

- Impura: 5d4+10
- Estable: 5d6+12
- Superior: 6d6+16
- Excepcional: 7d6+20

Qi:

`ALCHEMY_QI_RECOVERY_CONTRACT_V0_2.json`

Estado:

`READY_HUMAN_RATIFIED`

LIV Tempestad:

- Impura: 32
- Estable: 34
- Superior: 36
- Excepcional: 38

Reglas de combate ratificadas en contrato Qi:

- beber consume la acción completa;
- recuperación absoluta;
- cap en Qi máximo;
- sin cooldown artificial de poción.

El stress de jefes existente además presupone que el enemigo conserva su respuesta normal después de beber.

## Lo que NO está canonizado

La cantidad de pociones que lleva el personaje.

El stress histórico usa:

- 1 / 2 / 3 pociones HP excepcionales;
- 0 / 1 poción Qi excepcional.

Eso se conserva como **eje LAB**, no como inventario canon.

## Diseño analítico

Cada frente tendrá dos lecturas:

### Headline
Sin consumibles.

Sirve para atribuir potencia a Ulti/técnica/equipo.

### Prepared Consumable Stress
Misma seed y mismo loadout, añadiendo uno de los brazos de cantidad.

Sirve para responder:

- cuánto cambia la supervivencia por preparación;
- cuánto se prolonga F1/F2/F3;
- si la poción permite llegar a una ventana de Ulti que antes no aparecía;
- si una Ulti parece fuerte sólo porque el jugador compra tiempo con curación;
- si el consumo de una acción para beber es tácticamente caro frente a la Grulla;
- si el Qi adicional cambia la fase óptima de activación.

## Política de uso

HP conserva la regla ya usada en stress:

`HP <= 60% max AND missing HP >= potion minimum`

Para FULL_LOADOUT:

Qi conserva:

`current Qi < cheapest usable offensive technique cost`

Para ULTIS_EQUIPMENT no se debe reutilizar esa regla porque no hay técnicas normales. El adapter expone un trigger de **stress**, no canon:

`Qi actual < coste de la Ulti aún no activada`

Ese brazo debe reportarse aparte y nunca confundirse con IA/política final de jugador.

## Phase sweep

Pociones también deben registrarse por fase:

- usos HP en F1/F2/F3;
- usos Qi en F1/F2/F3;
- HP/Qi restaurado por fase;
- acciones gastadas bebiendo;
- acciones de la Grulla recibidas como consecuencia;
- si beber retrasó o adelantó la activación de la Ulti.

Esto se cruza con:

`F1 / F2 / F3 / PREPARED_OPPORTUNITY`

## Regla estadística

Nunca comparar:

`con consumibles vs sin consumibles`

si cambian a la vez seed, equipo, estado inicial o policy.

Consumibles son una dimensión pareada más.
