# Player Power Envelope LI — FIX5

FIX5 corrige exclusivamente el remanente end-to-end de F3-R01 detectado por Astra en FIX4.
No rebalancea técnicas, monstruos, equipo, policies ni progresión.

Después de execute_missing(screen), FIX5 llama validate_resume_state(..., allow_create_selection=True), reconstruye/verifica la selección determinista y expected refine, valida cualquier fila refine existente contra esa autoridad y sólo entonces continúa con execute_missing(refine).

Fuego FIX3 permanece sellado y NO se repite.

- Fuego FIX3 recipe: 15586b2cfc1aafe2deb5c95988c2b55a5482758770d788a92aaa4c6fc36b9ebc
- CRN epoch: 13b6c488bfd3cf516b76cdea1ff22a38f981dbe5f565d6fa435378ee720050c8
- Fuego REVIEW SHA-256: b4f65c18f6d176d4163faa1d5b1c10dab9c9961910df821eab9d93c259a2c2f2
- FIX5 runner SHA-256: eeaf8c835be407be9b5219368f82a9179adb07e362234b0bef8e9d1383cd8d8e
- FIX5 package SHA-256: 293c3d221fc572b1f90beb74cda781488e9604b50337bbad9020c7bcf7467a91
- FIX5 common recipe: 9b36d8fd1e74f35d931ac20bc11e05a47ee272dc176cfb07b0137bbf91e1c69b

Local end-to-end reproduction:
- 2 screen ×12;
- selection persisted;
- only 1 refine ×128 confirmed in Session A;
- Session B resumed from clean working;
- screen was not recomputed;
- only second refine executed;
- second reopen had zero pending jobs.

This does NOT replace the real Kaggle Save Version -> Input -> resume smoke.
