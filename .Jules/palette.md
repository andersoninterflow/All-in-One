## 2024-05-24 - Contextual ARIA labels in lists
**Learning:** Repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') in lists of items (like order histories) lack unique, descriptive context for screen readers if they only have the button text.
**Action:** Append the item's title/identifier using template literals (e.g., aria-label={`Abrir suporte para ${item.title}`}) to provide contextual ARIA labels for these repeated buttons.
