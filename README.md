# Solar Design System

A modern design system built with Vue 3 and Tailwind CSS. This library provides a set of reusable components to help build consistent UIs quickly.

## Features

- 🔥 Built with Vue 3 Composition API and TypeScript
- 🎨 Styled with Tailwind CSS
- 📦 Includes common UI components
- 📝 Fully typed props and events
- 📱 Responsive design
- ♿ Accessibility built-in

## Installation

```bash
npm install solar-design-system
```

## Usage

### Global Registration

```js
// main.js or main.ts
import { createApp } from 'vue'
import App from './App.vue'
import SolarDesignSystem from 'solar-design-system'
import 'solar-design-system/style.css'

const app = createApp(App)
app.use(SolarDesignSystem)
app.mount('#app')
```

### Individual Component Import

```vue
<script setup>
import { Button } from 'solar-design-system'
import 'solar-design-system/style.css'
</script>

<template>
  <Button variant="primary">Click Me</Button>
</template>
```

## Available Components

### Button

A versatile button component with various styles and states.

```vue
<Button variant="primary" size="md">Click Me</Button>
```

Props:
- `variant`: 'primary' | 'secondary' | 'outline' | 'ghost'
- `size`: 'sm' | 'md' | 'lg'
- `disabled`: boolean
- `loading`: boolean

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build the library
npm run build
```

## Browser Tools Integration

This project supports integration with the Agent Desk AI browser-tools for enhanced development capabilities when working with Cursor IDE and Claude. The browser-tools server will automatically start when you run the development server or Storybook if the feature is enabled.

### Usage

1. Run development server with browser-tools:
   ```bash
   # Enable browser-tools
   BROWSER_TOOLS_ENABLED=true npm run dev

   # Or on Windows PowerShell
   $env:BROWSER_TOOLS_ENABLED = "true"; npm run dev
   ```

2. Run Storybook with browser-tools:
   ```bash
   # Enable browser-tools
   BROWSER_TOOLS_ENABLED=true npm run storybook

   # Or on Windows PowerShell
   $env:BROWSER_TOOLS_ENABLED = "true"; npm run storybook
   ```

3. Run just the browser-tools server:
   ```bash
   npm run browser-tools
   ```

### Disabling Browser Tools

If you need to run without the browser-tools server:
```bash
# Explicitly disable browser-tools
BROWSER_TOOLS_ENABLED=false npm run dev

# Or use the direct commands
npm run dev:no-tools
npm run storybook:no-tools
```

## GitHub Pages Deployment

The documentation site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

## License

MIT
