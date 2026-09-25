# Fuente Maestra ver55 — selección literal T281 · M16

**Origen:** `La_Grulla_Blanca_Fuente_Maestra_Fusionada_ver55`  
**Turno:** T281  
**Fecha UTC:** 2026-09-20T07:31:21.863Z  
**Carácter:** SELECCIÓN LITERAL PARA AUDITORÍA. No sustituye el turno completo de la Fuente Maestra.

---

> La clave es que M16 **no sea seis misiones pequeñas simultáneas**. El jugador participa personalmente en aproximadamente dos frentes; los otros cuatro son atendidos por la gente que ha conocido durante todo el arco. El resultado depende de cómo llega la secta a la crisis, no de haber completado una checklist secreta.

Inicio recuperado:

```text
arc1.estado = LIV_CRISIS
M16 = ACTIVA

frentes:
MEDICINA     PENDIENTE
RUTAS        PENDIENTE
FORMACIONES  PENDIENTE
RECURSOS     PENDIENTE
SAUCES       PENDIENTE
JARDINES     PENDIENTE
```

También se activa temporalmente `EMERGENCIA_SECTA`, sólo para rutas necesarias durante la crisis; no abre Archivos restringidos, Núcleo profundo, sellos antiguos ni lugares sin relación con la emergencia.

## Los seis frentes — síntesis literal de T281

- **MEDICINA:** inversión de circulación, pacientes con meridianos vulnerables; Lan Meihua con Chen Bo y Yao Fen.
- **RUTAS:** fauna desplazada, pasos inestables y comunicaciones; Jiang Rui y Ren Bo.
- **FORMACIONES:** matrices exteriores se sobrecompensan; He Zhen con Wen Tao.
- **RECURSOS:** talleres/almacenes/conducciones bajo pulsos irregulares y necesidades incompatibles; Duan Shibo, Ma Qiren y Lu Cheng.
- **SAUCES:** caudal redirigido amenaza personas, viviendas y cultivos; Xu An con apoyo local.
- **JARDINES:** qi de riego alterado, cultivos y semillas en riesgo; Su Lian.

> Cada intervención personal debería durar aproximadamente **una pequeña secuencia de 2–4 objetivos**, no una misión completa con introducción, desarrollo y epílogo.

> No habrá pantalla `FRENTES DISPONIBLES: 6 / INTERVENCIONES RESTANTES: 2`.

> Los compañeros no son unidades que asignamos.

Asignaciones típicas citadas por T281:

```text
Lin Yue  → RUTAS
Han Qiao → RECURSOS
Zhao Wen → FORMACIONES
Mei Lian → SAUCES o MEDICINA
Guo Chen → RECURSOS o RUTAS
Luo Yan  → FORMACIONES / coordinación
```

La asignación no se congela como única y depende de trayectoria/ubicación. Afinidad no controla la autonomía básica.

## Resolución

T281 usa cuatro factores semánticos:

```text
RESPONSABLE
PREPARACION
APOYO
INTERVENCION
```

El macroresultado no lo decide `Azar.random()`.

Estados de coste:

```text
ESTABLE
COSTOSO
DAÑADO
```

`DAÑADO` nunca puede impedir completar M17.

Los frentes pueden influirse moderadamente; no deben formar un dominó de soft-locks.

Los seis atajos de Primera Ala pueden ayudar, pero ningún frente exige uno y 6/6 no produce automáticamente una crisis perfecta.

## EMERGENCIA_SECTA

```text
si acceso admite EMERGENCIA
y emergencia activa
→ autorizado temporalmente
```

No sustituye `ARCHIVO_RESTRINGIDO`, `PRIMERA_ALA_INVESTIGACION`, `NUCLEO_PROFUNDO` ni abre barreras físicas.

Al concluir: `EMERGENCIA_SECTA = EXPIRADA`.

## Secuencia

```text
DESENCADENADA
↓
primeros seis informes
↓
RESPUESTA I
↓
primer frente personal
↓
actualización de situación
↓
RESPUESTA II
↓
segundo frente personal
↓
RESOLUCIÓN DE FRENTES
↓
informes de los equipos
↓
ESTABILIZACIÓN
↓
M16 HECHA
```

El resolvedor de los otros frentes se ejecuta una sola vez; repetirlo devuelve los mismos resultados.

M16 concede reconocimiento institucional, pero no debe puntuar cada frente como competición. No atender un frente no reduce Prestigio automáticamente.

No existe resultado perfecto global: incluso una partida muy preparada conserva heridos, desgaste, daños menores o interrupciones.

Invariante final literal:

```text
M16 == HECHA
→ ningún frente == PENDIENTE
```

**Fin de selección. Para desempates o matices, consultar T281 completo en la Fuente Maestra.**
