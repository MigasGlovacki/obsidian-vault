---
doc_id: "readme"
game_version: "Pokemon FireRed (USA) GBA v1.0"
tags:
  - "index"
  - "firered"
  - "ai-guide"
source_snapshot: "df4449a27cd78dd747ce269e47d3ab4a0149d8f4"
---

# Pokémon FireRed AI Guide

Base modular em PT-BR para Pokémon FireRed GBA USA v1.0. Nomes de Pokémon, moves, items, abilities e locations permanecem em inglês.

## Comece aqui

1. Um agente deve ler `AGENT_GUIDE.md`.
2. Para conduzir uma partida, abra o capítulo correto em `walkthrough/`.
3. Para perguntas pontuais, consulte `reference/`.
4. Para cálculos ou automação, trate `data/` como fonte canônica; Markdown é uma visualização gerada.

## Cobertura

- 21 capítulos: história, conteúdo opcional, Sevii Islands, pós-game, Cerulean Cave, League Round 2 e eventos.
- Encounters por método, nível, slot e taxa agregada.
- Item balls, hidden items, NPC gifts, lojas, Game Corner e vending machines.
- Batalhas regulares, chefes, variantes do rival e VS Seeker/rematches presentes nos scripts.
- Fixed encounters, gifts, in-game trades e Move Tutors.

## Autoridade e proveniência

- Fonte técnica fixada: `pret/pokefirered@df4449a27cd78dd747ce269e47d3ab4a0149d8f4`.
- SHA-1 da ROM de referência: `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`.
- Bulbapedia e StrategyWiki são usadas apenas para conferir progressão. A redação é original.
- FireRed v1.1 e Switch não são autoridades deste pacote.

## Arquivos

| Pasta | Uso |
| --- | --- |
| `walkthrough/` | sequência jogável com estados verificáveis |
| `reference/` | consulta humana/semântica por entidade |
| `data/` | registros JSON canônicos |
| `schemas/` | contratos dos registros |
| `tools/` | regeneração e validação |
| `qa/` | relatório de auditoria |

## Regeneração

```powershell
python tools/build_guide.py --source <checkout-pokefirered-no-commit-fixado> --output .
```

O gerador aborta se o checkout não estiver exatamente no commit fixado.

## Capítulos

- [01. Introdução e Pallet Town](walkthrough/01-introducao-pallet-town.md) — 26 entidades relacionadas
- [02. Route 1, Viridian City e retorno a Pallet Town](walkthrough/02-route-1-viridian-retorno.md) — 69 entidades relacionadas
- [03. Viridian Forest, Pewter City e Boulder Badge](walkthrough/03-viridian-forest-pewter.md) — 37 entidades relacionadas
- [04. Route 3, Mt. Moon e Route 4](walkthrough/04-route-3-mt-moon-route-4.md) — 139 entidades relacionadas
- [05. Cerulean, Cascade Badge, Routes 24–25 e Bill](walkthrough/05-cerulean-routes-24-25.md) — 143 entidades relacionadas
- [06. Route 6, Vermilion City, S.S. Anne e Thunder Badge](walkthrough/06-route-6-vermilion-ss-anne.md) — 127 entidades relacionadas
- [07. Route 11, Diglett's Cave, Route 2 leste e Route 9](walkthrough/07-route-11-diglett-route-9.md) — 151 entidades relacionadas
- [08. Rock Tunnel, Lavender Town e chegada a Celadon](walkthrough/08-rock-tunnel-lavender-celadon.md) — 157 entidades relacionadas
- [09. Celadon City, Rocket Hideout e Pokémon Tower](walkthrough/09-celadon-rocket-pokemon-tower.md) — 232 entidades relacionadas
- [10. Routes 12–18, Safari Zone, Fuchsia e Soul Badge](walkthrough/10-routes-12-18-fuchsia.md) — 411 entidades relacionadas
- [11. Saffron City, Silph Co., Fighting Dojo e Marsh Badge](walkthrough/11-saffron-silph-gym.md) — 90 entidades relacionadas
- [12. Routes 19–20 e Seafoam Islands](walkthrough/12-routes-19-20-seafoam.md) — 165 entidades relacionadas
- [13. Cinnabar Island, Pokémon Mansion e Volcano Badge](walkthrough/13-cinnabar-mansion-gym.md) — 120 entidades relacionadas
- [14. Sevii Islands I: One, Two e Three Island](walkthrough/14-sevii-parte-1.md) — 469 entidades relacionadas
- [15. Route 21, Power Plant e Earth Badge](walkthrough/15-route-21-power-plant-viridian.md) — 169 entidades relacionadas
- [16. Routes 22–23 e Victory Road](walkthrough/16-routes-22-23-victory-road.md) — 140 entidades relacionadas
- [17. Indigo Plateau e Pokémon League](walkthrough/17-indigo-plateau-liga.md) — 22 entidades relacionadas
- [18. Pós-game I: National Pokédex, Four Island e Six Island](walkthrough/18-pos-game-four-six-island.md) — 702 entidades relacionadas
- [19. Pós-game II: Five Island, Rocket Warehouse e Seven Island](walkthrough/19-pos-game-five-seven-island.md) — 567 entidades relacionadas
- [20. Cerulean Cave, Mewtwo, Legendary Beast e League Round 2](walkthrough/20-cerulean-cave-liga-round-2.md) — 133 entidades relacionadas
- [21. Conteúdo de evento: Birth Island e Navel Rock](walkthrough/21-eventos-birth-navel.md) — 4 entidades relacionadas
