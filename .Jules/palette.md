## 2026-08-25 - Contextual ARIA labels for repeated actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual context create a poor experience for screen reader users, as all buttons sound the same.
**Action:** Always append the item's title/identifier using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to repeated action buttons to provide unique, descriptive context.
