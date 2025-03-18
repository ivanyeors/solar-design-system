# ConfigPanel Component

## Overview

The ConfigPanel component provides a standardized configuration interface for the interactive playground sections across the design system. It's designed to be reusable, theme-aware, and accessible.

## Features

- **Theme Compatibility**: Automatically adapts to light and dark themes using design tokens
- **Standardized Controls**: Consistent UI for common component properties
- **Responsive Design**: Adapts to different screen sizes
- **Accessibility**: Built with proper ARIA attributes and keyboard navigation
- **Typescript Support**: Fully typed component props and events

## Directory Location

```
src/components/ConfigPanel.vue
```

## Implementation Guidelines

All component playground sections must use the ConfigPanel component instead of implementing custom control panels. See `src/docs/ConfigPanelUsage.md` for detailed implementation instructions.

## Component Structure

The ConfigPanel is organized into several sections:

1. **Header**: Component title and action buttons
2. **Control Groups**: Configuration options organized by category
   - Size controls
   - State controls
   - Type/variant controls
   - Label controls
   - Icon controls
3. **Token Values**: Displays design tokens used by the component

## Design Token Usage

The ConfigPanel uses the following design tokens:

- **Colors**: Surface, border, text, and icon colors
- **Spacing**: Padding, gaps, and margins
- **Typography**: Font sizes and weights
- **Borders**: Border widths, styles, and radii
- **Transitions**: Timing functions and durations

## Customizing the ConfigPanel

The ConfigPanel is designed to be comprehensive enough for most components. If you need additional functionality:

1. Consider if the functionality would benefit other components as well
2. Propose the addition to the design system team
3. Do not create component-specific variants of ConfigPanel

## Best Practices

- Pass all required props to ConfigPanel
- Implement the update event handler correctly
- Keep configuration options minimal and focused on common use cases
- Use appropriate design tokens for any surrounding layout elements
- Test the ConfigPanel in both light and dark themes

## Example Implementation

See `src/components/showcase/ButtonPreview.vue` for a complete implementation example. 