## 2024-05-23 - Contextual ARIA labels for repeated list items
**Learning:** In lists like order histories, repeated buttons (e.g., "Abrir suporte", "Avaliar") without context cause accessibility issues for screen readers. Dynamic states in these buttons also need matching labels.
**Action:** Always append contextual information (like item titles) to ARIA labels using template literals for repeated list items, ensuring they match visual text states (e.g., `aria-label={\`${reviewedOrders.has(item.id) ? 'Avaliacao enviada' : 'Avaliar'} para ${item.title}\`}`).
