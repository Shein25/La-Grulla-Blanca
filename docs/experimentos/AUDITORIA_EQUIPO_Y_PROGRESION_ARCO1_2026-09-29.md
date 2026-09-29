# Auditoría — equipo y progresión por etapas de LianQi

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **ARQUITECTURA DE BALANCE / SIN STATS LEGACY**

## 0. Propósito

Preparar el balance serio del Arco 1 teniendo en cuenta dos fuentes de crecimiento simultáneas:

1. recompensas por ascender de etapa;
2. equipo realmente obtenible durante cada etapa.

Las cifras antiguas de equipo quedan obsoletas. Sólo se preservan identidad, slot y fuente de obtención cuando esa fuente sigue existiendo.

---

## 1. Progresión de etapa

El contrato actual considera como control:

```text
cultivo
→ HP
→ Qi
→ acceso/puntos/desbloqueos
```

Pero el laboratorio debe permitir probar hipótesis alternativas, por ejemplo:

```text
+ Precisión por etapa
+ Evasión por etapa
+ DEF por etapa
+ crítico por etapa
+ Control/Tenacidad por etapa
+ % daño por etapa
```

sin convertir ninguna hipótesis en canon.

Se implementó:

`experimentos/balance_nuevo/progression_lab.py`

Permite comparar una política control contra políticas LAB y medir acumulación en LianQi I–IV.

### Barridos preparados

Por ascenso II/III/IV:

- Precisión: 0 / +2 / +5;
- Evasión: 0 / +2 / +5;
- DEF: 0 / +0.5 / +1;
- crítico: 0 / +1 / +2 pp;
- daño crítico: 0 / +2.5 / +5 pp;
- Control: 0 / +2 / +5;
- Tenacidad: 0 / +2 / +5;
- daño global: 0 / +2.5 / +5%.

Son **valores LAB para sensibilidad**, no recomendaciones finales.

Esto permitirá responder preguntas como:

> ¿qué ocurre si LianQi IV obtiene +3 DEF acumulada por cultivo además del equipo?

o:

> ¿dar +5 Precisión por etapa vuelve irrelevante la Evasión de los enemigos?

---

## 2. Estado actual del equipo existente

El runtime contiene diez objetos equipables identificables.

Sus estadísticas antiguas se ignoran por completo.

### Actualmente obtenibles

| Objeto | Slot | Fuente actual | Disponibilidad actual |
|---|---|---|---|
| espada de madera | mano | inventario inicial | inicio |
| cuchillo de hueso | mano | origen callejero | inicio, sólo ese origen |
| uniforme de discípulo externo | torso | inventario inicial | inicio |
| anillo herrumbroso | dedo | Camino de la Montaña | mundo inicial |
| amuleto de colmillo | cuello | drop del lobo espiritual | mundo inicial |

Con todos los gates iniciales cerrados existen 185 salas físicamente alcanzables. El Camino de la Montaña está dentro de ese conjunto. También hay presencia/territorio del lobo espiritual en zona inicialmente alcanzable.

Por tanto, con la estructura actual todos esos objetos pueden entrar en el ecosistema de **LianQi I**.

### Definidos pero sin fuente jugable actual

| Objeto | Slot | Estado |
|---|---|---|
| espada de hierro | mano | sin fuente activa |
| túnica reforzada | torso | sin fuente activa |
| bandana de cuero | cabeza | sin fuente activa |
| sandalias de viento | piernas | sin fuente activa |
| uniforme de discípulo interno | torso | sin fuente activa |

Motivo:

```text
CATALOGO = []
COMPRAR = pendiente
TIENDA = pendiente
SERVICIOS/CANJEAR = pendiente
QUESTS = {}
```

Por eso sus precios o estadísticas históricas no implican que sean realmente conseguibles.

---

## 3. Problema de progresión actual

No existe una curva de equipo LianQi I → II → III → IV.

Hoy la situación es aproximadamente:

```text
LianQi I
├─ arma inicial
├─ torso inicial
├─ anillo
├─ posible amuleto
└─ posible cuchillo por origen

LianQi II
└─ no existe una nueva capa de equipo garantizada

LianQi III
└─ no existe una nueva capa de equipo garantizada

LianQi IV
└─ no existe una nueva capa de equipo garantizada
```

Esto impide balancear correctamente los ascensos.

---

## 4. Nueva regla de diseño para objetos

Cada objeto nuevo/revisado deberá declarar:

```text
id
slot
etapa mínima
fuente
rareza/accesibilidad
stats del contrato nuevo
si compite con otro objeto del mismo slot
```

La etapa mínima no implica que el jugador lo obtenga automáticamente; indica el primer momento realista en que puede conseguirlo.

Ejemplo estructural:

```python
EquipmentItem(
    item_id="...",
    slot="torso",
    min_stage="LianQi_II",
    source_type="QUEST_REWARD",
    source_id="...",
    stats={
        "defense": ...,
        "hp_max": ...,
    },
)
```

---

## 5. Qué debe simularse por etapa

Para cada LianQi I–IV habrá al menos tres estados:

```text
NAKED
→ sólo cultivo + raíz + técnica

EXPECTED
→ equipo razonablemente obtenible a esa altura

HIGH_ROLL
→ mejor equipo plausible sin farm extremo
```

Opcionalmente:

```text
MINIMAL
→ jugador que ignoró exploración/comercio
```

Esto evita balancear enemigos contra un personaje perfectamente equipado cuando la mayoría aún no puede conseguir ese equipo.

---

## 6. Matriz de pruebas de ascenso

Cada salto deberá comparar:

```text
I → II
II → III
III → IV
```

separando:

1. crecimiento por cultivo;
2. nueva rama de técnica;
3. equipo nuevo disponible;
4. efecto combinado.

Ejemplo conceptual:

```text
A. mismos stats/equipo, sólo Tramo nuevo
B. HP/Qi nuevos, mismo equipo
C. stats extra LAB por ascenso
D. equipo esperado de la nueva etapa
E. todo combinado
```

Así podremos saber qué parte provoca una subida de poder excesiva.

---

## 7. Riesgo principal

Si damos estadísticas de combate por:

```text
cultivo
+
rama
+
equipo
```

la misma estadística puede crecer tres veces.

Ejemplo:

```text
+DEF por ascenso
+DEF de Piel/Armadura
+DEF del torso
```

Puede volver trivial el daño enemigo.

Por eso el laboratorio debe medir contribución marginal de cada capa, no sólo el resultado final.

---

## 8. Marco implementado

Archivos:

- `experimentos/balance_nuevo/progression_lab.py`
- `experimentos/balance_nuevo/equipment_lab.py`
- `experimentos/balance_nuevo/sim_core.py`
- `experimentos/balance_nuevo/run_matrix.py`
- `experimentos/balance_nuevo/COLAB_BALANCE_NUEVO.ipynb`

Las stats antiguas de los objetos no se importan.

---

## 9. Próximo trabajo recomendado

Antes de diseñar stats de objetos:

1. fijar LianQi I desnudo;
2. definir qué slots queremos que estén disponibles en cada etapa;
3. distribuir los diez objetos existentes o reemplazarlos;
4. decidir qué fuentes son:
   - inicial;
   - drop;
   - misión;
   - comercio;
   - contribución;
   - exploración;
5. crear stats nuevos de equipo;
6. ejecutar la matriz NAKED / EXPECTED / HIGH_ROLL;
7. probar políticas alternativas de recompensa por ascenso.

La economía del equipo y la progresión de cultivo deben cerrarse juntas, porque ambas determinan el crecimiento real de poder del Arco 1.
