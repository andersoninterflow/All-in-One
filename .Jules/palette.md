## 2026-08-24 - Contextual ARIA labels for repeated list actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack unique context for screen readers when they only contain generic text.
**Action:** Always append the item's title/identifier to the button's ARIA label using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide descriptive context.
