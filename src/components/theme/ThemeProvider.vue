<script setup lang="ts">
import { ref, provide, onMounted } from 'vue';

// Theme options
type ThemeMode = 'light' | 'dark' | 'system';
type BrandMode = 'evydcore' | 'bruhealth';

// State refs
const themeMode = ref<ThemeMode>('system');
const effectiveTheme = ref<'light' | 'dark'>('light');
const currentBrand = ref<BrandMode>('evydcore');

// Provide theme context to child components
provide('themeMode', themeMode);
provide('effectiveTheme', effectiveTheme);
provide('currentBrand', currentBrand);

// Function to set the theme mode
const setThemeMode = (mode: ThemeMode) => {
  themeMode.value = mode;
  updateEffectiveTheme();
  
  // Save preference
  localStorage.setItem('themeMode', mode);
};

// Function to set the brand
const setBrand = (brand: BrandMode) => {
  currentBrand.value = brand;
  
  // Update data-brand attribute to trigger CSS changes
  document.documentElement.setAttribute('data-brand', brand);
  
  // Preserve the current theme when changing brands, don't override it
  const currentThemeValue = document.documentElement.getAttribute('data-theme') || 'light';
  document.documentElement.setAttribute('data-theme', currentThemeValue);
  
  // Save preference
  localStorage.setItem('brandMode', brand);
};

// Update the effective theme based on system preference if needed
const updateEffectiveTheme = () => {
  if (themeMode.value === 'system') {
    effectiveTheme.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  } else {
    effectiveTheme.value = themeMode.value as 'light' | 'dark';
  }
  
  // Apply the theme to the document
  document.documentElement.setAttribute('data-theme', effectiveTheme.value);
  
  // Make sure brand is preserved when changing themes
  const currentBrandValue = document.documentElement.getAttribute('data-brand') || 'evydcore';
  document.documentElement.setAttribute('data-brand', currentBrandValue);
  
  if (effectiveTheme.value === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

// Watch for system theme changes
const setupSystemThemeWatcher = () => {
  const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  
  const updateSystemTheme = () => {
    if (themeMode.value === 'system') {
      updateEffectiveTheme();
    }
  };
  
  // Listen for changes
  darkModeMediaQuery.addEventListener('change', updateSystemTheme);
};

onMounted(() => {
  // Restore saved preferences
  const savedThemeMode = localStorage.getItem('themeMode') as ThemeMode | null;
  const savedBrandMode = localStorage.getItem('brandMode') as BrandMode | null;
  
  // Set initial values from saved preferences or defaults
  if (savedThemeMode) {
    themeMode.value = savedThemeMode;
  }
  
  if (savedBrandMode) {
    currentBrand.value = savedBrandMode;
  }
  
  // Apply initial theme
  updateEffectiveTheme();
  
  // Ensure data-brand attribute is set
  document.documentElement.setAttribute('data-brand', currentBrand.value);
  
  // Setup system theme watcher
  setupSystemThemeWatcher();
  
  // Log initial state
  console.log(`Theme provider initialized: Brand=${currentBrand.value}, ThemeMode=${themeMode.value}, EffectiveTheme=${effectiveTheme.value}`);
});
</script>

<template>
  <slot 
    :theme-mode="themeMode" 
    :effective-theme="effectiveTheme" 
    :current-brand="currentBrand"
    :set-theme-mode="setThemeMode"
    :set-brand="setBrand"
  />
</template> 