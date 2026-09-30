# ETAPA 18 — Equipo de Arco 1 · Diseño completo LianQi I–IV

Fecha: 2026-09-29  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **CATÁLOGO PROVISIONAL COMPLETO / LISTO PARA BENCHMARK EN COLAB**

## 1. Propósito

El equipo pasa a ser uno de los pilares centrales de la progresión de Arco 1, pero sin convertir el juego en una escalera MMO de colores, +1…+10 o reemplazo obligatorio de set en cada ascenso.

Principio:

```text
CULTIVO
→ crecimiento intrínseco

TÉCNICAS
→ identidad y dominio

EQUIPO
→ especialización, compensación y adaptación

CONCORDANCIAS
→ interacción avanzada posterior
```

El personaje debe ser viable desnudo. El equipo da margen y permite construir estilos de juego diferentes; ninguna misión principal se balanceará suponiendo el mejor set posible.

Este documento diseña **68 piezas** para los 13 slots previstos. No modifica runtime/HTML.

Fuentes machine-readable:
- `experimentos/balance_nuevo/equipment_arc1_catalog.json`
- `experimentos/balance_nuevo/equipment_arc1_catalog.py`

## 2. Base de investigación xianxia

Se adopta una estructura inspirada en patrones recurrentes del género, no una copia de una obra:
- las sectas entregan dotación al ascender de estatus;
- misiones producen piedras y/o mérito/contribución;
- pabellones y talleres concentran armas, ropas, objetos protectores y artefactos;
- existe una economía abierta y otra institucional;
- los objetos pueden ser compra, canje, servicio de especialista, premio, exploración o tesoro.

Referencias consultadas:
- I Shall Seal the Heavens, caps. 3–4 — promoción, ropa, Treasure Pavilion y objeto mágico;
- A Will Eternal, cap. 9 — misiones, piedras y merit points;
- Martial World, cap. 293 — Treasure Pavilion y refinería institucional;
- A Blind Swordsman's Sword Coffin, cap. 24 — Mission Pavilion, spirit stones y contribution points;
- An Alchemist's Path to Eternity, cap. 22 — espada voladora, armadura interior y artefactos.

## 3. Slots de Arco 1

| Grupo | Slot | Capacidad |
|---|---|---:|
| Marcial | Arma | 1 |
| Marcial | Tocado | 1 |
| Marcial | Vestidura | 1 |
| Marcial | Brazales | 1 |
| Marcial | Fajín | 1 |
| Marcial | Piernas | 1 |
| Marcial | Calzado | 1 |
| Accesorio | Amuleto | 1 |
| Accesorio | Pulsera | 1 |
| Accesorio | Anillo | 2 |
| Tesoro | Tesoro espiritual | 2 |

Los dos anillos usan el mismo catálogo de ANILLO. Los dos slots usan el mismo catálogo de TESORO_ESPIRITUAL, pero Arco 1 sólo ofrece un tesoro obtenible. El segundo slot queda vacío. Un objeto único no puede duplicarse.

No es objetivo llenar los 13 slots en LianQi I ni II.

## 4. Filosofía de poder

No hay rarezas MMO. `grade` describe fabricación/procedencia:
- MUNDANO_TRABAJADO;
- TRABAJO_ESPIRITUAL_MENOR;
- REFINADO_MENOR;
- REFINADO_DE_SECTA;
- ARTEFACTO_MENOR;
- ANTIGUO_FUNCIONAL.

Cada pieza tiene un `power_budget` diagnóstico, no visible al jugador.

Techos por pieza:

| Etapa | techo diagnóstico |
|---|---:|
| LianQi I | 1.50 |
| LianQi II | 2.50 |
| LianQi III | 3.50 |
| LianQi IV | 4.00 |

DEF plana es deliberadamente cara. El catálogo completo sólo permite un máximo teórico de **+1 DEF de equipo** en Arco 1, y recién desde LianQi III. LI/LII usan HP, Tenacidad y Evasión para aguante. Así no destruimos DEF_CAP2, Placas ni el valor de los impactos pequeños.

## 5. Economías y adquisición

### Piedras espirituales

Economía abierta/personal:
- compra en Mercado del Valle o Sauces;
- paga trabajos privados de Lu Cheng/Ning Cai;
- compite con consumibles y futura recuperación/cultivo.

Bandas orientativas:
- LII: 7–12 piedras por pieza normal;
- LIII: 16–22;
- LIV: 24–30 sólo para trabajos abiertos excepcionales.

### Contribución

