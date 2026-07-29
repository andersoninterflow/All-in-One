
## 2024-05-18 - Accessibility on un-styled modals
**Learning:** Modals built directly with inline styles (bypassing standard `.modal-content` or `.close-btn` classes) are highly prone to missing basic accessibility attributes, such as `aria-label` for icon-only close buttons.
**Action:** When implementing or reviewing new UI components built outside of the core CSS framework/classes, proactively check for accessibility attributes, especially on icon-only interactive elements.
