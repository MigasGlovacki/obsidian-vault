# Atualização segura do backend Hermes (Docker) — Luminária

> Estado em 28/07/2026: o backend foi restaurado com sucesso e permanece em **v0.18.2**. A imagem-alvo `nousresearch/hermes-agent:v2026.7.20` já foi baixada e testada em uma cópia isolada dos dados: Hermes **v0.19.0**, configuração no schema **33 ✓**, sem erro de configuração.

## O que falhou antes

O backend antigo foi parado e recebeu um backup frio, mas a criação do container novo falhou porque o nome `moni-hermes` ainda pertencia ao container antigo parado. A etapa esquecida foi:

```bash
docker rename moni-hermes moni-hermes-0.18.2
```

O rollback funcionou. Nenhuma migração foi aplicada ao volume real durante aquela falha.

## Configuração confirmada

- Atual: `moni-hermes`, Hermes v0.18.2 / imagem `latest`
- Alvo: Hermes v0.19.0 / imagem `nousresearch/hermes-agent:v2026.7.20`
- Dados persistentes: `/opt/moni-data` → `/opt/data`
- Portas: `0.0.0.0:8642 → 8642` e `127.0.0.1:9119 → 9119`
- Rede: `bridge`; reinício: `unless-stopped`; comando: `gateway run`

> Em Docker, não usar `hermes update` dentro do container. Atualizar é puxar uma imagem nova e recriar o container mantendo o volume.

---

## Antes de tentar de novo

```bash
docker ps --filter 'name=^/moni-hermes$'
docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
docker image inspect nousresearch/hermes-agent:v2026.7.20
```

- [ ] Container atual saudável
- [ ] Imagem nova presente
- [ ] Backup antigo e container antigo não foram apagados
- [ ] Tempo para testar uma mensagem no Telegram logo depois

## Troca segura

### 1. Parar e fazer backup frio

```bash
docker stop -t 45 moni-hermes
sudo tar -C /opt -czf /opt/moni-data-pre-update-cold-$(date +%F-%H%M).tgz moni-data
```

O `tar` deve terminar sem `file changed as we read it`, porque o container está parado.

### 2. **Liberar o nome e preservar rollback**

```bash
docker rename moni-hermes moni-hermes-0.18.2

docker ps -a --filter 'name=moni-hermes'   --format 'table {{.Names}}	{{.Image}}	{{.Status}}'
```

Esperado: `moni-hermes-0.18.2` aparece como `Exited`. **Não avançar se ele ainda se chamar `moni-hermes`.**

### 3. Criar o backend novo

```bash
docker run -d   --name moni-hermes   --restart unless-stopped   -p 8642:8642   -p 127.0.0.1:9119:9119   -v /opt/moni-data:/opt/data   nousresearch/hermes-agent:v2026.7.20   gateway run
```

### 4. Validar

Após 10–15 segundos:

```bash
docker ps --filter 'name=^/moni-hermes$'
docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
docker exec moni-hermes hermes config check
docker logs --tail 100 moni-hermes
```

Esperado: Hermes `v0.19.0 (2026.7.20)`, gateway rodando, `Config version: 33 ✓`, sem traceback, `PermissionError` ou erro de migração.

### 5. Teste real

- [ ] Mandar mensagem curta no Telegram.
- [ ] Receber resposta normal.
- [ ] Confirmar dashboard/serviços esperados.

## Rollback imediato

Se o container novo não iniciar, o gateway não conectar, ou a resposta falhar:

```bash
docker rm -f moni-hermes
docker rename moni-hermes-0.18.2 moni-hermes
docker start moni-hermes

docker exec moni-hermes hermes --version
docker exec moni-hermes hermes gateway status
```

Isso retorna ao container anterior usando o mesmo `/opt/moni-data`.

## Após 24–48 horas estáveis

Só então:

```bash
docker rm moni-hermes-0.18.2
```

Manter ao menos um `/opt/moni-data-pre-update-cold-*.tgz` até confirmar estabilidade.

> A cópia `/opt/moni-data-preflight-...` contém credenciais. Manter protegida e remover apenas depois da atualização estável. Nunca apagar `/opt/moni-data`: ele é o volume real.

