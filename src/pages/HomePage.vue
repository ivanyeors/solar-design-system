<script setup lang="ts">
import Button from '../components/ui/Button.vue';
</script>

<template>
  <div>
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-extrabold text-gray-900 sm:text-5xl dark:text-white">
        Solar Design System
      </h1>
      <p class="mt-4 text-xl text-gray-600 max-w-3xl mx-auto dark:text-gray-400">
        A modern, accessible, and customizable design system for building beautiful Vue applications.
      </p>
      <div class="mt-8 flex justify-center gap-4">
        <Button size="lg" variant="primary">Get Started</Button>
        <Button size="lg" variant="outline">View on GitHub</Button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
      <!-- Feature 1 -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 dark:bg-gray-900 dark:border-gray-800">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 dark:bg-primary-900/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Customizable</h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Easily customize components to match your brand with Tailwind CSS utility classes.
        </p>
      </div>
      
      <!-- Feature 2 -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 dark:bg-gray-900 dark:border-gray-800">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 dark:bg-primary-900/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Performant</h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Built with performance in mind, ensuring your applications stay fast and responsive.
        </p>
      </div>
      
      <!-- Feature 3 -->
      <div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 dark:bg-gray-900 dark:border-gray-800">
        <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 dark:bg-primary-900/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-600 dark:text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Accessible</h3>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Designed with accessibility in mind, following WCAG guidelines for inclusive experiences.
        </p>
      </div>
    </div>
    
    <div class="mt-16 bg-white p-8 rounded-lg shadow-sm border border-gray-200 dark:bg-gray-900 dark:border-gray-800">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Getting Started</h2>
      <p class="mt-4 text-gray-600 dark:text-gray-400">
        Install the Solar Design System using npm:
      </p>
      <pre class="mt-4 bg-gray-100 p-4 rounded-md overflow-x-auto text-sm dark:bg-gray-800 dark:text-gray-300"><code>npm install solar-design-system</code></pre>
      
      <p class="mt-6 text-gray-600 dark:text-gray-400">
        Import and use components in your Vue application:
      </p>
      <pre class="mt-4 bg-gray-100 p-4 rounded-md overflow-x-auto text-sm dark:bg-gray-800 dark:text-gray-300"><code>import { Button } from 'solar-design-system';

// In your component template
&lt;Button variant="primary"&gt;Click Me&lt;/Button&gt;</code></pre>
    </div>
  </div>
</template> 