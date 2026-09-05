## 2024-05-18 - Contextual ARIA Labels for Repeated Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels create ambiguity for screen reader users, who hear identical labels multiple times without knowing which item they apply to.
**Action:** Always append the item's title/identifier to the `aria-label` of repeated action buttons in lists, using template literals (e.g., `aria-label={\`Abrir suporte para \${item.title}\`}`), to provide unique, descriptive context.
