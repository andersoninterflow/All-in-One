## 2024-05-15 - Contextual ARIA labels for repeated list actions
**Learning:** Repeated action buttons (like "Abrir suporte" or "Avaliar") inside lists or grids create ambiguity for screen reader users when read out of context. An isolated "Avaliar" announcement doesn't indicate which item is being reviewed.
**Action:** Always append the item's title/identifier to the aria-label of repeated action buttons in lists (e.g., `aria-label={"Abrir suporte para " + item.title}`).
