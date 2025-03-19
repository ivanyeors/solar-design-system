<script setup lang="ts">
import { computed } from 'vue';
import { createTokenStyles } from '../../lib/tokens';

const props = defineProps<{
  /**
   * The badge variant
   */
  variant?: 'default' | 'brand' | 'success' | 'warning' | 'danger' | 'outline';
  /**
   * The badge size
   */
  size?: 's' | 'm' | 'l';
}>();

// Computing styles based on our semantic tokens
const badgeStyles = computed(() => {
  const variant = props.variant || 'default';
  const size = props.size || 'm';
  
  // Base styles for all badges
  const baseStyles = {
    borderRadius: 'var(--comp-badge-text-radius)',
    gap: 'var(--comp-badge-text-gap)',
  };
  
  // Variant-specific styles
  const variantStyles = {
    default: {
      backgroundColor: 'var(--color-fill-grey-rest)',
      color: 'var(--comp-badge-text-rest)',
      border: 'none',
    },
    brand: {
      backgroundColor: 'var(--comp-badge-surface-brand)',
      color: 'var(--comp-badge-text-brand)',
      border: 'none',
    },
    success: {
      backgroundColor: 'var(--comp-badge-surface-success)',
      color: 'var(--comp-badge-text-success)',
      border: 'none',
    },
    warning: {
      backgroundColor: 'var(--comp-badge-surface-warning)',
      color: 'var(--comp-badge-text-warning)',
      border: 'none',
    },
    danger: {
      backgroundColor: 'var(--comp-badge-surface-danger)',
      color: 'var(--comp-badge-text-danger)',
      border: 'none',
    },
    outline: {
      backgroundColor: 'transparent',
      color: 'var(--comp-badge-text-rest)',
      border: `1px solid var(--comp-badge-border-line)`,
    }
  };
  
  // Size-specific styles
  const sizeStyles = {
    s: {
      padding: `var(--comp-badge-text-v-padding-s) var(--comp-badge-text-h-padding-s)`,
      fontSize: '0.75rem',
    },
    m: {
      padding: `var(--comp-badge-text-v-padding-m) var(--comp-badge-text-h-padding-m)`,
      fontSize: '0.875rem',
    },
    l: {
      padding: `var(--comp-badge-text-v-padding-l) var(--comp-badge-text-h-padding-l)`,
      fontSize: '1rem',
    },
  };
  
  return {
    ...baseStyles,
    ...variantStyles[variant],
    ...sizeStyles[size],
  };
});
</script>

<template>
  <span
    class="inline-flex items-center font-medium"
    :style="badgeStyles"
  >
    <slot></slot>
  </span>
</template> 