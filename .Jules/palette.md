## 2023-10-21 - Explore UI Opportunities
**Learning:** Found several missing ARIA labels on "X" close buttons and action buttons without enough context, missing tooltips. Let's look for one clear win that makes the UX better.
**Action:** Let's focus on adding contextual ARIA labels to repetitive buttons to improve screen reader experience, as described in the prompt's examples.
## 2023-10-21 - Contextual ARIA Labels for List Action Buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels provide a poor screen reader experience. Furthermore, when appending contextual ARIA labels to buttons with dynamic text states, the `aria-label` must dynamically match the same conditional states to prevent contradicting the visual label.
**Action:** Always append contextual information (like the item's title) using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to repeated action buttons in lists, ensuring dynamic visual states are also reflected.
