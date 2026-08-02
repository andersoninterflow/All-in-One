## 2024-08-02 - Contextual ARIA labels in action lists
**Learning:** In lists of items, such as order histories, repeated action buttons (like "Abrir suporte", "Avaliar") need contextual ARIA labels appended with the item's title/identifier to provide unique, descriptive context for screen readers. Otherwise, users hear repeated generic actions without knowing which item they apply to.
**Action:** When creating a list with repeated action buttons for items, always append the item's name or title to the aria-label of the buttons.
