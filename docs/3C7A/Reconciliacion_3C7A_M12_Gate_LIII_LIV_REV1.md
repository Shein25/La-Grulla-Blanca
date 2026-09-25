# Reconciliación 3C.7A — M12 + gate LIII→LIV — REV1

**Fecha:** 2026-09-25  
**Estado:** `LISTA_PARA_AUDITORIA_DOCUMENTAL_CON_DECISION_HUMANA_PENDIENTE`  
**Alcance:** M12, evidencia de Primera Ala, Custodio de Dos Alas y gate de cultivo LIII→LIV.  
**No incluye:** implementación, M13 completo, M14+, M16+, balance numérico final.

## 1. Autoridad y frontera

Jerarquía aplicada:

1. decisiones humanas posteriores explícitas;
2. Auditoría 6 canónica;
3. Auditoría 6 estructurada cuando sea legible;
4. Fase1 REV2 como recuperación derivada;
5. ver74/3C.5 sólo para infraestructura real;
6. topología 329 congelada.

La fórmula de gate recuperada por Fase1 REV2 es:

```text
qi >= 75
+ DosAlas == COMPRENDIDAS
+ redPrimeraAla == CONCLUYENTE
+ autorización institucional
```

Fase1 REV2 además congela que el gate **NO exige**:

- 6/6 atajos;
- todos los únicos ecológicos;
- todas las rooms de Primera Ala.

La fuente primaria completa del párrafo exacto del gate no está íntegramente disponible en el recorte de Auditoría 6 almacenado en esta rama; por eso esta fórmula debe ser revalidada por auditoría externa antes del contrato.

## 2. Tres gates distintos

No mezclar:

### A. `GATES_329.M12`

Extremos existentes en ver74:

```text
formaciones_sello_antiguo
↕
formaciones_descenso_tecnico
```

Función: acceso oficial a Primera Ala durante M12.

### B. Gate de cultivo LIII→LIV

No es gate topológico. Es la condición para pasar:

```text
LianQi etapa 3 (Consolidación)
→
LianQi etapa 4 (Refinamiento)
```

Debe sustituir el legacy:

```text
PUERTAS[4] = { pildoras: 2, logros: ["comprension:6"] }
```

### C. `GATES_329.PASO_MANTENIMIENTO`

Extremos:

```text
ala_umbral_mantenimiento
↕
mantenimiento_acceso
```

Debe permanecer `false` durante M12. M12 permite conocer/ver `ala_umbral_mantenimiento`, pero no descender. Su apertura pertenece a M13.

## 3. Ruta oficial M12

Rooms literales confirmadas por Auditoría 6/Fase1 y existentes en ver74:

```text
formaciones_sello_antiguo
→ formaciones_descenso_tecnico
→ ala_vestibulo
→ ala_nudo_seis_corrientes
→ ala_camara_dos_alas
```

También pertenece al recorrido de M12:

```text
ala_umbral_mantenimiento
```

La entrada oficial **no es ninguno de los seis `ATAJO_ALA_*`**.

Los atajos pueden permanecer cerrados durante toda M12 y no son requisito de cierre ni del gate LIII→LIV.

## 4. Activación y permiso de M12

Requiere:

```text
M11=HECHA
arc1.estado=LIII_INVESTIGACION
```

Propuesta técnica:

```text
HABLAR he_zhen
@ formaciones_sello_antiguo
```

produce:

```text
M12=ACTIVA
flags.arc1.permisos.PRIMERA_ALA_INVESTIGACION=true
gates.M12=true
```

Clasificación de la room y el gate: `CANON_FUERTE_RESPALDADO_TOPOLOGIA`.

Clasificación de `HABLAR he_zhen` como disparador exacto: `ELECCION_TECNICA_3C7_AUDITAR`.

### Vigencia del permiso

`PRIMERA_ALA_INVESTIGACION` **no expira al cerrar M12**.

Motivo de reconciliación: M12 puede cerrar con evidencia SUFICIENTE, mientras el gate LIII→LIV exige CONCLUYENTE. El jugador necesita poder continuar investigando sin soft-lock.

No confundir este permiso con la autorización institucional del gate LIII→LIV; esa equivalencia no está demostrada.

## 5. Estado persistente propuesto

Extender `flags.arc1`:

```text
evidenciaPrimeraAla:
  nivel: INSUFICIENTE | SUFICIENTE | CONCLUYENTE
  tipos: Set lógico / array normalizado de tipos únicos
  ramasFuncionales: conjunto de familias de rama
  fuentes: claves room.scenery ya registradas

custodioPrimeraAla:
  estado: NO_RESUELTO | COMBATE | PROTOCOLO

sintesis:
  DOS_ALAS: DESCONOCIDO | PRINCIPIO | COMPRENDIDAS
  SEGUNDA_RAMA: DESCONOCIDO | APLICACION_CORPORAL

permisos:
  PRIMERA_ALA_INVESTIGACION: boolean
```

No crear claves top-level.

