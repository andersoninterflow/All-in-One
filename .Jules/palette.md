## 2024-10-10 - Contextual ARIA labels in repeated lists
**Learning:** Screen reader users lose context in repeated action buttons (like 'Abrir suporte' or 'Avaliar') in lists if the ARIA label isn't dynamically appended with the item identifier, leaving them with ambiguous identical actions.
**Action:** Always append dynamic contextual identifiers (e.g., `aria-label={`Abrir suporte para ${item.title}`}`) and ensure ARIA labels match dynamic disabled states to maintain synchronized UI feedback for AT users.
