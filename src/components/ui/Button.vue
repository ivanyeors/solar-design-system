<script setup lang="ts">
import { computed } from 'vue';
import { createTokenStyles, TOKEN_TYPES, TOKEN_STATES } from '../../lib/tokens';

const props = defineProps<{
  /**
   * The button variant
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
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
    fontWeight: `var(--comp-button-main-text-weight)`,
    transition: `var(--comp-button-main-transition)`,
  };
  
  // Variant-specific styles
  const variantStyles = {
    primary: createTokenStyles({
      backgroundColor: 'comp-button-main-fill-rest-pri',
      color: 'comp-button-main-text-color-fill-pri',
      borderWidth: 'comp-button-main-border-width',
      borderStyle: 'comp-button-main-border-style',
      borderColor: 'comp-button-main-border-color-fill-pri',
    }),
    secondary: createTokenStyles({
      backgroundColor: 'comp-button-main-fill-rest-sec',
      color: 'comp-button-main-text-color-fill-sec',
      borderWidth: 'comp-button-main-border-width',
      borderStyle: 'comp-button-main-border-style',
      borderColor: 'comp-button-main-border-color-fill-sec',
    }),
    outline: createTokenStyles({
      backgroundColor: 'comp-button-main-fill-rest-out',
      color: 'comp-button-main-text-color-out',
      borderWidth: 'comp-button-main-border-width',
      borderStyle: 'comp-button-main-border-style',
      borderColor: 'comp-button-main-border-color-out',
    }),
    ghost: createTokenStyles({
      backgroundColor: 'comp-button-main-fill-rest-ghost',
      color: 'comp-button-main-text-color-ghost',
      borderWidth: 'comp-button-main-border-width',
      borderStyle: 'comp-button-main-border-style',
      borderColor: 'comp-button-main-border-color-ghost',
    }),
  };
  
  // Size-specific styles
  const sizeStyles = {
    sm: {
      padding: `var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s)`,
      fontSize: `var(--comp-button-main-text-size-s)`,
      height: `var(--comp-button-main-height-s)`,
    },
    md: {
      padding: `var(--comp-button-main-v-padding-m) var(--comp-button-main-h-padding-m)`,
      fontSize: `var(--comp-button-main-text-size-m)`,
      height: `var(--comp-button-main-height-m)`,
    },
    lg: {
      padding: `var(--comp-button-main-v-padding-l) var(--comp-button-main-h-padding-l)`,
      fontSize: `var(--comp-button-main-text-size-l)`,
      height: `var(--comp-button-main-height-l)`,
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
/* Using hover states for buttons based on semantic tokens */
.btn-primary:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-pri);
  border-color: var(--comp-button-main-border-color-fill-hover-pri);
  color: var(--comp-button-main-text-color-fill-hover-pri);
}
.btn-primary:not(:disabled):active {
  background-color: var(--comp-button-main-fill-press-pri);
  border-color: var(--comp-button-main-border-color-fill-press-pri);
  color: var(--comp-button-main-text-color-fill-press-pri);
}
.btn-primary:focus {
  outline: var(--comp-button-main-focus-width) solid var(--comp-button-main-focus-color-pri);
  outline-offset: var(--comp-button-main-focus-offset);
}

.btn-secondary:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-sec);
  border-color: var(--comp-button-main-border-color-fill-hover-sec);
  color: var(--comp-button-main-text-color-fill-hover-sec);
}
.btn-secondary:not(:disabled):active {
  background-color: var(--comp-button-main-fill-press-sec);
  border-color: var(--comp-button-main-border-color-fill-press-sec);
  color: var(--comp-button-main-text-color-fill-press-sec);
}
.btn-secondary:focus {
  outline: var(--comp-button-main-focus-width) solid var(--comp-button-main-focus-color-sec);
  outline-offset: var(--comp-button-main-focus-offset);
}

.btn-outline:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-out);
  border-color: var(--comp-button-main-border-color-hover-out);
  color: var(--comp-button-main-text-color-hover-out);
}
.btn-outline:not(:disabled):active {
  background-color: var(--comp-button-main-fill-press-out);
  border-color: var(--comp-button-main-border-color-press-out);
  color: var(--comp-button-main-text-color-press-out);
}
.btn-outline:focus {
  outline: var(--comp-button-main-focus-width) solid var(--comp-button-main-focus-color-out);
  outline-offset: var(--comp-button-main-focus-offset);
}

.btn-ghost:not(:disabled):hover {
  background-color: var(--comp-button-main-fill-hover-ghost);
  border-color: var(--comp-button-main-border-color-hover-ghost);
  color: var(--comp-button-main-text-color-hover-ghost);
}
.btn-ghost:not(:disabled):active {
  background-color: var(--comp-button-main-fill-press-ghost);
  border-color: var(--comp-button-main-border-color-press-ghost);
  color: var(--comp-button-main-text-color-press-ghost);
}
.btn-ghost:focus {
  outline: var(--comp-button-main-focus-width) solid var(--comp-button-main-focus-color-ghost);
  outline-offset: var(--comp-button-main-focus-offset);
}

/* Handle disabled state */
button:disabled {
  opacity: var(--comp-button-main-disabled-opacity);
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