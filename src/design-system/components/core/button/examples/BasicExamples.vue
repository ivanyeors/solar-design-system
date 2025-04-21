<script setup lang="ts">
import { Button, ButtonOption, ButtonPill, ButtonCard } from '../';
</script>

<template>
  <div class="button-examples">
    <h3>Basic Button Examples</h3>
    <div class="examples-grid">
      <div class="example-item">
        <Button>Primary Button</Button>
      </div>
      <div class="example-item">
        <ButtonOption>Option Button</ButtonOption>
      </div>
      <div class="example-item">
        <ButtonPill>Pill Button</ButtonPill>
      </div>
      <div class="example-item">
        <ButtonCard>Card Button</ButtonCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.button-examples {
  padding: 1rem;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.example-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.5rem;
}
</style> 