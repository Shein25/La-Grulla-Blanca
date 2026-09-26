# Investigación — counters de absorción para la Grulla Fase I v0.1

**Fecha:** 2026-09-26  
**Estado:** EXPERIMENTAL / RUTA ALTERNATIVA AL NERF NUMÉRICO PURO  
**Rama:** `experiment/monster-adaptive-survival-lab-v0.1`

## 1. Motivo

Después de validar `G234_D1` como rebalance numérico seguro para Piel de Cobre, se abre una segunda hipótesis:

> mantener una Piel más fuerte contra ataques ordinarios, pero introducir ataques concretos capaces de atravesar, romper o castigar una absorción activa.

La idea preserva mejor la identidad de una burbuja poderosa y convierte el exceso de defensa en un problema de lectura táctica, no sólo de números.

No supersede todavía `G234_D1`.

## 2. Precedentes externos

Se revisaron ejemplos conocidos de diseño:

- **Warframe**: Toxin puede saltar escudos y dañar directamente la vida; otros tipos de daño reciben ventajas específicas contra escudos.
  - https://www.warframe.com/en/guides/quests/vox-solaris
  - https://www.warframe.com/es/patch-notes/pc/27-2-0
- **League of Legends**: Serpent's Fang usa una mecánica dedicada de anti-shield que reduce escudos existentes y futuros.
  - https://www.leagueoflegends.com/en-gb/news/game-updates/patch-11-5-notes/
- **Rainbow Six Siege**: determinadas fuentes, entre ellas explosiones y efectos concretos, provocan Guard Break sobre portadores de escudo.
  - https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates/6VV3TGmosIJOUzjegN7eDh/y5s33-designers-notes
- **Genshin Impact**: algunos Shadowy Husks obtienen beneficios cuando sus ataques alcanzan personajes protegidos por escudo; el Defender puede aumentar ATK y reforzarse, mientras otras variantes generan escudos o curación.
  - https://genshin-impact.fandom.com/wiki/Shadowy_Husk:_Defender
  - https://www.hoyolab.com/article/19815297

Patrones útiles:

```text
BYPASS
parte o todo el daño ignora absorción

ANTI-SHIELD DAMAGE
el ataque hace más daño contra una burbuja activa

SHIELD BREAK
el ataque destruye o agota la defensa

STATE PUNISH
estar protegido activa una ventaja del atacante
```

## 3. Primer screening — Campanada como counter

Forma probada:

```text
Cobre flexible + Cobre grueso
2 PT
```

Piel CURRENT:

```text
Guardia 7
duración 3
reserva 21
```

Aproximación rápida de 2.000 duelos por escenario:

| Campanada | DEF13 | DEF14 |
|---|---:|---:|
| normal | 97,07% | 95,60% |
| 50% bypass | 95,94% | 93,78% |
| +25% daño si Piel activa | 90,55% | 88,02% |
| **+50% daño si Piel activa** | **80,96%** | **77,23%** |
| rompe/ignora Piel | 65,63% | 61,26% |

Conclusión inicial:

- sólo atravesar 50% no basta;
- +50% condicionado a Piel sí lleva CURRENT a una zona comparable con G234_D1;
- romper por completo la burbuja parece demasiado severo.

## 4. Problema de Campanada-only

Se hizo un retest focal de la antigua sinergia problemática:

```text
C02_F03
Cobre grueso + Lazo medido
CURRENT
```

Resultado aproximado:

| Modelo | DEF13 | DEF14 |
|---|---:|---:|
| normal | 93,14% | 86,82% |
| Campanada +50% vs Piel | 91,07% | 83,44% |
| Campanada rompe Piel | 90,90% | 82,92% |

El counter pierde eficacia porque Filamento puede cancelar Campanada. Si el control acierta, el ataque anti-absorción tampoco ocurre.

Por eso **Campanada no debe ser el único counter de Piel** si se conserva CURRENT.

## 5. Hipótesis mejor — Pata Inmóvil prepara un golpe anti-absorción

La secuencia permite un telegraph natural:

