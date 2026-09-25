# Fuente Maestra ver55 — extracto literal T289 · M13–M15

**Origen:** `La_Grulla_Blanca_Fuente_Maestra_Fusionada_ver55(2).md`
**Turno:** T289
**Fecha UTC del turno:** 2026-09-20T07:53:01.000Z
**Carácter:** EXTRACTO LITERAL PARA AUDITORÍA. No es reconciliación ni sustituye la fuente completa.
**Rango recuperado:** líneas 173194–173943.

---
- Fecha UTC: `2026-09-20T07:53:01.000Z`.
- Estado devuelto por la fuente: `completed`.

#### T289.1 — Usuario

ID: `bdcf62bf-91af-411f-a07a-4fadb1623977` · SHA-256 del texto recuperado: `960a6a2f19732c93887afeeff32f5eb63332c855e2ffd634402852bb27f49b65`.

<!-- BEGIN-RECOVERED-TEXT T289-01 -->
````markdown
Continua
````
<!-- END-RECOVERED-TEXT T289-01 -->

#### T289.2 — Asistente original

ID: `7458744c-8152-4eeb-b008-934455596081` · SHA-256 del texto recuperado: `2ce2652b6a220768c33cf2fa43544aded71b2fa183b224450b0c0687a92388ac`.

<!-- BEGIN-RECOVERED-TEXT T289-02 -->
````markdown
Perfecto. Continuemos con **M13–M15**, donde el arco cambia de naturaleza. Hasta M12 la pregunta era «¿qué fue Primera Ala?». Desde ahora la pregunta pasa a ser:

> **Si era una instalación abandonada, ¿por qué continúa funcionando y quién sigue pagando su coste?**

Aquí conviene romper claramente con el recorrido viejo de ver55. La versión actual todavía hace avanzar el tramo profundo reuniendo reliquias de guardianes y derrotando entidades para abrir la cumbre. :chatgpt-content-reference{index="0"} En el Arc1 nuevo, el acceso profundo nace de **investigación, autorización y evidencia**, no de llevar dos objetos-llave.

# M13 · Todo consume algo

M12 termina frente a `ala_umbral_mantenimiento`. El jugador ya sabe que Primera Ala era una red única, pero todavía puede pensar que está observando una ruina inactiva.

M13 destruye esa idea.

La misión comienza cuando Duan Shibo y He Zhen reciben el informe de Primera Ala. Lo extraño no es solamente que exista un nivel de mantenimiento debajo, sino que ciertos registros actuales de Producción contienen consumos que nunca pudieron asignarse a una instalación moderna.

El permiso de misión puede ser:

```text
MANTENIMIENTO_INVESTIGACION
```

de fuente institucional, limitado a los corredores necesarios. No concede Núcleo.

La estructura de M13 queda:

```text
MANTENIMIENTO
→ CONSUMOS_ANTIGUOS
→ COMPARACION_MODERNA
→ CONCLUSION
```

## Descenso

El jugador atraviesa por primera vez:

```text
ala_umbral_mantenimiento
↓
mantenimiento_acceso
```

y descubre un entorno completamente distinto de Primera Ala.

Arriba había arquitectura de investigación.

Aquí hay:

> conductos;
> depósitos;
> válvulas;
> herramientas;
> dormitorios de turno;
> registros de reparación;
> zonas donde alguien tenía que trabajar cada día.

Esto conecta directamente con los secretos opcionales que diseñamos.

El alojamiento `mantenimiento_dormitorio_turnos` queda disponible si se visita, pero sigue siendo:

```text
seguro = true
purifica = false
```

## La primera evidencia inquietante

No quiero que el primer aparato encontrado tenga una luz roja diciendo:

> RED ACTIVA.

Debe ser más material.

Por ejemplo, una conducción que debería llevar décadas fría está ligeramente templada.

Una bandeja de recolección contiene sedimento reciente.

Un contador mecánico ha avanzado desde la última marca conservada.

El jugador puede pensar inicialmente:

> calor residual;
> filtración;
> movimiento natural.

Después encuentra otra señal.

Y otra.

La conclusión empieza a ser inevitable:

> **algo continúa circulando.**

## No revelar todavía la entidad viva

Aquí tenemos que ser muy disciplinados.

