<script setup lang="ts">
import { BaseButton } from '@/design-system/components/core/button';
import { BaseBadge } from '@/design-system/components/core/badge';
</script>

<template>
  <div class="home-page">
    <div class="mb-12 text-center">
      <h1 class="text-4xl font-extrabold text-primary sm:text-5xl">
        Solar Design System
      </h1>
      <p class="mt-4 text-xl text-secondary max-w-3xl mx-auto">
        A modern, accessible, and customizable design system for building beautiful Vue applications.
      </p>
      <div class="mt-8 flex justify-center gap-4">
        <BaseButton size="lg" variant="primary">Get Started</BaseButton>
        <BaseButton size="lg" variant="outline">View on GitHub</BaseButton>
      </div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
      <!-- Feature 1 -->
      <div class="bg-surface-primary feature-card hover-card">
        <div class="feature-header">
          <div class="feature-icon bg-fill-brand-pale">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 icon-brand" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
            </svg>
          </div>
          <BaseBadge variant="brand" size="s">Design</BaseBadge>
        </div>
        <h3 class="text-lg font-semibold text-primary">Customizable</h3>
        <p class="mt-2 text-secondary">
          Easily customize components to match your brand with Tailwind CSS utility classes.
        </p>
      </div>
      
      <!-- Feature 2 -->
      <div class="bg-surface-primary feature-card hover-card">
        <div class="feature-header">
          <div class="feature-icon bg-fill-brand-pale">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 icon-brand" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <BaseBadge variant="success" size="s">Performance</BaseBadge>
        </div>
        <h3 class="text-lg font-semibold text-primary">Performant</h3>
        <p class="mt-2 text-secondary">
          Built with performance in mind, ensuring your applications stay fast and responsive.
        </p>
      </div>
      
      <!-- Feature 3 -->
      <div class="bg-surface-primary feature-card hover-card">
        <div class="feature-header">
          <div class="feature-icon bg-fill-brand-pale">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 icon-brand" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <BaseBadge variant="warning" size="s">Accessibility</BaseBadge>
        </div>
        <h3 class="text-lg font-semibold text-primary">Accessible</h3>
        <p class="mt-2 text-secondary">
          Designed with accessibility in mind, following WCAG guidelines for inclusive experiences.
        </p>
      </div>
    </div>
    
    <div class="mt-16 bg-surface-secondary code-block">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-2xl font-bold text-primary">Getting Started</h2>
        <BaseBadge variant="outline">v1.0</BaseBadge>
      </div>
      <p class="mt-4 text-secondary">
        Install the Solar Design System using npm:
      </p>
      <pre class="mt-4 code-snippet"><code>npm install solar-design-system</code></pre>
      
      <p class="mt-6 text-secondary">
        Import and use components in your Vue application:
      </p>
      <pre class="mt-4 code-snippet"><code>import { Button, Badge } from 'solar-design-system';

// In your component template
&lt;Button variant="primary"&gt;Click Me&lt;/Button&gt;
&lt;Badge variant="brand"&gt;New&lt;/Badge&gt;</code></pre>

      <div class="mt-8 flex justify-end">
        <a href="/foundation/tokens" class="link-brand">
          Explore Design Tokens →
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 1.5rem;
  border-radius: 0.5rem;
  transition: all 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.1);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.375rem;
}

.icon-brand {
  color: var(--color-brand-500);
}

.code-block {
  padding: 2rem;
  border-radius: var(--comp-modal-radius);
  border: 1px solid var(--color-border-primary-rest);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.code-snippet {
  background-color: var(--color-fill-grey-rest);
  padding: 1rem;
  border-radius: var(--comp-button-main-radius);
  overflow-x: auto;
  font-size: 0.875rem;
  border: 1px solid var(--color-border-primary-rest);
}

.link-brand {
  color: var(--color-text-brand-rest);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.link-brand:hover {
  color: var(--color-text-brand-hover);
}

.link-brand:active {
  color: var(--color-text-brand-press);
}

.text-primary {
  color: var(--color-text-primary-rest);
}

.text-primary:hover {
  color: var(--color-text-primary-hover);
}

.text-secondary {
  color: var(--color-text-secondary-rest);
}

.text-secondary:hover {
  color: var(--color-text-secondary-hover);
}

.bg-surface-primary {
  background-color: var(--color-surface-primary-rest);
}

.bg-surface-secondary {
  background-color: var(--color-surface-secondary-rest);
}

.bg-fill-brand-pale {
  background-color: var(--color-fill-brand-pale-rest);
}
</style> 