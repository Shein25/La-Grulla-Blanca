# Blueprint — integración de la Grulla trifásica en ver74 v0.1

**Estado:** EXPERIMENTAL / LISTO PARA RAMA DEDICADA DE INTEGRACIÓN  
**Fuente de verdad:** cierres Fase I, II y III en `adaptive/`  
**Objetivo:** traducir el contrato cerrado al motor productivo sin recalibrar ni contaminar la rama `implement/3c5-npc-ver74`.

## 1. Guardia de rama

`implement/3c5-npc-ver74` está dedicada exclusivamente a 3C.5 NPC/movilidad.

Por tanto:

```text
NO parchear boss en implement/3c5-npc-ver74
NO tocar main
NO merge automático
NO cambiar SAVE_SCHEMA_VERSION
NO modificar ROOMS.exits ni GATES_329
```

Este blueprint y sus módulos viven sólo en:

`experiment/monster-adaptive-survival-lab-v0.1`

La aplicación al HTML deberá hacerse después en una rama dedicada al boss/integración.

## 2. Hallazgo de ver74

El `ver74` actual NO contiene una Grulla trifásica dentro de `MOBS`.

Los `unico:true` existentes son otros jefes/élites. El Mirador de la Grulla contiene actualmente `centinela_pluma`, no el boss trifásico.

Por ello no se debe convertir silenciosamente un mob existente en la Grulla.

El identificador usado por el adaptador:

`grulla_boss_v01`

es únicamente un **discriminador interno de combate especial**. No es todavía `mobId` canónico ni decisión narrativa.

## 3. Frontera productiva correcta

`Juego.entrarCombate(enemigo, mobId, especial, buff, permitirHuir)` ya es el punto único de entrada al combate.

La Grulla debe entrar como **combate especial**, no como mob genérico de una sola técnica/cadencia.

Forma conceptual:

```js
entrarCombate(
  enemigoRuntime,
  mobIdProductivoPendiente,
  GRULLA_SPECIAL_COMBAT_TAG,
  0,
  false
)
```

`mobIdProductivoPendiente` y la ubicación narrativa NO se fijan en este laboratorio.

## 4. Estado especial dentro de Combate

Al construir `Combate`, sólo cuando:

```js
this.especial === GRULLA_SPECIAL_COMBAT_TAG
```

crear:

```js
this.grullaEspecial = createGrullaSpecialCombatState()
```

Los combates normales no reciben estado nuevo.

El snapshot visible se obtiene de:

`grullaSpecialPublicSnapshot()`

y no expone historia interna, plan oculto ni RNG.

## 5. Gate de técnica — ANTES de resolver efectos

En `turno('tecnica')`, ver74 ya resuelve:

```text
tid
conf
TECNICAS[tid]
coste
tipo
elemento(s)
```

El orden requerido es:

```text
1. validar técnica/cooldown/qi como hoy
2. construir metadata de la técnica
3. consultar gate de la Grulla
4. descontar qi como hoy
5. si gate.blocked:
      mostrar telegraph/counter
      NO aplicar daño/control/guardia/esquiva/fortificación/aflicciones
   si no:
      ejecutar exactamente la técnica existente
6. registrar la acción RESUELTA en memoria
```

Esto preserva el contrato:

```text
uso 1 -> entra
uso 2 -> entra
uso 3 -> entra y la Grulla aprende
uso 4 -> consume qi pero queda suprimido
```

El gate ya está implementado en:

`integration/grulla-technique-gate-v0.1.mjs`

## 6. Observación de acción — DESPUÉS de resolver al jugador

El cerebro nunca debe observar intención futura.

Después de terminar la acción del jugador y antes de elegir la respuesta enemiga, emitir uno de:

```text
BASIC
DEFEND
RECOVER
TECHNIQUE / CONTROL
```

El adaptador:

`integration/grulla-player-action-adapter-v0.1.mjs`

preserva:

- techniqueId real;
- tipo real de `TECNICAS[tid].tipo`;
- elemento realmente resuelto;
- qi realmente gastado;
- daño realmente causado;
- BASIC como variación significativa.

