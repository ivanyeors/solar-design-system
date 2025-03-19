import { ref, computed } from 'vue';

export type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'warning' | 'success';

export interface TokenDefinition {
  name: string;
  value: string;
  usage: string;
}

// ==============================================
// Button Component Token Categories
// ==============================================

/**
 * Component-specific button tokens that apply to all variants
 */
const componentButtonTokens = {
  // Layout tokens
  layout: [
    { name: '--comp-button-main-radius', usage: 'Button corner radius' },
    { name: '--comp-button-main-gap', usage: 'Gap between elements in button' },
  ],
  // Padding tokens
  padding: [
    { name: '--comp-button-main-h-padding-s', usage: 'Horizontal padding for small buttons' },
    { name: '--comp-button-main-v-padding-s', usage: 'Vertical padding for small buttons' },
    { name: '--comp-button-main-h-padding-m', usage: 'Horizontal padding for medium buttons' },
    { name: '--comp-button-main-v-padding-m', usage: 'Vertical padding for medium buttons' },
    { name: '--comp-button-main-h-padding-l', usage: 'Horizontal padding for large buttons' },
    { name: '--comp-button-main-v-padding-l', usage: 'Vertical padding for large buttons' },
    { name: '--comp-button-main-h-padding-xl', usage: 'Horizontal padding for extra large buttons' },
    { name: '--comp-button-main-v-padding-xl', usage: 'Vertical padding for extra large buttons' },
  ],
  // State tokens
  states: [
    { name: '--comp-button-main-disabled-opacity', usage: 'Opacity for disabled state' },
  ]
};

/**
 * Variant-specific semantic tokens mapping
 */
const variantTokenCategories = {
  primary: {
    prefix: '--comp-button-main',
    relevantTokens: [
      { type: 'fill-pri', usage: 'Primary button background' },
      { type: 'text-color-fill-pri', usage: 'Primary button text color' },
      { type: 'color-stroke-pri', usage: 'Primary button border color' },
    ],
    semanticTokens: {
      background: [
        { name: '--color-fill-brand-rest', usage: 'Default background' },
        { name: '--color-fill-brand-hover', usage: 'Hover background' },
        { name: '--color-fill-brand-press', usage: 'Pressed background' },
        { name: '--color-fill-brand-focus', usage: 'Focused background' },
        { name: '--color-fill-brand-disabled', usage: 'Disabled background' },
      ],
      text: [
        { name: '--color-text-primary-inverse', usage: 'Default text color' },
        { name: '--color-text-primary-inverse', usage: 'Hover text color' },
        { name: '--color-text-primary-inverse', usage: 'Pressed text color' },
        { name: '--color-text-primary-inverse', usage: 'Focused text color' },
        { name: '--color-text-primary-disabled', usage: 'Disabled text color' },
      ],
      border: [
        { name: '--color-border-brand-rest', usage: 'Default border' },
        { name: '--color-border-brand-hover', usage: 'Hover border' },
        { name: '--color-border-brand-press', usage: 'Pressed border' },
        { name: '--color-border-brand-focus', usage: 'Focus ring color' },
        { name: '--color-border-brand-disabled', usage: 'Disabled border' },
      ],
    }
  },
  secondary: {
    prefix: '--comp-button-main',
    relevantTokens: [
      { type: 'fill-sec', usage: 'Secondary button background' },
      { type: 'text-color-fill-sec', usage: 'Secondary button text color' },
      { type: 'color-stroke-sec', usage: 'Secondary button border color' },
    ],
    semanticTokens: {
      background: [
        { name: '--color-surface-primary-rest', usage: 'Default background' },
        { name: '--color-surface-primary-hover', usage: 'Hover background' },
        { name: '--color-surface-primary-press', usage: 'Pressed background' },
        { name: '--color-surface-primary-focus', usage: 'Focused background' },
        { name: '--color-surface-primary-disabled', usage: 'Disabled background' },
      ],
      text: [
        { name: '--color-text-primary-rest', usage: 'Default text color' },
        { name: '--color-text-primary-hover', usage: 'Hover text color' },
        { name: '--color-text-primary-press', usage: 'Pressed text color' },
        { name: '--color-text-primary-focus', usage: 'Focused text color' },
        { name: '--color-text-primary-disabled', usage: 'Disabled text color' },
      ],
      border: [
        { name: '--color-border-primary-rest', usage: 'Default border' },
        { name: '--color-border-primary-hover', usage: 'Hover border' },
        { name: '--color-border-primary-press', usage: 'Pressed border' },
        { name: '--color-border-primary-focus', usage: 'Focus ring color' },
        { name: '--color-border-primary-disabled', usage: 'Disabled border' },
      ],
    }
  },
  danger: {
    prefix: '--color',
    relevantTokens: [
      { type: 'fill-danger', usage: 'Danger button background' },
      { type: 'text-danger', usage: 'Danger button text color' },
      { type: 'border-danger', usage: 'Danger button border color' },
    ],
    semanticTokens: {
      background: [
        { name: '--color-fill-danger-rest', usage: 'Default background' },
        { name: '--color-fill-danger-hover', usage: 'Hover background' },
        { name: '--color-fill-danger-press', usage: 'Pressed background' },
        { name: '--color-fill-danger-focus', usage: 'Focused background' },
        { name: '--color-fill-danger-disabled', usage: 'Disabled background' },
      ],
      text: [
        { name: '--color-text-primary-inverse', usage: 'Default text color' },
        { name: '--color-text-primary-inverse', usage: 'Hover text color' },
        { name: '--color-text-primary-inverse', usage: 'Pressed text color' },
        { name: '--color-text-primary-inverse', usage: 'Focused text color' },
        { name: '--color-text-danger-disabled', usage: 'Disabled text color' },
      ],
      border: [
        { name: '--color-border-danger-rest', usage: 'Default border' },
        { name: '--color-border-danger-hover', usage: 'Hover border' },
        { name: '--color-border-danger-press', usage: 'Pressed border' },
        { name: '--color-border-danger-focus', usage: 'Focus ring color' },
        { name: '--color-border-danger-disabled', usage: 'Disabled border' },
      ],
    }
  },
  warning: {
    prefix: '--color',
    relevantTokens: [
      { type: 'fill-warning', usage: 'Warning button background' },
      { type: 'text-warning', usage: 'Warning button text color' },
      { type: 'border-warning', usage: 'Warning button border color' },
    ],
    semanticTokens: {
      background: [
        { name: '--color-fill-warning-rest', usage: 'Default background' },
        { name: '--color-fill-warning-hover', usage: 'Hover background' },
        { name: '--color-fill-warning-press', usage: 'Pressed background' },
        { name: '--color-fill-warning-focus', usage: 'Focused background' },
        { name: '--color-fill-warning-disabled', usage: 'Disabled background' },
      ],
      text: [
        { name: '--color-text-primary-inverse', usage: 'Default text color' },
        { name: '--color-text-primary-inverse', usage: 'Hover text color' },
        { name: '--color-text-primary-inverse', usage: 'Pressed text color' },
        { name: '--color-text-primary-inverse', usage: 'Focused text color' },
        { name: '--color-text-warning-disabled', usage: 'Disabled text color' },
      ],
      border: [
        { name: '--color-border-warning-rest', usage: 'Default border' },
        { name: '--color-border-warning-hover', usage: 'Hover border' },
        { name: '--color-border-warning-press', usage: 'Pressed border' },
        { name: '--color-border-warning-focus', usage: 'Focus ring color' },
        { name: '--color-border-warning-disabled', usage: 'Disabled border' },
      ],
    }
  },
  success: {
    prefix: '--color',
    relevantTokens: [
      { type: 'fill-success', usage: 'Success button background' },
      { type: 'text-success', usage: 'Success button text color' },
      { type: 'border-success', usage: 'Success button border color' },
    ],
    semanticTokens: {
      background: [
        { name: '--color-fill-success-rest', usage: 'Default background' },
        { name: '--color-fill-success-hover', usage: 'Hover background' },
        { name: '--color-fill-success-press', usage: 'Pressed background' },
        { name: '--color-fill-success-focus', usage: 'Focused background' },
        { name: '--color-fill-success-disabled', usage: 'Disabled background' },
      ],
      text: [
        { name: '--color-text-primary-inverse', usage: 'Default text color' },
        { name: '--color-text-primary-inverse', usage: 'Hover text color' },
        { name: '--color-text-primary-inverse', usage: 'Pressed text color' },
        { name: '--color-text-primary-inverse', usage: 'Focused text color' },
        { name: '--color-text-success-disabled', usage: 'Disabled text color' },
      ],
      border: [
        { name: '--color-border-success-rest', usage: 'Default border' },
        { name: '--color-border-success-hover', usage: 'Hover border' },
        { name: '--color-border-success-press', usage: 'Pressed border' },
        { name: '--color-border-success-focus', usage: 'Focus ring color' },
        { name: '--color-border-success-disabled', usage: 'Disabled border' },
      ],
    }
  }
};

