# Técnicas de Arco 1 — diseño aprobado hasta Tierra

Fecha: 2026-09-28  
Rama: `experiment/combat-stat-contract-v0.1`  
Estado: **diseño / contrato; NO implementación runtime**

## 0. Alcance y advertencias

Este documento consolida las decisiones de diseño aprobadas en la sesión posterior al checkpoint `CHECKPOINT_TECNICAS_ARCO1_2026-09-28.md`.

- No tocar `main`.
- No hacer merge.
- No contaminar `implement/3c5-npc-ver74`.
- Los valores numéricos de daño, coste, DEF, Tenacidad, duración, porcentajes y umbrales son **provisionales para benchmark** salvo que un contrato global los marque como cerrados.
- La identidad, función y estructura de ramas sí se consideran decisiones de diseño aprobadas salvo notas de pendiente.
- Falta diseñar Viento.
- Falta cerrar economía de puntos de técnica por etapa de LianQi.
- La auditoría arquitectónica externa fue realizada; falta cerrar la matriz global de 20 Concordancias y mapearla sobre cada técnica.

---

# 1. Regla general de progresión de técnicas

Cada técnica básica de Arco 1 tiene:

```text
TÉCNICA BASE
├─ Tramo I  → 3 opciones mutuamente excluyentes
├─ Tramo II → 3 opciones mutuamente excluyentes
└─ Tramo III→ 3 opciones mutuamente excluyentes
```

Dirección actual de acceso:

- LianQi I · Percepción: técnica base.
- LianQi II · Circulación: Tramo I.
- LianQi III · Consolidación: Tramo II.
- LianQi IV · Refinamiento: Tramo III.

Reglas:

1. Cada tramo ofrece exactamente 3 opciones.
2. Una opción posterior debe funcionar aunque el jugador no haya elegido la opción temática equivalente en el tramo anterior.
3. Las opciones de una misma identidad pueden reconocer elecciones previas y producir **sinergias de especialización**.
4. Mezclar identidades debe seguir siendo válido.
5. Repetir la misma identidad durante I + II + III debe producir una versión claramente especializada.
6. No debe existir una elección-trampa que quede inútil por una decisión anterior.
7. La cantidad de puntos ganados en cada etapa de LianQi queda pendiente. El objetivo es que el jugador deba decidir entre profundizar una técnica o repartir inversión entre varias.
8. En Arco 2 una técnica básica puede evolucionar o ser desplazada por una técnica superior; el Tramo III no obliga a mantenerla para siempre.

---

# 2. Regla obligatoria de Concordancias por técnica

Una técnica no se considera completamente cerrada hasta declarar:

1. qué Eco genera y cuándo;
2. qué Ecos puede consumir;
3. qué propiedad exacta modifica cada Concordancia;
4. cómo interactúa la Concordancia con sus ramas;
5. qué Concordancias no acepta;
6. que toda Concordancia habilitada tenga una aplicación real y visible.

Las Concordancias no deben convertirse en un bono genérico de emergencia.

---

# 3. Contrato global AOE

Contrato ya incorporado al documento global de combate:

```text
AOE
→ alcanza a todos los NPC hostiles presentes en la sala
→ incorpora inmediatamente al combate a los hostiles alcanzados
→ cada objetivo resuelve su propio impacto
```

Reglas:

- No existe límite base de 3/4/6 objetivos.
- Las ramas AOE no aumentan cantidad de objetivos.
- El daño no se reparte.
- 2+ objetivos: 100% del daño calculado.
- 1 objetivo: conserva provisionalmente 65% del daño calculado, igual que el runtime actual de ver74.
- El 65% es global y queda sujeto a benchmark final.

---

# 4. FUEGO

Identidad general: presión ofensiva, daño directo, Quemadura y conversión defensiva→ofensiva.

## 4.1 Palma Ardiente — unitarget

Base provisional:

- daño nominal: 10;
- coste: 6 Qi;
- 1 acción → 1 impacto → 1 porción [TÉCNICA][DIRECTO][ELEMENTAL][FUEGO];
- crítico y Precisión globales normales;
- no aplica Quemadura de base;
- al impactar genera Eco de Fuego.

### Tramo I

**Ascua Adherente — DOT**
- Quemadura: 15% del daño base nominal por tick × 3 ticks;
- máximo 3 cargas independientes.

**Palma Compacta — directo**
- +20% daño directo de Palma.

**Respiración de Brasa — eficiencia**
- coste 6 → 5 Qi.

### Tramo II

**Brasa Devoradora — DOT**
- sola: habilita Quemadura 10% × 3;
- con Ascua: 20% × 3, máximo 4 cargas.

**Corazón del Horno — directo**
- +25% daño directo;
- +1 Qi;
- con Compacta: +10% daño crítico.

**Circulación Incandescente — eficiencia**
- −10% coste;
- con Respiración: +5 Precisión.

### Tramo III

**Combustión Persistente — DOT**
- sola: 10% × 3;
- especialización DOT completa: 20% × 4 ticks, máximo 4 cargas.

**Golpe Incandescente — directo**
- +15% directo;
- especialización directa completa: añade +5 pp crítico.
- total orientativo de ruta completa: +60% directo, +5 pp crítico y +10% daño crítico, con el sobrecoste de Tramo II.

**Flujo Constante — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste porcentual, +10 Precisión;
- sujeto al futuro piso global de coste.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Fuego.

---

## 4.2 Respiración del Cuerpo-Horno — defensiva

Base provisional:

- coste: 7 Qi;
- duración: 2 turnos;
- Absorción = 15% Vida máxima;
- genera Eco de Fuego;
- no se acumula consigo misma;
- reactivar reemplaza reserva y reinicia duración.

