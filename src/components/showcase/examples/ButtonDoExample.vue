<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
    <div class="flex gap-4 items-center">
      <Button variant="primary">Save Changes</Button>
      <Button variant="secondary">Cancel</Button>
    </div>
    <p class="mt-4 text-sm text-green-600 dark:text-green-400">
      Clear, action-oriented labels
    </p>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script> 