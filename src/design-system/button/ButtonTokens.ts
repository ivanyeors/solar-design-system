// Button Token Definitions
export interface TokenDefinition {
  name: string;
  value: string;
  usage: string;
}

// Common Button Tokens
export const getCommonButtonTokens = (): TokenDefinition[] => {
  return [
    {
      name: '--comp-button-main-radius',
      value: '0.375rem',
      usage: 'Border radius for buttons'
    },
    {
      name: '--comp-button-main-gap',
      value: '0.5rem',
      usage: 'Gap between button elements (like text and icons)'
    },
    {
      name: '--comp-button-main-transition',
      value: 'all 0.2s ease',
      usage: 'Transition for button interactions'
    }
  ];
};

// Size Tokens
export const getButtonSizeTokensBySize = (size: string): TokenDefinition[] => {
  const sizeTokens: Record<string, TokenDefinition[]> = {
    sm: [
      {
        name: '--comp-button-main-h-padding-s',
        value: '0.75rem',
        usage: 'Horizontal padding for small buttons'
      },
      {
        name: '--comp-button-main-v-padding-s',
        value: '0.375rem',
        usage: 'Vertical padding for small buttons'
      },
      {
        name: '--comp-button-main-font-size-s',
        value: '0.875rem',
        usage: 'Font size for small buttons'
      }
    ],
    md: [
      {
        name: '--comp-button-main-h-padding-m',
        value: '1rem',
        usage: 'Horizontal padding for medium buttons'
      },
      {
        name: '--comp-button-main-v-padding-m',
        value: '0.5rem',
        usage: 'Vertical padding for medium buttons'
      },
      {
        name: '--comp-button-main-font-size-m',
        value: '1rem',
        usage: 'Font size for medium buttons'
      }
    ],
    lg: [
      {
        name: '--comp-button-main-h-padding-l',
        value: '1.25rem',
        usage: 'Horizontal padding for large buttons'
      },
      {
        name: '--comp-button-main-v-padding-l',
        value: '0.625rem',
        usage: 'Vertical padding for large buttons'
      },
      {
        name: '--comp-button-main-font-size-l',
        value: '1.125rem',
        usage: 'Font size for large buttons'
      }
    ],
    xl: [
      {
        name: '--comp-button-main-h-padding-xl',
        value: '1.5rem',
        usage: 'Horizontal padding for extra large buttons'
      },
      {
        name: '--comp-button-main-v-padding-xl',
        value: '0.75rem',
        usage: 'Vertical padding for extra large buttons'
      },
      {
        name: '--comp-button-main-font-size-xl',
        value: '1.25rem',
        usage: 'Font size for extra large buttons'
      }
    ]
  };

  return sizeTokens[size] || [];
};

// State Tokens
export const getButtonStateTokens = (state: string): TokenDefinition[] => {
  const stateTokens: Record<string, TokenDefinition[]> = {
    rest: [
      {
        name: '--comp-button-main-opacity-rest',
        value: '1',
        usage: 'Opacity for button in rest state'
      }
    ],
    hover: [
      {
        name: '--comp-button-main-opacity-hover',
        value: '0.9',
        usage: 'Opacity for button in hover state'
      }
    ],
    press: [
      {
        name: '--comp-button-main-opacity-press',
        value: '0.8',
        usage: 'Opacity for button in pressed state'
      }
    ],
    focus: [
      {
        name: '--comp-button-main-outline-width-focus',
        value: '2px',
        usage: 'Outline width for button in focus state'
      },
      {
        name: '--comp-button-main-outline-offset-focus',
        value: '2px',
        usage: 'Outline offset for button in focus state'
      }
    ],
    disabled: [
      {
        name: '--comp-button-main-opacity-disabled',
        value: '0.5',
        usage: 'Opacity for button in disabled state'
      }
    ]
  };

  return stateTokens[state] || [];
};

