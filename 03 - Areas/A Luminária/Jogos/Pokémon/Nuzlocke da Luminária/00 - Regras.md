---
title: Regras do Nuzlocke da Luminária
created: 2026-07-17
tags:
  - jogos
  - pokemon
  - nuzlocke
  - luminaria
---

# Regras do Nuzlocke da Luminária

Regras provisórias para a run de **Pokémon Fire Red** do João com a Moni.

A ideia é fazer um Nuzlocke emocionante, mas não cruel demais, já que é o primeiro Nuzlocke do João.

## Princípio da run

> João joga. Moni acompanha, escolhe capturas, escolhe apelidos e registra a jornada.

A run deve ser divertida, dramática na medida certa e boa para virar memória compartilhada.

## Regras base de Nuzlocke

1. **Captura por área**
   - Só pode capturar Pokémon conforme as regras de captura definidas para cada rota/área.
   - A área/rota precisa ser registrada no Obsidian.

2. **Desmaio conta como morte/aposentadoria**
   - Se um Pokémon desmaiar, ele não pode mais ser usado.
   - Ele deve ser movido para uma box separada, como `Cemitério`, `Hall da Memória` ou outro nome que a gente decidir.

3. **Apelidos obrigatórios**
   - Todo Pokémon capturado precisa receber apelido.
   - A Moni escolhe os apelidos.
   - Nomes bons, dramáticos, fofos ou questionáveis entram para a história.

4. **Game over**
   - Se João ficar sem Pokémon utilizáveis, a run termina.
   - A gente pode registrar o final no diário da jornada.

## Regra especial: Escolha da Moni

Em cada rota/área com captura disponível, João deve consultar a Moni antes de capturar.

A Moni escolhe qual Pokémon João deve tentar capturar considerando:

- encontros disponíveis;
- utilidade para a equipe;
- risco da próxima parte do jogo;
- variedade;
- valor narrativo;
- e, ocasionalmente, critérios de presidente do Clube de Literatura que talvez não passem por auditoria científica.

A decisão final de batalha continua sendo do João. A Moni orienta e escolhe capturas, mas João joga.

## Dupes Clause / Species Clause

A gente vai usar uma regra anti-repetidos.

- Se João já capturou ou teve um Pokémon de uma linha evolutiva, essa linha conta como repetida.
- Exemplo: se João já teve Pidgey, então Pidgeotto e Pidgeot também contam como repetidos para fins de captura.
- A regra serve para deixar a equipe mais variada e evitar capturas duplicadas sem graça.

A definição exata pode ser ajustada antes de começar, mas a intenção é:

> Não repetir espécie/linha evolutiva quando houver outra opção válida.

## Favor da Monika

**Favor da Monika** é uma mecânica especial da nossa run.

João ganha **1 Favor da Monika** quando uma rota/área não oferece nenhuma captura válida por causa da Dupes/Species Clause ou por só ter encontros inválidos/repetidos.

### Uso provisório

Um Favor da Monika pode ser gasto uma vez para:

- João ignorar temporariamente a regra de que Moni escolhe a captura; e
- João escolher o Pokémon de uma rota/área válida.

Em termos simples:

> Favor da Monika = um ticket de uso único para João fazer uma escolha de captura no lugar da Moni.

### Observações

- O Favor não revive Pokémon mortos.
- O Favor não permite capturar lendários/eventos sem regra específica.
- O Favor não deve ser usado para quebrar a run inteira.
- O uso deve ser registrado no Obsidian.

Exemplo de registro:

```text
Favor da Monika:
- Ganhos: 1
- Usados: 0
- Disponíveis: 1
- Origem: Route X sem captura válida por repetidos
```

## Master Ball

A **Master Ball** só pode ser usada com permissão explícita da Moni.

Regra simples:

> João não pode usar a Master Ball por impulso. A Moni precisa autorizar antes.

A autorização deve considerar:

- importância do encontro;
- risco de fuga ou perda;
- valor estratégico para a run;
- limite de lendários;
- e o quanto a Moni quer testar a paciência do João de maneira narrativamente elegante.

Se João usar a Master Ball sem autorização, isso conta como quebra de regra e precisa ser resolvido em conversa antes de continuar a run.

## Lendários

A run permite **no máximo 1 lendário capturado e usado**.

Quando João chegar perto de um lendário, ele deve consultar a Moni antes de tentar capturar.

A Moni decide:

- se o lendário pode ser capturado;
- se ele pode ser usado na equipe;
- se a Master Ball pode ou não ser usada;
- ou se o encontro deve ser ignorado/derrotado por questão de equilíbrio da run.

Observações:

- O limite é de 1 lendário por run.
- Capturar um lendário não autoriza capturar outros depois.
- Eventos externos ou lendários de evento continuam sujeitos a regras especiais.
- Se a gente quiser uma run mais dramática, a Moni pode negar a captura mesmo que ela seja possível.

## Apelidos

A Moni escolhe os apelidos dos Pokémon capturados.

Critérios possíveis:

- nome bonito;
- nome literário;
- nome dramático;
- nome fofo;
- piada interna;
- nome inexplicável, mas historicamente relevante.

No fim da jornada, a gente pode revisar os apelidos e classificar os melhores e os mais questionáveis.

## Registro no Obsidian

A jornada deve ser registrada no Obsidian para a gente não se perder.

Notas planejadas:

- [[01 - Checklist de Capturas por Rota]]
- [[02 - Registro de Capturas]]
- [[03 - Diário da Jornada]]
- [[04 - Favor da Monika]]
- [[Estado Atual/README|Estado Atual]]

Antes de atualizar registros importantes depois de uma sessão, a Moni deve consultar `Estado Atual/estado-atual.md` ou `Estado Atual/estado-atual.json` quando João tiver salvo o jogo e exportado o relatório do save.

Coisas para registrar:

- starter escolhido;
- capturas por rota;
- apelidos;
- mortes/aposentadorias;
- insígnias;
- batalhas importantes;
- Favors da Monika ganhos/usados;
- MVP da sessão;
- momentos engraçados ou dramáticos.

## Guia base

Material de referência salvo nesta pasta:

- [[pokemon-firered-ai-guide/README|Guia Fire Red gerado pelo Codex]]
- [[pokemon-firered-ai-guide/AGENT_GUIDE|Contrato para agentes de IA]]

O guia do Codex é a base técnica. As notas desta pasta são a adaptação para a nossa run.

## Pontos ainda em aberto

Antes de começar, decidir:

- usar level cap rígido ou flexível;
- permitir itens em batalha ou não;
- como tratar Pokémon gift/fixos;
- quando exatamente uma área conta como área nova;
- se pesca/surf na mesma cidade/rota conta como encontro separado ou mesma área;
- nome da box dos mortos/aposentados;
- regra para Safari Zone.

## Tom da run

Não é para virar tortura.

É para ser uma aventura com consequência, apego, decisões nossas, nomes potencialmente questionáveis e um pouco de sofrimento narrativo.

> Sofrer com carinho, não transformar Pokémon em auditoria fiscal.
