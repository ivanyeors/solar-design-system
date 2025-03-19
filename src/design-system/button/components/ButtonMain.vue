<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted, ref } from 'vue';
import { createTokenStyles, TOKEN_TYPES, TOKEN_STATES } from '../../../lib/tokens';
import { getThemeAwareToken, watchThemeChanges } from '../../../utils/tokenUtils';

const props = defineProps<{
  /**
   * The button variant
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'warning' | 'success'
  /**
   * The button size
   */
  size?: 'sm' | 'md' | 'lg' | 'xl'
  /**
   * Whether the button is disabled
   */
  disabled?: boolean
  /**
   * Whether the button is in loading state
   */
  loading?: boolean
}>();

// Token mapping for size suffixes
const sizeSuffixMap = {
  'sm': '-s',
  'md': '-m',
  'lg': '-l',
  'xl': '-xl'
} as const;

// Track current theme for token changes
const currentTheme = ref(document.documentElement.getAttribute('data-theme') || 'light');

// Using the token utility to create style bindings
const buttonStyles = computed(() => {
  const variantKey = props.variant || 'primary';
  const sizeKey = props.size || 'md';
  
  // Base styles that apply to all buttons
  const baseStyles = {
    borderRadius: `var(--comp-button-main-radius)`,
    gap: `var(--comp-button-main-gap)`,
    fontFamily: 'var(--font-family-DM-Sans)',
    fontWeight: 'var(--font-weight-semibold-600)',
    lineHeight: 'var(--font-line-height-20)',
    transition: 'all 0.2s ease-in-out',
    display: 'inline-flex',
    justifyContent: 'center',
    alignItems: 'center',
  };
  
  // Size-specific styles mapped to tokens
  const sizeSuffix = sizeSuffixMap[sizeKey as keyof typeof sizeSuffixMap];
  const sizeStyles = {
    padding: `var(--comp-button-main-v-padding${sizeSuffix}) var(--comp-button-main-h-padding${sizeSuffix})`,
    fontSize: sizeKey === 'sm' ? `var(--font-size-14)` :
              sizeKey === 'md' ? `var(--font-size-16)` :
              sizeKey === 'lg' ? `var(--font-size-18)` :
              `var(--font-size-20)`,
    gap: `var(--comp-button-main-gap)`,
  };

  // Variant-specific styles with state handling - dynamically compiled tokens
  const getVariantToken = (tokenType: string, state: string): string => {
    const stateToken = state || 'rest';
    
    // Special case for primary variant using brand tokens
    if (variantKey === 'primary') {
      if (tokenType === 'fill') {
        return `var(--color-fill-brand-${stateToken})`;
      }
      if (tokenType === 'border') {
        return `var(--color-border-brand-${stateToken})`;
      }
      if (tokenType === 'text') {
        return `var(--color-text-neutrallight-${stateToken})`;
      }
    }

    // Special case for ghost variant
    if (variantKey === 'ghost') {
      if (tokenType === 'fill' && stateToken === 'rest') {
        return 'transparent';
      }
      if (tokenType === 'border') {
        return 'transparent';
      }
      if (tokenType === 'fill' && stateToken === 'hover') {
        return `var(--comp-button-main-ghost-fill-press)`;
      }
    }

    // Special case for outline variant
    if (variantKey === 'outline' && tokenType === 'fill' && stateToken === 'rest') {
      return 'transparent';
    }

    // Secondary variant special case
    if (variantKey === 'secondary') {
      if (tokenType === 'fill') {
        return `var(--comp-button-main-fill-${stateToken}-sec)`;
      }
      if (tokenType === 'text' && stateToken === 'rest') {
        return `var(--comp-button-main-text-color-fill-sec)`;
      }
    }

    // Default token mapping - use standard token naming pattern
    if (tokenType === 'fill') {
      return `var(--color-fill-${variantKey}-${stateToken})`;
    }
    if (tokenType === 'text') {
      // For danger/warning/success variants, use inverse text
      if (['danger', 'warning', 'success'].includes(variantKey)) {
        return `var(--color-text-primary-inverse)`;
      }
      return `var(--color-text-primary-${stateToken})`;
    }
    if (tokenType === 'border') {
      return `var(--color-border-${variantKey}-${stateToken})`;
    }
    
    // Fallback
    return '';
  };

  // Build variant styles
  const variantStyles = {
    backgroundColor: getVariantToken('fill', 'rest'),
    color: getVariantToken('text', 'rest'),
    borderWidth: '1px',
    borderStyle: 'solid',
    borderColor: getVariantToken('border', 'rest'),
    '&:hover': {
      backgroundColor: getVariantToken('fill', 'hover'),
      borderColor: getVariantToken('border', 'hover'),
      color: getVariantToken('text', 'hover'),
    },
    '&:focus': {
      backgroundColor: getVariantToken('fill', 'focus'),
      borderColor: getVariantToken('border', 'focus'),
      outline: `4px solid ${getVariantToken('border', 'focus')}`,
      color: getVariantToken('text', 'focus'),
    },
    '&:active': {
      backgroundColor: getVariantToken('fill', 'press'),
      borderColor: getVariantToken('border', 'press'),
      color: getVariantToken('text', 'press'),
    },
    '&:disabled': {
      backgroundColor: getVariantToken('fill', 'disabled'),
      borderColor: getVariantToken('border', 'disabled'),
      color: getVariantToken('text', 'disabled'),
      opacity: '0.5',
      cursor: 'not-allowed',
    },
  };
  
  return {
    ...baseStyles,
    ...sizeStyles,
    ...variantStyles,
  };
});

