# Matriz experimental — Progresión natural de monstruos por etapa v0.1

**Estado:** EXPERIMENTAL / NO CANÓNICO.

## Regla central

La progresión queda separada en tres capas:

```text
ETAPA NATIVA DE LA ESPECIE
        +
ROL DENTRO DE SU ZONA
        +
APRENDIZAJE ADAPTATIVO CONTRA EL JUGADOR
```

La etapa del jugador **no escala automáticamente HP/ATQ/DEF** de criaturas antiguas.

Subir de etapa amplía el techo de aprendizaje de una población que ya ha peleado con el jugador.

## Bandas ecológicas observadas en ver74

La distribución real de spawns produce cuatro bandas muy claras:

```text
LianQi I   → Secta Exterior / Bosques
LianQi II  → Cantera y Vetas
LianQi III → Aguas y Barrancos
LianQi IV  → Alturas
```

No es una agrupación inventada: los 18 combatientes actuales aparecen exactamente en esas franjas, salvo la Rata de Qi que ocupa Secta Exterior como amenaza introductoria.

## Asignación propuesta

| Etapa | Monstruo | Rol | Lectura |
|---|---|---|---|
| I | Rata de Qi | NORMAL | tutorial ecológico / amenaza básica |
| I | Avispa de Jade | NORMAL | criatura frágil con estado |
| I | Serpiente de Qi | NORMAL | primer veneno sostenido |
| I | Macaco ladrón | SKIRMISHER | presión de Qi y movilidad |
| I | Lobo espiritual | APEX_BRIDGE | depredador que cierra Bosques y anticipa Etapa II |
| II | Sapo de Ceniza | NORMAL | ofensiva elemental + quemadura |
| II | Escarabajo de Hierro | TANK | defensa alta y carga |
| II | Eco del Caído | ELITE | único sin técnica pero con cuerpo/daño superiores |
| II | Sapo Caldera | BOSS | jefe termal; daño sostenido alto |
| II | Rey Escarabajo | BOSS | jefe acorazado; gran defensa y daño |
| III | Pez Lunar | NORMAL | atacante acuático medio |
| III | Anguila Estelar | SKIRMISHER | daño + drenaje de Qi |
| III | Sombra Ahogada | ELITE | único con aflicción de grado superior |
| III | Guardián Coral | BOSS | gran HP/DEF + drenaje |
| IV | Devorador de Niebla | NORMAL | fauna avanzada de altura |
| IV | Halcón de Tormenta | SKIRMISHER | alta precisión y daño de picado |
| IV | Mantis de Nube | BOSS | depredador máximo de movilidad/corte |
| IV | Centinela de Plumas | BOSS | guardián final resistente |

Distribución:

```text
Etapa I   5
Etapa II  5
Etapa III 4
Etapa IV  4
TOTAL    18
```

## Filosofía de dificultad

Cada etapa no tiene sólo "mobs del mismo nivel".

Debe contener:

```text
NORMAL
→ enseña la nueva presión de la zona

SKIRMISHER / TANK
→ cambia cómo se resuelve el combate

ELITE / APEX
→ comprueba dominio del sistema

BOSS
→ no representa la dificultad media de la etapa
```

Por eso un jefe puede conservar una tasa de victoria mucho más baja que los normales de su misma banda sin obligarnos a moverlo de etapa.

## Regla para encuentros adelantados

Si el jugador entra en contacto con una criatura **antes** de su etapa nativa:

```text
playerStage < nativeStage
→ Tier adaptativo 0
→ BASE_NATURAL
→ sin bonificaciones de aprendizaje extra
```

La criatura ya es peligrosa por su ficha natural; no necesita además ventajas adaptativas anticipadas.

## Progresión adaptativa según etapa del jugador

La etapa nativa determina cuándo empieza a ser razonable que esa población desarrolle aprendizaje contra el jugador.

```text
playerStage == nativeStage
→ Tier adaptativo máximo 1
→ SUPERVIVENCIA
→ una defensa propia de especie

playerStage == nativeStage + 1
→ Tier máximo 2
→ reconocimiento persistente de patrones
→ puede anticipar una apertura conocida

playerStage == nativeStage + 2
→ Tier máximo 3
→ contraadaptación
→ puede elegir una rama defensiva permitida por especie

playerStage == nativeStage + 3
→ Tier máximo 4
→ adaptación madura
→ puede adquirir una segunda adaptación compatible
```

El techo **no concede** esas capacidades. Sólo las habilita.

La experiencia adaptativa sigue siendo necesaria.

## Ejemplo — Rata de Qi

```text
Jugador LianQi I
Rata Tier máximo 1
→ puede aprender Reflejo de Madriguera

Jugador LianQi II
Rata Tier máximo 2
→ puede recordar aperturas repetidas

Jugador LianQi III
Rata Tier máximo 3
→ puede especializar su respuesta frente al estilo observado

Jugador LianQi IV
Rata Tier máximo 4
→ población veterana puede poseer una segunda adaptación
```

Pero:

```text
Rata de Qi ≠ 40 HP
Rata de Qi ≠ daño de monstruo de Alturas
```

El jugador debe seguir sintiendo que superó la zona.

## Ejemplo — monstruo de Etapa IV

Una Mantis de Nube ya pertenece a la última banda de Arco I.

Con jugador en LianQi IV:

```text
nativeStage 4
playerStage 4
delta 0
→ Tier adaptativo máximo 1
```

Eso no la vuelve simple: su ficha base y su perfil cognitivo ya son avanzados.

La progresión adaptativa es una capa adicional, no un reemplazo de la fuerza natural de la especie.

## Interacción con Monster Adaptive Survival

```text
nativeStage / role
        ↓
adaptive capability ceiling
        ↓
adaptive XP real
        ↓
survival evolution / memoria / futuras ramas
        ↓
effectiveKit
        ↓
Monster Combat AI existente
```

No se crea otro motor de decisión.
