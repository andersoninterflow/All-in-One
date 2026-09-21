## 2024-09-21 - Adicionar labels contextuais ARIA aos botões em listas
**Learning:** Em listas de itens (como o histórico de pedidos), botões de ação repetidos (ex: 'Abrir suporte', 'Avaliar') podem causar confusão para usuários de leitores de tela se não tiverem contexto único.
**Action:** Sempre anexar o título ou identificador do item ao `aria-label` usando template literals (ex: `aria-label={\`Abrir suporte para \${item.title}\`}`) em botões dentro de listas dinâmicas.
