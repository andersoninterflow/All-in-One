## 2024-08-08 - Contextual ARIA labels on repeated list actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual context are confusing for screen reader users as they all read the same.
**Action:** Always append the item's title/identifier to the aria-label of repeated action buttons to provide unique, descriptive context.