M13 puede demostrar:

```text
energía entra
material se consume
presión se redistribuye
residuos se producen
```

pero no:

```text
“una criatura viva está sosteniendo esto”
```

Eso es R7 y pertenece a M17.

Los mecanismos profundos pueden desaparecer tras conductos que todavía no están autorizados.

## Comparación moderna

La misión exige volver a cruzar la evidencia antigua con el presente.

Duan Shibo y Ma Qiren aportan registros de materiales.

Lu Cheng reconoce especificaciones de piezas que todavía se fabrican ocasionalmente sin que el taller conozca su destino final.

Song Rui puede localizar órdenes antiguas que, generación tras generación, fueron recategorizadas bajo encabezados cada vez más genéricos:

> mantenimiento profundo;
> reserva de infraestructura;
> estabilización inferior.

Nadie necesariamente falsificó la contabilidad.

La función original se perdió mientras el procedimiento sobrevivía.

Ésta es exactamente la clase de decadencia institucional que queremos contar.

## Revelación

Finalmente:

```text
R6 = CONFIRMADO
```

> **Primera Ala no está muerta. La red antigua continúa consumiendo recursos en el presente.**

No sabemos todavía qué sostiene.

No sabemos todavía para qué necesita exactamente esos recursos.

Pero la hipótesis de «ruina histórica» queda descartada.

M13 concede:

```text
Comprensión +1
fuente = ARC1_M13_CONSUMO_ACTUAL
```

porque el personaje integra infraestructura antigua y economía presente en una sola conclusión.

También concede Mérito importante: demostrar que una infraestructura olvidada continúa absorbiendo recursos institucionales es un hallazgo serio.

## La Sombra de Marea Residual

Éste es un buen punto para introducirla, pero **no la haría necesaria para demostrar R6**.

Puede estar en una cámara lateral o atravesar una sección secundaria de Mantenimiento.

Su secuencia:

```text
PULSO
→ CONTRAFLUJO
→ CRECIDA
→ QUIETUD
```

representa circulación residual, no una persona muerta ni una criatura biológica.

Derrotarla o resolverla ayuda a comprender cómo se comportan ciertos flujos antiguos y quizá hace más cómodo explorar una rama.

Pero M13 debe poder completarse sin convertir:

> matar Sombra = demostrar que la red consume.

La evidencia principal es técnica.

---

# M14 · La promesa aplazada

Después de M13 surge una pregunta inevitable:

> Si todavía existe una carga central, ¿qué se suponía originalmente que debía sostener?

Por primera vez el Consejo autoriza un acceso muy limitado al nivel superior del Núcleo:

```text
NUCLEO_SUPERIOR
```

No `NUCLEO_PROFUNDO`.

El recorrido parte de:

```text
mantenimiento_compuerta_nucleo
↓
nucleo_pozo_voto
```

Aquí cambia otra vez la atmósfera.

Mantenimiento era trabajo.

Núcleo Superior es:

> pacto;
> memoria;
> regulación central;
> decisiones fundacionales.

La estructura de M14:

```text
NUCLEO_SUPERIOR
→ VOTO
→ PRIMER_PACTO
→ CONSENTIMIENTO
```

## El Pozo del Voto

No quiero una cinemática fantasmal que muestre la historia completa.

El lugar conserva evidencia suficiente para reconstruir un acto formal entre los primeros cultivadores y la Grulla.

Puede combinar:

> inscripciones;
> posiciones de formación;
> un registro de testigos;
> una memoria incompleta del qi del lugar.

Una de las cosas importantes es que la arquitectura tiene **dos participantes diferenciados**.

No:

> una jaula y algo atrapado dentro.

Sino:

> dos posiciones que debían responderse mutuamente.

Eso ya contradice implícitamente la versión más simple de «los fundadores capturaron una bestia».

## El pacto histórico

La evidencia principal establece que los primeros cultivadores encontraron dos corrientes incompatibles y que la Grulla ya podía reconciliarlas naturalmente.

Los humanos podían construir infraestructura.

La Grulla aportaba un modelo vivo que las formaciones todavía no podían reproducir.

La cooperación permitía estabilizar la montaña.

Y aquí llega R8:

```text
R8 = CONFIRMADO
```

