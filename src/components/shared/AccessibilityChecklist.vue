<script setup lang="ts">
interface AccessibilityItem {
  guideline: string;
  status: boolean;
  description: string;
}

defineProps({
  items: {
    type: Array as () => AccessibilityItem[],
    required: true,
    default: () => []
  }
});
</script>

<template>
  <div class="accessibility-container">
    <table class="w-full">
      <thead>
        <tr class="accessibility-border">
          <th class="text-left p-2">Guideline</th>
          <th class="text-left p-2">Status</th>
          <th class="text-left p-2">Description</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="index" class="accessibility-border">
          <td class="p-2 font-medium">{{ item.guideline }}</td>
          <td class="p-2">
            <span 
              v-if="item.status" 
              class="status-badge status-badge-success"
            >
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              Compliant
            </span>
            <span 
              v-else 
              class="status-badge status-badge-error"
            >
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
              Not Compliant
            </span>
          </td>
          <td class="p-2 accessibility-description">{{ item.description }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.accessibility-container {
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.75rem;
  padding: 1rem;
}

@media (min-width: 1024px) {
  .accessibility-container {
    padding: 1.5rem;
  }
}

.accessibility-border {
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.accessibility-description {
  color: var(--color-text-secondary-rest);
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge-success {
  background-color: var(--color-surface-success-rest);
  color: var(--color-text-success-rest);
}

.status-badge-error {
  background-color: var(--color-surface-error-rest);
  color: var(--color-text-error-rest);
}
</style> 