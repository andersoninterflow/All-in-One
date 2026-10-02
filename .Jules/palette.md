## 2026-10-02 - Contextual ARIA labels on action buttons
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels provide a confusing experience for screen reader users, as they hear multiple buttons with the same text without knowing which item they apply to.
**Action:** Add dynamic ARIA labels using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to repeated action buttons in lists, ensuring unique context for assistive technologies.
