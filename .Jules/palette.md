
## 2024-05-23 - Contextual ARIA labels in order histories
**Learning:** Repeated action buttons like "Abrir suporte" or "Avaliar" in list contexts lack unique identification for screen readers without contextual ARIA labels.
**Action:** Always append the item's title or identifier using template literals (e.g., `aria-label={\`Abrir suporte para \${item.title}\`}`) to ensure descriptive context.
