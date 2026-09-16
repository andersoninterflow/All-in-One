## 2024-09-16 - [UX Improvement Pattern]
**Learning:** Some close buttons on modals and wizards lack an aria-label which makes them inaccessible for screen readers.
**Action:** Always add aria-label='Fechar' to icon-only close buttons.

## 2024-09-16 - [Contextual ARIA Labels in Lists]
**Learning:** Action buttons repeated in a list (like 'Abrir suporte' or 'Avaliar' in an order history) lose context for screen readers if they lack descriptive ARIA labels identifying the specific item.
**Action:** Always append the item's title/identifier to the aria-label (e.g., aria-label={`Abrir suporte para ${item.title}`}) when using action buttons within a list of items.
