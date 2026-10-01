# COLAB OVERNIGHT — LOS 5 MONSTRUOS LIANQI I

Rama:

`experiment/stage1-integral-t0-colab-all-v0.1`

Runner:

`experimentos/balance_nuevo/stage1_integral_t0_optuna/colab_all_monsters.py`

## Qué ejecuta

En orden y sin tocar CANON:

1. Rata de Qi
2. Avispa de Jade
3. Serpiente de Qi
4. Mono Ladrón de Píldoras
5. Lobo Espiritual de Tres Colas

Para cada especie:

- búsqueda NSGA-II;
- frente Pareto;
- cobertura geométrica neutral del Pareto;
- revalidación con common random numbers;
- nueva cobertura neutral;
- high-precision de cobertura.

No elige un ganador.
No escribe READY.
No ejecuta T1-T4.
No usa Definitivas.
No usa BLOOD_1.

## Preset recomendado esta noche

`overnight`

Por especie:

- 1.500 trials;
- 100 peleas por cada uno de los 10 contextos primarios durante search;
- hasta 50 candidatos de cobertura Pareto;
- 1.000 peleas/contexto en revalidación;
- hasta 5 representantes;
- 5.000 peleas/contexto en high precision.

Aproximadamente, si todos los caps se llenan:

- search: 7.500.000 peleas total;
- revalidación: 2.500.000;
- high precision: 1.250.000;
- total máximo aproximado: **11.250.000 peleas**.

## Archivos livianos

No se guarda ninguna pelea individual.

Cada especie produce:

- `<especie>.sqlite3`: checkpoint para reanudar;
- `trials.jsonl.gz`: una fila comprimida por trial;
- `pareto_search.json.gz`;
- `pareto_search_coverage.json.gz`;
- `revalidate_all.json.gz`;
- `revalidate_pareto.json.gz`;
- `final_coverage_input.json.gz`;
- `high_precision_all.json.gz`;
- `high_precision_pareto.json.gz`;
- `summary.json`.

Al final se crea:

`RESULTADOS_PARA_ANALIZAR.zip`

Ese ZIP **excluye los SQLite**. Es el archivo que conviene compartir para
análisis. Los SQLite quedan al lado sólo para recuperación/reanudación.

## Colab — celdas

### 1. Montar Google Drive

```python
from google.colab import drive
drive.mount('/content/drive')
```

### 2. Clonar la rama experimental

```bash
!rm -rf /content/La-Grulla-Blanca
!git clone --depth 1 --branch experiment/stage1-integral-t0-colab-all-v0.1 \
  https://github.com/Shein25/La-Grulla-Blanca.git /content/La-Grulla-Blanca
%cd /content/La-Grulla-Blanca/experimentos/balance_nuevo/stage1_integral_t0_optuna
!pip -q install "optuna>=4,<5"
```

### 3. Lanzar toda la noche

```bash
!python colab_all_monsters.py \
  --preset overnight \
  --outdir "/content/drive/MyDrive/GRULLA_STAGE1_OVERNIGHT"
```

Se puede cerrar la pestaña del navegador sólo si la sesión de Colab continúa
activa; Drive conserva los checkpoints ya escritos.

### 4. Mañana

El archivo a recuperar es:

`/content/drive/MyDrive/GRULLA_STAGE1_OVERNIGHT/RESULTADOS_PARA_ANALIZAR.zip`

## Si Colab se corta

Volver a ejecutar exactamente el mismo comando. El runner abre los mismos
SQLite y completa sólo los trials faltantes.

## Más carga

Preset `deep`:

- 3.000 trials;
- 150 peleas/contexto search;
- hasta 75 Pareto;
- 2.000 peleas/contexto revalidación;
- 7 representantes;
- 10.000 peleas/contexto high precision.

Usar sólo si se acepta una corrida considerablemente más larga.

## No usar GPU por este motivo

El resolver actual es Python/CPU y no está vectorizado para CUDA. Una GPU de
Colab no acelera automáticamente este laboratorio. Es preferible priorizar
una sesión estable y almacenamiento en Drive.
