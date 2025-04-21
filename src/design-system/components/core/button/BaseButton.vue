<script setup lang="ts">
import { computed, watch, onMounted, onUnmounted, ref } from 'vue';
import { createTokenStyles, TOKEN_TYPES, TOKEN_STATES } from '@/lib/tokens';
import { getThemeAwareToken, watchThemeChanges } from '@/utils/tokenUtils';

const props = defineProps<{
  /**
   * The button variant
   * @default 'primary'
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'warning' | 'success'
  /**
   * The button size
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg' | 'xl'
  /**
   * Whether the button is disabled
   * @default false
   */
  disabled?: boolean
  /**
   * Whether the button is in loading state
   * @default false
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

  return {
    ...baseStyles,
    ...sizeStyles,
  };
});

// Watch for theme changes
onMounted(() => {
  const cleanup = watchThemeChanges((theme) => {
    currentTheme.value = theme;
  });

  onUnmounted(() => {
    cleanup();
  });
});

// Emit click events
const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>();

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};
</script>

<template>
  <button
    :style="buttonStyles"
    :disabled="disabled || loading"
    :aria-disabled="disabled || loading"
    :data-loading="loading"
    class="base-button"
    :class="[
      `base-button--${variant || 'primary'}`,
      `base-button--${size || 'md'}`,
      {
        'base-button--disabled': disabled,
        'base-button--loading': loading
      }
    ]"
    @click="handleClick"
  >
    <span v-if="loading" class="base-button__loader" role="status" aria-label="Loading">
      <!-- Add your loading spinner component or icon here -->
    </span>
    <slot></slot>
  </button>
</template>

<style scoped>
.base-button {
  position: relative;
  cursor: pointer;
  border: none;
  outline: none;
  background: none;
  padding: 0;
  margin: 0;
  text-decoration: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

.base-button:focus-visible {
  outline: 2px solid var(--comp-button-main-focus-ring-color);
  outline-offset: 2px;
}

.base-button--disabled {
  cursor: not-allowed;
  opacity: var(--comp-button-main-opacity-disabled);
}

.base-button--loading {
  cursor: wait;
}

.base-button__loader {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

/* Variant styles will be handled through dynamic classes and CSS variables */
</style> 