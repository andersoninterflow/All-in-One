## 2026-06-03 - Improved Custom Toggle Group Accessibility
**Learning:** Custom toggle buttons grouped in a `div` need a proper accessibility structure (`role="group"` and `aria-label`) on the container, and `aria-pressed` on the buttons to communicate the selected state properly to screen readers.
**Action:** When implementing custom visual toggles instead of native radio buttons or checkboxes, always apply `role="group"` to the parent container and `aria-pressed` to the toggle buttons.
