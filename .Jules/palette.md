## 2024-05-18 - Contextual ARIA labels in repeated action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack context for screen readers when they only say the action name.
**Action:** Append contextual ARIA labels with the item's title/identifier using template literals (e.g., `aria-label={`Abrir suporte para ${item.title}`}`) to provide unique, descriptive context for screen readers.
