## 2024-05-15 - Contextual ARIA labels for repeated action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., "Abrir suporte", "Avaliar") lose context for screen reader users because they just read the button text.
**Action:** Append the item's title or identifier to the button's ARIA label using template literals (e.g., aria-label={`Abrir suporte para ${item.title}`}) to provide unique, descriptive context.