Economía interna de secta:
- se gasta;
- no reduce Mérito;
- paga equipo institucional, talleres financiados por la secta y artefactos autorizados.

Economía temprana ya cerrada:

| Misión | Contribución |
|---|---:|
| M02 | 1 |
| M03 | 0 |
| M04 | 2 |
| M05 | 3 |
| M06 | 2 |
| M07 | 4 |
| **Total M02–M07** | **12** |

Propuesta de presupuesto posterior, todavía PROVISIONAL para sincronizar con misiones:

| LIII | Contribución |
|---|---:|
| M08 | 4 |
| M09 | 2 |
| M10 | 3 |
| M11 | 3 |
| M12 | 6 |
| **Total LIII** | **18** |

| LIV | Contribución |
|---|---:|
| M13 | 4 |
| M14 | 3 |
| M15 | 1 |
| M16 | 6 |
| M17 | 5 |
| M18 | 0 |
| **Total LIV** | **19** |

### Mérito

No se gasta como precio. Sigue siendo historial/prestigio y puede contribuir a autorizaciones narrativas, pero los objetos usan permisos semánticos concretos.

## 6. Quién provee qué

- **Lu Cheng**: armas, metal, ajustes, penetración, brazales metálicos; servicio, no profesión jugable.
- **Ning Cai**: textiles, cuero, calzado, vestiduras, amuletos montados y accesorios flexibles; servicio, no profesión jugable.
- **Jiang Rui**: dotación de patrulla y canjes de servicio territorial.
- **Chen Bo / Lan Meihua**: equipo médico, meridianos, Tenacidad/Control.
- **He Zhen / Wen Tao**: instrumentos de formaciones y tesoros auxiliares.
- **Song Rui**: piezas vinculadas a acceso documental; no “vende” un comercio abierto.
- **Qiao Ren**: autorizaciones institucionales y canjes ligados a disciplina/rango.
- **Duan Shibo**: producción/logística y equipo de mantenimiento.
- **Ji Xueying**: dotación tardía de Núcleo, no tienda común.
- **Mercado del Valle / artesanos de Sauces**: comercio abierto con piedras. Se mantienen como puestos genéricos hasta que el NPC mercader definitivo quede canónicamente cerrado.

## 7. Catálogo por etapa

### LianQi_I — 14 piezas nuevas

| Pieza | Slot | Stats | Efecto | Fuente | Precio | Perfil |
|---|---|---|---|---|---|---|
| **Espada de madera de entrenamiento** | ARMA | Prec +1 | — | Tao Ming · P | sin coste · dotación | PRECISION, BALANCED |
| **Cuchillo de hueso pulido** | ARMA | Básico plano +1; Prec -1 | — | exploración · P | sin coste · origen | BASIC_ATTACK, AGGRESSION |
| **Bastón de fresno de práctica** | ARMA | Ten +2 | — | Wei Jian · M03 | 1 contrib. | TENACITY, BALANCED |
| **Uniforme gris de aspirante** | VESTIDURA | HP +2 | — | Tao Ming · P | sin coste · dotación | HP, DEFENSE, BALANCED |
| **Bandana de lino simple** | TOCADO | Ten +2 | — | Ning Cai · M02 | 1 contrib. | TENACITY, ANTI_CONTROL |
| **Vendas de antebrazo de práctica** | BRAZALES | Prec +2 | — | Wei Jian · M03 | 1 contrib. | PRECISION |
| **Fajín de discípulo externo** | FAJIN | Qi +2 | — | Qiao Ren · M03 | sin coste · recompensa | QI, BALANCED |
| **Pantalón de viaje gris** | PIERNAS | HP +2 | — | Ning Cai · M02 | 1 contrib. | HP |
| **Zapatos de suela blanda** | CALZADO | EVA +2 | — | Ning Cai · M02 | 1 contrib. | EVASION |
| **Colgante de fragmento de jade** | AMULETO | Control +2 | — | camino_montana | exploración oculta | CONTROL |
| **Pulsera de fibra trenzada** | PULSERA | Qi +1; Ten +1 | — | Ning Cai · M02 | 1 contrib. | QI, TENACITY |
| **Anillo de hierro oxidado** | ANILLO | Qi +1 | +1 Qi al meditar (pendiente recuperación) | camino_montana | exploración oculta | QI, UTILITY |
| **Cinta de patio del aspirante** | TOCADO | Prec +1; Ten +1 | — | Tao Ming · M02 | 1 contrib. | PRECISION, TENACITY |
| **Anillo de cobre sin sello** | ANILLO | Qi +1; Control +1 | — | Tao Ming · M02 | 1 contrib. | QI, CONTROL |

