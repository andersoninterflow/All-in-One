## 2024-05-24 - Contextual ARIA labels for list items
**Learning:** When lists have identical action buttons (like "Abrir suporte" or "Avaliar") repeated for multiple items, screen reader users lose context on which item the button affects if the button only announces the generic text.
**Action:** Always append contextual information to the `aria-label` using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) on repeating list item buttons to ensure clarity and improve accessibility.
