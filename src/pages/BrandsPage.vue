<script setup lang="ts">
import { inject, ref } from 'vue';
import Badge from '../components/ui/Badge.vue';
import Button from '../components/ui/Button.vue';

// Get theme controls from provider
const currentBrand = inject('currentBrand', ref('evydcore'));
const setBrand = inject('setBrand', (brand: string) => {});

// Available brands
const brands = [
  { id: 'evydcore', name: 'EvydCore', description: 'Default brand with blue accents' },
  { id: 'bruhealth', name: 'BruHealth', description: 'Health-focused brand with teal accents' },
];

// Change the current brand
const changeBrand = (brandId: string) => {
  if (typeof setBrand === 'function') {
    setBrand(brandId);
  }
};
</script>

<template>
  <div class="brands-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-primary">Brand Variants</h1>
      <router-link 
        to="/foundation/colors" 
        class="px-4 py-2 rounded-md border border-border-primary flex items-center"
      >
        <span>View Color Tokens</span>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 ml-2">
          <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
        </svg>
      </router-link>
    </div>
    <p class="text-secondary mb-8 max-w-3xl">
      The design system supports multiple brand variants through semantic tokens. 
      Each brand has its own color palette, but uses the same semantic token names, 
      allowing components to adapt to different brands without changing their code.
    </p>
    
    <div class="mb-12">
      <h2 class="text-2xl font-semibold text-primary mb-4">Available Brands</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="brand in brands" 
          :key="brand.id"
          :class="[
            'p-6 rounded-lg border transition-colors',
            currentBrand === brand.id 
              ? 'border-border-brand-rest bg-fill-brand-pale-rest' 
              : 'border-border-primary-rest bg-surface-primary-rest hover:bg-surface-primary-hover'
          ]"
        >
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-medium text-primary">{{ brand.name }}</h3>
            <Button 
              v-if="currentBrand !== brand.id"
              size="sm" 
              variant="outline"
              @click="changeBrand(brand.id)"
            >
              Switch to {{ brand.name }}
            </Button>
            <Badge v-else variant="brand">Active Brand</Badge>
          </div>
          <p class="text-secondary mb-6">{{ brand.description }}</p>
          
          <!-- Color samples -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="color-sample">
              <div class="h-10 rounded-md bg-fill-brand-rest mb-1"></div>
              <span class="text-xs text-secondary">Brand</span>
            </div>
            <div class="color-sample">
              <div class="h-10 rounded-md bg-fill-success-rest mb-1"></div>
              <span class="text-xs text-secondary">Success</span>
            </div>
            <div class="color-sample">
              <div class="h-10 rounded-md bg-fill-warning-rest mb-1"></div>
              <span class="text-xs text-secondary">Warning</span>
            </div>
            <div class="color-sample">
              <div class="h-10 rounded-md bg-fill-danger-rest mb-1"></div>
              <span class="text-xs text-secondary">Danger</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="component-preview mb-12">
      <h2 class="text-2xl font-semibold text-primary mb-4">Component Examples</h2>
      <p class="text-secondary mb-6">
        See how components adapt to the current brand. Try switching brands to see the difference.
      </p>
      
      <div class="p-6 bg-surface-secondary-rest rounded-lg">
        <h3 class="text-xl font-medium text-primary mb-4">Buttons</h3>
        <div class="flex flex-wrap gap-4 mb-8">
          <Button variant="primary">Primary Button</Button>
          <Button variant="secondary">Secondary Button</Button>
          <Button variant="outline">Outline Button</Button>
          <Button variant="ghost">Ghost Button</Button>
        </div>
        
        <h3 class="text-xl font-medium text-primary mb-4">Badges</h3>
        <div class="flex flex-wrap gap-4">
          <Badge variant="default">Default</Badge>
          <Badge variant="brand">Brand</Badge>
          <Badge variant="success">Success</Badge>
          <Badge variant="warning">Warning</Badge>
          <Badge variant="danger">Danger</Badge>
          <Badge variant="outline">Outline</Badge>
        </div>
      </div>
    </div>
    
    <div class="implementation-guide mb-12">
      <h2 class="text-2xl font-semibold text-primary mb-4">Adding a New Brand</h2>
      <p class="text-secondary mb-4">
        To add a new brand to the design system, you need to:
      </p>
      
      <ol class="list-decimal pl-5 space-y-2 text-secondary mb-6">
        <li>Create a new SCSS file with your brand colors (e.g., <code>_newbrand_colors_light.scss</code>)</li>
        <li>Create brand-specific semantic tokens (e.g., <code>_newbrand_comp.scss</code>)</li>
        <li>Import your brand files in <code>semanticTokens.scss</code></li>
        <li>Add your brand to the theme provider</li>
      </ol>
      
      <pre class="bg-fill-grey-rest p-4 rounded-md overflow-x-auto text-sm mb-4">
// Example semantic token definition
:root[data-brand="newbrand"] {
  --color-fill-brand-rest: #6b21a8;
  --color-fill-brand-hover: #7c3aed;
  --color-fill-brand-press: #5b21b6;
  --color-fill-brand-focus: #6b21a8;
  
  // ... more token definitions
}
      </pre>
    </div>
  </div>
</template>

<style scoped>
.brands-page {
  max-width: 1200px;
  margin: 0 auto;
}

.color-sample {
  display: flex;
  flex-direction: column;
}
</style> 