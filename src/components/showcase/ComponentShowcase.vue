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
  <div class="showcase-container">
    <!-- Component header -->
    <div class="showcase-header">
      <h2 class="showcase-title">{{ title }}</h2>
      <p v-if="description" class="showcase-description">{{ description }}</p>
    </div>
    
    <!-- Tab navigation -->
    <div class="showcase-tabs-border">
      <nav class="flex -mb-px">
        <button
          @click="activeTab = 'preview'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'preview'
              ? 'tab-active'
              : 'tab-inactive'
          ]"
        >
          Preview
        </button>
        <button
          @click="activeTab = 'code'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'code'
              ? 'tab-active'
              : 'tab-inactive'
          ]"
        >
          Code
        </button>
        <button
          @click="activeTab = 'props'"
          :class="[
            'px-4 py-3 text-sm font-medium border-b-2 focus:outline-none',
            activeTab === 'props'
              ? 'tab-active'
              : 'tab-inactive'
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
        <pre class="code-block"><code><slot name="code"></slot></code></pre>
      </div>
      
      <!-- Props tab -->
      <div v-if="activeTab === 'props'" class="p-6">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y showcase-table-divider">
            <thead>
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Prop</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Type</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Default</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Description</th>
              </tr>
            </thead>
            <tbody class="showcase-table-body showcase-table-divider">
              <slot name="props"></slot>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.showcase-container {
  background-color: var(--color-surface-primary-rest);
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border-primary-rest);
  overflow: hidden;
}

.showcase-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.showcase-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary-rest);
}

.showcase-description {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary-rest);
}

.showcase-tabs-border {
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.tab-active {
  border-color: var(--color-primary-rest);
  color: var(--color-primary-rest);
}

.tab-inactive {
  border-color: transparent;
  color: var(--color-text-secondary-rest);
}

.tab-inactive:hover {
  color: var(--color-text-secondary-hover);
  border-color: var(--color-border-secondary-hover);
}

.code-block {
  background-color: var(--color-surface-secondary-rest);
  padding: 1rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  font-size: 0.875rem;
  color: var(--color-text-secondary-rest);
}

.showcase-table-divider {
  border-color: var(--color-border-primary-rest);
}

.showcase-table-body {
  background-color: var(--color-surface-primary-rest);
}

.table-header {
  color: var(--color-text-secondary-rest);
}
</style> 