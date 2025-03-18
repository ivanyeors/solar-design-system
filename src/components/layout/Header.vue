<script setup lang="ts">
const emit = defineEmits(['toggleMobileMenu']);

const toggleMobileMenu = () => {
  emit('toggleMobileMenu');
};
</script>

<template>
  <header class="header">
    <div class="px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 items-center justify-between">
        <!-- Mobile menu button -->
        <button 
          @click="toggleMobileMenu"
          class="icon-button lg:hidden"
          aria-label="Open main menu"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <!-- Logo (visible on mobile) -->
        <div class="flex lg:hidden">
          <span class="text-xl font-bold logo-text">Solar Design</span>
        </div>
        
        <!-- Search (hidden on mobile) -->
        <div class="hidden lg:flex lg:flex-1 lg:justify-center">
          <div class="w-full max-w-lg">
            <label for="search" class="sr-only">Search</label>
            <div class="relative">
              <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                id="search"
                name="search"
                class="search-input"
                placeholder="Search components..."
                type="search"
              />
            </div>
          </div>
        </div>
        
        <!-- Right side actions -->
        <div class="flex items-center">
          <!-- Theme toggle -->
          <slot name="theme-controls"></slot>
          
          <!-- GitHub link -->
          <a
            href="https://github.com/ivanyeors/solar-design-system"
            target="_blank"
            class="icon-button ml-4"
            aria-label="GitHub"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 30;
  width: 100%;
  background-color: var(--color-surface-primary-rest);
  border-bottom: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

.logo-text {
  color: var(--color-text-primary-rest);
  transition: color 0.2s ease;
}

.icon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: var(--comp-button-main-radius);
  transition: all 0.2s ease;
  color: var(--color-icon-primary-rest);
}

.icon-button:hover {
  background-color: var(--color-surface-primary-hover);
  color: var(--color-icon-primary-hover);
}

.icon-button svg {
  width: 1.5rem;
  height: 1.5rem;
}

.search-icon {
  color: var(--color-icon-secondary-rest);
  transition: color 0.2s ease;
}

.search-input {
  display: block;
  width: 100%;
  border-radius: 0.375rem;
  border: 1px solid var(--color-border-primary-rest);
  background-color: var(--color-surface-primary-rest);
  color: var(--color-text-primary-rest);
  padding: 0.375rem 0.75rem;
  padding-left: 2.5rem;
  font-size: 0.875rem;
  line-height: 1.5rem;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: var(--color-text-secondary-rest);
  transition: color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-border-brand-focus);
  box-shadow: 0 0 0 1px var(--color-border-brand-focus);
}

/* Theme-specific styles */
:root[data-theme="light"] .header {
  background-color: var(--color-surface-primary-rest);
  border-color: var(--color-border-primary-rest);
}

:root[data-theme="light"] .icon-button {
  color: var(--color-icon-primary-rest);
}

:root[data-theme="light"] .search-input {
  background-color: var(--color-surface-primary-rest);
  border-color: var(--color-border-primary-rest);
  color: var(--color-text-primary-rest);
}

:root[data-theme="dark"] .header {
  background-color: var(--color-surface-primary-rest);
  border-color: var(--color-border-primary-rest);
}

:root[data-theme="dark"] .icon-button {
  color: var(--color-icon-primary-rest);
}

:root[data-theme="dark"] .search-input {
  background-color: var(--color-surface-primary-rest);
  border-color: var(--color-border-primary-rest);
  color: var(--color-text-primary-rest);
}
</style> 