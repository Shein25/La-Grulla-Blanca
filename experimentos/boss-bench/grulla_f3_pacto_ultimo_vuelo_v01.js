"use strict";

/**
 * PACTO_ULTIMO_VUELO — helper contractual LAB.
 *
 * No conoce IDs de NPC, UI ni runtime. El integrador debe invocarlo únicamente
 * para la Grulla al entrar en F3 y en el punto autoritativo de commit a Vida.
 */

const PACTO_ESTADO = Object.freeze({
  ACTIVE: "ACTIVE",
  CRACKED_WAITING_FOR_F3_ACTION: "CRACKED_WAITING_FOR_F3_ACTION",
  RELEASED: "RELEASED",
});

function crearPactoUltimoVuelo() {
  return {
    state: PACTO_ESTADO.ACTIVE,
    lethalPreventions: 0,
    preventedLethalDamage: 0,
    maxSingleOverkillPrevented: 0,
    skipAttempted: false,
    firstRealF3ActionResolved: false,
  };
}

function pactoProtege(pacto) {
  return !!pacto && pacto.state !== PACTO_ESTADO.RELEASED;
}

/**
 * Aplica un compromiso de daño a Vida ya calculado por el motor.
 * Retorna hpAfter y telemetría; no decide DEF/Abs/crit.
 */
function comprometerDanioVidaConPacto({ hpBefore, lifeDamage, pacto, source = "UNKNOWN" }) {
  const hp = Math.max(0, Number(hpBefore) || 0);
  const dmg = Math.max(0, Number(lifeDamage) || 0);
  const rawAfter = hp - dmg;

  if (!pactoProtege(pacto) || rawAfter > 0) {
    return {
      hpAfter: Math.max(0, rawAfter),
      lethalPrevented: false,
      overkillPrevented: 0,
      source,
    };
  }

  // La Vida no puede caer por debajo de 1 mientras el Pacto protege.
  const hpAfter = 1;
  const overkillPrevented = Math.max(0, 1 - rawAfter);

  pacto.state = PACTO_ESTADO.CRACKED_WAITING_FOR_F3_ACTION;
  pacto.lethalPreventions += 1;
  pacto.preventedLethalDamage += overkillPrevented;
  pacto.maxSingleOverkillPrevented = Math.max(
    pacto.maxSingleOverkillPrevented,
    overkillPrevented
  );
  pacto.skipAttempted = true;

  return {
    hpAfter,
    lethalPrevented: true,
    overkillPrevented,
    source,
  };
}

/**
 * Sólo libera el Pacto cuando una intención REAL de F3 terminó de resolverse.
 * Un intento bloqueado por Control no cuenta.
 */
function registrarResolucionIntencionF3(pacto, {
  phase,
  realIntent = false,
  resolved = false,
  prevented = false,
} = {}) {
  if (!pactoProtege(pacto)) return false;
  if (Number(phase) !== 3) return false;
  if (!realIntent || !resolved || prevented) return false;

  pacto.firstRealF3ActionResolved = true;
  pacto.state = PACTO_ESTADO.RELEASED;
  return true;
}

function selfCheckPactoUltimoVuelo() {
  const failures = [];

  const check = (cond, name) => { if (!cond) failures.push(name); };

  // 1. no letal normal
  {
    const p = crearPactoUltimoVuelo();
    const r = comprometerDanioVidaConPacto({hpBefore:50, lifeDamage:20, pacto:p, source:"DIRECT"});
    check(r.hpAfter === 30 && !r.lethalPrevented && p.state === PACTO_ESTADO.ACTIVE, "nonlethal");
  }

  // 2. letal directo queda en 1
  {
    const p = crearPactoUltimoVuelo();
    const r = comprometerDanioVidaConPacto({hpBefore:10, lifeDamage:25, pacto:p, source:"ULTI"});
    check(r.hpAfter === 1 && r.lethalPrevented && p.skipAttempted, "direct_lethal_floor");
  }

  // 3. segundo hit de la misma acción tampoco puede matar
  {
    const p = crearPactoUltimoVuelo();
    const a = comprometerDanioVidaConPacto({hpBefore:8, lifeDamage:12, pacto:p, source:"MULTIHIT_1"});
    const b = comprometerDanioVidaConPacto({hpBefore:a.hpAfter, lifeDamage:99, pacto:p, source:"MULTIHIT_2"});
    check(a.hpAfter === 1 && b.hpAfter === 1 && p.lethalPreventions === 2, "multihit_cannot_bypass");
  }

  // 4. DOT/Hemorragia quedan cubiertos por el mismo commit
  {
    const p = crearPactoUltimoVuelo();
    const r = comprometerDanioVidaConPacto({hpBefore:3, lifeDamage:4, pacto:p, source:"DOT"});
    check(r.hpAfter === 1 && r.lethalPrevented, "dot_lethal_floor");
  }

  // 5. control que impide actuar NO libera
  {
    const p = crearPactoUltimoVuelo();
    registrarResolucionIntencionF3(p, {phase:3, realIntent:true, resolved:false, prevented:true});
    check(p.state === PACTO_ESTADO.ACTIVE, "control_does_not_release");
  }

  // 6. primera intención real resuelta sí libera
  {
    const p = crearPactoUltimoVuelo();
    const released = registrarResolucionIntencionF3(p, {phase:3, realIntent:true, resolved:true, prevented:false});
    check(released && p.state === PACTO_ESTADO.RELEASED, "real_f3_action_releases");
    const r = comprometerDanioVidaConPacto({hpBefore:1, lifeDamage:1, pacto:p, source:"POST_RELEASE"});
    check(r.hpAfter === 0 && !r.lethalPrevented, "kill_allowed_after_release");
  }

  return {
    pass: failures.length === 0,
    failures,
    tests: 6,
  };
}

if (typeof module !== "undefined") {
  module.exports = {
    PACTO_ESTADO,
    crearPactoUltimoVuelo,
    pactoProtege,
    comprometerDanioVidaConPacto,
    registrarResolucionIntencionF3,
    selfCheckPactoUltimoVuelo,
  };

  if (require.main === module) {
    const result = selfCheckPactoUltimoVuelo();
    console.log(JSON.stringify(result, null, 2));
    if (!result.pass) process.exitCode = 1;
  }
}