### Tramo I

**Cámara Sellada — barrera**
- Absorción 15% → 20% Vida máxima.

**Horno Latente — conversión**
- 25% del daño absorbido → Calor;
- tope Calor = 5% Vida máxima;
- Calor se consume en una técnica ofensiva de Fuego posterior como una porción secundaria de Fuego;
- la cantidad almacenada no vuelve a escalar con pools ofensivos ni puede criticar;
- esa porción sí pasa por DEF y Absorción, no usa Penetración y no genera Robo de Vida;
- no es Reflect ni Retaliation.

**Respiración Mesurada — eficiencia**
- 7 → 6 Qi.

### Tramo II

**Crisol de Nueve Sellos — barrera**
- +5 pp de Vida máxima como Absorción;
- con Cámara: sinergia adicional +5 pp.

**Corazón Reavivado — conversión**
- sola: 20% absorbido → Calor, tope 5% HP;
- con Horno Latente: 45%, tope 10% HP.

**Circuito del Horno — eficiencia**
- −10% coste;
- con Respiración Mesurada: duración 2 → 3.

### Tramo III

**Muro de Calor — barrera**
- +5 pp Absorción;
- ruta completa: alrededor de 35% HP de Absorción y 3 turnos.

**Calor Acumulado — conversión**
- ruta completa: 60% del daño absorbido → Calor;
- tope 15% Vida máxima.

**Horno Continuo — eficiencia**
- −10% coste;
- ruta completa: duración hasta 4 turnos y +5 pp Absorción.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Fuego.

---

## 4.3 Círculo de las Cien Ascuas — AOE

El `65%` de duelo se aplica como capa global antes de DEF y antes del redondeo final; no reduce por sí mismo Control, debuffs, duración ni stacks.

CORRECCIÓN GLOBAL:

- afecta a **todos los NPC hostiles presentes en la sala**;
- arrastra a los hostiles alcanzados al combate;
- no tiene máximo de 3 objetivos;
- 2+ objetivos: daño completo;
- 1 objetivo: 65% del daño calculado provisional.

Base provisional:
- daño nominal: 7 por enemigo;
- coste: 9 Qi;
- no aplica Quemadura de base;
- genera un Eco de Fuego por ejecución válida, no uno por enemigo.

### Tramo I

**Lluvia de Ascuas — DOT**
- Quemadura 10% del daño base × 3 ticks por objetivo.

**Anillo Incandescente — directo**
- +15% daño directo.

**Respiración de las Cien Ascuas — eficiencia**
- 9 → 8 Qi.

### Tramo II

**Mar de Brasas — DOT**
- sola: 8% × 3;
- con Lluvia: 15% × 3, máximo 4 cargas.

**Corona Ardiente — directo**
- +20% directo;
- +2 Qi;
- con Anillo: +10% daño crítico.

**Flujo Circular — eficiencia**
- −10% coste;
- con Respiración: +5 Precisión.

### Tramo III

**Brasas Persistentes — DOT**
- sola: 8% × 3;
- ruta completa: 20% × 3, máximo 4 cargas.

**Estallido Circular — directo**
- +15% directo;
- +1 Qi;
- ruta completa: +50% directo, +5 pp crítico, +10% daño crítico;
- coste alto y penalización global de duelo si sólo hay un enemigo.

**Círculo Estable — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, +10 Precisión.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Fuego.

---

# 5. METAL

Identidad general: Penetración, ejecución precisa, fortificación segmentada y ruptura estructural.

## 5.1 Destello de Plata — unitarget

Base provisional:

- daño nominal: 9;
- coste: 6 Qi;
- +10 pp Penetración % propia;
- genera Eco de Metal al impactar.

### Tramo I

**Filo Abierto — penetración**
- +10 pp Penetración %.

**Corte Preciso — precisión**
- +10 Precisión.

**Flujo de Plata — eficiencia**
- −1 Qi.

### Tramo II

**Punta de Acero — penetración**
- +3 Penetración plana;
- con Filo Abierto: pasa a +5 plana.

**Golpe Certero — ejecución**
- +5 Precisión;
- +5 pp crítico;
- con Corte Preciso: +10% daño crítico.

**Circulación Ligera — eficiencia**
- −10% coste;
- con Flujo de Plata: +5 Precisión.

### Tramo III

**Corte Profundo — penetración**
- +5 pp Penetración %;
- ruta completa: +25 pp Penetración % propia y +7 Penetración plana.

**Destello Certero — ejecución**
- +5 Precisión;
- +5 pp crítico;
- ruta completa orientativa: +20 Precisión, +10 pp crítico, +20% daño crítico.

**Ritmo de Plata — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, +10 Precisión.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Metal.

---

## 5.2 Armadura de Plata — defensiva

Mecánica central aprobada: **Placas de Plata consumibles por impacto**.

Base provisional:

- coste: 7 Qi;
- duración máxima: 4 turnos;
- 3 Placas;
- mientras quede al menos una Placa: la **Placa activa** concede +3 DEF contra ese impacto directo;
- las Placas son cargas secuenciales: 3 Placas no significan +9 DEF simultánea;
- después del impacto válido se consume 1 Placa;
- una evasión no consume Placa;
- DOT no consume Placas;
- genera Eco de Metal.

### Tramo I

**Placas Gruesas — resistencia**
- +3 → +4 DEF por Placa.

**Acero Flexible — adaptación**
- al romperse una Placa: +5 Tenacidad hasta el comienzo del próximo turno.

**Reserva de Plata — cantidad**
- 3 → 4 Placas.

