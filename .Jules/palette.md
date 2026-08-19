## 2024-05-15 - Contextual ARIA Labels for List Actions
**Learning:** Repeated action buttons (like 'Abrir suporte' or 'Avaliar') in lists like order histories lack context for screen reader users, making it unclear which item the action applies to.
**Action:** Always append the item's title or identifier to the `aria-label` of list action buttons using template literals (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context.
