## 2024-05-24 - Contextual ARIA labels for repeated list actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') need contextual ARIA labels (e.g. `aria-label={`Avaliar ${item.title}`}`) to provide unique, descriptive context for screen readers so users know exactly which item the action applies to.
**Action:** Always append the item's title/identifier to the ARIA label of repeated action buttons in lists.
