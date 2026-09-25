# Fuente Maestra ver55 — extracto literal T288 · M12 + gate LIII→LIV

**Origen:** `La_Grulla_Blanca_Fuente_Maestra_Fusionada_ver55(2).md`
**Turno:** T288
**Fecha UTC del turno:** 2026-09-20T07:49:52.893Z
**Carácter:** EXTRACTO LITERAL PARA AUDITORÍA. No es una reconciliación ni sustituye el archivo fuente completo.
**Rango recuperado de la copia de fuente:** líneas 172890–173154.

---
## M12 · La red que nadie dibuja

M12 es la primera gran incursión histórica del arco.

Su acceso oficial está ya conceptualmente congelado:

```text
formaciones_sello_antiguo
        ↓
formaciones_descenso_tecnico
        ↓
ala_vestibulo
```

Este acceso **no es uno de los seis atajos**.

Los atajos son conexiones laterales que pueden abrirse desde abajo. La entrada oficial existe independientemente de ellos.

Al iniciar M12 se concede:

```text
PRIMERA_ALA_INVESTIGACION
```

y se abre el sello antiguo mediante procedimiento institucional, no porque el jugador haya encontrado una llave secreta.

### Primera impresión

La Primera Ala no debería aparecer como:

> mazmorra maldita abandonada.

Debe sentirse como una instalación grande que fue desocupada, sellada y parcialmente olvidada.

El `ala_vestibulo` conduce al `ala_nudo_seis_corrientes`, y allí ocurre la primera gran demostración espacial:

> **seis ramas salen del mismo centro.**

No necesitamos decir:

> «¡Son seis sectores de una única red!»

Todavía.

El jugador debe comprobarlo.

### Reconstrucción

La misión exige evidencia suficiente de arquitectura compartida.

No:

```text
MEDICINA 1/6
JARDINES 2/6
...
```

Podemos usar `evaluarEvidenciaPrimeraAla()` con:

```text
INSUFICIENTE
SUFICIENTE
CONCLUYENTE
```

Un recorrido principal obligatorio muestra varias cosas suficientes: el nudo central, Cámara de Dos Alas, al menos una rama funcional y señales de que las demás utilizan el mismo diseño.

Explorar ramas adicionales enriquece la evidencia y puede llevar a `CONCLUYENTE`, secretos y atajos.

Pero:

> **M12 nunca exige 6/6.**

### Los atajos

Al explorar desde abajo, el jugador puede abrir cualquiera de los seis atajos que ya definimos.

Cada uno tiene una única fuente de verdad:

```text
SELLADO
ABIERTO
```

No almacenamos “abierto desde arriba” y “abierto desde abajo”.

Y no se abren automáticamente al completar M12.

Si encontraste uno y lo abriste:

> queda abierto.

Si no:

> sigue sellado.

Esto hará que Primera Ala siga ofreciendo exploración después de la misión principal.

### Cámara de Dos Alas

`ala_camara_dos_alas` debe ser uno de los puntos principales.

Aquí la arquitectura demuestra físicamente lo aprendido en M11.

No repite la explicación con otro pergamino.

Se puede observar que los sistemas se organizaban alrededor de dos funciones complementarias:

> estabilizar/contener;

> transferir/presionar.

El jugador reconoce el patrón porque ya hizo M11.

Sin M11 no estaría autorizado a estar aquí en la ruta principal.

### Primera gran conclusión

Después de suficiente recorrido:

```text
R5 = CONFIRMADO
```

La verdad:

> Medicina antigua, Jardines, Cantera, Aguas, Archivos y Formaciones no eran seis proyectos separados.

Eran:

> **seis ramas de una misma infraestructura: Primera Ala.**

Aquí concede:

```text
Comprensión +1
fuente = ARC1_M12_RED_PRIMERA_ALA
```

porque nuevamente existe una síntesis real.

### El Custodio de Dos Alas

La salida principal de la investigación queda bloqueada por el Custodio.

No porque sea “el boss final de la dungeon”, sino porque su función antigua todavía protege el límite entre la red operativa y áreas de mantenimiento más profundas.

Su encuentro utiliza las dos posturas que ya diseñamos:

```text
ALA_DE_CONTENCION
ALA_DE_PRESION
```

y puede resolverse de dos maneras.

**Combate:** superar su sistema defensivo.

**Protocolo:** reconstruir una orden válida usando Dos Alas + evidencia suficiente de Primera Ala.

La ruta de protocolo debe poder reconstruirse con:

```text
M11 completada
+
evidencia principal suficiente de M12
```

No requiere:

```text
6 atajos
14 secretos
único ecológico
Afinidad alta
```

Eso queda contractual.

Ambas resoluciones terminan en un estado semántico:

```text
Custodio = DERROTADO
```

o:

```text
Custodio = RESUELTO_POR_PROTOCOLO
```

y ambas permiten concluir M12.

Ninguna entrega mejor premio.

### El umbral de Mantenimiento

Tras resolver al Custodio, el jugador llega hasta:

```text
ala_umbral_mantenimiento
```

y descubre que la instalación continúa hacia abajo.

Pero todavía no tiene autorización ni contexto para descender.

El umbral queda **visible**.

No accesible.

Eso es importante porque M13 empieza con una pregunta concreta:

> si Primera Ala fue abandonada, ¿por qué existe todavía un nivel de mantenimiento debajo de ella?

M12 termina aquí.

No debemos permitir que un explorador entusiasmado se meta en Mantenimiento antes de que M13 pueda darle significado.

## Cierre de M12

Al regresar o formalizar el hallazgo:

```text
M12 = HECHA
R5 = CONFIRMADO
Custodio = terminal
LIII gate = satisfecho narrativamente
ala_umbral_mantenimiento = conocido
```

Da Mérito importante y reconocimiento institucional.

No da piedras, técnica legendaria ni uniforme.

El jugador ha hecho algo mucho más significativo:

> ha demostrado que una parte de la historia material de la secta estaba mal entendida.

## Gate LIII → LIV

La transición queda:

```text
vaso LIII = 75
+
M11 HECHA
+
M12 HECHA
+
R3 CONFIRMADO
+
R5 CONFIRMADO
+
autorización institucional correspondiente
```

Cuando se consagra/avanza:

```text
LianQi III → LianQi IV
arc1.estado = LIV_REVELACION
M13 = DISPONIBLE
```
