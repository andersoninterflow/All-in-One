## 2024-11-09 - Contextual ARIA labels in repeating lists
**Learning:** When action buttons like 'Abrir suporte' or 'Avaliar' are repeated in a list of items (like an order history), screen readers need additional context to distinguish which item the action applies to.
**Action:** Use template literals to dynamically append the item's title to the `aria-label` attribute (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) and ensure dynamic visual states match the dynamic ARIA labels.
