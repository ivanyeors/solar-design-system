<script setup lang="ts">
defineProps({
  versions: {
    type: Array,
    required: true,
    default: () => []
  }
});
</script>

<template>
  <div class="space-y-6">
    <div 
      v-for="(version, index) in versions" 
      :key="index"
      class="relative pl-8 pb-6"
      :class="index !== versions.length - 1 ? 'border-l-2 border-gray-200 dark:border-gray-700' : ''"
    >
      <!-- Version dot -->
      <div class="absolute left-[-8px] w-4 h-4 rounded-full bg-blue-500 dark:bg-blue-400 border-4 border-white dark:border-gray-900"></div>
      
      <!-- Version content -->
      <div class="bg-gray-50 dark:bg-gray-800/50 rounded-lg p-4 ml-4">
        <div class="flex flex-wrap justify-between items-start mb-3">
          <h3 class="font-semibold text-lg text-gray-900 dark:text-white">{{ version.version }}</h3>
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ version.date }}</span>
        </div>
        
        <ul class="space-y-2">
          <li 
            v-for="(change, changeIndex) in version.changes" 
            :key="changeIndex"
            class="text-gray-600 dark:text-gray-300 flex items-start"
          >
            <span class="text-blue-500 dark:text-blue-400 mr-2">•</span>
            <span>{{ change }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Timeline styling */
.relative:last-child {
  padding-bottom: 0;
}
</style> 