Para híbridas, si el motor no resolvió un elemento concreto, se usa `element:null`; no se inventa.

## 7. Punto temporal exacto en turno()

En ver74 actual:

```js
if (consume) {
  this.round++;
  ...
}

if (consume && quedanVivos) {
  this.intentarUnionCombate(out);
  this.respuestaEnemigos(out);
}
```

El hook de observación del jugador debe ocurrir:

```text
DESPUÉS de resolver la acción
ANTES de elegir/resolver la respuesta de la Grulla
```

No debe reconstruirse desde logs.

## 8. Daño al boss — centralización obligatoria

En `class Combate` se localizaron cuatro rutas de daño al enemigo que pueden afectar a la Grulla:

1. `ATACAR` básico: `this.e.hp -= dmg`;
2. técnica ofensiva: `objetivo.hp -= dmg`;
3. daño de atadura de Filamento: `this.e.hp -= d`;
4. DOT enemigo en `tick()`: `mob.hp -= d`.

Todas deben pasar por una única frontera conceptual:

```js
aplicarDanioObjetivoCombate(mob, damage, source)
```

Comportamiento:

```text
si NO es Grulla especial:
    conservar exactamente mob.hp -= damage

si ES Grulla especial y mob es el boss:
    applyGrullaSpecialBossDamage(...)
    sincronizar mob.hp con session.phaseHp
    sincronizar mob.max_hp con pool actual
    si transición I->II o II->III:
        NO ejecutar muerte/recompensa/cadáver
        mostrar transición de fase
    si derrota FIII:
        dejar hp=0
        permitir cleanup/victoria final
```

Overkill nunca se transfiere:

```text
Fase I  150 -> Fase II 100 completa
Fase II 100 -> Fase III 50 completa
```

## 9. Cleanup genérico

El cleanup actual elimina cualquier `mob.hp <= 0`.

Por eso la transición de fase debe ocurrir **antes** de:

```js
const derrotadosAhora = this.combatientes.filter(m => m.hp <= 0)
```

Tras I→II o II→III, el objeto visual/productivo del boss debe volver a tener HP positivo y `max_hp` igual al nuevo pool.

Sólo Fase III derrotada llega al cleanup final.

## 10. Respuesta enemiga especial

El bloque actual llama:

`this.respuestaEnemigos(out)`

Para la Grulla especial debe existir una bifurcación mínima:

```js
if (esGrullaEspecial) this.respuestaGrulla(out);
else this.respuestaEnemigos(out);
```

`respuestaGrulla()` NO decide por cuenta propia.

Debe pedir:

```js
chooseGrullaSpecialEnemyAction(...)
```

con sólo contexto actual/resuelto:

- HP actual del jugador / max;
- qi actual / max;
- HP actual de la fase / max;
- RNG normal del motor.

Después bindea la instrucción ya cerrada del runtime y la resuelve con las reglas existentes de impacto/estados.

## 11. Ejecución por fase

### Fase I

```text
Golpe de Ala      1d6+2
Campanada         2d6+2
Pata              +3 DEF siguiente ofensiva
```

Pata resuelta llama `markGrullaSpecialEnemyActionResolved()` y arma Resonancia.

El siguiente Golpe de Ala usa:

`resolveGrullaSpecialPhase1Wing()`

si existe Piel activa.

Orden congelado:

```text
tirar impacto
tirar daño bruto
x1,75 si Resonancia+Piel
absorber con Piel
restar HP
consumir Resonancia incluso si falló
```

### Fase II

Usar exclusivamente `CHAIN_A`:

```text
Golpe             1d4
Tormenta          1d6+1 / drain 1
Cerrar Alas       ABS 3 / reserva 6
Recordar Filo     +10 EVA siguiente ofensiva
Eco               drain 3 condicional
```

### Fase III

Usar exclusivamente `M_A`:

