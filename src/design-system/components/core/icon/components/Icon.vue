<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  /**
   * The name of the icon from Material Symbols
   */
  name: string;
  /**
   * Size of the icon
   */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /**
   * Whether the icon should use the filled variant
   */
  filled?: boolean;
  /**
   * Weight of the icon (400 is regular, 700 is bold)
   */
  weight?: 100 | 200 | 300 | 400 | 500 | 600 | 700;
  /**
   * Color variant for the icon
   */
  color?: 'inherit' | 'primary' | 'secondary' | 'brand' | 'success' | 'warning' | 'error';
}>();

// Default values
const fill = computed(() => props.filled ? 1 : 0);
const iconWeight = computed(() => props.weight || 400);

// Size mapping
const sizeClasses = computed(() => {
  switch(props.size) {
    case 'sm': return 'text-base';
    case 'lg': return 'text-2xl';
    case 'xl': return 'text-3xl';
    case 'md':
    default: return 'text-xl';
  }
});

// Color mapping
const colorClasses = computed(() => {
  switch(props.color) {
    case 'primary': return 'text-primary';
    case 'secondary': return 'text-secondary';
    case 'brand': return 'text-brand';
    case 'success': return 'text-success';
    case 'warning': return 'text-warning';
    case 'error': return 'text-error';
    case 'inherit':
    default: return 'text-inherit';
  }
});
</script>

<template>
  <span 
    class="material-symbols-rounded"
    :class="[sizeClasses, colorClasses]"
    :style="{
      fontVariationSettings: `'FILL' ${fill}, 'wght' ${iconWeight}, 'GRAD' 0, 'opsz' 24`
    }"
  >
    {{ name }}
  </span>
</template>

<style scoped>
/* Ensure proper vertical alignment of icons */
.material-symbols-rounded {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  vertical-align: middle;
}
</style> 