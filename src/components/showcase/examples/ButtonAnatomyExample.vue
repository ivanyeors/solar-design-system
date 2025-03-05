<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-8">
    <div class="relative inline-block">
      <Button variant="primary" size="lg">
        <template #leading-icon>
          <i class="icon-mail"></i>
        </template>
        Send Message
        <template #trailing-icon>
          <i class="icon-arrow-right"></i>
        </template>
      </Button>
      
      <!-- Anatomy Labels -->
      <div class="absolute -top-6 left-0 text-xs text-gray-500">1. Container</div>
      <div class="absolute top-1/2 -translate-y-1/2 -left-24 text-xs text-gray-500">2. Leading Icon</div>
      <div class="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 text-xs text-gray-500">3. Label</div>
      <div class="absolute top-1/2 -translate-y-1/2 -right-24 text-xs text-gray-500">4. Trailing Icon</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script> 