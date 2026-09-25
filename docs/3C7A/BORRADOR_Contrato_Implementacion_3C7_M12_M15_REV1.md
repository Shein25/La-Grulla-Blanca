# Borrador de Contrato de Implementación — 3C.7 — M12–M15

**Proyecto:** La Grulla Blanca  
**Fecha:** 2026-09-25  
**Estado:** `BORRADOR_NO_LISTO_PARA_IMPLEMENTACION`

Este documento organiza el contrato técnico futuro para M12–M15, pero **no autoriza implementación**.

## 0. Precondiciones obligatorias antes de convertirlo en contrato ejecutable

Debe existir evidencia documental de:

1. PASS runtime definitivo de 3C.6;
2. cierre documental independiente de M08–M11 REV2;
3. resolución del modelo uniforme de permisos;
4. definición concreta de `CORROBORACION_FUERTE_INDEPENDIENTE`;
5. definición técnica del PROTOCOLO y localización final del Custodio;
6. balance numérico M12–M15;
7. rama de implementación exclusiva creada desde el runtime predecesor aprobado.

Si falta cualquiera, mantener `NO_LISTO_PARA_IMPLEMENTACION`.

## 1. Autoridad

Implementar únicamente contra:

1. `CIERRE_3C7A_M12_GATE_REV2.md`;
2. `Reconciliacion_3C7A_M12_Gate_LIII_LIV_REV2.md`;
3. `Matriz_Implementacion_3C7A_M12_Gate_LIII_LIV_REV2.json`;
4. `CIERRE_3C7A_M13_M15_REV2.md`;
5. `Reconciliacion_3C7A_M13_M15_REV2.md`;
6. `Matriz_Implementacion_3C7A_M13_M15_REV2.json`;
7. `Auditoria_Cierre_3C7A_M12_M15_REV2_CLAUDE.md`;
8. M08–M11 REV2 cerrado documentalmente;
9. runtime predecesor aprobado de 3C.6;
10. `grulla-blanca_ver74.html` sólo como referencia de infraestructura/topología donde siga aplicando.

### Matrices congeladas

M12/gate REV2 SHA-256:
`4741f6bc28a36d71d4309783dff51ee8b9a8a187f6250e93a450616d8c222978`

M13–M15 REV2 SHA-256:
`53d3bc817713aba9177d86bb55cf2a44c1b1a02fcdeff0b194137fe36ecab846`

## 2. Invariantes globales

Mantener:
- 329 rooms;
- 17 áreas;
- 787 exits dirigidos;
- `ROOMS.exits` sin cambios;
- gates existentes como fuente física de bloqueo;
- save schema 2 salvo auditoría explícita que demuestre imposibilidad;
- sin tiempo diegético;
- sin timers narrativos;
- sin crear rooms nuevas para controles/protocolo;
- sin abrir M16, R7, R10 o Núcleo Profundo.

## 3. Alcance M12

Implementar:
- activación institucional de M12;
- apertura `GATES_329.M12`;
- `PRIMERA_ALA_INVESTIGACION`;
- evidencia semántica Primera Ala;
- niveles INSUFICIENTE/SUFICIENTE/CONCLUYENTE;
- Custodio con rutas COMBATE/PROTOCOLO equivalentes;
- seis atajos opcionales e independientes;
- cierre M12;
- R5 CONFIRMADO;
- +1 Comprensión one-shot;
- autorización institucional profunda;
- gate LIII→LIV;
- sustitución de `PUERTAS[4]` legacy para etapa 3→4.

### 3.1 Cierre

`M12=HECHA` sólo si:

`evidenciaPrimeraAla=CONCLUYENTE`

y

`custodioDosAlas` terminal.

### 3.2 SUFICIENTE

`SUFICIENTE` puede habilitar PROTOCOLO, pero no cierra la misión.

### 3.3 CONCLUYENTE

Debe obtenerse mediante `SUFICIENTE + CORROBORACION_FUERTE_INDEPENDIENTE`.

El Custodio no promueve automáticamente a CONCLUYENTE.

### 3.4 Custodio

Persistencia única:
`NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`.

COMBATE y PROTOCOLO deben ser equivalentes para progreso y recompensa narrativa.

### 3.5 Umbral Mantenimiento

`ala_umbral_mantenimiento` puede quedar conocido tras M12.

`PASO_MANTENIMIENTO=false` hasta M13.

## 4. Gate LIII→LIV

Condición narrativa:
`qi>=75 + M11 HECHA + M12 HECHA + R3 CONFIRMADO + R5 CONFIRMADO + autorización institucional`.

