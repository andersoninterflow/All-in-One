## 2024-05-24 - Contextual ARIA labels in order lists
**Learning:** In lists of items like order histories with repeated action buttons ("Abrir suporte", "Avaliar"), screen readers can easily get confused if buttons lack specific context, as all buttons will just announce as their visual text.
**Action:** Always append the item's title or identifier to the `aria-label` (e.g., `aria-label={"Avaliar " + item.title}`) for repeated action buttons to provide unique, descriptive context.
