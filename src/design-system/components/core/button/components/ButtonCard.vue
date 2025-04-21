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
  },
  title: {
    type: String,
    default: ''
  },
  description: {
    type: String,
    default: ''
  }
});
</script>

<template>
  <button
    class="button-card"
    :class="[
      `button-card--${variant}`,
      `button-card--${size}`,
      { 'button-card--disabled': disabled }
    ]"
    :disabled="disabled"
  >
    <div class="button-card__content">
      <slot name="icon"></slot>
      <div class="button-card__text">
        <h3 class="button-card__title" v-if="title">{{ title }}</h3>
        <p class="button-card__description" v-if="description">{{ description }}</p>
        <slot></slot>
      </div>
    </div>
  </button>
</template>

<style scoped>
.button-card {
  display: flex;
  width: 100%;
  text-align: left;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  /* Add additional styling based on variants and sizes */
}

.button-card__content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  width: 100%;
}

.button-card__text {
  flex: 1;
}

.button-card__title {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.button-card__description {
  color: var(--color-text-secondary-rest);
}

/* Placeholder styles - would be replaced with proper token-based styling */
.button-card--primary {
  background-color: var(--color-fill-brand-rest);
  color: white;
  border: 1px solid var(--color-fill-brand-rest);
}

.button-card--secondary {
  background-color: var(--color-surface-secondary-rest);
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
}

.button-card--outline {
  background-color: transparent;
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
}

.button-card--ghost {
  background-color: transparent;
  color: var(--color-text-primary-rest);
  border: 1px solid transparent;
}

.button-card--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Size variants */
.button-card--sm {
  padding: 0.75rem;
}

.button-card--md {
  padding: 1rem;
}

.button-card--lg {
  padding: 1.25rem;
}

.button-card--xl {
  padding: 1.5rem;
}
</style> 