---
doc_id: "qa-firered-encounter-audit"
game_version: "Pokemon FireRed (USA) GBA v1.0"
tags:
  - "qa"
  - "encounters"
  - "firered"
source_snapshot: "df4449a27cd78dd747ce269e47d3ab4a0149d8f4"
---

# Auditoria FireRed-only dos encounters

Objetivo: garantir que o guia do MoniLocke use **somente encounters selvagens de Pokémon FireRed**, sem completar rotas com tabelas LeafGreen quando as fontes externas agrupam FR/LG.

## Política aplicada

- Fonte técnica primária: `pret/pokefirered@df4449a27cd78dd747ce269e47d3ab4a0149d8f4`.
- ROM de referência: `Pokemon FireRed (USA) GBA v1.0`, SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- O gerador importa apenas tabelas `*_FireRed` de `src/data/wild_encounters.json`.
- Tabelas `*_LeafGreen` são descartadas antes da geração de `data/encounters.json` e do Markdown.
- Fontes FRLG genéricas, como walkthroughs, ficam apenas para progressão/ordem de áreas; não são autoridade para wild encounters quando FR/LG divergem.

## Validação local

O arquivo canônico atual contém:

- `2176` linhas em `data/encounters.json`.
- `2176` linhas com `version: "FireRed"`.
- `0` linhas com `LeafGreen` em `encounter_table_id` ou no `id`.

Amostras FireRed verificadas localmente:

| Área | Método | Totais FireRed |
| --- | --- | --- |
| Route 2 | land | Rattata 45%, Pidgey 45%, Caterpie 5%, Weedle 5% |
| Viridian Forest | land | Caterpie 40%, Weedle 40%, Kakuna 10%, Metapod 5%, Pikachu 5% |
| Route 24 | land | Weedle 20%, Caterpie 20%, Pidgey 15%, Oddish 25%, Abra 15%, Kakuna 4%, Metapod 1% |
| Route 25 | land | Weedle 20%, Caterpie 20%, Pidgey 15%, Oddish 25%, Abra 15%, Kakuna 4%, Metapod 1% |

## Validação online por amostragem

Amostras comparadas contra PokeAPI usando `location-area` + `version_details=firered`:

| PokeAPI location-area | Área | Resultado |
| --- | --- | --- |
| `296` | Kanto Route 2 south towards Viridian City | compatível |
| `321` | Viridian Forest | compatível |
| `314` | Kanto Route 24 | compatível |
| `315` | Kanto Route 25 | compatível |

Nota importante para a run: **Caterpie e Weedle aparecem juntos em FireRed** nas primeiras áreas. A diferença suspeita não era “Weedle só de LeafGreen”; o ponto que precisa de cuidado é não inverter detalhes FireRed/LeafGreen como Metapod/Kakuna e espécies exclusivas posteriores. Para o MoniLocke, sempre consultar `data/encounters.json` filtrado por `version: "FireRed"`.

## Ferramenta de verificação

Use:

```bash
python tools/validate_firered_encounters.py --guide .
python tools/validate_firered_encounters.py --guide . --online
```

O modo `--online` consulta a PokeAPI e pode falhar se a rede estiver indisponível; a validação local não depende de internet.
