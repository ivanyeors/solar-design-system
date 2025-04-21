# Solar Design System

## Component Naming and Export Standards

### Export Patterns

All components are exported with both their original name and a Base-prefixed version for flexibility:

```js
// Importing with Base prefix (recommended)
import { BaseButton } from '@/design-system/components/core/button';

// Importing with original name (also supported)
import { Button } from '@/design-system/components/core/button';
```

### Implementation

We use a standardized export utility to ensure consistent naming throughout the design system:

```js
// In component index files
import { createComponentExports } from '@/lib/utils/components';
import ComponentFile from './components/Component.vue';

export const { Component, BaseComponent } = createComponentExports(ComponentFile, 'Component');
```

### Best Practices

1. Always use the Base-prefixed version in application code for clarity
2. Keep component names consistent with their file names
3. Use the component export utility for all design system components
4. Follow the established directory structure
5. Import directly from the component's index file

## Directory Structure

```
/src
├── design-system/    # Design system core
│   ├── tokens/      # Design tokens
│   ├── components/  # Base components library
│   │   ├── core/    # Core components
│   │   │   ├── button/
│   │   │   │   ├── components/   # Component implementations
│   │   │   │   ├── index.ts      # Component exports
│   │   │   │   └── ButtonTokens.ts  # Component-specific tokens
│   │   │   ├── badge/
│   │   │   └── icon/
│   │   └── composite/  # Composite components
│   └── patterns/    # Common UI patterns and layouts
├── lib/            # Shared libraries and utilities
│   └── utils/      # Utility functions
├── utils/          # Application utilities
└── pages/          # Application pages
```

## Token and Utility Organization

- Core token definitions and functions: `src/lib/tokens.ts`
- Component-specific tokens: `src/design-system/components/core/[component]/[Component]Tokens.ts`
- Component export utility: `src/lib/utils/components.ts`
- Supplementary token utilities: `src/utils/tokenUtils.ts` 