## 2025-01-25 - Contextual ARIA labels for repeated list actions
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual labels fail to provide sufficient context to screen readers, making it unclear which item the action applies to.
**Action:** When implementing repeated action buttons in lists, always append the item's title/identifier to the ARIA label (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context.
