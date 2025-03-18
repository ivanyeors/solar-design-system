# ConfigPanel Usage Guide

## Overview
The `ConfigPanel` component provides a standardized interface for interactive playground sections across all components in the design system. It ensures consistent styling and behavior for configuration panels, while adapting to both light and dark themes automatically through the use of design tokens.

## Implementation Requirements

All interactive playground sections in component pages must use the `ConfigPanel` component rather than implementing custom control panels. This ensures:

1. Consistent visual appearance across all component pages
2. Proper theme support (light and dark modes)
3. Accessibility compliance
4. Scalable and maintainable code
5. Design token usage instead of hardcoded values

## Basic Implementation Example

Here's a typical implementation of the `ConfigPanel` in a component preview:

```vue
<script setup lang="ts">
import { ref } from 'vue';
import YourComponent from '../ui/YourComponent.vue';
import ConfigPanel from '../ConfigPanel.vue';

// State for component configuration
const size = ref('md');
const variant = ref('primary');
const showLabel = ref(true);
// ... other component-specific state

// Handle config updates from ConfigPanel
const updateConfig = (configKey: string, value: any) => {
  if (configKey === 'size') size.value = value;
  if (configKey === 'variant') variant.value = value;
  if (configKey === 'showLabel') showLabel.value = value;
  // ... handle other properties
};
</script>

<template>
  <div class="flex flex-col lg:flex-row gap-8">
    <!-- Component Preview Area -->
    <div class="flex-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-8 flex items-center justify-center">
      <YourComponent 
        :size="size"
        :variant="variant"
        :show-label="showLabel"
        <!-- ... other props -->
      />
    </div>

    <!-- Config Panel -->
    <ConfigPanel 
      title="your-component-v1.0.0"
      :current-size="size"
      :current-variant="variant"
      :show-label="showLabel"
      :size-options="[
        { value: 'sm', label: 'Small' },
        { value: 'md', label: 'Medium' },
        { value: 'lg', label: 'Large' }
      ]"
      :variant-options="[
        { value: 'primary', label: 'Primary' },
        { value: 'secondary', label: 'Secondary' }
      ]"
      :token-values="{
        padding: '8px 16px',
        fontSize: '14px',
        brand: 'Auto (Default)',
        colorMode: 'Auto (Light/Dark)',
        tokenColor: 'Auto (Default)'
      }"
      @update:config="updateConfig"
    />
  </div>
</template>
```

## ConfigPanel Props

| Prop | Type | Description |
|------|------|-------------|
| `title` | String | Component name and version |
| `currentSize` | String | Current selected size value |
| `currentState` | String | Current component state |
| `currentType` | String | Current component type/variant |
| `showLabel` | Boolean | Whether to show component label |
| `labelText` | String | Text for component label |
| `showLeadingIcon` | Boolean | Whether to show leading icon |
| `showTrailingIcon` | Boolean | Whether to show trailing icon |
| `sizeOptions` | Array | Options for size selection |
| `stateOptions` | Array | Options for state selection |
| `typeOptions` | Array | Options for type/variant selection |
| `tokenValues` | Object | Token values to display |

## Events

| Event | Payload | Description |
|-------|---------|-------------|
| `update:config` | `(key: string, value: any)` | Emitted when a config value changes |

## Extending ConfigPanel

For components with unique configuration needs:

1. Submit a request to extend ConfigPanel with new capabilities
2. Do not create component-specific control panels
3. Ensure all extensions follow design system guidelines

## Troubleshooting

If you encounter issues implementing ConfigPanel:

1. Verify you're using the latest version of ConfigPanel
2. Check props are being passed correctly
3. Review event handler implementation
4. Ensure token values are being used properly

For further assistance, contact the design system team. 