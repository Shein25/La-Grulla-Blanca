"""Derivación estable de seeds independiente del orden de ejecución."""
from __future__ import annotations

import hashlib

MASTER_SEED=20261001


def stable_seed(*parts,master_seed: int=MASTER_SEED) -> int:
    token="|".join([str(master_seed),*(str(x) for x in parts)])
    digest=hashlib.sha256(token.encode("utf-8")).digest()
    # random.Random acepta enteros arbitrarios; 64 bits son suficientes y
    # facilitan exportación interoperable.
    return int.from_bytes(digest[:8],"big",signed=False)
