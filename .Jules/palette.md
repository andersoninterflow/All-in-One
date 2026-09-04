## 2024-09-04 - ARIA labels in Repeated Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without unique contextual labels are confusing for screen reader users because they just hear "Abrir suporte" multiple times without knowing which item it refers to.
**Action:** Always append the item's title/identifier to the aria-label of action buttons within list items using template literals (e.g., `aria-label={\`Abrir suporte para \${item.title}\`}`).
