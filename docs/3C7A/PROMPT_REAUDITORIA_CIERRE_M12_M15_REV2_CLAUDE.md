# Prompt — reauditoría de cierre 3C.7A M12–M15 REV2

Auditá exclusivamente las correcciones REV2 introducidas tras la auditoría externa anterior.

Modo solo lectura. No modifiques archivos, no implementes, no crees ramas y no hagas merge.

## Archivos principales

- `docs/3C7A/Reconciliacion_3C7A_M12_Gate_LIII_LIV_REV2.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M12_Gate_LIII_LIV_REV2.json`
- `docs/3C7A/Reconciliacion_3C7A_M13_M15_REV2.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M13_M15_REV2.json`
- `docs/3C7A/Reconciliacion_3C7A_M08_M11_REV2.md`
- `docs/3C7A/Matriz_Implementacion_3C7A_M08_M11_REV2.json`
- T257/T288/T289 y ver74 como fuentes de contraste.

## Bloque A — comprobar resolución de H-A1/H-A2/H-A3

### H-A1
Verificá que REV2 ya NO afirme como canon que `SUFICIENTE + Custodio terminal` eleva automáticamente a `CONCLUYENTE`.

Debe quedar:
- `SUFICIENTE` habilita progreso/protocolo;
- `CONCLUYENTE = SUFICIENTE + CORROBORACION_FUERTE_INDEPENDIENTE`;
- Custodio terminal es requisito separado de cierre;
- la corroboración concreta permanece etiquetada `ELECCION_TECNICA_3C7_AUDITAR`;
- debe existir una ruta alcanzable que evite soft-lock.

Clasificá H-A1 como `RESUELTO`, `PARCIAL` o `NO_RESUELTO`.

### H-A2
Verificá la ruta física corregida desde `ala_camara_dos_alas` hasta `ala_umbral_mantenimiento`, incluyendo regreso por `ala_nudo_seis_corrientes`, `ala_vestibulo` y paso por `ala_galeria_distribucion`.

Clasificá H-A2.

### H-A3
Contrastá directamente M08–M11 REV2 y confirmá o refutá:
`M11=HECHA => R3=CONFIRMADO` y `sintesis.DOS_ALAS=PRINCIPIO`.

Clasificá H-A3.

## Bloque B — comprobar resolución de H-B1/H-B2/H-B3

### H-B1
Verificá que `RELEVO_PREVISTO` sea premisa de R9 y NO un cuarto aplazamiento.

Los tres aplazamientos deben ser exactamente conceptualmente:
1. técnico/prototipo insuficiente;
2. ruptura/pérdida de capacidad de Primera Ala;
3. normalización como mantenimiento/procedimiento.

Clasificá H-B1.

### H-B2
Verificá que el evaluador M13 (`CONSUMO_ANTIGUO_IDENTIFICADO`, `OPERACION_PRESENTE`, `CORRELACION_PRODUCCION`) esté explícitamente marcado `ELECCION_TECNICA_3C7_AUDITAR` y no como canon literal de T289.

Clasificá H-B2.

### H-B3
Verificá que el inicio M16 quede registrado como dependencia formal de cierre del tramo M12–M16 y que:
- no se active en el mismo cierre de M15;
- no use temporizador;
- deba ser evento separado, alcanzable e idempotente;
- deba producir una única transición `LIV_REVELACION -> LIV_CRISIS`;
- no se sustituya por `entrarSala()` genérico.

Clasificá H-B3.

## Puntos que pueden seguir pendientes sin provocar FAIL

Si están correctamente etiquetados como pendientes técnicos/documentales, NO los conviertas automáticamente en fallo:
- fuente concreta de `CORROBORACION_FUERTE_INDEPENDIENTE`;
- interfaz de PROTOCOLO del Custodio;
- localización final del Custodio;
- modelo uniforme de permisos;
- balance numérico;
- evento M16, porque se reconciliará en documento separado;
- runtime predecesor hasta PASS de 3C.6.

## Entrega

Entregá:
1. tabla H-A1/A2/A3 y H-B1/B2/B3 con `RESUELTO / PARCIAL / NO_RESUELTO / REGRESION`;
2. cualquier nueva contradicción introducida por REV2;
3. consistencia MD↔JSON de ambos bloques;
4. riesgos de soft-lock restantes;
5. correcciones mínimas sólo si siguen siendo necesarias.

Usá dos veredictos independientes:

`3C7A_M12_GATE_REV2_APTA_PARA_CONTRATO`
`3C7A_M12_GATE_REV2_REQUIERE_CORRECCIONES`

y

`3C7A_M13_M15_REV2_APTA_PARA_CONTRATO`
`3C7A_M13_M15_REV2_REQUIERE_CORRECCIONES`

No implementes. No avances M16.
