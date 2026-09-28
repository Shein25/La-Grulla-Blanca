# CHECKPOINT — REDISEÑO DE TÉCNICAS ARCO 1
Fecha: 2026-09-28
Rama de trabajo: `experiment/combat-stat-contract-v0.1`
Contrato principal: `docs/experimentos/CONTRATO_COMBATE_ESTADISTICAS_DOT_V0_1.md`

## 1. Propósito de este checkpoint

Este documento fija el estado exacto del rediseño antes de continuar en otro chat.

NO implementar runtime desde este checkpoint.
NO tocar `main`.
NO hacer merge.
NO contaminar `implement/3c5-npc-ver74`.
El trabajo actual sigue siendo de contrato/diseño hasta autorización explícita de implementación.

---

## 2. Punto exacto de reanudación

La próxima conversación debe continuar AQUÍ:

> Antes de diseñar la técnica inicial de Fuego, revisar las ETAPAS DEL JUEGO y localizar/confirmar el contrato de las 3 RAMAS por técnica.

Orden inmediato:

1. Revisar cómo están estructuradas las etapas/reinos/progresión de Arco 1.
2. Verificar en repo/documentación si existe una regla explícita que establezca que cada técnica tiene exactamente 3 ramas y cómo deben funcionar.
3. Si la regla existe, recuperarla literalmente y usarla.
4. Si no existe de forma explícita, no inventarla silenciosamente: establecerla como decisión nueva con Lucas.
5. Recién entonces diseñar desde cero la técnica inicial de Fuego.
6. Después continuar Metal, Agua, Tierra y Viento.

IMPORTANTE:
- La técnica inicial de cada uno de los 5 elementos será OFENSIVA.
- No empezar todavía por números de daño/coste.
- Primero cerrar identidad, función, interacción con Concordancias, etapa de disponibilidad y ramas.
- Todas las técnicas comunes de Arco 1 se recrean desde cero.

---

## 3. Dirección cerrada para técnicas comunes de Arco 1

El catálogo común de `ver74` NO se migra mecánicamente.

Se puede conservar:
- nombre;
- fantasía;
- concepto;

sólo si sigue encajando.

NO se hereda automáticamente:
- daño;
- coste de Qi;
- duración;
- DEF/Guardia;
- Evasión;
- Control;
- ramas;
- requisitos;
- efectos secundarios;
- balance antiguo.

Cada técnica nueva debe declararse contra el contrato nuevo:
- elemento;
- rol;
- efecto principal;
- coste;
- requisitos;
- compatibilidades de Concordancia;
- etapa de acceso;
- ramas/especializaciones.

Las 5 técnicas iniciales:
- Fuego → ofensiva
- Metal → ofensiva
- Agua → ofensiva
- Tierra → ofensiva
- Viento → ofensiva

La diferenciación defensiva/control/utilitaria/aflicciones aparece luego por nuevas técnicas y progresión.

---

## 4. Recordatorio del prólogo — PENDIENTE

El prólogo debe revisarse para permitir selección coherente entre los CINCO elementos canónicos:
- Fuego
- Metal
- Agua
- Tierra
- Viento

El prólogo actual deriva de un esquema antiguo de tres raíces/técnicas.

Pendiente decidir:
- si alcanza la estructura actual de preguntas;
- si se añade 1 pregunta;
- si se añaden 2 preguntas;
- cómo evitar que el prólogo rigidice demasiado la build futura.

No modificar todavía el runtime del prólogo.

---

## 5. Núcleo de combate ya cerrado y que las técnicas nuevas deben respetar

### Acción / impacto / porciones
```text
ACTION
 └─ 1..N IMPACTS
     └─ 1..N DAMAGE PORTIONS
```

Arco 1 normalmente usa un impacto por acción.

### Precisión / Evasión
```text
Hit Chance =
clamp(Effective Precision - target Evasion, 5, 100)
```

Precisión base normal de referencia: 100.
Evasión forma parte de esa misma probabilidad; no hay segundo roll de esquiva.

### Crítico
- base 5%
- multiplicador base x1.50
- bonificaciones de probabilidad = puntos porcentuales salvo definición explícita distinta
- daño crítico se suma al multiplicador
- un roll de crítico por impacto
- DOT no critica por defecto

### Daño ofensivo
Porciones compatibles reciben flats y % normales en pool aditivo.
Crítico es capa separada.

### DEF
- reducción plana universal del daño directo
- una vez por impacto, después de sumar porciones
- puede reducir a 0
- DOT ignora DEF

