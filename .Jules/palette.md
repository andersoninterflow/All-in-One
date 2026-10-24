## 2024-10-24 - Contextual ARIA Labels for Repeated Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without context are confusing for screen reader users, who hear "Abrir suporte" repeatedly without knowing for which item.
**Action:** Append the item's title/identifier to the ARIA label using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
