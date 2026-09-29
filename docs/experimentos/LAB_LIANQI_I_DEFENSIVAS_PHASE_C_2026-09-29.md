# LAB — LianQi I PHASE C · Espejo de Luna y Piel de Cobre

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **LAB / DEFENSIVAS BASE / NO CANON**

## Objetivo

Comprobar si una técnica defensiva justifica gastar una acción completa y Qi
antes de continuar con el resto de PHASE C.

Baseline LAB:

- jugador: HP base 30 / Qi 30 / DEF 1 / EVA 5;
- enemigo: HP 28 / PREC 90 / EVA 20 / DEF 2 / ataque `2d4+1`;
- Arrastre efectivo 50% para Agua;
- Peso `STACK_REFRESH` para Tierra;
- ataque básico `1d4+4`;
- técnicas ofensivas narrow;
- cap de impacto 100.

Runner:

`experimentos/balance_nuevo/phase_c_defensives_lab.py`

## 1. Espejo de Luna

Base provisional actual:

- coste base 7 Qi;
- Agua principal lo convierte en 6 Qi efectivos;
- duración 3 turnos;
- Absorción = 12% HP máximo;
- Reflujo = 25% de la reserva máxima al comienzo del turno si queda reserva.

Con HP30, 12% equivale a sólo 3.6 de Absorción.

### Ofensiva pura vs apertura defensiva

Confirmación de 120.000 duelos por punto seleccionado:

| Estrategia | Absorción | Win rate | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|---:|
| Sólo ofensiva + Arrastre | — | 86.83% | 6.20 | 42.72% | 63.62% |
| Espejo apertura | 12% | 81.36% | 7.32 | 36.15% | 90.26% |
| Espejo apertura | 22% | 88.17% | 7.49 | 46.51% | 90.49% |
| Espejo apertura | 24% | 89.06% | 7.51 | 48.44% | 90.42% |
| Espejo apertura | 25% | 89.65% | 7.52 | 49.23% | 90.37% |

### Lectura

**12% falla el criterio principal.**

La reserva suele romperse en el primer impacto conectado. Cuando llega a 0,
Reflujo deja de funcionar, por lo que la identidad de la técnica apenas llega
a expresarse.

La zona de transición aparece aproximadamente en **21–22% HP**.

- 22% ya supera ligeramente la estrategia puramente ofensiva.
- 24–25% da valor defensivo visible sin llegar todavía a una seguridad extrema.
- El 30% histórico no se reutilizó como autoridad; vuelto a probar en el
  sistema nuevo resulta fuerte, pero ya no parece necesario llegar tan alto.

Rango principal LAB para continuar:

`Espejo de Luna = 22–25% HP máximo de Absorción`

No tocar Reflujo todavía.

## 2. Piel de Cobre

Base provisional:

- coste 7 Qi;
- duración 3 turnos;
- al activar: +2 DEF y +1 Arraigo;
- cada Arraigo: +1 DEF y +3 Tenacidad;
- máximo 3;
- puede ganar Arraigo por daño directo a Vida;
- al máximo puede extender una vez la duración.

Tierra principal parte de 33 HP por su +10% de Vida.

Al activar Piel, con DEF base1:

- DEF inicial efectiva durante Piel: 4;
- DEF posible a 3 Arraigos: 6.

### Resultado con coste 7

| Estrategia | Win rate | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|
| Sólo ofensiva + Peso | 91.85% | 5.24 | 43.07% | 33.50% |
| Piel apertura · coste 7 | 94.47% | 7.10 | 53.99% | 96.97% |

**Piel sí justifica defensivamente el turno.**

Pero aparece un problema económico:

- Qi30 − Piel7 = 23;
- Golpe de Montaña cuesta 6;
- caben sólo 3 Golpes;
- quedan 5 Qi que no alcanzan para otra técnica.

Eso fuerza el ataque básico en casi todos los combates.

### Sensibilidad a coste 6

Con coste6:

- Qi30 − Piel6 = 24;
- caben 4 Golpes de Montaña.

Resultado:

| Estrategia | Win rate | Turnos | HP restante | Usa básico |
|---|---:|---:|---:|---:|
| Piel apertura · coste 6 | 96.28% | 6.60 | 60.85% | 67.08% |

El salto demuestra que el coste de Piel está fuertemente acoplado al Qi máximo
30 y a los bloques discretos de coste6.

No debe cerrarse coste6 ni coste7 antes de cerrar PHASE B.

## 3. Lectura sistémica

### Espejo

Problema principal:

`magnitud demasiado pequeña → se rompe en un impacto → Reflujo no participa`

Variable a recalibrar: **Absorción base**.

### Piel

Problema principal:

`defensa sí funciona → coste7 + Qi30 deja 5 Qi muertos → fallback excesivo`

Variable a revisar: **economía de Qi**, no la DEF de Piel.

## 4. Hallazgo nuevo para PHASE B

PHASE B no puede cerrarse contando sólo cuántos ataques ofensivos caben desde
Qi lleno.

También debe evaluar secuencias mixtas:

- ofensiva6;
- defensiva6 + ofensivas6;
- defensiva7 + ofensivas6;
- técnicas base7 con reducción de Agua.

Qi30 parece perfecto para cinco técnicas de coste6, pero puede ser incómodo
para una defensiva de coste7.

## 5. Estado

Espejo de Luna:

- 12% HP → **FAIL LAB como magnitud base**;
- 22–25% HP → **zona prometedora LAB**.

Piel de Cobre:

- magnitud defensiva base → **PASS LAB inicial**;
- coste6/7 → **NO CERRAR** hasta revisar Qi.

## 6. Próximo paso

Reabrir PHASE B sólo para **economía mixta** y barrer Qi máximo alrededor de:

- 28;
- 30;
- 32;
- 34;
- 36.

Después volver a Espejo/Piel con una economía de recurso mejor justificada.