### Tramo II

**Núcleo Reforzado — resistencia**
- +1 DEF por Placa;
- con Placas Gruesas: especialización llega orientativamente a +6 DEF por Placa en este tramo.

**Temple Reactivo — adaptación**
- sola: +5 Tenacidad al romperse una Placa;
- con Acero Flexible: +10 Tenacidad y una Placa no se consume si el impacto fue completamente detenido por DEF.

**Segunda Capa — cantidad**
- +1 Placa;
- con Reserva de Plata: sinergia adicional +1 Placa, alcanzando 6.

### Tramo III

**Acero Cerrado — resistencia**
- +1 DEF por Placa;
- ruta completa: 3 Placas de alrededor de +8 DEF cada una.

**Temple Perfecto — adaptación**
- +5 Tenacidad al romperse una Placa;
- ruta completa: +15 Tenacidad reactiva;
- si DEF reduce el impacto a 0, no consume Placa;
- primera vez por activación que un Control falle: recupera 1 Placa rota, sin superar el máximo inicial.

**Armadura Laminada — cantidad**
- +1 Placa;
- con Reserva de Plata + Segunda Capa, añade además +1 Placa de sinergia final;
- ruta completa de cantidad: **8 Placas** de +3 DEF base cada una, consumidas secuencialmente.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Metal.

---

## 5.3 Lluvia de Filos — AOE

El `65%` de duelo se aplica como capa global antes de DEF y antes del redondeo final; no reduce por sí mismo Control, debuffs, duración ni stacks.

CORRECCIÓN GLOBAL:

- afecta a todos los NPC hostiles de la sala;
- sin máximo fijo;
- 2+ objetivos: daño completo;
- 1 objetivo: 65% del daño calculado provisional.

Base provisional:

- daño: 6 por enemigo;
- coste: 9 Qi;
- +10 pp Penetración % por impacto;
- genera un Eco de Metal por ejecución válida.

### Tramo I

**Filos Dentados — ruptura**
- enemigos impactados: −1 DEF durante 2 turnos;
- se aplica después del impacto, no retroactivamente.

**Barrido Cerrado — directo**
- +15% daño directo.

**Paso Ligero — eficiencia**
- 9 → 8 Qi.

### Tramo II

**Ruptura Profunda — ruptura**
- sola: −1 DEF durante 2 turnos;
- con Filos Dentados: −2 DEF durante 2 turnos y +5 pp Penetración %.

**Tormenta de Acero — directo**
- +20% directo;
- +1 Qi;
- con Barrido: +35% directo total y +5 pp crítico.

**Ritmo de Filos — eficiencia**
- −10% coste;
- con Paso Ligero: −1 Qi, −10% coste, +5 Precisión.

### Tramo III

**Defensa Quebrada — ruptura**
- sola: −1 DEF;
- ruta completa: −3 DEF durante 3 turnos y +10 pp Penetración % adicional para Lluvia.

**Círculo de Acero — directo**
- +15% directo;
- +1 Qi;
- ruta completa: +50% directo, +5 pp crítico, +10% daño crítico.

**Flujo Continuo — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, +10 Precisión y +5 pp Penetración %.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Metal.

---

# 6. AGUA

Identidad general: control del tempo, eficiencia, debilitación y defensa que vuelve a fluir.

## 6.1 Latigazo de Marea — unitarget/control

La función de **hacer perder la próxima acción** pertenece a la técnica base; no depende de preparar Cadencia.

Base provisional:

- daño: 8;
- coste: 7 Qi;
- al impactar intenta aplicar **Arrastre** mediante Control vs Tenacidad;
- **base_control PROVISIONAL de Arrastre: 65** para benchmark LianQi I;
- contra la Tenacidad ordinaria PROVISIONAL 20, Agua principal (+5 Control) parte de 50% efectivo;
- Arrastre: el objetivo pierde su próxima acción;
- puede cortar una acción enemiga anunciada todavía no ejecutada;
- no elimina efectos ya activos;
- anti-bloqueo: después de sufrir Arrastre, el objetivo debe completar una acción normal antes de poder sufrir Arrastre otra vez;
- genera Eco de Agua al impactar.

### Tramo I

**Corriente Firme — Control**
- +10 Control para Arrastre.

**Golpe de Corriente — daño**
- +20% directo.

**Flujo Continuo — eficiencia**
- 7 → 6 Qi.

### Tramo II

**Marea Envolvente — Control**
- +10 Control;
- con Corriente Firme: Arrastre exitoso aplica −5 Precisión hasta que el objetivo complete su próxima acción normal.

**Rompiente — daño**
- +25% directo;
- con Golpe de Corriente: +45% directo total y +5 pp crítico.

**Circulación Serena — eficiencia**
- −10% coste;
- con Flujo Continuo: +5 Precisión.

### Tramo III

**Dominio de la Corriente — Control**
- +10 Control;
- ruta completa: +30 Control total para Arrastre;
- Arrastre exitoso hace que el siguiente Latigazo contra ese objetivo obtenga +10 Precisión;
- nunca ignora la regla anti-bloqueo.

**Golpe de Marea — daño**
- +20% directo;
- ruta completa: +65% directo y +5 pp crítico.

**Corriente Constante — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, +10 Precisión.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Agua.

---

## 6.2 Espejo de Luna — defensiva

Aprobada.

Base provisional:

- coste: 7 Qi;
- duración: 3 turnos;
- Absorción = 12% Vida máxima;
- **Reflujo**: al comienzo del turno, si queda Absorción, recupera 25% de la **reserva máxima de esa instancia**;
- nunca supera reserva máxima;
- si llega a 0, se rompe y deja de regenerarse salvo ramas específicas;
- genera Eco de Agua.

