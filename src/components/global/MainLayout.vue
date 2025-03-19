<script setup lang="ts">
import { ref } from 'vue';
import Header from './Header.vue';
import SideNavigation from './SideNavigation.vue';

const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};
</script>

<template>
  <div class="min-h-screen bg-surface-canvas-rest">
    <Header 
      @toggleMobileMenu="toggleMobileMenu" 
    >
      <template #theme-controls>
        <slot name="theme-controls"></slot>
      </template>
    </Header>
    
    <SideNavigation 
      :isMobileMenuOpen="isMobileMenuOpen" 
      @closeMobileMenu="closeMobileMenu" 
    />
    
    <main class="lg:pl-64">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Any additional scoped styles */
</style> 