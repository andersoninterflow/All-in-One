## 2024-05-24 - Contextual ARIA labels on dynamic buttons
**Learning:** When appending contextual ARIA labels to buttons with dynamic text states, the aria-label must dynamically match the same conditional states to prevent contradicting the visual label for screen readers.
**Action:** Always map the ternary condition of the button's content exactly to its ARIA label when dynamic text is present.
