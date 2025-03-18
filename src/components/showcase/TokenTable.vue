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
    <table class="min-w-full divide-y token-table-divider">
      <thead class="token-table-header">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium token-header-text uppercase tracking-wider">
            Token
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium token-header-text uppercase tracking-wider">
            Value
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium token-header-text uppercase tracking-wider">
            Usage
          </th>
        </tr>
      </thead>
      <tbody class="token-table-body divide-y token-table-divider">
        <tr v-for="token in tokens" :key="token.name">
          <td class="px-6 py-4 whitespace-nowrap">
            <code class="font-mono text-sm token-code-text token-code-bg px-2 py-1 rounded">
              {{ token.name }}
            </code>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center gap-2">
              <code class="font-mono text-sm token-code-text token-code-bg px-2 py-1 rounded">
                {{ token.value }}
              </code>
              <button
                class="copy-button"
                :class="{ 'copied': copiedToken === token.name }"
                @click="copyToClipboard(token)"
                :title="'Copy token value'"
              >
                <i class="icon-copy w-4 h-4"></i>
              </button>
            </div>
          </td>
          <td class="px-6 py-4 text-sm token-usage-text">
            {{ token.usage }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.token-table-divider {
  border-color: var(--color-border-primary-rest);
}

.token-table-header {
  background-color: var(--color-surface-secondary-rest);
}

.token-table-body {
  background-color: var(--color-surface-primary-rest);
}

.token-header-text {
  color: var(--color-text-secondary-rest);
}

.token-code-text {
  color: var(--color-text-primary-rest);
}

.token-code-bg {
  background-color: var(--color-surface-secondary-rest);
}

.token-usage-text {
  color: var(--color-text-secondary-rest);
}

.copy-button {
  color: var(--color-text-tertiary-rest);
  transition: all 0.2s;
}

.copy-button:hover {
  color: var(--color-text-secondary-hover);
}

.copy-button.copied {
  color: var(--color-success-rest);
}

.icon-copy {
  transition: color 0.2s;
}
</style> 