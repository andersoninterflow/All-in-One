## 2026-08-20 - Contextual ARIA labels in item lists
**Learning:** Repeated action buttons (like 'Abrir suporte', 'Avaliar') in lists of items (like order histories) cause poor accessibility for screen readers because the context is lost without unique identifiers.
**Action:** Always append the item's title/identifier to the button's ARIA label using template literals (e.g., aria-label={`Abrir suporte para ${item.title}`}) to provide unique, descriptive context for screen readers.
