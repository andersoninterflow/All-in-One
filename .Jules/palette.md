## 2024-10-25 - Contextual ARIA labels for list action buttons
**Learning:** Screen reader users lose context when multiple items in a list have identical action buttons like 'Abrir suporte' or 'Avaliar'.
**Action:** Always use template literals to append the item's title/identifier to the aria-label of repeated action buttons, and ensure the aria-label matches any dynamic text states (e.g. disabled/sent states).
