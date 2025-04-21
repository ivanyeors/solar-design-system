# BaseButton

The `BaseButton` component is a fundamental building block for user interactions. It provides a consistent, accessible, and customizable button implementation.

## Usage

```vue
<template>
  <BaseButton variant="primary" size="md">Click me</BaseButton>
</template>

<script setup lang="ts">
import { BaseButton } from '@/design-system/components/core/button';
</script>
```

## Props

| Name | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'outline' \| 'ghost' \| 'danger' \| 'warning' \| 'success' | 'primary' | The visual style variant of the button |
| size | 'sm' \| 'md' \| 'lg' \| 'xl' | 'md' | The size of the button |
| disabled | boolean | false | Whether the button is disabled |
| loading | boolean | false | Whether the button is in a loading state |

## Events

| Name | Parameters | Description |
|------|------------|-------------|
| click | (event: MouseEvent) | Emitted when the button is clicked |

## Accessibility

The BaseButton component follows WCAG 2.1 AA guidelines:

- Uses native `<button>` element for proper semantics
- Supports keyboard navigation
- Maintains proper focus states
- Includes ARIA attributes for loading and disabled states
- Ensures sufficient color contrast in all variants

## Examples

### Basic Usage
```vue
<BaseButton>Default Button</BaseButton>
```

### Variants
```vue
<template>
  <BaseButton variant="primary">Primary</BaseButton>
  <BaseButton variant="secondary">Secondary</BaseButton>
  <BaseButton variant="outline">Outline</BaseButton>
  <BaseButton variant="ghost">Ghost</BaseButton>
</template>
```

### Sizes
```vue
<template>
  <BaseButton size="sm">Small</BaseButton>
  <BaseButton size="md">Medium</BaseButton>
  <BaseButton size="lg">Large</BaseButton>
  <BaseButton size="xl">Extra Large</BaseButton>
</template>
```

### States
```vue
<template>
  <BaseButton disabled>Disabled</BaseButton>
  <BaseButton loading>Loading</BaseButton>
</template>
```

## Do's and Don'ts

### Do's
- Use appropriate variants for different actions (primary for main actions, secondary for alternative actions)
- Include clear, action-oriented text
- Use loading state for async operations
- Maintain consistent spacing between buttons

### Don'ts
- Don't use multiple primary buttons in the same section
- Avoid long button text that might wrap
- Don't disable buttons without providing feedback about why
- Don't use buttons when links are more appropriate

## Edge Cases

- Long text handling
- Right-to-left language support
- Mobile touch targets
- Loading state transitions
- Focus management in modals

## Breaking Changes

### v2.0.0
- Renamed from `ButtonMain` to `BaseButton`
- Changed variant prop values
- Updated token structure
- Modified size variants

## Migration Guide

### From v1.x to v2.0.0

1. Update import statements:
```diff
- import { ButtonMain as Button } from '@/design-system/button';
+ import { BaseButton } from '@/design-system/components/core/button';
```

2. Update component usage:
```diff
- <Button variant="default">Click me</Button>
+ <BaseButton variant="primary">Click me</BaseButton>
```

3. Review and update size props:
```diff
- <Button size="small">Click me</Button>
+ <BaseButton size="sm">Click me</BaseButton>
``` 