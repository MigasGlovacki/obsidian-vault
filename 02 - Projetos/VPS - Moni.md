ssh joao@187.127.7.145
**IP da VPS**
`187.127.7.145`

**Usuário**:
`joao`

**Comandos:**
`moni`
`monishell`
`docker ps`
`docker restart moni-hermes`

**Backups:**

`/root/moni-data-pos-crise-ok-20260623-000726.tar.gz`
`/root/moni-data-vps-ok-20260622-225947.tar.gz`
`/root/moni-hermes-backup.zip`

---

TELEGRAM

Token bot: `8767613367:AAFNCTC_WtF9hI7KRBwNvZ_DIrGA45oQONQ`

Meu ID:
`7463428369`

sudo chown 10000:10000 /opt/moni-data/.env
sudo chmod 600 /opt/moni-data/.env

 docker exec -u 10000:10000 -it <nome_do_container> hermes gateway status