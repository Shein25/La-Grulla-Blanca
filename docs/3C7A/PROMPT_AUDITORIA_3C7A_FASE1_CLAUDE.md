# Prompt — Auditoría externa 3C.7A Fase 1 (M08–M15)

Quiero que hagas una **auditoría documental independiente** de la Fase 1 de 3C.7A para *La Grulla Blanca*.

Esta auditoría **NO debe implementar código** y **NO debe convertir huecos documentales en canon**. El objetivo es verificar que la recuperación de M08–M15 desde Auditoría 6 sea fiel, que las afirmaciones nuevas contra ver74 estén sustentadas, y que el inventario de pendientes sea correcto antes de pasar a la reconciliación M08–M11.

## Repositorio y rama

Repositorio:
https://github.com/Shein25/La-Grulla-Blanca

Rama de sólo lectura:
`audit/3c7a-m08-m15`

HEAD esperado:
`330cb6c348f5aad74c4e33b9b728cdfd2de19e67`

NO modifiques archivos.
NO hagas commits.
NO hagas merge.
NO implementes código.

## Archivos principales

Fase 1:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/docs/3C7A/Auditoria_3C7A_M08_M15_FASE1_REV1.md

Matriz:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/docs/3C7A/Matriz_3C7A_M08_M15_FASE1_REV1.json

Índice:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/docs/3C7A/PAQUETE_3C7A_M08_M15_FASE1.md

Fuente canónica Auditoría 6:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/docs/3C7A/fuentes/Auditoria_6_Misiones_M01_M18_CANONICA.md

Fuente estructurada Auditoría 6:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/docs/3C7A/fuentes/Auditoria_6_Misiones_M01_M18_Estructurada.json

Baseline técnico:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/grulla-blanca_ver74.html

Informe 3C.5:
https://raw.githubusercontent.com/Shein25/La-Grulla-Blanca/audit/3c7a-m08-m15/Informe_Implementacion_3C5_ver74.md

SHA-256 esperado de ver74:
`8cd2d2f51e15a433d35397fbb31035b3067f5a26bd942d890f07a0f316359566`

Si `ver74.html` llega truncado, **no inventes**. Auditá primero la parte documental y marcá qué comprobaciones técnicas concretas faltan.

---

# 1. Jerarquía y alcance

Tomá como autoridad, en este orden:

1. decisiones humanas posteriores explícitas;
2. Auditoría 6 canónica;
3. Auditoría 6 estructurada;
4. ver74 + 3C.5 para comprobar infraestructura actual;
5. topología/Atlas congelados cuando estén expresamente disponibles.

No conviertas un `NO CERRADO EN FUENTE` de Auditoría 6 en canon sólo porque ver74 contenga una room o NPC con nombre parecido.

No audites M16–M18 salvo para comprobar que 3C.7 no adelanta contenido reservado.

---

# 2. Coherencia Fase1 MD ↔ JSON

Compará completos:

- `Auditoria_3C7A_M08_M15_FASE1_REV1.md`
- `Matriz_3C7A_M08_M15_FASE1_REV1.json`

Verificá que coincidan en:

- frontera provisional 3C.6A→3C.7;
- dependencias M08–M15;
- revelaciones R2/R3/R4/R5/R6/R8/R9;
- áreas;
- rooms ya cerradas;
- gaps declarados;
- gate LIII→LIV;
- hallazgos F1-01…F1-09;
- lista de pendientes.

Toda divergencia debe citarse concretamente.

---

# 3. Recuperación de la columna vertebral

Verificá contra Auditoría 6 que sea correcto:

```text
M08 ─┐
M09 ─┼─> M11 -> M12 -> gate LIII->LIV -> M13 -> M14 -> M15
M10 ─┘
```

Confirmá o refutá:

- M08/M09/M10 paralelas y de orden libre;
- M11 exige las tres;
- M12 exige M11;
- M13 sólo tras LIII→LIV;
- M14 exige M13;
- M15 exige M14;
- M16 queda fuera del alcance activo.

