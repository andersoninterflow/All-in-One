## 2024-05-18 - Contextual ARIA Labels in Lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without unique context are problematic for screen reader users because they all sound identical (e.g., "Button, Avaliar. Button, Avaliar.").
**Action:** Always append the item's title or identifier to the `aria-label` for repeated action buttons in a list (e.g., `aria-label={"Avaliar " + item.title}`).
