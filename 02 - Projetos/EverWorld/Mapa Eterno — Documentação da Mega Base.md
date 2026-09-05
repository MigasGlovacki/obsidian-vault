# 🏛️ Mapa Eterno — Mega Base

> **Status:** Planejamento / construção em Criativo  
> **Objetivo:** Base principal permanente do Mapa Eterno  
> **Versão do projeto:** 1.0  
> **Filosofia:** organização, automação, expansão futura e facilidade de manutenção.

---

# 1. Visão Geral

A Mega Base será o centro principal de operações do **Mapa Eterno**.

A estrutura é subterrânea e organizada ao redor de um **Hub Central circular**, responsável por conectar todas as áreas da base.

A base possui quatro alas principais:

| Direção | Função |
|---|---|
| 🟢 **Oeste** | Construção & Natureza |
| 🔵 **Leste** | Recursos & Utilidades |
| 🟣 **Norte** | Museu / Trophy Room |
| 🟠 **Sul** | Logística & Infraestrutura |

A filosofia geral de navegação é:

> **Oeste:** quero construir alguma coisa.  
> **Leste:** preciso de algum recurso ou item.  
> **Norte:** quero guardar/exibir algo importante.  
> **Sul:** quero depositar, processar ou gerenciar itens.

---

# 2. Estrutura Geral

## Hub Central

O coração da base é um **Hub circular**.

Ele conecta diretamente:

- Ala Oeste
- Ala Leste
- Ala Norte
- Ala Sul

O acesso principal da base ocorre pelo **1º andar**.

As alas e o sistema principal de armazenamento ficam associados ao **2º andar**.

---

# 3. Sistema de Alturas

Para permitir que corredores sejam expandidos indefinidamente sem que as alas acabem colidindo entre si, diferentes eixos podem ocupar diferentes níveis verticais.

### Níveis planejados

| Ala | Nível relativo |
|---|---:|
| Norte | Y ±0 |
| Sul | Y ±0 |
| Oeste | **Y +10** |
| Leste | **Y +10** |

Portanto:

```text
                 NORTE
                  Y 0
                   │
                   │
OESTE Y+10 ────── HUB ────── LESTE Y+10
                   │
                   │
                  Y 0
                  SUL
```

As transições Oeste/Leste para **Y +10** acontecem após a saída do Hub.

### Objetivo

Essa separação permite que corredores sejam estendidos no futuro sem necessariamente entrarem em conflito físico com corredores de outras alas.

---

# 4. Layout dos Corredores

As alas utilizam um sistema baseado em **9 corredores**.

O número ímpar foi escolhido propositalmente para existir um **corredor central (nº 5)**.

Exemplo:

```text
1   2   3   4   [5]   6   7   8   9
                 ↑
               CENTRO
```

Isso cria:

- simetria;
- ponto central claro;
- melhor orientação;
- possibilidade de destacar arquitetonicamente o corredor nº 5.

---

# 5. 🟢 Ala Oeste — Construção & Natureza

**Função:** armazenar principalmente blocos utilizados para construção, terraformação e decoração.

Regra mental:

> **"Se estou procurando algo principalmente para construir, provavelmente está no Oeste."**

| # | Categoria | Exemplos |
|---|---|---|
| **O1** | Pedras naturais | Stone, cobblestone, deepslate, granite, diorite, andesite, tuff, calcite, dripstone |
| **O2** | Pedra trabalhada / Alvenaria | Stone bricks, deepslate bricks/tiles, bricks, mud bricks, quartz, prismarine, purpur |
| **O3** | Madeiras | Logs, wood, planks, stripped variants, bamboo blocks e derivados |
| **O4** | Natureza & Vegetação | Dirt, moss, leaves, flowers, vines, mushrooms, roots e plantas decorativas |
| **O5** | **Arquitetura / Variantes** | Stairs, slabs, walls, fences, fence gates, doors, trapdoors |
| **O6** | Blocos coloridos | Wool, concrete, concrete powder, terracotta, glazed terracotta |
| **O7** | Vidro & Decoração | Glass, panes, carpets, banners, pots, candles, chains e decoração |
| **O8** | Terreno & materiais naturais | Sand, red sand, sandstone, gravel, clay, mud, snow, ice |
| **O9** | Iluminação & blocos especiais | Lanterns, glowstone, sea lanterns, froglights, shroomlights e miscellaneous |

### Corredor central — O5

O corredor nº 5 é dedicado a **variantes arquitetônicas**, tornando itens extremamente utilizados em construção fáceis de localizar.

---

# 6. 🔵 Ala Leste — Recursos & Utilidades

**Função:** armazenar recursos, componentes e itens funcionais.

Regra mental:

> **"Se preciso de um recurso ou item para fazer alguma coisa, provavelmente está no Leste."**

