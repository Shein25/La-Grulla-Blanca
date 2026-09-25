Usá este backup como estado actual y retomá exactamente desde este punto de La Grulla Blanca.

FUENTES DE CONTINUIDAD:
- experimentos/backups/BACKUP_MAESTRO_CONTINUIDAD_2026-09-25_CORTE_MOTOR_COMBATE.md
- experimentos/backups/HANDOFF_MAESTRO_EXPERIMENTOS_2026-09-24.md
- el ZIP de continuidad que adjunto en este chat.

REGLAS:
- Verificá GitHub en vivo antes de afirmar HEAD/branch/PR.
- No mezcles producción con experimentos.
- No reabras ni modifiques silenciosamente Monster Combat AI v0.1 ni Autonomous NPC Loop v0.1: ambos están cerrados y mergeados como snapshots experimentales.
- No hagas merge ni toques main sin mi orden explícita.
- No avances integración Adaptive Ecology × Monster AI hasta que Adaptive Ecology REV2 quede auditada y congelada.
- No toques implement/3c6-prologo-m01-m07 durante esta auditoría; sólo leer.
- No inventes capacidades del motor de combate: distinguí soporte real, soporte declarativo/UI y soporte todavía no conectado.

ESTADO CLAVE:
- main = de3a7593dc59120f5940b3589bc42ed6e500ba9b
- producción 3C.6 = implement/3c6-prologo-m01-m07 @ 748bd4480e37fd2523fa833081b20522b9724dab
- archivo productivo = grulla-blanca_ver75.html
- blob ver75 = 1c897be6ddf3d18436a043fab0c848ef7f3fb18c
- Monster Combat AI v0.1: cerrado, auditado, PR #13 mergeado.
- Autonomous NPC Loop v0.1: cerrado, auditado, PR #12 mergeado.
- Adaptive Ecology v0.1: diseño FINAL congelado; implementación REV2 pendiente de Claude. No existe todavía rama experiment/monster-ecology-adaptation-v0.1.

TAREA ACTIVA AL RETOMAR:
Continuar la auditoría del motor de combate real y diseñar el contrato experimental “Combat Ability Contract v0.1”.

YA VERIFICADO:
1. class Combate de ver74 y ver75 tiene la misma lógica; sólo cambian espacios en blanco.
2. El jugador ya soporta realmente:
   - ofensiva y AOE;
   - precisión/ataque;
   - critMin y critMult;
   - quemadura;
   - debuff de ataque;
   - control/atadura;
   - evasión temporal;
   - defensa temporal;
   - absorción con reserva;
   - DEFENDER porcentual;
   - concordancia/elementos.
3. Estados declarados:
   esquiva, defensa, guardia, dano, ataque, tenacidad, quemadura, veneno, debil, atadura.
4. IMPORTANTE: dano y ataque existen como categorías preparadas/UI, pero todavía no están conectados como buffs temporales genéricos al pipeline.
5. Contrato actual de técnica enemiga:
   { name, cada, ataque?, daño?, veneno?, quemadura?, drenaQi? }
6. respuestaEnemigos() permite técnica periódica, ataque/daño puntual, veneno, quemadura y drenaQi.
7. ASIMETRÍA CRÍTICA:
   aplicarAMob() puede guardar estados genéricos en un enemigo, pero el pipeline de ataque contra mobs no consulta actualmente estados del mob de defensa, evasión, guardia/absorción, ataque o dano. Guardar el estado no implica que funcione.

DECISIÓN ARQUITECTÓNICA:
effectiveKit no debe contener sólo ataques. Debe poder incluir ofensiva, defensa, evasión, absorción, control, buffs de ataque, crítico, daño crítico y habilidades híbridas.

PRINCIPIO:
Adaptive Ecology habilita repertorio.
Monster Combat AI decide.
Combat Engine resuelve.

SIGUIENTE TRABAJO:
- terminar de mapear funciones y fronteras de Combate;
- crear una matriz “capacidad / soporte real / soporte declarativo / falta adapter”;
- diseñar Combat Ability Contract v0.1 sin tocar producción;
- incluir al menos OFFENSE, DEFENSE, EVASION, ABSORPTION, CONTROL, BUFF_ATTACK, BUFF_CRIT_CHANCE, BUFF_CRIT_DAMAGE y HYBRID;
- definir qué señales necesita Monster AI para decidir sin hacer future-read;
- mantener daño, crítico, defensa, evasión y absorción dentro del motor, no dentro de la IA;
- preparar luego especificación + tests sintéticos + prompt de implementación experimental.

No empieces reescribiendo código productivo. Primero completá la auditoría y presentame el mapa del motor + propuesta de contrato para revisar.
