---
name: Lumina Dark
colors:
  surface: '#0c1324'
  surface-dim: '#0c1324'
  surface-bright: '#33394c'
  surface-container-lowest: '#070d1f'
  surface-container-low: '#151b2d'
  surface-container: '#191f31'
  surface-container-high: '#23293c'
  surface-container-highest: '#2e3447'
  on-surface: '#dce1fb'
  on-surface-variant: '#bacac1'
  inverse-surface: '#dce1fb'
  inverse-on-surface: '#2a3043'
  outline: '#85948c'
  outline-variant: '#3c4a43'
  surface-tint: '#2fe0aa'
  primary: '#44edb7'
  on-primary: '#003828'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#006c4f'
  secondary: '#b9c7e0'
  on-secondary: '#233144'
  secondary-container: '#3c4a5e'
  on-secondary-container: '#abb9d2'
  tertiary: '#cbd2ed'
  on-tertiary: '#283044'
  tertiary-container: '#afb7d0'
  on-tertiary-container: '#40485d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#d5e3fd'
  secondary-fixed-dim: '#b9c7e0'
  on-secondary-fixed: '#0d1c2f'
  on-secondary-fixed-variant: '#3a485c'
  tertiary-fixed: '#dae2fd'
  tertiary-fixed-dim: '#bec6e0'
  on-tertiary-fixed: '#131b2e'
  on-tertiary-fixed-variant: '#3f465c'
  background: '#0c1324'
  on-background: '#dce1fb'
  surface-variant: '#2e3447'
typography:
  headline-xl:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
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
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
---

## Brand & Style

The design system establishes a high-performance, sophisticated environment for financial management. It targets a modern audience that values precision, security, and clarity. The brand personality is authoritative yet approachable, utilizing a **Corporate / Modern** style with **Minimalist** leanings to reduce cognitive load during complex data analysis.

The aesthetic utilizes deep, monochromatic layers to create a sense of infinite depth, allowing the vibrant emerald accents to guide the user's attention toward critical growth metrics and primary actions. The emotional response should be one of calm confidence and technological edge.

## Colors

The palette is rooted in a deep slate and black monochromatic theme to prioritize visual comfort and focus. 

- **Surface & Background**: The foundation uses a near-black (#020617) for the primary background, providing maximum contrast for data visualization.
- **Surface Containers**: Progressively lighter slates (#0F172A, #1E293B) are used to define cards, sidebars, and modular sections.
- **Accent**: Emerald Green (#00D09C) is reserved strictly for growth indicators, primary call-to-actions, and "positive" financial states.
- **Typography**: Pure White is used for headers to ensure immediate hierarchy, while Body text utilizes a muted Slate-White (#94A3B8) to prevent eye strain during long reading sessions.
- **Borders**: Subdued outlines (#1E293B) replace heavy shadows to define structure without adding visual noise.

## Typography

This design system uses a triple-font strategy to balance character with utility:
1. **Manrope (Headlines)**: A modern, geometric sans-serif that feels both professional and accessible. It is used for all primary titles to establish a refined brand voice.
2. **Inter (Body)**: The workhorse of the system, selected for its exceptional legibility on digital screens, particularly for dense financial data and long-form text.
3. **JetBrains Mono (Labels/Data)**: A technical, monospaced font used for numerical data, currency values, and metadata labels to ensure alignment and a "fintech" precision feel.

Line heights are generous to prevent the dark background from making the text feel cramped.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop to maintain structural integrity of complex dashboards, while transitioning to a **Fluid Grid** for mobile.

- **Desktop**: A 12-column grid with a maximum container width of 1440px. Gutters are fixed at 24px to provide clear separation between data widgets.
- **Tablet**: An 8-column grid with 24px margins.
- **Mobile**: A 4-column fluid grid with 16px margins. 

Spacing follows a strict 4px/8px baseline rhythm. Modular components should favor `padding-md` (24px) for internal whitespace to ensure a premium, airy feel even in a dark environment.

## Elevation & Depth

This design system utilizes **Tonal Layers** rather than heavy shadows to indicate elevation. In a dark theme, depth is achieved by "lifting" surfaces closer to the light source, making them lighter in color:

- **Level 0 (Background)**: #020617 - The furthest back layer.
- **Level 1 (Sections/Cards)**: #0F172A - Default container level.
- **Level 2 (Popovers/Modals)**: #1E293B - Used for elements that float above the primary UI.

Shadows are used sparingly. When necessary, use a subtle, large-radius shadow with a #000000 color at 40% opacity to create a soft separation. Low-contrast outlines (#334155) are preferred for defining card boundaries over shadows.

## Shapes

The shape language is "Soft" (0.25rem / 4px base), reflecting a precise and professional financial instrument. 

- **Buttons & Inputs**: Use `rounded` (4px) to maintain a crisp, structured appearance.
- **Cards & Containers**: Use `rounded-lg` (8px) to provide a subtle friendliness at the macro level.
- **Status Tags/Chips**: May use `rounded-xl` (12px) for high contrast against the rectilinear grid.

The goal is to maintain a professional "tool" aesthetic while avoiding the harshness of 0px sharp corners.

## Components

- **Buttons**: Primary buttons are solid Emerald Green (#00D09C) with black text for maximum contrast. Secondary buttons use a ghost style with #1E293B borders and white text.
- **Input Fields**: Backgrounds use the Level 1 surface (#0F172A) with a subtle border. On focus, the border transitions to Emerald Green.
- **Cards**: Utilize the Level 1 surface with a 1px border (#1E293B). Titles within cards should be Manrope SemiBold.
- **Chips**: Used for categories. These should have a subtle slate background (#1E293B) and JetBrains Mono text.
- **Lists**: Row items are separated by subtle 1px dividers (#0F172A). Hover states should use a slight tonal lift to #1E293B.
- **Data Visualization**: Line charts and bars should primarily use Emerald Green for positive data, with Slate-400 for neutral benchmarks. Avoid using red unless indicating a critical error or severe financial loss.