// States to include for each token type
const tokenStates = ['rest', 'hover', 'press', 'focus', 'disabled'];

/**
 * Gets the computed value of a CSS variable
 */
const getCSSVariableValue = (variableName: string): string => {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(variableName)
    .trim();
};

/**
 * Gets all component-specific tokens for buttons
 */
export const getComponentButtonTokens = (): TokenDefinition[] => {
  const tokens: TokenDefinition[] = [];

  // Add layout tokens
  componentButtonTokens.layout.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  // Add padding tokens
  componentButtonTokens.padding.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  // Add state tokens
  componentButtonTokens.states.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  return tokens;
};

/**
 * Gets all semantic tokens for a specific button variant
 */
export const getVariantSemanticTokens = (variant: keyof typeof variantTokenCategories): TokenDefinition[] => {
  const tokens: TokenDefinition[] = [];
  const variantConfig = variantTokenCategories[variant];

  // Add background tokens
  variantConfig.semanticTokens.background.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  // Add text tokens
  variantConfig.semanticTokens.text.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  // Add border tokens
  variantConfig.semanticTokens.border.forEach(token => {
    tokens.push({
      name: token.name,
      value: getCSSVariableValue(token.name),
      usage: token.usage
    });
  });

  return tokens;
};

/**
 * Gets all tokens for a specific button variant
 */
export const getButtonTokens = (variant: keyof typeof variantTokenCategories): TokenDefinition[] => {
  // Get component-specific tokens
  const componentTokens = getComponentButtonTokens();
  
  // Get semantic tokens for the variant
  const semanticTokens = getVariantSemanticTokens(variant);

  // Combine and return all tokens
  return [...componentTokens, ...semanticTokens];
};

/**
 * Gets tokens for specific button sizes
 * @param sizes Array of size options ('sm' | 'md' | 'lg')
 * @returns Array of token definitions
 */
export const getButtonSizeTokens = (sizes: Array<keyof typeof sizeTokens>): TokenDefinition[] => {
  return sizes.map(size => ({
    name: sizeTokens[size].name,
    value: getCSSVariableValue(sizeTokens[size].name),
    usage: sizeTokens[size].usage
  }));
};

/**
 * Gets common button tokens that apply to all variants
 * @returns Array of token definitions
 */
export const getCommonButtonTokens = (): TokenDefinition[] => {
  return commonButtonTokens.map(token => ({
    name: token.name,
    value: getCSSVariableValue(token.name),
    usage: token.usage
  }));
}; 