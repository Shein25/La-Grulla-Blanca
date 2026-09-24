# 3C.7A — M08–M15 — Fase 1 / Inventario canónico REV2

**Fecha:** 2026-09-24  
**Estado:** `LISTA_PARA_REAUDITORIA_DE_CIERRE`  
**Baseline:** `grulla-blanca_ver74.html`  
**SHA-256 recalculado:** `8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

REV2 corrige H-01…H-09 de la auditoría externa de Claude sin convertir pendientes de reconciliación en canon.

## 1. Autoridad y frontera

Jerarquía:
1. decisiones humanas posteriores;
2. Auditoría 6 canónica;
3. Auditoría 6 estructurada;
4. ver74/3C.5 sólo para infraestructura;
5. topología/Atlas congelados.

Frontera provisional hasta cierre de 3C.6A REV3.1:

```text
arc1.estado=LIII_INVESTIGACION
SECTA_INTERIOR=true
M12=false
ATAJO_ALA_*=false
```

## 2. Cierre 3C.5 correctamente citado

3C.5 sí está cerrado por una auditoría posterior al informe de implementación:

```text
docs/AUDITORIA_3C5_VER74_2026-09-23.md
3C5_IMPLEMENTACION_AUDITADA_PASS
398/398 PASS en Chromium real
```

El informe de implementación incluido en el paquete era anterior a ese cierre.

## 3. Columna vertebral

```text
M08 ─┐
M09 ─┼─> M11 -> M12 -> gate LIII→LIV -> M13 -> M14 -> M15
M10 ─┘
```

M08/M09/M10 son paralelas. M11 exige las tres. M12 exige M11. M13 requiere LIV_REVELACION. M14 exige M13. M15 exige M14. M16 queda fuera.

## 4. Revelaciones

```text
M08 R2 CONFIRMADO
M09 R3 PARCIAL
M10 R4 CONFIRMADO
M11 R3 CONFIRMADO
M12 R5 CONFIRMADO
M13 R6 CONFIRMADO
M14 R8 CONFIRMADO
M15 R9 CONFIRMADO
```

R7, R10, dependencia viva, identidad actual de la Grulla y LIBERAR/CUSTODIAR quedan reservados.

## 5. Restricciones negativas recuperadas

### M08
- `FORMACIONES_INVESTIGACION` permanece activo tras M08.
- M08 no realiza la síntesis de Dos Alas.

### M09
- No revela Primera Ala como red completa.
- “Dos Alas” puede aparecer sin definición cerrada.

### M10
- No confirma Segunda Rama = Dos Alas.
- No habilita injerto jugable.
- `ESTUDIAR INJERTO` no queda visible en Arc1; el verbo futuro es `LEER APENDICE`.
- Nadie realiza injerto en M10.

### M12
- `ala_umbral_mantenimiento` queda conocido/visible, pero no accesible hasta M13.
- Nunca exige 6/6 atajos.

### M13
- Demuestra flujo/consumo actual, no dependencia viva. R7 pertenece a M17.

### M14
- Confirma consentimiento original.
- No confirma aún temporalidad del pacto.
- No revela R10.
- No modifica el vínculo.

### M15
- Confirma relevo previsto y aplazado.
- No revela R7/R10.
- `nucleo_descenso_pulso` sigue cerrado hasta M17/NUCLEO_PROFUNDO.
- R8+R9 no determinan LIBERAR/CUSTODIAR.
- Cadena fuente: `prototipo insuficiente -> ruptura de Primera Ala -> normalización del mantenimiento`.

## 6. Mapeos: canon vs candidato técnico

### M08
`formaciones_sala_mapas` existe en ver74, pero sigue siendo sólo candidato técnico hasta reconciliación.

### M09
Archivo Común/Restringido continúan sin room exacta congelada.

### M10
ver74 contiene:

```text
sala_anatomica
archivo_clinico
```

y Chen Bo tiene ambas en su territorio. Esto **no** las convierte retroactivamente en canon de Auditoría 6. Se clasifican:

`CANDIDATO_TECNICO_A_RECONCILIAR_NO_CANON_POR_NOMBRE`.

### M11
La room de la reunión sigue pendiente. “Manantial Partido” sigue siendo una referencia ambigua y no se toma como room de reunión.

## 7. M12 y gate LIII→LIV

Rooms de M12 recuperadas de Auditoría 6:

```text
formaciones_sello_antiguo
formaciones_descenso_tecnico
ala_vestibulo
ala_nudo_seis_corrientes
ala_camara_dos_alas
ala_umbral_mantenimiento
```

Entrada oficial Formaciones→Primera Ala ≠ seis atajos.

Custodio: COMBATE o PROTOCOLO. No requiere secretos opcionales, 6/6 atajos, único ecológico ni Afinidad alta.

Canon del gate:

```text
qi>=75
+ DosAlas==COMPRENDIDAS
+ redPrimeraAla==CONCLUYENTE
+ autorización institucional
```

No exige todos los atajos, únicos o rooms.

Legacy ver74 verificado:

```text
PUERTAS[4] = 2 píldoras + comprensión:6
```

Clasificación: `CAMBIO_NECESARIO_3C7`.

Pendientes explícitos, no resueltos por Fase1:
1. M12 puede cerrar con evidencia SUFICIENTE mientras el gate pide CONCLUYENTE: definir continuidad de evidencia sin soft-lock.
2. M11 produce `DOS_ALAS=PRINCIPIO`; gate usa `DosAlas==COMPRENDIDAS`: definir equivalencia normalizada.
3. definir origen exacto de la autorización institucional.

## 8. Legacy M12/M17

El modelo de `reliquias_verticales`/reliquias-llave es legacy y no se usa como canon de M12.
La aparente clasificación inconsistente dentro de Auditoría 6 se registra como deuda documental histórica, no como regla de 3C.7.
M17 queda fuera de alcance y se tratará en su frente correspondiente.

## 9. Verificaciones técnicas de ver74

- SHA-256 recalculado: coincide con el baseline esperado.
- `PUERTAS[4]`: legacy confirmado.
- existen `sala_anatomica`, `archivo_clinico`, `formaciones_sala_mapas`.
- existen He Zhen, Wen Tao, Song Rui, Lan Meihua, Chen Bo, Qiao Ren, Duan Shibo, Ma Qiren y Lu Cheng.
- Chen Bo incluye `sala_anatomica` y `archivo_clinico` en su territorio.

Estas comprobaciones sólo validan infraestructura actual; no convierten mappings históricos ambiguos en canon.

## 10. Pendientes para Reconciliación 3C.7

- mappings M08/M09/M10/M11;
- Manantial Partido;
- evidencia Primera Ala y SUFICIENTE→CONCLUYENTE;
- normalización Dos Alas;
- autorización institucional;
- sustitución del gate legacy;
- permisos: fuente/origen/vigencia;
- anclajes;
- recompensas numéricas;
- one-shots/idempotencia;
- evidencias M13–M15;
- legacy reliquias;
- M16 fuera de alcance.

## 11. Estado

`3C7A_FASE1_REV2_LISTA_PARA_REAUDITORIA`

La Fase 1 sólo pretende certificar una recuperación canónica suficiente para comenzar la reconciliación. No es todavía un contrato de implementación.