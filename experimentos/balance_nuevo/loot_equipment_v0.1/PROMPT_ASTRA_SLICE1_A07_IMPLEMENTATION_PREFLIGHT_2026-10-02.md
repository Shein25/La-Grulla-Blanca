# PROMPT ASTRA — COMERCIO ARCO 1 · SLICE 1 NING CAI
## Auditoría de integración A07 + Comercio + Equipo · NO IMPLEMENTAR

Estamos cerrando el primer slice comercial de **La Grulla Blanca**.

Esta ronda es exclusivamente:

```text
AUDITORÍA DE INTEGRACIÓN
+
PLAN DE PATCH MÍNIMO
+
PRUEBAS PROPUESTAS
```

No implementes todavía el Slice 1.

---

# 1. Autoridades humanas ya ratificadas

Tomar como autoridad actual, en este orden:

```text
ARC1_COMMERCE_AUTHORITY_V0_4.json
ARC1_MERCHANT_CAPABILITIES_V0_1.json
ARC1_COMMERCE_TRANSACTION_CONTRACT_V0_1.json
ARC1_COMMERCE_CATALOG_UI_V0_1.json
ARC1_CONTRIBUTION_CLEANSLATE_V0_1.json
ARC1_EQUIPMENT_RUNTIME_BINDING_V0_1.json
ARC1_COMMERCE_SLICE1_A07_PREFLIGHT_V0_1.json
```

No volver a discutir decisiones ya ratificadas salvo contradicción técnica demostrable.

El contrato final es clean-slate:

```text
NO legacy compatibility
NO migration
NO aliases
NO old/new coexistence
NO fallback legacy
NO old save support
```

---

# 2. Guardias de repositorio

No:

```text
main
merge
push
rebase destructivo
```

No modificar:

```text
ROOMS.exits
```

No promover candidate a runtime oficial.

No modificar `grulla-blanca_ver76.html` en esta ronda.

Si tu branch/HEAD productivo actual no coincide con la continuidad real de integración que ya contiene A07 cerrado, documenta el estado exacto y detente antes de aplicar cualquier patch.

---

# 3. A07 no se reabre

A07.9 está cerrado dentro de Arco 1.

Preservar:

```text
canonical handler / gestionarMisionesNpc
>
general conversation host
```

y:

```text
freeAiText=false
```

No rediseñar:

```text
ROLE
SELF_INTRODUCTION
knowledge authority
voice
memory
relations
affinity
NPC↔NPC
authoring corpus
84 player entries
501 frozen lines
```

El Comercio debe ser un dominio lateral.

---

# 4. Actor piloto ratificado

```text
actorId: ning_cai
room: taller_ning_cai
mobility: ANCLADO

capabilities:
SELL
FULFILL
```

No habilitar en Slice 1:

```text
BUY
SERVICE
AUTHORIZE
finite stock
discounts
material recipes
Contribution gate
```

---

# 5. Oferta única del Slice 1

```text
itemId: calzas_sendero_pinos
nombre: Calzas de sendero de pinos
slot: PIERNAS
precio: 8 piedras espirituales
stock: ROUTINE_UNLIMITED
Contribution: 0
permiso: ninguno
sourceMission: M04
minStage: LianQi_II

stats:
hp_max +3
evasion +1
```

Regla de disponibilidad ya ratificada:

```text
NO mostrar por minStage solamente.

La oferta aparece únicamente cuando la fuente real de M04
ha quedado satisfecha/completada según el runtime canónico.
```

Debes identificar el predicado productivo exacto que representa esto.

No inventar un nuevo flag si ya existe una autoridad suficiente.

---

# 6. Entrada desde A07

Objetivo ratificado:

```text
HABLAR Ning Cai
↓
handler canónico tiene prioridad
↓
si handled → FIN
↓
host A07 general
↓
opciones conversacionales normales
+
DOMAIN:COMMERCE si está autorizado
```

La opción visible puede ser:

```text
Quisiera comerciar.
```

Pero técnicamente:

```text
DOMAIN:COMMERCE
≠ authored A07 entry
≠ A07 conversational intent
≠ NPC utterance
```

No debe aumentar ni alterar las 84 entradas authored existentes.

