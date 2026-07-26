## 2026-06-03 - Initial Setup\n**Learning:** Started analyzing the UI components.\n**Action:** Will look for a11y enhancements like adding ARIA labels to buttons without text.
## 2026-06-03 - Semantic HTML for Interactive Elements
**Learning:** Found several `div` elements being used as interactive toggle and tab buttons in the Rider app. This makes them inaccessible to screen readers and keyboard users as they lack proper roles, states, and focus indication.
**Action:** Replaced `div`s with `<button>`s, added `role="switch"`/`role="tab"`, `aria-checked`/`aria-selected`, and focus-visible styles in CSS. Always verify that interactive elements use semantic HTML or equivalent ARIA attributes.
