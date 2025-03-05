<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';

defineProps<{
  isMobileMenuOpen?: boolean;
}>();

const emit = defineEmits(['closeMobileMenu']);
const route = useRoute();

const navItems = [
  {
    title: 'Getting Started',
    items: [
      { name: 'Introduction', path: '/' },
      { name: 'Installation', path: '/#installation' },
      { name: 'Usage', path: '/#usage' },
    ]
  },
  {
    title: 'Foundation',
    items: [
      { name: 'Colors', path: '/foundation/colors' },
      { name: 'Typography', path: '/foundation/typography' },
      { name: 'Spacing', path: '/foundation/spacing' },
      { name: 'Breakpoints', path: '/foundation/breakpoints' },
    ]
  },
  {
    title: 'Components',
    items: [
      { name: 'Button', path: '/components/button' },
      { name: 'Input', path: '/components/input' },
      { name: 'Card', path: '/components/card' },
      { name: 'Badge', path: '/components/badge' },
    ]
  }
];

const closeMobileMenu = () => {
  emit('closeMobileMenu');
};
</script>

<template>
  <div class="sidebar-container">
    <!-- Mobile nav overlay -->
    <div 
      v-if="isMobileMenuOpen" 
      class="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
      @click="closeMobileMenu"
    ></div>
    
    <!-- Sidebar -->
    <aside 
      class="fixed top-0 left-0 z-50 h-full w-64 transform bg-white border-r border-gray-200 
             overflow-y-auto transition-transform duration-300 ease-in-out
             dark:bg-gray-900 dark:border-gray-800
             lg:translate-x-0"
      :class="{ 'translate-x-0': isMobileMenuOpen, '-translate-x-full': !isMobileMenuOpen }"
    >
      <div class="p-5">
        <div class="flex items-center justify-between mb-6">
          <router-link to="/" class="text-xl font-bold text-gray-900 dark:text-white">Solar Design</router-link>
          <button 
            @click="closeMobileMenu"
            class="p-2 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100 lg:hidden
                  dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="h-6 w-6">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <nav class="space-y-8">
          <div v-for="(section, index) in navItems" :key="index">
            <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400">
              {{ section.title }}
            </h3>
            <ul class="mt-3 space-y-2">
              <li v-for="(item, itemIndex) in section.items" :key="itemIndex">
                <router-link 
                  :to="item.path" 
                  :class="[
                    'block px-3 py-2 rounded-md text-sm font-medium',
                    route.path === item.path || (route.path === '/' && item.path === '/')
                      ? 'bg-primary-50 text-primary-600 dark:bg-primary-900/20 dark:text-primary-400'
                      : 'text-gray-700 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800'
                  ]"
                  @click="closeMobileMenu"
                >
                  {{ item.name }}
                </router-link>
              </li>
            </ul>
          </div>
        </nav>
        
        <div class="mt-12 pt-8 border-t border-gray-200 dark:border-gray-800">
          <a 
            href="https://github.com/ivanyeors/solar-design-system" 
            target="_blank"
            class="flex items-center text-gray-700 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white"
          >
            <svg class="h-5 w-5 mr-2" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </a>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
/* Any additional scoped styles */
</style> 