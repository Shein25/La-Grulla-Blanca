# Auditoría — Mutant Suffix T0/T1 Focal V02

Fecha: 2026-10-06
Estado: **VALID RESULTS / TAXONOMY CANDIDATE — AWAITING HUMAN RATIFICATION**

Review SHA-256:
`f4bf7356973b074befd4d0dab6c5de6c67c7ba9bb1c7b6c146823404910ef036`

## Integridad

- ZIP íntegro.
- Manifest 10/10 hashes y bytes correctos.
- 500.000 spawns por especie = 2.500.000.
- 143.360 combates focales Acorazado/Voraz.
- 184.320 combates multi-sufijo con CRN pareado.
- Total combate V02: 327.680.
- R128.
- T0 y T1 congelado.
- 0 timeouts.
- 0 NaN/Inf.
- `issues=[]`.
- Sin ratificación automática.
- Sin piso mínimo de win-rate del jugador contra Mutantes.

## Semántica correcta

El T0 congelado no es un monstruo normal fijo. Es el piso natural.

Cada individuo repetible recibe sus propios `q_axis` independientes. El Mutante emerge cuando la conjunción de esos rasgos cae en la cola excepcional. Los sufijos deben describir esa conjunción; no son un RNG independiente.

## Incidencia Mutante observada

- Rata Qi: 0,7458%.
- Serpiente Qi: 0,7488%.
- Avispa Jade: 0,7382%.
- Mono Píldoras: ~0,758%.
- Lobo Espiritual: ~0,762%.

Se conserva la banda objetivo ~0,75% y la guardia <1%.

## Excepcional / Ascendido — hallazgo fuerte

Contar **ejes individuales** con `q_axis >= 0.95` produce una separación notablemente estable entre especies.

### Exactamente 2 ejes >=0.95 — candidato EXCEPCIONAL

| especie | % de Mutantes | incidencia sobre todos los spawns |
|---|---:|---:|
| Avispa | 29,07% | 0,2146% |
| Lobo | 25,70% | 0,1958% |
| Mono | 26,14% | 0,1982% |
| Rata | 27,33% | 0,2038% |
| Serpiente | 27,62% | 0,2068% |

La incidencia absoluta queda extraordinariamente estable (~0,20%) pese a que las especies tienen distinto número de ejes variables.

### 3 o más ejes >=0.95 — candidato ASCENDIDO

| especie | % de Mutantes | incidencia sobre todos los spawns |
|---|---:|---:|
| Avispa | 8,02% | 0,0592% |
| Lobo | 3,23% | 0,0246% |
| Mono | 5,17% | 0,0392% |
| Rata | 1,42% | 0,0106% |
| Serpiente | 8,39% | 0,0628% |

Es una cola claramente más rara. La diferencia entre especies es esperable porque no todas poseen la misma cantidad de ejes variables reales.

### Lectura

Esto es más robusto que definir Excepcional/Ascendido por `multi_margin` entre grupos de sufijos. El `multi_margin` generaba demasiados MULTI y dependía de la geometría de grupos de cada especie.

**Candidato de taxonomía, NO ratificado todavía:**

```text
Mutante especializado
  = cola Mutante sin convergencia extrema de múltiples ejes;
    su identidad se deriva del grupo dominante
    (Acorazado/Fugaz/Acechante/Indómito/Voraz).

Excepcional
  = exactamente 2 ejes variables con q >= 0.95.

Ascendido
  = 3 o más ejes variables con q >= 0.95.
```

No hay RNG adicional.

## Acorazado

V02 confirma activación limpia incluso cuando el cruce de 50% HP ocurre por DOT del jugador.

La absorción media usada crece de forma monotónica:

- Serpiente T0: A10 0,694 / A15 0,900 / A20 0,991.
- Lobo T0: A10 1,316 / A15 1,648 / A20 1,838.
- Mono T0: A10 0,427 / A15 0,501 / A20 0,539.

Hay rendimiento decreciente claro entre A15 y A20. A15 queda como candidato de centro eficiente; A20 sigue siendo candidato válido si se quiere una identidad más extrema.

## Voraz

El bug V01 de cruces causados por DOT quedó corregido.

La tasa de activación ahora es coherente:
- Avispa V1/V2/V3 T0: ~49,9% / 71,8% / 89,8%.
- Serpiente: ~75,5% / 86,6% / 90,5%.
- Mono: ~79,8% / 95,2% / 98,9%.
- Lobo: ~90,9% / 97,7% / 99,6%.

V3 tiene identidad muy visible y acelera las derrotas; V2 mantiene una presión fuerte sin activar casi universalmente en Avispa. No existe bloqueo por baja win-rate.

## Multi-sufijo / ALL_SUPPORTED

El V02 rehace esta fase con CRN pareado.

Resultado:
- 0 timeout / soft-lock;
- T0/T1 sobreviven a pares y ALL_SUPPORTED;
- las combinaciones pueden coexistir mecánicamente;
- no se detecta interacción explosiva de runtime.

Esto valida infraestructura, no obliga a que Excepcional/Ascendido acumulen automáticamente todas las habilidades.

## Pendiente humano

1. Ratificar o rechazar la separación:
   - Excepcional = exactamente 2 ejes q>=0.95;
   - Ascendido = >=3 ejes q>=0.95.
2. Elegir intensidad final de Acorazado (A15 vs A20).
3. Elegir intensidad final de Voraz (V2 vs V3).
4. Revisar junto con V01 las intensidades finales de Fugaz, Acechante e Indómito.
5. Decidir cómo asignan habilidades Excepcional/Ascendido:
   - heredar habilidades de los grupos implicados;
   - versión reducida;
   - o identidad propia posterior.

No tocar main. No merge. No activar runtime canónico todavía.
