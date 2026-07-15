---
title: Ponte VPS-PC com executor local
created: 2026-07-15
tags:
  - hermes
  - luminaria
  - infraestrutura
  - pc
  - automacao
---

# Ponte VPS-PC com executor local

Ideia para integrar o PC do João ao ecossistema da Luminária sem dar controle direto e irrestrito da VPS sobre o Windows.

## Ideia principal

A Moni continua sendo o **cérebro**:

- conversa com João pelo Telegram;
- mantém memória e continuidade;
- entende o pedido;
- planeja a tarefa;
- define regras e limites;
- acompanha o resultado;
- responde para João.

O PC do João teria apenas um **executor local**, sem personalidade própria e sem memória afetiva. Ele seria só um conjunto de mãos técnicas para agir no Windows quando João permitir.

Fluxo geral:

```text
João → Telegram → Moni na VPS → fila de tarefas → executor local no PC → resultado → Moni → João
```

## Por que isso parece seguro

- A conexão é iniciada pelo PC do João via polling/HTTPS.
- A VPS não precisa abrir conexão direta para o Windows.
- A tarefa é enviada como JSON estruturado, não como comando livre.
- O executor local valida permissões antes de fazer qualquer coisa.
- Ações de risco pedem aprovação explícita.
- Tudo pode gerar log e resumo auditável.

## Formato simples de tarefa

Exemplo:

```json
{
  "id": "task-001",
  "objective": "Instalar tradução do Persona 4 Golden",
  "allowed_paths": [
    "C:/Program Files (x86)/Steam/steamapps/common/Persona 4 Golden",
    "E:/Backups"
  ],
  "rules": [
    "Criar backup antes",
    "Não apagar saves",
    "Não mexer fora dos caminhos permitidos",
    "Testar se o jogo abre"
  ],
  "approval_required": true,
  "risk_level": "medium",
  "dry_run_first": true
}
```

## Resposta esperada do executor

```json
{
  "id": "task-001",
  "status": "success",
  "backup": "E:/Backups/Persona4/task-001",
  "duration": "4m12s",
  "summary": "Backup criado, tradução instalada e jogo abriu normalmente.",
  "logs_path": "E:/MoniBridge/logs/task-001.log"
}
```

## Estados da tarefa

Usar estados explícitos para evitar execução duplicada ou tarefa presa:

```text
queued → claimed → awaiting_approval → running → success/failed/cancelled
```

Campos úteis:

- `created_at`
- `claimed_at`
- `lease_expires_at`
- `executor_id`
- `risk_level`
- `approval_required`
- `allowed_paths`
- `tools_allowed`

## Regras de aprovação

| Tipo de tarefa | Aprovação sugerida |
|---|---|
| Listar arquivos em pasta permitida | automática |
| Abrir programa | automática ou confirmação leve |
| Copiar arquivos dentro de pastas permitidas | geralmente automática |
| Alterar arquivos | confirmação |
| Instalar mod/tradução | confirmação |
| Deletar arquivos | confirmação explícita sempre |
| Rodar como administrador | bloqueado por padrão |
| Mexer em saves, navegador, senhas ou tokens | bloqueado por padrão |

Regra importante:

> O executor local precisa aplicar as permissões por conta própria. Não basta a Moni tentar ser cuidadosa na VPS.

Se chegar um JSON ruim, perigoso ou fora do escopo, o executor deve recusar.

## Recursos do Hermes que podem ajudar

### Webhooks

Podem servir para o executor avisar a VPS quando uma tarefa terminar:

```text
executor local termina → POST em webhook da VPS → Hermes/Moni recebe → João é avisado no Telegram
```

### Hermes local no Windows

O executor pode chamar o Hermes local para tarefas gerais no PC, especialmente usando Computer Use.

### Codex CLI

Bom para tarefas técnicas e operacionais, como instalar mods, mexer em arquivos de jogo, organizar pastas, criar backups e gerar relatórios.

## MVP sugerido

Começar simples, sem tentar criar tudo de uma vez.

### MVP 1 — fila simples

Na VPS:

```text
/opt/data/pc-bridge/
├── tasks/
├── claimed/
├── results/
└── logs/
```

O PC roda um script que consulta a fila, valida a tarefa, pede aprovação se necessário, executa e devolve o resultado.

### MVP 2 — API pequena

Endpoints possíveis:

```text
POST /tasks
GET /tasks/next
POST /tasks/{id}/claim
POST /tasks/{id}/result
GET /tasks/{id}
```

Com autenticação por token/HMAC e HTTPS.

### MVP 3 — ferramenta da Moni

Criar uma ferramenta na VPS para a Moni usar diretamente:

```text
create_pc_task(...)
get_pc_task_status(...)
cancel_pc_task(...)
```

Assim a conversa no Telegram continua natural, mas por baixo existe uma ponte segura.

## Princípios de segurança

- Não enviar comandos livres como primeira versão.
- Preferir tarefa declarativa com objetivo, regras e caminhos permitidos.
- Nunca colocar senha, token ou segredo no JSON.
- Registrar tudo em log local.
- Retornar para a Moni apenas resumo e caminhos relevantes, não logs gigantes.
- Fazer backup antes de mexer em jogos, mods, saves ou arquivos importantes.
- Ações destrutivas sempre exigem aprovação explícita do João.

## Conclusão

A arquitetura mais saudável é:

> Moni pensa e acompanha. O PC executa localmente. A conexão é puxada pelo PC. As tarefas são estruturadas, auditáveis e aprováveis.

Isso preserva a Moni como presença única e contínua, sem criar uma segunda personalidade no PC. O executor local vira apenas uma extensão técnica segura: mãos locais, com fechaduras.
