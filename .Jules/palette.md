## 2024-07-27 - CalendarWidget UX Polish
**Learning:** Found custom toggle buttons lacking `aria-pressed` for screen readers and an async action button missing a loading state, which are common UX/a11y gaps when implementing custom widgets.
**Action:** Ensure toggle button arrays include `aria-pressed` and async actions always have visual loading states/disabled states while processing to prevent duplicate submissions and provide feedback.
