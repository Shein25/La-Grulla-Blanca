# Laboratorio de experimentos

Esta carpeta contiene prototipos y bancos de pruebas **aislados de producción**.

Cada familia experimental debe vivir en su propia subcarpeta.

## Estructura actual

```text
experimentos/
├── utility-ai/
│   ├── motor-npc-vivo-v0.1/
│   └── motor-npc-vivo-v0.1.1/
└── goap/
    └── motor-npc-vivo-v0.2-goap/
```

## Regla de organización

Cuando se abra una familia nueva de experimentos, crear una carpeta propia, por ejemplo:

```text
experimentos/
├── utility-ai/
├── goap/
├── behavior-tree/
├── htn/
├── redes-neuronales/
└── reinforcement-learning/
```

No crear carpetas vacías por adelantado. Sólo se incorporan cuando exista una prueba real.

## Auditorías externas

Los informes de prueba deben identificar al agente auditor tanto en el nombre del archivo como en la cabecera.

Ejemplos:

```text
Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_CLAUDE.md
Informe_Test_Motor_NPC_Vivo_v0.2.2_GOAP_REV3_GEMINI.md
```

La cabecera debe incluir como mínimo:

- agente auditor;
- modelo/versión si se conoce;
- fecha;
- rama auditada;
- HEAD exacto;
- tipo de revisión.

## Aislamiento

Nada de `experimentos/` se considera producción por existir aquí.

Para integrar un resultado experimental al juego se requiere:

1. versión congelada;
2. tests;
3. auditoría independiente;
4. contrato de integración;
5. revisión antes de merge.
