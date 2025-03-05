<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-8">
    <div class="flex flex-col gap-8">
      <!-- Horizontal spacing example -->
      <div>
        <h4 class="text-sm font-medium mb-4">Horizontal Spacing (8px)</h4>
        <div class="flex gap-2 items-center">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
        </div>
      </div>
      
      <!-- Vertical spacing example -->
      <div>
        <h4 class="text-sm font-medium mb-4">Vertical Spacing (16px)</h4>
        <div class="flex flex-col gap-4">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script> 