// Variant Tokens
export const getButtonVariantTokens = (variant: string): TokenDefinition[] => {
  const variantTokens: Record<string, TokenDefinition[]> = {
    primary: [
      {
        name: '--comp-button-main-bg-primary',
        value: 'var(--color-fill-brand-rest)',
        usage: 'Background color for primary button'
      },
      {
        name: '--comp-button-main-text-primary',
        value: 'var(--color-text-neutrallight-rest)',
        usage: 'Text color for primary button'
      },
      {
        name: '--comp-button-main-border-primary',
        value: 'var(--color-border-brand-rest)',
        usage: 'Border color for primary button'
      }
    ],
    secondary: [
      {
        name: '--comp-button-main-bg-secondary',
        value: 'var(--color-surface-secondary-rest)',
        usage: 'Background color for secondary button'
      },
      {
        name: '--comp-button-main-text-secondary',
        value: 'var(--color-text-primary-rest)',
        usage: 'Text color for secondary button'
      },
      {
        name: '--comp-button-main-border-secondary',
        value: 'var(--color-border-primary-rest)',
        usage: 'Border color for secondary button'
      }
    ],
    outline: [
      {
        name: '--comp-button-main-bg-outline',
        value: 'transparent',
        usage: 'Background color for outline button'
      },
      {
        name: '--comp-button-main-text-outline',
        value: 'var(--color-text-primary-rest)',
        usage: 'Text color for outline button'
      },
      {
        name: '--comp-button-main-border-outline',
        value: 'var(--color-border-primary-rest)',
        usage: 'Border color for outline button'
      }
    ],
    ghost: [
      {
        name: '--comp-button-main-bg-ghost',
        value: 'transparent',
        usage: 'Background color for ghost button'
      },
      {
        name: '--comp-button-main-text-ghost',
        value: 'var(--color-text-primary-rest)',
        usage: 'Text color for ghost button'
      },
      {
        name: '--comp-button-main-border-ghost',
        value: 'transparent',
        usage: 'Border color for ghost button'
      }
    ]
  };

  return variantTokens[variant] || [];
};

// Component-specific Button Tokens
export const getComponentButtonTokens = (): TokenDefinition[] => {
  return [
    {
      name: '--comp-button-main-font-weight',
      value: 'var(--font-weight-medium-500)',
      usage: 'Font weight for buttons'
    },
    {
      name: '--comp-button-main-line-height',
      value: '1.5',
      usage: 'Line height for buttons'
    },
    {
      name: '--comp-button-main-focus-ring-color',
      value: 'var(--color-border-brand-focus)',
      usage: 'Focus ring color for buttons'
    }
  ];
};

// Helper function to get theme-aware token values
export const getThemeAwareToken = (tokenName: string): string => {
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  // This is a placeholder implementation
  // In a real app, you'd have a more sophisticated way to determine theme-aware values
  return `var(${tokenName})`;
};

// Function to get all tokens for the current theme
export const getAllTokensForTheme = (): TokenDefinition[] => {
  const commonTokens = getCommonButtonTokens();
  const sizeTokens = [
    ...getButtonSizeTokensBySize('sm'),
    ...getButtonSizeTokensBySize('md'),
    ...getButtonSizeTokensBySize('lg'),
    ...getButtonSizeTokensBySize('xl')
  ];
  const stateTokens = [
    ...getButtonStateTokens('rest'),
    ...getButtonStateTokens('hover'),
    ...getButtonStateTokens('press'),
    ...getButtonStateTokens('focus'),
    ...getButtonStateTokens('disabled')
  ];
  const variantTokens = [
    ...getButtonVariantTokens('primary'),
    ...getButtonVariantTokens('secondary'),
    ...getButtonVariantTokens('outline'),
    ...getButtonVariantTokens('ghost')
  ];
  const componentTokens = getComponentButtonTokens();

  return [...commonTokens, ...sizeTokens, ...stateTokens, ...variantTokens, ...componentTokens];
};

// Utility to watch for theme changes
export const watchThemeChanges = (callback: () => void): (() => void) => {
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

  // Return cleanup function
  return () => observer.disconnect();
}; 