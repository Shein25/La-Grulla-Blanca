# ETAPA 17C — Potencia intrínseca de cultivo y papel del equipo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO CONTRATO PROVISIONAL ESTRUCTURAL**

## Objetivo

Corregir una limitación del modelo previo:

> ascender de reino debe hacer al cultivador intrínsecamente más fuerte incluso
> desnudo, sin convertir el cultivo en un +X% a todas las estadísticas.

El resto del crecimiento queda deliberadamente en:

- equipo;
- ramas de técnica;
- Concordancias;
- buffs;
- recursos y sistemas explícitos.

No se modifica runtime/HTML.

---

# 1. Golpe básico por etapa

El ataque común gratuito escala con la transformación física/espiritual del cultivador.

| Etapa | Golpe básico | Media |
|---|---|---:|
| LianQi I | 1d4+4 | 6.5 |
| LianQi II | 1d4+5 | 7.5 |
| LianQi III | 1d4+6 | 8.5 |
| LianQi IV | 1d4+7 | 9.5 |

Crecimiento respecto de LianQi I:

- II: +15.38%;
- III: +30.77%;
- IV: +46.15%.

El Golpe básico sigue siendo:

- coste 0 Qi;
- una acción normal;
- inferior a una técnica especializada;
- elegible para modificadores que declaren ATAQUE_COMUN;
- NO una técnica.

---

# 2. Potencia de cultivo para daño directo de técnicas

Se introduce un escalar de magnitud base:

| Etapa | CULTIVATION_DIRECT_TECH_SCALAR |
|---|---:|
| LianQi I | x1.00 |
| LianQi II | x1.08 |
| LianQi III | x1.16 |
| LianQi IV | x1.24 |

Interpretación:

- representa una cultivation base más densa/poderosa;
- no es una estadística de ATQ;
- no aparece como +Ataque permanente;
- modifica sólo la magnitud base compatible del daño directo de una técnica.

Ejemplo con magnitud media10 antes de raíz/equipo:

- I: 10.0;
- II: 10.8;
- III: 11.6;
- IV: 12.4.

---

# 3. Orden de cálculo

Para una porción DIRECTA de daño de TÉCNICA compatible:

magnitud base de la técnica
→ escalar de cultivo de etapa
→ bonos planos compatibles
→ % ofensivos normales
→ crítico
→ daño recibido
→ DEF
→ Absorción
→ HP

El escalar de cultivo se aplica una sola vez y no se suma al pool de porcentajes ofensivos normales.

---

# 4. Qué recibe el escalar

Sí:

- Palma Ardiente: porción directa;
- Destello de Plata: porción directa;
- Latigazo de Marea: porción directa;
- Golpe de Montaña: porción directa;
- Lanza que Parte Nubes: porción directa;
- AOE iniciales: porciones directas compatibles;
- futuras técnicas cuyo efecto declare explícitamente cultivation_direct_scaling=true.

No:

- Golpe básico, porque ya tiene su propia progresión de dado;
- DOT/ticks;
- Reflect;
- Retaliation;
- Calor almacenado de Cuerpo-Horno;
- Robo de Vida;
- curaciones;
- Absorción;
- DEF;
- Evasión;
- Precisión;
- Control;
- Tenacidad;
- duración;
- cargas;
- recursos internos;
- daño secundario marcado no_offensive_rescale.

---

# 5. Efectos porcentuales de HP/Qi

No reciben el escalar de cultivo.

Ejemplos:

- Cuerpo-Horno 25% HP;
- Espejo 24% HP;
- curaciones 5% HP de Piel;
- thresholds 10%/30% HP.

Ya progresan porque cambia el recurso máximo de referencia. Aplicar además x1.08/x1.16/x1.24 sería doble escalado.

---

# 6. Defensa y estadísticas planas

El reino NO aumenta automáticamente:

- DEF;
- Precisión;
- Evasión;
- Crítico;
- Penetración;
- Control;
- Tenacidad.

La mejora desnuda defensiva se expresa principalmente mediante HP 30→36→42→48, mayor Qi, acceso a ramas y técnicas elegidas. El resto lo proporcionan principalmente equipo/build.

---

# 7. Papel del equipo

El equipo será la principal segunda capa de progresión cuantitativa.

El cultivo garantiza:

- cuerpo más resistente;
- reserva espiritual mayor;
- golpe común más fuerte;
- mayor potencia base de daño directo de técnicas;
- acceso a refinamientos.

El equipo puede aportar explícitamente:

- daño plano/% compatible;
- DEF;
- Precisión;
- Evasión;
- crítico;
- daño crítico;
- Penetración;
- Control;
- Tenacidad;
- HP/Qi;
- efectos reactivos y propiedades especiales.

No se fijan todavía presupuestos numéricos de equipo.

Guardia:

> no usar el equipo para reparar un baseline roto; el baseline debe ser jugable desnudo y el equipo debe especializar/amplificar.

---

# 8. Curva estructural vigente

| Etapa | HP | Qi | Golpe básico | Tech directa | Puntos |
|---|---:|---:|---|---:|---:|
| LianQi I | 30 | 37 | 1d4+4 | x1.00 | 0 |
| LianQi II | 36 | 43 | 1d4+5 | x1.08 | +2 |
| LianQi III | 42 | 49 | 1d4+6 | x1.16 | +2 |
| LianQi IV | 48 | 55 | 1d4+7 | x1.24 | +2 |

Total de puntos a LianQi IV: 6.

---

# 9. Estado

PROVISIONAL:

- progresión Golpe básico;
- escalar de daño directo de técnica;
- HP/Qi;
- economía de puntos.

No CANON hasta validar contra perfiles enemigos LianQi II–IV.

## Próximo bloque

Construir enemigos de LianQi II primero y validar:

1. personaje II desnudo;
2. Golpe básico7.5;
3. técnicas directas x1.08;
4. HP36/Qi43;
5. Tramo I;
6. posteriormente equipo como capa separada.