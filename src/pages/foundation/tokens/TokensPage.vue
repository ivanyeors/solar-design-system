<template>
  <div class="tokens-page">
    <h1>{{ title || 'Design Tokens' }}</h1>
    <section class="documentation">
      <h2>Overview</h2>
      <p>Design tokens are the visual design atoms of the design system—specifically, they are named entities that store visual design attributes.</p>

      <template v-if="!title">
        <!-- General tokens documentation -->
        <h2>Token Categories</h2>
        <div class="token-categories">
          <div v-for="category in categories" :key="category.name" class="token-category">
            <h3>{{ category.name }}</h3>
            <p>{{ category.description }}</p>
          </div>
        </div>
      </template>

      <template v-else-if="title === 'Colors'">
        <!-- Colors specific documentation -->
        <h2>Color Palette</h2>
        <div class="color-grid">
          <div v-for="token in colorTokens" :key="token.name" class="color-item">
            <div class="color-preview" :style="{ backgroundColor: token.value }"></div>
            <div class="color-info">
              <code>{{ token.name }}</code>
              <span>{{ token.value }}</span>
            </div>
          </div>
        </div>
      </template>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { TOKEN_TYPES, TokenDefinition, getCssVar } from '../../../lib/tokens';

interface Props {
  title?: string;
}

const props = withDefaults(defineProps<Props>(), {
  title: ''
});

const categories = [
  {
    name: 'Colors',
    description: 'Color tokens for text, backgrounds, borders, and other visual elements'
  },
  {
    name: 'Typography',
    description: 'Font families, sizes, weights, and line heights'
  },
  {
    name: 'Spacing',
    description: 'Margin, padding, and gap values for consistent spacing'
  },
  {
    name: 'Breakpoints',
    description: 'Responsive design breakpoints for different screen sizes'
  }
];

const colorTokens = computed(() => {
  const tokens: TokenDefinition[] = [];
  const colorTypes = [
    TOKEN_TYPES.COLOR_TEXT,
    TOKEN_TYPES.COLOR_FILL,
    TOKEN_TYPES.COLOR_BORDER,
    TOKEN_TYPES.COLOR_SURFACE
  ];

  colorTypes.forEach(type => {
    const vars = document.documentElement.style;
    for (let i = 0; i < vars.length; i++) {
      const prop = vars[i];
      if (prop.startsWith(`--${type}`)) {
        tokens.push({
          name: prop,
          value: getCssVar(prop.substring(2)),
          usage: `${type} token`
        });
      }
    }
  });

  return tokens;
});
</script>

<style scoped>
.tokens-page {
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
  margin-bottom: 0.5rem;
}

.token-categories {
  display: grid;
  gap: 2rem;
  margin: 2rem 0;
}

.token-category {
  padding: 1.5rem;
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  background: var(--color-surface-primary-rest);
}

.color-grid {
  display: grid;
  gap: 1.5rem;
  margin: 2rem 0;
}

.color-item {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.color-preview {
  width: 3rem;
  height: 3rem;
  border-radius: 0.375rem;
  border: 1px solid var(--color-border-primary-rest);
}

.color-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

code {
  font-family: monospace;
  font-size: 0.875rem;
  color: var(--color-text-code-rest);
  background: var(--color-surface-code-rest);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

@media (min-width: 768px) {
  .token-categories {
    grid-template-columns: repeat(2, 1fr);
  }

  .color-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}
</style> 