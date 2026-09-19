## 2024-03-20 - Contextual ARIA Labels for Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') must have contextual ARIA labels appended with the item's title/identifier. Otherwise, screen reader users just hear "Avaliar, button", "Avaliar, button" without knowing which order they are evaluating.
**Action:** Use template literals (e.g., `aria-label={\`Avaliar \${item.title}\`}`) to provide unique, descriptive context for screen readers when mapping over items to generate buttons.