> **La Grulla aceptó participar originalmente.**

Eso debe estar demostrado sin ambigüedad suficiente.

No:

> quizá estuvo de acuerdo.

No:

> alguien dijo siglos después que estuvo de acuerdo.

El jugador encuentra evidencia fundacional suficientemente sólida.

## Pero todavía NO sabemos que debía ser temporal

Este límite es crítico.

El pacto encontrado en M14 puede describir:

> deberes mutuos;
> protección del territorio;
> participación de la Grulla;
> trabajo humano sobre la red.

Pero la parte que establece el relevo **no aparece aquí**.

Quizá el registro principal termina antes.

Quizá el pacto operativo y el plan de sustitución fueron archivados por separado.

Así evitamos que M14 absorba M15.

## Tampoco sabemos que la Grulla actual siga siendo la misma

Otra distinción crítica.

El personaje sabe:

> una Grulla histórica participó voluntariamente.

Todavía no sabe:

> que una Grulla sigue siendo necesaria hoy.

Ni:

> que la misma lleva trescientos años sosteniendo el vínculo.

R7 y R10 permanecen cerrados.

## Comprensión

M14 concede:

```text
Comprensión +1
fuente = ARC1_M14_CONSENTIMIENTO
```

No porque «descubriste un dato», sino porque cambia completamente cómo interpretar la fundación:

> la secta no nació explotando simplemente algo ajeno; nació mediante cooperación.

Eso hará que lo siguiente resulte todavía más incómodo.

---

# M15 · Lo que debía terminar

M14 podría ofrecer una explicación tranquilizadora:

> hubo un pacto voluntario.

M15 impide que esa explicación se convierta en absolución fácil.

Su pregunta es:

> **¿Qué prometieron hacer después?**

La estructura queda:

```text
PROMESA
→ RELEVO
→ APLAZAMIENTOS
→ DEUDA
```

## El Archivo de la Promesa

El recorrido superior del Núcleo incluye:

```text
nucleo_archivo_promesa
```

que sigue siendo accesible con `NUCLEO_SUPERIOR`.

La salida hacia:

```text
nucleo_descenso_pulso
```

permanece cerrada porque exige:

```text
NUCLEO_PROFUNDO
```

que no llegará hasta M17.

Eso nos da un límite físico perfecto.

El jugador puede descubrir toda la promesa histórica sin poder comprobar todavía qué ocurre realmente en el fondo.

## El relevo

Los registros muestran algo muy importante:

> el sistema original no pretendía depender indefinidamente de la participación viva de la Grulla.

Los fundadores esperaban que el conocimiento aprendido mediante Dos Alas permitiera trasladar progresivamente funciones a:

> formaciones;
> operadores;
> regulación distribuida;
> infraestructuras capaces de compartir la carga.

Esto encaja con nuestro secreto opcional `SEC_NUC_02`, pero la existencia de **alguna forma de relevo obligatorio** pertenece a M15 y no puede depender de ese secreto.

El secreto solo puede ampliar cómo imaginaban hacerlo.

Entonces:

```text
R9 = CONFIRMADO
```

> **El vínculo debía ser temporal. Existía una obligación de sustituirlo o relevarlo.**

## Por qué no ocurrió

Aquí quiero evitar por completo:

> «Un anciano malvado decidió esclavizarla para siempre.»

Los registros muestran una cadena.

Primero un prototipo de relevo resultó insuficiente.

Después ocurrió la ruptura de Primera Ala y se perdieron personas/conocimiento.

Una reparación urgente obligó a extender el arreglo existente.

Más tarde otra generación heredó un sistema estable pero incompletamente comprendido.

Luego una orden temporal se convirtió en procedimiento.

Después el procedimiento se convirtió en tradición.

Cada decisión aislada puede resultar defendible.

El conjunto produce una deuda enorme.

No necesitamos inventar guerras, emperadores o catástrofes externas si no forman parte del resto del mundo.

La propia degradación institucional alcanza.

## Tres aplazamientos son suficientes

No haría veinte documentos.

Bastan quizá tres hitos claramente distintos:

| Etapa | Justificación | Problema |
|---|---|---|
| Primer aplazamiento | el relevo técnico todavía no era seguro | razonable |
| Segundo | pérdida de capacidad tras la ruptura | razonable pero ya costoso |
| Tercero | mantener el sistema existente parecía menos peligroso que reconstruirlo | la excepción empieza a normalizarse |

