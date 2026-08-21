
## 2026-08-21 - Contextual ARIA labels for repeated list actions
**Learning:** When lists of items (like order histories) have repeated action buttons (e.g., "Abrir suporte", "Avaliar"), screen readers lose context. Adding `aria-label` with the item's title using template literals provides unique, descriptive context.
**Action:** Always append the item identifier/title to repeated action buttons in list views (e.g. `aria-label={\`Abrir suporte para \${item.title}\`}`).
