## 2026-10-11 - Contextual ARIA labels for repeated list items
**Learning:** Screen reader users lose context in lists with repeated action buttons (e.g., "Avaliar"), making it hard to know which item the action applies to.
**Action:** Use template literals to add the item's specific identifier to the aria-label dynamically, keeping it synchronized with conditional button states.
