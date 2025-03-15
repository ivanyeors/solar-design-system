<script setup lang="ts">
defineProps({
  name: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  path: {
    type: String,
    required: true
  }
});
</script>

<template>
  <router-link 
    :to="path"
    class="block p-5 bg-gray-50 dark:bg-gray-800/50 rounded-xl border border-gray-200 dark:border-gray-700 transition-all duration-200 hover:shadow-md hover:border-blue-200 dark:hover:border-blue-800 hover:bg-blue-50/50 dark:hover:bg-blue-900/10"
  >
    <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white">{{ name }}</h3>
    <p class="text-gray-600 dark:text-gray-400">{{ description }}</p>
    <div class="mt-3 flex items-center text-blue-600 dark:text-blue-400 font-medium">
      <span>View component</span>
      <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
      </svg>
    </div>
  </router-link>
</template> 