### Penetración
```text
DEF real
→ shred/reducción de DEF
→ % penetración
→ penetración plana
→ DEF efectiva
```

### Absorción
Directo:
```text
DIRECTO → DEF → ABSORCIÓN → HP
```
DOT:
```text
DOT → ABSORCIÓN → HP
```

### Control / Tenacidad
```text
Control Chance =
clamp(Effective Control - target Tenacity, 5, 100)
```

### Redondeo
No redondear intermedios.
Un único redondeo al modificar el recurso discreto.

### Qi
NO existe regeneración pasiva de Qi por turno.
Fuentes válidas:
- Meditación
- consumibles explícitos
- robo/drenaje
- piedras espirituales
- efectos futuros explícitos

---

## 6. Elementos y raíces — CERRADO

Elementos canónicos:
- Fuego
- Metal
- Agua
- Tierra
- Viento

No existe Madera.
No existen resistencias elementales base.
Los elementos son etiquetas/interacciones, no una segunda familia defensiva.
No migrar el antiguo rock-paper-scissors elemental de `ver74`.

### Rasgos de raíz principal

Fuego:
- +10% daño directo general
- +5 puntos porcentuales de crítico

Metal:
- +10 puntos porcentuales de penetración porcentual general
- +5 Precisión

Agua:
- -10% coste de Qi de todas las técnicas
- +5 Control

Tierra:
- +10% Vida máxima
- +5 Tenacidad

Viento:
- +10 puntos de Evasión base
- +5% Daño Crítico (se suma al multiplicador)

---

## 7. Injerto espiritual — CERRADO

```text
RAÍZ PRINCIPAL
→ 100% rasgos
→ 100% afinidad

INJERTO
→ 80% rasgos
→ 100% afinidad
→ 90% aprendizaje
```

Valores del injerto:
- Fuego: +8% daño directo, +4 pp crítico
- Metal: +8 pp penetración, +4 Precisión
- Agua: -8% coste de Qi, +4 Control
- Tierra: +8% Vida máxima, +4 Tenacidad
- Viento: +8 Evasión base, +4% Daño Crítico

Sólo un injerto permanente.

Las raíces NO determinan si una técnica es ofensiva/defensiva/control/etc.
Eso lo determina cada técnica.

---

## 8. Concordancias — 5 ramas / 20 relaciones conceptuales

Principio:
- una técnica deja un Eco elemental;
- la siguiente técnica compatible puede consumirlo;
- el efecto depende de ORIGEN → DESTINO;
- no existe un +X% genérico universal;
- cada Concordancia habilitada debe tener al menos una técnica receptora real que pueda expresar su efecto;
- si una Concordancia no tiene receptor compatible en una etapa, no se introduce todavía en esa etapa.

### Fuego como origen
Fuego → Tierra:
- Cimiento cocido
- consolidación
- ofensiva: potencia magnitud ofensiva principal
- defensiva: potencia DEF/Absorción generada

Fuego → Metal:
- forja/templado
- ofensiva: Penetración
- defensiva: magnitud defensiva Metal

Fuego → Agua:
- presurización/vapor
- ofensiva/control: Control o debilitación compatible
- defensiva: respuesta reactiva Agua

Fuego → Viento:
- corriente ascendente/aceleración
- ofensiva: propiedad crítica compatible
- defensiva: Evasión generada

### Metal como origen
Metal → Fuego:
- chispa/ignición
- ofensiva: aplicación/potencia de Quemadura compatible
- defensiva: respuesta térmica/reactiva

Metal → Agua:
- cauce tallado/canalización
- ofensiva/control: Control o precisión del efecto
- defensiva/utilitaria: eficiencia de Qi

Metal → Tierra:
- anclaje de hierro
- ofensiva: ruptura/penetración compatible
- defensiva: Absorción/Tenacidad/magnitud defensiva propia

Metal → Viento:
- filo en la corriente
- ofensiva: Precisión
- defensiva: Evasión generada, sujeto a validación con técnica real

### Agua como origen
Agua → Fuego:
- Vapor súbito
- potencia propiedad compatible de Quemadura/expansión/presión
- defensiva: respuesta térmica/reactiva

Agua → Metal:
- Templar el filo
- ofensiva: Daño Crítico
- defensiva: estabilidad/fortificación

Agua → Tierra:
- Erosión/sedimentación
- ofensiva: reducción de DEF para impactos posteriores
- defensiva: estabilidad/cohesión

Agua → Viento:
- Velo de niebla
- ofensiva: reducción de Precisión / desorientación
- defensiva: Evasión generada

