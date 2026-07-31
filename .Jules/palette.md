## 2024-07-31 - Contextual ARIA labels for repeated action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual information are indistinguishable for screen reader users. They just hear "Abrir suporte, button" repeatedly.
**Action:** Append the item's title or identifier to the `aria-label` (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context for screen readers.