Audita exactamente dónde puede componerse esta opción sin contaminar el corpus ni duplicar respuesta.

---

# 7. Handoff A07 → Comercio

Al elegir Comercio:

1. consumir/inutilizar la capability/lease A07 actual;
2. crear una capability privada one-shot del dominio Comercio;
3. ligarla como mínimo a:
   - actor canónico;
   - room/contexto;
   - player/session owner;
   - runtime generation/epoch disponible;
   - procedencia auténtica de la interacción;
4. impedir spoof/replay.

No diseñar una API pública tipo:

```js
openCommerce("ning_cai")
resumeNpcConversation("ning_cai")
```

si un caller puede fabricarla únicamente con IDs.

Audita el mecanismo privado mínimo compatible con el host real A07.

---

# 8. Catálogo

No crear una UI MMORPG nueva.

Se preserva el patrón textual/listado del MUD.

Slice 1:

```text
TALLER DE NING CAI

Piedras espirituales: <actual>

Calzas de sendero de pinos
HP +3 · EVA +1
8 piedras

[COMPRAR]
[VOLVER A LA CONVERSACIÓN]
[CERRAR]
```

Puedes reutilizar infraestructura visual/input ya existente si es segura.

No reutilizar lógica económica legacy.

La UI:

```text
NO es autoridad de precio
NO es autoridad de stock
NO es autoridad de gates
NO muta player directamente
```

---

# 9. Request económico

El intent mínimo debe equivaler a:

```js
{
  type: "BUY",
  npcId: "ning_cai",
  itemId: "calzas_sendero_pinos",
  quantity: 1
}
```

La UI NO debe entregar como autoridad:

```text
price
stock
Contribution
permission
materials
player balance
availability
discount
```

---

# 10. Pipeline ratificado

Mantener:

```text
EVALUATE
→ CONFIRM
→ REVALIDATE
→ BUILD_DELTA
→ COMMIT
→ RECEIPT
```

En confirmación, volver a resolver desde autoridad real:

```text
actor
copresence
room
capability
offer binding
M04 availability
price=8
funds
item definition
quantity
session validity
```

Delta Slice 1:

```text
piedras -8
inventario +1 calzas_sendero_pinos
```

No autoequipar.

ROUTINE_UNLIMITED no persiste cantidad de stock.

---

# 11. Atomicidad / persistencia

La compra debe ser todo-o-nada respecto del estado observable.

Audita el writer nativo real de save/persistencia que debe usarse.

Preferencia ratificada de diseño:

```text
preparar estado/snapshot aislado
→ validar
→ durable write nativo
→ publicar RAM
→ receipt
```

No:

```text
restar piedras live
→ save
→ push item live
```

Debes documentar con exactitud:

- punto durable real;
- qué devuelve el writer;
- qué ocurre ante throw/false;
- qué ocurre ante outcome incierto;
- cómo se impide retry automático del mismo token;
- cómo se invalida A07/Commerce durante LOAD/new game/etc.

SAVE objetivo clean-slate:

```text
SAVE_SCHEMA_VERSION = 3
facciones_version = 2
```

No migrar schema 2.

---

# 12. Doble click / replay

Debe existir defensa en dos capas:

```text
UI reentry guard
+
engine one-shot request/prepared capability guard
```

El mismo token/request no puede:

```text
cobrar dos veces
entregar dos objetos
persistir dos commits
```

No prometas idempotencia persistente entre LOADs si no existe ledger persistido.

LOAD invalida la sesión anterior.

---

# 13. Volver a conversación

Ratificado:

```text
[VOLVER A LA CONVERSACIÓN]
```

NO debe:

```text
llamar cmd_hablar()
volver a ejecutar gestionarMisionesNpc()
repetir SELF_INTRODUCTION
repetir opening por obligación
reutilizar lease A07 antiguo
```

Debe:

1. cerrar/consumir la sesión de Comercio;
2. emitir capability privada de retorno;
3. revalidar Ning Cai, room, copresencia, player/actor state y runtime generation;
4. si todo es válido, crear una **NUEVA** capability A07;
5. reconstruir las opciones disponibles del mismo actor;
6. si ya no es válido, cerrar a gameplay normal.

Determina el binding técnico exacto con el host actual.

---

# 14. Cerrar / movimiento