## 6. Evaluador semántico de evidencia

### 6.1 Principio

M12 no será:

```text
"visita X/41 rooms"
"abre 6/6 atajos"
"encuentra 14 secretos"
```

La evidencia se registra por significado y por fuente única `room.scenery`.

### 6.2 Tipos de evidencia

#### A. `ARQUITECTURA_RED`

Fuente principal:

```text
ala_nudo_seis_corrientes
```

Scenery candidato: `seis_rutas`, `anillo`, `marcas` o `centro`.

Significado: existe una red deliberada que distribuye funciones.

#### B. `PRINCIPIO_DOS_ALAS`

Fuente principal:

```text
ala_camara_dos_alas
```

Scenery candidato: `trazado_izquierdo`, `trazado_derecho`, `centro` o `inscripciones`.

Significado: dos sistemas diferentes coexisten y se relacionan sin fusionarse.

#### C. `RAMA_FUNCIONAL`

Se registra por familia, no por cantidad de rooms.

Familias:

```text
MEDICINA
JARDINES
CANTERA
AGUAS
ARCHIVOS
FORMACIONES
```

Una familia cuenta cuando se examina evidencia que revele su función dentro de la red, no sólo por entrar a una room.

#### D. `PATRON_COMPARTIDO`

Se obtiene al contar con evidencia significativa de **al menos dos familias distintas** y reconocer elementos estructurales repetidos/compatibles.

Esto es una `ELECCION_TECNICA_3C7_AUDITAR`, no un número canónico heredado.

#### E. `CONTINUIDAD_MODERNA`

Evidencia fuerte opcional para elevar el nivel a CONCLUYENTE.

Fuentes técnicas idóneas: terminales de rama que muestran continuidad física hacia infraestructura moderna, sin cruzar el atajo:

```text
ala_med_06
ala_jardines_06
ala_cantera_06
ala_aguas_06
ala_archivos_06
ala_formaciones_06
```

