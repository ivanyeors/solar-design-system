<template>
  <div class="spacing-example">
    <div class="flex flex-col gap-8">
      <!-- Horizontal spacing example -->
      <div>
        <h4 class="text-sm font-medium mb-4 spacing-heading">Horizontal Spacing (8px)</h4>
        <div class="flex gap-2 items-center">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
        </div>
      </div>
      
      <!-- Vertical spacing example -->
      <div>
        <h4 class="text-sm font-medium mb-4 spacing-heading">Vertical Spacing (16px)</h4>
        <div class="flex flex-col gap-4">
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script>

<style scoped>
.spacing-example {
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  padding: 2rem;
}

.spacing-heading {
  color: var(--color-text-primary-rest);
}
</style> 