<script setup lang="ts">
import { MainLayout } from './components/global';
import ThemeProvider from './components/theme/ThemeProvider.vue';
import ThemeToggle from './components/theme/ThemeToggle.vue';
</script>

<template>
  <ThemeProvider v-slot="{ themeMode, setThemeMode }">
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