### LianQi_II — 21 piezas nuevas

| Pieza | Slot | Stats | Efecto | Fuente | Precio | Perfil |
|---|---|---|---|---|---|---|
| **Espada de hierro equilibrada** | ARMA | Básico plano +1; Prec +2 | — | Lu Cheng · M04 | 12 piedras / 5 contrib. | BASIC_ATTACK, PRECISION, BALANCED |
| **Sable de patrulla del valle** | ARMA | Básico plano +2; Prec -1 | — | Lu Cheng · M04 | 10 piedras | BASIC_ATTACK, AGGRESSION |
| **Aguja de acero frío** | ARMA | Prec +3; Pen% +3 pp | — | Lu Cheng · M06 | 5 contrib. | PRECISION, PENETRATION |
| **Bandana de cuero reforzada** | TOCADO | Ten +3; HP +1 | — | Ning Cai · M04 | 7 piedras / 2 contrib. | TENACITY, HP |
| **Capucha del observador del valle** | TOCADO | Prec +3 | — | Puestos del Mercado del Valle · M05 | 7 piedras | PRECISION |
| **Sobretúnica de patrulla** | VESTIDURA | HP +3; Ten +2 | — | Jiang Rui · M04 | 3 contrib. | HP, DEFENSE |
| **Túnica de ruta de Sauces** | VESTIDURA | EVA +2; HP +2 | — | Artesanos de Sauces · M05 | 10 piedras | EVASION, HP |
| **Brazales de cuero cruzado** | BRAZALES | HP +2; Ten +2 | — | Ning Cai · M04 | 9 piedras / 3 contrib. | DEFENSE |
| **Brazales de pulso firme** | BRAZALES | Control +2; Ten +2 | — | Chen Bo · M06 | 3 contrib. | CONTROL, TENACITY |
| **Fajín de patrulla** | FAJIN | Qi +3; Ten +1 | — | Jiang Rui · M04 | 2 contrib. | QI, TENACITY |
| **Calzas de sendero de pinos** | PIERNAS | HP +3; EVA +1 | — | Ning Cai · M04 | 8 piedras | HP, EVASION |
| **Sandalias de corriente ligera** | CALZADO | EVA +4 | — | Artesanos de Sauces · M05 | 11 piedras | EVASION |
| **Botas de piedra húmeda** | CALZADO | Ten +3; EVA +1 | — | Puestos del Mercado del Valle · M05 | 9 piedras | TENACITY, EVASION |
| **Amuleto de colmillo montado** | AMULETO | Daño técnica directa% +3 pp | — | Ning Cai · M05 | 4 piedras / material: colmillo_lobo_legitimo | TECHNIQUE_DIRECT_DAMAGE |
| **Amuleto de sauce sereno** | AMULETO | Control +3; Qi +1 | — | Artesanos de Sauces · M05 | 10 piedras | CONTROL, QI |
| **Pulsera de cauce trenzado** | PULSERA | Qi +3 | — | Artesanos de Sauces · M05 | 8 piedras | QI |
| **Anillo del sello de hierro** | ANILLO | Pen% +4 pp | — | Lu Cheng · M06 | 4 contrib. | PENETRATION |
| **Anillo de corriente clara** | ANILLO | Prec +2; Control +2 | — | Puestos del Mercado del Valle · M05 | 10 piedras | PRECISION, CONTROL |
| **Pulsera de tensión meridiana** | PULSERA | Daño técnica directa% +2 pp | — | Lan Meihua · M06 | 4 contrib. | TECHNIQUE_DIRECT_DAMAGE |
| **Calzas de guardia externa** | PIERNAS | HP +2; Ten +2 | — | Jiang Rui · M04 | 2 contrib. | HP, TENACITY |
| **Anillo de reserva menor** | ANILLO | Qi +2; Prec +1 | — | Puestos del Mercado del Valle · M05 | 8 piedras | QI, PRECISION |

### LianQi_III — 19 piezas nuevas