Después, generaciones posteriores ya ni siquiera redactan:

> «aplazamos el relevo».

Simplemente presupuestan:

> mantenimiento.

Ahí está el verdadero golpe.

## La deuda

M15 no concluye:

> los fundadores fueron malos.

Concluye:

> **la institución actual heredó una obligación que dejó de recordar como obligación.**

Eso es mucho más fuerte y más coherente con la tesis del arco.

El jugador acaba de convertirse en miembro de esa misma institución.

Por eso la revelación le pertenece personalmente.

## Comprensión

M15 concede:

```text
Comprensión +1
fuente = ARC1_M15_RELEVO_APLAZADO
```

y es uno de los mejores candidatos para `HISTORY`.

No por haber elegido LIBERAR todavía.

Sino porque el personaje ahora debe decidir cómo interpretar una responsabilidad heredada.

Una posible acción canónica podría registrar la postura que adopta al presentar el hallazgo:

> tratarlo principalmente como deuda;

> tratarlo principalmente como riesgo técnico;

> insistir en que ambas cosas no pueden separarse.

Ninguna determina el final.

Pero sí puede aparecer después en ESPEJO.

---

# Algo muy importante: R8 + R9 no dictan LIBERAR

Después de M15 el jugador sabe:

```text
La Grulla aceptó.
El vínculo debía ser temporal.
El relevo fue aplazado.
```

Sería muy fácil que el autor insinuara:

> entonces LIBERAR es obviamente la opción buena.

No debemos hacerlo.

Todavía faltan hechos decisivos:

```text
¿La red sigue dependiendo realmente de una entidad viva?
¿Puede retirarse ahora sin consecuencias graves?
¿La misma Grulla sigue allí?
¿Cuál es el estado presente del vínculo?
```

M16 mostrará qué ocurre cuando el centro pierde estabilidad.

M17 confirmará R7 y R10.

Solo entonces LIBERAR/CUSTODIAR será una elección informada.

Esto mantiene ambas rutas legítimas.

---

# M15 tampoco abre el Núcleo Profundo

Al final:

```text
nucleo_archivo_promesa
↓
nucleo_descenso_pulso
```

sigue bloqueado.

El jugador sabe que existe algo debajo.

Puede incluso sentir:

> una vibración;
> una presión;
> un pulso.

Pero el acceso responde:

> autorización insuficiente.

No hay ruta ilegal genérica para saltarlo.

`NUCLEO_PROFUNDO` es una decisión institucional extraordinaria que llegará en M17.

---

# El inicio de M16

M15 termina con la investigación aceptada.

No quiero que el personaje cierre el libro y, por abrirlo, provoque mágicamente la crisis.

La red ya venía mostrando tensión desde M07.

M13 demostró que seguía consumiendo.

M14–M15 simplemente ocurrieron mientras esa presión continuaba aumentando.

Poco después de formalizar M15 comienzan a llegar avisos simultáneos:

> una corrección en Formaciones no se estabilizó;

> Medicina reporta circulación irregular;

> Sauces observa alteración del caudal;

> una patrulla informa desplazamiento brusco de fauna.

Entonces:

```text
arc1.estado = LIV_CRISIS
M16 = DISPONIBLE
```

La relación es:

> **la crisis confirma que el problema actual ya no puede seguir tratándose como historia.**

No:

> el jugador rompió el mundo por investigar.

---

# Recompensas M13–M15

El patrón queda bastante limpio:

| Misión | Comprensión | Mérito | Contribución | Acceso |
|---|---:|---|---|---|
| M13 | +1 | importante | moderada | Mantenimiento |
| M14 | +1 | importante | pequeña/moderada | `NUCLEO_SUPERIOR` |
| M15 | +1 | importante | mínima o ninguna | conocimiento/posición institucional |

No quiero que cada una termine también con:

> piedras;
> consumible;
> equipo;
> técnica.

A esta altura del juego las principales recompensas son:

> verdad;
> autoridad;
> responsabilidad.

---

# Qué reemplazamos de ver55

