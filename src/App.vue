<script setup lang="ts">
import Button from './components/ui/Button.vue';
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <div class="text-center">
        <h1 class="text-3xl font-extrabold text-gray-900 sm:text-4xl">
          Solar Design System
        </h1>
        <p class="mt-3 text-xl text-gray-500 sm:mt-4">
          A modern design system built with Vue and Tailwind CSS
        </p>
      </div>

      <div class="mt-16">
        <h2 class="text-2xl font-bold text-gray-900">Button Component</h2>
        
        <div class="mt-8 space-y-8">
          <div class="space-y-2">
            <h3 class="text-lg font-medium text-gray-900">Variants</h3>
            <div class="flex flex-wrap gap-4">
              <Button variant="primary">Primary</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
            </div>
          </div>

          <div class="space-y-2">
            <h3 class="text-lg font-medium text-gray-900">Sizes</h3>
            <div class="flex flex-wrap items-center gap-4">
              <Button size="sm">Small</Button>
              <Button size="md">Medium</Button>
              <Button size="lg">Large</Button>
            </div>
          </div>

          <div class="space-y-2">
            <h3 class="text-lg font-medium text-gray-900">States</h3>
            <div class="flex flex-wrap gap-4">
              <Button disabled>Disabled</Button>
              <Button loading>Loading</Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