| Pieza | Slot | Stats | Efecto | Fuente | Precio | Perfil |
|---|---|---|---|---|---|---|
| **Espada de vena clara** | ARMA | Básico plano +1; Prec +3; Pen% +3 pp | — | Lu Cheng · M08 | 20 piedras / 7 contrib. | BASIC_ATTACK, PRECISION, PENETRATION |
| **Vara de dos corrientes** | ARMA | Control +4; Ten +2 | — | He Zhen · M11 | 7 contrib. | CONTROL, TENACITY |
| **Sable de anillo gris** | ARMA | Básico plano +2; Prec -1; Daño técnica directa% +2 pp | — | Lu Cheng · M08 | 18 piedras | BASIC_ATTACK, TECHNIQUE_DIRECT_DAMAGE, AGGRESSION |
| **Tocado de hilo de formación** | TOCADO | Prec +3; Control +2 | — | Wen Tao · M08 | 5 contrib. | PRECISION, CONTROL |
| **Velo del archivo sereno** | TOCADO | Ten +4; Qi +2 | — | Song Rui · M09 | 5 contrib. | TENACITY, QI |
| **Túnica reforzada de trama de cobre** | VESTIDURA | DEF +1; HP +2 | — | Ning Cai · M08 | 22 piedras / 8 contrib. | DEFENSE, HP |
| **Vestidura de flujo ligero** | VESTIDURA | EVA +4; Qi +2 | — | Ning Cai · M08 | 20 piedras | EVASION, QI |
| **Brazales de pulso médico** | BRAZALES | Ten +4; Control +2 | — | Lan Meihua · M10 | 6 contrib. | TENACITY, CONTROL |
| **Fajín de las Dos Alas** | FAJIN | Qi +4; Control +2 | — | He Zhen · M11 | sin coste · recompensa | QI, CONTROL |
| **Calzas de paso silencioso** | PIERNAS | EVA +3; HP +3 | — | Ning Cai · M08 | 16 piedras | EVASION, HP |
| **Calzado de nube baja** | CALZADO | EVA +5; Prec +1 | — | Ning Cai · M11 | 6 contrib. | EVASION, PRECISION |
| **Amuleto de meridiano estable** | AMULETO | HP +3; Ten +4 | — | Lan Meihua · M10 | 6 contrib. | HP, TENACITY |
| **Pulsera de nudo de formación** | PULSERA | Qi +3; Control +3 | — | Wen Tao · M08 | 5 contrib. | QI, CONTROL |
| **Anillo de hilo de plata** | ANILLO | Crít. +2 pp; Prec +2 | — | Lu Cheng · M09 | 18 piedras | CRIT, PRECISION |
| **Anillo de tierra profunda** | ANILLO | HP +2; Ten +4 | — | Ning Cai · M10 | 5 contrib. | HP, TENACITY |
| **Espejo de Pulso Velado** | TESORO_ESPIRITUAL | EVA +5; Ten +3 | 1/combate al caer a ≤35% HP: Absorción 20% HP máx. | primera_ala · M12 | exploración oculta | EVASION, TENACITY, REACTIVE_DEFENSE, TREASURE |
| **Fajín de respiración larga** | FAJIN | Qi +4; EVA +1 | — | Ning Cai · M08 | 16 piedras | QI, EVASION |
| **Brazales de aguja de plata** | BRAZALES | Prec +2; Pen% +3 pp | — | Lu Cheng · M09 | 5 contrib. | PRECISION, PENETRATION |
| **Amuleto de flujo contenido** | AMULETO | Daño técnica directa% +2 pp; Qi +2 | — | Wen Tao · M08 | 6 contrib. | TECHNIQUE_DIRECT_DAMAGE, QI |

### LianQi_IV — 14 piezas nuevas

| Pieza | Slot | Stats | Efecto | Fuente | Precio | Perfil |
|---|---|---|---|---|---|---|
| **Hoja de seis corrientes** | ARMA | Básico plano +2; Prec +2; Daño técnica directa% +3 pp | — | Lu Cheng · M13 | 10 contrib. | BASIC_ATTACK, TECHNIQUE_DIRECT_DAMAGE, PRECISION |
| **Vara de relevo** | ARMA | Control +5; Ten +3; Qi +2 | — | Duan Shibo · M16 | 9 contrib. | CONTROL, TENACITY, QI |
| **Velo del vigilante del núcleo** | TOCADO | Prec +3; Ten +4 | — | Qiao Ren · M14 | 7 contrib. | PRECISION, TENACITY |
| **Manto de mantenimiento** | VESTIDURA | DEF +1; Ten +3; Qi +2 | — | Duan Shibo · M13 | 9 contrib. | DEFENSE, TENACITY, QI |
| **Brazales de relevo** | BRAZALES | HP +4; Ten +3 | — | Lu Cheng · M16 | 8 contrib. | DEFENSE, HP, TENACITY |
| **Fajín del núcleo profundo** | FAJIN | Qi +5; Ten +2 | — | Ji Xueying · M17 | sin coste · recompensa | QI, TENACITY |
| **Calzas de trama de sello** | PIERNAS | HP +4; EVA +3 | — | Ning Cai · M13 | 27 piedras | HP, EVASION |
| **Botas del voto inmóvil** | CALZADO | EVA +5; Ten +3 | — | Ning Cai · M17 | 8 contrib. | EVASION, TENACITY |
| **Amuleto de ancla resonante** | AMULETO | HP +3; Control +3; Ten +3 | — | He Zhen · M14 | 8 contrib. | HP, CONTROL, TENACITY |
| **Pulsera del nudo de crisis** | PULSERA | Qi +4; EVA +2; Ten +2 | — | Lan Meihua · M16 | 7 contrib. | QI, EVASION, TENACITY |
| **Anillo de relevo** | ANILLO | Crít. +2 pp; Daño técnica directa% +3 pp | — | Lu Cheng · M16 | 9 contrib. | TECHNIQUE_DIRECT_DAMAGE, CRIT |
| **Anillo de marca quieta** | ANILLO | Prec +3; Pen% +5 pp | — | Wen Tao · M13 | 8 contrib. | PRECISION, PENETRATION |
| **Vestidura del Ala Cerrada** | VESTIDURA | HP +5; Ten +4 | — | Qiao Ren · M14 | 8 contrib. | HP, TENACITY, DEFENSE |
| **Pulsera del meridiano profundo** | PULSERA | Qi +5; Control +3 | — | Lan Meihua · M16 | 8 contrib. | QI, CONTROL |

