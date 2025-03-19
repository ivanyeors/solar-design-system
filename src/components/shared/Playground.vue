<script lang="ts">
// Component registry for dynamic loading
const componentRegistry = {
  button: {
    name: 'Button',
    defaultProps: {
      size: 'sm',
      variant: 'primary',
      state: 'rest'
    },
    variants: [
      { value: 'primary', label: 'Primary' },
      { value: 'secondary', label: 'Secondary' },
      { value: 'outline', label: 'Outline' },
      { value: 'ghost', label: 'Ghost' },
      { value: 'danger', label: 'Danger' },
      { value: 'warning', label: 'Warning' },
      { value: 'success', label: 'Success' },
    ],
    sizes: [
      { value: 'sm', label: 'Small' },
      { value: 'md', label: 'Medium' },
      { value: 'lg', label: 'Large' },
      { value: 'xl', label: 'Extra Large' }
    ],
    states: [
      { value: 'rest', label: 'Rest' },
      { value: 'hover', label: 'Hover' },
      { value: 'press', label: 'Press' },
      { value: 'focus', label: 'Focus' },
      { value: 'disabled', label: 'Disabled' },
      { value: 'loading', label: 'Loading' }
    ],
    supportIcons: true,
    tokenGetters: {}
  },
  badge: {
    name: 'Badge',
    defaultProps: {
      variant: 'primary',
      state: 'rest'
    },
    variants: [
      { value: 'primary', label: 'Primary' },
      { value: 'secondary', label: 'Secondary' },
      { value: 'error', label: 'Error' },
      { value: 'success', label: 'Success' },
      { value: 'warning', label: 'Warning' },
      { value: 'info', label: 'Info' }
    ],
    states: [
      { value: 'rest', label: 'Rest' },
      { value: 'hover', label: 'Hover' },
      { value: 'disabled', label: 'Disabled' }
    ],
    sizes: [],
    supportIcons: false,
    tokenGetters: {}
  }
};

// Define the valid component types
const VALID_COMPONENT_TYPES = Object.keys(componentRegistry);
</script>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, defineAsyncComponent, shallowRef } from 'vue';
import { 
  TokenDefinition, 
  getComponentButtonTokens, 
  getButtonSizeTokensBySize, 
  getButtonStateTokens, 
  getButtonVariantTokens,
  getCommonButtonTokens,
  getAllTokensForTheme,
  watchThemeChanges,
  getThemeAwareToken
} from '../../utils/tokenUtils';
import { ButtonMain as Button } from '@/design-system/button';
import "@/style.css";

// Try to dynamically import Badge component (if it exists)
let Badge;
try {
  const badgeModule = import('@/design-system/badge');
  Badge = defineAsyncComponent(() => badgeModule.then(m => m.Badge));
} catch (e) {
  console.warn('Badge component not available:', e);
}

// Update component registry with actual components
const registryWithComponents = {
  ...componentRegistry,
  button: {
    ...componentRegistry.button,
    component: Button
  }
};

// Add Badge component to registry if available
if (Badge) {
  registryWithComponents.badge = {
    ...componentRegistry.badge,
    component: Badge
  };
}

interface Option {
  value: string;
  label: string;
}

interface TokenValues {
  padding: string;
  fontSize: string;
  brand: string;
  colorMode: string;
  tokenColor: string;
}

const props = defineProps({
  title: {
    type: String,
    default: 'component-v1.0.0'
  },
  componentType: {
    type: String,
    default: 'button',
    validator: (value: string) => VALID_COMPONENT_TYPES.includes(value)
  },
  currentSize: {
    type: String,
    default: 'sm'
  },
  currentState: {
    type: String,
    default: 'rest'
  },
  currentType: {
    type: String,
    default: 'primary'
  },
  showLabel: {
    type: Boolean,
    default: true
  },
  labelText: {
    type: String,
    default: 'Button Label'
  },
  showLeadingIcon: {
    type: Boolean,
    default: false
  },
  showTrailingIcon: {
    type: Boolean,
    default: false
  },
  sizeOptions: {
    type: Array as () => Option[],
    default: () => []
  },
  stateOptions: {
    type: Array as () => Option[],
    default: () => []
  },
  typeOptions: {
    type: Array as () => Option[],
    default: () => [
      { value: 'primary', label: 'Primary' },
      { value: 'secondary', label: 'Secondary' },
      { value: 'outline', label: 'Outline' },
      { value: 'ghost', label: 'Ghost' },
      { value: 'danger', label: 'Danger' },
      { value: 'warning', label: 'Warning' },
      { value: 'success', label: 'Success' },
    ]
  },
  tokens: {
    type: Array as () => TokenDefinition[],
    default: () => []
  },
  variant: {
    type: String,
    default: ''
  },
  showCommonTokens: {
    type: Boolean,
    default: true
  },
  showSizeTokens: {
    type: Boolean,
    default: true
  },
  tokenValues: {
    type: Object as () => TokenValues,
    default: () => ({
      padding: '0.5rem 1rem',
      fontSize: '0.875rem',
      brand: 'Auto (Default)',
      colorMode: 'Auto (Light/Dark)',
      tokenColor: 'Auto (Default)'
    })
  }
});

