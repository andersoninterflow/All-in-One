## 2024-10-28 - Contextual ARIA labels for repeated list actions
**Learning:** When lists have repeated action buttons like "Avaliar" or "Abrir suporte", screen reader users lack context on which item the button acts upon, especially when the text changes dynamically.
**Action:** Always append contextual ARIA labels using template literals (e.g., `aria-label={\`Avaliar ${item.title}\`}`) and ensure they match dynamic text states (e.g. `{hasReviewed ? 'Avaliacao enviada' : 'Avaliar'}`).
