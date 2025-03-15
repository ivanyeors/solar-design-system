# Solar Design System - Token Extractor

This repository contains a toolkit for extracting and organizing design tokens from TokenStudio's `tokens.json` file into a structured format following industry best practices.

## File Structure

The token extractor script organizes the tokens into a scalable file structure:

```
src/
└── tokens/
    ├── option-tokens/       # Base primitive tokens
    │   ├── colors.js        # Color palette tokens
    │   └── scale.js         # Scale, spacing, sizing tokens
    ├── semantic-tokens/     # Semantic application tokens
    │   ├── brands.js        # Brand-specific tokens
    │   └── themes.js        # Theme tokens (light/dark)
    └── index.js             # Main entry point exporting all tokens
```

## Token Organization

Following design system best practices, the tokens are organized into two main categories:

### 1. Option Tokens

These are the primitive, base-level design tokens that serve as the foundation of the design system:

- **Colors:** Base color palette including neutrals, brand colors, and supporting colors
- **Scale:** Foundational measurements including spacing, sizing, radius, etc.

### 2. Semantic Tokens

These tokens have semantic meaning and are used in specific contexts:

- **Brands:** Brand-specific tokens that define the visual identity of each brand
- **Themes:** Theme tokens for light and dark modes

## How It Works

The token extractor script:

1. Reads the `tokens.json` file from the TokenStudio directory
2. Processes the nested token structure into a flat format
3. Categorizes tokens based on their path and type
4. Generates JavaScript modules for each token category
5. Creates an index file to export all token modules

## Usage

### Running the Token Extractor

```bash
# Install dependencies (if needed)
npm install

# Run the token extractor script
node token-extractor.js
```

### Importing Tokens in Your Application

```javascript
// Import all tokens
import tokens from './src/tokens';

// Or import specific token groups
import { optionColors, themes } from './src/tokens';

// Usage example
const primaryColor = themes['brand-primary'];
const spacing = optionScale['spacing-medium'];
```

## Keeping Tokens Updated

The extractor script is designed to always pull the latest tokens from the `tokens.json` file. When tokens are updated:

1. Update the `tokens.json` file in the TokenStudio directory
2. Run the token extractor script
3. The tokens will be automatically updated in your application

## Best Practices

- **Reference, Don't Duplicate:** Always reference tokens directly rather than duplicating values
- **Use Semantic Tokens:** Prefer semantic tokens over direct color references
- **Theme Support:** Design components to use theme tokens for built-in dark/light mode support
- **Keep It Simple:** Group related tokens together to make them easier to find and use

## Industry Standards

This token organization follows industry standards from major design systems such as:

- Google's Material Design
- Salesforce Lightning Design System
- Atlassian Design System
- IBM Carbon Design System

By organizing tokens this way, we ensure scalability, maintainability, and compatibility with best practices in the design systems community.
