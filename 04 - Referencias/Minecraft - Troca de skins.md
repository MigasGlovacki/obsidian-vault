# 🎭 Minecraft — Workflow de troca de roupas (Blockbench)

> [!info] Objetivo
> Transferir a roupa de qualquer skin do Minecraft para minha skin original, preservando rosto, cabelo, olhos e sobrancelhas, incluindo a compatibilidade com Fresh Animations.

**Ferramenta:** Blockbench
**Projeto base:** `Migas_MASTER.bbmodel`
**Formato de exportação:** PNG 64×64

---

## 🔄 Workflow

### 1. Preparar o projeto

- [ ] Abrir `Migas_MASTER.bbmodel`.
- [ ] Salvar uma cópia do projeto para não modificar o original.
- [ ] Conferir se a skin base está carregada.

### 2. Importar a roupa

- [ ] Baixar a skin doadora em PNG 64×64.
- [ ] No Blockbench, ir em `File → Import → Texture`.
- [ ] Importar a textura sem substituir a original.
- [ ] Conferir se ambas aparecem no painel **TEXTURES**.

### 3. Copiar a roupa

- [ ] Selecionar a textura doadora.
- [ ] Ativar **Rectangle Select**.
- [ ] Selecionar a região de `Y = 16` até `Y = 63` (64×48 pixels).
- [ ] Pressionar `Ctrl + C`.

**Importante:** os primeiros 16 pixels contêm a cabeça e a camada do cabelo. Não copiar essa região.

### 4. Substituir a roupa antiga

- [ ] Selecionar a textura original.
- [ ] Apagar a região do corpo (`Y = 16–63`), incluindo as camadas externas.
- [ ] Pressionar `Ctrl + V`.
- [ ] Alinhar os pixels exatamente à posição original.
- [ ] Confirmar a colagem.

> [!warning] Atenção
> Apagar a roupa antiga antes de colar evita que pixels e camadas externas antigas continuem aparecendo nas áreas transparentes da roupa nova.

### 5. Inspecionar em 3D

- [ ] Conferir frente, costas e laterais.
- [ ] Conferir mangas, punhos e sapatos.
- [ ] Verificar se as camadas externas estão corretas.
- [ ] Confirmar que não existem pixels faltando.
- [ ] Confirmar que cabeça e sobrancelhas continuam intactas.

### 6. Exportar

- [ ] Exportar a textura final como PNG 64×64.
- [ ] Nomear como `Migas_[Roupa].png`.
- [ ] Testar no Minecraft, especialmente com Fresh Animations.

---

## 📁 Organização

```text
CinematicCraft/
└── Skins/
    ├── Migas_MASTER.bbmodel
    ├── Original/
    │   └── Migas_Base.png
    ├── Roupas/
    │   ├── Migas_Casual.png
    │   ├── Migas_DDLC.png
    │   └── Migas_Pijama.png
    └── Doadoras/
        └── DDLC_MC.png
```

## ⚠️ Problemas comuns

| Problema                      | Solução                                             |
| ----------------------------- | --------------------------------------------------- |
| Roupas antigas aparecendo     | Limpar corpo e segunda camada antes de colar        |
| Olhos ou sobrancelhas bugados | Preservar integralmente Head e Hat Layer            |
| Manga desalinhada             | Conferir compatibilidade Classic/Steve e Slim/Alex  |
| Pixels fora do lugar          | Conferir alinhamento da seleção 64×48               |
| Skin transparente             | Verificar se a camada base foi copiada corretamente |

---

## ⚡ Resumo rápido

**Abrir MASTER → Importar doadora → Copiar Y16–63 → Limpar roupa antiga → Colar → Conferir 3D → Exportar PNG.**

> [!tip] Regra de ouro
> A cabeça é a identidade do personagem. O restante da skin é o figurino. Nunca sobrescrever o MASTER original.
