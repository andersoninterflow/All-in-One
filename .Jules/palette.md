## 2024-09-30 - Contextual ARIA labels on repeated list actions
**Learning:** In list views (like order history), repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') without contextual ARIA labels sound identical to screen readers, losing the context of the item they refer to.
**Action:** Always append contextual ARIA labels using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context for screen readers. For buttons with dynamic states (like 'Review' / 'Sent'), make sure the ARIA label matches the dynamic state.