```text
[CERRAR]
→ destruir contexto comercial
→ gameplay normal
```

Movimiento:

```text
cambio de room
→ invalidar Comercio
→ resolver movimiento normal
```

No bloquear al jugador dentro del catálogo.

No cambiar `ROOMS.exits`.

---

# 15. Equipo nuevo

Slice 1 no termina conceptualmente en inventario.

El item comprado debe poder equiparse después mediante el contrato nuevo:

```text
equipado[PIERNAS] = array
capacity = 1
```

No usar slots legacy.

Al equipar las Calzas:

```text
NEW_COMBAT_STATS:
hp_max +3
evasion +1
```

Semántica HP ratificada:

```text
EQUIP:
max HP +3
current HP NO aumenta

UNEQUIP:
max HP -3
current HP = min(current HP, new max HP)
```

No debe existir curación por swap de equipo.

No traducir vía:

```text
ataque
daño
qi_med
slot piernas legacy
```

---

# 16. Qué debes auditar exactamente

Entrega locators concretos para:

1. `cmd_hablar()`;
2. canonical handler / `gestionarMisionesNpc`;
3. host general A07.9;
4. construcción/presentación de choices del jugador;
5. lifecycle/capability/lease A07;
6. eventos de invalidación SAVE/LOAD/new game/movement/death/combat;
7. current room/copresence authority;
8. piedras espirituales;
9. inventario;
10. writer durable de save;
11. ITEMS/equipment registration;
12. equip/unequip;
13. stat aggregation/new combat stats;
14. UI/input reusable para catálogo.

Para cada uno:

```text
archivo
función/símbolo
locator/fingerprint estable
read/write
qué puede reutilizarse
qué extensión mínima requiere
riesgo
```

---

# 17. Tests mínimos requeridos para una futura implementación

Diseña la suite exacta para demostrar:

```text
canonical handler handled
→ no Commerce
→ no segunda respuesta

Ning Cai elegible
→ una sola opción DOMAIN:COMMERCE

DOMAIN:COMMERCE
→ no altera 84 authored entries

8 piedras
→ -8 +1 item

7 piedras
→ 0 mutation

precio UI adulterado
→ se ignora

double click/replay
→ máximo un commit

movimiento antes de confirmar
→ 0 mutation

CERRAR
→ gameplay normal

VOLVER
→ nueva capability A07
→ sin HABLAR/misión replay

save/load tras compra
→ piedras/item correctos

equipar calzas
→ PIERNAS contiene exactamente 1
→ hp_max +3
→ evasion +1
→ current HP no sube

desequipar
→ exactamente 1 item vuelve al inventario
→ current HP clamp correcto
```

Añadir regresión A07 relevante.

---

# 18. No implementar todavía

Esta ronda NO autoriza modificar:

```text
grulla-blanca_ver76.html
candidate HTML productivo
A07 closed implementation
runtime economy
save schema real
ITEMS real
equipment real
```

Puedes crear únicamente:

```text
docs
audit scripts
static tests
matrices
patch proposal
review package
```

No aplicar el patch.

---

# 19. Entrega obligatoria

Entregar un paquete de review con, como mínimo:

```text
README_REVIEW.md
RESULTADOS.md
MANIFEST_SHA256.txt

git/
  BRANCH.txt
  HEAD.txt
  STATUS.txt
  DIFF.patch
  CHANGED_FILES.txt

contracts/
  SLICE1_BINDING_MATRIX.json
  SLICE1_LIFECYCLE_MATRIX.json
  SLICE1_TRANSACTION_BOUNDARY.json
  SLICE1_EQUIPMENT_BINDING.json

evidence/
  static_checks.txt
  regression_plan.txt

patch/
  PROPOSED_PATCH_PLAN.md
```

No necesito un HTML modificado en esta ronda.

---

# 20. Veredicto requerido

Termina con exactamente uno:

```text
SLICE1_A07_INTEGRATION_READY_FOR_LIMITED_IMPLEMENTATION
```

o:

```text
SLICE1_A07_INTEGRATION_BLOCKED
```

Si bloqueado, enumera cada blocker con evidencia concreta y propuesta mínima.

No rediseñes A07, Comercio o equipo para resolver un blocker sin devolverlo primero a revisión humana.