Sólo se necesita **una** continuidad moderna independiente; no 6/6.

Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`.

### 6.3 Niveles propuestos

```text
INSUFICIENTE
si falta cualquiera de:
- ARQUITECTURA_RED
- PRINCIPIO_DOS_ALAS
- al menos una RAMA_FUNCIONAL
- PATRON_COMPARTIDO
```

```text
SUFICIENTE
si existen:
ARQUITECTURA_RED
+ PRINCIPIO_DOS_ALAS
+ >=1 RAMA_FUNCIONAL
+ PATRON_COMPARTIDO
```

```text
CONCLUYENTE
si:
SUFICIENTE
+ CONTINUIDAD_MODERNA
```

Esta regla permite cerrar M12 sin exigir recorrer todo el área y permite continuar hasta CONCLUYENTE sin soft-lock.

## 7. Cierre de M12

Fuente recuperada:

```text
evidencia suficiente
+ Custodio resuelto por COMBATE o PROTOCOLO
```

Cierre propuesto:

```text
evidenciaPrimeraAla.nivel >= SUFICIENTE
AND
custodioPrimeraAla.estado in {COMBATE, PROTOCOLO}
```

Produce one-shot:

```text
M12=HECHA
flags.arc1.revelaciones.R5=CONFIRMADO
Comprensión +1
clave one-shot = ARC1_M12_RED_PRIMERA_ALA
ala_umbral_mantenimiento = conocido
PRIMERA_ALA_INVESTIGACION permanece true
PASO_MANTENIMIENTO permanece false
```

Recompensas cualitativas preservadas:

- Comprensión: +1;
- Mérito: importante;
- Contribución: sí;
- prestigio institucional: significativo;
- números: `PENDIENTE_BALANCE_3C7`.

## 8. DOS_ALAS: PRINCIPIO → COMPRENDIDAS

M11 deja:

```text
flags.arc1.sintesis.DOS_ALAS=PRINCIPIO
```

Propuesta técnica de reconciliación:

```text
al cerrar M12
→ flags.arc1.sintesis.DOS_ALAS=COMPRENDIDAS
```

Razonamiento: M11 reconstruye intelectualmente el principio; M12 lo valida físicamente en la arquitectura.

No crear otro flag `DosAlasComprendidas`.

Clasificación: `ELECCION_TECNICA_3C7_AUDITAR`.

## 9. Custodio de Dos Alas

ver74 no contiene un NPC/mob literal llamado Custodio de Dos Alas. No reutilizar como canon Sombra/Centinela/reliquias verticales.

### Localización propuesta

```text
ala_camara_dos_alas
```

Clasificación: `ELECCION_TECNICA_RESPALDADA_VER74_AUDITAR`.

### Estado

```text
NO_RESUELTO
COMBATE
PROTOCOLO
```

COMBATE y PROTOCOLO son equivalentes para el cierre. Ninguno concede una recompensa narrativa superior.

### Rama COMBATE

- atacar y derrotar al Custodio → `COMBATE`;
- huir, morir o abandonar no cierra la misión;
- debe poder reintentarse;
- no debe producir loot/recompensa repetible explotable;
- resuelto una vez, no reaparece.

### Rama PROTOCOLO

Disponible sólo cuando:

```text
M11=HECHA
evidenciaPrimeraAla.nivel >= SUFICIENTE
```

No exige:

- 6 atajos;
- secretos opcionales;
- único ecológico;
- afinidad alta;
- todos los rooms.

Interacción exacta propuesta: acción contextual/HABLAR con el Custodio. El verbo exacto queda `ELECCION_TECNICA_3C7_AUDITAR`.

### Aparición

Propuesta mínima: materializar al Custodio en `ala_camara_dos_alas` mientras M12 esté ACTIVA y `custodioPrimeraAla.estado=NO_RESUELTO`.

No convertirlo en un errante global ni alterar territorios NPC de 3C.5.

## 10. Continuación SUFICIENTE → CONCLUYENTE

Cerrar M12 **no congela** `evidenciaPrimeraAla`.

Si el jugador cerró M12 en SUFICIENTE:

```text
M12=HECHA
PRIMERA_ALA_INVESTIGACION=true
gates.M12=true
```

puede regresar a Primera Ala y obtener `CONTINUIDAD_MODERNA`.

En el mismo evento que registra la nueva evidencia:

```text
evaluarEvidenciaPrimeraAla()
→ nivel=CONCLUYENTE
```

No requiere reabrir M12 ni repetir Custodio/recompensas.

## 11. Gate LIII→LIV

### 11.1 Condiciones

Contrato a auditar:

```text
player.qi >= 75
flags.arc1.sintesis.DOS_ALAS == COMPRENDIDAS
flags.arc1.evidenciaPrimeraAla.nivel == CONCLUYENTE
autorización institucional == válida
```

No exige M12=ACTIVA; en flujo normal M12 ya estará HECHA por las dos condiciones narrativas anteriores.

### 11.2 Sustitución del legacy

En 3C.7, la etapa 3→4 no debe exigir ni consumir:

```text
2 píldoras de consolidación
comprensión:6
```

La implementación futura deberá sustituir la lógica legacy de `PUERTAS[4]` por el contrato anterior o neutralizar sus campos legacy (`pildoras=0`, sin `comprension:6`) y evaluar las condiciones Arc1 explícitamente.

No debe quedar una doble puerta accidental.

### 11.3 Consagración

El gate se evalúa antes de cualquier consumo/mutación irreversible.

Al superar la etapa:

```text
arc1.estado = LIV_REVELACION
player.etapa = 4
qi_max = 110
```

Debe conservarse la semántica de 3C.6 aprobada para la consagración, incluida la preservación del qi existente antes de ampliar el vaso, si esa semántica supera la auditoría actual de 3C.6.

## 12. Autorización institucional — PENDIENTE

No se congela una fuente inventada.

Opciones compatibles a auditar:

### Opción A

`PRIMERA_ALA_INVESTIGACION` satisface también la autorización institucional del gate.

Ventaja: estado mínimo.

Riesgo: confundir permiso para investigar con permiso para avanzar institucionalmente.

### Opción B

Después de M12/CONCLUYENTE, una revisión institucional crea un permiso separado, por ejemplo:

```text
AUTORIZACION_LIV=true
```

La fuente/NPC exactos deben estar respaldados antes de congelarse.

### Opción C

La autorización se deriva de otro estado institucional ya existente, si una fuente de autoridad lo demuestra.

**Estado REV1:** `DECISION_HUMANA_PENDIENTE_O_FUENTE_POR_RECUPERAR`.

## 13. Anclajes M12

No se inventan anclajes nuevos para Song Rui/Wen Tao.

Propuesta técnica mínima:

- He Zhen puede anclarse temporalmente en `formaciones_sello_antiguo` sólo hasta activar/abrir M12;
- después se libera a territorio válido;
- el Custodio es entidad de misión, no NPC social de 3C.5.

Todo anclaje debe ser one-shot/idempotente.

## 14. Legacy que no debe regresar

No usar como requisito M12:

- `reliquias_verticales`;
- Sombra/Centinela como llaves;
- seis atajos abiertos;
- únicos ecológicos;
- afinidad alta;
- todos los secretos;
- todas las rooms.

## 15. Pendientes antes de contrato

1. revalidar externamente la fórmula literal del gate LIII→LIV;
2. auditar el evaluador semántico propuesto y sus umbrales;
3. auditar `DOS_ALAS PRINCIPIO→COMPRENDIDAS` al cierre M12;
4. auditar localización/contrato del Custodio;
5. decidir/recuperar fuente exacta de autorización institucional;
6. fijar balance numérico M12;
7. congelar runtime predecesor sólo cuando 3C.6 supere su reauditoría;
8. no implementar M13 todavía.

## Estado final

`3C7A_M12_GATE_LIII_LIV_REV1_LISTA_PARA_AUDITORIA_DOCUMENTAL`

**NO IMPLEMENTAR TODAVÍA.**
