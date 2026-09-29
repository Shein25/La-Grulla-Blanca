# Pass 0 — sistema nuevo sin estadísticas legacy

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **VALIDACIÓN DE SENSIBILIDAD / NO ES LIANQI I**

## Guardia

Este test NO usa:

- HP/Qi de ver74;
- ATQ/DEF de ver74;
- probabilidades antiguas de impacto;
- daño de monstruos de ver74;
- conversiones de estadísticas antiguas a nuevas;
- equipo viejo.

Fuentes permitidas:

- contrato nuevo de combate;
- registro universal;
- técnicas nuevas aprobadas/provisionales;
- raíces nuevas cerradas;
- parámetros LAB declarados explícitamente.

## Qué puede comprobarse antes de fijar LianQi I

Como HP/Qi y perfiles enemigos nuevos por etapa todavía no están cerrados, este Pass no calcula TTK ni supervivencia.

Sí permite comprobar:

- efecto de Precisión/Evasión;
- efecto de DEF/Penetración;
- efecto de raíces;
- crítico;
- variabilidad de daño manteniendo igual media nominal;
- estabilidad del orden relativo entre técnicas.

## Distribuciones LAB

Para cada daño nominal se comparan dos distribuciones con la misma media:

| Nominal | estrecha | amplia |
|---:|---|---|
| 10 | 2d4+5 | 2d6+3 |
| 9 | 2d4+4 | 2d6+2 |
| 8 | 2d4+3 | 2d6+1 |
| 7 | 2d4+2 | 2d6 |
| 6 | 2d4+1 | 2d6−1 |

No son dados canónicos.

Su finalidad es separar:

```text
POTENCIA MEDIA
de
VARIANZA / SENSACIÓN DEL GOLPE
```

## Perfiles LAB

| Perfil | DEF | Evasión |
|---|---:|---:|
| LAB-A | 0 | 0 |
| LAB-B | 2 | 15 |
| LAB-C | 4 | 30 |
| LAB-D | 6 | 45 |

No corresponden a COMMON/ELITE/BOSS ni a ninguna etapa.

## Raíces y propiedades aplicadas

- Fuego: +10% directo y +5 pp crítico.
- Metal: +10 pp Penetración y +5 Precisión.
- Destello: +10 pp Penetración propia adicional.
- Agua: el +5 Control no aumenta daño directo.
- Tierra: HP/Tenacidad no aumentan daño directo.
- Viento: +10 Evasión al actor y +5% daño crítico.
- Lanza: +5 Precisión y +5 pp crítico propios.

Crítico universal: 5%, x1.50.  
Precisión normal de referencia: 100.

## Resultado — daño medio por acción

Distribución amplia; incluye fallos, crítico y DEF.

| Técnica | LAB-A | LAB-B | LAB-C | LAB-D |
|---|---:|---:|---:|---:|
| Palma | 11.54 | 8.11 | 5.29 | 3.06 |
| Destello | 9.22 | 6.86 | 4.53 | 2.67 |
| Latigazo* | 8.19 | 5.27 | 2.96 | 1.36 |
| Golpe* | 9.22 | 6.14 | 3.66 | 1.83 |
| Lanza | 8.43 | 5.80 | 3.35 | 1.62 |

`*` No se están contando Arrastre/Peso u otras utilidades persistentes; esta tabla mide sólo el impacto directo inmediato.

## Resultado — precisión efectiva del grid

| Técnica | LAB-A | LAB-B | LAB-C | LAB-D |
|---|---:|---:|---:|---:|
| Palma/Latigazo/Golpe | 100% | 85% | 70% | 55% |
| Destello/Lanza | 100% | 90% | 75% | 60% |

Esto sale únicamente del contrato nuevo:

```text
clamp(Precision - Evasion, 5, 100)
```

## Estrecha vs amplia

Ejemplo Palma LAB-C:

```text
2d4+5 → media por acción ≈5.27
2d6+3 → media por acción ≈5.29
```

pero el percentil alto cambia aproximadamente:

```text
estrecha p90 ≈9.2
amplia   p90 ≈10.85
```

Conclusión:

> con la misma media nominal, ampliar dados cambia sensación, extremos y probabilidad de remate; casi no altera el presupuesto medio.

Esto permite decidir la identidad de variabilidad de cada elemento separadamente del balance de potencia.

## Lectura provisional

1. El nuevo sistema de Precisión/Evasión produce degradación suave al aumentar Evasión.
2. La DEF plana castiga más a las técnicas de menor magnitud, como corresponde; su escala absoluta deberá fijarse junto a HP/daño de Etapa I.
3. Metal gana consistencia contra DEF mediante Penetración sin necesitar daño base extra.
4. Fuego conserva mayor presión directa por su raíz.
5. Viento gana consistencia por Precisión/crítico, no por daño base superior.
6. Agua no puede juzgarse por esta tabla hasta cerrar Control/Arrastre.
7. Tierra no puede juzgarse sólo por daño porque su raíz y Peso desplazan valor a supervivencia/fiabilidad posterior.

## Qué NO concluye este Pass

No concluye:

- HP inicial;
- Qi inicial;
- DEF/Evasión de un enemigo LianQi I;
- dados definitivos;
- TTK;
- supervivencia;
- valor final de Horno/Espejo/Paso/Piel/Armadura;
- crecimiento II–IV.

## Siguiente cierre necesario

Antes del primer benchmark serio de LianQi I deben definirse **desde cero**:

1. HP inicial nuevo.
2. Qi máximo inicial nuevo.
3. rango objetivo de daño recibido por acción.
4. DEF objetivo de enemigos de Etapa I.
5. Evasión objetivo de enemigos de Etapa I.
6. Tenacidad objetivo.
7. Control base de técnicas.
8. distribución de daño candidata de cada técnica base.

Una vez congelado ese paquete, el notebook Colab puede ejecutar automáticamente todas las matrices sin reescribir el simulador.
