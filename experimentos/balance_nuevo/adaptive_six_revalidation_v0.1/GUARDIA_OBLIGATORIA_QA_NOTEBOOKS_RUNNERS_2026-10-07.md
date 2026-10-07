# Guardia obligatoria — QA previo a entrega de notebooks y runners

Fecha: 2026-10-07
Rama: `experiment/monster-adaptive-six-revalidation-v0.1`
Estado: HUMAN_DECISION / GUARDIA PERMANENTE DEL FRENTE

## Regla

NINGÚN notebook, runner o paquete de simulación debe entregarse al usuario sin ejecutar primero un chequeo de pre-entrega.

Esta guardia es obligatoria y debe asumirse implícitamente en todo trabajo posterior de este frente.

## Checklist mínimo obligatorio

Antes de entregar:

1. **Sintaxis**
   - compilar runner;
   - compilar todas las celdas Python del notebook.

2. **Entrypoint**
   - verificar que la función principal realmente puede invocarse;
   - verificar firmas y número de argumentos;
   - detectar llamadas incompatibles antes de entrega.

3. **Workers / capacidad**
   - comprobar la configuración de CPU conocida;
   - para el entorno actual de referencia: 2 CPU lógicas -> 2 workers salvo evidencia de inestabilidad;
   - mostrar workers efectivos al inicio.

4. **Progreso visible**
   - si se prometió barra, comprobar que sea visible desde la celda del notebook;
   - no basta con que `tqdm` exista dentro de un subprocess;
   - preferir ejecución in-kernel o salida streaming verificada;
   - mostrar porcentaje, completado/total, velocidad y ETA cuando corresponda.

5. **Checkpoints**
   - verificar creación del checkpoint;
   - verificar que una segunda ejecución detecte y reutilice el checkpoint;
   - no recalcular chunks completados.

6. **Smoke test**
   - ejecutar una campaña mínima/reducida que atraviese el flujo real;
   - confirmar al menos un chunk escrito y leído;
   - confirmar que el proceso llega a generar outputs de prueba.
   - si el entorno local impide un smoke test real (por ejemplo, falta de red), declararlo explícitamente y no afirmar que fue probado en ejecución.

7. **Fuente**
   - commit/HEAD fijado;
   - rama correcta;
   - no main;
   - source lock consistente.

8. **Outputs**
   - comprobar nombres esperados;
   - comprobar que REVIEW/ZIP se genera en el flujo de prueba cuando sea posible;
   - comprobar que el notebook apunta a los mismos nombres que el runner.

9. **Integridad**
   - SHA-256 del runner/notebook/paquete;
   - no modificar seeds, R, grids o balance en un hotfix de UX salvo que se declare explícitamente.

10. **Resumen de entrega**
    - indicar qué fue validado realmente;
    - indicar qué NO pudo validarse;
    - no usar expresiones como "barra verificada" o "runner probado" si sólo se hizo una inspección estática.

## Criterio de salida

Sólo entregar cuando el estado sea:

`PRE_DELIVERY_QA = PASS`

o, si existe una limitación externa inevitable:

`PRE_DELIVERY_QA = PASS_WITH_DECLARED_LIMITATION`

con la limitación explícita.

No main. No merge. No push salvo autorización explícita.
