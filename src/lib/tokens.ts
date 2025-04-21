/**
 * Utility functions for accessing semantic design tokens across components
 */

// Common token prefixes
export const TOKEN_TYPES = {
  // Color tokens
  COLOR_TEXT: 'color-text',
  COLOR_FILL: 'color-fill',
  COLOR_BORDER: 'color-border',
  COLOR_ICON: 'color-icon',
  COLOR_SURFACE: 'color-surface',
  
  // Component-specific tokens
  COMP_BUTTON: '--comp-button',
  COMP_CARD: '--comp-card',
  COMP_INPUT: '--comp-input',
  COMP_MODAL: '--comp-modal',
  COMP_BADGE: '--comp-badge',
} as const;

// Common token states
export const TOKEN_STATES = {
  REST: 'rest',
  HOVER: 'hover',
  PRESS: 'press',
  FOCUS: 'focus',
  DISABLED: 'disabled'
} as const;

// Component token category mapping
export const COMPONENT_TOKEN_CATEGORIES = {
  FILL: 'fill',
  TEXT: 'text-color',
  BORDER: 'border-color',
  RADIUS: 'radius',
  GAP: 'gap',
  PADDING: 'padding',
  HEIGHT: 'height',
  WIDTH: 'width',
  TRANSITION: 'transition',
  FOCUS: 'focus',
  TEXT_SIZE: 'text-size',
  TEXT_WEIGHT: 'text-weight'
} as const;

export interface TokenDefinition {
  name: string;
  value: string;
  usage?: string;
}

/**
 * Create a style object usable in Vue components using semantic tokens
 * @param tokens Token definitions or style mappings
 * @returns Style object for binding in Vue templates
 */
export function createTokenStyles(tokens: TokenDefinition[] | Record<string, string>): Record<string, string> {
  if (Array.isArray(tokens)) {
    return tokens.reduce((styles, token) => {
      styles[token.name] = token.value;
      return styles;
    }, {} as Record<string, string>);
  }
  
  const result: Record<string, string> = {};
  for (const [property, tokenName] of Object.entries(tokens)) {
    result[property] = `var(--${tokenName})`;
  }
  return result;
}

/**
 * Get a CSS variable value from the current document
 * @param name CSS variable name (without the --) 
 * @returns The value of the CSS variable
 */
export function getCssVar(name: string): string {
  return getComputedStyle(document.documentElement).getPropertyValue(`--${name}`);
}

/**
 * Build a semantic token name with proper format
 * @param type Token type (e.g. COLOR_TEXT)
 * @param name Token name (e.g. 'primary')
 * @param state Token state (e.g. 'rest', 'hover')
 * @returns Formatted token name
 */
export function buildTokenName(
  type: typeof TOKEN_TYPES[keyof typeof TOKEN_TYPES], 
  name: string, 
  state: typeof TOKEN_STATES[keyof typeof TOKEN_STATES] = TOKEN_STATES.REST
): string {
  return `${type}-${name}-${state}`;
}

/**
 * Get all available tokens of a specific component
 * @param componentPrefix Component prefix (e.g. 'comp-button')
 * @returns Array of token names
 */
export function getComponentTokens(componentPrefix: string): string[] {
  const tokens: string[] = [];
  const styles = getComputedStyle(document.documentElement);
  
  for (let i = 0; i < styles.length; i++) {
    const prop = styles[i];
    if (prop.startsWith(`--${componentPrefix}`)) {
      tokens.push(prop.substring(2)); // Remove the -- prefix
    }
  }
  
  return tokens;
}

/**
 * Get specific token types for a component
 * @param componentPrefix Component prefix (e.g. 'comp-button')
 * @param category Token category (e.g. 'fill', 'text-color')
 * @returns Array of token names matching the category
 */
export function getComponentTokensByCategory(
  componentPrefix: string,
  category: typeof COMPONENT_TOKEN_CATEGORIES[keyof typeof COMPONENT_TOKEN_CATEGORIES]
): string[] {
  return getComponentTokens(componentPrefix).filter(token => token.includes(category));
}

/**
 * Watch for theme changes in the document root
 * @param callback Function to call when theme changes
 * @returns Cleanup function
 */
export function watchThemeChanges(callback: () => void): () => void {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === 'attributes' &&
        mutation.attributeName === 'data-theme'
      ) {
        callback();
      }
    });
  });

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['data-theme']
  });

  return () => observer.disconnect();
}

/**
 * Get a theme-aware token value
 * @param tokenName Token name
 * @returns Theme-aware token value
 */
export function getThemeAwareToken(tokenName: string): string {
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  return `var(${tokenName})`;
} 