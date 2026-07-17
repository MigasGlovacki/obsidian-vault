---
doc_id: "agent-guide"
game_version: "Pokemon FireRed (USA) GBA v1.0"
tags:
  - "agent-contract"
  - "firered"
source_snapshot: "df4449a27cd78dd747ce269e47d3ab4a0149d8f4"
---

# Contrato para agentes de IA

## Ordem de autoridade

1. `data/*.json`: fatos extraídos do jogo.
2. `walkthrough/*.md`: ordem operacional e estados.
3. `reference/*.md`: visualizações para consulta.
4. Blocos **Recomendação**: estratégia opinativa, nunca regra do jogo.

## Resolução de consultas

- Identifique a versão. Este pacote responde por **Pokemon FireRed (USA) GBA v1.0**.
- Determine o estado: Badges, Key Items, capítulo, starter, Pokémon capturados e eventos únicos já resolvidos.
- Consulte o capítulo da visita atual. Áreas revisitadas podem ter pré-requisitos diferentes.
- Use IDs e `map_id` para cruzar encounters, itens, batalhas e lojas.
- Ao responder taxas, some apenas slots do mesmo `map_id`, método e espécie; o campo `species_total_rate_percent` já contém esse total.
- Nunca apresente `event_required`, `trade_required` ou `unavailable_normally` como obtenção normal.

## Estado mínimo recomendado

```json
{
  "chapter": 1,
  "location_map_id": "MAP_PALLET_TOWN",
  "starter": null,
  "badges": [],
  "key_items": [],
  "captured_species": [],
  "resolved_unique_encounters": [],
  "story_flags_summary": []
}
```

## Política de navegação

- Direções naturais orientam humanos.
- `map_id` e coordenadas `(x, y)` são a referência determinística.
- Coordenadas ausentes significam que o evento é global, móvel ou não está ligado a um object event único; não invente posição.

## Fato versus recomendação

- Fato: possui `source.repository`, `source.commit` e `source.path`.
- Recomendação: aparece explicitamente em bloco rotulado e pode variar conforme a equipe.
- Se duas fontes secundárias divergirem, prefira o dado técnico do commit fixado e registre a divergência.

## Acesso externo

- `trade_required`: troca com NPC ou outro jogo, conforme o registro.
- `event_required`: ticket/distribuição externa.
- `unavailable_normally`: conteúdo presente nos dados mas não liberado numa partida GBA comum.
- `version_specific`: válido apenas na variante declarada.