### Tierra como origen
Tierra → Fuego:
- Corazón de magma
- ofensiva: persistencia/intensidad de aflicción de Fuego compatible
- defensiva: contención/aprovechamiento del daño recibido

Tierra → Metal:
- Forja asentada
- ofensiva: Probabilidad Crítica
- defensiva: estabilidad de DEF/Absorción/fortificación

Tierra → Agua:
- Cauce represado
- ofensiva/control: reducción de Evasión / movilidad
- defensiva/utilitaria: duración de efecto compatible

Tierra → Viento:
- Tormenta de polvo
- ofensiva: área/propagación / eficiencia multiobjetivo
- defensiva: duración de Evasión

### Viento como origen
Viento → Fuego:
- Avivar las brasas
- ofensiva: daño directo de la ejecución
- defensiva: magnitud inmediata del efecto defensivo

Viento → Metal:
- Filo impulsado
- ofensiva: Precisión
- defensiva: eficiencia de ejecución / reducción de coste compatible

Viento → Agua:
- Corriente ligera
- reduce % de coste de Qi de la técnica Agua receptora
- entra al pool general de reducción de coste

Viento → Tierra:
- Impacto de vendaval
- ofensiva/control: Control
- defensiva: Tenacidad generada cuando corresponda

Las magnitudes numéricas de Concordancia NO están cerradas.

---

## 9. Definitivas híbridas — PRINCIPIOS CERRADOS

Las híbridas son las DEFINITIVAS del personaje.

Características:
- máxima expresión de dos disciplinas;
- herramienta excepcional, no rotación normal;
- alto coste de Qi;
- cooldown alto;
- potencia excepcional;
- decisión táctica sobre cuándo usarla;
- rara y difícil de obtener;
- no se regala por progresión básica;
- tener raíces compatibles NO concede automáticamente la Definitiva;
- la obtención puede ser maestro/manual/prueba/evento/legado/misión/etc.;
- puede encontrarse una Definitiva sin relación con la raíz principal ni injerto;
- el jugador decide si el coste/beneficio justifica desarrollarla.

### Afinidad
Confluencia:
- afinidad con ambos elementos
- uso más natural
- sin retroceso espiritual

Parcial:
- afinidad con uno
- retroceso espiritual leve

Ajena:
- afinidad con ninguno
- retroceso espiritual mayor
- posible Herida Meridiana bajo condiciones/probabilidad explícita

### Retroceso espiritual
Representa circulación forzada de Qi por meridianos no adaptados.
Puede ser pequeña pérdida de Vida proporcional a Vida máxima.
No usa:
- Precisión
- Crítico
- DEF
- Penetración
- Life Leech

No es DOT.
No dispara eventos ofensivos normales.

Herida Meridiana:
- consecuencia seria y poco frecuente
- no ocurre automáticamente en cada uso ajeno

Desviación de Qi:
- sólo para eventos excepcionales de incompatibilidad extrema/abuso/fallo grave/narrativa
- NO penalidad cotidiana

Pendientes numéricos:
- porcentaje de retroceso
- probabilidad/condiciones de Herida Meridiana
- interacción con Absorción
- si puede matar al usuario

### Concordancias y Definitivas
Las Definitivas quedan COMPLETAMENTE fuera de Concordancias:
- no consumen Eco;
- no generan Eco;
- no reciben mejoras de Concordancia;
- no activan Concordancias.

### Cantidad de elementos
Por ahora:
- híbrida/Definitiva = exactamente 2 elementos

Una técnica de 3 elementos queda reservada para futuro y requerirá contrato propio.

---

## 10. Híbridas históricas existentes — sólo anclas de concepto

Actualmente `ver74` contiene:
- Fuego + Viento → Brasa del Vendaval
- Agua + Viento → Aguja del Río de Plata
- Metal + Tierra → Coraza del Crisol Sereno
- Agua + Fuego → Loto de Vapor Concordante

No conservar automáticamente números ni funcionamiento viejo.
Se revisarán/recrearán bajo el nuevo contrato.

---

## 11. Catálogo común histórico de ver74 — sólo referencia

Encontrado en `grulla-blanca_ver74.html`.

Iniciales/tempranas históricas:
- Palma Ardiente — Fuego — ofensiva
- Filo de Qi Metálico — Metal — ofensiva
- Látigo de Agua — Agua — ofensiva
- Paso de Nube Ligera — Viento — esquiva
- Piel de Cobre — Tierra — guardia
- Filamento de Agua — Agua — control

