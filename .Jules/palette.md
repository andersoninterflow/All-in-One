## 2024-05-18 - Contextual ARIA labels for repeated action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without specific ARIA labels lack context for screen readers. Screen readers would just announce "Abrir suporte, button" repeatedly.
**Action:** Appended the item's title/identifier to the button's `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para \${item.title}\`}`) to provide unique, descriptive context.
