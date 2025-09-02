# Material Design System Guide
## Vue.js + Tailwind CSS Implementation

### Overview
This design system follows Google's Material Design 3 (Material You) principles for consistent UI components across the Vue.js application using Tailwind CSS utility classes.

---

## Color System

### Primary Colors
- **Primary**: `bg-blue-600` `text-blue-600` `border-blue-600`
- **Primary Container**: `bg-blue-100` `text-blue-900`
- **On Primary**: `text-white`
- **On Primary Container**: `text-blue-900`

### Secondary Colors
- **Secondary**: `bg-slate-600` `text-slate-600` `border-slate-600`
- **Secondary Container**: `bg-slate-100` `text-slate-900`
- **On Secondary**: `text-white`
- **On Secondary Container**: `text-slate-900`

### Surface Colors
- **Surface**: `bg-white` `text-gray-900`
- **Surface Variant**: `bg-gray-50` `text-gray-700`
- **On Surface**: `text-gray-900`
- **On Surface Variant**: `text-gray-700`
- **Outline**: `border-gray-300`
- **Outline Variant**: `border-gray-200`

### State Colors
- **Error**: `bg-red-600` `text-red-600` `border-red-600`
- **Warning**: `bg-amber-600` `text-amber-600` `border-amber-600`
- **Success**: `bg-green-600` `text-green-600` `border-green-600`
- **Info**: `bg-blue-600` `text-blue-600` `border-blue-600`

---

## Typography

### Font Scale
```css
/* Apply these Tailwind classes */
text-xs     /* 12px - Caption */
text-sm     /* 14px - Body Small */
text-base   /* 16px - Body Medium */
text-lg     /* 18px - Body Large */
text-xl     /* 20px - Title Small */
text-2xl    /* 24px - Title Medium */
text-3xl    /* 30px - Title Large */
text-4xl    /* 36px - Headline Small */
text-5xl    /* 48px - Headline Medium */
text-6xl    /* 60px - Headline Large */
```

### Font Weights
- **Regular**: `font-normal` (400)
- **Medium**: `font-medium` (500)
- **Semibold**: `font-semibold` (600)
- **Bold**: `font-bold` (700)

### Text Styles by Component Type
- **Headlines**: `font-normal` to `font-medium`
- **Body Text**: `font-normal`
- **Labels/Buttons**: `font-medium`
- **Captions**: `font-normal text-sm text-gray-600`

---

## Spacing System

### Material Design Spacing Scale (8dp grid)
```css
p-1   /* 4px */
p-2   /* 8px */
p-3   /* 12px */
p-4   /* 16px */
p-5   /* 20px */
p-6   /* 24px */
p-8   /* 32px */
p-10  /* 40px */
p-12  /* 48px */
p-16  /* 64px */
```

### Component Spacing Guidelines
- **Buttons**: `px-6 py-3` (horizontal), `px-4 py-2` (compact)
- **Cards**: `p-4` to `p-6`
- **Input Fields**: `px-3 py-2` to `px-4 py-3`
- **List Items**: `py-3 px-4`

---

## Elevation & Shadows

### Shadow Scale
```css
shadow-none     /* No elevation */
shadow-sm       /* Level 1 - 2dp */
shadow          /* Level 2 - 4dp */
shadow-md       /* Level 3 - 8dp */
shadow-lg       /* Level 4 - 12dp */
shadow-xl       /* Level 5 - 16dp */
shadow-2xl      /* Level 6 - 24dp */
```

### Component Elevation Guidelines
- **Cards**: `shadow-sm` (resting), `shadow-md` (hover)
- **FAB**: `shadow-lg`
- **App Bar**: `shadow-sm`
- **Dialogs**: `shadow-xl`
- **Menus**: `shadow-lg`

---

## Border Radius

### Radius Scale
```css
rounded-none    /* 0px - Sharp corners */
rounded-sm      /* 2px - Small */
rounded         /* 4px - Medium (default) */
rounded-md      /* 6px - Medium+ */
rounded-lg      /* 8px - Large */
rounded-xl      /* 12px - Extra Large */
rounded-2xl     /* 16px - 2X Large */
rounded-3xl     /* 24px - 3X Large */
rounded-full    /* 50% - Circular */
```

### Component Radius Guidelines
- **Buttons**: `rounded-full` (primary), `rounded-lg` (outlined/text)
- **Cards**: `rounded-xl`
- **Input Fields**: `rounded-md`
- **Chips**: `rounded-full`
- **Dialogs**: `rounded-2xl`

---

## Component Specifications

### Buttons

#### Primary Button
```css
/* Classes to apply */
bg-blue-600 hover:bg-blue-700 active:bg-blue-800
text-white font-medium
px-6 py-3 rounded-full
shadow-sm hover:shadow-md
transition-all duration-200
focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
disabled:bg-gray-300 disabled:text-gray-500 disabled:cursor-not-allowed
```

#### Secondary/Outlined Button
```css
/* Classes to apply */
border border-blue-600 hover:bg-blue-50 active:bg-blue-100
text-blue-600 font-medium
px-6 py-3 rounded-lg
transition-all duration-200
focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
disabled:border-gray-300 disabled:text-gray-400 disabled:cursor-not-allowed
```