## 8. Dotación garantizada y recompensas directas

El juego no debe regalar una armadura completa por seguir la historia. La columna garantizada es deliberadamente estrecha:

| Momento | Entrega | NPC / fuente |
|---|---|---|
| Prólogo P | Espada de madera + Uniforme gris | dotación de ingreso / Tao Ming |
| Origen callejero | Cuchillo de hueso | sólo ese origen; alternativa, no pieza acumulable |
| M03 | Fajín de discípulo externo | Qiao Ren, promoción |
| M11 | Fajín de las Dos Alas | He Zhen, síntesis de investigación |
| M17 | Fajín del núcleo profundo | Ji Xueying, autorización de descenso |

**M18 no entrega equipo.** El cierre del arco no debe funcionar como “espada legendaria justo antes/después del jefe”.

## 9. Tesoros espirituales

Aunque la arquitectura permite **dos slots de Tesoro Espiritual**, durante el Arco 1 sólo existe **un tesoro obtenible**.

Esto es deliberado: los Tesoros Espirituales son objetos excepcionalmente poderosos y difíciles de conseguir. No deben convertirse en accesorios normales con otro nombre.

```text
2 slots disponibles
≠
2 tesoros en Arco 1

Arco 1
→ 1 único Tesoro Espiritual
→ oculto
→ difícil de obtener
→ completamente opcional
→ no comprable
→ no canjeable
→ no recompensa automática
```

### Espejo de Pulso Velado

| Campo | Diseño |
|---|---|
| Etapa mínima | LianQi III |
| Slot | Tesoro Espiritual |
| Fuente | exploración oculta de la Primera Ala |
| Ventana narrativa | durante/después de M12 |
| Compra | no |
| Contribución | no |
| Garantizado | no |
| Único | sí |
| Stats | **+5 Evasión; +3 Tenacidad** |
| Efecto | **1 vez por combate**, al caer por primera vez a ≤35% HP, genera **Absorción = 20% del HP máximo** |
| Power budget diagnóstico | 3.42 |

El segundo slot de Tesoro Espiritual permanece **vacío por diseño durante todo el Arco 1**.

El Espejo no es una llave de M12 ni de M18. El jugador puede terminar el arco sin encontrarlo. Los encuentros principales nunca se balancearán suponiendo que lo posee.

Precisamente porque sólo existe uno en todo el arco, puede superar claramente a un accesorio ordinario sin iniciar una escalada de artefactos.

## 10. Requisiciones que alimentan la economía

No son profesiones nuevas ni tiendas separadas. Son necesidades ocasionales de departamentos.

Objetivo de implementación futuro: definir ~10 y activar **5–8 por partida normal**, no todas simultáneamente.

