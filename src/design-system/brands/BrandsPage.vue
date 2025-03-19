<script setup lang="ts">
import { inject, ref, computed, onMounted } from 'vue';
import { Badge } from '../badge';
import { ButtonMain as Button } from '../button';

// Get theme controls from provider
const currentBrand = inject('currentBrand', ref('evydcore'));
const setBrand = inject('setBrand', (brand: string) => {});

// Available brands with enhanced metadata
const brands = [
  { 
    id: 'evydcore', 
    name: 'EvydCore', 
    description: 'Default brand with blue accents',
    accentColor: 'var(--color-fill-brand-rest)'
  },
  { 
    id: 'bruhealth', 
    name: 'BruHealth', 
    description: 'Health-focused brand with teal accents',
    accentColor: 'var(--color-fill-brand-rest)'
  },
];

// Change the current brand with immediate UI update
const changeBrand = (brandId: string) => {
  if (typeof setBrand === 'function') {
    setBrand(brandId);
    // Update data-brand attribute to trigger immediate CSS changes
    document.documentElement.setAttribute('data-brand', brandId);
  }
};

// Computed property to get current brand info
const currentBrandInfo = computed(() => 
  brands.find(b => b.id === currentBrand.value) || brands[0]
);

// Get the other brand option for switching
const getOtherBrand = computed(() => 
  brands.find(b => b.id !== currentBrand.value) || brands[0]
);
</script>

<template>
  <div class="brands-page">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-primary">Brand Variants</h1>
      
      <!-- Brand Toggle Switch - Centralized control -->
      <div class="flex items-center gap-3">
        <span class="text-secondary">Select Brand:</span>
        <div class="brand-toggle bg-surface-secondary-rest border border-border-primary rounded-full p-1 flex">
          <button 
            v-for="brand in brands" 
            :key="brand.id"
            @click="changeBrand(brand.id)"
            :class="[
              'brand-toggle-btn px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-300',
              currentBrand === brand.id 
                ? 'bg-fill-brand-rest text-text-on-brand shadow-sm' 
                : 'text-secondary hover:text-primary'
            ]"
          >
            {{ brand.name }}
          </button>
        </div>
        
        <router-link 
          to="/foundation/colors" 
          class="px-4 py-2 rounded-md border border-border-primary flex items-center ml-2"
        >
          <span>View Color Tokens</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 ml-2">
            <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
          </svg>
        </router-link>
      </div>
    </div>
    
    <p class="text-secondary mb-8 max-w-3xl">
      The design system supports multiple brand variants through semantic tokens. 
      Each brand has its own color palette, but uses the same semantic token names, 
      allowing components to adapt to different brands without changing their code.
    </p>
    
    <div class="mb-12">
      <div class="mb-6">
        <h2 class="text-2xl font-semibold text-primary">Available Brands</h2>
        <p class="text-secondary mt-1">Click on a brand card to activate it and preview its theme.</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div 
          v-for="brand in brands" 
          :key="brand.id"
          :class="[
            'p-6 rounded-lg border transition-all duration-300 cursor-pointer',
            currentBrand === brand.id 
              ? 'border-border-brand-rest bg-fill-brand-pale-rest shadow-sm' 
              : 'border-border-primary-rest bg-surface-primary-rest hover:bg-surface-primary-hover hover:border-border-brand-rest'
          ]"
          @click="changeBrand(brand.id)"
        >
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-xl font-medium text-primary">{{ brand.name }}</h3>
            <Badge 
              v-if="currentBrand === brand.id" 
              variant="brand" 
              class="transition-colors duration-300"
            >
              Active
            </Badge>
          </div>
          <p class="text-secondary mb-6">{{ brand.description }}</p>
          
          <!-- Color samples with transitions -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div 
              v-for="(type, index) in ['Brand', 'Success', 'Warning', 'Danger']" 
              :key="type"
              class="color-sample transition-all duration-300"
            >
              <div 
                class="h-10 rounded-md mb-1 transition-colors duration-300"
                :class="{
                  'bg-fill-brand-rest': type === 'Brand',
                  'bg-fill-success-rest': type === 'Success',
                  'bg-fill-warning-rest': type === 'Warning',
                  'bg-fill-danger-rest': type === 'Danger'
                }"
              ></div>
              <span class="text-xs text-secondary">{{ type }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="component-preview mb-12">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold text-primary">Component Examples</h2>
        <div class="flex items-center gap-2">
          <span class="text-secondary">Current Brand:</span>
          <Badge variant="brand" class="transition-colors duration-300">
            {{ currentBrandInfo.name }}
          </Badge>
        </div>
      </div>
      <p class="text-secondary mb-6">
        See how components adapt to the current brand. Use the brand toggle at the top of the page to switch brands and see the changes.
      </p>
      
      <div class="p-6 bg-surface-secondary-rest rounded-lg">
        <h3 class="text-xl font-medium text-primary mb-4">Buttons</h3>
        <div class="flex flex-wrap gap-4 mb-8">
          <Button variant="primary" class="transition-colors duration-300">Primary Button</Button>
          <Button variant="secondary" class="transition-colors duration-300">Secondary Button</Button>
          <Button variant="outline" class="transition-colors duration-300">Outline Button</Button>
          <Button variant="ghost" class="transition-colors duration-300">Ghost Button</Button>
        </div>
        
        <h3 class="text-xl font-medium text-primary mb-4">Badges</h3>
        <div class="flex flex-wrap gap-4">
          <Badge variant="default" class="transition-colors duration-300">Default</Badge>
          <Badge variant="brand" class="transition-colors duration-300">Brand</Badge>
          <Badge variant="success" class="transition-colors duration-300">Success</Badge>
          <Badge variant="warning" class="transition-colors duration-300">Warning</Badge>
          <Badge variant="danger" class="transition-colors duration-300">Danger</Badge>
          <Badge variant="outline" class="transition-colors duration-300">Outline</Badge>
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
  padding: 2rem;
}

.color-sample {
  display: flex;
  flex-direction: column;
}

/* Add smooth transitions for brand changes */
:deep(.button),
:deep(.badge) {
  transition: all 0.3s ease-in-out;
}

/* Enhance hover states */
.color-sample:hover .h-10 {
  transform: scale(1.05);
}

/* Brand toggle styling */
.brand-toggle {
  position: relative;
}

.brand-toggle-btn {
  position: relative;
  z-index: 1;
}

/* Add visual feedback on card hover */
.grid > div:hover {
  transform: translateY(-2px);
}
</style> 