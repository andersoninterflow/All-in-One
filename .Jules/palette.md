## 2026-06-03 - Contextual ARIA labels for list items
**Learning:** In lists like order histories, repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels are confusing for screen reader users as they all sound the same.
**Action:** Always append the item's title/identifier to the aria-label of repeated action buttons using template literals.
