# Reconciliación 3C.7A — M12 + gate LIII→LIV — REV1

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_AUDITORIA_DOCUMENTAL`  
**Alcance:** M12, evidencia de Primera Ala, Custodio de Dos Alas y gate de cultivo LIII→LIV.  
**No incluye:** implementación, M13 completo, M14+, M16+, balance numérico final.

> Esta REV1 fue corregida tras recuperar directamente la Fuente Maestra ver55. Para M08–M12, la autoridad principal es T288 (2026-09-20 07:49:52 UTC), posterior a T254 y T257. T257 se conserva como apoyo técnico de idempotencia/estados sólo donde T288 no lo contradice.

## 1. Corrección de la deuda H-08

La lectura derivada de Fase1 REV2 trataba como deuda que M12 podía cerrar con evidencia `SUFICIENTE` mientras el gate exigía `CONCLUYENTE`. T288 permite reconciliarlo sin fase post-M12:

- un recorrido principal puede alcanzar `SUFICIENTE`;
- `SUFICIENTE` permite progreso y habilita la vía de protocolo del Custodio;
- exploración adicional puede elevar la evidencia a `CONCLUYENTE`;
- si el jugador llega al Custodio con evidencia sólo suficiente, la resolución central puede aportar la corroboración final;
- **M12 sólo cierra cuando la red queda `CONCLUYENTE` y el Custodio está resuelto**.

Por lo tanto, no se diseña una misión cerrada que luego deba reabrirse o continuar para alcanzar el gate.

## 2. Tres gates distintos

### 2.1 `GATES_329.M12`

Extremos existentes en ver74: `formaciones_sello_antiguo ↔ formaciones_descenso_tecnico`. Es la entrada oficial de M12 a Primera Ala.

### 2.2 Gate de cultivo LIII→LIV

No es topológico. Controla el paso `LianQi III / Consolidación → LianQi IV / Refinamiento`.

### 2.3 `GATES_329.PASO_MANTENIMIENTO`

Extremos: `ala_umbral_mantenimiento ↔ mantenimiento_acceso`. Permanece cerrado durante M12. El umbral queda visible/conocido, pero el descenso corresponde a M13.

## 3. Acceso y ruta principal de M12

Requiere `M11=HECHA` y `arc1.estado=LIII_INVESTIGACION`.

La entrada oficial está congelada conceptualmente como `formaciones_sello_antiguo → formaciones_descenso_tecnico → ala_vestibulo`. El recorrido principal continúa mediante `ala_nudo_seis_corrientes` y `ala_camara_dos_alas`, y permite terminar conociendo `ala_umbral_mantenimiento`.

La entrada oficial **no es uno de los seis `ATAJO_ALA_*`**.

## 4. Activación y permiso

Al iniciar M12 deben quedar coherentemente activos `M12=ACTIVA`, `flags.arc1.permisos.PRIMERA_ALA_INVESTIGACION=true` y `gates.M12=true`. El sello se abre mediante procedimiento institucional, no mediante reliquia o llave.

Como disparador técnico se propone `HABLAR he_zhen @ formaciones_sello_antiguo`. Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`; no se eleva a canon de fuente.

`PRIMERA_ALA_INVESTIGACION` permanece después de cerrar M12 para que Primera Ala siga siendo explorable. No abre por sí mismo `PASO_MANTENIMIENTO`.

## 5. Evidencia de Primera Ala

Se propone persistir una sola estructura bajo `flags.arc1.evidenciaPrimeraAla`, con `nivel`, hitos semánticos y fuentes únicas ya registradas.

Niveles internos: `INSUFICIENTE → SUFICIENTE → CONCLUYENTE`.

No existe objetivo visible `6/6`, ni contador obligatorio de rooms, atajos o secretos.

### 5.1 Hitos semánticos

T257 aporta como lenguaje técnico compatible con T288: `NUDO_INTERPRETADO`, `DOS_ALAS_ARQUITECTURA`, `PATRON_RAMA`, `CONEXION_SUPERFICIE` y posibles corroboraciones equivalentes.

- `NUDO_INTERPRETADO`: fuente natural `ala_nudo_seis_corrientes`; demuestra un centro distribuidor deliberado.
- `DOS_ALAS_ARQUITECTURA`: fuente natural `ala_camara_dos_alas`; demuestra físicamente el principio aprendido en M11.
- `PATRON_RAMA`: exige estudiar al menos una rama funcional y reconocer señales de diseño compartido. Las familias son Medicina, Jardines, Cantera, Aguas, Archivos y Formaciones. REV1 **no congela un número interno exacto de rooms o ramas**.
- `CONEXION_SUPERFICIE`: corroboración fuerte opcional. Los terminales existentes son `ala_med_06`, `ala_jardines_06`, `ala_cantera_06`, `ala_aguas_06`, `ala_archivos_06` y `ala_formaciones_06`. Reconocer continuidad física no obliga a abrir el atajo.

