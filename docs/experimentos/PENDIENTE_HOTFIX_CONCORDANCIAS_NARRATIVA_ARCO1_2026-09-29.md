# PENDIENTE — Hotfix narrativo: Concordancias como enseñanza de la Grulla Blanca

Fecha de registro: 2026-09-29  
Rama de trabajo: `experiment/combat-stat-contract-v0.1`  
Estado: **AGENDADO / NO IMPLEMENTAR TODAVÍA**

## Disparador

Este hotfix debe abordarse **después de cerrar e integrar los diálogos NPC de A07**.

No debe adelantarse mientras los diálogos sigan en revisión, porque la auditoría deberá revisar también qué sabe cada NPC, cuándo puede decirlo y con qué nivel de certeza.

## Decisión de diseño

La **Concordancia** queda establecida como una enseñanza característica y básica de la Secta de la Grulla Blanca.

No implica una pasiva, bonus numérico ni sistema nuevo.

La especialidad de la secta se expresa mediante:

- circulación precisa del Qi;
- estabilidad de meridianos;
- enseñanza sistemática de Concordancias entre técnicas y disciplinas;
- progresión posterior hacia artes híbridas.

La Concordancia sigue siendo una capacidad del motor general. La Grulla Blanca se distingue porque la estudia, formaliza y enseña deliberadamente.

## Doctrina pública

Mantener:

- **La estabilidad precede a la ascensión.**
- **Asentar · Circular · Elevar.**

La Concordancia debe introducirse como consecuencia natural de la enseñanza de **Circular**, no como un cuarto principio público.

## Secreto narrativo

No revelar prematuramente el principio antiguo/perdido de **Entrelazar**.

Separación obligatoria:

```text
ENSEÑANZA PÚBLICA
Asentar
Circular
Elevar
Concordancia entre técnicas
        ≠
SECRETO HISTÓRICO
Entrelazar
Dos Alas
investigación antigua
raíces / injerto
vínculo
```

El injerto debe conservar su papel como extensión histórica/prohibida de una pregunta mucho más peligrosa:

> si pueden entrelazarse disciplinas, ¿pueden entrelazarse raíces?

## Auditoría obligatoria antes del hotfix

Auditar la continuidad completa:

```text
Prólogo
M01
M02
M03
M04–M07
M08–M10
M11–M12
M13–M15
M16–M17
M18
Epílogo
```

La auditoría debe detectar al menos:

1. **Falta de siembra** — conceptos importantes que aparezcan demasiado tarde sin preparación.
2. **Spoiler prematuro** — NPC o textos que revelen información antes de la etapa correcta.
3. **Terminología inconsistente** — Concordancia / combinación / entrelazar / Dos Alas usados como equivalentes sin serlo.
4. **Contradicción doctrinal** — textos que presenten a la Grulla Blanca como simple secta de Viento, de una técnica insignia aislada o de poder bruto.
5. **Conocimiento por NPC** — verificar SOSPECHA / SABE / CONFIRMADO y permisos narrativos.
6. **Compatibilidad con flags y gates** — el hotfix narrativo no debe alterar progresión, revelaciones, estados ni gating salvo decisión humana posterior.

## Puntos preliminares a revisar

### Prólogo
Sólo insinuación de una tradición particular. No tutorializar Concordancias.

### M01 — Un nombre entre miles
Buen punto para sembrar doctrina institucional y **Asentar · Circular · Elevar**.

### M02 — Trabajo que alguien debe hacer
No cargar con Concordancias; mantener su función de servicio, Examen y vida cotidiana.

### M03 — Aprender a permanecer
Punto principal candidato para introducir formalmente el término **Concordancia** dentro de la enseñanza de Shen Baojun.

La misión ya contiene:
- Piel de Cobre;
- práctica;
- evaluación de circulación;
- ingreso formal como Discípulo Externo.

No crear una misión nueva sólo para esto.

### M04–M07
Revisar diálogos NPC para que el vocabulario de circulación y Concordancia aparezca de forma natural, sin repetir tutorial.

### M08–M10
Revisar siembra de investigación antigua y que no se explique demasiado pronto el injerto.

### M11–M12
Revisar relación temática con **Dos Alas** y estructuras mayores de circulación/entrelazado.

### M13–M17
Revisar cómo las consecuencias históricas recontextualizan la enseñanza básica sin revelar antes de tiempo R7/R10 ni la verdad del vínculo.

### M18 / Epílogo
Revisar que el cierre permita reinterpretar la doctrina de la secta a la luz de la verdad descubierta.

## Orden futuro de trabajo

1. Cerrar diálogos NPC / A07.
2. Congelar la versión candidata de diálogos.
3. Auditar Prólogo→M18/Epílogo con esta decisión como criterio.
4. Proponer cambios de texto separados por etapa.
5. Revisar manualmente spoilers y niveles de conocimiento.
6. Aplicar hotfix narrativo.
7. Ejecutar regresión de quests/flags/gates.
8. Reauditar continuidad narrativa.

## Guardia

Hasta activar este pendiente:

- NO modificar runtime/HTML por esta decisión;
- NO modificar misiones;
- NO introducir nuevos flags;
- NO inventar bonuses de secta;
- NO convertir Concordancia en exclusiva mecánica de la Grulla Blanca;
- NO revelar Entrelazar/injerto en escenas tempranas.

