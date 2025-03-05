<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import Header from './Header.vue';
import SideNavigation from './SideNavigation.vue';

const isDarkMode = ref(false);
const isMobileMenuOpen = ref(false);

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  
  // Update the document class for dark mode
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
};

// Check for saved theme preference or prefer-color-scheme
onMounted(() => {
  const savedTheme = localStorage.getItem('theme');
  
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkMode.value = true;
    document.documentElement.classList.add('dark');
  } else {
    isDarkMode.value = false;
    document.documentElement.classList.remove('dark');
  }
});
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950">
    <Header 
      :isDarkMode="isDarkMode" 
      @toggleDarkMode="toggleDarkMode" 
      @toggleMobileMenu="toggleMobileMenu" 
    />
    
    <SideNavigation 
      :isMobileMenuOpen="isMobileMenuOpen" 
      @closeMobileMenu="closeMobileMenu" 
    />
    
    <main class="lg:pl-64 pt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <slot />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Any additional scoped styles */
</style> 