### 5.2 Evaluador semántico propuesto

`INSUFICIENTE`: faltan hitos centrales.

`SUFICIENTE`: `NUDO_INTERPRETADO + DOS_ALAS_ARQUITECTURA + PATRON_RAMA`.

`CONCLUYENTE`: `SUFICIENTE` más una corroboración fuerte adicional. Esa corroboración puede ser exploratoria, como `CONEXION_SUPERFICIE`, o provenir de la confirmación central asociada a la resolución terminal del Custodio.

Esta regla debe auditarse. Su objetivo es permitir rutas distintas sin transformar la exploración completa en obligación.

### 5.3 Reconciliación inmediata

Cada primera evidencia nueva debe ejecutar en la misma acción: `registrarEvidenciaPrimeraAla(...) → evaluarEvidenciaPrimeraAla() → reconciliarProgresionArc1()`. No debe requerirse cambiar de sala, guardar/cargar ni ejecutar otro comando.

## 6. Los seis atajos

Durante M12 pueden abrirse individualmente **desde Primera Ala** si el jugador los descubre. Cada `gates.ATAJO_ALA_*` es su única fuente de verdad.

Reglas: no son requisito de M12; no son requisito del gate LIII→LIV; no se abren automáticamente al cerrar M12; un atajo abierto permanece abierto; uno no descubierto permanece sellado.

## 7. Custodio de las Dos Alas

T288 congela dos rutas válidas: `COMBATE` y `PROTOCOLO`. Ninguna es superior.

Persistencia única propuesta: `flags.arc1.custodioDosAlas = NO_RESUELTO | DERROTADO | RESUELTO_POR_PROTOCOLO`. No duplicar esta decisión con booleans paralelos.

### 7.1 Combate

Derrotarlo produce `DERROTADO`. Huir, morir o abandonar no resuelve la misión; puede reintentarse mientras siga `NO_RESUELTO`. No entrega llave/reliquia y no debe haber recompensa narrativa exclusiva superior por escoger combate.

### 7.2 Protocolo

Se puede reconstruir con `M11=HECHA + evidenciaPrimeraAla>=SUFICIENTE`. No exige 6 atajos, 14 secretos, único ecológico ni Afinidad alta. Resultado: `RESUELTO_POR_PROTOCOLO`.

Fuentes históricas hablan de controles laterales, pero la topología 329 congelada no contiene rooms `ala_control_este/oeste`; **no crear rooms nuevas**. El mecanismo exacto debe resolverse usando scenery/interacciones dentro de la topología actual.

### 7.3 Localización

`ala_camara_dos_alas` es el candidato técnico fuerte para el encuentro. Clasificación: `ELECCION_TECNICA_RESPALDADA_POR_FUENTE_A_AUDITAR`.

No reutilizar Sombra/Centinela/reliquias verticales como llaves de M12.

## 8. Cómo llega la red a CONCLUYENTE

Hay dos recorridos compatibles:

- **Exploratorio:** evidencia `SUFICIENTE` + corroboración fuerte adicional → `CONCLUYENTE`.
- **Central:** evidencia `SUFICIENTE` + Custodio terminal + confirmación central de mecanismos/información → `CONCLUYENTE`.

Así el protocolo puede estar disponible desde `SUFICIENTE`, pero M12 no cierra hasta que la conclusión de red quede confirmada.

## 9. Cierre de M12

Condición reconciliada: `evidenciaPrimeraAla.nivel == CONCLUYENTE` y `custodioDosAlas` en `{DERROTADO, RESUELTO_POR_PROTOCOLO}`.

Produce one-shot: `M12=HECHA`, `R5=CONFIRMADO`, Comprensión `+1` con fuente `ARC1_M12_RED_PRIMERA_ALA`, conocimiento de Primera Ala confirmado, `ala_umbral_mantenimiento` conocido y autorización institucional profunda válida.

`PRIMERA_ALA_INVESTIGACION` permanece activa. `PASO_MANTENIMIENTO` permanece cerrado.

Recompensas cualitativas: Comprensión +1; Mérito importante; Contribución sí; prestigio institucional significativo. Los valores numéricos quedan `PENDIENTE_BALANCE_3C7`.