const emit = defineEmits(['update:config', 'update:tokenValues']);

const copiedToken = ref<string | null>(null);
const activeTab = ref<'config' | 'tokens'>('config');
const showToast = ref(false);
const toastMessage = ref('');
const currentTheme = ref(document.documentElement.getAttribute('data-theme') || 'light');

const updateConfig = (key: string, value: any) => {
  emit('update:config', key, value);
};

// Compute dynamic styles for the preview component
const componentStyles = computed(() => {
  if (props.componentType === 'button') {
    return {
      '--button-background': currentTokenValues.value.background,
      '--button-text': currentTokenValues.value.text,
      '--button-border': currentTokenValues.value.border,
      '--button-icon': currentTokenValues.value.icon,
      '--button-outline': currentTokenValues.value.outline,
      '--button-surface': currentTokenValues.value.surface,
      '--button-surface-hover': currentTokenValues.value.surfaceHover,
      '--button-surface-press': currentTokenValues.value.surfacePress,
      '--button-transition': 'all 0.2s ease-in-out'
    };
  } else if (props.componentType === 'badge') {
    return {
      '--badge-background': currentTokenValues.value.background,
      '--badge-text': currentTokenValues.value.text,
      '--badge-border': currentTokenValues.value.border,
      '--badge-transition': 'all 0.2s ease-in-out'
    };
  }
  
  // Default empty styles
  return {};
});

// Function to copy component code
const copyComponentCode = () => {
  // Prepare formatted code for the current component configuration
  let code;
  
  if (props.componentType === 'button') {
    code = `<Button
  size="${props.currentSize}"
  variant="${props.currentType}"
  ${props.currentState === 'disabled' ? 'disabled' : ''}
  ${props.currentState === 'loading' ? 'loading' : ''}
>
  ${props.showLeadingIcon ? '<template #leading-icon><i class="icon-mail"></i></template>' : ''}
  ${props.showLabel ? props.labelText : ''}
  ${props.showTrailingIcon ? '<template #trailing-icon><i class="icon-arrow-right"></i></template>' : ''}
</Button>`;
  } else if (props.componentType === 'badge') {
    code = `<Badge
  variant="${props.currentType}"
  ${props.currentState === 'disabled' ? 'disabled' : ''}
>
  ${props.showLabel ? props.labelText : ''}
</Badge>`;
  } else {
    // Generic component code
    code = `<${activeComponent.value.name}
  variant="${props.currentType}"
  ${props.currentState === 'disabled' ? 'disabled' : ''}
>
  ${props.showLabel ? props.labelText : ''}
</${activeComponent.value.name}>`;
  }

  // Copy to clipboard
  navigator.clipboard.writeText(code)
    .then(() => {
      toastMessage.value = 'Component code copied to clipboard';
      showToast.value = true;
      setTimeout(() => {
        showToast.value = false;
      }, 2000);
    })
    .catch(err => {
      console.error('Failed to copy code:', err);
      toastMessage.value = 'Failed to copy code';
      showToast.value = true;
      setTimeout(() => {
        showToast.value = false;
      }, 2000);
    });
};

