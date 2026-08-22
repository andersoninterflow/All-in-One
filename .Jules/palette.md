## 2024-08-22 - Contextual ARIA Labels for List Action Buttons
**Learning:** In lists of items, repeated action buttons (like 'Abrir suporte' or 'Avaliar') without contextual ARIA labels create a poor experience for screen reader users, as they hear the same generic action without knowing which item it applies to.
**Action:** Always append the item's title or identifier to repeated action buttons using template literals for the `aria-label` (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`).
