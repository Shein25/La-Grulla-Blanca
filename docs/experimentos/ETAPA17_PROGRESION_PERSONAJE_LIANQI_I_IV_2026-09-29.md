# ETAPA 17 — Progresión del personaje LianQi I–IV

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: CERRADA COMO CONTRATO PROVISIONAL ESTRUCTURAL

## 1. Stats iniciales: fijos, no aleatorios

Los stats nucleares desnudos de combate serán fijos.

Motivos:
- evita reroll de personajes buscando una tirada superior;
- mantiene reproducible el balance;
- hace que las diferencias nazcan de raíz, técnicas, equipo, Concordancias y decisiones;
- evita castigos permanentes por mala suerte inicial.

La aleatoriedad futura puede existir en rasgos narrativos, botín, encuentros o talentos con presupuesto equivalente, pero no en el baseline bruto de combate.

## 2. Baseline desnudo LianQi I

Antes de raíz, equipo, buffs o técnicas:

| Stat | Valor | Estado |
|---|---:|---|
| HP máximo | 30 | PROVISIONAL |
| Qi máximo | 31 | PROVISIONAL |
| Precisión | 100 | CANON |
| Evasión | 5 | PROVISIONAL |
| DEF | 1 | PROVISIONAL |
| Control | 0 | PROVISIONAL |
| Tenacidad | 0 | PROVISIONAL |
| Crítico | 5% | CANON |
| Daño crítico | x1.50 | CANON |
| Penetración % | 0 | CANON baseline |
| Penetración plana | 0 | CANON baseline |
| bono daño % | 0 | CANON baseline |
| Absorción | 0 | sin fuente activa |

No existe un stat universal de ATQ que suba automáticamente por cultivo.

## 3. Aplicación de raíz

La raíz se aplica después del baseline fijo.

- Fuego: HP30, Qi31, Prec100, EVA5, DEF1, +10% daño directo, crítico10%.
- Metal: Prec105, Penetración %10, resto baseline.
- Agua: Control5 y costes Qi compatibles x0.90 antes del redondeo.
- Tierra: HP33 tras +10% HP, Tenacidad5, DEF sigue1 fuera de técnicas.
- Viento: EVA15, daño crítico x1.55, resto baseline.

No hay tirada aleatoria adicional.

## 4. Progresión estructural por etapa

Se adopta provisionalmente:

| Etapa | Nombre | HP | Qi | Puntos ganados | Total puntos | Acceso |
|---|---|---:|---:|---:|---:|---|
| LianQi I | Percepción | 30 | 31 | 0 | 0 | BASE |
| LianQi II | Circulación | 36 | 37 | +2 | 2 | Tramo I |
| LianQi III | Consolidación | 42 | 43 | +2 | 4 | Tramo II |
| LianQi IV | Refinamiento | 48 | 49 | +2 | 6 | Tramo III |

Regla de avance:

- +6 HP;
- +6 Qi;
- +2 puntos de técnica;
- +1 nuevo techo de Tramo.

No suben automáticamente otras estadísticas nucleares.

## 5. Por qué Qi 31→37→43→49

Ofensivas base coste6:

- LianQi I: 5 usos;
- LianQi II: 6;
- LianQi III: 7;
- LianQi IV: 8.

Defensiva coste7 + ofensivas coste6:

- Qi31: defensa +4 ofensivas = 5 acciones;
- Qi37: defensa +5 = 6;
- Qi43: defensa +6 = 7;
- Qi49: defensa +7 = 8.

Agua, con defensiva efectiva6, obtiene la misma cantidad total de acciones.

La igualdad conseguida en ETAPA16 se conserva en todas las etapas.

## 6. AOE y secuencias mixtas

AOE base cuesta9.

Usos AOE puros:

- Qi31: 3;
- Qi37: 4;
- Qi43: 4;
- Qi49: 5.

Una AOE9 seguida de ofensivas6:

- Qi31: AOE +3 ofensivas = 4 acciones;
- Qi37: AOE +4 = 5;
- Qi43: AOE +5 = 6;
- Qi49: AOE +6 = 7.

Defensiva7 + AOE9 + ofensivas6:

- Qi31: 4 acciones totales;
- Qi37: 5;
- Qi43: 6;
- Qi49: 7.

Las ramas de Eficiencia pueden cruzar umbrales adicionales deliberadamente; ése es su premio de build y deberá revalidarse por etapa.

## 7. Economía de puntos de técnica

Cada avance II/III/IV concede +2 puntos de técnica.

