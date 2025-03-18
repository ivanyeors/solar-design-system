<script setup lang="ts">
import MainLayout from './components/layout/MainLayout.vue';
import ThemeProvider from './components/theme/ThemeProvider.vue';
import ThemeToggle from './components/theme/ThemeToggle.vue';
</script>

<template>
  <ThemeProvider v-slot="{ themeMode, effectiveTheme, currentBrand, setThemeMode, setBrand }">
    <MainLayout>
      <template #theme-controls>
        <ThemeToggle 
          :value="themeMode" 
          @change="setThemeMode" 
        />
      </template>
      
      <router-view />
    </MainLayout>
  </ThemeProvider>
</template>

<style>
/* Global styles can go here if needed */
</style>
