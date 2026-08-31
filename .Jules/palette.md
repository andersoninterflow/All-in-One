## 2024-05-24 - Contextual ARIA labels in lists
**Learning:** Repeated action buttons (like 'Abrir suporte' or 'Avaliar') in lists of items (like order histories) lack descriptive context for screen readers if they only say the action name.
**Action:** Always append the item's title or identifier using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique context.
