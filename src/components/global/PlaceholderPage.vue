<script setup lang="ts">
defineProps<{
  title: string;
}>();
</script>

<template>
  <div class="text-center py-12">
    <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">{{ title }}</h1>
    <p class="text-gray-600 dark:text-gray-400">
      This page is currently under development. Check back soon for updates!
    </p>
  </div>
</template> 