### Tramo I

**Marea Profunda — reserva**
- 12% → 17% Vida máxima.

**Agua Renovada — Reflujo**
- 25% → 35%.

**Circulación Serena — eficiencia**
- 7 → 6 Qi.

### Tramo II

**Marea Alta — reserva**
- +5 pp de Vida máxima como Absorción;
- con Marea Profunda: sinergia, orientativamente 25% total.

**Corriente de Retorno — regeneración**
- +10 pp Reflujo;
- con Agua Renovada: una vez por activación, si se rompe, al siguiente turno se reconstruye con 40% de su reserva máxima.

**Flujo Ligero — eficiencia**
- −10% coste;
- con Circulación Serena: duración 3 → 4.

### Tramo III

**Mar Interior — reserva**
- +5 pp;
- ruta completa: alrededor de 30% Vida máxima de reserva.

**Marea Eterna — regeneración**
- +10 pp Reflujo;
- ruta completa: Reflujo 50%;
- reconstrucción una vez por activación con 50% de la reserva máxima.

**Corriente Ininterrumpida — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, duración 3 → 5;
- si termina naturalmente conservando Absorción: recupera 1 Qi (fuente explícita, no regeneración pasiva).

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Agua.

---

## 6.3 Marea de las Ocho Orillas — AOE

El `65%` de duelo se aplica como capa global antes de DEF y antes del redondeo final; no reduce por sí mismo Control, debuffs, duración ni stacks.

Aprobada con corrección global AOE:

- afecta a todos los NPC hostiles de la sala;
- sin máximo fijo;
- 2+ objetivos: daño completo;
- 1 objetivo: 65% del daño calculado provisional.

Base provisional:

- daño: 6 por enemigo;
- coste: 9 Qi;
- cada enemigo impactado recibe **Desbalance: −3 Precisión durante 1 turno**;
- Desbalance es debuff estadístico, no Control;
- genera un Eco de Agua por ejecución válida.

### Tramo I

**Corriente Turbia — debilitación**
- Desbalance −3 → −5 Precisión.

**Oleada Fuerte — daño**
- +15% directo.

**Flujo Amplio — eficiencia**
- 9 → 8 Qi.

### Tramo II

**Marea Inestable — debilitación**
- Desbalance dura +1 turno;
- con Corriente Turbia: −8 Precisión durante 2 turnos;
- la siguiente técnica Agua que intente Control contra ese objetivo obtiene +5 Control.

**Rompiente Abierta — daño**
- +20% directo;
- +1 Qi;
- con Oleada: +35% total y +5 pp crítico.

**Circulación Extendida — eficiencia**
- −10% coste;
- con Flujo Amplio: −1 Qi, −10% coste y +5 Precisión.

### Tramo III

**Mar Revuelto — debilitación**
- −3 Precisión adicional;
- ruta completa: Desbalance −12 Precisión durante 2 turnos;
- primera técnica Agua que intente Control sobre cada afectado: +10 Control.

**Marea Creciente — daño**
- +15% directo;
- ruta completa: +50% directo y +5 pp crítico.

**Curso Inagotable — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste, +10 Precisión;
- si impacta a todos los hostiles presentes y hay grupo real, puede devolver 1 Qi una vez por ejecución; revisar en benchmark para evitar abuso en salas pobladas.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Agua.

---

# 7. TIERRA

Identidad general: peso, estabilidad, fijación del enemigo y resistencia que se asienta bajo presión.

## 7.1 Golpe de Montaña — unitarget

Aprobada.

Base provisional:

- daño: 9;
- coste: 6 Qi;
- aplica **Peso**;
- Peso base: −3 Evasión por carga, duración 2 turnos, máximo 2;
- semántica PROVISIONAL: `STACK_REFRESH`;
- owner del estado: objetivo afectado;
- `duration_unit = TARGET_TURN`; decrementa en `TURN_END` del objetivo;
- cada aplicación válida añade 1 carga y refresca la duración completa;
- al expirar la duración se eliminan todas las cargas;
- no es Control;
- genera Eco de Tierra.

### Tramo I

**Paso Pesado — presión**
- Peso −3 → −4 Evasión por carga.

**Golpe Macizo — daño**
- +20% directo.

**Base Firme — estabilidad**
- tras impactar: +5 Tenacidad hasta el próximo turno.

### Tramo II

**Carga de Piedra — presión**
- máximo Peso 2 → 3;
- con Paso Pesado: hasta −12 Evasión;
- al máximo, duración 2 → 3.

**Impacto Profundo — daño**
- +25% directo;
- con Golpe Macizo: +45%;
- contra objetivo con Peso máximo: +10% adicional.

**Postura Inamovible — estabilidad**
- +5 Tenacidad;
- con Base Firme: +10 Tenacidad y +1 DEF hasta próximo turno.

### Tramo III

**Anclaje de Montaña — presión**
- ruta completa: 3 cargas, −5 Evasión por carga, máximo −15, duración 3 turnos.

**Golpe de Cumbre — daño**
- +20% directo;
- ruta completa: +65% permanente;
- con Peso máximo: +15% adicional; total ideal +80%.

**Raíz Inamovible — estabilidad**
- +5 Tenacidad;
- ruta completa: +15 Tenacidad, +2 DEF hasta próximo turno;
- si un Control falla en ese período, siguiente Golpe de Montaña +5 Precisión.

### Concordancias
Mapeo receptor canónico: `MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`. Como técnica pura, genera Eco de Tierra.

---

## 7.2 Piel de Cobre — defensiva

Aprobada para testeo posterior.

