## 2024-05-24 - Contextual ARIA labels in lists
**Learning:** In lists of items (like order histories), repeated action buttons without contextual information are indistinguishable to screen readers.
**Action:** Always append the item's title/identifier to ARIA labels on repeated action buttons using template literals (e.g., `aria-label={`Abrir suporte para ${item.title}`}`) to provide unique, descriptive context.