#### Text Button
```css
/* Classes to apply */
text-blue-600 hover:bg-blue-50 active:bg-blue-100
font-medium px-4 py-2 rounded-lg
transition-all duration-200
focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
disabled:text-gray-400 disabled:cursor-not-allowed
```

### Cards

#### Standard Card
```css
/* Classes to apply */
bg-white rounded-xl shadow-sm hover:shadow-md
border border-gray-100
transition-shadow duration-200
p-4 md:p-6
```

#### Elevated Card
```css
/* Classes to apply */
bg-white rounded-xl shadow-lg
p-4 md:p-6
transition-shadow duration-200
```

### Input Fields

#### Outlined Text Field
```css
/* Container */
relative w-full

/* Input */
w-full px-3 py-3 border border-gray-300 rounded-md
focus:border-blue-600 focus:ring-1 focus:ring-blue-600
placeholder-gray-500 text-gray-900
disabled:bg-gray-50 disabled:text-gray-500

/* Label (floating) */
absolute -top-2 left-3 px-1 bg-white text-sm text-gray-600
peer-focus:text-blue-600 transition-colors duration-200
```

#### Filled Text Field
```css
/* Input */
w-full px-3 py-3 bg-gray-50 border-b-2 border-gray-300 rounded-t-md
focus:border-blue-600 focus:bg-white
placeholder-gray-500 text-gray-900
```

### Navigation

#### App Bar/Header
```css
/* Classes to apply */
bg-white shadow-sm border-b border-gray-100
px-4 py-3 md:px-6 md:py-4
flex items-center justify-between
```

#### Bottom Navigation
```css
/* Container */
fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200
px-2 py-1
flex justify-around items-center

/* Nav Item */
flex flex-col items-center py-2 px-3 rounded-lg
text-gray-600 hover:text-blue-600 hover:bg-blue-50
transition-all duration-200

/* Active Nav Item */
text-blue-600 bg-blue-50
```

### Lists

#### List Item
```css
/* Classes to apply */
flex items-center py-3 px-4
hover:bg-gray-50 active:bg-gray-100
border-b border-gray-100 last:border-b-0
transition-colors duration-150
```

### Chips

#### Standard Chip
```css
/* Classes to apply */
inline-flex items-center px-3 py-1 rounded-full
bg-gray-100 hover:bg-gray-200
text-gray-800 text-sm font-medium
transition-colors duration-200
```

#### Selected Chip
```css
/* Classes to apply */
inline-flex items-center px-3 py-1 rounded-full
bg-blue-100 text-blue-800
text-sm font-medium
```

---

## Animation & Transitions

### Standard Transitions
```css
/* Apply to interactive elements */
transition-all duration-200 ease-in-out     /* General purpose */
transition-colors duration-200              /* Color changes */
transition-shadow duration-200              /* Elevation changes */
transition-transform duration-150           /* Movement/scale */
```

### Hover States
- **Scale**: `hover:scale-105` (for cards, buttons)
- **Lift**: `hover:shadow-md` (for elevated elements)
- **Color**: `hover:bg-blue-50` (for interactive surfaces)

---

## Accessibility Guidelines

### Focus States
```css
/* Apply to all interactive elements */
focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
focus:outline-none
```

### Color Contrast
- Ensure minimum 4.5:1 contrast ratio for normal text
- Ensure minimum 3:1 contrast ratio for large text
- Use `text-gray-900` on `bg-white` for maximum readability

### Touch Targets
- Minimum touch target: `min-h-[44px] min-w-[44px]`
- For mobile: `py-3 px-4` minimum

---

## Responsive Design

### Breakpoints (Tailwind defaults)
```css
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Component Responsiveness
- **Padding**: `p-4 md:p-6 lg:p-8`
- **Text**: `text-sm md:text-base lg:text-lg`
- **Spacing**: `space-y-4 md:space-y-6`
- **Grid**: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`

---

## Implementation Notes for Claude Code Agent

### Vue.js Specific Considerations
1. **Component Props**: Use TypeScript interfaces for prop definitions
2. **Composables**: Create shared composables for common Material Design behaviors
3. **Slots**: Design components with flexible slot-based content insertion
4. **Emits**: Follow Material Design interaction patterns for event emission

### Tailwind CSS Optimization
1. **Custom Components**: Create Tailwind component classes for frequently used combinations
2. **Configuration**: Extend Tailwind config with custom Material Design values if needed
3. **Purging**: Ensure all used classes are included in the build

### Code Patterns
```vue
<!-- Example button component structure -->
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
// Component implementation following Material Design patterns
</script>
```

---

## Quick Reference

### Most Common Class Combinations
- **Primary Button**: `bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-3 rounded-full shadow-sm hover:shadow-md transition-all duration-200`
- **Card**: `bg-white rounded-xl shadow-sm hover:shadow-md border border-gray-100 p-6 transition-shadow duration-200`
- **Input**: `w-full px-3 py-3 border border-gray-300 rounded-md focus:border-blue-600 focus:ring-1 focus:ring-blue-600`
- **List Item**: `flex items-center py-3 px-4 hover:bg-gray-50 border-b border-gray-100`

This design system ensures consistent Material Design implementation across all Vue.js components using Tailwind CSS utilities.