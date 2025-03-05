# Vue Design System

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
npm install vue-design-system
```

## Usage

### Global Registration

```js
// main.js or main.ts
import { createApp } from 'vue'
import App from './App.vue'
import VueDesignSystem from 'vue-design-system'
import 'vue-design-system/style.css'

const app = createApp(App)
app.use(VueDesignSystem)
app.mount('#app')
```

### Individual Component Import

```vue
<script setup>
import { Button } from 'vue-design-system'
import 'vue-design-system/style.css'
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

## GitHub Pages Deployment

The documentation site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

## License

MIT