| ID | Etapa | Departamento / NPC | Material | Contribución |
|---|---|---|---|---:|
| req_med_gl_fria | LianQi_II | Medicina · Lan Meihua | glándula fría de Salamandra de Musgo Frío | 2 |
| req_med_sanguijuela | LianQi_II | Medicina · Chen Bo | muestra útil de Sanguijuela de Vena | 2 |
| req_jardin_fibra_jade | LianQi_II | Jardines · Su Lian | fibra de jade limpia | 1 |
| req_ning_seda | LianQi_II | Ning Cai · Ning Cai | seda pálida íntegra | 2 |
| req_lu_mineral | LianQi_II | Lu Cheng · Lu Cheng | fragmento de mineral trabajable | 2 |
| req_recursos_muestra | LianQi_II | Recursos · Duan Shibo | muestra mineral estable | 2 |
| req_form_saco_resonante | LianQi_III | Formaciones · Wen Tao | saco resonante de Murciélago de Veta | 2 |
| req_form_filamento | LianQi_III | Formaciones · He Zhen | filamento antiguo utilizable | 3 |
| req_ning_membrana | LianQi_III | Ning Cai · Ning Cai | membrana vibratoria íntegra | 2 |
| req_med_meridiano | LianQi_III | Medicina · Lan Meihua | muestra meridiana estable | 3 |

Esto permite que un jugador que explora/Examina/Recolecta pueda financiar más opciones de equipo sin convertir las misiones principales en una lluvia de moneda.

## 11. Perfiles para futuras simulaciones

Los monstruos NO se balancearán contra HIGH_ROLL.

### MANDATORY_ENTRY

Equipo que puede asumirse al entrar a una etapa por progresión obligatoria previa.

| Etapa | Piezas | Stats agregados |
|---|---|---|
| LianQi_I | espada_madera_entrenamiento, uniforme_gris_externo | Prec +1; HP +1; DEF +0.25 |
| LianQi_II | espada_madera_entrenamiento, uniforme_gris_externo, fajin_discipulo_externo | Prec +1; HP +1; DEF +0.25; Qi +2 |
| LianQi_III | espada_madera_entrenamiento, uniforme_gris_externo, fajin_discipulo_externo | Prec +1; HP +1; DEF +0.25; Qi +2 |
| LianQi_IV | espada_madera_entrenamiento, uniforme_gris_externo, fajin_dos_alas | Prec +1; HP +1; DEF +0.25; Qi +4; Control +2 |

### EXPECTED_STAGE

Objetivo de jugador razonablemente activo, con varias decisiones de gasto.

| Etapa | Piezas | Stats agregados |
|---|---|---|
| LianQi_I | espada_madera_entrenamiento, uniforme_gris_externo, fajin_discipulo_externo, zapatos_suela_blanda | Prec +1; HP +1; DEF +0.25; Qi +2; EVA +2 |
| LianQi_II | espada_hierro_equilibrada, bandana_cuero_reforzada, sobretunica_patrulla, fajin_patrulla, sandalias_viento, pulsera_cauce_trenzado, anillo_herrumbroso | Básico plano +1; Prec +2; Ten +4; HP +4; DEF +0.25; Qi +7; EVA +4 |
| LianQi_III | espada_vena_clara, tocado_hilo_formacion, tunica_reforzada, brazales_pulso_medico, fajin_dos_alas, calzado_nube_baja, amuleto_meridiano_estable, anillo_hilo_plata | Básico plano +1; Prec +9; Pen% +3 pp; Control +6; DEF +0.75; HP +6; Ten +8; Qi +4; EVA +5; Crít. +2 pp |
| LianQi_IV | hoja_seis_corrientes, velo_vigilante_nucleo, manto_mantenimiento, brazales_pulso_medico, fajin_dos_alas, calzas_trama_sello, calzado_nube_baja, amuleto_ancla_resonante, anillo_hilo_plata, placa_mantenimiento_antigua | Básico plano +2; Daño técnica directa% +3 pp; Prec +8; Ten +17; DEF +0.75; Qi +6; Control +7; HP +7; EVA +8; Crít. +2 pp |

### HIGH_ROLL_STRESS

Perfil deliberadamente cargado para comprobar que el sistema no se rompe. No es supuesto de diseño de encuentros.

