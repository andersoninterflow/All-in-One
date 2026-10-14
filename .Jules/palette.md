## 2026-10-14 - Contextual ARIA labels for repeated list items
**Learning:** Repeated action buttons in lists (like "Abrir suporte" or "Avaliar" in order histories) lack context for screen reader users when read out of context.
**Action:** Always append contextual information (like the item title or ID) dynamically to the `aria-label` for these repeated buttons, matching conditional visual states when present.
