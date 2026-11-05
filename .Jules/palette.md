## 2024-11-05 - Contextual ARIA Labels in Lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels provide no context to screen reader users about which item the action applies to.
**Action:** Always append the item's title/identifier to the aria-label using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) when rendering repeated list actions.