```text
Campanada
-> Pata Inmóvil
-> siguiente Golpe de Ala recibe propiedad anti-absorción
```

Ventajas:

- Filamento no puede cancelar este counter al cancelar Campanada.
- El jugador ve Pata antes del golpe especial.
- Piel sigue funcionando normalmente contra los demás ataques.
- Castiga especialmente la persistencia excesiva de una burbuja entre ciclos.
- Pata gana una identidad táctica adicional sin necesidad de convertirla en daño directo.

Screening focal sobre CURRENT óptima:

| Golpe preparado por Pata | DEF13 | DEF14 |
|---|---:|---:|
| normal | 97,07% | 95,60% |
| +50% daño vs Piel | 93,93% | 91,34% |
| rompe/ignora Piel | 83,01% | 78,43% |

Sobre la vieja `C02_F03` CURRENT:

| Golpe preparado por Pata | DEF13 | DEF14 |
|---|---:|---:|
| normal | 93,14% | 86,82% |
| +50% daño vs Piel | 83,80% | 74,83% |
| rompe/ignora Piel | 60,08% | 48,57% |
| +50% daño + 50% bypass | 78,24% | 67,56% |

Esto demuestra que ubicar el counter fuera de Campanada sí corta la sinergia Piel+Filamento.

## 6. Modelo intermedio prometedor

También se probó de forma focal:

```text
G345_D1
base Guardia 3 / duración 1
Endurecido 4
Grueso 5
```

Forma óptima de Piel:

```text
Cobre flexible + Cobre grueso
Guardia 5
duración 2
reserva 10
```

Resultados aproximados:

| Counter preparado por Pata | DEF13 | DEF14 |
|---|---:|---:|
| sin counter | 88,45% | 84,69% |
| +25% daño vs Piel | 84,61% | 80,38% |
| **+50% daño vs Piel** | **80,91%** | **76,17%** |
| 50% bypass | 85,63% | 81,29% |
| rompe/ignora Piel | 72,25% | 66,30% |

`G345_D1 + overload 50%` merece un grid completo porque:

- conserva una burbuja más fuerte que G234_D1;
- no queda cerca de 95–97%;
- crea un counter táctico específico;
- no exige que todos los enemigos del juego tengan anti-shield.

## 7. Decisión provisional

No seleccionar todavía entre:

```text
A) G234_D1 puro
B) G345_D1 + counter preparado por Pata
C) otro punto intermedio
```

Antes de decidir:

1. barrer las 16 ramas bajo el counter de Pata;
2. confirmar finalistas;
3. retestar Piel + Filamento;
4. retestar Paso + Piel;
5. sólo entonces volver a sensibilidad DEF13/14 y bonus de Pata.

El script de sensibilidad de Pata creado antes de esta investigación queda conservado, pero su ejecución final se pospone hasta resolver esta ruta.


## 8. Grid completo — G345_D1 + Pata OVERLOAD_150

Mecánica ensayada:

```text
Pata Inmóvil
-> mantiene +3 DEF contra la siguiente ofensiva del jugador
-> prepara el siguiente Golpe de Ala

Golpe preparado
-> si conecta con Piel de Cobre activa:
   daño bruto ×1,50
   después Piel absorbe normalmente
-> si falla:
   no hace daño
   el estado preparado se consume igualmente
```

Se conservaron:

- PIEL_READER;
- costes;
- burbuja persistente;
- reserva = Guardia × duración;
- no caducidad por rondas.

Grid:

```text
16 configuraciones Piel
× 27 formas raíz
× 2 DEF
× 5.000
=
4.320.000 duelos
```

Top:

| Configuración | Guardia | Duración | Reserva | DEF13 | DEF14 |
|---|---:|---:|---:|---:|---:|
| **Cobre flexible + Cobre grueso** | **5** | **2** | **10** | **81,08%** | **76,11%** |
| Cobre endurecido + Placas continuas | 4 | 2 | 8 | 72,33% | 66,65% |
| Cobre flexible + Placas continuas | 3 | 3 | 9 | 67,98% | 62,31% |
| Cobre sobrio + Cobre grueso | 5 | 1 | 5 | 67,60% | 61,45% |
| Cobre grueso | 5 | 1 | 5 | 66,89% | 60,73% |

