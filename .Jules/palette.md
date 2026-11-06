## 2024-11-06 - Contextual ARIA labels for repetitive action buttons
**Learning:** In lists like order histories, repeated action buttons ("Abrir suporte", "Avaliar") lack unique context for screen readers. This makes it difficult for users to know which specific order the action applies to without reading the surrounding context.
**Action:** Append the item's title/identifier to the button's `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
