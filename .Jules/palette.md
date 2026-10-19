## 2024-10-19 - Contextual ARIA labels in lists
**Learning:** Repeated action buttons in lists without contextual ARIA labels are confusing for screen readers. Dynamic UI states must also be reflected in the aria-label to prevent contradicting the visual label.
**Action:** Use template literals to append the item's title/identifier to the aria-label of repeated action buttons in lists, matching any conditional visual text states exactly.
