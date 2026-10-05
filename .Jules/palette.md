## 2024-10-05 - Contextual ARIA labels on repeated action buttons
**Learning:** In lists like order histories, repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack unique context for screen readers when they rely only on visible text.
**Action:** When mapping over lists, append contextual ARIA labels using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to ensure unique, descriptive context. Ensure dynamic states (e.g. `reviewedOrders.has(item.id)`) are also reflected in the aria-label.