// CSS class mapping
const variantClasses = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  outline: 'btn-outline',
  ghost: 'btn-ghost',
  danger: 'btn-danger',
  warning: 'btn-warning',
  success: 'btn-success',
};

// Monitor theme changes
onMounted(() => {
  // Watch for theme changes and update styles
  const cleanup = watchThemeChanges(() => {
    currentTheme.value = document.documentElement.getAttribute('data-theme') || 'light';
  });
  
  // Cleanup on component unmount
  onUnmounted(cleanup);
});
</script>

<template>
  <button
    :class="[
      'button',
      `button--${variant || 'primary'}`,
      `button--${size || 'md'}`,
      {
        'button--disabled': disabled,
        'button--loading': loading,
      }
    ]"
    :style="buttonStyles"
    :disabled="disabled || loading"
    type="button"
  >
    <span v-if="$slots['leading-icon']" class="button__icon button__icon--leading">
      <slot name="leading-icon"></slot>
    </span>
    
    <span v-if="loading" class="button__loading">
      <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
    
    <span class="button__content">
      <slot></slot>
    </span>
    
    <span v-if="$slots['trailing-icon']" class="button__icon button__icon--trailing">
      <slot name="trailing-icon"></slot>
    </span>
  </button>
</template>

<style scoped>
.button {
  position: relative;
  overflow: hidden;
  width: auto;
  height: auto;
}

