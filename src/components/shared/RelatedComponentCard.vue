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
    class="related-component-card"
  >
    <h3 class="related-component-title">{{ name }}</h3>
    <p class="related-component-description">{{ description }}</p>
    <div class="related-component-link">
      <span>View component</span>
      <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
      </svg>
    </div>
  </router-link>
</template>

<style scoped>
.related-component-card {
  display: block;
  padding: 1.25rem;
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.75rem;
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s;
}

.related-component-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-color: var(--color-primary-rest);
  background-color: var(--color-surface-brand-subtle);
}

.related-component-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary-rest);
}

.related-component-description {
  color: var(--color-text-secondary-rest);
}

.related-component-link {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  color: var(--color-primary-rest);
  font-weight: 500;
}
</style> 