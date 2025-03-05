<script setup lang="ts">
defineProps<{
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

const variantClasses = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500',
  secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500',
  outline: 'bg-transparent border border-gray-300 hover:bg-gray-50 focus:ring-gray-500',
  ghost: 'bg-transparent hover:bg-gray-100 focus:ring-gray-500',
};

const sizeClasses = {
  sm: 'px-3 py-1.5 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-5 py-2.5 text-base',
};
</script>

<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors',
      variantClasses[variant || 'primary'],
      sizeClasses[size || 'md'],
      disabled || loading ? 'opacity-50 cursor-not-allowed' : '',
    ]"
    :disabled="disabled || loading"
    type="button"
  >
    <span v-if="loading" class="mr-2">
      <!-- Loading spinner -->
      <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
    <slot />
  </button>
</template> 