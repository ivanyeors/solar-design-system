<template>
  <div class="anatomy-example">
    <div class="relative inline-block">
      <Button variant="primary" size="lg">
        <template #leading-icon>
          <i class="icon-mail"></i>
        </template>
        Send Message
        <template #trailing-icon>
          <i class="icon-arrow-right"></i>
        </template>
      </Button>
      
      <!-- Anatomy Labels -->
      <div class="absolute -top-6 left-0 text-xs anatomy-label">1. Container</div>
      <div class="absolute top-1/2 -translate-y-1/2 -left-24 text-xs anatomy-label">2. Leading Icon</div>
      <div class="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 text-xs anatomy-label">3. Label</div>
      <div class="absolute top-1/2 -translate-y-1/2 -right-24 text-xs anatomy-label">4. Trailing Icon</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '../../ui/Button.vue';
</script>

<style scoped>
.anatomy-example {
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  padding: 2rem;
}

.anatomy-label {
  color: var(--color-text-secondary-rest);
}
</style> 