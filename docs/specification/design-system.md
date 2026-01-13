# ShutterZilla Design System

This document outlines the design system for the ShutterZilla platform, providing a consistent visual language and component library for implementation.

## 1. Color Palette

The color palette is designed to be clean, modern, and accessible, with a primary teal accent.

| Color Name | Hex Value | CSS Variable | Usage |
|---|---|---|---|
| **Teal** | `#0d9488` | `--color-teal` | Primary actions, links, active states, highlights |
| **Teal Light** | `#14b8a6` | `--color-teal-light` | Hover states for primary actions |
| **Slate Dark** | `#334155` | `--color-slate-dark` | Body text, headings, footer background |
| **Slate** | `#475569` | `--color-slate` | Secondary text, subtitles |
| **Slate Light** | `#64748b` | `--color-slate-light` | Muted text, icons, borders |
| **Gray 100** | `#f1f5f9` | `--color-gray-100` | Light backgrounds, hover states |
| **Gray 200** | `#e2e8f0` | `--color-gray-200` | Borders, dividers |
| **Gray 300** | `#cbd5e1` | `--color-gray-300` | Input borders |
| **White** | `#ffffff` | `--color-white` | Card backgrounds, text on dark backgrounds |
| **Background** | `#f8f9fa` | `--color-background` | Main page background |

### Source & Status Colors

| Color | Hex | Usage |
|---|---|---|
| **Success** | `#dcfce7` / `#166534` | Success messages, online indicators |
| **Sold / Error** | `#ef4444` | Sold badges, error messages |
| **Mercari Red** | `#ff4444` | Mercari source badge |
| **Buyee Amber** | `#ff9900` | Buyee source badge |
| **eBay Gradient** | `linear-gradient(...)` | eBay source badge |

## 2. Typography

We use the "Inter" font for a clean, sans-serif look, with a system font fallback.

- **Font Family:** `Inter`, -apple-system, BlinkMacSystemFont, `Segoe UI`, Roboto, sans-serif
- **Base Font Size:** 16px
- **Line Height:** 1.5

| Element | Font Size | CSS Variable |
|---|---|---|
| Small | 14px | `--font-size-sm` |
| Base | 16px | `--font-size-base` |
| Large | 18px | `--font-size-lg` |
| Extra Large | 24px | `--font-size-xl` |
| 2x Extra Large | 32px | `--font-size-2xl` |

## 3. Spacing

A consistent 4px-based spacing scale is used for padding, margins, and gaps.

| Name | Value | CSS Variable |
|---|---|---|
| `xs` | 4px | `--spacing-xs` |
| `sm` | 8px | `--spacing-sm` |
| `md` | 16px | `--spacing-md` |
| `lg` | 24px | `--spacing-lg` |
| `xl` | 32px | `--spacing-xl` |
| `2xl` | 48px | `--spacing-2xl` |

## 4. Border Radius

| Name | Value | CSS Variable |
|---|---|---|
| `sm` | 4px | `--radius-sm` |
| `md` | 8px | `--radius-md` |
| `lg` | 12px | `--radius-lg` |
| `full` | 9999px | `--radius-full` |

## 5. Shadows

| Name | Value | CSS Variable |
|---|---|---|
| `sm` | `0 1px 2px rgba(0, 0, 0, 0.05)` | `--shadow-sm` |
| `md` | `0 4px 6px rgba(0, 0, 0, 0.1)` | `--shadow-md` |

## 6. Logo Usage

| Logo | File | Dimensions | Usage |
|---|---|---|---|
| **Top Bar Logo** | `assets/logo-topbar.png` | 176x50px | Top bar on all app pages |
| **Footer Logo** | `assets/logo-footer.png` | 176x50px | Inverted version for the dark footer |

## 7. Official Slogan

> "Modern apps for your vintage cameras"
