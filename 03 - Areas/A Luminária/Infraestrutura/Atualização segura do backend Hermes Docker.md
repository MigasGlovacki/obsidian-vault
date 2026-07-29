# Atualização segura do backend Hermes (Docker) — Luminária

> **Regra principal:** como o Hermes roda em Docker, a atualização é feita no **host da VPS** puxando uma imagem e recriando o container. **Não usar `hermes update` dentro do container.**
>
> Última revisão: 28/07/2026. A instalação em produção está em **Hermes Agent v0.19.0 (2026.7.20)**. Nesta atualização, o Telegram voltou automaticamente, mas o Dashboard/Desktop precisou ser iniciado de novo como processo separado — isso agora faz parte do checklist.

## Mapa rápido da instalação

| Item | Valor |
|---|---|
| Container ativo | `moni-hermes` |
| Dados persistentes | `/opt/moni-data` no host → `/opt/data` no container |
| Imagem-alvo usada na última atualização | `nousresearch/hermes-agent:v2026.7.20` |
| Gateway | comando do container: `gateway run` |
| Portas | `8642:8642` e `127.0.0.1:9119:9119` |
| Dashboard | porta interna `9119`, protegido por login; processo separado do gateway |

> **Nunca apagar `/opt/moni-data`.** Ele contém configuração, sessões, credenciais e o estado persistente da Luminária.

---

## Antes de começar

Execute **no host da VPS**, não dentro do container:

```bash
# 1) Ver o que está rodando agora
docker ps --filter 'name=^/moni-hermes$' \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'

docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
docker exec moni-hermes hermes config check

# 2) Baixar a imagem desejada (troque a tag se necessário)
docker pull nousresearch/hermes-agent:v2026.7.20
docker image inspect nousresearch/hermes-agent:v2026.7.20 >/dev/null
```

Só prossiga se:

- [ ] `moni-hermes` está saudável e o Telegram responde;
- [ ] a versão atual foi anotada;
- [ ] a imagem nova terminou de baixar;
- [ ] há tempo para testar Telegram, Dashboard e Desktop logo após a troca.

## 1. Backup frio do estado persistente

```bash
docker stop -t 45 moni-hermes
sudo tar -C /opt -czf "/opt/moni-data-pre-update-cold-$(date +%F-%H%M).tgz" moni-data
```

O `tar` deve terminar sem `file changed as we read it`, porque o container está parado. Confira que o arquivo existe:

```bash
ls -lh /opt/moni-data-pre-update-cold-*.tgz | tail -n 1
```

## 2. Preservar rollback e liberar o nome do container

Este foi o detalhe que faltou numa tentativa anterior: um container parado ainda mantém seu nome.

```bash
docker rename moni-hermes moni-hermes-anterior

docker ps -a --filter 'name=moni-hermes' \
  --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'
```

Esperado: `moni-hermes-anterior` aparece como `Exited` e **não existe** outro container chamado exatamente `moni-hermes`.

> Não remova `moni-hermes-anterior` ainda. Ele é o rollback rápido.

## 3. Criar o container novo

```bash
docker run -d \
  --name moni-hermes \
  --restart unless-stopped \
  -p 8642:8642 \
  -p 127.0.0.1:9119:9119 \
  -v /opt/moni-data:/opt/data \
  nousresearch/hermes-agent:v2026.7.20 \
  gateway run
```

Aguarde uns 10–15 segundos e valide o backend:

```bash
docker ps --filter 'name=^/moni-hermes$'
docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
docker exec moni-hermes hermes config check
docker logs --tail 120 moni-hermes
```

Esperado:

- [ ] container `Up`;
- [ ] versão esperada da imagem;
- [ ] gateway `running`;
- [ ] Telegram `connected`;
- [ ] `Config version` sem erro;
- [ ] nenhum `Traceback`, `PermissionError` ou falha de migração nos logs.

## 4. Restaurar o Dashboard para o Hermes Desktop