## 9. Confirmación — 20.000

Finalistas:

```text
Cobre flexible + Cobre grueso
Cobre endurecido + Placas continuas
Cobre flexible + Placas continuas
```

Volumen:

```text
3 × 27 × 2 × 20.000
=
3.240.000 duelos
```

Resultado:

| Configuración | DEF13 | DEF14 |
|---|---:|---:|
| **Cobre flexible + Cobre grueso** | **80,96%** | **76,01%** |
| Cobre endurecido + Placas continuas | 72,58% | 67,06% |
| Cobre flexible + Placas continuas | 68,18% | 62,50% |

La confirmación reproduce el grid.

Comparación:

```text
CURRENT óptima original
97,13 / 95,54

G234_D1 óptima
82,61 / 77,91

G345_D1 + Pata OVERLOAD_150
80,96 / 76,01
```

El nuevo modelo llega a una magnitud similar a G234_D1, pero por una vía distinta:

- Piel conserva más fuerza contra golpes normales;
- la debilidad está concentrada en un ataque telegráfico;
- la persistencia entre ciclos tiene riesgo;
- la identidad de burbuja se mantiene.

## 10. Estado de la hipótesis

```text
AISLADO G345_D1 + PATA OVERLOAD_150   CONFIRMADO
PIEL + FILAMENTO                      PENDIENTE
PASO + PIEL                           PENDIENTE
TRIPLE                                PENDIENTE
DEF13 / DEF14                         NO SELECCIONAR AÚN
PATA +3                               SIGUE PROVISIONAL
```

No reemplazar todavía G234_D1. El siguiente test obligatorio es Piel + Filamento, porque Campanada-only ya demostró que un counter que Filamento pueda cancelar no resuelve el espacio combinado.


## 11. Sanity check combinado — G345_D1 + Piel/Filamento

Antes del grid deduplicado completo se probaron dos puntos de referencia a 2.000 duelos por escenario.

### C22_F00

```text
Piel:
Cobre flexible + Cobre grueso
Guardia 5
reserva 10
2 PT

Filamento base
0 PT
```

| Estado | DEF13 | DEF14 |
|---|---:|---:|
| sin counter de Pata | 76,29% | 64,33% |
| **Pata -> Golpe ×1,50 vs Piel** | **58,12%** | **46,78%** |

### C02_F03

```text
Piel:
Cobre grueso
Guardia 5
reserva 5
1 PT

Filamento:
Lazo medido
+1d4 al atar
1 PT
```

| Estado | DEF13 | DEF14 |
|---|---:|---:|
| sin counter de Pata | 67,23% | 55,08% |
| **Pata -> Golpe ×1,50 vs Piel** | **49,71%** | **38,74%** |

Lectura:

- a diferencia del counter exclusivo de Campanada, Filamento no puede borrar esta amenaza;
- la Piel fuerte sigue sirviendo en su propio duelo aislado;
- intentar apilar control + absorción paga un coste real de acciones;
- el counter puede estar siendo demasiado eficiente en MULTI_READER, por lo que todavía hace falta el grid completo antes de seleccionar este diseño.

Script reproducible preparado:

`benchmark/colab/grulla-phase1-piel-g345d1-pata-filamento-v0.1.py`

## 12. Estado actualizado

```text
G234_D1                           VALIDADO / FALLBACK SEGURO
G345_D1 + PATA OVERLOAD_150       AISLADO CONFIRMADO
G345_D1 PIEL+FILAMENTO             SANITY CHECK OK / GRID COMPLETO PENDIENTE

PATA SENSITIVITY ANTIGUA           PAUSADA, NO DESCARTADA
DEF13 / DEF14                      NO SELECCIONAR
FASE II                            NO TOCAR
FASE III                           NO TOCAR
```
