## 2024-05-16 - Contextual ARIA Labels for List Actions
**Learning:** Repeated action buttons (like "Abrir suporte" or "Avaliar") in lists (like order histories) cause screen reader ambiguity if they lack unique context.
**Action:** Always append the specific list item identifier (e.g., `item.title`) to the `aria-label` using template literals to provide unique context for each button.
