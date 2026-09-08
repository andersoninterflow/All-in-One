## 2024-05-18 - Contextual ARIA Labels in Lists
**Learning:** In lists of items (like order histories), repeated action buttons (e.g., "Abrir suporte", "Avaliar") without unique context create accessibility issues because screen readers will announce the same generic action without indicating which item it applies to.
**Action:** Always append the item's title/identifier to the aria-label using template literals (e.g., `aria-label={`Abrir suporte para ${item.title}`}`) to provide unique, descriptive context.
