## 2024-10-18 - Contextual ARIA labels on repeated action buttons
**Learning:** Repeated action buttons in list views (like "Abrir suporte" or "Avaliar" in an order history) lose context for screen reader users when isolated. Dynamic labels must exactly match the visual text states (e.g., "Avaliacao enviada" without accents if the original lacks them) to prevent contradictions.
**Action:** Always append the item's title to the ARIA label using template literals (e.g., `aria-label={\`Abrir suporte para ${item.title}\`}`) to provide unique, descriptive context.