| Etapa | Piezas | Stats agregados |
|---|---|---|
| LianQi_I | espada_madera_entrenamiento, uniforme_gris_externo, fajin_discipulo_externo, zapatos_suela_blanda, colgante_fragmento_jade, anillo_herrumbroso | Prec +1; HP +1; DEF +0.25; Qi +3; EVA +2; Control +2 |
| LianQi_II | aguja_acero_frio, bandana_cuero_reforzada, tunica_ruta_sauces, brazales_cuero_cruzado, fajin_patrulla, calzas_sendero_pinos, sandalias_viento, amuleto_colmillo_montado, pulsera_cauce_trenzado, anillo_sello_hierro, anillo_corriente_clara, placa_ruta_grulla | Prec +5; Pen% +7 pp; Ten +6; HP +6; EVA +7; DEF +0.5; Qi +6; Daño técnica directa% +3 pp; Control +2 |
| LianQi_III | espada_vena_clara, tocado_hilo_formacion, tunica_reforzada, brazales_pulso_medico, fajin_dos_alas, calzas_paso_silencioso, calzado_nube_baja, amuleto_meridiano_estable, pulsera_nudo_formacion, anillo_hilo_plata, anillo_tierra_profunda, brujula_seis_corrientes, espejo_pulso_velado | Básico plano +1; Prec +11; Pen% +3 pp; Control +11; DEF +0.75; HP +11; Ten +12; Qi +7; EVA +10; Crít. +2 pp |
| LianQi_IV | hoja_seis_corrientes, tocado_hilo_formacion, tunica_reforzada, vendas_antebrazo_practica, fajin_dos_alas, calzas_paso_silencioso, calzado_nube_baja, amuleto_colmillo_montado, pulsera_nudo_formacion, anillo_hilo_plata, anillo_marca_quieta, brujula_seis_corrientes | Básico plano +2; Daño técnica directa% +6 pp; Prec +15; Control +9; DEF +0.75; HP +6; Qi +7; EVA +8; Crít. +2 pp; Pen% +5 pp |

## 12. Builds que el catálogo debe permitir

### Duelista / Precisión
Armas equilibradas, capuchas/tocados de observación, anillos de corriente o marca quieta y Brújula. Busca conectar golpes y neutralizar Evasión.

### Agresión / Crítico
Sables, Amuleto de Colmillo, Anillo de Hilo de Plata y Anillo de Relevo. Gana daño sin convertir el equipo en multiplicador universal de reino.

### Ruptura / Penetración
Aguja de Acero, Espada de Vena Clara, Anillo del Sello de Hierro y Marca Quieta. Especializa contra DEF; sacrifica otros slots.

### Evasión
Túnica de Sauces/Flujo Ligero, Calzas silenciosas, Sandalias/Botas, Espejo de Pulso. No concede segunda tirada de esquiva.

### Resistencia / Tenacidad
Sobretúnica, Túnica Reforzada/Manto, Brazales, Amuleto Meridiano/Ancla y Placa de Mantenimiento. La DEF de equipo permanece contenida; gran parte del aguante llega vía HP/Tenacidad.

### Control
Vara de Dos Corrientes/Relevo, Tocado de Formación, Fajín Dos Alas, Pulsera de Nudo, Brújula/Campana. Es una build real, no una propiedad exclusiva de Agua.

### Qi / continuidad
Fajines, pulseras, velo del archivo y piezas de crisis. Aumenta reserva, no crea regeneración pasiva universal.

### Equilibrada
Mezcla 1–2 piezas de cada eje. Es el perfil que más se parece a EXPECTED_STAGE.

Ninguna pieza está bloqueada por raíz elemental. La raíz crea sinergias, no permisos artificiales.

## 12B. Daño de técnicas aportado por equipo

Sí existe, pero de forma intencionalmente pequeña y explícita mediante:

`technique_direct_damage_percent`

Este stat aumenta **sólo el daño directo compatible de técnicas**.

No modifica:
- Golpe básico;
- DOT;
- Reflect;
- Retaliation;
- Calor almacenado;
- curaciones;
- Absorción;
- daño secundario marcado `no_offensive_rescale`.

Piezas actuales:

| Pieza | Etapa | Bono |
|---|---|---:|
| Amuleto de colmillo montado | LianQi II | +3% daño directo de técnicas |
| Sable de anillo gris | LianQi III | +2% |
| Hoja de seis corrientes | LianQi IV | +3% |
| Anillo de relevo | LianQi IV | +3% |

Un personaje de LianQi IV que sacrifique varios slots para apilar las piezas compatibles puede alcanzar aproximadamente **+8–9%** de daño directo de técnica según el arma elegida. Eso ya es una build ofensiva especializada, no el baseline esperado.

Además, Precisión, crítico y Penetración pueden mejorar el rendimiento ofensivo de las técnicas sin multiplicar su magnitud base.

## 13. Guardias de balance

