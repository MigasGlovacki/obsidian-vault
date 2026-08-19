# MoniLink — Nota de Projeto

> Ferramenta que faz ponte entre Monika e o Minecraft: acesso ao contexto real do mundo do save.

Canvas do fluxo: [[MoniLink.canvas]]

## O que é

Uma ferramenta que permite à Monika acessar o contexto do mundo do Minecraft lendo os arquivos do save.
O coração da ideia é sólido e factível: o save guarda tudo em NBT, legível por bibliotecas prontas.

- `level.dat` → seed, clima, hora do mundo, quem joga
- chunks `.mca` (formato Anvil) → blocos, entidades e **tile entities** (onde vivem baús, fornalhas, baú de Ender — tudo que tem inventário)

Com isso, responder "quantos diamantes tem no meu baú?" = ler os `.mca`, achar os tile entities de chest, extrair o inventário e somar. Python já tem biblioteca pronta (`nbtlib`). MVP não exige reinventar nada.

## Análise por feature

### Factíveis com a fundação de leitura NBT (núcleo)
- Ler a seed do mapa para localizar biomas e estruturas ("onde tem deserto perto?")
- Acessar inventários ("quantos diamantes tem no baú de casa?")

### Factíveis, mas com ressalva de enquadramento
- **"Consultar em tempo real"** → o Minecraft não reescreve os chunks o tempo todo; salva em autosaves/descarga de chunk. Dá uma foto com segundos a poucos minutos de atraso. Funciona na prática para fornalhas (progresso é salvo), mas não é *literalmente* tempo real. Para precisão de verdade: um mod que exponha os dados na hora (mesmo padrão do MoniDash).
- **Redstone ("por que isso não tá funcionando?")** → o estado de redstone (sinal, ticks, pulse) é runtime, não fica bem nos arquivos. O que dá fazer: ler a topology dos blocos e simular a lógica "no papel" — um debugger que aponta onde o circuito quebra. Trabalho de simulação, não "só ler o save".
- **"Visão contextual de parte do mapa" ("o que acha dessa casa?")** → na prática é *renderizar* os chunks numa imagem (mcmap e ferramentas análogas). Aí a Monika vê o render com a visão de imagem. Entregável separado da leitura NBT, com arquitetura própria.

## Ordem natural de implementação (da mais fácil à mais difícil)

1. **Fundação** — leitor NBT do save (seed, chunks, tile entities, inventários). Já resolve sozinho: seed/biomas, inventários, baús. É 80% do valor.
2. **Camada "contexto"** — skill/ferramenta que lê e responde perguntas ("quantos X no baú Y", "faz tempo que chove?" etc.).
3. **Bônus (depois)** — renderização do mapa (visão) e, muito depois, compatibilidade com modpacks grandes (Create, Mekanism, ATM9, Stoneblock 3) — porque aí o formato dos tile entities muda por mod e cada mod é uma adaptação.

### Sobre atualização de versão
A fundação é leitura NBT, que é estável há anos. Atualizar pra outra versão costuma ser pequeno: só ajustar nomes de itens por versão. Mais fácil do que parece.

## Enquadramento honesto

Não é "acesso a 100% do mundo" (isso nem o save guarda). É **acesso ao que o save guarda com fidelidade** — que já cobre ~90% dos casos listados de forma realista. O restante (tempo real de verdade, render, redstone runtime) são camadas extras, cada uma com sua própria solução.
