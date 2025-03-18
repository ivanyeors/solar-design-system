<template>
  <div class="guideline-example">
    <div class="flex gap-4 items-center">
      <Button variant="primary">Click Here</Button>
      <Button variant="secondary">Submit</Button>
    </div>
    <p class="mt-4 text-sm guideline-text-error">
      Avoid generic, non-descriptive labels
    </p>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script>

<style scoped>
.guideline-example {
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  padding: 1rem;
}

.guideline-text-error {
  color: var(--color-text-error-rest);
}
</style> 