<script setup lang="ts">
import { ref } from 'vue';

interface Token {
  name: string;
  value: string;
  usage: string;
}

defineProps<{
  tokens: Token[];
}>();

const copiedToken = ref<string | null>(null);

const copyToClipboard = async (token: Token) => {
  try {
    await navigator.clipboard.writeText(token.value);
    copiedToken.value = token.name;
    setTimeout(() => {
      copiedToken.value = null;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy token:', err);
  }
};
</script>

<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
      <thead class="bg-gray-50 dark:bg-gray-800">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
            Token
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
            Value
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
            Usage
          </th>
        </tr>
      </thead>
      <tbody class="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-700">
        <tr v-for="token in tokens" :key="token.name">
          <td class="px-6 py-4 whitespace-nowrap">
            <code class="font-mono text-sm text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
              {{ token.name }}
            </code>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center gap-2">
              <code class="font-mono text-sm text-gray-900 dark:text-white bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                {{ token.value }}
              </code>
              <button
                class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                @click="copyToClipboard(token)"
                :title="'Copy token value'"
              >
                <i class="icon-copy w-4 h-4" :class="{ 'text-green-500': copiedToken === token.name }"></i>
              </button>
            </div>
          </td>
          <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
            {{ token.usage }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.icon-copy {
  @apply transition-colors duration-200;
}
</style> 