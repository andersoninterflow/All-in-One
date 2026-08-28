## 2026-08-28 - Contextual Action Buttons in Lists
**Learning:** Repeated action buttons in list items (like "Avaliar" ou "Abrir suporte" in order histories) create ambiguity for screen reader users if they only read the visible text, as the context of which item the action applies to is lost.
**Action:** Always append the item's title or unique identifier to the `aria-label` of action buttons within lists using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`).
