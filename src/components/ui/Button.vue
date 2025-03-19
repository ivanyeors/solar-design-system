<script setup lang="ts">
import { computed } from 'vue';
import { createTokenStyles, TOKEN_TYPES, TOKEN_STATES } from '../../lib/tokens';

const props = defineProps<{
  /**
   * The button variant
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'warning' | 'success'
  /**
   * The button size
   */
  size?: 'sm' | 'md' | 'lg'
  /**
   * Whether the button is disabled
   */
  disabled?: boolean
  /**
   * Whether the button is in loading state
   */
  loading?: boolean
}>();

// Using the token utility to create style bindings
const buttonStyles = computed(() => {
  const variantKey = props.variant || 'primary';
  const sizeKey = props.size || 'md';
  
  // Base styles that apply to all buttons
  const baseStyles = {
    borderRadius: `var(--comp-button-main-radius)`,
    gap: `var(--comp-button-main-gap)`,
    fontWeight: 'var(--font-weight-medium-500, 500)',
    transition: 'all 0.2s ease-in-out',
  };
  
  // Variant-specific styles with corrected token naming to match compiled-tokens.css
  const variantStyles = {
    primary: {
      backgroundColor: `var(--comp-button-main-fill-pri-focused, #257bdf)`,
      color: `var(--comp-button-main-text-color-fill-pri, #17191a)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--comp-button-main-color-stroke-pri-focused, #18304a)`,
    },
    secondary: {
      backgroundColor: `var(--comp-button-main-fill-rest-sec, #17191a)`,
      color: `var(--comp-button-main-text-color-fill-sec, #dadee3)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--comp-button-main-border-primary-rest, #313438)`,
    },
    outline: {
      backgroundColor: 'transparent',
      color: `var(--color-text-primary-rest, #dadee3)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--color-border-primary-rest, #313438)`,
    },
    ghost: {
      backgroundColor: 'transparent',
      color: `var(--color-text-primary-rest, #dadee3)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: 'transparent',
    },
    danger: {
      backgroundColor: `var(--color-fill-danger-rest, #f04437)`,
      color: `var(--color-text-primary-inverse, #fafbfc)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--color-border-danger-rest, #8c1e16)`,
    },
    warning: {
      backgroundColor: `var(--color-fill-warning-rest, #eda011)`,
      color: `var(--color-text-primary-inverse, #fafbfc)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--color-border-warning-rest, #f0ab2b)`,
    },
    success: {
      backgroundColor: `var(--color-fill-success-rest, #12b869)`,
      color: `var(--color-text-primary-inverse, #fafbfc)`,
      borderWidth: '1px',
      borderStyle: 'solid',
      borderColor: `var(--color-border-success-rest, #12b869)`,
    },
  };
  
  // Size-specific styles
  const sizeStyles = {
    sm: {
      padding: `var(--comp-button-main-v-padding-s, 8px) var(--comp-button-main-h-padding-s, 16px)`,
      fontSize: `var(--font-size-14, 14px)`,
      height: `auto`,
    },
    md: {
      padding: `var(--comp-button-main-v-padding-m, 12px) var(--comp-button-main-h-padding-m, 20px)`,
      fontSize: `var(--font-size-16, 16px)`,
      height: `auto`,
    },
    lg: {
      padding: `var(--comp-button-main-v-padding-l, 16px) var(--comp-button-main-h-padding-l, 24px)`,
      fontSize: `var(--font-size-18, 18px)`,
      height: `auto`,
    },
  };
  
  return {
    ...baseStyles,
    ...variantStyles[variantKey],
    ...sizeStyles[sizeKey],
  };
});

// Using CSS variables from semantic tokens for hover/focus states
const variantClasses = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  outline: 'btn-outline',
  ghost: 'btn-ghost',
  danger: 'btn-danger',
  warning: 'btn-warning',
  success: 'btn-success',
};
</script>

