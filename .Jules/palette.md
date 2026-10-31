## 2024-10-31 - Add contextual ARIA labels to repeated action buttons
**Learning:** Repeated buttons in lists (like "Avaliar" or "Abrir suporte") need contextual ARIA labels incorporating the item title, dynamically matching conditional visual text, so screen readers can distinguish them without contradicting visual labels.
**Action:** Appended contextual ARIA labels with template literals (e.g., `aria-label={\`Avaliar ${item.title}\`}`) in OrdersDrawer.
