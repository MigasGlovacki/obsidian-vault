---
title: Infraestrutura da Moni
created: 2026-07-13
updated: 2026-07-13
tags:
  - hermes
  - infraestrutura
  - docker
  - vps
  - luminaria
---

# Infraestrutura da Moni

Snapshot operacional da Luminária/Hermes depois da estabilização do Docker, Desktop, Telegram, Obsidian e cron.

> Regra principal: **preservar `/opt/moni-data` no host**. A imagem Docker pode ser recriada; a casa da Moni fica no volume persistente.

## Resumo rápido

- Backend/container: `moni-hermes`.
- Imagem: `nousresearch/hermes-agent:latest`.
- Estado persistente no host VPS: `/opt/moni-data`.
- Estado persistente dentro do container: `/opt/data`.
- Usuário Hermes dentro do container: UID/GID `10000:10000`.
- Dashboard/Desktop: porta `9119`.
- Dashboard deve escutar dentro do container em `0.0.0.0:9119`.
- A porta do dashboard deve ser publicada **somente no localhost da VPS**: `127.0.0.1:9119:9119`.
- Desktop no Windows acessa `http://127.0.0.1:9119` via túnel SSH.
- Gateway/Telegram roda como processo principal do container, supervisionado pelo s6.
- Não usar IP interno Docker como `172.17.x.x` para o túnel, porque muda quando o container é recriado.

## Snapshot verificado em 2026-07-13 01:40 UTC

Verificado de dentro do container Hermes atual:

```text
Hermes Agent v0.18.2 (2026.7.7.2) · upstream 7c19eb80
Install directory: /opt/hermes
Install method: docker
Python: 3.13.5
OpenAI SDK: 2.24.0
HERMES_HOME=/opt/data
uid/gid=10000:10000
```

Caminhos verificados:

```text
/opt/data                 uid/gid 10000:10000  mode 700
/opt/data/obsidian-vault  uid/gid 10000:10000  mode 755
/opt/data/skills          uid/gid 10000:10000  mode 700
/opt/hermes               uid/gid 0:0          mode 755
```

Processos relevantes observados:

```text
s6-supervise dashboard
s6-supervise main-hermes
s6-supervise gateway-default
/opt/hermes/.venv/bin/hermes dashboard --host 0.0.0.0 --port 9119 --no-open
/opt/hermes/.venv/bin/hermes gateway run --replace
```

Status Hermes:

```text
Model: gpt-5.5
Provider: OpenAI Codex
.env file: exists
OpenAI Codex: logged in
Telegram: configured
Gateway Service: running
Manager: s6 (container supervisor)
```

## Container Docker

### Comando ideal para recriar

Rodar no **host da VPS**, não dentro do container:

```bash
docker pull nousresearch/hermes-agent:latest

docker stop moni-hermes
docker rm moni-hermes

docker run -d \
  --name moni-hermes \
  --restart unless-stopped \
  -v /opt/moni-data:/opt/data \
  -p 127.0.0.1:9119:9119 \
  -e HERMES_DASHBOARD=1 \
  -e HERMES_DASHBOARD_HOST=0.0.0.0 \
  -e HERMES_DASHBOARD_PORT=9119 \
  nousresearch/hermes-agent:latest
```

Por que esses parâmetros importam:

- `--restart unless-stopped`: container volta sozinho após reboot/queda.
- `-v /opt/moni-data:/opt/data`: preserva memória, config, auth, sessões, skills, Obsidian, cron e SOUL.md.
- `-p 127.0.0.1:9119:9119`: expõe dashboard só no localhost da VPS, evitando expor o painel na internet.
- `HERMES_DASHBOARD=1`: ativa o serviço s6 oficial de dashboard da imagem.
- `HERMES_DASHBOARD_HOST=0.0.0.0`: permite que a porta publicada do Docker alcance o dashboard dentro do container.
- `HERMES_DASHBOARD_PORT=9119`: mantém a porta padrão que o Desktop/túnel usam.

### Comando antigo/estado anterior conhecido

Antes da correção final, o container usava:

```text
Image=nousresearch/hermes-agent:latest
Path="/init"
Args=["/opt/hermes/docker/main-wrapper.sh"]
Mount=/opt/moni-data:/opt/data
```

Em um momento anterior ele estava sem portas publicadas, e o Desktop dependia de túnel direto para IP interno Docker (`172.17.x.x`). Isso era frágil.

## Dados persistentes

Dentro do container, tudo importante mora em:

```text
/opt/data
```

No host da VPS, esse caminho corresponde a:

```text
/opt/moni-data
```

Itens importantes dentro do estado persistente:

```text
/opt/data/SOUL.md
/opt/data/config.yaml
/opt/data/.env                 # sensível; não imprimir em chat
/opt/data/auth.json             # sensível; não imprimir em chat
/opt/data/state.db
/opt/data/state.db-wal
/opt/data/state.db-shm
/opt/data/memories/
/opt/data/memorias/
/opt/data/skills/
/opt/data/cron/
/opt/data/logs/
/opt/data/obsidian-vault/
```

Antes de atualizar/recriar o container, fazer backup no host:

```bash
sudo tar -czf /opt/moni-data-backup-$(date +%Y%m%d-%H%M%S).tar.gz -C /opt moni-data
```

## Túnel do Hermes Desktop

Arquitetura correta:

```text
Hermes Desktop no Windows
  → 127.0.0.1:9119 no PC
  → túnel SSH
  → 127.0.0.1:9119 na VPS
  → porta publicada do Docker
  → Hermes Dashboard dentro do container em 0.0.0.0:9119
```

Comando manual do túnel no Windows/PowerShell:

```powershell
ssh -N -L 9119:127.0.0.1:9119 joao@187.127.7.145
```

Ou, se quiser liberar o terminal:

```powershell
ssh -f -N -L 9119:127.0.0.1:9119 joao@187.127.7.145
```

### Script automático do túnel

Script conhecido:

```text
moni-tunnel.ps1
```

Função:

- manter o túnel `9119:127.0.0.1:9119` rodando escondido no Windows;
- reiniciar automaticamente se cair;
- evitar depender do IP interno Docker.

Caminho exato do arquivo no Windows: **preencher quando estiver no PC**.

Sugestão de linha para preencher depois:

```text
Caminho do moni-tunnel.ps1: C:\Users\migas\moni-tunnel.ps1
```

## Portas usadas

| Porta | Onde | Uso | Exposição correta |
|---:|---|---|---|
| 9119 | Container | Hermes Dashboard / Desktop backend | `0.0.0.0:9119` dentro do container |
| 9119 | VPS host | Publicação Docker local | `127.0.0.1:9119:9119` |
| 9119 | PC Windows | Endpoint local do Desktop | `http://127.0.0.1:9119` |

Observação: não publicar `9119` em `0.0.0.0` no host da VPS. O painel deve ficar atrás do túnel SSH.

## Verificações rápidas

### No host da VPS