```text
Picotazo          +1 ATQ / 1d4+1
Campana           +1 ATQ / 1d6+2 / drain 2
Ala Vacía         +10 EVA
Pata              +3 DEF
Romper Ritmo      +2 ATQ / 1d6+2
```

`Romper Ritmo` sólo puede bindearse cuando el cerebro entrega `committed:true`.

## 12. Piel G345_D1

El `ver74` actual todavía declara la Piel histórica:

```text
guardia 3
duración 2
```

Eso NO coincide con el balance cerrado.

En la futura rama de integración debe trasladarse G345_D1 sin cambiar su semántica de burbuja:

```text
base              guardia 3 / multiplicador 1 / reserva 3
Endurecido        guardia 4
Flexible          +1 multiplicador
Sobrio            coste -1
Aliento económico coste -1
Grueso            guardia 5
Placas continuas  +1 multiplicador
```

Flexible + Grueso = guardia 5 / reserva 10.

No restaurar la Piel original de reserva 21.

## 13. Estados existentes reutilizables

Debe reutilizarse el sistema de estados de `Combate`, no crear un segundo motor:

- `guardia` para absorciones;
- `esquiva` para Paso/Ala Vacía;
- `defensa` para fortificación/bonos temporales;
- `atadura` + Tenacidad para control;
- aflicciones existentes para DOT.

El session controller decide intención/memoria/fase; `Combate` sigue resolviendo impacto, estados, UI y recursos.

## 14. Unión de otros enemigos

`intentarUnionCombate(out)` existe en el flujo genérico.

Como la ubicación narrativa/productiva de la Grulla todavía no está fijada, este laboratorio NO decide si durante el boss se permiten incorporaciones externas.

Al crear la rama productiva deberá fijarse explícitamente una de estas políticas:

```text
A. encounter aislado: no intentarUnionCombate
B. encounter abierto: conservar unión
```

No inferirla del balance.

## 15. Identidad/recompensa narrativa pendiente

El laboratorio deliberadamente NO fija:

- `mobId` productivo;
- habitación exacta de aparición;
- trigger narrativo de inicio;
- loot/recompensa final;
- cadáver/no cadáver;
- flags/misión posterior;
- posibilidad de huir.

El benchmark sólo cerró combate.

Esos datos pertenecen a integración narrativa/Arco correspondiente.

## 16. Módulos ya preparados

```text
integration/grulla-encounter-runtime-contract-v0.1.mjs
integration/grulla-player-action-adapter-v0.1.mjs
integration/grulla-technique-gate-v0.1.mjs
integration/grulla-encounter-session-v0.1.mjs
integration/grulla-ver74-special-combat-adapter-v0.1.mjs
```

Tests dirigidos:

```text
tests/grulla-encounter-runtime-contract.test.mjs
tests/grulla-player-action-adapter.test.mjs
tests/grulla-technique-gate.test.mjs
tests/grulla-encounter-session.test.mjs
tests/grulla-ver74-special-combat-adapter.test.mjs
```

Comando preparado:

`npm run test:grulla-integration-ready`

## 17. Criterio de integración aprobada

No considerar integrado hasta verificar en una rama dedicada:

1. las cinco suites dirigidas pasan;
2. pruebas históricas de combate siguen pasando;
3. la tercera repetición entra y la cuarta queda bloqueada;
4. BASIC rompe lock; DEFENDER/RECOVER no;
5. Resonancia x1,75 ocurre antes de absorción;
6. fallo del Golpe consume Resonancia;
7. overkill no salta fases;
8. I→II nace con 100 HP; II→III con 50 HP;
9. sólo FIII genera victoria final;
10. Paso/Piel/Filamento conservan sus counters cerrados;
11. no se lee acción futura ni inventario/cooldowns ocultos;
12. no se toca `CADENCE_COMPAT` para otros monstruos.

## 18. Próxima acción autorizable

El código del boss está **integration-ready en laboratorio**, pero no debe copiarse todavía a `implement/3c5-npc-ver74`.

El siguiente paso productivo correcto es crear/usar una rama dedicada a integración de la Grulla a partir del baseline aprobado y aplicar este blueprint allí.