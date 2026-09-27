## 2025-02-12 - Contextual ARIA labels in lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') with the same visual text become ambiguous for screen reader users because they don't know which item the action applies to.
**Action:** Always append contextual information to ARIA labels on repeated action buttons within lists using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
