<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';

// Theme options
type ThemeMode = 'light' | 'dark' | 'system';

const props = defineProps<{
  /**
   * Current theme mode
   */
  value?: ThemeMode;
}>();

const emit = defineEmits<{
  (e: 'change', value: ThemeMode): void;
}>();

const currentTheme = ref<ThemeMode>(props.value || 'system');

// System theme detection
const systemTheme = ref<'light' | 'dark'>('light');
const effectiveTheme = computed(() => {
  return currentTheme.value === 'system' ? systemTheme.value : currentTheme.value;
});

// Update the document with the current theme
const applyTheme = (theme: 'light' | 'dark') => {
  document.documentElement.setAttribute('data-theme', theme);
  
  // Apply appropriate CSS class
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

// Watch for system theme changes
const watchSystemTheme = () => {
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  
  const updateSystemTheme = (e: MediaQueryListEvent | MediaQueryList) => {
    systemTheme.value = e.matches ? 'dark' : 'light';
    
    // If using system theme, apply the new system theme
    if (currentTheme.value === 'system') {
      applyTheme(systemTheme.value);
    }
  };
  
  // Set initial value
  updateSystemTheme(darkModeMediaQuery);
  
  // Listen for changes
  darkModeMediaQuery.addEventListener('change', updateSystemTheme);
};

// Watch for theme changes
watch(effectiveTheme, (newTheme) => {
  applyTheme(newTheme);
});

// Update theme when value changes from parent
watch(() => props.value, (newValue) => {
  if (newValue) {
    currentTheme.value = newValue;
  }
});

const setTheme = (theme: ThemeMode) => {
  currentTheme.value = theme;
  emit('change', theme);
};

onMounted(() => {
  watchSystemTheme();
  
  // Apply initial theme
  applyTheme(effectiveTheme.value);
});
</script>

<template>
  <div class="theme-toggle">
    <div class="flex items-center space-x-2">
      <button
        @click="setTheme('light')"
        :class="[
          'p-2 rounded-md focus:outline-none transition-colors',
          effectiveTheme === 'light' ? 
            'bg-fill-brand-pale-rest text-icon-brand-rest' : 
            'text-icon-secondary-rest hover:text-icon-secondary-hover'
        ]"
        aria-label="Light Mode"
        title="Light Mode"
      >
        <!-- Sun icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      </button>
      <button
        @click="setTheme('dark')"
        :class="[
          'p-2 rounded-md focus:outline-none transition-colors',
          effectiveTheme === 'dark' ? 
            'bg-fill-brand-pale-rest text-icon-brand-rest' : 
            'text-icon-secondary-rest hover:text-icon-secondary-hover'
        ]"
        aria-label="Dark Mode"
        title="Dark Mode"
      >
        <!-- Moon icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
        </svg>
      </button>
      <button
        @click="setTheme('system')"
        :class="[
          'p-2 rounded-md focus:outline-none transition-colors',
          currentTheme === 'system' ? 
            'bg-fill-brand-pale-rest text-icon-brand-rest' : 
            'text-icon-secondary-rest hover:text-icon-secondary-hover'
        ]"
        aria-label="System Theme"
        title="System Theme"
      >
        <!-- Computer icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      </button>
    </div>
  </div>
</template> 