| # | Categoria | Exemplos |
|---|---|---|
| **L1** | Minérios & recursos minerais | Raw ores, ingots, nuggets, coal, diamond, emerald, lapis, amethyst |
| **L2** | Mob Drops | Bones, string, rotten flesh, gunpowder, slime, blaze rods, ender pearls |
| **L3** | Agricultura & plantas úteis | Wheat, seeds, sugar cane, bamboo, cactus, crops |
| **L4** | Comida | Carnes, frutas, vegetais e comidas preparadas |
| **L5** | **Redstone & componentes técnicos** | Redstone, repeaters, comparators, pistons, observers, hoppers, droppers, crafters |
| **L6** | Poções & Magia | Brewing ingredients, potions, bottles e enchanting-related items |
| **L7** | Transporte & Exploração | Minecarts, rails, boats, saddles, leads, compasses, maps |
| **L8** | Ferramentas & Equipamentos | Tools, weapons, bows, crossbows, shields, fishing rods |
| **L9** | Utilidades diversas | Buckets e outros itens funcionais/miscellaneous |

### Corredor central — L5

O corredor nº 5 é dedicado à **Redstone**.

Além de ser uma categoria importante, é uma das categorias técnicas mais utilizadas durante projetos e manutenção da própria base.

---

# 7. 🟣 Ala Norte — Museu / Trophy Room

A Ala Norte não é apenas armazenamento.

Ela funciona como o **registro histórico físico do Mapa Eterno**.

O objetivo é que itens adquiridos durante anos de jogo contem a história do mundo.

## Categorias planejadas

| # | Categoria |
|---|---|
| **N1** | Arsenal — armaduras, armas e Armor Trims |
| **N2** | Cabeças e troféus de mobs/bosses |
| **N3** | Itens raros e colecionáveis |
| **N4** | Coleções completas — Music Discs, Pottery Sherds etc. |
| **N5** | **Relíquias do Mundo** |
| **N6** | Conquistas e marcos |
| **N7** | Mapas e registros |
| **N8** | Exposições temáticas |
| **N9** | Expansão / futuras coleções |

## N5 — Relíquias do Mundo

Uma das áreas mais importantes do museu.

Aqui ficam itens cujo valor não necessariamente vem da raridade, mas de sua **história**.

Exemplos:

- primeira picareta importante;
- primeira Elytra;
- equipamento usado em uma mega construção;
- ferramenta relacionada a alguma aventura memorável;
- item recuperado após uma morte particularmente absurda;
- equipamentos aposentados;
- itens associados a grandes projetos.

Quando necessário, **lecterns + books** podem registrar a história do objeto.

---

# 8. 🟠 Ala Sul — Logística & Infraestrutura

A Ala Sul funciona como o **backend operacional da Mega Base**.

Enquanto Oeste/Leste são principalmente áreas onde itens são encontrados, Sul concentra sistemas que **recebem, processam e administram itens**.

| # | Sistema |
|---|---|
| **S1** | Unsorted Storage |
| **S2** | Bulk Storage |
| **S3** | Shulker Management |
| **S4** | Input / Item Processing |
| **S5** | Smelting |
| **S6** | Crafting & Workshop |
| **S7** | Maintenance / Redstone Access |
| **S8** | Expansão / Sistema futuro |
| **S9** | Reserva |

---

## S1 — Unsorted Storage

Destino de itens que não possuem filtro ou destino reconhecido pelo sistema.

Fluxo:

```text
INPUT
  ↓
SISTEMA DE ROTEAMENTO
  ↓
ITEM NÃO RECONHECIDO
  ↓
UNSORTED STORAGE
```

Deve possuir capacidade considerável para impedir overflow.

---

## S2 — Bulk Storage

Armazenamento dedicado a recursos produzidos ou coletados em quantidades extremamente grandes.

Exemplos:

- Cobblestone
- Stone
- Iron
- Bamboo
- outros materiais produzidos em massa

Evita utilizar dezenas de módulos convencionais para itens com produção industrial.

---

## S3 — Shulker Management

Área dedicada ao gerenciamento de Shulker Boxes.

Possíveis funções:

- armazenamento de shulkers vazias;
- carregamento;
- descarregamento;
- distribuição;
- processamento automático.

---

## S4 — Input / Item Processing

Principal ponto de depósito de itens.

Objetivo:

> Chegar de uma viagem/projeto → depositar inventário → sistema assume o restante.

O sistema de armazenamento é responsável por transportar e rotear os itens posteriormente.

---

## S5 — Smelting

Área dedicada ao processamento em fornalhas.

Pode conter:

- Super Smelter;
- Blast Furnaces;
- Smokers;
- armazenamento de combustível;
- input/output automatizado.

---

## S6 — Crafting & Workshop

Oficina técnica da base.

Pode conter:

- Crafting Tables;
- Crafters;
- Stonecutters;
- Anvils;
- Grindstones;
- Smithing Tables;
- outros workstations.

---

## S7 — Maintenance / Redstone Access

Área dedicada ao acesso técnico aos sistemas escondidos da base.

Objetivo principal:

> **Nunca precisar destruir a decoração para consertar Redstone.**

Sempre que possível, sorters, transporte de itens e mecanismos devem possuir acesso através de corredores técnicos.

---

## S8 / S9 — Reserva

Espaço deliberadamente não comprometido.

Serve para:

