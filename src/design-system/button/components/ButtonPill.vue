<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'secondary', 'outline', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value: string) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <button
    class="button-pill"
    :class="[
      `button-pill--${variant}`,
      `button-pill--${size}`,
      { 'button-pill--disabled': disabled }
    ]"
    :disabled="disabled"
  >
    <slot></slot>
  </button>
</template>

<style scoped>
.button-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px; /* This makes it a pill shape */
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  /* Add additional styling based on variants and sizes */
}

/* Placeholder styles - would be replaced with proper token-based styling */
.button-pill--primary {
  background-color: var(--color-fill-brand-rest);
  color: white;
  border: 1px solid var(--color-fill-brand-rest);
}

.button-pill--secondary {
  background-color: var(--color-surface-secondary-rest);
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
}

.button-pill--outline {
  background-color: transparent;
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
}

.button-pill--ghost {
  background-color: transparent;
  color: var(--color-text-primary-rest);
  border: 1px solid transparent;
}

.button-pill--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Size variants */
.button-pill--sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.button-pill--md {
  padding: 0.5rem 1rem;
  font-size: 1rem;
}

.button-pill--lg {
  padding: 0.625rem 1.25rem;
  font-size: 1.125rem;
}

.button-pill--xl {
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
}
</style> 