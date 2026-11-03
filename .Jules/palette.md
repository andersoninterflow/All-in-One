## 2024-10-25 - Contextual ARIA labels for repeated list actions
**Learning:** Repeated action buttons in lists (like order histories) lack context for screen reader users when their visual labels are identical (e.g., "Abrir suporte" on every item).
**Action:** Always append the item's unique identifier/title to the `aria-label` using template literals to provide clear context without altering the visual design.