Al superar:
- `player.etapa=4`;
- `arc1.estado=LIV_REVELACION`;
- M13 disponible derivada;
- sin cambio de rango institucional.

Eliminar/neutralizar para etapa 3→4:
- requisito de dos píldoras;
- consumo de dos píldoras;
- `comprension:6`;
- doble validación legacy + Arc1.

## 5. Alcance M13

Activación tras LIV_REVELACION/M12.

Conceder `MANTENIMIENTO_INVESTIGACION` y abrir únicamente `PASO_MANTENIMIENTO`.

R6 debe demostrar continuidad de consumo/operación/correlación moderna, sin revelar entidad viva.

Categorías técnicas actuales:
- `CONSUMO_ANTIGUO_IDENTIFICADO`;
- `OPERACION_PRESENTE`;
- `CORRELACION_PRODUCCION`.

Son `ELECCION_TECNICA_3C7_AUDITAR`, no etiquetas canónicas obligatorias.

Cierre:
- M13 HECHA;
- R6 CONFIRMADO;
- Comprensión +1 one-shot;
- M14 disponible derivada.

## 6. Alcance M14

Conceder `NUCLEO_SUPERIOR` y abrir únicamente `PASO_NUCLEO`.

Confirmar consentimiento original mediante evidencia material/documental.

Categorías técnicas actuales:
- `ACTO_FORMAL`;
- `PARTICIPACION_MUTUA`;
- `CONSENTIMIENTO_DOCUMENTADO`.

Cierre:
- M14 HECHA;
- R8 CONFIRMADO;
- Comprensión +1 one-shot;
- M15 disponible derivada.

No revelar R9/R7/R10 ni modificar vínculo.

## 7. Alcance M15

Centro documental: `nucleo_archivo_promesa`.

Premisa:
`RELEVO_PREVISTO`.

Tres aplazamientos:
1. `APLAZAMIENTO_TECNICO`;
2. `APLAZAMIENTO_RUPTURA`;
3. `NORMALIZACION_MANTENIMIENTO`.

`RELEVO_PREVISTO` no es cuarto aplazamiento.

Cierre:
- M15 HECHA;
- R9 CONFIRMADO;
- Comprensión +1 one-shot;
- condiciones previas de M16 satisfechas.

Mantener:
- `PASO_PULSO=false`;
- `NUCLEO_PROFUNDO=false`;
- R7 cerrado;
- R10 cerrado;
- LIBERAR/CUSTODIAR sin decidir.

## 8. M16 fuera de alcance

No implementar M16.

El contrato debe dejar sólo una dependencia diagnóstica/documental de que M15 terminó.

El futuro evento M16 será:
- separado de M15;
- alcanzable;
- idempotente;
- transición única `LIV_REVELACION → LIV_CRISIS`;
- sin temporizador;
- sin `entrarSala()` genérico como disparador oculto.

## 9. Persistencia

Todo estado nuevo bajo `flags.arc1` / `this.quests`.

No crear duplicados persistentes para hechos derivables.

No crear `DOS_ALAS=COMPRENDIDAS` si el estado sigue siendo derivable de M11/R3/PRINCIPIO.

## 10. Idempotencia

Cada evidencia/hito/recompensa/permiso debe ser one-shot.

Save/load no debe:
- registrar evidencia nueva;
- completar hitos;
- abrir gates nuevos;
- mover misiones;
- repagar Comprensión/Mérito/Contribución;
- resolver Custodio;
- activar M16.

## 11. Tests mínimos futuros

Obligatorios al convertir este borrador en contrato ejecutable:

- topología 329/17/787 intacta;
- gates M12/Mantenimiento/Núcleo/Pulso;
- rutas COMBATE/PROTOCOLO;
- evidencia SUFICIENTE sin cierre;
- evidencia CONCLUYENTE sin Custodio;
- Custodio terminal con sólo SUFICIENTE no cierra;
- corroboración fuerte antes/después del Custodio sin soft-lock;
- atajos 0/6 a 6/6 sin ser requisitos;
- LIII→LIV sin `PUERTAS[4]` legacy;
- M13 no revela R7;
- M14 no revela R9/R7/R10;
- M15 no abre Pulso/Núcleo Profundo;
- M15 no activa M16;
- save/load en mitad de cada misión;
- idempotencia de todos los one-shots.

## 12. Estado del borrador

`3C7_M12_M15_CONTRATO_BORRADOR_NO_LISTO_PARA_IMPLEMENTACION`

**No autoriza implementación ni merge.**
