## 2024-10-07 - Contextual ARIA labels on repeated action buttons
**Learning:** In lists with repeated action buttons (like order histories), screen readers announce "Abrir suporte" or "Avaliar" multiple times without context, causing ambiguity.
**Action:** Always append the item's title/identifier to the `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) on repeated action buttons. Ensure dynamic labels match dynamic visual states.
