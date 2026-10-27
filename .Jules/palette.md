## 2024-10-27 - Contextual ARIA Labels for List Action Buttons
**Learning:** Screen reader users lose context when multiple items in a list have identical action buttons (e.g., "Avaliar"). Furthermore, ARIA labels must dynamically match conditional visual states (e.g., "Avaliacao enviada") to prevent contradiction.
**Action:** Append contextual item identifiers to ARIA labels using template literals for repeated buttons, and ensure any dynamic label changes are mapped exactly to their visual text.
