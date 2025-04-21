<template>
  <div class="brands-page">
    <h1>Brands</h1>
    <section class="documentation">
      <h2>Overview</h2>
      <p>Our brand guidelines ensure consistent representation across all platforms and materials.</p>

      <h2>Logo Usage</h2>
      <div class="logo-grid">
        <div class="logo-item">
          <h3>Primary Logo</h3>
          <div class="logo-preview">
            <!-- Logo placeholder -->
            <div class="logo-placeholder"></div>
          </div>
          <div class="logo-guidelines">
            <h4>Usage Guidelines</h4>
            <ul>
              <li>Maintain clear space around the logo</li>
              <li>Do not alter the logo colors</li>
              <li>Do not distort or rotate the logo</li>
              <li>Use approved color variations only</li>
            </ul>
          </div>
        </div>
      </div>

      <h2>Color Palette</h2>
      <div class="color-grid">
        <div v-for="color in brandColors" :key="color.name" class="color-item">
          <div class="color-preview" :style="{ backgroundColor: color.value }"></div>
          <div class="color-info">
            <h4>{{ color.name }}</h4>
            <code>{{ color.value }}</code>
            <p>{{ color.usage }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { TokenDefinition } from '../../../lib/tokens';

const brandColors = ref<TokenDefinition[]>([
  {
    name: 'Primary Brand',
    value: 'var(--color-brand-primary)',
    usage: 'Main brand color for key elements'
  },
  {
    name: 'Secondary Brand',
    value: 'var(--color-brand-secondary)',
    usage: 'Supporting brand color'
  },
  {
    name: 'Accent',
    value: 'var(--color-brand-accent)',
    usage: 'Highlights and call-to-actions'
  }
]);
</script>

<style scoped>
.brands-page {
  padding: 2rem;
}

.documentation {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 2rem;
  font-size: 2.5rem;
  font-weight: 600;
}

h2 {
  margin: 2rem 0 1rem;
  font-size: 1.75rem;
  font-weight: 500;
}

h3 {
  font-size: 1.25rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

h4 {
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.logo-grid {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.logo-item {
  padding: 2rem;
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  background: var(--color-surface-primary-rest);
}

.logo-preview {
  margin: 2rem 0;
  display: flex;
  justify-content: center;
}

.logo-placeholder {
  width: 200px;
  height: 80px;
  background: var(--color-surface-secondary-rest);
  border: 2px dashed var(--color-border-primary-rest);
  border-radius: 0.375rem;
}

.logo-guidelines ul {
  list-style-type: disc;
  margin-left: 1.5rem;
  margin-top: 0.5rem;
}

.logo-guidelines li {
  margin-bottom: 0.5rem;
  color: var(--color-text-primary-rest);
}

.color-grid {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.color-item {
  display: flex;
  gap: 1.5rem;
  padding: 1.5rem;
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  background: var(--color-surface-primary-rest);
}

.color-preview {
  width: 6rem;
  height: 6rem;
  border-radius: 0.375rem;
  border: 1px solid var(--color-border-primary-rest);
}

.color-info {
  flex: 1;
}

code {
  display: inline-block;
  font-family: monospace;
  font-size: 0.875rem;
  color: var(--color-text-code-rest);
  background: var(--color-surface-code-rest);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  margin: 0.5rem 0;
}

@media (min-width: 768px) {
  .color-grid {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  }
}
</style> 