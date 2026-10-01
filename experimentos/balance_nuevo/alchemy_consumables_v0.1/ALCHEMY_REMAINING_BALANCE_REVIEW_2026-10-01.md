# Alquimia — propuesta integrada del balance restante

Fecha: 2026-10-01

Estado: **HP CERRADO / RESTO EN PROPUESTA**

## 1. HP

Autoridad cerrada:

`ALCHEMY_VITALITY_HP_CONTRACT_V0_1.json`

No se recalibra.

## 2. Qi puro

Propuesta:

| Etapa | Impura | Estable | Superior | Excepcional |
|---|---:|---:|---:|---:|
| LI | 8 | 12 | 16 | 20 |
| LII | 10 | 15 | 20 | 26 |
| LIII | 12 | 18 | 25 | 33 |
| LIV | 14 | 22 | 30 | 40 |

Pools desnudos: 37 / 43 / 49 / 55.

La excepcional representa aproximadamente 54% / 60% / 67% / 73% del pool
desnudo de su etapa. Ninguna restaura el depósito completo.

El objetivo es medir el recurso en acciones adicionales:

- técnica base: ~6 Qi;
- defensiva típica: ~7 Qi;
- AOE: ~9 Qi.

Por tanto LI Excepcional 20 equivale a unas 3 técnicas base adicionales antes
de considerar el turno consumido al beber.

## 3. Destilado Lunar

Se mantiene como híbrido, no como elixir puro:

```text
Impura       8 Qi + 1 impureza
Estable     14 Qi + purifica 1
Superior    20 Qi + purifica 2
Excepcional 26 Qi + purifica 2
```

Siempre queda por debajo de un puro LIII equivalente porque compra utilidad
adicional con parte de su presupuesto.

## 4. Recetas de Vitalidad

Propuesta de materiales:

```text
Básica LI · sencilla
1 raíz de sangre
1 hoja de claridad

Templada LII · normal
1 raíz de sangre
1 hongo de médula
1 pétalo de ceniza

Profunda LIII · difícil
1 raíz de sangre
1 médula fúngica
1 musgo lunar
1 rocío de niebla

Condensada LIV · muy difícil
1 raíz de sangre
1 semilla del trueno
1 fibra de tempestad
1 polvo de nube
```

Todos son renovables. Ninguna exige un drop único/jefe para una receta que el
jugador debe repetir varias veces para dominar.

## 5. Práctica necesaria

Con el sistema actual:

```text
Sencilla      Excepcional desde 2ª válida
Normal        desde 3ª
Difícil       desde 6ª
Muy difícil   desde 6ª
```

Por eso Profunda y Condensada usan cuatro unidades por intento, pero no piezas
únicas.

## 6. XP

Recomendación: mantener el núcleo actual.

XP máximo útil aproximado por receta:

```text
Sencilla      18,4
Normal        22,1
Difícil       25,8
Muy difícil   29,5
```

Las cuatro formulaciones de Vitalidad completamente dominadas aportan ~95,8
XP. Eso supera Novicio 50 pero no convierte una sola receta en método de
grindeo infinito porque la repetición llega a 0 XP.

El XP por encima del techo formal del Arco 1 debe conservarse. El jugador puede
acumular progreso aunque no pueda ascender a Aprendiz hasta un arco posterior.

## 7. Coste económico

Fabricar:

- 0 piedras directas;
- 0 Contribución gastada;
- consume ingredientes;
- consume 2 acciones/tiempo;
- fallo consume materiales y da 0 XP;
- salida base = 1 medicina.

Contribución sólo puede funcionar como requisito de acceso/permiso.

Poción común:

```text
2d4+3 HP
precio propuesto: 5 piedras
sin gasto de Contribución
```

Las cuatro formulaciones principales no deberían venderse de manera ilimitada:
su vía normal es Alquimia.

## 8. Remedios específicos

Antídoto de Jade y Bálsamo de Ceniza tienen un problema actual: Superior y
Excepcional apenas mejoran respecto de Estable.

Propuesta:

```text
Impura       cura grado I +1 impureza
Estable      cura grado I
Superior     cura grado I + purifica 1
Excepcional  cura grado I + purifica 2
```

No aumenta el grado máximo curable en Arco 1.

## 9. Lo que no tocaría

Por ahora conservar:

- Píldora de Purificación: 1 / 3 / 4 / 5;
- Remiendo Meridiano:
  impura = repara1 + impureza1
  estable = repara1
  superior = repara1 + purifica1
  excepcional = repara2 + purifica1.

Deben pasar después por economía/disponibilidad, no por rediseño funcional.

## 10. Estado

HP está ratificado.

Qi, ingredientes, economía y mejoras de remedios específicos permanecen como
propuesta hasta aprobación humana.

No se modifica ver74/runtime.
