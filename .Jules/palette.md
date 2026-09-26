## 2024-09-26 - Contextual ARIA Labels for Dynamic States
**Learning:** Contextual ARIA labels for repeated action buttons are essential for screen reader users to distinguish between items, and they must dynamically match visual text states.
**Action:** When adding ARIA labels to buttons with dynamic labels based on state, ensure the aria-label correctly mirrors the dynamic state format (e.g. `aria-label={hasReviewed ? \`Avaliacao enviada para ${item.title}\` : \`Avaliar ${item.title}\`}`).
