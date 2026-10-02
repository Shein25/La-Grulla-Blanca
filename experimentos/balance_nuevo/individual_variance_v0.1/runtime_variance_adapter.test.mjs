import fs from "node:fs";
import assert from "node:assert/strict";
import { instantiateMonsterVariance } from "./runtime_variance_adapter.mjs";

const cfg = JSON.parse(fs.readFileSync(
  new URL("./monster_individual_variance_v0.1.json", import.meta.url),
  "utf8"
));
const registry = JSON.parse(fs.readFileSync(
  new URL("../monster_arc1_registry.json", import.meta.url),
  "utf8"
));

const species = ["rata_qi","avispa_jade","serpiente_qi","mono_pildoras","lobo_espiritual","sapo_ceniza","escarabajo_hierro","pez_lunar","anguila_estelar","devorador_niebla","halcon_tormenta"];

function sequenceRandom(values) {
  let i = 0;
  return () => values[Math.min(i++, values.length - 1)];
}

for (const sid of species) {
  const canonical = registry.profiles[sid];
  const before = JSON.stringify(canonical);

  const low = instantiateMonsterVariance({
    speciesId:sid,
    canonicalProfile:canonical,
    varianceConfig:cfg,
    random:() => 0,
    instanceId:`${sid}:low`,
  });
  assert.equal(low.species_id, sid);
  assert.equal(low.mutant, false);
  assert.equal(low.rewards.loot_multiplier, 1);
  assert.equal(low.rewards.combat_xp_multiplier, 1);
  assert.equal(low.rewards.apply_to_profession_xp, false);
  assert.equal(low.rewards.scale_legacy_drop_probability, false);

  for (const key of cfg.variable_stats) {
    assert.equal(low.stats[key], cfg.species[sid].base[key], `${sid} ${key} low`);
  }

  const high = instantiateMonsterVariance({
    speciesId:sid,
    canonicalProfile:canonical,
    varianceConfig:cfg,
    random:() => 0.999999999,
    instanceId:`${sid}:high`,
  });
  assert.equal(high.mutant, true, `${sid} all-high should be Mutante`);
  assert.equal(high.suffix, "Mutante");
  assert.match(high.display_name, / Mutante$/);
  assert.equal(high.rewards.loot_multiplier, 1.5);
  assert.equal(high.rewards.combat_xp_multiplier, 1.5);
  assert.equal(high.rewards.unique_drop_probability_multiplier, 1);

  for (const key of cfg.variable_stats) {
    assert.ok(high.stats[key] >= cfg.species[sid].base[key], `${sid} ${key} below T0`);
    assert.ok(high.stats[key] <= cfg.species[sid].upper_envelope[key], `${sid} ${key} above envelope`);
  }

  assert.equal(JSON.stringify(canonical), before, `${sid}: canonical profile mutated`);
  assert.equal(high.combat_profile.id, canonical.id);
  assert.equal(high.combat_profile.stats_status, "READY");
  assert.equal(high.adaptive.tier_granted_by_variance, null);
}

const mono = registry.profiles.mono_pildoras;
const monoHigh = instantiateMonsterVariance({
  speciesId:"mono_pildoras",
  canonicalProfile:mono,
  varianceConfig:cfg,
  random:() => 0.999999999,
});
assert.equal(monoHigh.combat_profile.technique.params.qi_drain, 5);
assert.equal(monoHigh.combat_profile.technique.params.cadence, 2);
assert.equal(monoHigh.combat_profile.technique.name, "Manotazo al Dantian");

const loboLow = instantiateMonsterVariance({
  speciesId:"lobo_espiritual",
  canonicalProfile:registry.profiles.lobo_espiritual,
  varianceConfig:cfg,
  random:() => 0,
});
assert.equal(loboLow.stats.precision, 97);


for (const sid of ["eco_caido","sapo_caldera","rey_escarabajo","sombra_ahogada","guardian_coral","mantis_nube","centinela_pluma"]) {
  assert.throws(() => instantiateMonsterVariance({
    speciesId:sid,
    canonicalProfile:registry.profiles[sid],
    varianceConfig:cfg,
    random:() => 0.5,
  }), /unique species variance forbidden/);
}
assert.equal(cfg.guards.unique_species_variance_forbidden, true);

console.log("PASS: runtime variance adapter preserves canonical T0 and identity");
console.log("PASS: Mutante metadata exposes x1.5 loot/combat XP without touching profession XP/drop probabilities");
