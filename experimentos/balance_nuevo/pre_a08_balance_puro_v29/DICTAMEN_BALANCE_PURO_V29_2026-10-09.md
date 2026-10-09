# PRE-A08 V29 — Balance puro: ataque básico y momento de tratamiento

**Fecha 2026-10-09 · LAB PASS · NO CANON · NO RUNTIME · NO FREEZE.**
Continuidad V28. No se estudian precios, comercio, inventario disponible ni economía.

## Evidencias y comparaciones
- El `monster_arc1_registry.json` LAB READY declara para `serpiente_qi` daño básico `1d2+2` y especial `POISON_DOT` sin `direct_damage`; `avispa_jade` daño básico `1d2+1` e igualmente no declara daño directo en su especial. `sapo_ceniza` sí declara `direct_damage=1d2+4` y `BURN_DOT`.
- El antiguo `grulla-blanca_ver74.html::Combate.respuestaEnemigos()` ejecutaba `atacar(eMod,def)` durante el especial y solo reemplazaba el daño básico si `tec.daño` existía. El nuevo `etapa19b_combat_engine.py::execute_monster_turn()` ejecuta solo un chequeo de precisión cuando falta `direct_damage`, pero permite `MONSTER_DOT` por impacto. Ello entra en tensión con la regla de aplicación persistente que exige daño real a Vida.
- Dos brazos diagnósticos: `STRICT_HP_DAMAGE` usa descriptor LAB sin daño extra; `VER74_BASIC_DIRECT` restaura SOLO EN LAB el golpe básico durante un especial sin `direct_damage` y exige `actual_hp_damage>0` para envenenar. NO ratificar todavía esa traducción. Sapo es control: ambos modos equivalen.

## Batería realizada
- DISCOVERY semillas 103100–103101: 79.584 ejecuciones reales; HOLDOUT 103500–103501: 80.340.
- **159.924 ejecuciones nuevas** = 1.920 primeros combates únicos + 158.004 segundos; **161.280 filas de escenarios comparativos**, pues las siete preparaciones reutilizan el mismo primer combate.
- Primer encuentro T0 con Serpiente, Avispa o Sapo; segundo contra seis monstruos originales LII, T1/T2. Cinco raíces, cuatro builds por raíz, dos políticas, M03/COAT_DEF1 candidata.
- Preparaciones: sin remedio, cura antes o después de caminar, HP solo, cura antes+HP, cura después+HP, remedio incompatible. Una caminata consume un pulso de aflicción; aplicar medicina fuera del combate no lo consume. HP Templada estable `3d4+9` RATIFICADA.
- **0 timeouts, 0 acciones debidas omitidas**; remedio incompatible idéntico al control sin tratar y ausencia de infección implica identidad de resultados entre tratar y no tratar. Prueba fría separada: **40.320 filas × 44 columnas coinciden exactamente**, salvo etiqueta `cohort`; no se suman a combates nuevos.
- QA del adaptador: algunos supervivientes LAB terminan con HP fraccional positivo inferior a 1. El suelo protector de 1 HP para DOT exterior no puede convertirse en curación accidental. Se corrigió el adaptador de laboratorio sin tocar runtime.

## Aflicciones al ganar el primer duelo: conteos sin duplicación
| Origen y modalidad | Primeras victorias / 320 | Aflicción activa ENTRE VICTORIAS | Expira con 1 caminata | Persiste tras caminar |
|---|---:|---:|---:|---:|
| Serpiente STRICT | 320 | 0 | 0 | 0 |
| Serpiente VER74_BASIC_DIRECT | 319 | **162** | 63 | 99 |
| Avispa STRICT | 320 | 0 | 0 | 0 |
| Avispa VER74_BASIC_DIRECT | 320 | **62** | **62** | 0 |
| Sapo STRICT | 301 | **142** | 43 | 99 |
| Sapo VER74_BASIC_DIRECT | 301 | **142** | 43 | 99 |

Atención: 163 Serpiente / 156 Sapo son estados después del primer combate INCLUYENDO derrotas; el denominador correcto para secuencias supervivientes es 162 / 142. Cada primer encuentro puede continuarse ante seis especies y dos tiers; no multiplicar infectados únicos por 12.

## Victoria en segundo duelo T2 + Sobretúnica DEF1 candidata, solo entre infectados que ganaron el primero
| Origen | Contextos pareados | Cura+HP ANTES | Cura+HP DESPUÉS | Ventaja antes |
|---|---:|---:|---:|---:|
| Avispa (VER74_BASIC_DIRECT) | 156 | 21,80 % | 19,23 % | **+2,56 pp** |
| Serpiente (VER74_BASIC_DIRECT) | 474 | 15,19 % | 11,81 % | **+3,38 pp** |
| Sapo (STRICT) | 480 | 12,29 % | 7,08 % | **+5,21 pp** |

Bootstrap descriptivo con unidad de remuestreo = PRIMER ENCUENTRO (6 monstruos secundarios comparten primer estado), 4.000 remuestreos:
- Avispa: 26 primeros encuentros infectados del estrato; ventaja +2,56 pp, intervalo [0,64; 5,13] pp.
- Serpiente: 79 primeros encuentros infectados; ventaja +3,38 pp, intervalo [1,90; 5,06] pp.
- Sapo: 80 primeros encuentros infectados; ventaja +5,21 pp, intervalo [3,13; 7,50] pp.
Son sensibilidades de un conjunto concreto de monstruos y políticas, no estimadores universales para el juego.

## Dictamen y límites
1. **Tratar ANTES de caminar** evita el daño físico del próximo pulso. Tratar DESPUÉS elimina el estado restante si aún está activo, sin restituir HP perdido. Si ya expiró, no se gasta medicina. Avispa mantiene un solo pulso restante al terminar la primera pelea en los casos infectados ensayados.
2. **NO modificar** daños DOT ni potencia de antídotos/bálsamos. V29 prueba oportunidad de uso y fidelidad de fuente, no un fallo numérico de tratamiento.
3. **Pendiente de autoridad humana:** ¿Serpiente y Avispa deben llevar componente directo explícito igual al golpe básico de la especie, preservando `ON_HP_DAMAGE` (antecedente ver74), o se ratifica un estado puro con una excepción formal de aplicación por impacto? La segunda alternativa exigiría cambiar contrato; no se aprueba implícitamente. La primera tampoco se implementa sin ratificación del contrato nuevo de monstruos.
4. Mantener Sobretúnica DEF+1/HP+2 como candidato no aplicado; conservar monstruos originales, V19 Cangrejo/Jabalí pendientes, V25 Embalse pendiente, V26 magnitudes condicionales no ratificadas.
5. V29 es un LAB con fuentes de ataque realmente ejecutadas. NO prueba persistencia de producción en ver76/A08, adquisición real de consumibles, T3/T4, AOE o jefes. **No cerrar PRE-A08 integral ni resolver B01 todavía.**

## Paquete externo y guardias
- ZIP `GRULLA_PRE_A08_V29_BALANCE_PURO_GOLPE_Y_TRATAMIENTOS_2026-10-09.zip`, SHA-256 `f5e6f20e82bcb467fe3b9495d451b9c99fb79de0a6f758bbf56e978949cfcde6`, 64 archivos; CRC, manifiesto, ocho pruebas mecánicas y COLD portable 40.320 filas exactas: PASS.
- Runner, bruto gzip, README, QA por cohorte y CI agrupados están en el ZIP adjunto a la conversación, NO en el repositorio.
- Rama autorizada exclusivamente; no main, no merge, no HTML, no ROOMS.exits, no A07, no cambios de comercio ni valores canónicos.