const copyToClipboard = async (token: TokenDefinition) => {
  try {
    // Copy either the token name (for CSS variables) or the value
    const textToCopy = token.name.startsWith('--') || token.name.startsWith('var(--') 
      ? token.name 
      : token.value;
    
    await navigator.clipboard.writeText(textToCopy);
    copiedToken.value = token.name;
    toastMessage.value = `Token copied: ${textToCopy}`;
    showToast.value = true;
    setTimeout(() => {
      copiedToken.value = null;
      showToast.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};

// Add size suffix mapping
const sizeSuffixMap = {
  'sm': '-s',
  'md': '-m',
  'lg': '-l',
  'xl': '-xl'
} as const;

// Dynamic token retrieval functions
const getThemeAwareTokenValue = (type: string, variant: string, state: string) => {
  const theme = document.documentElement.getAttribute('data-theme') || 'light';
  const isDefaultState = state === 'rest';
  
  // Handle special cases for primary variant
  if (variant === 'primary') {
    if (type === 'text') {
      return `var(--color-text-neutrallight-${state})`;
    }
    if (type === 'fill') {
      return `var(--color-fill-brand-${state})`;
    }
    if (type === 'border') {
      return `var(--color-border-brand-${state})`;
    }
  }

  // Handle ghost variant special cases
  if (variant === 'ghost') {
    if (type === 'fill' && isDefaultState) {
      return 'transparent';
    }
    if (type === 'border') {
      return 'transparent';
    }
    if (type === 'surface' && state === 'hover') {
      return `var(--comp-button-main-ghost-fill-press)`;
    }
  }

  // Handle outline variant special cases
  if (variant === 'outline' && type === 'fill' && isDefaultState) {
    return 'transparent';
  }

  // Handle secondary variant special cases
  if (variant === 'secondary') {
    if (type === 'fill') {
      return `var(--comp-button-main-fill-${state}-sec)`;
    }
    if (type === 'text' && isDefaultState) {
      return `var(--comp-button-main-text-color-fill-sec)`;
    }
  }

  // Default token mapping
  const tokenMap = {
    fill: `var(--color-fill-${variant}-${state})`,
    text: `var(--color-text-primary-${state})`,
    border: `var(--color-border-${variant}-${state})`,
    icon: `var(--color-icon-${variant}-${state})`,
    surface: `var(--color-surface-${variant}-${state})`
  };

  return tokenMap[type as keyof typeof tokenMap];
};

// Get active component config from registry
const activeComponent = computed(() => {
  return registryWithComponents[props.componentType as keyof typeof registryWithComponents] || registryWithComponents.button;
});

// Dynamic option getters based on active component
const sizeOptions = computed(() => activeComponent.value.sizes || []);
const stateOptions = computed(() => activeComponent.value.states || []);
const typeOptions = computed(() => activeComponent.value.variants || []);
const showIconOptions = computed(() => activeComponent.value.supportIcons);

// Collect tokens dynamically based on active component type
const dynamicCollectAllTokens = computed(() => {
  // If current component has token getters, use them
  const tokenGetters = activeComponent.value.tokenGetters || {};
  
  const commonTokens = tokenGetters.commonTokens ? tokenGetters.commonTokens() : [];
  const sizeTokens = tokenGetters.sizeTokens ? tokenGetters.sizeTokens(props.currentSize) : [];
  const stateTokens = tokenGetters.stateTokens ? tokenGetters.stateTokens(props.currentState) : [];
  const variantTokens = tokenGetters.variantTokens ? tokenGetters.variantTokens(props.currentType) : [];
  const componentTokens = tokenGetters.componentTokens ? tokenGetters.componentTokens() : [];

  // Combine all tokens and ensure they're unique
  const allTokens = [
    ...commonTokens, 
    ...sizeTokens, 
    ...stateTokens, 
    ...variantTokens,
    ...componentTokens
  ].reduce((unique: TokenDefinition[], token) => {
    if (!unique.some(t => t.name === token.name)) {
      unique.push(token);
    }
    return unique;
  }, []);

  return allTokens;
});

// Use dynamic token collection if available, otherwise fall back to the button-specific one
const collectAllTokens = computed(() => {
  if (props.componentType === 'button') {
    // Original button token logic
    const commonTokens = getCommonButtonTokens();
    const sizeTokens = getButtonSizeTokensBySize(props.currentSize);
    const stateTokens = getButtonStateTokens(props.currentState);
    const variantTokens = getButtonVariantTokens(props.currentType);
    const componentTokens = getComponentButtonTokens();

    // Combine all tokens and ensure they're unique
    const allTokens = [
      ...commonTokens, 
      ...sizeTokens, 
      ...stateTokens, 
      ...variantTokens,
      ...componentTokens
    ].reduce((unique: TokenDefinition[], token) => {
      if (!unique.some(t => t.name === token.name)) {
        unique.push(token);
      }
      return unique;
    }, []);

    return allTokens;
  }
  
  // For other components, use the dynamic approach
  return dynamicCollectAllTokens.value;
});

// Update the token filtering and display logic
const activeTokens = computed(() => {
  // Use both dynamically fetched tokens and any that were passed in as props
  const allTokens = [...collectAllTokens.value, ...props.tokens];
  const currentState = props.currentState;
  const currentType = props.currentType;
  const sizeSuffix = sizeSuffixMap[props.currentSize as keyof typeof sizeSuffixMap];

  const filteredTokens = allTokens.filter(token => {
    // Skip tokens without a name
    if (!token.name) return false;

    // Always show token-code entries
    if (token.name.includes('token-code')) {
      return true;
    }

    // Filter size-specific tokens
    if (token.name.includes('padding') || token.name.includes('height') || token.name.includes('width')) {
      return token.name.endsWith(sizeSuffix);
    }

    // Filter state-specific tokens
    if (token.name.includes(currentState) || 
        (currentState === 'hover' && token.name.includes('-hover')) ||
        (currentState === 'press' && token.name.includes('-press')) ||
        (currentState === 'focus' && token.name.includes('-focus')) ||
        (currentState === 'disabled' && token.name.includes('-disabled'))) {
      return true;
    }

    // Filter variant-specific tokens
    if (currentType && (
        token.name.includes(`-${currentType}-`) ||
        token.name.includes(`-${currentType}.`) ||
        token.name.includes(`${currentType}-`))) {
      return true;
    }

    // Keep common tokens that don't have size/state/variant variations
    if (token.name.includes('main') && 
        !token.name.includes('padding') && 
        !token.name.includes('height') && 
        !token.name.includes('width') &&
        !token.name.includes('hover') &&
        !token.name.includes('press') &&
        !token.name.includes('focus') &&
        !token.name.includes('disabled')) {
      return true;
    }

    return false;
  });

  // Update token values based on current theme
  for (const token of filteredTokens) {
    try {
      // Add default usage if missing
      if (!token.usage) {
        token.usage = 'Design token';
      }
      
      // Update token values with current theme values
      if (typeof token.name === 'string') {
        if (token.name.startsWith('--')) {
          token.value = getComputedStyle(document.documentElement).getPropertyValue(token.name).trim();
        } else if (token.name.startsWith('var(--')) {
          const tokenName = token.name.substring(4, token.name.length - 1);
          token.value = getComputedStyle(document.documentElement).getPropertyValue(tokenName).trim();
        }
      }
    } catch (err) {
      console.error(`Error updating token ${token.name}:`, err);
    }
  }

  return filteredTokens;
});

// Update the groupedTokens computed property
const groupedTokens = computed(() => {
  const groups: { [key: string]: TokenDefinition[] } = {
    common: [],
    sizes: [],
    states: [],
    variants: [],
    icons: []
  };

  const sizeSuffix = sizeSuffixMap[props.currentSize as keyof typeof sizeSuffixMap];

  activeTokens.value.forEach(token => {
    // Group icon tokens
    if (token.name.includes('icon')) {
      groups.icons.push(token);
    }
    // Group size-related tokens
    else if (token.name.includes('token-code') || 
        (token.name.includes('padding') && token.name.endsWith(sizeSuffix)) || 
        (token.name.includes('height') && token.name.endsWith(sizeSuffix)) || 
        (token.name.includes('width') && token.name.endsWith(sizeSuffix))) {
      groups.sizes.push(token);
    }
    // Group state-related tokens
    else if (token.name.includes(props.currentState) || 
             token.name.includes('hover') || 
             token.name.includes('press') || 
             token.name.includes('focus') || 
             token.name.includes('disabled')) {
      groups.states.push(token);
    }
    // Group variant-specific tokens
    else if (token.name.includes(props.currentType)) {
      groups.variants.push(token);
    }
    // Group common tokens
    else if (!token.name.includes('padding') && 
             !token.name.includes('height') && 
             !token.name.includes('width')) {
      groups.common.push(token);
    }
  });

  // Sort tokens within groups
  Object.keys(groups).forEach(groupKey => {
    groups[groupKey].sort((a, b) => {
      // Keep token-code at the top
      if (a.name.includes('token-code')) return -1;
      if (b.name.includes('token-code')) return 1;

      // Sort by token type
      const typeOrder = ['padding', 'height', 'width', 'icon', 'text', 'background', 'border'];
      const aType = typeOrder.find(type => a.name.includes(type)) || '';
      const bType = typeOrder.find(type => b.name.includes(type)) || '';
      
      if (aType !== bType) {
        return typeOrder.indexOf(aType) - typeOrder.indexOf(bType);
      }

      // Sort by state for state tokens
      if (groupKey === 'states') {
        const stateOrder = ['rest', 'hover', 'press', 'focus', 'disabled'];
        const aState = stateOrder.find(state => a.name.includes(state)) || '';
        const bState = stateOrder.find(state => b.name.includes(state)) || '';
        if (aState !== bState) {
          return stateOrder.indexOf(aState) - stateOrder.indexOf(bState);
        }
      }

      return a.name.localeCompare(b.name);
    });
  });

  return groups;
});

// Update the token group display logic
const shouldShowTokenGroup = (groupName: string) => {
  if (groupName === 'common' && props.showCommonTokens) return true;
  if (groupName === 'sizes' && props.showSizeTokens) return true;
  if (['states', 'variants', 'icons'].includes(groupName)) return true;
  return false;
};

// Update the token group title
const getTokenGroupTitle = (groupName: string) => {
  const themeLabel = currentTheme.value === 'dark' ? '(Dark)' : '(Light)';
  
  switch (groupName) {
    case 'common':
      return `Common Tokens ${themeLabel}`;
    case 'sizes':
      return `Size Tokens (${props.currentSize.toUpperCase()})`;
    case 'states':
      return `State Tokens (${props.currentState})`;
    case 'variants':
      return `${props.currentType.charAt(0).toUpperCase() + props.currentType.slice(1)} Variant Tokens`;
    case 'icons':
      return `Icon Tokens ${themeLabel}`;
    default:
      return groupName;
  }
};

// Update the currentTokenValues computed property
const currentTokenValues = computed(() => {
  const isDefaultState = props.currentState === 'rest';
  const currentType = props.currentType;

  return {
    padding: {
      sm: 'var(--comp-button-main-h-padding-s)',
      md: 'var(--comp-button-main-h-padding-m)',
      lg: 'var(--comp-button-main-h-padding-l)',
      xl: 'var(--comp-button-main-h-padding-xl)'
    }[props.currentSize],
    fontSize: {
      sm: 'var(--font-size-14)',
      md: 'var(--font-size-16)',
      lg: 'var(--font-size-18)',
      xl: 'var(--font-size-20)'
    }[props.currentSize],
    background: getThemeAwareTokenValue('fill', currentType, props.currentState),
    text: currentType === 'primary' 
      ? getThemeAwareTokenValue('text', 'neutrallight', props.currentState)
      : getThemeAwareTokenValue('text', currentType === 'secondary' && isDefaultState ? 'secondary' : 'primary', props.currentState),
    border: getThemeAwareTokenValue('border', currentType, props.currentState),
    icon: currentType === 'primary'
      ? getThemeAwareTokenValue('icon', 'primary-inverse', props.currentState)
      : getThemeAwareTokenValue('icon', currentType, props.currentState),
    outline: getThemeAwareTokenValue('border', currentType, 'focus'),
    surface: getThemeAwareTokenValue('surface', currentType, props.currentState),
    surfaceHover: getThemeAwareTokenValue('surface', currentType, 'hover'),
    surfacePress: getThemeAwareTokenValue('surface', currentType, 'press')
  };
});

// Add theme observer and force recomputation on theme changes
onMounted(() => {
  // Set up theme observer to refresh tokens when theme changes
  const cleanup = watchThemeChanges(() => {
    currentTheme.value = document.documentElement.getAttribute('data-theme') || 'light';
    
    // Force recomputation of token values and dynamic tokens
    activeTokens.value.forEach(token => {
      try {
        // Ensure token.value is updated with latest theme-aware value
        if (token.name.startsWith('--')) {
          token.value = getComputedStyle(document.documentElement).getPropertyValue(token.name).trim();
        } else if (token.name.startsWith('var(--')) {
          const tokenName = token.name.substring(4, token.name.length - 1);
          token.value = getComputedStyle(document.documentElement).getPropertyValue(tokenName).trim();
        }
      } catch (err) {
        console.error(`Error updating token ${token.name}:`, err);
      }
    });
    
    // Force recompute of token values for the preview
    emit('update:tokenValues', currentTokenValues.value);
    
    // Update preview styles
    updatePreviewStyles();
  });

  // Ensure the initial token values are set correctly
  updatePreviewStyles();

  return cleanup;
});

// Cleanup on component unmount
onUnmounted(() => {
  if (typeof cleanup === 'function') {
    cleanup();
  }
});

// Function to update preview styles directly
const updatePreviewStyles = () => {
  const previewButton = document.querySelector('.preview-button');
  if (previewButton) {
    previewButton.style.setProperty('--button-background', currentTokenValues.value.background);
    previewButton.style.setProperty('--button-text', currentTokenValues.value.text);
    previewButton.style.setProperty('--button-border', currentTokenValues.value.border);
    previewButton.style.setProperty('--button-icon', currentTokenValues.value.icon);
    previewButton.style.setProperty('--button-outline', currentTokenValues.value.outline);
    previewButton.style.setProperty('--button-surface', currentTokenValues.value.surface);
    previewButton.style.setProperty('--button-surface-hover', currentTokenValues.value.surfaceHover);
    previewButton.style.setProperty('--button-surface-press', currentTokenValues.value.surfacePress);
  }
};

// Add watchers for state changes
watch([() => props.currentSize, () => props.currentState, () => props.currentType], 
  ([size, state, type]) => {
    // Emit token values update
    emit('update:tokenValues', currentTokenValues.value);
    
    // Update preview styles
    updatePreviewStyles();
  },
  { immediate: true }
);

// Function to get the actual color value for token preview
const getTokenColorValue = (token: TokenDefinition): string => {
  if (!token.value) return 'transparent';
  
  // If the value is a CSS variable reference
  if (token.value.startsWith('var(--')) {
    try {
      // Extract the variable name and get its computed value
      const varName = token.value.match(/var\((--[^)]+)\)/)?.[1];
      if (varName) {
        return getComputedStyle(document.documentElement).getPropertyValue(varName).trim() || 'transparent';
      }
    } catch (e) {
      console.error('Error getting token color:', e);
    }
    return 'transparent';
  }
  
  // If the value is a direct color value (e.g., #fff, rgb(255,255,255))
  if (/^(#|rgb|hsl)/.test(token.value)) {
    return token.value;
  }
  
  return 'transparent';
};

// Function to format token value for display
const formatTokenValue = (token: TokenDefinition): string => {
  if (!token.value) return '';
  
  // Handle case when token value might be an object or array
  if (typeof token.value !== 'string') {
    try {
      return JSON.stringify(token.value);
    } catch {
      return String(token.value);
    }
  }
  
  // If it's a reference to another token, try to resolve it for display
  if (token.value.startsWith('var(--')) {
    try {
      const varName = token.value.match(/var\((--[^)]+)\)/)?.[1];
      if (varName) {
        const resolvedValue = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
        if (resolvedValue) {
          return `${token.value} → ${resolvedValue}`;
        }
      }
    } catch (e) {
      console.error('Error formatting token value:', e);
    }
  }
  
  return token.value;
};

// Reset component to default settings
const resetToDefaults = () => {
  const defaults = activeComponent.value.defaultProps || {};
  
  if (defaults.size) emit('update:config', 'size', defaults.size);
  if (defaults.state) emit('update:config', 'state', defaults.state);
  if (defaults.variant) emit('update:config', 'type', defaults.variant);
  
  emit('update:config', 'showLabel', true);
  
  if (activeComponent.value.supportIcons) {
    emit('update:config', 'showLeadingIcon', false);
    emit('update:config', 'showTrailingIcon', false);
  }
  
  emit('update:config', 'label', `${activeComponent.value.name} Label`);
  
  // Show toast notification
  toastMessage.value = 'Reset to defaults';
  showToast.value = true;
  setTimeout(() => {
    showToast.value = false;
  }, 2000);
};
</script>

<template>
  <div class="playground">
    <!-- Toast Notification -->
    <div 
      v-if="showToast" 
      class="toast-notification"
      :class="{ 'toast-notification--show': showToast }"
    >
      {{ toastMessage }}
    </div>

    <!-- Header -->
    <div class="playground-header">
      <div class="icon-group">
        <button class="icon-button" aria-label="Copy component code" @click="copyComponentCode">
          <i class="icon-copy"></i>
        </button>
        <button class="icon-button" aria-label="Reset to defaults" @click="resetToDefaults">
          <i class="icon-refresh"></i>
        </button>
      </div>
    </div>

    <!-- Preview and Config Container -->
    <div class="preview-config-container">
      <!-- Preview Section -->
      <div class="preview-section">
        <div class="preview-area">
          <!-- Dynamic component rendering based on componentType -->
          <component 
            :is="activeComponent.component"
            :size="componentType === 'button' ? currentSize : undefined"
            :variant="currentType"
            :disabled="currentState === 'disabled'"
            :loading="currentState === 'loading'"
            class="preview-component"
            :class="[
              `${componentType}-${currentType}`,
              componentType === 'button' ? `${componentType}-${currentSize}` : '',
              {
                'hover': currentState === 'hover',
                'active': currentState === 'press',
                'focus': currentState === 'focus',
                'disabled': currentState === 'disabled'
              }
            ]"
            :style="componentStyles"
          >
            <template v-if="showLeadingIcon && showIconOptions" #leading-icon>
              <i class="icon-mail" :style="{ color: 'var(--button-icon)' }"></i>
            </template>
            <span v-if="showLabel">{{ labelText }}</span>
            <template v-if="showTrailingIcon && showIconOptions" #trailing-icon>
              <i class="icon-arrow-right" :style="{ color: 'var(--button-icon)' }"></i>
            </template>
          </component>
        </div>
      </div>

      <!-- Config Section -->
      <div class="config-section">
        <h4 class="panel-title">Configuration</h4>
        <div class="config-controls">
          <!-- Size controls - only shown for components with size options -->
          <div class="control-group" v-if="sizeOptions.length > 0">
            <label class="control-label">Size</label>
            <div class="control-options">
              <button 
                v-for="option in sizeOptions" 
                :key="option.value"
                class="control-button"
                :class="{ 'control-button--selected': currentSize === option.value }"
                @click="updateConfig('size', option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- State controls -->
          <div class="control-group">
            <label class="control-label">State</label>
            <div class="control-options control-options--wrap">
              <button 
                v-for="option in stateOptions" 
                :key="option.value"
                class="control-button"
                :class="{ 'control-button--selected': currentState === option.value }"
                @click="updateConfig('state', option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- Type/Variant controls -->
          <div class="control-group">
            <label class="control-label">Type</label>
            <div class="control-options control-options--wrap">
              <button 
                v-for="option in typeOptions" 
                :key="option.value"
                class="control-button"
                :class="{ 'control-button--selected': currentType === option.value }"
                @click="updateConfig('type', option.value)"
              >
                {{ option.label }}
              </button>
            </div>
          </div>

          <!-- Label controls -->
          <div class="control-group">
            <div class="control-row">
              <label class="control-label">Show Label</label>
              <button 
                class="toggle-switch" 
                :class="{ 'toggle-switch--active': showLabel }"
                @click="updateConfig('showLabel', !showLabel)"
              >
                <span class="toggle-switch__handle"></span>
              </button>
            </div>
            <input 
              v-if="showLabel"
              :value="labelText"
              @input="updateConfig('label', ($event.target as HTMLInputElement).value)"
              class="config-input" 
              placeholder="Button Label"
            >
          </div>

          <!-- Icon controls - only shown for components that support icons -->
          <div class="control-group" v-if="showIconOptions">
            <div class="control-row">
              <label class="control-label">Show Leading Icon</label>
              <button 
                class="toggle-switch" 
                :class="{ 'toggle-switch--active': showLeadingIcon }"
                @click="updateConfig('showLeadingIcon', !showLeadingIcon)"
              >
                <span class="toggle-switch__handle"></span>
              </button>
            </div>
            <div class="control-row">
              <label class="control-label">Show Trailing Icon</label>
              <button 
                class="toggle-switch" 
                :class="{ 'toggle-switch--active': showTrailingIcon }"
                @click="updateConfig('showTrailingIcon', !showTrailingIcon)"
              >
                <span class="toggle-switch__handle"></span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Design Tokens Section -->
    <div class="tokens-panel">
      <h4 class="panel-title">Design Tokens</h4>
      <div class="tokens-section">
        <div class="token-table-wrapper">
          <table class="token-table">
            <thead class="token-table-header">
              <tr>
                <th class="token-table-th">Token</th>
                <th class="token-table-th">Value</th>
                <th class="token-table-th">Usage</th>
              </tr>
            </thead>
            <tbody class="token-table-body">
              <template v-for="(group, groupName) in groupedTokens" :key="groupName">
                <tr v-if="shouldShowTokenGroup(groupName)" class="token-group-row">
                  <td colspan="3" class="token-group-header">
                    <div class="token-group-title">
                      {{ getTokenGroupTitle(groupName) }}
                      <span v-if="groupName === 'states' || groupName === 'variants'" class="token-variant-label">
                        {{ currentType }}/{{ currentState }}
                      </span>
                    </div>
                  </td>
                </tr>
                <template v-for="token in group" :key="token.name">
                  <tr v-if="shouldShowTokenGroup(groupName)"
                    @click="copyToClipboard(token)"
                    class="token-row"
                    :class="{
                      'active-token': token.name.includes(currentState),
                      'token-code-row': token.name.includes('token-code'),
                      'variant-token': token.name.includes(currentType),
                      'state-token': token.name.includes(currentState),
                      'size-token': componentType === 'button' && token.name.endsWith(sizeSuffixMap[currentSize])
                    }"
                  >
                    <td class="token-table-td token-name-cell">
                      <div class="token-name-container">
                        <code class="token-code" :class="{ 
                          'is-token-code': token.name.includes('token-code'),
                          'is-active-token': token.name.includes(currentState),
                          'is-variant-token': token.name.includes(currentType),
                          'is-size-token': componentType === 'button' && token.name.endsWith(sizeSuffixMap[currentSize])
                        }">
                          {{ token.name }}
                        </code>
                        <span class="copy-indicator" v-if="copiedToken === token.name">
                          <i class="icon-check"></i>
                        </span>
                      </div>
                    </td>
                    <td class="token-table-td token-value-cell">
                      <div class="token-value-container">
                        <code class="token-value" :class="{ 
                          'is-token-code': token.name.includes('token-code'),
                          'is-active-value': token.name.includes(currentState)
                        }">
                          {{ formatTokenValue(token) }}
                        </code>
                        <div v-if="(token.name.includes('color') || token.name.includes('fill')) && getTokenColorValue(token) !== 'transparent'" 
                             class="token-color-preview"
                             :style="{ backgroundColor: getTokenColorValue(token) }"
                        ></div>
                      </div>
                    </td>
                    <td class="token-table-td token-usage-cell">
                      <span class="token-usage">{{ token.usage }}</span>
                    </td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base Layout */
