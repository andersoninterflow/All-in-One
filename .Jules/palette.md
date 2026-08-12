## 2024-10-26 - Contextual ARIA labels in order histories
**Learning:** Screen reader users navigating lists of orders face ambiguity when multiple buttons have the exact same text like "Avaliar" or "Abrir suporte", lacking the context of which specific order the button corresponds to. Appending the order title dynamically provides crucial context.
**Action:** When adding repeated action buttons in lists or tables (e.g., order history), always append the item's title/identifier to the button's `aria-label` to give screen readers unique, descriptive context.