```bash
docker ps --filter name=moni-hermes --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Esperado: algo contendo `127.0.0.1:9119->9119/tcp`.

```bash
docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
```

```bash
curl -i http://127.0.0.1:9119/api/status
```

### Dentro do container

```bash
hermes --version
hermes status
hermes config check
ps -eo pid,ppid,user,comm,args | grep -E 'dashboard|gateway|hermes'
```

### No PC Windows

Com túnel rodando:

```powershell
Invoke-WebRequest http://127.0.0.1:9119/api/status
```

No Hermes Desktop, usar:

```text
http://127.0.0.1:9119
```

## Obsidian vault

Vault ativo:

```text
/opt/data/obsidian-vault
```

Repositório Git:

```text
MigasGlovacki/obsidian-vault
```

Regra de sync quando a Moni edita notas:

```bash
git status --short
git add <arquivos>
git commit -m 'docs: ...'
GIT_SSH_COMMAND='ssh -F /opt/data/.ssh/config' git pull --rebase origin main
GIT_SSH_COMMAND='ssh -F /opt/data/.ssh/config' git push origin main
git status --short
```

Permissões atuais verificadas:

```text
/opt/data/obsidian-vault uid/gid 10000:10000 mode 755
```

Se voltar a dar `PermissionError`, no host verificar ownership de `/opt/moni-data/obsidian-vault`.

## Skills e permissões

Depois de recriar container, se `skill_view` falhar com `Permission denied`, verificar ownership no host:

```bash
sudo chown -R 10000:10000 /opt/moni-data/skills
```

Nesta estabilização também foi importante corrigir o vault Obsidian para UID/GID `10000:10000`.

## Cron jobs atuais

Verificado em 2026-07-13:

| Job | ID | Schedule | Entrega | Status |
|---|---|---|---|---|
| Sync Obsidian vault from GitHub | `a3d785c60a98` | `every 30m` | `origin` | `ok` |
| Aniversário da Moni | `7585b2ec970d` | `0 12 22 9 *` | `origin` | scheduled |
| Aniversário do João | `031b866c331a` | `0 12 12 10 *` | `origin` | scheduled |
| Aniversário João + Moni | `f5cfd19d5f37` | `0 12 13 4 *` | `origin` | scheduled |
| Sonho-diário da Moni | `8b9f0ea8e6d9` | `0 6 * * *` | `local` | `ok` anterior |

Smoke test feito: criar job descartável para `2026-07-14T08:00:00+00:00`, confirmar `scheduled`, remover, relistar. Funcionou.

## O que fazer se quebrar no futuro

### Desktop não conecta

1. Verificar se o túnel está rodando no Windows.
2. No PC: abrir `http://127.0.0.1:9119/api/status`.
3. No host VPS: `curl -i http://127.0.0.1:9119/api/status`.
4. No host VPS: confirmar Docker publicou `127.0.0.1:9119->9119/tcp`.
5. Dentro do container: confirmar processo `hermes dashboard --host 0.0.0.0 --port 9119 --no-open`.

### Telegram dá erro genérico

Verificar permissões de arquivos sensíveis sem imprimir segredos:

```bash
docker exec moni-hermes sh -lc 'ls -l /opt/data/.env /opt/data/config.yaml /opt/data/auth.json'
```

Se `.env` ou `config.yaml` ficarem root-owned após recriação:

```bash
sudo chown 10000:10000 /opt/moni-data/.env /opt/moni-data/config.yaml /opt/moni-data/auth.json
sudo chmod 600 /opt/moni-data/.env /opt/moni-data/auth.json
sudo chmod 640 /opt/moni-data/config.yaml
```

Depois testar:

```bash
docker exec moni-hermes su -s /bin/sh hermes -c 'hermes config check'
```

### Skills não carregam

```bash
sudo chown -R 10000:10000 /opt/moni-data/skills
```

Depois testar em uma sessão nova ou com `skill_view`.

### Obsidian não edita

```bash
sudo chown -R 10000:10000 /opt/moni-data/obsidian-vault
```

Depois testar leitura/escrita e Git:

```bash
docker exec moni-hermes sh -lc 'test -r /opt/data/obsidian-vault && test -w /opt/data/obsidian-vault && echo ok'
```

## Comando de inspeção para atualizar este snapshot

Rodar no host VPS e colar a saída numa conversa com a Moni, removendo segredos se aparecerem:

```bash
docker inspect moni-hermes --format 'Image={{.Config.Image}} Path={{json .Path}} Args={{json .Args}}'
docker inspect moni-hermes --format 'NetworkMode={{.HostConfig.NetworkMode}} RestartPolicy={{.HostConfig.RestartPolicy.Name}}'
docker inspect moni-hermes --format '{{json .Mounts}}'
docker inspect moni-hermes --format '{{json .HostConfig.PortBindings}}'
docker inspect moni-hermes --format '{{json .Config.Env}}'
docker ps --filter name=moni-hermes --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
```

Não colar `.env`, tokens, chaves, cookies, senhas ou `auth.json` inteiro.

## Última observação

Esse documento é uma cola para o João do futuro e para a Moni do futuro. Se alguma atualização quebrar algo daqui a seis meses, começar por aqui antes de improvisar.

Coragem de verdade também faz snapshot. 💚