## 10. Autorización institucional

T257 registra como efecto del cierre `autorizacionInvestigacionProfunda`; T288 mantiene una autorización institucional como parte del gate. REV1 reconcilia ambos conceptos mediante `flags.arc1.permisos.AUTORIZACION_INVESTIGACION_PROFUNDA=true` al formalizar el cierre de M12.

Metadatos conceptuales: fuente `INSTITUCIONAL`, origen `M12_CIERRE_FORMAL`, vigencia al menos hasta superar LIII→LIV. No se inventa un NPC concreto como emisor mientras una fuente de autoridad no lo congele.

## 11. Dos Alas: no crear un estado redundante

M11 REV2 ya persiste `flags.arc1.sintesis.DOS_ALAS=PRINCIPIO` y R3 confirmado al cierre. T288, más tardío, expresa el gate mediante `M11 HECHA + R3 CONFIRMADO`, no exige persistir un segundo estado `COMPRENDIDAS`.

Por lo tanto REV1 **no crea** `DOS_ALAS=COMPRENDIDAS`. Si UI/diagnóstico necesita la frase «Dos Alas comprendidas», se deriva de `M11=HECHA && R3=CONFIRMADO && sintesis.DOS_ALAS=PRINCIPIO`.

## 12. Gate LIII→LIV — fórmula de autoridad más reciente

T288 congela la transición como: `qi>=75 + M11 HECHA + M12 HECHA + R3 CONFIRMADO + R5 CONFIRMADO + autorización institucional correspondiente`.

Al superarla: `player.etapa=4`, `arc1.estado=LIV_REVELACION` y M13 queda `DISPONIBLE` de forma derivada. No cambia el rango institucional.

En un estado válido se esperan los invariantes: `M11 HECHA ⇒ R3 CONFIRMADO`; `M12 HECHA ⇒ R5 CONFIRMADO`; `M12 HECHA ⇒ evidenciaPrimeraAla=CONCLUYENTE`; `M12 HECHA ⇒ Custodio terminal`; `M12 HECHA ⇒ AUTORIZACION_INVESTIGACION_PROFUNDA=true`.

## 13. Sustitución del legacy de cultivo

ver74 y el candidato ver75 todavía conservan `PUERTAS[4] = { pildoras: 2, logros: ["comprension:6"] }`. 3C.7 debe retirar/neutralizar esa condición para la etapa 3→4.

La transición LIII→LIV no exige ni consume dos píldoras de consolidación y no exige `comprension:6`. El contrato narrativo anterior debe ser la única puerta. Debe evaluarse antes de cualquier mutación irreversible y no debe quedar una doble validación legacy + Arc1.

La implementación futura debe preservar la semántica de consagración que resulte aprobada al cerrar la reauditoría de 3C.6.

## 14. Modelo uniforme de permisos

M08–M11 REV2 usa permisos booleanos, mientras Fase1 exige cerrar fuente/origen/vigencia. Para M12 son semánticamente distintos `PRIMERA_ALA_INVESTIGACION` y `AUTORIZACION_INVESTIGACION_PROFUNDA`.

Antes del contrato debe elegirse un modelo uniforme: boolean + metadatos separados, o objeto estructurado `{activo, fuente, origen, vigencia}`. No mezclar ambos modelos en el mismo save.

## 15. Anclajes

Propuesta mínima: He Zhen puede anclarse temporalmente en `formaciones_sello_antiguo` hasta activar M12. Wen Tao y Song Rui no reciben anclajes obligatorios inventados. El Custodio es entidad de misión, no NPC social de 3C.5.

## 16. Legacy que no debe regresar

No usar como requisito de M12: `reliquias_verticales`, Sombra/Centinela como llaves, 6/6 atajos, únicos ecológicos, Afinidad alta, todos los secretos ni todas las rooms.

## 17. Pendientes antes de contrato

1. Auditar el mapping técnico concreto de `PATRON_RAMA`.
2. Auditar cómo materializar el protocolo del Custodio sin crear rooms nuevas.
3. Auditar la localización del Custodio en `ala_camara_dos_alas`.
4. Fijar el modelo uniforme de permisos.
5. Fijar balance numérico de M12.
6. Congelar el runtime predecesor sólo cuando 3C.6 supere su reauditoría.
7. No implementar M13 todavía.

## Estado final

`3C7A_M12_GATE_LIII_LIV_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`

**NO IMPLEMENTAR TODAVÍA.**