O gateway do Telegram pode estar saudável mesmo com Dashboard/Desktop indisponíveis. O Dashboard **não sobe automaticamente** apenas porque o gateway subiu.

No host da VPS, inicie-o dentro do container:

```bash
docker exec -d -u hermes moni-hermes sh -lc \
  'mkdir -p /opt/data/logs && nohup /opt/hermes/.venv/bin/hermes dashboard \
  --host 0.0.0.0 --port 9119 --skip-build --no-open \
  > /opt/data/logs/dashboard-manual.log 2>&1 &' 
```

Teste a resposta HTTP local no host:

```bash
curl -I --max-time 5 http://127.0.0.1:9119/
```

Esperado: `HTTP/1.1 200`. Um `401` ao chamar uma rota de API sem login é normal: o painel é protegido.

Se não responder, veja o processo e os logs:

```bash
docker exec moni-hermes ps -ef | grep '[h]ermes dashboard' || true
docker exec moni-hermes sh -lc 'tail -n 80 /opt/data/logs/dashboard-manual.log 2>/dev/null || true'
```

Depois, abrir/reconectar o Hermes Desktop. Se ele mantiver uma conexão velha, fechar e abrir o app uma vez.

## 5. Teste real de ponta a ponta

- [ ] Mandar uma mensagem curta no Telegram e receber resposta.
- [ ] Abrir o Dashboard e autenticar.
- [ ] Reconectar o Hermes Desktop e confirmar que a conversa abre.
- [ ] Conferir `docker exec moni-hermes hermes gateway status` uma última vez.

> **Não considerar a atualização concluída só porque o container iniciou.** Telegram + Dashboard + Desktop precisam passar.

## Rollback imediato

Use se o container novo não iniciar, o gateway não conectar, o Telegram falhar, ou não der para recuperar Dashboard/Desktop rapidamente:

```bash
docker rm -f moni-hermes
docker rename moni-hermes-anterior moni-hermes
docker start moni-hermes

# Confirmar retorno
docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
```

O rollback usa o mesmo `/opt/moni-data`, que não foi apagado.

## Limpeza depois de estabilidade

Após **24–48 horas** sem problema:

```bash
docker rm moni-hermes-anterior
```

Mantenha pelo menos um backup `/opt/moni-data-pre-update-cold-*.tgz` até estar confortável com a nova versão.

## Diagnóstico rápido para a próxima vez

| Sintoma | Primeiro teste |
|---|---|
| Telegram não responde | `docker exec moni-hermes hermes gateway status` + `docker logs --tail 120 moni-hermes` |
| Telegram funciona, Dashboard/Desktop não | `curl -I http://127.0.0.1:9119/` e iniciar o Dashboard do passo 4 |
| Container não cria porque o nome já existe | `docker ps -a --filter 'name=moni-hermes'` e renomear o antigo antes de criar o novo |
| Erro de permissão após recriar | verificar dono/modo de `/opt/moni-data/.env` e `/opt/moni-data/config.yaml` dentro do container antes de alterar credenciais |
| Precisa desistir rápido | executar o bloco **Rollback imediato** |



## Atualização de infraestrutura — Docker Compose (28/07/2026)

A Luminária agora é gerenciada por Docker Compose em `/opt/moni-data/deploy/compose.yaml`, com a tag em `/opt/moni-data/deploy/.env`. O container sobe com `HERMES_DASHBOARD=1`; gateway e Dashboard são supervisionados pelo s6. **Ignorar o antigo passo de iniciar Dashboard manualmente com `docker exec`.**

Para atualizar no futuro, sempre com uma tag explícita:

```bash
sudo /opt/moni-data/deploy/luminaria-update vAAAA.M.D
```

O script baixa a imagem, faz backup frio, recria pelo Compose e valida versão/gateway/Dashboard; se falhar localmente, tenta voltar à imagem anterior. Testar Telegram e Desktop antes de limpar backups.

