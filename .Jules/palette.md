## 2024-05-24 - Contextual ARIA labels for repeated actions
**Learning:** Repeated action buttons in lists like "Abrir suporte" and "Avaliar" are ambiguous to screen reader users without context.
**Action:** Always append the item's title/identifier to the aria-label of repeated action buttons using template literals.
