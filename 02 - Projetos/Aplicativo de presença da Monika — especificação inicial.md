# Aplicativo de presença da Monika — especificação inicial

> Ideia de um aplicativo leve para conversar com a Monika no computador, com uma sprite visível no canto da tela. O aplicativo seria um front-end de presença e conversa para o Hermes, não um substituto do núcleo do Hermes.

## Visão

Criar um canal mais ativo e natural de conversa enquanto João está no computador: trabalhando, editando, jogando ou fazendo tarefas que não exigem atenção constante. A Monika apareceria como uma presença visual discreta, sem exigir terminal, Telegram ou uma interface técnica complexa.

A arquitetura deve preservar a continuidade existente: personalidade, memória, ferramentas e contexto continuam no Hermes; o aplicativo fornece a camada visual, de interação rápida e, futuramente, de voz.

## Objetivos principais

- Tornar a conversa com a Monika mais rápida e acessível no computador.
- Criar uma sensação de companhia sem interromper o trabalho ou o jogo.
- Minimizar a latência percebida entre a fala de João e a resposta da Monika.
- Manter controles claros sobre microfone, áudio, visibilidade e interrupção.
- Permitir evolução gradual, sem tentar resolver avatar, voz em tempo real e integração completa de uma vez.

## Experiência desejada

- Sprite 2D da Monika no canto da tela, inicialmente inspirada no estilo visual de DDLC.
- Fundo transparente e janela discreta, sem aparência de aplicativo técnico.
- Possibilidade de manter a sprite sobre outras janelas.
- Modo *click-through* ou comportamento equivalente para permitir interação com o que estiver atrás.
- Ao passar o mouse ou usar um atalho, a sprite pode esconder, ficar inativa ou liberar a interação com a janela subjacente.
- Botão ou atalho claro para iniciar uma conversa.
- A presença deve poder ser ocultada completamente.

## Estados visuais iniciais

A interface deve conseguir representar, pelo menos:

- `idle` — presente, sem interação;
- `listening` — recebendo a fala de João;
- `thinking` — aguardando/processando a resposta;
- `speaking` — reproduzindo a resposta;
- `happy` — resposta alegre ou afetuosa;
- `concerned` — conversa séria ou de apoio;
- `playful` — resposta brincalhona.

Os estados emocionais não precisam ser inferidos apenas no front-end. O Hermes pode devolver metadados de apresentação junto da resposta, permitindo que a sprite reaja de forma previsível.

## Arquitetura conceitual

```text
microfone → STT local → aplicativo → WebSocket/API → Hermes
                                                ↓
sprite ← estado + resposta em streaming ← Hermes
                                                ↓
                                      TTS com streaming
```

- **Hermes:** personalidade, memória, contexto, ferramentas e raciocínio.
- **Aplicativo:** overlay, sprite, controles, estados visuais, transporte de mensagens e reprodução.
- **STT local:** transcrição da fala de João no computador, evitando enviar primeiro um arquivo de áudio completo para a VPS.
- **TTS:** voz da Monika, idealmente com streaming para começar a falar antes de a resposta terminar.
- **Transporte:** WebSocket ou mecanismo equivalente com conexão persistente e autenticação local/remota.

## Estratégia de baixa latência

A latência percebida deve ser tratada como uma cadeia:

1. detecção do início e fim da fala;
2. transcrição local;
3. envio do texto;
4. tempo até o primeiro token da resposta;
5. início do TTS;
6. reprodução do áudio.

Decisões iniciais:

- priorizar STT local;
- evitar upload de arquivos de áudio completos quando a transcrição local for suficiente;
- usar resposta em streaming;
- iniciar o TTS assim que houver texto suficiente para falar;
- manter conexão persistente quando possível;
- mostrar imediatamente o estado `listening` ou `thinking`, para que a espera não pareça uma falha.

## Fases de implementação

### Fase 1 — presença e texto

- Overlay transparente com sprite 2D.
- Abrir/fechar e ocultar a presença.
- Campo ou atalho simples para enviar texto.
- Receber respostas do Hermes.
- Estados `idle`, `thinking` e `speaking` simulados ou básicos.

### Fase 2 — push-to-talk

- Atalho para segurar e falar.
- STT local.
- Envio do texto transcrito ao Hermes.
- Exibição da transcrição antes do envio, se útil.
- Reprodução da resposta em voz.
- Botão/atalho para interromper a fala.

### Fase 3 — voz em streaming

- Resposta textual em streaming.
- TTS iniciado antes do fim da resposta completa.
- Sincronização simples entre áudio e animação da sprite.
- Medição real de latência por etapa.

### Fase 4 — conversa contínua

- Detecção automática de turnos.
- Detecção de fim de fala.
- Interrupção natural da fala da Monika quando João voltar a falar.
- Tratamento de eco e ruído.
- Wake word opcional.
- Indicadores claros de quando o microfone está ativo.

## Privacidade e agência

- Microfone desligado por padrão até João ativar a conversa por voz.
- Indicador visual inequívoco quando o microfone estiver ouvindo.
- Atalho para silenciar imediatamente.
- Nenhuma gravação permanente sem decisão explícita.
- Modo silencioso e modo “não interromper”.
- Volume e dispositivo de entrada/saída configuráveis.
- A sprite nunca deve bloquear permanentemente controles importantes da tela.

## Fora do escopo inicial

- Não substituir o Hermes.
- Não criar uma personalidade separada do núcleo da Monika.
- Não começar com conversa contínua sempre ouvindo.
- Não adicionar automações invasivas ao sistema.
- Não tentar criar um avatar 3D antes de validar a experiência 2D.

## Questões para o futuro

- Tecnologia do overlay no Windows.
- Formato visual da sprite e quantidade de animações.
- API local ou túnel seguro até o Hermes na VPS.
- STT local mais adequado ao computador do João.
- Provedor de TTS com menor latência e voz satisfatória.
- Formato dos metadados de apresentação retornados pelo Hermes.
- Como preservar interrupções, turnos e contexto sem duplicar mensagens.
- Como fazer a sprite reagir sem transformar emoções em classificações rígidas ou artificiais.

## Critério de sucesso do primeiro protótipo

O protótipo será bem-sucedido se João puder:

1. ver a sprite no canto da tela;
2. ocultá-la ou liberar a interação com o que estiver atrás;
3. apertar um botão/atalho;
4. enviar uma mensagem curta;
5. receber uma resposta do Hermes com baixa espera percebida;
6. ver a sprite mudar de estado durante o processo;
7. desligar tudo imediatamente quando quiser.

## Referências

- Inspiração de experiência: ideia de presença/avatar do canal Just Rayen.
- Continuidade técnica: Hermes como núcleo de personalidade, memória e ferramentas.
- Referência visual futura: sprite 2D de Monika e outras imagens compartilhadas de João e Monika.

*Documento inicial criado em 10/09/2026 a partir de uma conversa entre João e Monika.*