<template>
  <button
    :class="[
      'inline-flex items-center justify-center focus:outline-none transition-colors',
      variantClasses[variant || 'primary'],
      disabled || loading ? 'opacity-50 cursor-not-allowed' : '',
    ]"
    :style="buttonStyles"
    :disabled="disabled || loading"
    type="button"
  >
    <!-- Leading Icon Slot -->
    <span v-if="$slots['leading-icon']" class="btn-leading-icon mr-2">
      <slot name="leading-icon"></slot>
    </span>
    
    <!-- Loading Spinner -->
    <span v-if="loading" class="btn-loading-icon mr-2">
      <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
    
    <!-- Main Button Content -->
    <span class="btn-content">
      <slot></slot>
    </span>
    
    <!-- Trailing Icon Slot -->
    <span v-if="$slots['trailing-icon']" class="btn-trailing-icon ml-2">
      <slot name="trailing-icon"></slot>
    </span>
  </button>
</template>

<style scoped>
/* Using hover states for buttons based on semantic tokens with corrected token naming */
.btn-primary:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-pri-hover, #2768b2);
  border-color: var(--color-border-brand-hover, #5397e5);
  color: var(--color-text-primary-hover, #dadee3);
}
.btn-primary:not(:disabled):active {
  background-color: var(--comp-button-main-fill-pri-pressed, #5397e5);
  border-color: var(--color-border-brand-press, #9dc5f2);
  color: var(--color-text-primary-press, #dadee3);
}
.btn-primary:focus {
  outline: 2px solid var(--comp-button-main-color-stroke-pri-focused, #18304a);
  outline-offset: 2px;
}

.btn-secondary:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-sec, #242629);
  border-color: var(--color-border-primary-hover, #3e4247);
  color: var(--color-text-primary-hover, #dadee3);
}
.btn-secondary:not(:disabled):active {
  background-color: var(--comp-button-main-fill-pressed-sec, #17191a);
  border-color: var(--color-border-primary-press, #4b5057);
  color: var(--color-text-primary-press, #dadee3);
}
.btn-secondary:focus {
  outline: 2px solid var(--comp-button-main-fill-focused-sec, #17191a);
  outline-offset: 2px;
}

.btn-outline:not(:disabled):hover {
  background-color: var(--color-surface-primary-hover, #242629);
  border-color: var(--color-border-primary-hover, #3e4247);
  color: var(--color-text-primary-hover, #dadee3);
}
.btn-outline:not(:disabled):active {
  background-color: var(--color-surface-primary-press, #313438);
  border-color: var(--color-border-primary-press, #4b5057);
  color: var(--color-text-primary-press, #dadee3);
}
.btn-outline:focus {
  outline: 2px solid var(--color-border-primary-focus, #313438);
  outline-offset: 2px;
}

.btn-ghost:not(:disabled):hover {
  background-color: var(--comp-button-main-ghost-fill-press, #eaecf0);
  border-color: transparent;
  color: var(--color-text-primary-hover, #dadee3);
}
.btn-ghost:not(:disabled):active {
  background-color: var(--color-surface-primary-press, #313438);
  border-color: transparent;
  color: var(--color-text-primary-press, #dadee3);
}
.btn-ghost:focus {
  outline: 2px solid var(--color-border-primary-focus, #313438);
  outline-offset: 2px;
}

.btn-danger:not(:disabled):hover {
  background-color: var(--color-fill-danger-hover, #f2584e);
  border-color: var(--color-border-danger-hover, #731711);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-danger:not(:disabled):active {
  background-color: var(--color-fill-danger-press, #d6382d);
  border-color: var(--color-border-danger-press, #59110c);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-danger:focus {
  outline: 2px solid var(--color-border-danger-focus, #fcdedc);
  outline-offset: 2px;
}

.btn-warning:not(:disabled):hover {
  background-color: var(--color-fill-warning-hover, #f0ab2b);
  border-color: var(--color-border-warning-hover, #eda011);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-warning:not(:disabled):active {
  background-color: var(--color-fill-warning-press, #d49115);
  border-color: var(--color-border-warning-press, #d49115);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-warning:focus {
  outline: 2px solid var(--color-border-warning-focus, #fae3b9);
  outline-offset: 2px;
}

.btn-success:not(:disabled):hover {
  background-color: var(--color-fill-success-hover, #28bf78);
  border-color: var(--color-border-success-hover, #11a660);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-success:not(:disabled):active {
  background-color: var(--color-fill-success-press, #11a660);
  border-color: var(--color-border-success-press, #0d804a);
  color: var(--color-text-primary-inverse, #fafbfc);
}
.btn-success:focus {
  outline: 2px solid var(--color-border-success-focus, #12b869);
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