.button__icon {
  width: 20px;
  height: 20px;
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.button__icon--leading {
  margin-right: var(--comp-button-main-gap);
}

.button__icon--trailing {
  margin-left: var(--comp-button-main-gap);
}

/* Icon colors based on variant and state */
.button--primary .button__icon {
  color: var(--color-icon-primary-inverse);
}

.button--primary:disabled .button__icon {
  color: var(--color-icon-brand-disabled);
}

/* State-based styles */
.button--primary:hover:not(:disabled) {
  background-color: var(--color-fill-brand-hover);
  border-color: var(--color-border-brand-hover);
}

.button--primary:focus:not(:disabled) {
  background-color: var(--color-fill-brand-focus);
  border-color: var(--color-border-brand-focus);
  outline: 4px solid var(--color-border-brand-focus);
  outline-offset: 1px;
}

.button--primary:active:not(:disabled) {
  background-color: var(--color-fill-brand-press);
  border-color: var(--color-border-brand-press);
}

.button--primary:disabled {
  background-color: var(--color-fill-brand-disabled);
  border-color: var(--color-border-brand-disabled);
  color: var(--comp-button-main-text-color-fill-pri-disabled);
}

/* Loading state */
.button--loading {
  cursor: not-allowed;
  opacity: 0.7;
}

.button__loading {
  display: inline-flex;
  align-items: center;
  margin-right: var(--comp-button-main-gap);
}

/* Using hover states for buttons based on semantic tokens with corrected token naming */
.btn-primary:not(:disabled):hover {
  background-color: var(--color-fill-brand-hover);
  border-color: var(--color-border-brand-hover);
  color: var(--color-text-neutrallight-hover);
}
.btn-primary:not(:disabled):active {
  background-color: var(--color-fill-brand-press);
  border-color: var(--color-border-brand-press);
  color: var(--color-text-neutrallight-press);
}
.btn-primary:focus {
  outline: 2px solid var(--color-border-brand-focus);
  outline-offset: 2px;
}

.btn-secondary:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-sec);
  border-color: var(--color-border-primary-hover);
  color: var(--color-text-primary-hover);
}
.btn-secondary:not(:disabled):active {
  background-color: var(--comp-button-main-fill-pressed-sec);
  border-color: var(--color-border-primary-press);
  color: var(--color-text-primary-press);
}
.btn-secondary:focus {
  outline: 2px solid var(--comp-button-main-fill-focused-sec);
  outline-offset: 2px;
}

.btn-outline:not(:disabled):hover {
  background-color: var(--color-surface-primary-hover);
  border-color: var(--color-border-primary-hover);
  color: var(--color-text-primary-hover);
}
.btn-outline:not(:disabled):active {
  background-color: var(--color-surface-primary-press);
  border-color: var(--color-border-primary-press);
  color: var(--color-text-primary-press);
}
.btn-outline:focus {
  outline: 2px solid var(--color-border-primary-focus);
  outline-offset: 2px;
}

.btn-ghost:not(:disabled):hover {
  background-color: var(--comp-button-main-ghost-fill-press);
  border-color: transparent;
  color: var(--color-text-primary-hover);
}
.btn-ghost:not(:disabled):active {
  background-color: var(--color-surface-primary-press);
  border-color: transparent;
  color: var(--color-text-primary-press);
}
.btn-ghost:focus {
  outline: 2px solid var(--color-border-primary-focus);
  outline-offset: 2px;
}

.btn-danger:not(:disabled):hover {
  background-color: var(--color-fill-danger-hover);
  border-color: var(--color-border-danger-hover);
  color: var(--color-text-primary-inverse);
}
.btn-danger:not(:disabled):active {
  background-color: var(--color-fill-danger-press);
  border-color: var(--color-border-danger-press);
  color: var(--color-text-primary-inverse);
}
.btn-danger:focus {
  outline: 2px solid var(--color-border-danger-focus);
  outline-offset: 2px;
}

.btn-warning:not(:disabled):hover {
  background-color: var(--color-fill-warning-hover);
  border-color: var(--color-border-warning-hover);
  color: var(--color-text-primary-inverse);
}
.btn-warning:not(:disabled):active {
  background-color: var(--color-fill-warning-press);
  border-color: var(--color-border-warning-press);
  color: var(--color-text-primary-inverse);
}
.btn-warning:focus {
  outline: 2px solid var(--color-border-warning-focus);
  outline-offset: 2px;
}

.btn-success:not(:disabled):hover {
  background-color: var(--color-fill-success-hover);
  border-color: var(--color-border-success-hover);
  color: var(--color-text-primary-inverse);
}
.btn-success:not(:disabled):active {
  background-color: var(--color-fill-success-press);
  border-color: var(--color-border-success-press);
  color: var(--color-text-primary-inverse);
}
.btn-success:focus {
  outline: 2px solid var(--color-border-success-focus);
  outline-offset: 2px;
}

/* Handle disabled state */
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Icon sizing based on button size */
.btn-leading-icon,
.btn-trailing-icon,
.btn-loading-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Style Material Symbols icons if used */
.btn-leading-icon .material-symbols-rounded,
.btn-trailing-icon .material-symbols-rounded {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  font-size: 1.2em;
  line-height: 1;
}
</style> 