### Base revisada — PROVISIONAL tras Etapas 1–6

- coste: 7 Qi;
- duración: 3 turnos;
- al activar: +2 DEF inmediata y +1 Arraigo;
- cada Arraigo aporta +3 Tenacidad;
- la contribución de DEF de Arraigo usa **DEF_CAP2 PROVISIONAL**:
  - 1 Arraigo: +1 DEF por Arraigo acumulado;
  - 2 Arraigos: +2 DEF acumulada;
  - 3 Arraigos: la contribución acumulada de Arraigo permanece en +2 DEF;
- máximo 3 Arraigos;
- cada acción enemiga de daño directo que quite Vida: +1 Arraigo, máximo una vez por acción;
- primera vez por activación que una acción enemiga quite al menos 10% de Vida máxima: gana +2 Arraigos en vez de +1;
- DOT no genera Arraigo;
- al alcanzar Arraigo máximo: +1 turno a la duración restante, una vez por activación;
- genera Eco de Tierra.

Valores base por estado de Piel:

```text
al activar / 1 Arraigo: +3 DEF / +3 Tenacidad
2 Arraigos:              +4 DEF / +6 Tenacidad
3 Arraigos:              +4 DEF / +9 Tenacidad
```

Nota de benchmark:

- frente a un personaje con DEF base1, Piel produce DEF total 4 → 5 → 5;
- la tercera carga sigue siendo mecánicamente relevante por +3 Tenacidad adicional y por activar la extensión de duración;
- esta curva sustituye PROVISIONALMENTE la antigua escalera 4 → 5 → 6 del benchmark;
- la promoción se apoya en `ETAPA1`–`ETAPA6` de Piel del 2026-09-29.

### Tramo I

**Corteza Endurecida — fortificación — PROVISIONAL**
- mantiene la nueva filosofía `DEF_CAP2`: la tercera carga no vuelve a añadir otra unidad incremental de DEF;
- reemplaza la contribución acumulada de DEF de Arraigo `1 / 2 / 2` por `2 / 3 / 3`;
- con la +2 DEF inmediata de Piel, la técnica aporta `+4 / +5 / +5 DEF`;
- con DEF base1 del benchmark, produce DEF total `5 → 6 → 6`;
- validada en 1v1, 2 enemigos y 3 enemigos durante Etapas 8A–8C;
- el aumento de DEF reduce ON_HP_DAMAGE y autolimita generación de Arraigo/extensión;
- no implica autorización para que Tramos II/III sigan sumando DEF plana linealmente.

**Centro Firme — estabilidad**
- cada Arraigo da +5 Tenacidad en vez de +3.

**Tierra Persistente — aguante**
- +1 turno de duración desde la activación.

### Tramo II

**Estratos Compactos — fortificación — PROVISIONAL**
- usa `ESTRATO_REACTIVO_2`;
- mientras Piel esté activa, cuando Arraigo aumente y el nuevo valor sea 2 o 3, gana/refresca 1 **Estrato Compacto**;
- máximo 1 Estrato almacenado;
- el siguiente impacto directo conectado contra el usuario recibe +2 DEF sólo para ese impacto;
- después de ese impacto conectado, el Estrato se consume;
- una evasión no consume Estrato;
- si un trigger hace saltar Arraigo directamente de 1→3, genera un solo Estrato;
- si el ascenso ocurre 1→2→3, puede proteger como máximo dos impactos en toda la activación;
- no aumenta la DEF permanente de Piel;
- no modifica Tenacidad, duración ni máximo de Arraigo;
- funciona aunque no se haya elegido Corteza Endurecida;
- con Corteza muestra retornos decrecientes en los benchmarks, en vez de crear una suma lineal de DEF;
- validado provisionalmente en 1v1, perfil pesado, 2 enemigos y 3 enemigos durante Etapas 9A–9C;
- deberá revalidarse contra un perfil enemigo autoritativo de LianQi III cuando exista.

**Raíz Profunda — estabilidad**
- con 2+ Arraigos: +5 Tenacidad adicional;
- con Centro Firme: primera vez que falle un Control contra el usuario, +1 turno de duración.

**Suelo que Sostiene — aguante**
- primera vez que alcanza 3 Arraigos: recupera 5% Vida máxima;
- con Tierra Persistente: +1 turno adicional de duración máxima.

### Tramo III

**Cuerpo de Roca — fortificación**
- **PENDIENTE DE REBENCHMARK tras DEF_CAP2**;
- mantiene la identidad de especialización defensiva;
- los números de DEF máxima deben reconstruirse desde la nueva base 4 → 5 → 5, no desde la antigua 4 → 5 → 6.

**Inamovible — estabilidad**
- +5 Tenacidad con al menos 1 Arraigo;
- ruta completa orientativa: +25 Tenacidad;
- primera vez que resiste Control con Arraigo máximo: siguiente Golpe de Montaña +10 Precisión.

**Montaña Persistente — aguante**
- +1 turno de duración máxima;
- ruta completa: duración base efectiva 3 → 5 antes de extensiones reactivas;
- al alcanzar Arraigo máximo: 5% Vida máxima;
- una vez por activación, si baja de 30% Vida mientras Piel sigue activa: otro 5% Vida máxima.

### Concordancias receptoras — LEGACY / NO CANÓNICAS

> Las entradas siguientes conservan intención histórica, pero sus magnitudes y hooks quedaron superados por la matriz global y la regla de escalado relativo. No deben implementarse. El mapeo canónico se declarará mediante `concordance_hooks[]`.

**Fuego → Tierra · Cimiento cocido**
- +1 DEF adicional mientras Piel permanezca activa.

