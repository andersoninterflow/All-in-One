## 2024-08-06 - Add Contextual ARIA Labels to Repeated Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels can be confusing for screen reader users, as the context is lost when navigating button by button.
**Action:** Appended the item's title/identifier to the `aria-label` attribute on action buttons within lists (e.g., `aria-label={"Abrir suporte para " + item.title}`) to provide unique, descriptive context.
