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

const sizes = [
  { value: 'sm', label: 'Small' },
  { value: 'md', label: 'Medium' },
  { value: 'lg', label: 'Large' }
];

const states = [
  { value: 'rest', label: 'Rest' },
  { value: 'hover', label: 'Hover' },
  { value: 'disabled', label: 'Disabled' },
  { value: 'loading', label: 'Loading' }
];

const types = [
  { value: 'primary', label: 'Primary' },
  { value: 'secondary', label: 'Secondary' },
  { value: 'outline', label: 'Outline' },
  { value: 'ghost', label: 'Ghost' }
];
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
        <div class="flex gap-2">
          <button
            v-for="sizeOption in sizes"
            :key="sizeOption.value"
            @click="size = sizeOption.value"
            class="px-3 py-1 rounded-full text-sm"
            :class="[
              size === sizeOption.value
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            ]"
          >
            {{ sizeOption.label }}
          </button>
        </div>
      </div>

      <!-- State Control -->
      <div class="space-y-2">
        <label class="text-gray-400 text-sm">State</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="stateOption in states"
            :key="stateOption.value"
            @click="state = stateOption.value"
            class="px-3 py-1 rounded-full text-sm"
            :class="[
              state === stateOption.value
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            ]"
          >
            {{ stateOption.label }}
          </button>
        </div>
      </div>

      <!-- Type Control -->
      <div class="space-y-2">
        <label class="text-gray-400 text-sm">Type</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="typeOption in types"
            :key="typeOption.value"
            @click="type = typeOption.value"
            class="px-3 py-1 rounded-full text-sm"
            :class="[
              type === typeOption.value
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            ]"
          >
            {{ typeOption.label }}
          </button>
        </div>
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

      <!-- Token Values -->
      <div class="space-y-4 pt-4 border-t border-gray-800">
        <h4 class="text-gray-400 text-sm font-medium">Token Values</h4>
        
        <!-- Size-specific tokens -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-400">Padding</span>
            <button 
              @click="copyTokenValue(tokenValues.padding[size])"
              class="text-gray-300 hover:text-white flex items-center gap-2"
            >
              {{ tokenValues.padding[size] }}
              <i class="icon-copy text-gray-500"></i>
            </button>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-400">Font Size</span>
            <button 
              @click="copyTokenValue(tokenValues.fontSize[size])"
              class="text-gray-300 hover:text-white flex items-center gap-2"
            >
              {{ tokenValues.fontSize[size] }}
              <i class="icon-copy text-gray-500"></i>
            </button>
          </div>
        </div>

        <!-- Theme tokens -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-400">Brand</span>
            <button 
              @click="copyTokenValue(tokenValues.brands)"
              class="text-gray-300 hover:text-white flex items-center gap-2"
            >
              {{ tokenValues.brands }}
              <i class="icon-copy text-gray-500"></i>
            </button>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-400">Color Mode</span>
            <button 
              @click="copyTokenValue(tokenValues.color)"
              class="text-gray-300 hover:text-white flex items-center gap-2"
            >
              {{ tokenValues.color }}
              <i class="icon-copy text-gray-500"></i>
            </button>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-400">Token Color</span>
            <button 
              @click="copyTokenValue(tokenValues.tokenColor)"
              class="text-gray-300 hover:text-white flex items-center gap-2"
            >
              {{ tokenValues.tokenColor }}
              <i class="icon-copy text-gray-500"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.icon-copy {
  @apply w-4 h-4;
}
</style> 