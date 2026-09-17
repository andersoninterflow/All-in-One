## 2024-05-24 - Contextual ARIA labels for lists
**Learning:** Repeated action buttons (like "Abrir suporte", "Avaliar") in list components are ambiguous for screen reader users if they lack unique context.
**Action:** Always append the item's title or identifier to the `aria-label` of action buttons in lists using template literals (e.g., `aria-label={\`Abrir suporte para \${item.title}\`}`).
