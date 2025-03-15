<script setup lang="ts">
defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  }
});
</script>

<template>
  <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4 lg:p-6">
    <table class="w-full">
      <thead>
        <tr class="border-b border-gray-200 dark:border-gray-700">
          <th class="text-left p-2">Guideline</th>
          <th class="text-left p-2">Status</th>
          <th class="text-left p-2">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="index" class="border-b border-gray-200 dark:border-gray-700">
          <td class="p-2 font-medium">{{ item.guideline }}</td>
          <td class="p-2">
            <span 
              v-if="item.status" 
              class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
            >
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Compliant
            </span>
            <span 
              v-else 
              class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400"
            >
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
              Not Compliant
            </span>
          </td>
          <td class="p-2 text-gray-600 dark:text-gray-400">{{ item.description }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template> 