**Metal → Tierra · Anclaje de hierro**
- primera vez que gana Arraigo por daño directo: +1 Arraigo adicional;
- una vez por activación.

**Agua → Tierra · Sedimentación**
- +1 turno de duración base.

**Viento → Tierra · Impacto de vendaval**
- cada Arraigo: +2 Tenacidad adicional durante esa ejecución.

Como técnica pura, Piel genera Eco de Tierra al activarse.

---

## 7.3 Temblor de Montaña — AOE

El `65%` de duelo se aplica como capa global antes de DEF y antes del redondeo final; no reduce por sí mismo Control, debuffs, duración ni stacks.

Aprobada con corrección de alcance.

Base provisional:

- daño: 6 por enemigo;
- coste: 9 Qi;
- objetivos: **todos los NPC hostiles de la sala**;
- 2+ objetivos: 100% daño;
- 1 objetivo: 65% daño calculado provisional;
- cada impactado recibe **Suelo Inestable: −3 Evasión durante 1 turno**;
- no es Control;
- genera un Eco de Tierra por ejecución válida.

### Tramo I

**Suelo Quebrado — debilitación**
- Suelo Inestable −3 → −5 Evasión.

**Golpe Sísmico — daño**
- +15% directo.

**Resonancia — preparación**
- impactados quedan con Resonancia 1 turno;
- siguiente técnica Tierra que impacte: +5 Precisión y consume Resonancia.

### Tramo II

**Hundimiento — debilitación**
- Suelo Inestable 1 → 2 turnos;
- con Suelo Quebrado: −8 Evasión durante 2 turnos;
- primera técnica Tierra contra cada afectado: +5 Precisión.

**Réplica — daño**
- +20% directo;
- +1 Qi;
- con Golpe Sísmico: +35% total y +5 pp crítico.

**Eco de la Falla — preparación**
- Resonancia dura 2 turnos;
- funciona aun sin Tramo I generando una versión menor;
- con Resonancia: siguiente técnica Tierra +10 Precisión;
- si esa técnica impacta, Suelo Inestable dura +1 turno.

### Tramo III

**Terreno Hundido — debilitación**
- −3 Evasión adicional;
- ruta completa: Suelo Inestable −10 Evasión durante 2 turnos;
- si el enemigo ya tenía reducción de Evasión, puede durar 3 turnos; testear.

**Sacudida Mayor — daño**
- +15% directo;
- +1 Qi;
- ruta completa: +50% directo, +5 pp crítico, +10% daño crítico;
- sigue recibiendo la penalización global AOE al usarse en duelo.

**Falla Resonante — preparación**
- sola: siguiente técnica Tierra +5 Precisión;
- ruta completa: siguiente técnica Tierra +15 Precisión;
- si la receptora puede generar Peso, consume Resonancia y genera +1 carga de Peso adicional.

### Concordancias receptoras — LEGACY / NO CANÓNICAS

> Las entradas siguientes conservan intención histórica, pero no son autoridad mecánica. Se reemplazarán por el mapeo formal de `concordance_hooks[]`.



**Fuego → Tierra · Cimiento cocido**
- +15% daño directo para toda la ejecución.

**Metal → Tierra · Anclaje de hierro**
- +10 pp Penetración % para todos los impactos.

**Agua → Tierra · Sedimentación**
- después del daño, cada impactado recibe −1 DEF durante 2 turnos;
- no mejora retroactivamente el impacto que la aplicó.

**Viento → Tierra · Impacto de vendaval**
- Suelo Inestable recibe −2 Evasión adicional sobre todos los afectados.

Como técnica pura, genera Eco de Tierra.

---

# 8. VIENTO

Identidad general: Evasión, circulación, precisión e impulso sin crear estadísticas de movilidad o Velocidad.

## 8.1 Lanza que Parte Nubes — unitarget

**APROBADA.**

Identidad: ataque directo de Viento basado en trayectoria limpia, precisión propia y aprovechamiento crítico. No crea movilidad ni una segunda tirada de esquiva.

Base provisional:

- daño nominal: 8;
- coste: 6 Qi;
- objetivo: 1 enemigo;
- +5 Precisión propia;
- +5 pp Probabilidad Crítica propia;
- 1 acción → 1 impacto → 1 porción [TECHNIQUE][DIRECT][ELEMENTAL][WIND];
- genera Eco de Viento al impactar.

### Tramo I

**Ojo del Vendaval — precisión**
- +5 Precisión.

**Punta de Tormenta — impacto**
- +20% daño directo.

**Respiración del Cielo — eficiencia**
- coste 6 → 5 Qi.

### Tramo II

**Horizonte Claro — precisión**
- +5 Precisión;
- +5 pp crítico;
- con Ojo del Vendaval: +10% Daño Crítico.

**Nube Partida — impacto**
- +25% daño directo;
- +1 Qi;
- con Punta de Tormenta: +45% daño directo acumulado.

**Corriente Continua — eficiencia**
- −10% coste;
- con Respiración del Cielo: +5 Precisión.

### Tramo III

**Mirada del Cielo Vacío — precisión**
- +5 Precisión;
- +5 pp crítico;
- ruta completa: Precisión propia alta, +10 pp crítico acumulado y +10% Daño Crítico;
- los valores finales de Precisión quedan sujetos a benchmark.

**Lanza que Abre el Cielo — impacto**
- +15% daño directo;
- ruta completa: +60% daño directo.

**Aliento sin Interrupción — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste y +10 Precisión;
- sujeto al piso global futuro de coste.

### Hooks canónicos