Posteriores históricas:
- Sello de la Montaña Oprimida — Tierra — ofensiva
- Espejo de Luna — Agua — fortificación
- Lanza que Parte Nubes — Viento — ofensiva
- Círculo de las Cien Ascuas — Fuego — AOE ofensiva
- Lluvia de los Mil Filos — Metal — AOE ofensiva
- Marea que Barre las Ocho Orillas — Agua — AOE ofensiva
- Tijera del Vendaval Partido — Viento — AOE ofensiva
- Respiración del Cuerpo-Horno — Fuego — guardia

Estos nombres NO fijan el nuevo catálogo.

---

## 12. DOT / aflicciones

Hemorragia:
- cerrada
- física persistente
- sólo acciones explícitas de corte
- requiere ON_HP_DAMAGE
- activa con acción voluntaria del afectado
- ignora DEF
- pasa por Absorción
- sin crítico por defecto
- stacks independientes

Quemadura:
- dirección avanzada, todavía no cerrada numéricamente
- Fire DOT explícito
- tick al inicio del turno afectado
- stacks independientes
- ignora DEF
- pasa por Absorción
- sin crítico por defecto

Veneno:
- todavía pendiente de contrato definitivo
- debe diferenciarse de Quemadura
- más acumulación / duración / presión sostenida como dirección

---

## 13. Cultivo/progresión — principio ya cerrado

Cultivar aumenta capacidad/acceso, NO infla automáticamente todas las estadísticas de combate.

Puede otorgar:
- Vida máxima
- Qi máximo
- puntos de técnica
- nuevas ramas
- desbloqueos
- parámetros de cultivo/meditación

No otorga automáticamente:
- daño
- DEF
- Precisión
- Evasión
- crítico
- Penetración
- Control
- Tenacidad
- Life Leech
- Absorción

Por eso las ETAPAS deben revisarse antes de diseñar técnicas: hay que saber cuándo debe aparecer cada herramienta y cuándo pueden habilitarse ramas/concordancias.

---

## 14. Punto abierto crítico: 3 ramas por técnica

Lucas recuerda que cada técnica tiene 3 ramas y que el contrato probablemente especificaba cómo debían ser.

Verificación hecha al crear este checkpoint:
- el contrato actual contiene muchas referencias a “ramas”;
- NO se encontró en el contrato principal una cláusula inequívoca con el texto “cada técnica tiene exactamente 3 ramas”;
- búsqueda textual en el repo por “3 ramas”, “tres ramas”, “ramas de técnica”, “rama ofensiva”, “rama defensiva” no devolvió coincidencias directas.

Por tanto, PRIMERA TAREA del próximo chat:
- revisar documentación/commits anteriores y estructura actual de especializaciones;
- recuperar la regla exacta si existe;
- si no existe, establecerla explícitamente antes de crear Fuego.

No asumir silenciosamente la estructura de las 3 ramas.

---

## 15. Próximo diseño: Fuego inicial

NO diseñarlo todavía antes de revisar etapas + contrato de ramas.

Cuando esos dos puntos estén claros, diseñar:
- nombre provisional/definitivo;
- fantasía;
- rol ofensivo;
- daño/efecto principal conceptual;
- qué enseña del elemento Fuego;
- qué Eco deja;
- qué Concordancias puede recibir;
- qué Concordancias prepara;
- etapa de acceso;
- 3 ramas (si la regla queda confirmada);
- recién después: números y balance.

Objetivo:
La técnica inicial de Fuego debe ser simple de entender, útil al principio y capaz de crecer sin contradecir las Concordancias ni la futura identidad de Quemadura.

---

## 16. Pendientes globales que NO deben perderse

- piso global exacto de reducción de coste de Qi;
- stacking exacto de múltiples escudos de Absorción;
- cierre numérico de Quemadura;
- contrato final de Veneno;
- números de retroceso espiritual;
- Herida Meridiana por Definitivas ajenas;
- balance final de Definitivas;
- revisión completa del prólogo de 5 elementos;
- reconstrucción completa del equipo desde cero después de técnicas;
- luego benchmarks del jugador;
- luego monstruos/jefes;
- la integración de IA NPC/monstruos/jefes la maneja otro agente.

---

## 17. Último estado aceptado por Lucas

1. Todas las técnicas comunes de Arco 1 se recrean desde cero.
2. El prólogo deberá contemplar los cinco elementos; quizá se agregue 1 o 2 preguntas.
3. Las cinco técnicas iniciales serán ofensivas.
4. Se empezará por Fuego.
5. ANTES de Fuego hay que revisar:
   - etapas del juego;
   - regla/contrato de las 3 ramas por técnica.

Éste es el punto exacto para continuar en el próximo chat.