1. **No full-set bonus** en Arco 1.
2. No refuerzo +1/+10, durabilidad ni rareza de color.
3. Equipo DEF máxima deliberadamente pequeña; evitar múltiples +1 DEF.
4. El equipo no reduce costes Qi porcentualmente en Arco 1: eso pertenece a ramas de Eficiencia y evita cruzar umbrales ocultos.
5. Daño directo, crítico y Penetración están distribuidos en pocos slots para impedir apilamiento gratuito.
6. No hay equipo elemental obligatorio ni root-lock.
7. Los efectos reactivos usan primitivas ya compatibles con el motor: Absorción, chequeo de Control, Precisión siguiente, refund explícito.
8. El Anillo Herrumbroso no entra en simulación de combate hasta cerrar el contrato de meditación.
9. Lu Cheng y Ning Cai son servicios NPC; no se habilita Forja/Sastrería como profesiones.
10. Uniforme de Discípulo Interno queda **fuera de Arco 1**.
11. M18 no es fuente de loot legendario.
12. MONSTRUOS: balancear contra MANDATORY_ENTRY y revisar EXPECTED_STAGE; HIGH_ROLL sólo stress.

## 14. Estado del catálogo

```text
68 piezas totales

LianQi I   14
LianQi II  21
LianQi III 19
LianQi IV  14

ARMA                 11
TOCADO                6
VESTIDURA             6
BRAZALES              5
FAJIN                  4
PIERNAS                4
CALZADO                5
AMULETO                5
PULSERA                4
ANILLO                 7
TESORO_ESPIRITUAL      1
```

Política de tesoros Arco 1:
- capacidad arquitectónica: 2;
- tesoros obtenibles: **1**;
- segundo slot: vacío por diseño;
- el único Tesoro Espiritual es el **Espejo de Pulso Velado**.

El catálogo machine-readable pasó validación de:
- IDs únicos;
- slots;
- límites por pieza;
- precios requeridos;
- perfiles sin overflow de slots.

## 15. Pendientes antes de CANON

Este catálogo es **PROVISIONAL**. Antes de promover:
1. ejecutar Monte Carlo por etapa con NAKED / MANDATORY_ENTRY / EXPECTED / HIGH_ROLL;
2. probar siete arquetipos especializados;
3. validar economía de piedras;
4. sincronizar los valores propuestos de Contribución M08–M17 con contratos de misión;
5. cerrar recuperación/meditación para valorar Qi adicional;
6. probar efectos reactivos de tesoros en el motor universal;
7. revalidar contra enemigos LianQi II–IV cuando existan.

El siguiente bloque correcto es **ETAPA 18B — simulación de equipo**, no implementación runtime.


## ADDENDUM ETAPA18A — catálogo ampliado y contrato de inspección

ETAPA18A amplía y corrige este diseño.

Autoridad adicional:
- `docs/experimentos/ETAPA18A_AMPLIACION_CATALOGO_PROLOGO_DESCRIPCIONES_2026-09-29.md`

Cambios vigentes:
- catálogo ampliado de 58 a **68 piezas**;
- 14 LI / 21 LII / 19 LIII / 14 LIV;
- todos los objetos de equipo tienen campo obligatorio `description`;
- MIRAR/EXAMINAR mostrará descripción diegética y luego propiedades estructuradas;
- el Prólogo entrega en `descansillo`, una sola vez:
  - `uniforme_gris_aspirante`;
  - `espada_madera_entrenamiento`;
- el origen callejero conserva `cuchillo_hueso_callejero` y puede elegir arma activa;
- no se entrega equipo de secta al crear el personaje;
- todo equipo legacy queda sustituido por IDs nuevos; coexistencia prohibida;
- consumibles/materiales/manuales están fuera de este reemplazo;
- auditoría integral de adquisición y Colab masivo quedan deliberadamente diferidos.

El JSON `equipment_arc1_catalog.json` es la fuente machine-readable vigente.


## ADDENDUM — Contrato numérico entero de equipo

Corrección posterior:
- los stats planos de equipo deben ser **enteros**;
- queda prohibida la DEF fraccionaria;
- porcentajes y puntos porcentuales usan campos explícitos (`*_percent`, `*_pp`);
- DEF de equipo:
  - LianQi I: máximo0;
  - LianQi II: máximo0;
  - LianQi III: máximo+1;
  - LianQi IV: máximo+1.

Cambios principales:
- Uniforme gris de aspirante: HP +2, sin DEF;
- Sobretúnica de patrulla: HP +3, Tenacidad +2;
- Brazales de cuero cruzado: HP +2, Tenacidad +2;
- Túnica reforzada de trama de cobre: DEF +1, HP +2;
- Manto de mantenimiento: DEF +1, Tenacidad +3, Qi +2;
- Brazales de relevo: HP +4, Tenacidad +3;
- Vestidura del Ala Cerrada: HP +5, Tenacidad +4.

No existe ningún `+0.25/+0.5/+0.75 DEF` en el catálogo vigente.
