## 2026-08-16 - Contextual ARIA labels for repeated list actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack context for screen reader users if they don't specify which item the action applies to.
**Action:** Always append the item's title or identifier to the `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