```text
role_primary = OFFENSIVE
tags = [TECHNIQUE, DIRECT, ELEMENTAL, WIND, UNITARGET]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PRECISION
- CRIT_CHANCE

mechanical_hooks POR RAMA:
- CRIT_DAMAGE
- QI_COST_PERCENT

concordance_hooks BASE:
- PRECISION
- CRIT_CHANCE

concordance_hooks POR RAMA:
CRITICAL:
- CRIT_DAMAGE
```

`DIRECT_DAMAGE` no se expone como `concordance_hook`.

Recepción elemental base:

- Fuego→Viento · Corriente Ascendente: `CRIT_CHANCE`;
- Metal→Viento · Filo en la Corriente: `PRECISION`;
- Agua→Viento · Velo de Niebla: sin hook compatible;
- Tierra→Viento · Tormenta de Polvo: sin hook compatible.

Si no existe hook compatible, el Eco no se consume por Concordancia; al completar una ejecución válida, el Eco de Viento generado por Lanza puede sustituirlo según el contrato universal.

---

## 8.2 Paso de Nube Ligera — defensiva

**APROBADA.**

Identidad: defensa de Viento basada en Evasión, adaptación y continuidad. "Paso" es una imagen narrativa; la técnica no introduce movilidad, Velocidad ni una segunda tirada de esquiva.

Base provisional:

- coste: 7 Qi;
- duración: 2 turnos;
- +15 Evasión;
- genera Eco de Viento al activarse;
- no se acumula consigo misma;
- reactivar reemplaza la instancia y reinicia duración.

### Tramo I

**Nube Velada — evasión**
- +5 Evasión.

**Estela Vacía — respuesta**
- primera Evasión válida mientras Paso esté activo;
- crea `CORRIENTE_CLARA`;
- la siguiente técnica pura de Viento obtiene +5 Precisión;
- una vez por activación.

**Respiración Ligera — eficiencia**
- coste 7 → 6 Qi.

### Tramo II

**Cuerpo de Nube — evasión**
- +5 Evasión;
- con Nube Velada: Paso alcanza provisionalmente +25 Evasión.

**Huella del Cielo — respuesta**
- sola: primera Evasión válida → siguiente técnica Viento +5 Precisión;
- con Estela Vacía: `CORRIENTE_CLARA` otorga +10 Precisión;
- no concede una acción gratuita ni contraataque automático.

**Circulación del Vendaval — eficiencia**
- −10% coste;
- con Respiración Ligera: duración 2 → 3 turnos.

### Tramo III

**Nube Inalcanzable — evasión**
- +5 Evasión;
- ruta completa provisional: +30 Evasión total otorgada por Paso;
- magnitud final pendiente de benchmark.

**Paso sin Sombra — respuesta**
- sola: primera Evasión válida → siguiente técnica Viento +5 Precisión;
- ruta completa: `CORRIENTE_CLARA` otorga +15 Precisión y +5 pp crítico a la siguiente técnica Viento;
- se consume mediante la regla universal de modificación de la siguiente acción;
- no genera una segunda acción.

**Aliento de las Nubes — eficiencia**
- −10% coste;
- ruta completa: −1 Qi, −20% coste y duración máxima 4 turnos;
- sujeto al piso global futuro de Qi.

### Hooks canónicos

```text
role_primary = DEFENSIVE
tags = [TECHNIQUE, ELEMENTAL, WIND, DEFENSIVE]

mechanical_hooks BASE:
- EVASION_GRANTED
- DEFENSIVE_DURATION

mechanical_hooks POR RAMA:
- REACTIVE_RESPONSE
- QI_COST_PERCENT
- PRECISION
- CRIT_CHANCE

concordance_hooks BASE:
- EVASION_GRANTED
- DEFENSIVE_DURATION

concordance_hooks POR RAMA:
ESTELA:
- REACTIVE_RESPONSE
  trigger = successful_evasion
  scale_target = next_wind_precision

EFFICIENCY:
- QI_COST_PERCENT
```

Recepción elemental:

- Fuego→Viento: prioriza `EVASION_GRANTED`;
- Metal→Viento: `QI_COST_PERCENT` si la rama lo expone; después `REACTIVE_RESPONSE`; después `EVASION_GRANTED`;
- Agua→Viento: `REACTIVE_RESPONSE` si la rama lo expone; si no, `DEFENSIVE_DURATION`;
- Tierra→Viento: `DEFENSIVE_DURATION`.

---

## 8.3 Tijera del Vendaval Partido — AOE

**APROBADA.**

Identidad: corrientes cruzadas de Viento que golpean e interfieren con la lectura del combate. No introduce movilidad, Velocidad ni Control automático.

El `65%` de duelo se aplica como capa global antes de DEF y antes del redondeo final; no reduce por sí mismo debuffs, duración, stacks ni otros estados que no escalen con daño.

Base provisional:

- daño nominal: 6 por enemigo;
- coste: 9 Qi;
- objetivos: todos los `VALID_HOSTILE_COMBATANT`;
- sin target cap;
- sin split;
- 2+ objetivos: 100% magnitud;
- 1 objetivo: `AOE_SINGLE_TARGET_SCALAR = 0.65` provisional;
- cada objetivo cuyo impacto conecte recibe **Turbulencia**;
- genera Eco de Viento por ejecución válida.

### Turbulencia

```text
PRECISION_DEBUFF = -3 Precisión
duration_value = 1
duration_unit = OWNER_TURNS
```

Reglas:

- es un debuff estadístico;
- no es Control;
- no modifica Evasión;
- no impide acciones;
- no representa movilidad;
- sólo se aplica a objetivos cuyo impacto conecte.

La técnica expone además:

```text
AREA_EFFICIENCY
scale_target = offensive_aoe_magnitude
```

### Tramo I

**Ojo de la Tormenta — interferencia**
- Turbulencia: −3 → −5 Precisión.

**Alas Cortantes — tempestad**
- +15% daño directo.

**Corriente Ordenada — circulación**
- coste 9 → 8 Qi;
- +5 Precisión propia.

### Tramo II

**Cielo Turbio — interferencia**
- sola: Turbulencia 1 → 2 OWNER_TURNS;
- con Ojo de la Tormenta: −8 Precisión durante 2 OWNER_TURNS.

**Vendaval Gemelo — tempestad**
- +20% daño directo;
- +1 Qi;
- con Alas Cortantes: +35% daño directo acumulado y +5 pp Probabilidad Crítica.

**Cauce del Aire — circulación**
- −10% coste;
- con Corriente Ordenada: +5 Precisión adicional.

### Tramo III

**Tormenta Ciega — interferencia**
- −3 Precisión adicional;
- ruta completa: Turbulencia −12 Precisión durante 2 OWNER_TURNS;
- el snapshot de Turbulencia se conserva para los objetivos ya afectados aunque otros mueran durante la resolución de la misma AOE.

**Cizalla del Cielo — tempestad**
- +15% daño directo;
- ruta completa: +50% daño directo, +10 pp Probabilidad Crítica y +10% Daño Crítico;
- sigue recibiendo `AOE_SINGLE_TARGET_SCALAR` en duelo.

**Corriente Perfecta — circulación**
- −10% coste;
- ruta completa: −1 Qi, −20% coste y +15 Precisión propia;
- sujeto al piso global futuro de Qi.

### Hooks canónicos

```text
role_primary = OFFENSIVE

tags = [
  TECHNIQUE,
  DIRECT,
  ELEMENTAL,
  WIND,
  AOE,
  DEBUFF
]

mechanical_hooks BASE:
- DIRECT_DAMAGE
- PRECISION_DEBUFF
- DEBUFF_DURATION
- AREA_EFFICIENCY

mechanical_hooks POR RAMA:
INTERFERENCE:
- PRECISION_DEBUFF
- DEBUFF_DURATION

TEMPEST:
- CRIT_CHANCE
- CRIT_DAMAGE

FLOW:
- PRECISION
- QI_COST_PERCENT

concordance_hooks BASE:
- PRECISION_DEBUFF
- DEBUFF_DURATION
- AREA_EFFICIENCY

concordance_hooks POR RAMA:
TEMPEST:
- CRIT_CHANCE
- CRIT_DAMAGE

FLOW:
- PRECISION
```

`DIRECT_DAMAGE` y `QI_COST_PERCENT` no se exponen como `concordance_hooks` en esta técnica.

Recepción elemental:

- Fuego→Viento: base sin hook compatible; ruta Tempestad abre `CRIT_CHANCE`;
- Metal→Viento: base sin hook compatible; ruta Corriente abre `PRECISION`;
- Agua→Viento: `PRECISION_DEBUFF` de base;
- Tierra→Viento: `AREA_EFFICIENCY` de base.

---

# 9. Correcciones retroactivas obligatorias ya identificadas

Antes de considerar cerrado el paquete completo de Arco 1:

1. auditar Concordancias receptoras de:
   - Palma Ardiente;
   - Respiración del Cuerpo-Horno;
   - Círculo de las Cien Ascuas;
   - Destello de Plata;
   - Armadura de Plata;
   - Lluvia de Filos;
   - Latigazo de Marea;
   - Espejo de Luna;
   - Marea de las Ocho Orillas;
   - Golpe de Montaña.
2. aplicar a Círculo, Lluvia y Marea el contrato AOE global de todos los hostiles + 65% provisional en duelo.
3. no crear ramas de “más objetivos” en ninguna AOE.
4. diseñar Viento ya con Concordancias incorporadas desde el inicio.
5. al terminar las 15 técnicas, ajustar:
   - puntos ganados por etapa de LianQi;
   - coste de cada tramo;
   - cuántas técnicas puede maximizar razonablemente un personaje;
   - piso global de reducción de coste de Qi.
6. hacer benchmark numérico de todas las cifras marcadas provisionales.

---

# 10. Estado del paquete elemental

```text
FUEGO   3/3 diseñadas
METAL   3/3 diseñadas
AGUA    3/3 diseñadas
TIERRA  3/3 diseñadas
VIENTO  3/3 diseñadas
```

Total actual: 15/15 técnicas básicas de Arco 1 diseñadas.


---

# Nota global — CONCORDANCIAS LEGACY / SUPERADAS

Cualquier mapeo antiguo de Concordancia escrito dentro de una técnica como aumento absoluto (`+1 DEF`, `+1 stack`, `+N puntos`, etc.) se considera **referencia histórica de intención**, no magnitud canónica.

La matriz global de Concordancias prevalece.

Cuando una Concordancia aumente una magnitud escalable deberá hacerlo porcentualmente sobre el hook receptor. Las transformaciones discretas sólo se conservan cuando son estructurales y coherentes con la identidad global de la relación.


---

# 11. Autoridad actual de hooks de Concordancia

Las declaraciones canónicas de:

```text
role_primary
mechanical_hooks[]
concordance_hooks[]
```

para las 12 técnicas están en:

`docs/experimentos/MAPEO_HOOKS_TECNICAS_ARCO1_2026-09-29.md`

Cualquier bloque anterior denominado "Concordancias receptoras" que contenga bonos absolutos debe leerse como LEGACY / NO CANÓNICO.

La matriz global y el mapeo de hooks prevalecen.
