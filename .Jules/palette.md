## 2025-02-27 - Rótulos contextuais para ações repetidas em listas
**Learning:** Em listas com muitos itens, os leitores de tela não conseguem distinguir botões repetidos como "Abrir suporte" ou "Avaliar". Botões com o mesmo texto visível precisam de distinção no contexto.
**Action:** Utilizar `aria-label` com interpolação de strings (template literals), incluindo o título ou identificador único do item, ex: `aria-label={\`Abrir suporte para \${item.title}\`}` para garantir que o contexto não se perca.
