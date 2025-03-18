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
        <span class="font-mono prop-name">{{ name }}</span>
        <span v-if="required" class="ml-2 text-xs font-medium required-badge">Required</span>
      </div>
    </td>
    <td class="px-4 py-3 text-sm font-mono prop-type">{{ type }}</td>
    <td class="px-4 py-3 text-sm font-mono prop-default">
      <span v-if="defaultValue">{{ defaultValue }}</span>
      <span v-else class="prop-default-empty">-</span>
    </td>
    <td class="px-4 py-3 text-sm prop-description">{{ description }}</td>
  </tr>
</template>

<style scoped>
.prop-name {
  color: var(--color-text-primary-rest);
}

.required-badge {
  color: var(--color-error-rest);
}

.prop-type, .prop-description {
  color: var(--color-text-secondary-rest);
}

.prop-default {
  color: var(--color-text-secondary-rest);
}

.prop-default-empty {
  color: var(--color-text-tertiary-rest);
}
</style> 