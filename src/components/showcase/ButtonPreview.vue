<script setup lang="ts">
import { ref } from 'vue';
import Button from '../ui/Button.vue';

const size = ref('sm');
const state = ref('rest');
const type = ref('primary');
const showLabel = ref(true);
const showLeadingIcon = ref(true);
const showTrailingIcon = ref(false);
const label = ref('Open Mail');
const leadingIcon = ref('mail-01');

// Token values for display
const tokenValues = {
  brands: 'Auto (EVYDCore)',
  color: 'Auto (Light)',
  tokenColor: 'Auto (EVYD Core)',
  padding: {
    sm: '0.5rem 1rem',
    md: '0.75rem 1.5rem',
    lg: '1rem 2rem'
  },
  fontSize: {
    sm: '0.875rem',
    md: '1rem',
    lg: '1.125rem'
  }
};

const copyTokenValue = async (value: string) => {
  try {
    await navigator.clipboard.writeText(value);
    // You could add a toast notification here
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};
</script>

<template>
  <div class="flex gap-8">
    <!-- Preview Area -->
    <div class="flex-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-8 flex items-center justify-center">
      <Button
        :size="size"
        :variant="type"
        :disabled="state === 'disabled'"
        :loading="state === 'loading'"
      >
        <template v-if="showLeadingIcon" #leading-icon>
          <i :class="`icon-${leadingIcon}`"></i>
        </template>
        <span v-if="showLabel">{{ label }}</span>
        <template v-if="showTrailingIcon" #trailing-icon>
          <i class="icon-arrow-right"></i>
        </template>
      </Button>
    </div>

    <!-- Controls Area -->
    <div class="w-80 bg-gray-900 rounded-lg p-6 space-y-6">
      <div class="flex justify-between items-center">
        <h3 class="text-white text-sm font-medium">button-main-v1.1.0</h3>
        <div class="flex gap-2">
          <button class="text-gray-400 hover:text-white">
            <i class="icon-copy"></i>
          </button>
          <button class="text-gray-400 hover:text-white">
            <i class="icon-refresh"></i>
          </button>
        </div>
      </div>

      <!-- Size Control -->
      <div class="space-y-2">
        <label class="text-gray-400 text-sm">Size</label>
        <select v-model="size" class="w-full bg-gray-800 text-white rounded-md p-2">
          <option value="sm">Small</option>
          <option value="md">Medium</option>
          <option value="lg">Large</option>
        </select>
      </div>

      <!-- State Control -->
      <div class="space-y-2">
        <label class="text-gray-400 text-sm">State</label>
        <select v-model="state" class="w-full bg-gray-800 text-white rounded-md p-2">
          <option value="rest">Rest</option>
          <option value="hover">Hover</option>
          <option value="disabled">Disabled</option>
          <option value="loading">Loading</option>
        </select>
      </div>

      <!-- Type Control -->
      <div class="space-y-2">
        <label class="text-gray-400 text-sm">Type</label>
        <select v-model="type" class="w-full bg-gray-800 text-white rounded-md p-2">
          <option value="primary">Primary</option>
          <option value="secondary">Secondary</option>
          <option value="outline">Outline</option>
          <option value="ghost">Ghost</option>
        </select>
      </div>

      <!-- Label Controls -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <label class="text-gray-400 text-sm">Show Label</label>
          <button 
            class="w-10 h-6 rounded-full relative"
            :class="showLabel ? 'bg-blue-600' : 'bg-gray-700'"
            @click="showLabel = !showLabel"
          >
            <span 
              class="w-4 h-4 bg-white rounded-full absolute top-1"
              :class="showLabel ? 'right-1' : 'left-1'"
            ></span>
          </button>
        </div>
        <input 
          v-if="showLabel"
          v-model="label"
          class="w-full bg-gray-800 text-white rounded-md p-2"
          placeholder="Button Label"
        >
      </div>

      <!-- Icon Controls -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <label class="text-gray-400 text-sm">Show Leading Icon</label>
          <button 
            class="w-10 h-6 rounded-full relative"
            :class="showLeadingIcon ? 'bg-blue-600' : 'bg-gray-700'"
            @click="showLeadingIcon = !showLeadingIcon"
          >
            <span 
              class="w-4 h-4 bg-white rounded-full absolute top-1"
              :class="showLeadingIcon ? 'right-1' : 'left-1'"
            ></span>
          </button>
        </div>
        <div class="flex items-center justify-between">
          <label class="text-gray-400 text-sm">Show Trailing Icon</label>
          <button 
            class="w-10 h-6 rounded-full relative"
            :class="showTrailingIcon ? 'bg-blue-600' : 'bg-gray-700'"
            @click="showTrailingIcon = !showTrailingIcon"
          >
            <span 
              class="w-4 h-4 bg-white rounded-full absolute top-1"
              :class="showTrailingIcon ? 'right-1' : 'left-1'"
            ></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template> 