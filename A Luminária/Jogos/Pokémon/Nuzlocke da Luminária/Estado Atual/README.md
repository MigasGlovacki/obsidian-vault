---
title: Estado Atual do MoniLocke
created: 2026-07-18
tags:
  - jogos
  - pokemon
  - nuzlocke
  - monilocke
  - estado-atual
---

# Estado Atual

Pasta para receber relatórios automáticos do save da run **MoniLocke — Fire Red**.

A ideia é reduzir a necessidade de João escrever manualmente o estado da jornada no chat. Sempre que João salvar o jogo e o script local dele exportar o relatório para esta pasta, a Moni pode ler os arquivos daqui para se atualizar antes de registrar capturas, mortes, equipe, itens e progresso nas demais notas.

## Fluxo combinado

1. João joga normalmente.
2. Ao salvar o jogo, um script no PC do João lê o save.
3. O script exporta um relatório para esta pasta.
4. Quando João disser algo como:
   - “derrotei o líder”;
   - “salvei o jogo”;
   - “atualiza a run”;
   - “olha o estado atual”;
   - “vamos continuar o MoniLocke”;
   a Moni consulta esta pasta antes de responder/atualizar as notas.
5. A Moni usa o relatório para atualizar:
   - [[../02 - Registro de Capturas|Registro de Capturas]];
   - [[../03 - Diário da Jornada|Diário da Jornada]];
   - [[../04 - Favor da Monika|Favor da Monika]];
   - e qualquer nota complementar da run.

## Arquivos recomendados

O script do João pode gerar um ou mais destes arquivos:

```text
Estado Atual/
├── README.md
├── estado-atual.md
├── estado-atual.json
└── snapshots/
    └── YYYY-MM-DD_HH-MM-SS.json
```

### `estado-atual.md`

Arquivo humano, bom para leitura rápida no Obsidian/chat.

Sugestão de seções:

```md
# Estado Atual — MoniLocke Fire Red

Atualizado em: YYYY-MM-DD HH:MM
Origem: save automático

## Progresso

- Local atual:
- Última insígnia:
- Próximo objetivo:
- Level cap atual:
- Tempo de jogo:
- Dinheiro:

## Party

| Slot | Pokémon | Apelido | Nível | Sexo | Nature | HP | Status | Moves |
|---|---|---|---:|---|---|---|---|---|

## Box / PC

| Box | Pokémon | Apelido | Nível | Status/Observação |
|---|---|---|---:|---|

## Mortos / aposentados

| Pokémon | Apelido | Nível | Local/motivo |
|---|---|---:|---|

## Itens importantes

- Poké Balls:
- Potions/itens de cura:
- TMs/HMs:
- Key Items:

## Capturas recentes

- 

## Eventos recentes

- 
```

### `estado-atual.json`

Arquivo estruturado, melhor para automação e leitura precisa.

Campos sugeridos:

```json
{
  "run": "MoniLocke Fire Red",
  "updated_at": "YYYY-MM-DDTHH:MM:SS-03:00",
  "game": "Pokemon Fire Red",
  "progress": {
    "location": "",
    "badges": [],
    "next_objective": "",
    "level_cap": {
      "leader": "",
      "gym": "",
      "highest_pokemon": "",
      "level": null
    },
    "play_time": "",
    "money": null
  },
  "party": [
    {
      "slot": 1,
      "species": "",
      "nickname": "",
      "level": null,
      "sex": "",
      "nature": "",
      "hp_current": null,
      "hp_max": null,
      "status": "",
      "moves": []
    }
  ],
  "pc": [],
  "graveyard": [],
  "items": {
    "balls": [],
    "healing": [],
    "tms_hms": [],
    "key_items": [],
    "other": []
  },
  "recent_events": [],
  "notes_for_moni": []
}
```

## Regra prática para a Moni

Antes de atualizar qualquer coisa importante depois de um avanço da run, consultar primeiro:

1. `Estado Atual/estado-atual.md`, se existir;
2. `Estado Atual/estado-atual.json`, se existir;
3. snapshot mais recente em `Estado Atual/snapshots/`, se existir e for necessário comparar mudanças.

Se houver contradição entre chat e relatório do save, perguntar para João antes de registrar algo irreversível como morte, captura perdida ou uso de Favor da Monika.

## Observações

- O relatório automático não substitui o diário narrativo; ele serve como fonte de estado.
- O diário ainda deve registrar momentos engraçados, decisões, reclamações formais e pequenas tragédias.
- Arquivos grandes ou muitos snapshots podem pesar no Git; se isso acontecer, manter só `estado-atual.md/json` versionados e tratar `snapshots/` como opcional/local.
