## 2024-08-14 - Contextual ARIA labels for repeated list items
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without unique descriptions are confusing for screen reader users, as they all read the same.
**Action:** When mapping over lists to render items with actions, use template literals to append the item's title or identifier to the `aria-label` (e.g., ``aria-label={`Abrir suporte para ${item.title}`}``) to provide unique, descriptive context.
