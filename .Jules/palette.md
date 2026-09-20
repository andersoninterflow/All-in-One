## 2024-09-20 - Contextual ARIA labels for dynamic list items
**Learning:** Action buttons repeated across list items (like "Avaliar" ou "Abrir suporte") lack context for screen reader users, and dynamically changing labels (like "Avaliar" to "Avaliacao enviada") must have their ARIA labels matched to prevent contradicting the visual label.
**Action:** Append contextual item identifiers to the ARIA labels (e.g. `aria-label={\`Avaliar ${item.title}\`}`) and ensure any conditional text states also apply to the ARIA label.
