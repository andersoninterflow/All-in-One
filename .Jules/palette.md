## 2024-05-24 - Contextual ARIA Labels for List Items
**Learning:** Repeated action buttons in lists (like "Abrir suporte" or "Avaliar" for orders) need contextual ARIA labels appended with the item's identifier. Without this, screen readers read out identical "Avaliar" labels consecutively without distinguishing which item the action applies to.
**Action:** Always use template literals to build dynamic ARIA labels (e.g., `aria-label={\`Avaliar ${item.title}\`}`) on repeated action buttons to ensure unique and descriptive context.
