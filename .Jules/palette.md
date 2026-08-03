## 2024-05-24 - Contextual ARIA labels for repeated action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') must have contextual ARIA labels appended with the item's title/identifier (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context for screen readers.
**Action:** When reviewing or adding list components with actions, always ensure `aria-label` includes the context of the list item.
