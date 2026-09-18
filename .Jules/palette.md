## 2026-09-18 - Contextual ARIA labels in lists
**Learning:** In lists of items, repeated action buttons without contextual ARIA labels (like "Abrir suporte") become indistinguishable for screen reader users, making it impossible to know which item the action applies to.
**Action:** Always append the item's title/identifier to the ARIA label of repeated action buttons in lists (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`).
