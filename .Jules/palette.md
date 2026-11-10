## 2024-11-10 - Contextual ARIA Labels in Lists
**Learning:** Repeated action buttons in item lists (like "Abrir suporte" or "Avaliar" in order histories) lack descriptive context for screen readers when they only contain generic visual text.
**Action:** Append contextual information from the item (e.g., item title) to the `aria-label` using template literals to differentiate actions for screen readers.
