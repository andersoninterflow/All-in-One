## 2024-05-15 - Contextual ARIA labels in repeating lists
**Learning:** In lists of items, repeated action buttons without contextual ARIA labels provide a poor experience for screen reader users as they hear repeating labels without context.
**Action:** Append the item's title or identifier to the `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to ensure each button is uniquely identifiable.
