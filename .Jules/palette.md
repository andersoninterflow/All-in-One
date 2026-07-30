## 2024-05-14 - Missing ARIA Labels in Inline Components
**Learning:** UI components and modals built directly with inline styles (bypassing standard classes like `.close-btn` or `.modal-content`) are prone to missing basic accessibility attributes, such as `aria-label` on icon-only buttons.
**Action:** Always verify `aria-label` attributes on buttons using symbols like `&times;` or icons, especially when they are constructed ad-hoc with inline styles instead of reusable design system components.