El contenido viejo usa Perla de la Marea + Pluma Celeste como dos respuestas materiales necesarias para abrir el tramo final, obtenidas derrotando Sombra y Centinela. :chatgpt-content-reference{index="1"} También registra directamente esas reliquias al derrotarlos. :chatgpt-content-reference{index="2"}

Ese modelo desaparece.

La Sombra y el Centinela sobreviven como **entidades antiguas con mecánicas propias**, pero:

```text
no sueltan reliquias-llave
no abren la historia por ser derrotados
no funcionan como dos mitades de una cerradura
```

El progreso principal ahora se produce mediante:

```text
investigar
→ comprender
→ informar
→ recibir autorización
→ descender
```

mucho más coherente con el Arc1 que estamos construyendo.

---

Con M13–M15 ya tenemos completa la transición:

```text
PRIMERA ALA ERA UNA RED
        ↓
LA RED SIGUE CONSUMIENDO
        ↓
LA GRULLA ORIGINAL PARTICIPÓ VOLUNTARIAMENTE
        ↓
ESA PARTICIPACIÓN DEBÍA TERMINAR
        ↓
LA INSTITUCIÓN DEJÓ DE TRATAR EL RELEVO COMO UNA DEUDA
```

Y justo ahí comienza **M16 · Cuando falla el centro**, que ya diseñamos en detalle.

Después de M16 solo quedarán dos misiones principales por concretar: **M17 · Descender**, donde el Consejo por fin autoriza Núcleo Profundo y descubrimos R7/R10 en ese orden, y **M18 · El Voto Inmóvil**, donde encontramos a la Grulla, intervenimos en el vínculo, libramos el combate final y elegimos LIBERAR/CUSTODIAR. Ésas son las siguientes que conviene cerrar.
````
<!-- END-RECOVERED-TEXT T289-02 -->


<a id="t290"></a>

### T290 — M17 y M18 · EL VOTO INMÓVIL

- ID del turno: `4498d9d6-3112-4f9b-93bc-972c2fa16d6c`.
- Fecha UTC: `2026-09-20T07:55:25.415Z`.
- Estado devuelto por la fuente: `completed`.

#### T290.1 — Usuario

ID: `4498d9d6-3112-4f9b-93bc-972c2fa16d6c` · SHA-256 del texto recuperado: `960a6a2f19732c93887afeeff32f5eb63332c855e2ffd634402852bb27f49b65`.

<!-- BEGIN-RECOVERED-TEXT T290-01 -->
````markdown
Continua
````
<!-- END-RECOVERED-TEXT T290-01 -->

#### T290.2 — Asistente original

ID: `bd2bb712-b336-4955-8ae7-7d49393a2717` · SHA-256 del texto recuperado: `eb26f283f29c3238529052f089156cc3d90a760dea8aa0cdd8ea5dab8e9d3fa2`.

**RECUPERACIÓN COMPLETADA.** El texto inicialmente truncado fue fusionado con su continuación original verificada del suplemento.

<!-- BEGIN-RECOVERED-TEXT T290-02 -->
````markdown
Perfecto. Cerramos ahora **M17 y M18**, las dos últimas misiones principales. Aquí ya no necesitamos introducir ningún sistema nuevo: todo debe apoyarse en autorización, exploración, conocimiento, entidades antiguas y el combate de la Grulla que ya diseñamos.

Hay además una ventaja técnica importante en ver55: el jefe final ya posee tres fases llamadas **EL VOTO INMÓVIL**, **LAS ALAS RECUERDAN** y **LA CAMPANA SIN DUEÑO**, y la interfaz ya distingue específicamente al jefe final. Esos nombres y buena parte de la presentación pueden conservarse; lo que cambia por completo es la IA periódica actual, la interpretación de sus HP y la resolución del encuentro. :chatgpt-content-reference{index="0"} :chatgpt-content-reference{index="1"}

# M17 · Descender

M16 termina demostrando algo que M13–M15 todavía podían tratar como historia e infraestructura:

> **cuando el centro pierde estabilidad, toda la secta y su territorio empiezan a compensarlo.**

Después de estabilizar los seis frentes, el Consejo ya no puede justificar mantener cerrado el Núcleo Profundo.

La misión se estructura:

```text
CONSEJO
↓
AUTORIZACIÓN
