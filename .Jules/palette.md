## 2024-05-24 - Contextual ARIA labels for list items
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack context for screen readers when read out of context.
**Action:** Always append the item's title/identifier to the aria-label (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context for screen readers.