.playground {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap-s);
  background-color: var(--color-surface-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-v-padding-xs);
}

/* Header Section */
.playground-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 0;
}

.playground-title {
  display: none;
}

.icon-group {
  display: flex;
  gap: var(--comp-button-main-gap-s);
}

.icon-button {
  color: var(--color-icon-secondary-rest);
  padding: var(--comp-button-main-v-padding-xs);
  border-radius: var(--comp-button-main-radius);
  transition: all 0.2s ease;
}

.icon-button:hover {
  color: var(--color-icon-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

/* Preview and Config Container */
.preview-config-container {
  display: flex;
  width: 100%;
  border-bottom: 1px solid var(--color-border-primary-rest);
  margin-bottom: var(--comp-button-main-gap-s);
}

.preview-section {
  width: 40%;
  padding: var(--comp-button-main-v-padding-s);
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--color-border-primary-rest);
}

.preview-area {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 1 / 1;
  padding: var(--comp-button-main-v-padding-s);
  border-radius: var(--comp-button-main-radius);
  position: relative;
  background-color: var(--color-fill-grey-rest);
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

/* Configuration Section */
.config-section {
  width: 60%;
  padding: var(--comp-button-main-v-padding-s);
}

.config-controls {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

/* Control Elements */
.control-group {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--comp-button-main-gap);
}

.control-label {
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
}

.control-options {
  display: flex;
  gap: var(--comp-button-main-gap);
}

.control-options--wrap {
  flex-wrap: wrap;
}

.control-button {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-regular-400);
  background-color: var(--color-surface-secondary-rest);
  color: var(--color-text-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

.control-button--selected {
  background-color: var(--color-fill-brand-rest);
  color: var(--color-text-primary-inverse);
  border-color: var(--color-border-brand-rest);
}

/* Input Styles */
.config-input {
  width: 100%;
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-12);
  font-family: var(--font-family-base);
  background-color: var(--color-surface-primary-rest);
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

.config-input:hover {
  border-color: var(--color-border-primary-hover);
}

.config-input:focus {
  border-color: var(--color-border-brand-focus);
  outline: none;
  box-shadow: var(--shadow-xs);
}

/* Toggle Switch */
.toggle-switch {
  width: 2.5rem;
  height: 1.5rem;
  border-radius: var(--comp-toggle-radius);
  background-color: var(--color-surface-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  position: relative;
  transition: all 0.2s ease;
}

.toggle-switch:hover {
  border-color: var(--color-border-primary-hover);
}

.toggle-switch--active {
  background-color: var(--color-fill-brand-rest);
  border-color: var(--color-border-brand-rest);
}

.toggle-switch__handle {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: var(--color-fill-neutral-rest);
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
  transition: all 0.2s ease;
}

.toggle-switch--active .toggle-switch__handle {
  left: 1.25rem;
  background-color: var(--color-fill-neutral-inverse);
}

/* Tokens Panel */
.tokens-panel {
  padding: var(--comp-button-main-v-padding-s);
  margin-top: 0;
}

.panel-title {
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  margin-bottom: var(--comp-button-main-gap-s);
  text-transform: uppercase;
}

/* Token Table */
.token-table-wrapper {
  overflow: hidden;
}

.token-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background-color: var(--color-surface-secondary-rest);
}

.token-table-header {
  position: sticky;
  top: 0;
  z-index: 1;
  background-color: var(--color-surface-secondary-rest);
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.token-table-th {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-m);
  text-align: left;
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.token-table-th:first-child {
  width: 40%;
  padding-left: 0;
}

.token-table-th:nth-child(2) {
  width: 35%;
}

.token-table-th:last-child {
  width: 25%;
}

/* Token Groups */
.token-group-row {
  color: var(--color-text-secondary-rest);
}

.token-group-header {
  padding: var(--comp-button-main-v-padding-s) 0;
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.token-group-title {
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  display: flex;
  align-items: center;
  gap: var(--comp-button-main-gap-s);
  text-transform: uppercase;
}

.token-variant-label {
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-regular-400);
  color: var(--color-text-secondary-rest);
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  background-color: var(--color-surface-secondary-rest);
  border-radius: calc(var(--comp-button-main-radius) * 0.75);
}

/* Token Cells */
.token-table-td {
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-m);
  vertical-align: middle;
  border-bottom: 1px solid var(--color-border-primary-subtle);
  background-color: var(--color-surface-secondary-rest);
  font-size: var(--font-size-12);
}

.token-table-td:first-child {
  padding-left: 0;
}

.token-name-container,
.token-value-container {
  display: flex;
  align-items: center;
  gap: var(--comp-button-main-gap-xs);
  min-width: 0;
}

/* Token Code */
.token-code {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-12);
  color: var(--color-text-primary-rest);
  background-color: var(--color-surface-secondary-hover);
  padding: var(--8px-scale-50percent);
  margin-bottom: var(--comp-button-main-v-padding-s);
  border-radius: var(--comp-button-main-radius);
  user-select: all;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

.token-code.is-size-token,
.token-code.is-token-code,
.token-code.is-active-token,
.token-code.is-variant-token {
  color: var(--color-text-primary-rest);
  background-color: var(--color-surface-secondary-hover);
}

.token-code.is-size-token:hover,
.token-code.is-token-code:hover,
.token-code.is-active-token:hover,
.token-code.is-variant-token:hover {
  background-color: var(--color-surface-brand-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-xs);
}

/* Token Value */
.token-value {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-12);
  color: var(--color-text-secondary-rest);
  background-color: var(--color-surface-secondary-hover);
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  border-radius: calc(var(--comp-button-main-radius) * 0.75);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: calc(100% - 2rem);
}

/* Token Color Preview */
.token-color-preview {
  width: 1rem;
  height: 1rem;
  border-radius: calc(var(--comp-button-main-radius) * 0.5);
  border: 1px solid var(--color-border-primary-subtle);
  flex-shrink: 0;
}

/* Token Usage */
.token-usage {
  font-size: var(--font-size-12);
  color: var(--color-text-secondary-rest);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Copy Indicator */
.copy-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-success-rest);
  font-size: var(--font-size-12);
  opacity: 0;
  transform: translateX(-0.5rem);
  transition: all 0.2s ease;
}

.token-code:hover + .copy-indicator {
  opacity: 1;
  transform: translateX(0);
}

/* Toast Notification */
.toast-notification {
  position: fixed;
  bottom: var(--comp-button-main-v-padding-l);
  right: var(--comp-button-main-h-padding-l);
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-m);
  background-color: var(--color-surface-success-rest);
  color: var(--color-text-success-rest);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  opacity: 0;
  transform: translateY(1rem);
  transition: all 0.2s ease;
  z-index: 50;
  box-shadow: var(--shadow-xs);
}

.toast-notification--show {
  opacity: 1;
  transform: translateY(0);
}

/* Responsive Styles */
@media (max-width: 768px) {
  .preview-config-container {
    flex-direction: column;
  }
  
  .preview-section,
  .config-section {
    width: 100%;
    border: none;
  }
  
  .preview-section {
    border-bottom: 1px solid var(--color-border-primary-rest);
  }
  
  .preview-area {
    aspect-ratio: auto;
    min-height: 160px;
  }

  .token-table-wrapper {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .token-table {
    min-width: 600px;
  }
}

/* Common transitions */
.icon-button,
.preview-area,
.control-button,
.config-input,
.toggle-switch,
.toggle-switch__handle,
.copy-indicator,
.toast-notification {
  transition: all 0.2s ease;
}

/* Common text styles */
.control-label,
.panel-title,
.token-group-title {
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
}

/* Common radius */
.icon-button,
.preview-area,
.control-button,
.config-input,
.toast-notification {
  border-radius: var(--comp-button-main-radius);
}
</style> 