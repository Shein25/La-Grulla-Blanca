# CIERRE 3C.6A — REV3.1

**Fecha:** 2026-09-24  
**Estado:** `CERRADA_DOCUMENTALMENTE_APTA_PARA_CONTRATO`

## 1. Veredicto externo

La auditoría final independiente de Claude concluyó:

`3C6A_REV3_1_APTA_PARA_CONTRATO`

HEAD efectivamente auditado:

`3a9f9e59cf7b84a346de52ffda2b332055177216`

No se detectaron bloqueantes, regresiones nuevas ni soft-locks documentales de severidad media/alta.

N-01…N-09 quedaron RESUELTOS y N-10 RESUELTO_DOCUMENTALMENTE.

La auditoría completa queda preservada en:

`docs/3C6A/Auditoria_Final_3C6A_REV3_1_CLAUDE.md`

## 2. Fuente canónica REV3.1

La fuente de verdad documental para el futuro contrato es la versión del repositorio, no el artefacto local adjuntado en chat cuando difieran byte a byte:

- `docs/3C6A/Reconciliacion_3C6A_Prologo_M01_M07_REV3_1.md`
- `docs/3C6A/Matriz_Implementacion_3C6A_Prologo_M01_M07_REV3_1.json`

SHA-256 canónico del JSON del HEAD auditado:

`96d6a73383fdd5636005460bd3483f3e6b7f8f358a5354fdaa1f76cab0e3d881`

El paquete de auditoría fue corregido para declarar este hash canónico.

## 3. Aclaración contractual N-05

Sin modificar los artefactos ya auditados, se congela para el contrato:

> Cada vez que se registra por primera vez un nuevo tipo en `flags.arc1.evidenciaTerritorial.tipos`, debe invocarse inmediatamente `reconciliarProgresionArc1()`.

Consecuencia:

- si M04 y M05 ya están HECHAS;
- M06 todavía no está activa/hecha;
- y la nueva evidencia hace que exista al menos un tipo registrado;

M06 se activa en esa misma acción, sin requerir save/load, CONSAGRAR ni cerrar otra misión.

Esta aclaración cierra el único matiz menor señalado por la auditoría final.

## 4. Verificación adicional de las ocho fuentes M06

Tras la auditoría de Claude se comprobó el `grulla-blanca_ver74.html` completo.

Las ocho parejas room/scenery especificadas existen literalmente:

### DESPLAZAMIENTO_FAUNA

- `bosque_collado_alto.huellas`
- `aguas_poza_profunda.marcas`

### ALTERACION_VEGETAL

- `aguas_senda_bosque.vegetacion`
- `terraza_cantera.vegetacion`

### ALTERACION_HIDRICA

- `aguas_cauce_alto.corriente`
- `aguas_paso_piedras.corriente`

### PATRON_TERRITORIAL

- `bosque_puesto_marcas.tablillas`
- `bosque_refugio_patrulla.registro`

Por tanto, la tabla de M06 puede implementarse exactamente como REV3.1 la define: 4 tipos y 2 fuentes independientes por tipo. No hace falta sustituir ninguna fuente.

## 5. Cambios obligatorios que pasan al contrato

El contrato de implementación debe incluir expresamente:

1. `SAVE_SCHEMA_VERSION` permanece en 2.
2. Migración discriminada de saves ver74.
3. `normalizarArc1()` + `reconciliarProgresionArc1()` fail-closed.
4. Reconciliación inmediata al registrar evidencia nueva.
5. Separación real Contribución/Mérito.
6. `normalizarFacciones()` deja de forzar `miembro` y `merito>=saldo`.
7. Nueva vía `otorgarMerito()` y separación del historial económico.
8. Inicialización de facción económica como `inactivo`; M03 la pasa a `miembro`.
9. Wrapper local de `rata_despensa` M02.
10. Instancia derivada/recreable de `muneco_practica` M03.
11. Hook M03 de MEDITAR antes de la rama de vaso lleno/CONSAGRAR.
12. Anclajes NPC de misión con owner y liberación/reubicación atómica.
13. Checkpoints M04/M05 basados en eventos, no en `visitadas` históricas.
14. Protección y única reemisión de la Píldora de Consolidación.
15. Tabla externa M06 de 8 fuentes verificadas.
16. M07 determinista y conocimiento NPC monotónico.
17. `compruebaPuerta()` fail-closed y sin consumo previo ante requisito desconocido.
18. CONSAGRAR deja de restar el vaso anterior al qi.
19. Reemplazar el stub `gestionarMisionesNpc()` por plumbing P–M07.
20. Actualizar tests legacy que exigían `QUESTS={}` o `merito>=saldo`.
21. No modificar `ROOMS.exits`, cantidad/identidad global de errantes ni 3C.4 global.

## 6. Invariantes congelados

La implementación debe conservar:

- 329 rooms;
- 17 áreas;
- 787 exits dirigidos;
- 0 reciprocidades rotas;
- 0 aisladas;
- 1 componente físico;
- `SECTA_INTERIOR=false => M12=false => ATAJO_ALA_*=false`;
- sin tiempo diegético;
- schema 2.

## 7. Próximo entregable

`Contrato_Implementacion_3C6_Prologo_M01_M07.md`

3C.6A queda cerrada documentalmente. No requiere otra ronda de decisiones humanas antes de redactar el contrato.
