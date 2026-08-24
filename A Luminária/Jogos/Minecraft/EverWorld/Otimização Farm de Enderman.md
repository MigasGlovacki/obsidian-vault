# Farm de Enderman (End) — Otimização de produção

> **Objetivo:** subir a taxa de enderman/hora (e XP) pra manter ferramentas com Mending.
> **Schema analisado:** `Farm-enderman.litematic` (23×51×31, 460 blocos sólidos).
> **Coordenadas neste guia são RELATIVAS ao schema** (origem no canto X=0, Z=0), igual ao Litematica. Pra aplicar no mundo, alinhe o schema no lugar construído e marque o desenho.
> **Fonte dos dados:** decode real do binário do schema feito pela Moni (blocos + entidades).

---

## Diagnóstico (por que a taxa é o que é)

A farm é uma **torre em espiral**: a cada ~4 níveis de altura, um anel de 8 blocos sobe em caracol. O endermite "Alado" (nas entidades do schema, dentro de um minecart) isca os enderman, que sobem a rampa, caem no eixo central vazio (X≈8–16, Z≈9–20) e despencam de **~Y44 até ~Y4-5** direto nos hoppers da base, onde você mata de espada.

O dado que segura a produção: **só 40 blocos de superfície de spawn** (pisos de `stone_bricks` + `stone_brick_slab`) espalhados em anéis finos. Farm no End é matemática de cap de mobs — **quanto menor a superfície spawnável, menos enderman entram por tick**, não importa o tamanho do poço. Queda (~40 blocos) e coleta já estão ótimos. O gargalo é a superfície.

Princípio usado (validação evidência no schema):
- Queda de 40 blocos ≥ o necessário pra matar enderman → poço não é o problema.
- No End, spawn ignora luz → tochas são inofensivas (não mexer).
- 460 blocos = ~40 de spawn → eixo de produção é a área da rampa.

---

## O plano (3 alavancas)

1. **Alargar cada piso da rampa** — transformar os blocos de corrida de 1×1 em plataformas 2×2. Quase dobra a superfície de spawn em cada um dos ~10 andares (ganho multiplicativo).
2. **Teto de folha sobre cada perna alargada** — prende o spawn na plataforma, não no vazio ao redor; mantém o cap de mobs do End todo dedicado à farm.
3. **Funil-guia no eixo central** — garante que quem cair vá pro ponto de matança, sem pendurar em borda e quebrar o ciclo.

**Como confirmar se o resultado veio:** base de teste = contagem de enderman/hora AFK. Antes de mexer, marque um valor (ex.: 5 min AFK, quantas pérolas/XP). Depois do upgrade, compare o mesmo teste. Só vale se for o mesmo teste dos dois lados.

---

## Upgrade bloco a bloco (andar por andar)

A rampa repete **4 padrões de andar** em espiral. Pisos atuais (`B` = stone_bricks, `P` = stone_brick_slab). Para cada um, **adicione os blocos à direita** = plataforma 2×2 (ou 3×3 onde couber) usando stone_brick_slab (mesmo material), e **folha de jungle (persistent) 1 bloco acima** sobre a área nova.

### Padrão A — andares Y=15, 30 e 45 (6 pisos por andar)

| Piso atual | Expansão (adicionar) |
|---|---|
| `(4,17)` | `(5,17)`, `(3,17)`, `(4,18)`, `(4,16)` |
| `(8,18)` | `(9,18)`, `(7,18)`, `(8,19)`, `(8,17)` |
| `(11,18)` | `(12,18)`, `(10,18)`, `(11,19)`, `(11,17)` |
| `(20,20)` | `(21,20)`, `(19,20)`, `(20,21)`, `(20,19)` |
| `(22,20)` | `(21,20)`, `(22,21)`, `(22,19)` |
| `(4,22)` | `(5,22)`, `(3,22)`, `(4,23)`, `(4,21)` |

### Padrão B — andares Y=19, 34 e 49 (2 pisos por andar)

| Piso atual | Expansão (adicionar) |
|---|---|
| `(20,11)` | `(21,11)`, `(19,11)`, `(20,12)`, `(20,10)` |
| `(22,11)` | `(21,11)`, `(22,12)`, `(22,10)` |

### Padrão C — andares Y=23 e 38 (6 pisos por andar)

| Piso atual | Expansão (adicionar) |
|---|---|
| `(15,1)` | `(16,1)`, `(14,1)`, `(15,2)`, `(15,0)` |
| `(20,2)` | `(21,2)`, `(19,2)`, `(20,3)`, `(20,1)` |
| `(22,2)` | `(21,2)`, `(22,3)`, `(22,1)` |
| `(8,5)` | `(9,5)`, `(7,5)`, `(8,6)`, `(8,4)` |
| `(11,5)` | `(12,5)`, `(10,5)`, `(11,6)`, `(11,4)` |
| `(15,6)` | `(16,6)`, `(14,6)`, `(15,7)`, `(15,5)` |

### Padrão D — andares Y=26 e 41 (2 pisos por andar)

| Piso atual | Expansão (adicionar) |
|---|---|
| `(8,27)` | `(9,27)`, `(7,27)`, `(8,28)`, `(8,26)` |
| `(11,27)` | `(12,27)`, `(10,27)`, `(11,28)`, `(11,26)` |

> **Atenção ao aplicar:** as células de expansão já foram conferidas como vazias no schema — mas o mundo real pode ter blocos que o schema não capturou. Antes de pôr cada bloco, confirme que o lugar está livre no jogo.
> **Interação com a espiral:** cada piso alargado só recebe folha de teto **se** não roubar a passagem da rampa acima. Ao pôr folha, deixe 2 blocos de altura livre pro enderman passar.

---

## Ordem de execução sugerida

1. **Marque a baseline** (5 min AFK, conte XP/pérolas) — sem isso não dá pra medir melhora.
2. **Alargue um andar só** (ex.: Y=15) e teste 5 min. Confirma que a troca funciona antes de replicar.
3. Replique nos 9 andares restantes.
4. Coloque folha de teto sobre as pernas alargadas.
5. **Confira o eixo central**: se notar enderman pendurado em borda sem cair, adicione um funil-guia (slab/bloco na borda pra empurrar pro vão central).
6. Compare baseline × resultado final.

---

## Notas

- Material: `stone_brick_slab` (mesmo da farm — consistência visual e de física).
- Enderman precisa de 3 blocos de altura livre pra spawnar — as plataformas alargadas mantêm isso se a folha de teto ficar 1 acima + 1 respiro.
- Análise feita a partir do schema enviado (27/08/2026). Se você mover/alargar a farm e quiser rechecar, me manda o `.litematic` novo que eu comparo com este.

---
*Nota de otimização da [[Farms.md]] — farm de Enderman.*