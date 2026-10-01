## 2026-10-01 - Contextual ARIA labels for dynamic list items
**Learning:** In lists of items, repeated action buttons with dynamic states must have contextual ARIA labels appended with the item's title/identifier. Furthermore, when the button text changes based on a state (e.g. from "Review" to "Sent"), the aria-label must also dynamically match this state to prevent contradicting the visual label for screen readers.
**Action:** Always use template literals to build dynamic `aria-label`s on repeated buttons within lists, and ensure their conditional logic mirrors the visual text's state.
