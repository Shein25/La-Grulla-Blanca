# LAB — A/B de techo de impacto · cap 95 vs cap 100

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / COMPARACIÓN DE POLÍTICA / NO CAMBIA CANON**

## Pregunta

Comparar:

```text
MODELO A — contrato actual
P(hit) = clamp(Precisión - Evasión, 5, 100)

MODELO B — variante
P(hit) = clamp(Precisión - Evasión, 5, 95)
```

La motivación es evitar que criaturas con Precisión alta acierten
automáticamente a objetivos sin Evasión.

## Configuración

Se mantuvo el candidato de duelo extendido:

- jugador: HP 30 / Qi 30 / DEF 1;
- Evasión base barrida: 0 / 5 / 10;
- Viento añade +10 Evasión;
- enemigo: HP 28 / EVA 20 / DEF 2;
- daño enemigo: `2d4+1`;
- Precisión enemiga: 80 / 85 / 90 / 95 / 100 / 105;
- jugador actúa primero;
- técnicas narrow + ataque básico 1d4+4.

Runner:

`experimentos/balance_nuevo/phase_c_accuracy_cap_lab.py`

## Hallazgo 1 — con EVA base 5, cap 95 y cap 100 son iguales hasta PREC 100

Porque:

```text
PREC 100 - EVA 5 = 95
```

El cap 95 todavía no interviene.

Confirmación de 100.000 duelos por raíz:

```text
EVA base 5 / PREC enemigo 100

cap 95
win medio       82.672%
hit enemigo     92.991%

cap 100
win medio       82.696%
hit enemigo     93.001%
```

La diferencia es ruido de Monte Carlo.

Conclusión:

> cambiar a cap 95 NO arregla el problema principal si el jugador ya posee
> algo de Evasión; lo que realmente controla el hit rate es la Precisión
> propia de cada criatura.

## Hallazgo 2 — cap 95 actúa como una esquiva gratuita para EVA 0

Con EVA base 0 y Precisión enemiga 100:

```text
cap 95
hit enemigo agregado ≈ 93.99%
win medio             ≈ 82.15%

cap 100
hit enemigo agregado ≈ 97.99%
win medio             ≈ 80.01%
```

El promedio de hit no es exactamente 95/100 porque Viento conserva +10 EVA.

Por raíz:

| Raíz | Hit enemigo cap95 | Hit enemigo cap100 |
|---|---:|---:|
| Fuego | ~95% | 100% |
| Metal | ~95% | 100% |
| Agua | ~95% | 100% |
| Tierra | ~95% | 100% |
| Viento | ~90% | ~90% |

Esto significa que el cap 95 concede un 5% de evasión implícita a cuatro
raíces que tienen EVA 0.

## Hallazgo 3 — cap 95 comprime la identidad de Viento contra precisión alta

En EVA base 0 / PREC 100:

```text
cap 100
normal → 100% hit
Viento → 90% hit
ventaja de Viento = 10 puntos

cap 95
normal → 95% hit
Viento → 90% hit
ventaja de Viento = 5 puntos
```

La ventaja efectiva de +10 Evasión queda reducida a la mitad.

Con Precisión enemiga 105:

```text
cap 95
normal: clamp(105 - 0, 5, 95) = 95
Viento: clamp(105 - 10, 5, 95) = 95

→ Viento obtiene 0 puntos efectivos de ventaja en hit rate.
```

El cap impide que la Evasión se exprese en ese tramo porque ambos resultados
chocan contra el mismo techo.

## Hallazgo 4 — bajar Precisión enemiga sí produce diferenciación limpia

Con el contrato actual cap 100 y EVA base 5:

| Precisión enemiga | Hit normal esperado | Hit contra Viento |
|---:|---:|---:|
| 85 | 80% | 70% |
| 90 | 85% | 75% |
| 95 | 90% | 80% |
| 100 | 95% | 85% |

Resultados agregados del duelo:

| Precisión | Win medio jugador | HP restante medio |
|---:|---:|---:|
| 85 | ~89.6% | ~42.8% |
| 90 | ~87.8% | ~39.6% |
| 95 | ~85.3% | ~36.5% |
| 100 | ~82.7% | ~33.3% |

Esto cambia gradualmente la presión sin regalar una esquiva universal.

## Lectura sistémica

### Cap 95

Ventajas:
- evita 100% de hit por acciones normales;
- añade una pequeña incertidumbre permanente.

Costes:
- entrega evasión implícita incluso a quien posee EVA 0;
- reduce el valor marginal de Evasión cerca del techo;
- comprime la diferencia de Viento;
- también comprime la utilidad de Precisión >95 cuando el objetivo tiene poca
  Evasión.

### Cap 100

Ventajas:
- Precisión y Evasión conservan una relación transparente;
- +10 Evasión significa realmente -10 puntos de impacto mientras no intervenga
  otro límite;
- alta Precisión puede contrarrestar Evasión de forma legible;
- permite diferenciar monstruos por su propia Precisión.

Coste:
- una criatura con PREC 100 contra EVA 0 acierta 100%;
- por tanto, PREC 100 no debe usarse como valor universal de monstruos.

## Resultado del A/B

**El cap 100 actual es el candidato más sano.**

No porque todos los enemigos deban tener 100 Precisión, sino precisamente por
lo contrario:

> mantener cap 100 y diseñar la Precisión criatura por criatura conserva mejor
> el significado de Precisión/Evasión que introducir un fallo gratuito del 5%.

El problema detectado estaba en el perfil de monstruo del test, no en la
fórmula.

## Hipótesis siguiente

Para LianQi I, probar como banda principal:

```text
enemigo común
PREC ~85–90

enemigo ágil/competente
PREC ~90–95

enemigo entrenado
PREC ~95–100

especialista
PREC >100
```

Esto sigue siendo LAB y no es todavía una tabla de bestiario.

## Próximo paso

Mantener el contrato actual cap 100 durante los siguientes tests y usar
**PREC 90** como nuevo centro LAB para enemigo ordinario.

Luego:

1. probar Arrastre;
2. probar Peso;
3. volver a comparar raíces;
4. decidir si PREC 90 pasa a PROVISIONAL como referencia ordinaria.

