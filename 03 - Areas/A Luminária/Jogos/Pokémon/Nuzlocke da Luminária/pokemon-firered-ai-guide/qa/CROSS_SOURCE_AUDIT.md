---
doc_id: "qa-cross-source-audit"
game_version: "Pokemon FireRed (USA) GBA v1.0"
tags:
  - "qa"
  - "cross-source"
source_snapshot: "df4449a27cd78dd747ce269e47d3ab4a0149d8f4"
---

# Auditoria cruzada por amostragem

Os dados técnicos abaixo foram extraídos do commit fixado. As fontes secundárias servem somente para detectar divergências de leitura ou progressão.

| Amostra | Resultado técnico | Segunda fonte | Resultado |
| --- | --- | --- | --- |
| Route 3 encounters | Spearow 35%, Pidgey 30%, Mankey 10%, Nidoran M 14%, Jigglypuff 10%, Nidoran F 1% | https://bulbapedia.bulbagarden.net/wiki/Kanto_Route_3 | Compatível com a tabela FRLG; nenhuma divergência aberta. |
| Brock | Geodude Lv.12; Onix Lv.14 | https://bulbapedia.bulbagarden.net/wiki/Brock_(game) | Compatível. |
| Viridian Mart | Poké Ball 200, Potion 300, Antidote 100, Parlyz Heal 200 | https://strategywiki.org/wiki/Pok%C3%A9mon_FireRed_and_LeafGreen/Viridian_City | Compatível. |
| Pokémon Mansion | Secret Key no B1F; quatro pisos; itens visíveis e ocultos separados | https://bulbapedia.bulbagarden.net/wiki/Pokemon_Mansion_(Kanto) | Compatível com a progressão e a separação por piso. |
| Itens falsos na Power Plant | Dois Electrode Lv.34 registrados como encontros fixos, não itens | https://bulbapedia.bulbagarden.net/wiki/Hidden_item | Compatível com a observação sobre item balls disfarçados. |

## Política de divergência

Se uma futura versão das fontes secundárias divergir, `data/*.json` continua obedecendo ao commit técnico fixado. A divergência deve ser adicionada a esta tabela antes de qualquer alteração factual.
