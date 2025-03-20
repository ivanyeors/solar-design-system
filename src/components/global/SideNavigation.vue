<script setup lang="ts">
// @ts-ignore - TypeScript doesn't recognize importmap resolutions, but it works at runtime
import { useRoute } from 'vue-router';
import SolarLogo from '@/assets/solar-design-system.svg';

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
      { name: 'Brands', path: '/foundation/brands' },
      { name: 'Colors', path: '/foundation/colors' },
      { name: 'Design Tokens', path: '/foundation/tokens' },
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
      class="mobile-overlay"
      @click="closeMobileMenu"
    ></div>
    
    <!-- Sidebar -->
    <aside 
      class="sidebar"
      :class="{ 'translate-x-0': isMobileMenuOpen, '-translate-x-full': !isMobileMenuOpen }"
    >
      <div class="p-5">
        <div class="flex items-center justify-between mb-6">
          <router-link to="/" class="flex items-center text-xl font-bold sidebar-logo">
            <img :src="SolarLogo" alt="Solar Design System" class="h-8 w-8 mr-2" />
            <span>Solar Design</span>
          </router-link>
          <button 
            @click="closeMobileMenu"
            class="sidebar-close-btn lg:hidden"
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
                    'nav-link',
                    route.path === item.path || (route.path === '/' && item.path === '/')
                      ? 'nav-link-active'
                      : 'nav-link-inactive'
                  ]"
                  @click="closeMobileMenu"
                >
                  {{ item.name }}
                </router-link>
              </li>
            </ul>
          </div>
        </nav>
        
        <div class="mt-12 pt-8 border-t sidebar-footer">
          <a 
            href="https://github.com/ivanyeors/solar-design-system" 
            target="_blank"
            class="github-link"
          >
            <svg class="mr-2" viewBox="0 0 24 24" fill="currentColor">
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
/* Mobile overlay */
.mobile-overlay {
  @apply fixed inset-0 z-40 lg:hidden;
  background-color: rgba(0, 0, 0, 0.5);
}

/* Sidebar */
.sidebar {
  @apply fixed top-[calc(4rem+1px)] left-0 z-50 h-[calc(100vh-4rem-1px)] w-64 transform overflow-y-auto 
         transition-transform duration-300 ease-in-out lg:top-[calc(4rem+1px)] lg:translate-x-0;
  background-color: var(--color-surface-primary-rest);
  border-right: 1px solid var(--color-border-primary-rest);
}

/* Logo */
.sidebar-logo {
  color: var(--color-text-primary-rest);
}

/* Close button */
.sidebar-close-btn {
  @apply p-2 rounded-md;
  color: var(--color-icon-secondary-rest);
}

.sidebar-close-btn:hover {
  color: var(--color-icon-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

/* Nav links */
.nav-link {
  @apply block py-2 px-3 rounded-lg transition-colors duration-200;
}

.nav-link-active {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

.nav-link-inactive {
  color: var(--color-text-secondary-rest);
}

.nav-link-inactive:hover {
  background-color: var(--color-surface-secondary-hover);
  color: var(--color-text-secondary-hover);
}

/* Footer */
.sidebar-footer {
  border-color: var(--color-border-primary-rest);
}

/* GitHub link */
.github-link {
  @apply flex items-center;
  color: var(--color-text-secondary-rest);
  transition: color 0.2s ease;
}

.github-link:hover {
  color: var(--color-text-secondary-hover);
}

.github-link svg {
  width: 20px;
  height: 20px;
}
</style> 