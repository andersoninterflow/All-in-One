## 2026-09-13 - Contextual ARIA labels for repeated list items
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels create ambiguity for screen reader users, as they hear the same action multiple times without knowing which item it applies to.
**Action:** Always append the item's title/identifier using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to repeated action buttons in lists to provide unique, descriptive context.
