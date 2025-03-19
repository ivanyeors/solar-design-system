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
            'showcase-tab',
            activeTab === 'preview'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
          ]"
        >
          Preview
        </button>
        <button
          @click="activeTab = 'code'"
          :class="[
            'showcase-tab',
            activeTab === 'code'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
          ]"
        >
          Code
        </button>
        <button
          @click="activeTab = 'props'"
          :class="[
            'showcase-tab',
            activeTab === 'props'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
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
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-xs);
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

.showcase-tab {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-m);
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  border-bottom: 2px solid transparent;
  transition: all var(--transition-fast);
}

.showcase-tab:focus {
  outline: none;
}

.showcase-tab:focus-visible {
  box-shadow: var(--shadow-focus);
}

.showcase-tab--active {
  color: var(--color-text-brand-rest);
  border-bottom-color: var(--color-border-brand-rest);
  background-color: transparent;
}

.showcase-tab--active:hover {
  color: var(--color-text-brand-hover);
  border-bottom-color: var(--color-border-brand-hover);
}

.showcase-tab--inactive {
  color: var(--color-text-secondary-rest);
  border-bottom-color: transparent;
  background-color: transparent;
}

.showcase-tab--inactive:hover {
  color: var(--color-text-secondary-hover);
  border-bottom-color: var(--color-border-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

.code-block {
  background-color: var(--color-surface-code-rest);
  padding: var(--comp-button-main-v-padding-m);
  border-radius: var(--comp-button-main-radius);
  overflow-x: auto;
  font-size: var(--font-size-14);
  color: var(--color-text-code-rest);
  font-family: var(--font-family-mono);
}

.showcase-table-divider {
  border-color: var(--color-border-primary-rest);
}

.showcase-table-body {
  background-color: var(--color-surface-primary-rest);
}

.table-header {
  color: var(--color-text-secondary-rest);
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}
</style> 