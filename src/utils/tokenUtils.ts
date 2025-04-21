/**
 * Token utilities for handling design tokens and theme changes.
 * Note: Core token functions are in lib/tokens.ts, these are supplementary utilities.
 */

import { ref, computed } from 'vue';
import type { TokenDefinition } from '../lib/tokens';

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
export const getButtonSizeTokens = (sizes: Array<'sm' | 'md' | 'lg' | 'xl'>): TokenDefinition[] => {
  const allSizeTokens = getDynamicButtonTokens().filter(token => 
    token.name.includes('padding') || 
    token.name.includes('height') || 
    token.name.includes('width')
  );
  
  return allSizeTokens.filter(token => {
    return sizes.some(size => {
      const sizeSuffix = size === 'sm' ? '-s' : 
                        size === 'md' ? '-m' : 
                        size === 'lg' ? '-l' : '-xl';
      return token.name.endsWith(sizeSuffix);
    });
  });
};

/**
 * Returns common button tokens that are not specific to a variant or state
 * @returns Array of common button tokens
 */
export const getCommonButtonTokens = (): TokenDefinition[] => {
  return getDynamicButtonTokens().filter(token => {
    // Include all component button tokens that don't have state/variant specificity
    return token.name.startsWith('--comp-button-main') && 
           !token.name.includes('-hover') && 
           !token.name.includes('-press') && 
           !token.name.includes('-focus') && 
           !token.name.includes('-disabled');
  });
};

/**
 * Gets all tokens for a specific selector (light or dark mode)
 * @param selector CSS selector for theme (:root or :root[data-theme="dark"])
 * @returns A collection of all tokens for the specified theme
 */
export const getAllTokensForTheme = (theme: 'light' | 'dark'): Record<string, string> => {
  const selector = theme === 'light' ? ':root' : ':root[data-theme="dark"]';
  const cssRules = Array.from(document.styleSheets)
    .filter(sheet => {
      try {
        // Filter to only include our compiled tokens CSS
        return sheet.href && sheet.href.includes('compiled-tokens.css');
      } catch (e) {
        // Cross-origin sheets will throw errors when attempting to access cssRules
        return false;
      }
    })
    .flatMap(sheet => Array.from(sheet.cssRules))
    .find(rule => rule instanceof CSSStyleRule && rule.selectorText === selector) as CSSStyleRule;
  
  if (!cssRules) return {};
  
  const styleObj: Record<string, string> = {};
  for (let i = 0; i < cssRules.style.length; i++) {
    const prop = cssRules.style[i];
    styleObj[prop] = cssRules.style.getPropertyValue(prop).trim();
  }
  
  return styleObj;
};

/**
 * Gets a token value for the current theme
 * @param tokenName Token name including the -- prefix
 * @returns The value of the token for the current theme
 */
export const getThemeAwareToken = (tokenName: string): string => {
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  return `var(${tokenName})`;
};

/**
 * Formats a token value based on its type
 * @param value Token value
 * @returns Formatted value
 */
export const formatTokenValue = (value: string): string => {
  // Try to detect colors and format them nicely
  if (value.startsWith('#') || value.startsWith('rgb') || value.startsWith('hsl')) {
    return value;
  }
  
  // Try to detect sizes
  if (value.endsWith('px') || value.endsWith('rem') || value.endsWith('em') || value.endsWith('%')) {
    return value;
  }
  
  // If it's a reference to another token, resolve it
  if (value.startsWith('var(--')) {
    const tokenName = value.substring(4, value.length - 1);
    return `${value} → ${getThemeAwareToken(tokenName)}`;
  }
  
  return value;
};

/**
 * Checks if the token is a valid CSS variable from compiled-tokens.css
 * @param tokenName Token name
 * @returns True if valid token
 */
export const isValidToken = (tokenName: string): boolean => {
  // Only check cache for the current theme to avoid unnecessary computation
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const allTokens = getAllTokensForTheme(currentTheme as 'light' | 'dark');
  return tokenName.startsWith('--') && tokenName in allTokens;
};

/**
 * Gets all button-related tokens from compiled-tokens.css for current theme
 * @returns Array of button tokens
 */
export const getDynamicButtonTokens = (): TokenDefinition[] => {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const allTokens = getAllTokensForTheme(currentTheme as 'light' | 'dark');
  
  return Object.entries(allTokens)
    .filter(([key]) => key.includes('button') || 
                       (key.startsWith('--color-') && 
                        (key.includes('-primary-') || 
                         key.includes('-brand-') || 
                         key.includes('-secondary-') || 
                         key.includes('-danger-') || 
                         key.includes('-warning-') || 
                         key.includes('-success-'))))
    .map(([key, value]) => {
      // Try to determine usage based on the token name
      let usage = '';
      if (key.includes('radius')) usage = 'Border radius';
      else if (key.includes('gap')) usage = 'Spacing between elements';
      else if (key.includes('padding')) usage = 'Internal spacing';
      else if (key.includes('text-color') || key.includes('color-text')) usage = 'Text color';
      else if (key.includes('fill')) usage = 'Background color';
      else if (key.includes('border')) usage = 'Border color';
      else usage = 'Button style token';
      
      return {
        name: key,
        value: formatTokenValue(value),
        usage
      };
    });
};

/**
 * Returns tokens relevant to a specific button state
 * @param state Button state (rest, hover, press, focus, disabled)
 * @returns Array of tokens for the specified state
 */
export const getButtonStateTokens = (state: string): TokenDefinition[] => {
  const allTokens = getDynamicButtonTokens();
  return allTokens.filter(token => token.name.includes(`-${state}`));
};

/**
 * Returns tokens relevant to a specific button variant
 * @param variant Button variant
 * @returns Array of tokens for the specified variant
 */
export const getButtonVariantTokens = (variant: string): TokenDefinition[] => {
  const allTokens = getDynamicButtonTokens();
  return allTokens.filter(token => {
    // Map 'primary' to 'brand' for some token types
    const searchVariant = variant === 'primary' ? 
      (token.name.includes('fill-') || token.name.includes('border-') ? 'brand' : 'primary') 
      : variant;
    
    return token.name.includes(`-${searchVariant}-`);
  });
};

/**
 * Returns tokens relevant to a specific button size
 * @param size Button size (sm, md, lg, xl)
 * @returns Array of tokens for the specified size
 */
export const getButtonSizeTokensBySize = (size: string): TokenDefinition[] => {
  const sizeSuffix = size === 'sm' ? '-s' : 
                     size === 'md' ? '-m' : 
                     size === 'lg' ? '-l' : 
                     size === 'xl' ? '-xl' : '';
  
  const allTokens = getDynamicButtonTokens();
  return allTokens.filter(token => 
    (token.name.includes('padding') || token.name.includes('height') || token.name.includes('width')) 
    && token.name.endsWith(sizeSuffix)
  );
};

/**
 * Watch for theme changes in the document
 * @param callback Function to call when theme changes
 * @returns Cleanup function
 */
export function watchThemeChanges(callback: (theme: string) => void): () => void {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'data-theme') {
        const theme = document.documentElement.getAttribute('data-theme') || 'light';
        callback(theme);
      }
    });
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme'],
  });

  return () => observer.disconnect();
} 