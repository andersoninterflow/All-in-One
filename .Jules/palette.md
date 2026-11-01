## 2024-11-01 - Contextual ARIA labels in lists
**Learning:** Botões de ação repetidos em listas (como "Abrir suporte" e "Avaliar") ficam confusos para leitores de tela sem contexto.
**Action:** Adicionar `aria-label` contextuais que incluam o título do item usando template literals, e se o texto do botão for condicional (ex: Avaliar/Avaliado), o `aria-label` também deve ser dinâmico para corresponder ao estado do botão.
