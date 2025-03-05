<template>
  <div class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
    <div class="flex gap-4 items-center">
      <Button variant="primary">Click Here</Button>
      <Button variant="secondary">Submit</Button>
    </div>
    <p class="mt-4 text-sm text-red-600 dark:text-red-400">
      Avoid generic, non-descriptive labels
    </p>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script> 