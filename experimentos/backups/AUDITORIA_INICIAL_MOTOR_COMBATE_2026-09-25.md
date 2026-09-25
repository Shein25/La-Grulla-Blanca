# Auditoría inicial — Motor de combate actual — 2026-09-25

## Fuente verificada

Producción activa 3C.6:

```text
branch = implement/3c6-prologo-m01-m07
HEAD   = 748bd4480e37fd2523fa833081b20522b9724dab
file   = grulla-blanca_ver75.html
blob   = 1c897be6ddf3d18436a043fab0c848ef7f3fb18c
```

Se compararon además los bloques de combate con `grulla-blanca_ver74.html` en `main`.

Resultado:

- reglas puras de impacto/crítico: idénticas;
- contrato de estados + técnicas: idéntico;
- `class Combate`: misma semántica; sólo diferencias de whitespace.

Por tanto esta auditoría describe el motor real actual de ver75.

## 1. Reglas puras

Constantes:

```text
ESQUIVA_INNATA = 5
MULTIPLICADOR_CRITICO = 1.5
```

Pipeline de impacto:

- d20;
- 1 siempre falla;
- 20 o tirada >= critMin impacta;
- resto: tirada + ataque >= defensa + evasión adicional;
- evasión adicional deriva de `esquiva`;
- crítico usa `critMin`;
- daño crítico usa `critMult`.

El motor ya acepta por llamada:

`atacar(a, d, critMin, critMult)`

## 2. Roles de técnicas del jugador ya implementados

```text
ofensiva
fortificacion
guardia
esquiva
control
```

Ofensiva soporta:

- daño;
- ataque/precisión;
- critMin;
- critMult;
- AOE;
- ventaja/desventaja elemental;
- concordancia;
- quemadura;
- debilitar ataque;
- control asociado a impacto.

Apoyo soporta:

- evasión temporal;
- defensa plana temporal;
- absorción con reserva;
- control con tenacidad de jefes.

## 3. Estados de combate

Categorías declaradas:

```text
esquiva
defensa
guardia
dano
ataque
tenacidad
quemadura
veneno
debil
atadura
```

Contrato:

- categorías distintas pueden coexistir;
- misma categoría reemplaza/refresca por defecto;
- existe modo futuro `modoAcumulacion:"acumular"`.

Pero NO todas las categorías declaradas participan hoy de la resolución.

Funcionan realmente en resolución:

- jugador: esquiva, defensa, guardia;
- enemigos: debil, atadura, quemadura/veneno;
- aflicciones persistentes sobre jugador.

`dano` y `ataque` están preparados como metadatos/UI, pero no son leídos por el pipeline actual como buffs temporales del jugador.

## 4. Absorción

Dos comportamientos reales:

1. `DEFENDER`:
   - porcentaje;
   - protege 2 impactos reales;
   - un fallo no lo consume.

2. técnicas guardia:
   - reducción máxima por golpe;
   - reserva total = reducción × duración inicial;
   - no decae por ronda;
   - se consume sólo con daño absorbido.

## 5. Enemigos actuales

Los mobs no usan el sistema completo de técnicas del jugador.

Contrato actual `mob.tecnica`:

- `name`;
- `cada`;
- opcional `ataque`;
- opcional `daño`;
- opcional `veneno`;
- opcional `quemadura`;
- opcional `drenaQi`.

`respuestaEnemigos()` ejecuta esa técnica en calendario fijo.

Puede:

- mejorar ataque para ese golpe;
- reemplazar daño para ese golpe;
- envenenar;
- quemar;
- drenar qi;
- provocar herida de meridiano bajo condición existente;
- telegraphar la técnica anterior al turno de uso.

No puede hoy, por esta ruta:

- elegir entre varias habilidades;
- usar una defensa propia;
- ganar evasión temporal;
- ganar defensa temporal;
- ganar absorción;
- ganar ataque temporal persistente;
- ganar daño temporal persistente;
- modificar critMin;
- modificar critMult;
- ejecutar una habilidad híbrida ataque + buff propio genérico.

## 6. Asimetría crítica

Aunque `aplicarAMob()` puede almacenar estados genéricos en un mob, el ataque del jugador usa actualmente:

`atacar(atacante, objetivo, critMin, critMult)`

donde `objetivo` aporta directamente sus stats base.

No hay lecturas actuales de:

- `estadoDeMob(...,"defensa")`;
- `estadoDeMob(...,"esquiva")`;
- `estadoDeMob(...,"guardia")`;
- `estadoDeMob(...,"ataque")`;
- `estadoDeMob(...,"dano")`.

Por tanto guardar esos estados en un enemigo NO basta: aún no afectan el combate.

## 7. Habilidades combinadas

El sistema de técnicas del jugador permite combinaciones ofensivas + efectos secundarios
(daño + quemadura, daño + debil, daño + control, crítico, etc.).

Pero la resolución usa ramas exclusivas por `t.tipo`:

`ofensiva / control / esquiva / fortificacion / guardia`.

No existe todavía un resolver genérico de múltiples efectos capaz de representar de forma limpia:

- ataque + evasión propia;
- ataque + absorción;
- defensa + crítico;
- daño + buff de ataque;
- otras composiciones arbitrarias.

## 8. Conclusión

Principio confirmado:

> Monster Combat AI debe decidir la habilidad.
> El motor de combate debe resolverla.

Pero antes de conectar Monster Combat AI necesitamos un contrato/adapter experimental que
exponga de forma simétrica y declarativa las capacidades reales del motor para monstruos.

No modificar producción todavía.

Siguiente fase propuesta:

`Combat Ability Contract v0.1`

Objetivo:

- definir catálogo declarativo de habilidades monstruo;
- distinguir efectos ofensivos, defensivos, buffs, debuffs, control e híbridos;
- mapear cada efecto al pipeline real existente;
- identificar explícitamente qué capacidades requieren adapter nuevo;
- mantener cálculo de daño/DEF/EVA/ABS/CRIT en el motor, nunca en Monster AI.
