## 2024-10-08 - Contextual ARIA labels in dynamic lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., "Abrir suporte", "Avaliar") lack context for screen reader users unless the context is added to the button label.
**Action:** Always append contextual information, such as the item's title or identifier, using template literals (e.g., `aria-label={`Abrir suporte para ${item.title}`}`) for repeated action buttons in lists to provide unique, descriptive context.
