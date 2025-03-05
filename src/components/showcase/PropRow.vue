<script setup lang="ts">
defineProps<{
  name: string;
  type: string;
  defaultValue?: string;
  description: string;
  required?: boolean;
}>();
</script>

<template>
  <tr>
    <td class="px-4 py-3 text-sm">
      <div class="flex items-center">
        <span class="font-mono text-gray-900 dark:text-white">{{ name }}</span>
        <span v-if="required" class="ml-2 text-xs font-medium text-red-500">Required</span>
      </div>
    </td>
    <td class="px-4 py-3 text-sm font-mono text-gray-700 dark:text-gray-300">{{ type }}</td>
    <td class="px-4 py-3 text-sm font-mono text-gray-700 dark:text-gray-300">
      <span v-if="defaultValue">{{ defaultValue }}</span>
      <span v-else class="text-gray-400 dark:text-gray-600">-</span>
    </td>
    <td class="px-4 py-3 text-sm text-gray-700 dark:text-gray-300">{{ description }}</td>
  </tr>
</template> 