- futuras atualizações;
- novos sistemas;
- novas mecânicas;
- necessidades ainda desconhecidas.

**Espaço vazio planejado é infraestrutura.**

---

# 9. Sistema Principal de Armazenamento

Cada item filtrado possui um módulo próprio.

## Capacidade por item

Cada módulo utiliza:

> **5 baús duplos por item**

Os baús ficam empilhados verticalmente.

Representação:

```text
      SISTEMA TÉCNICO
   ~~~~~~~~~~~~~~~~~~~~  ← Water Stream

        4 BLOCOS
       DE FOLGA
           ↕

      ┌───────────┐
      │  BAÚ 05   │
      ├───────────┤
      │  BAÚ 04   │
      ├───────────┤
      │  BAÚ 03   │
      ├───────────┤
      │  BAÚ 02   │
      ├───────────┤
      │  BAÚ 01   │
      └───────────┘
```

---

# 10. Water Streams

As Water Streams são responsáveis pelo transporte dos itens ao longo do sistema de armazenamento.

Foi definido um espaço técnico entre o armazenamento e a stream:

> **Topo do baú mais alto → 4 blocos de área técnica → Water Stream**

Os quatro blocos foram escolhidos para fornecer:

- espaço para mecanismos;
- separação entre armazenamento e teto;
- liberdade para decoração;
- acesso técnico;
- margem para alterações futuras.

### Regra de projeto

**Não reduzir essa distância apenas para economizar espaço.**

A Mega Base prioriza manutenção e expansão em vez de compactação extrema.

---

# 11. Camadas da Base

A arquitetura deve separar visualmente o sistema técnico da área utilizada pelo jogador.

Conceito:

```text
            ÁREA TÉCNICA

        Water Streams
        Redstone
        Sorters
        Transporte
        Manutenção

══════════════════════════════
       TETO / DECORAÇÃO
══════════════════════════════

          ÁREA VISÍVEL

        Corredores
        Iluminação
        Decoração
        Baús
        Sinalização
```

Princípio:

> **O jogador vê arquitetura.  
> O teto vê os crimes de engenharia.**

---

# 12. Sistema de Roteamento

O armazenamento não deve depender apenas de uma única linha gigante de sorters.

A arquitetura planejada utiliza um sistema hierárquico de roteamento.

Conceitualmente:

```text
                    INPUT
                      │
                      ▼
               ROUTER PRINCIPAL
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
         ALA         ALA         ALA
          │
          ▼
    ROUTER DA CATEGORIA
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
  ITEM   ITEM   ITEM
```

A ideia é semelhante a uma rede:

> Input → Roteamento → Ala → Categoria → Item → Armazenamento.

O transporte pode utilizar Water Streams, Hoppers e Hopper Minecarts dependendo da necessidade do trecho.

---

# 13. Filosofia de Expansão

A Mega Base pertence a um mundo planejado para existir por tempo indeterminado.

Portanto, decisões arquitetônicas devem priorizar:

1. **Expansibilidade**
2. **Manutenção**
3. **Organização**
4. **Legibilidade**
5. **Automação**
6. **Estética**
7. **Compactação**

Nunca assumir que a quantidade atual de conteúdo do Minecraft será definitiva.

Sempre que possível:

- permitir extensão dos corredores;
- reservar espaço técnico;
- manter corredores de manutenção;
- deixar áreas de reserva;
- evitar sistemas impossíveis de modificar posteriormente.

---

# 14. Regra Mental da Base

Caso seja necessário decidir onde colocar algo novo:

```text
É BLOCO / CONSTRUÇÃO?
        │
       SIM
        ▼
      OESTE


É RECURSO / ITEM FUNCIONAL?
        │
       SIM
        ▼
      LESTE


TEM VALOR HISTÓRICO / COLECIONÁVEL?
        │
       SIM
        ▼
      NORTE


É INFRAESTRUTURA / PROCESSAMENTO?
        │
       SIM
        ▼
       SUL
```

Se não encaixar claramente em nenhuma categoria:

> **Não forçar uma decisão. Utilizar espaço de reserva até uma categoria apropriada ser definida.**

---

# 15. Resumo

```text
                         🟣 NORTE
                    MUSEU / HISTÓRIA
                          Y ±0
                           │
                           │
                           │
                           │
 🟢 OESTE ──────────── HUB CENTRAL ──────────── 🔵 LESTE
 CONSTRUÇÃO                                      RECURSOS
   Y +10                                          Y +10
                           │
                           │
                           │
                           │
                          Y ±0
                       🟠 SUL
              LOGÍSTICA / INFRAESTRUTURA
```

## Identidade das alas

**OESTE**
→ O mundo enquanto material de construção.

**LESTE**
→ Os recursos necessários para jogar e criar.

**NORTE**
→ A história construída ao longo do mundo.

**SUL**
→ A infraestrutura que mantém todo o sistema funcionando.

---

> ### Princípio da Mega Base
>
> **Ela não deve ser projetada apenas para o Minecraft de hoje.**
>
> Deve ser capaz de crescer junto com o **Mapa Eterno**.