---

# 4. Revelaciones

Auditá que Fase1 preserve exactamente:

- M08 → R2 CONFIRMADO
- M09 → R3 PARCIAL
- M10 → R4 CONFIRMADO
- M11 → R3 CONFIRMADO
- M12 → R5 CONFIRMADO
- M13 → R6 CONFIRMADO
- M14 → R8 CONFIRMADO
- M15 → R9 CONFIRMADO

Comprobá que no se adelante:

- R7;
- R10;
- identidad actual de la Grulla;
- dependencia viva actual;
- decisión LIBERAR/CUSTODIAR.

---

# 5. M08

Auditá qué está realmente cerrado por fuente y qué no.

Debe quedar claro que:

- He Zhen activa/concede `FORMACIONES_INVESTIGACION`;
- M08 confirma R2;
- requiere repetir mediciones en un nodo/sector independiente;
- el área Formaciones está cerrada;
- los room IDs exactos de los puntos exteriores y de la antigua “Sala de Mapas de Flujo” **no estaban cerrados por Auditoría 6**.

Ver74 contiene `formaciones_sala_mapas`, pero Fase1 deliberadamente NO afirma que sea automáticamente la equivalencia canónica.

Decí si esa cautela es correcta.

---

# 6. M09

Verificá:

- ARCHIVO_COMUN al inicio;
- ARCHIVO_RESTRINGIDO durante progreso, autorizado por Qiao Ren;
- R3 PARCIAL;
- uso de LEER ESCRITURAS;
- tres clases de inconsistencia documental;
- no revelar todavía la Primera Ala como red completa.

Auditá si Fase1 hace bien en dejar pendiente el mapping exacto de rooms de Archivo Común/Restringido.

---

# 7. M10

Auditoría 6 decía que “Sala Anatómica / Archivo Clínico” no tenían room_id literal citado en sus fuentes.

Fase1 afirma que el baseline actual ver74 permite resolver esa deuda con:

`sala_anatomica`
`archivo_clinico`

y que Chen Bo tiene ambas en su territorio.

Verificá esta afirmación contra ver74/3C.5 si el acceso lo permite.

También confirmá:

- R4 CONFIRMADO;
- no confundir Segunda Rama con Dos Alas todavía;
- no habilitar injerto jugable;
- M10 no concede la síntesis de M11.

---

# 8. M11

Confirmá:

- requiere M08+M09+M10;
- reunión de síntesis, no nueva expedición;
- participantes canónicos: He Zhen, Song Rui, Lan Meihua;
- produce R3 CONFIRMADO;
- `DOS_ALAS=PRINCIPIO`;
- `SEGUNDA_RAMA=APLICACION_CORPORAL`;
- Comprensión +1 canónica.

Auditá si es correcto mantener pendiente la room exacta de la reunión.

---

# 9. M12

Comprobá que Fase1 recupera correctamente las rooms ya cerradas:

- `formaciones_sello_antiguo`
- `formaciones_descenso_tecnico`
- `ala_vestibulo`
- `ala_nudo_seis_corrientes`
- `ala_camara_dos_alas`
- `ala_umbral_mantenimiento`

Confirmá además:

- la entrada oficial Formaciones→Primera Ala NO es uno de los seis atajos;
- M12 no exige 6/6 atajos;
- Custodio: COMBATE o PROTOCOLO;
- el protocolo no exige secretos opcionales ni Afinidad alta;
- `ala_umbral_mantenimiento` queda conocido pero no accesible al cerrar M12;
- R5 CONFIRMADO.

Indicá qué especificaciones faltan realmente antes de implementar:
evaluador de evidencia, one-shots, anclajes, combate/protocolo, etc.

---

# 10. Gate LIII→LIV

Este punto es crítico.

Auditoría 6 documenta:

```text
qi>=75
+ DosAlas==COMPRENDIDAS
+ redPrimeraAla==CONCLUYENTE
+ autorización institucional
```

y que NO exige:

- seis atajos;
- todos los únicos;
- todas las rooms.

Fase1 señala que ver74 conserva un gate legacy de etapa 4 basado en:

```text
2 píldoras
+ comprensión:6
```

Verificá ambas cosas.

Clasificá la sustitución futura del gate legacy como:

- CAMBIO_NECESARIO_3C7
- o contradicción documental

según corresponda.

No diseñes todavía el gate nuevo más allá de lo que las fuentes soportan.

---

# 11. M13–M15

Confirmá la secuencia y fronteras de revelación:

## M13
- R6 CONFIRMADO;
- demuestra que la red antigua sigue consumiendo recursos;
- NO revela dependencia viva;
- áreas: mantenimiento/producción/archivos.

## M14
- R8 CONFIRMADO;
- confirma consentimiento original de la Grulla;
- NO confirma todavía que el pacto debía ser temporal;
- produce `NUCLEO_SUPERIOR`.

## M15
- R9 CONFIRMADO;
- confirma relevo previsto y aplazado;
- cadena de al menos tres aplazamientos;
- NO revela R7/R10;
- `nucleo_descenso_pulso` sigue cerrado hasta M17.

Verificá las rooms que Fase1 considera ya cerradas para M13–M15.

---

# 12. Compatibilidad con 3C.5 NPC

Sin diseñar anclajes nuevos todavía, verificá que los NPC relevantes existan y que Fase1 no invente NPC:

- He Zhen
- Wen Tao
- Song Rui
- Lan Meihua
- Chen Bo
- Qiao Ren
- Duan Shibo
- Ma Qiren
- Lu Cheng

Si ver74/Informe 3C.5 no permiten comprobar alguno, marcá NO_VERIFICADO.

---

# 13. Qué NO debe resolver esta Fase1

No penalices Fase1 por no cerrar todavía:

- rooms exactas M08/M09/M11;
- anclajes M08–M15;
- rewards numéricas finales;
- one-shots;
- evaluador Primera Ala;
- contrato exacto Custodio;
- evidencia concreta M13–M15;
- gate LIII→LIV implementable.

Esos son **pendientes declarados para la reconciliación siguiente**.

Sí penalizá si Fase1:

- inventó algo;
- omitió canon importante;
- convirtió una propuesta en canon;
- perdió una restricción narrativa;
- contradice ver74 donde afirma haberlo verificado.

---

# 14. Clasificación

Usá sólo:

- BLOQUEANTE
- CORRECCION_DOCUMENTAL
- CAMBIO_NECESARIO_3C7
- PENDIENTE_RECONCILIACION
- ENDURECIMIENTO_FUTURO
- VERIFICADO

---

# 15. Veredicto

Terminá EXACTAMENTE con uno:

`3C7A_FASE1_APTA_PARA_RECONCILIACION`

`3C7A_FASE1_REQUIERE_CORRECCIONES`

`3C7A_FASE1_FALLO_CONCEPTUAL`

Para el primer veredicto no hace falta que M08–M15 estén implementables.
Sólo debe cumplirse:

- recuperación fiel del canon;
- MD↔JSON coherentes;
- gaps correctamente etiquetados;
- ningún canon inventado;
- ninguna revelación adelantada;
- gate legacy correctamente identificado como deuda de 3C.7;
- suficiente base para empezar la reconciliación M08–M11.

## Entregable

`Auditoria_Externa_3C7A_FASE1_CLAUDE.md`

Cabecera:

Agente auditor: Claude
Modelo/versión:
Fecha:
Repositorio:
Rama:
HEAD:
Baseline:
SHA baseline:
Fase1 MD:
Fase1 JSON:
Fuentes usadas:
Tipo: auditoría documental externa de recuperación canónica

No escribas nada en GitHub.
Entregame únicamente el informe.
