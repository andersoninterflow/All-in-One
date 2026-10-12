## 2024-10-12 - Contextual ARIA labels for repeated list items
**Learning:** In lists of items, repeated action buttons (e.g., 'Abrir suporte', 'Avaliar') lack unique context for screen readers if they only describe the action, reducing accessibility.
**Action:** Appended contextual ARIA labels with the item's title using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context for screen readers.
