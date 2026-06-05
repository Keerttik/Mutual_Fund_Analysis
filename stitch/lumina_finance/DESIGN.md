---
name: Lumina Finance
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#3c4a43'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#6b7b72'
  outline-variant: '#bacac1'
  surface-tint: '#006c4f'
  primary: '#006c4f'
  on-primary: '#ffffff'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#2fe0aa'
  secondary: '#565e74'
  on-secondary: '#ffffff'
  secondary-container: '#dae2fd'
  on-secondary-container: '#5c647a'
  tertiary: '#505f76'
  on-tertiary: '#ffffff'
  tertiary-container: '#a8b9d2'
  on-tertiary-container: '#3a495f'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#dae2fd'
  secondary-fixed-dim: '#bec6e0'
  on-secondary-fixed: '#131b2e'
  on-secondary-fixed-variant: '#3f465c'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  currency-display:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-padding-x: 1.5rem
  container-padding-y: 1rem
  stack-gap-sm: 0.5rem
  stack-gap-md: 1rem
  stack-gap-lg: 2rem
  grid-gutter: 1.5rem
  section-margin: 3rem
---

## Brand & Style

This design system is built on the principles of **Precision Minimalism**. It is designed for high-stakes financial environments where clarity and trust are the primary currencies. The aesthetic prioritizes data density without clutter, using intentional whitespace to frame critical financial metrics.

The visual direction draws from **Corporate Modernism** with a focus on "High-Trust Tech." It utilizes a "light-first" approach for day-to-day management and a high-performance "pro-dark" mode for focused trading or analysis. The emotional response should be one of calm control, reliability, and professional sophistication. All elements follow a strict grid-based alignment to reinforce the feeling of a stable, engineered platform.

## Colors

The palette is anchored by **Emerald Green**, used strategically to signify growth, prosperity, and positive action.

- **Primary (#00D09C):** Reserved for the "Primary Action Path"—success states, growth percentages, and main CTA buttons.
- **Secondary (#0F172A):** A deep slate used for high-level headings and primary navigation icons to provide a grounded, professional contrast.
- **Neutral Surface:** In light mode, use `#FFFFFF` for main containers and `#F8FAFC` for background offsets. In dark mode, shift to a `#020617` (Deep Black/Slate) foundation.
- **Borders:** Use a subtle `#E2E8F0` slate border in light mode to define boundaries without adding visual weight.

## Typography

The design system utilizes **Inter** exclusively to maintain a systematic and utilitarian feel. 

- **Weight Strategy:** Use `Bold (700)` for currency values and section headers to establish immediate hierarchy. Use `Medium (500)` for labels and interactive text to ensure legibility at smaller sizes.
- **Numerical Data:** For tables and dashboards, ensure `tabular-nums` OpenType features are enabled to keep financial figures aligned vertically.
- **Scale:** High contrast between "Display" sizes for account balances and "Body" sizes for transactional details is essential for the "Groww-inspired" look.

## Layout & Spacing

This design system uses a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **The Padding Metric:** A core rule is the `px-6 py-4` (24px horizontal, 16px vertical) standard for card content and list items. This creates a horizontal "breathing room" that feels premium and spacious.
- **Hierarchy through Gap:** Use `2rem` (32px) to separate major functional blocks (e.g., Portfolio Summary vs. Watchlist). Use `1rem` (16px) for internal card spacing.
- **Responsive Reflow:** On mobile, all side-by-side card elements stack vertically. Margins compress from `24px` to `16px` to maximize screen real estate for data tables.

## Elevation & Depth

To maintain a minimalist profile, the design system avoids heavy drop shadows. Instead, it uses **Tonal Layering** and **Soft Ambient Shadows**.

- **Level 0 (Background):** Pure white or deep slate.
- **Level 1 (Cards/Containers):** A 1px border (`#E2E8F0`) with a very subtle shadow: `0px 1px 3px rgba(0,0,0,0.05)`.
- **Level 2 (Modals/Popovers):** Elevated with a more pronounced, diffused shadow: `0px 10px 25px rgba(0,0,0,0.1)`.
- **Interaction:** On hover, cards should not lift but rather deepen their border color or subtly shift the background hue to maintain a "flat but tactile" feel.

## Shapes

The shape language is defined by **Large Radii (rounded-2xl)**. This softness balances the "serious" nature of finance, making the application feel approachable and modern.

- **Main Containers:** All dashboard cards and primary containers must use `1rem` (16px) corner radius.
- **Interactive Elements:** Buttons and input fields follow the same 16px radius to ensure a cohesive "pill-adjacent" look without being fully circular.
- **Micro-elements:** Tags and small badges use a 4px or 8px radius to maintain distinctiveness from larger containers.

## Components

### Buttons
- **Primary:** Background `#00D09C`, Text `#FFFFFF`, Bold weight. High-contrast emerald glow on hover.
- **Secondary:** Transparent background, `1px` Slate border, Charcoal text.
- **Ghost:** No border, no background. Emerald text for "View All" or minor actions.

### Input Fields
- **Default State:** `px-4 py-3`, 1px slate border, Inter Medium 14px text.
- **Focus State:** 2px solid Emerald border with a subtle green outer glow.
- **Validation:** Error states use `#EB5757` for both text and border.

### Cards
- **Structure:** `rounded-2xl`, white background, 1px slate border.
- **Padding:** Strict adherence to `px-6 py-4`.
- **Content:** Header usually contains a `label-sm` (uppercase) and the footer contains the primary action or a "View Detail" link.

### Chips & Badges
- **Status Badges:** Use a light tint of the status color (e.g., 10% opacity green background) with a 100% opacity text color for high readability and a modern "shadcn" look.

### Data Tables
- **Styling:** No vertical borders. Only horizontal dividers (`1px solid #F1F5F9`).
- **Typography:** Labels use `label-md` in slate; values use `body-md` in charcoal. High-growth figures highlighted in Emerald.