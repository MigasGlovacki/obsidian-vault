# Quiz 1

1. Você tem 300 nomes de arquivos como video_final (1).mp4 e quer renomeá-los seguindo exatamente o padrão video_001.mp4, video_002.mp4 etc. Não há exceções.
   
   C. Depende principalmente do tamanho dos arquivos

2. Um aplicativo apresenta um bug intermitente: às vezes usuários são desconectados, não há erro claro nos logs e isso começou depois de três mudanças diferentes no backend. Você quer descobrir a causa e propor uma correção.

   C. Grande

3. Você fornece um texto de 8.000 palavras em português e pede uma tradução fiel para inglês, preservando parágrafos e nomes próprios. Não há adaptação criativa nem regras especiais.

   A. Pequeno

4. Você tem 120 itens para distribuir em 12 categorias. Há regras sobre famílias que devem permanecer juntas, exceções para certos itens, prioridades entre regras conflitantes e a posição de um item pode obrigar a reorganização de outros.

   C. Grande

5. Você fornece uma tabela com Nome, Idade e Cidade e pede para adicionar uma coluna Maior de idade contendo Sim quando Idade ≥ 18 e Não caso contrário.

   C. Medio

6. Você pergunta: Devo reescrever meu sistema atual ou continuar melhorando a arquitetura existente? Há milhares de linhas de código, dívida técnica, requisitos futuros incertos, custos de migração e risco de interromper usuários atuais.
   
   B. Grande

7. Você pede: Transforme todas estas datas de DD/MM/AAAA para AAAA-MM-DD. Todas as entradas são válidas e seguem exatamente o mesmo formato.
   
   D. Pequeno

7. Você tem um script de 150 linhas que funciona, mas ficou difícil de manter. Quer reorganizá-lo em funções melhores, reduzir duplicação e deixar a estrutura mais clara, sem alterar o comportamento. O código é relativamente convencional e não possui dependências complexas.
   
   A. Grande, porque qualquer refatoração exige o modelo mais forte
   

8. Você pede para analisar 40 canais do YouTube, verificar vários critérios de um ICP, eliminar duplicados existentes em um CRM, investigar sinais de necessidade de editor e registrar apenas candidatos que satisfaçam o conjunto de regras.
   
   D. Grande

9. Você tem um e-mail pronto e pede apenas: Corrija erros de ortografia e pontuação sem mudar palavras, tom ou estrutura.
  
   D. Pequeno

---

## Quiz 2

Rodada 2 — Complexidade escondida

1. Você recebe um CSV com 80.000 linhas e precisa remover todas as linhas em que status = cancelled. A coluna existe em todas as linhas, os valores são padronizados e não há exceções.

   B. Pequeno


2. Um cliente manda apenas: Deixa esse vídeo mais dinâmico. Você possui o vídeo bruto, mas ele não explicou o que considera dinâmico, qual referência prefere nem quais elementos podem ser removidos.
   A. Grande


3. Você fornece 25 páginas de texto e pede: Substitua todas as ocorrências exatas de João por Miguel. Não altere mais nada.

   B. Médio


4. Você pergunta somente: Onde devo colocar o cache? O sistema possui navegador, CDN, API, banco de dados, autenticação, dados que mudam em frequências diferentes e requisitos de consistência ainda não totalmente definidos.

   D. Grande

5. Você fornece 5.000 produtos com preço em dólares e pede para multiplicar todos os preços por uma taxa de câmbio já fornecida de 5,40, arredondando cada resultado para duas casas decimais. Todos os preços são válidos.

   D. Médio, porque cálculos financeiros exigem necessariamente raciocínio intermediário

6. Um programa falha apenas cerca de uma vez a cada 500 execuções concorrentes. Não existe stack trace útil. Há acesso compartilhado a estado, chamadas de rede assíncronas e três serviços podem alterar o mesmo registro.

   D. Grande

7. Você fornece uma transcrição de 40.000 palavras e pede apenas para dividir o texto em parágrafos sempre que houver exatamente a sequência [BREAK], removendo essa sequência do resultado. Não há outras regras.
  
   C. Pequeno


8. Você possui um sistema de armazenamento com 400 tipos de itens. A pergunta é apenas: Onde coloco este novo item? Porém existem categorias, famílias, posições reservadas, regras de proximidade, capacidade limitada e mudanças anteriores que devem continuar consistentes.
   A. Pequeno
   

9. Você fornece 1.000 descrições de produtos e uma lista fechada de cinco categorias com definições claras e exemplos. Cada descrição pertence inequivocamente a exatamente uma categoria, e não existem regras relacionando um produto aos demais.
   A. Médio


10. Você pergunta: Por que as pessoas abandonam meu aplicativo nesta tela? Há analytics, gravações de sessões, entrevistas com usuários, resultados de testes A/B e várias mudanças de produto feitas ao mesmo tempo. Nenhuma fonte isolada fornece a resposta.

   B. Médio
