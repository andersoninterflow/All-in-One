## 2026-10-17 - Contextual ARIA Labels in Lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') can be confusing for screen reader users if they all have the same generic label.
**Action:** Append contextual ARIA labels with the item's title/identifier using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