Total disponible al llegar a LianQi IV: 6 puntos.

Cada raíz posee inicialmente tres técnicas básicas:
- unitarget;
- defensiva;
- AOE.

Cada técnica posee tres Tramos.

Máximo teórico para cerrar las tres técnicas: 3 técnicas x 3 Tramos = 9 puntos.

El jugador sólo recibe 6, por lo que debe elegir entre profundizar y repartir.

## 8. Reglas para gastar puntos

1. un nodo cuesta 1 punto;
2. sólo puede elegirse una de las tres opciones de cada Tramo;
3. Tramo I requiere LianQi II;
4. Tramo II requiere LianQi III;
5. Tramo III requiere LianQi IV;
6. para comprar Tramo II de una técnica debe existir cualquier elección de Tramo I en esa técnica;
7. para comprar Tramo III debe existir cualquier elección de Tramo II;
8. no es necesario seguir la misma identidad de rama;
9. los puntos pueden guardarse;
10. una técnica aprendida tarde puede comprar Tramos inferiores mientras el reino actual los permita.

## 9. Ejemplos de builds con 6 puntos

Dos especialistas:
- unitarget III = 3;
- defensiva III = 3;
- AOE base = 0.

Equilibrado:
- unitarget II = 2;
- defensiva II = 2;
- AOE II = 2.

Especialista + cobertura:
- unitarget III = 3;
- defensiva II = 2;
- AOE I = 1.

## 10. Cómo afecta el cultivo a las habilidades

No existe multiplicador global por reino para daño, DEF, Precisión, Evasión o Control.

El cultivo afecta una técnica por cuatro vías:

A. Desbloqueo:
cada etapa abre un nuevo Tramo.

B. Puntos:
el jugador decide qué técnicas realmente se refinan.

C. Más Qi:
la técnica puede usarse más veces durante un combate; el coste no baja automáticamente.

D. Escalado por recurso:
una fórmula que use porcentaje de Vida máxima se recalcula con el nuevo HP máximo.

## 11. Ejemplos de escalado natural por HP

HP:
30 → 36 → 42 → 48.

Cuerpo-Horno base, 25% HP:
7.5 → 9.0 → 10.5 → 12.0 de reserva.

Ruta Barrera45%:
13.5 → 16.2 → 18.9 → 21.6.

Espejo base, 24% HP:
7.20 → 8.64 → 10.08 → 11.52.

Ruta Reserva42%:
12.60 → 15.12 → 17.64 → 20.16.

Curaciones de Piel, 5% HP:
1.50 → 1.80 → 2.10 → 2.40.

Los umbrales de Piel también crecen con HP:
- impacto fuerte = 10% HP;
- Vida baja = 30% HP.

## 12. Qué no escala automáticamente con el reino

Armadura de Plata:
las Placas y su DEF permanecen planas salvo ramas.

Paso de Nube:
la Evasión otorgada permanece plana salvo ramas.

Golpes ofensivos y AOE:
el daño base no recibe multiplicador automático de cultivo.

Palma, Destello, Latigazo, Golpe, Lanza y las AOE mejoran mediante:
- ramas;
- raíz;
- equipo;
- Concordancias;
- buffs;
- otros sistemas explícitos.

## 13. Separación de responsabilidades

El reino expresa:
- capacidad;
- reserva;
- techo de refinamiento.

La build expresa:
- daño;
- defensa;
- precisión;
- control;
- especialización.

Dos personajes del mismo reino pueden tener el mismo HP/Qi estructural y capacidades muy diferentes por sus decisiones de puntos.

## 14. Estado provisional

Se promueve estructuralmente para Arco 1:

- baseline de combate fijo, no aleatorio;
- HP LianQi I = 30;
- Qi LianQi I = 31;
- EVA base = 5;
- DEF base = 1;
- Control base = 0;
- Tenacidad base = 0;
- HP +6 por etapa;
- Qi +6 por etapa;
- +2 puntos de técnica por avance II/III/IV;
- sin multiplicador global de técnica por reino.

Todo permanece PROVISIONAL salvo stats ya CANON globalmente.

## 15. Pendientes de validación final

Todavía deben revalidarse con enemigos de etapa:
- HP36/42/48 contra enemigos II–IV;
- Qi37/43/49 con costes avanzados;
- ramas de Eficiencia;
- DEF plana frente a daño superior;
- Evasión frente a Precisión superior;
- perfiles enemigos II–IV.

Siguiente bloque: construir perfiles enemigos autoritativos de LianQi II, III y IV y revalidar cada Tramo contra su etapa real.
