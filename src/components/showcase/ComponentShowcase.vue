<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  title: string;
  description?: string;
  componentName: string;
}>();

const activeTab = ref('preview');
</script>

<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden dark:bg-gray-900 dark:border-gray-800">
    <!-- Component header -->
    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-800">
      <h2 class="text-xl font-semibold text-gray-900 dark:text-white">{{ title }}</h2>
      <p v-if="description" class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ description }}</p>
    </div>
    
    <!-- Tab navigation -->
    <div class="border-b border-gray-200 dark:border-gray-800">
      <nav class="flex -mb-px">
        <button
          @click="activeTab = 'preview'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'preview'
              ? 'border-primary-500 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-700'
          ]"
        >
          Preview
        </button>
        <button
          @click="activeTab = 'code'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'code'
              ? 'border-primary-500 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-700'
          ]"
        >
          Code
        </button>
        <button
          @click="activeTab = 'props'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'props'
              ? 'border-primary-500 text-primary-600 dark:text-primary-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-700'
          ]"
        >
          Props
        </button>
      </nav>
    </div>
    
    <!-- Tab content -->
    <div>
      <!-- Preview tab -->
      <div v-if="activeTab === 'preview'" class="p-6">
        <div class="flex flex-wrap gap-4">
          <slot name="preview"></slot>
        </div>
      </div>
      
      <!-- Code tab -->
      <div v-if="activeTab === 'code'" class="p-6">
        <pre class="bg-gray-100 p-4 rounded-md overflow-x-auto text-sm dark:bg-gray-800 dark:text-gray-300"><code><slot name="code"></slot></code></pre>
      </div>
      
      <!-- Props tab -->
      <div v-if="activeTab === 'props'" class="p-6">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-800">
            <thead>
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Prop</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Type</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Default</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider dark:text-gray-400">Description</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200 dark:bg-gray-900 dark:divide-gray-800">
              <slot name="props"></slot>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Any additional scoped styles */
</style> 