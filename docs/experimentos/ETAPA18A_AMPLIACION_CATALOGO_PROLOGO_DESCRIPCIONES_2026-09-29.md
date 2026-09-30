# ETAPA 18A — Ampliación de catálogo, Prólogo y descripciones de equipo

Fecha: 2026-09-29
Rama: experiment/combat-stat-contract-v0.1
Estado: **CERRADA COMO DISEÑO PROVISIONAL / ADQUISICIÓN Y MONTE CARLO DIFERIDOS**

## 1. Confirmación de ver74

La revisión de ver74 confirma dos comportamientos que se preservan conceptualmente.

### Descripciones de objetos

Los ítems ya usaban un campo `desc` y el texto era parte de la identidad examinable del objeto.

Ejemplos documentados en:
`docs/3C6A/ver74_extractos/05_items_pildora_piel_cobre_muneco_examen.md`

- Poción de sangre: descripción física + sabor/impureza;
- Píldora de consolidación;
- Hoja de claridad;
- manuales de técnicas.

Por tanto el catálogo nuevo exige:

```text
description
obligatoria para todo equipo
```

La interfaz futura de MIRAR/EXAMINAR debe mostrar:
1. nombre;
2. descripción diegética;
3. propiedades mecánicas estructuradas por separado.

No se incrustan números de balance dentro del flavor salvo que sean información deliberadamente visible.

### Equipo del Prólogo

ver74 creaba al personaje con:
`["pocion", "uniforme", "espada_madera"]`

y el origen callejero añadía `cuchillo_hueso`.

El contrato 3C.6 corrigió esto:
- quitar entrega automática de uniforme/espada en creación;
- entregar equipo en `descansillo`;
- one-shot `equipoInicialEntregado`;
- preservar beneficios de origen.

Informe de implementación 3C.6 confirma:
> uniforme y espada entregados una sola vez al entrar al descansillo.

## 2. Dotación exacta del Prólogo

El jugador NO recibe equipo de secta durante la creación.

Después del diagnóstico de raíz, al entrar por primera vez al `descansillo`:

### Entrega garantizada

1. **Uniforme gris de aspirante**
   - ID: `uniforme_gris_aspirante`
   - Slot: VESTIDURA
   - HP +1
   - DEF +0.25
   - se equipa automáticamente.

2. **Espada de madera de entrenamiento**
   - ID: `espada_madera_entrenamiento`
   - Slot: ARMA
   - Precisión +1
   - campesino/escolar: se equipa automáticamente.

### Origen callejero

Conserva:
- **Cuchillo de hueso pulido**;
- recibe igualmente la espada de práctica;
- mantiene ambas armas;
- el Prólogo puede usar esta situación para enseñar cambio de arma.

No se obliga al callejero a perder su objeto de origen.

### Consumibles

Esta etapa sólo redefine EQUIPO.

Consumibles, materiales, píldoras y manuales quedan fuera del reemplazo y se revisarán en sus auditorías correspondientes.

Por tanto no se añade ni elimina aquí la Poción de Sangre por razones de equipo.

## 3. Reemplazo completo de equipo legacy

Cuando se implemente el catálogo nuevo:

```text
equipo nuevo
REEMPLAZA
equipo legacy
```

No podrán coexistir ambos catálogos.

Mapa de migración previsto:

| ID legacy | Nuevo ID |
|---|---|
| espada_madera | espada_madera_entrenamiento |
| uniforme | uniforme_gris_aspirante |
| cuchillo_hueso | cuchillo_hueso_callejero |
| anillo_herrumbroso | anillo_hierro_oxidado |
| espada_hierro | espada_hierro_equilibrada |
| tunica_reforzada | tunica_reforzada_trama_cobre |
| bandana | bandana_cuero_reforzada |
| sandalias_viento | sandalias_corriente_ligera |
| amuleto_colmillo | amuleto_colmillo_montado |

Guardia:
- los IDs legacy no pueden reutilizarse como IDs del catálogo nuevo;
- migración de saves será obligatoria al implementar runtime;
- todavía NO se modifica runtime.

## 4. Catálogo ampliado

El catálogo pasa:

```text
58 -> 68 piezas
```

Distribución:

| Etapa | Piezas |
|---|---:|
| LianQi I | 14 |
| LianQi II | 21 |
| LianQi III | 19 |
| LianQi IV | 14 |

Por slot:

| Slot | Piezas |
|---|---:|
| Arma | 11 |
| Tocado | 7 |
| Vestidura | 7 |
| Brazales | 6 |
| Fajín | 5 |
| Piernas | 5 |
| Calzado | 5 |
| Amuleto | 6 |
| Pulsera | 6 |
| Anillo | 9 |
| Tesoro Espiritual | 1 |

