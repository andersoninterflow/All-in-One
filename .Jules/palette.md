## 2024-11-20 - Contextual Labels for Repeated Actions
**Learning:** Em listas de itens (como histórico de pedidos), botões de ação repetidos ("Abrir suporte", "Avaliar") ficam confusos para usuários de leitores de tela quando não possuem o contexto do item.
**Action:** Sempre usar template literals para anexar o título ou identificador do item ao `aria-label` de botões repetidos (ex: `aria-label={\`Abrir suporte para ${item.title}\`}`).