El Tesoro Espiritual único sigue siendo:
**Espejo de Pulso Velado**.

No se añadió ningún tesoro extra.

## 5. Diez nuevas piezas

### LianQi I

**Cinta de patio del aspirante**
- Tocado;
- +1 Precisión;
- +1 Tenacidad;
- alternativa temprana de consistencia.

**Anillo de cobre sin sello**
- Anillo;
- +1 Qi;
- +1 Control;
- primera opción de accesorio técnico.

### LianQi II

**Pulsera de tensión meridiana**
- Pulsera;
- +2% daño directo de técnicas;
- primera pieza ofensiva de pulsera.

**Calzas de guardia externa**
- Piernas;
- +2 HP;
- +2 Tenacidad;
- opción de patrulla/supervivencia.

**Anillo de reserva menor**
- Anillo;
- +2 Qi;
- +1 Precisión;
- continuidad con consistencia.

### LianQi III

**Fajín de respiración larga**
- Fajín;
- +4 Qi;
- +1 Evasión.

**Brazales de aguja de plata**
- Brazales;
- +2 Precisión;
- +3 pp Penetración.

**Amuleto de flujo contenido**
- Amuleto;
- +2% daño directo de técnicas;
- +2 Qi.

### LianQi IV

**Vestidura del Ala Cerrada**
- Vestidura;
- +4 HP;
- +3 Tenacidad;
- +0.25 DEF.

**Pulsera del meridiano profundo**
- Pulsera;
- +5 Qi;
- +3 Control.

## 6. Daño de técnicas por equipo tras la ampliación

Piezas actuales con `technique_direct_damage_percent`:

| Pieza | Etapa | Bono |
|---|---|---:|
| Amuleto de colmillo montado | II | +3% |
| Pulsera de tensión meridiana | II | +2% |
| Sable de anillo gris | III | +2% |
| Amuleto de flujo contenido | III | +2% |
| Hoja de seis corrientes | IV | +3% |
| Anillo de relevo | IV | +3% |

Máximo teórico por slots disponibles:

```text
LianQi I   0%
LianQi II  5%
LianQi III 7%
LianQi IV  11%
```

Ese máximo exige sacrificar varios slots a una build ofensiva específica.

No es el perfil esperado.

## 7. Contrato de descripción

Todos los 68 objetos contienen ahora:
`description`

No quedan placeholders.

La descripción:
- debe explicar aspecto, material, desgaste, manufactura o sensación espiritual;
- no debe parecer tooltip técnico;
- debe ser coherente con procedencia y etapa;
- puede insinuar función sin revelar fórmulas ocultas.

Ejemplo:

**Espejo de Pulso Velado**

> Un espejo de bronce ennegrecido, no más grande que una palma. No devuelve el rostro con fidelidad: bajo cierta luz muestra primero el pulso del qi, y sólo después a quien lo sostiene.

Los stats y efectos se muestran aparte.

## 8. Validaciones de catálogo

PASS:
- 68 IDs únicos;
- 68/68 con descripción;
- 0 placeholders;
- 0 IDs legacy reutilizados;
- 1/1 Tesoro Espiritual;
- dotación de Prólogo referencia IDs existentes;
- piezas nuevas dentro de sus presupuestos diagnósticos;
- perfiles existentes sin overflow de slots.

## 9. Trabajo deliberadamente diferido

Por decisión de diseño:

### NO hacer ahora
- auditoría integral de cada adquisición;
- reconciliación definitiva de todos los precios M08–M17;
- Monte Carlo masivo de equipo;
- integración del catálogo al Colab principal;
- implementación runtime;
- migración real de saves.

### Hacer después

**Auditoría integral de adquisición**
- verificar NPC;
- misión;
- momento exacto;
- permiso;
- piedras;
- Contribución;
- stock/repetibilidad;
- incompatibilidades narrativas.

Después:

**Registro y simulación masiva en Colab**
- NAKED;
- MANDATORY;
- EXPECTED;
- builds especializadas;
- HIGH_ROLL;
- sin sobrecargar el diseño antes de tiempo.

## 10. Estado

```text
CATÁLOGO                 68 piezas
DESCRIPCIONES            68/68 PASS
PRÓLOGO EQUIPO            CERRADO PROVISIONAL
TESOROS                   1 Arc1
REEMPLAZO LEGACY          CONTRATO DEFINIDO
ADQUISICIÓN INTEGRAL      DIFERIDA
COLAB MASIVO              DIFERIDO
RUNTIME                   SIN CAMBIOS
```
