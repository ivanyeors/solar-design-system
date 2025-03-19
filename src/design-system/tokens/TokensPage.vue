<script setup lang="ts">
import { ref, computed, inject, onMounted, onUnmounted, watch } from 'vue';
import { TOKEN_TYPES, TOKEN_STATES, getCssVar } from '../../lib/tokens';
import { ButtonMain as Button } from '../button';
import { Badge } from '../badge';

// Define props including an optional title
const props = defineProps({
  title: {
    type: String,
    default: 'Design System Tokens'
  }
});

// Get theme controls from provider
const themeMode = inject('themeMode', ref('system'));
const effectiveTheme = inject('effectiveTheme', ref('light'));
const currentBrand = inject('currentBrand', ref('evydcore'));
const setThemeMode = inject('setThemeMode', (mode: string) => {});
const setBrand = inject('setBrand', (brand: string) => {});

// Add a refresh trigger to force component updates when theme/brand changes
const refreshTrigger = ref(Date.now());

const brands = [
  { id: 'evydcore', name: 'EvydCore' },
  { id: 'bruhealth', name: 'BruHealth' },
];

// Define interfaces for token types
interface TokenState {
  id: string;
  name: string;
}

interface TokenCategory {
  id: string;
  name: string;
  prefix: string;
}

interface TokenInfo {
  name: string;
  displayName: string;
  value: string;
}

interface CommonTokens {
  text: string[];
  fill: string[];
  border: string[];
  icon: string[];
  surface: string[];
  [key: string]: string[];
}

// Token categories to display
const categories: TokenCategory[] = [
  { id: 'text', name: 'Text Colors', prefix: TOKEN_TYPES.COLOR_TEXT },
  { id: 'fill', name: 'Background Colors', prefix: TOKEN_TYPES.COLOR_FILL },
  { id: 'border', name: 'Border Colors', prefix: TOKEN_TYPES.COLOR_BORDER },
  { id: 'icon', name: 'Icon Colors', prefix: TOKEN_TYPES.COLOR_ICON },
  { id: 'surface', name: 'Surface Colors', prefix: TOKEN_TYPES.COLOR_SURFACE },
];

// Component token categories
const componentCategories: TokenCategory[] = [
  { id: 'button', name: 'Button', prefix: TOKEN_TYPES.COMP_BUTTON },
  { id: 'badge', name: 'Badge', prefix: TOKEN_TYPES.COMP_BADGE },
  { id: 'input', name: 'Input', prefix: TOKEN_TYPES.COMP_INPUT },
  { id: 'modal', name: 'Modal', prefix: TOKEN_TYPES.COMP_MODAL },
];

// Common token names to look for
const commonTokens: CommonTokens = {
  text: ['primary', 'secondary', 'brand', 'danger', 'success', 'warning', 'info', 'note'],
  fill: ['neutral', 'grey', 'brand', 'brand-pale', 'danger', 'success', 'warning', 'info', 'note'],
  border: ['primary', 'brand', 'danger', 'success', 'warning', 'info'],
  icon: ['primary', 'secondary', 'brand', 'danger', 'success', 'warning', 'info', 'note'],
  surface: ['canvas', 'primary', 'secondary']
};

// States to display for each token
const states: TokenState[] = [
  { id: TOKEN_STATES.REST, name: 'Default' },
  { id: TOKEN_STATES.HOVER, name: 'Hover' },
  { id: TOKEN_STATES.PRESS, name: 'Pressed' },
  { id: TOKEN_STATES.FOCUS, name: 'Focus' },
  { id: TOKEN_STATES.DISABLED, name: 'Disabled' }
];

// Function to generate token list for a category
const getTokensForCategory = (category: string, prefix: string): TokenInfo[] => {
  const tokens: TokenInfo[] = [];
  const baseNames = commonTokens[category] || ['main'];

  // Use refreshTrigger to force reevaluation when theme/brand changes
  if (refreshTrigger.value) {
    baseNames.forEach((baseName: string) => {
      states.forEach(state => {
        const tokenName = `${prefix}-${baseName}-${state.id}`;
        const value = getCssVar(tokenName);
        if (value) {
          tokens.push({
            name: tokenName,
            displayName: `${baseName} (${state.name})`,
            value
          });
        }
      });
    });
  }

  return tokens;
};

// Toggle dark/light mode
const toggleMode = () => {
  const newMode = effectiveTheme.value === 'light' ? 'dark' : 'light';
  setThemeMode(newMode);
  
  // Update UI immediately to reflect changes
  document.documentElement.setAttribute('data-theme', newMode);
  
  if (newMode === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  
  // Force refresh all displayed token values
  refreshTrigger.value = Date.now();
};

// Switch brand
const switchBrand = (brand: string) => {
  setBrand(brand);
  
  // Update data-brand attribute to trigger CSS changes
  document.documentElement.setAttribute('data-brand', brand);
  
  // Force refresh token values after brand switch
  setTimeout(() => {
    refreshTrigger.value = Date.now();
  }, 50);
};

// Get contrasting text color for a background
const getContrastText = (hexColor: string): string => {
  // Extract RGB components (handle rgba and short hex formats too)
  let r = 0, g = 0, b = 0;
  
  if (!hexColor || hexColor === 'transparent') return '#000000';
  
  if (hexColor.startsWith('rgb')) {
    const rgbMatch = hexColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
    if (rgbMatch) {
      r = parseInt(rgbMatch[1]);
      g = parseInt(rgbMatch[2]);
      b = parseInt(rgbMatch[3]);
    }
  } else {
    // Remove # if present
    hexColor = hexColor.replace('#', '');
    
    // Handle shorthand hex
    if (hexColor.length === 3) {
      hexColor = hexColor.split('').map((c: string) => c + c).join('');
    }
    
    // Parse the hex values
    r = parseInt(hexColor.substr(0, 2), 16) || 0;
    g = parseInt(hexColor.substr(2, 2), 16) || 0;
    b = parseInt(hexColor.substr(4, 2), 16) || 0;
  }
  
  // Calculate relative luminance
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
  
  // Use white text for dark backgrounds, black for light
  return luminance > 0.5 ? 'var(--color-text-primary-rest)' : 'var(--color-text-neutrallight-rest)';
};

// Watch for theme/brand changes from the provider
watch([effectiveTheme, currentBrand], () => {
  refreshTrigger.value = Date.now();
});

// Setup observer for theme attribute changes
onMounted(() => {
  // Initialize based on document state
  const dataTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const dataBrand = document.documentElement.getAttribute('data-brand') || 'evydcore';
  
  // Ensure UI is in sync with actual DOM state
  if (effectiveTheme.value !== dataTheme) {
    effectiveTheme.value = dataTheme as 'light' | 'dark';
  }
  
  if (currentBrand.value !== dataBrand) {
    currentBrand.value = dataBrand as 'evydcore' | 'bruhealth';
  }
  
  // Setup observer for attribute changes on document element
  const themeObserver = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.type === 'attributes') {
        if (mutation.attributeName === 'data-theme') {
          const newTheme = document.documentElement.getAttribute('data-theme') || 'light';
          effectiveTheme.value = newTheme as 'light' | 'dark';
          refreshTrigger.value = Date.now();
        } else if (mutation.attributeName === 'data-brand') {
          const newBrand = document.documentElement.getAttribute('data-brand') || 'evydcore';
          currentBrand.value = newBrand as 'evydcore' | 'bruhealth';
          refreshTrigger.value = Date.now();
        }
      }
    });
  });
  
  // Start observing
  themeObserver.observe(document.documentElement, { 
    attributes: true, 
    attributeFilter: ['data-theme', 'data-brand'] 
  });
  
  // Cleanup function
  onUnmounted(() => {
    themeObserver.disconnect();
  });
});
</script>

<template>
  <div class="tokens-page">
    <!-- Update right sidebar positioning -->
    <div class="right-sidebar bg-surface-primary-rest border-l border-border-primary-rest fixed right-0 overflow-y-auto p-6">
      <nav class="space-y-4">
        <h3 class="text-sm font-semibold text-text-secondary-rest uppercase tracking-wider mb-4">On this page</h3>
        <ul class="space-y-3">
          <li>
            <a href="#semantic-tokens" class="text-text-primary-rest hover:text-text-brand-hover">Semantic Tokens</a>
          </li>
          <li>
            <a href="#component-tokens" class="text-text-primary-rest hover:text-text-brand-hover">Component Tokens</a>
          </li>
          <li>
            <a href="#token-usage" class="text-text-primary-rest hover:text-text-brand-hover">Using Tokens</a>
          </li>
        </ul>
      </nav>
    </div>

    <div class="content-with-sidebar">
      <div class="header-controls bg-surface-primary mb-12 rounded-lg">
        <div class="px-8 py-6">
          <h1 class="text-3xl font-bold text-text-primary-rest mb-6">{{ props.title }}</h1>
          
          <div class="flex flex-col space-y-6">
            <!-- Theme Controls Row -->
            <div class="flex items-center justify-between">
              <button 
                class="px-4 py-2 rounded-md bg-fill-brand-pale-rest text-text-brand-rest border border-border-brand-rest hover:bg-fill-brand-pale-hover focus:outline-none transition-colors flex items-center space-x-2" 
                @click="toggleMode"
              >
                <span class="text-sm font-medium">Switch to {{ effectiveTheme === 'light' ? 'Dark' : 'Light' }} Mode</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                  <path v-if="effectiveTheme === 'light'" d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                  <path v-else fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
            
            <!-- Brand Controls Row -->
            <div class="flex items-center space-x-6">
              <div class="brand-selector flex space-x-2">
                <button 
                  v-for="brand in brands" 
                  :key="brand.id"
                  :class="[
                    'px-4 py-2 rounded-md border focus:outline-none transition-colors flex items-center space-x-2',
                    currentBrand === brand.id 
                      ? 'bg-fill-brand-rest text-text-neutrallight-rest border-border-brand-rest shadow-sm' 
                      : 'border-border-primary-rest hover:border-border-primary-hover text-text-primary-rest hover:bg-fill-neutral-hover'
                  ]"
                  @click="switchBrand(brand.id)"
                >
                  <span class="text-sm font-medium">{{ brand.name }}</span>
                  <div 
                    v-if="currentBrand === brand.id"
                    class="w-2 h-2 rounded-full bg-current"
                  ></div>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Bottom Border Line -->
        <div class="h-1 w-full bg-surface-secondary-rest rounded-b-lg"></div>
      </div>
      
      <section id="semantic-tokens" class="token-categories mb-12">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-text-primary-rest">Semantic Tokens</h2>
          <router-link to="/foundation/brands">
            <Button 
              variant="secondary"
              size="md"
            >
              View Brands
              <template #trailing-icon>
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  width="20" 
                  height="20" 
                  viewBox="0 0 24 24" 
                  class="button__icon button__icon--trailing"
                >
                  <path 
                    fill="currentColor" 
                    d="M8.59 16.59L13.17 12L8.59 7.41L10 6l6 6l-6 6l-1.41-1.41z"
                  />
                </svg>
              </template>
            </Button>
          </router-link>
        </div>
        <p class="text-text-secondary-rest mb-6">
          These tokens are used to maintain consistent design across the application. Values will change based on theme (light/dark) and brand.
        </p>
        
        <div v-for="category in categories" :key="category.id" class="mb-12">
          <h3 class="text-xl font-semibold text-text-primary-rest mb-4">{{ category.name }}</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div 
              v-for="baseName in (commonTokens[category.id] || [])" 
              :key="baseName"
              class="token-card bg-surface-primary-rest p-4 rounded-lg border border-border-primary-rest"
            >
              <h4 class="font-medium text-text-primary-rest mb-2">{{ baseName }}</h4>
              
              <div class="token-states flex flex-col space-y-2">
                <div 
                  v-for="state in states" 
                  :key="state.id"
                  class="token-sample flex items-center"
                >
                  <div 
                    class="color-swatch w-10 h-10 rounded-md mr-3"
                    :style="{
                      backgroundColor: `var(${category.prefix}-${baseName}-${state.id})`,
                      color: getContrastText(getCssVar(`${category.prefix.substring(2)}-${baseName}-${state.id}`))
                    }"
                  ></div>
                  <div>
                    <div class="text-sm text-text-primary-rest">{{ state.name }}</div>
                    <div class="text-xs text-text-secondary-rest">var({{ category.prefix }}-{{ baseName }}-{{ state.id }})</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section id="component-tokens" class="component-tokens mb-12">
        <h2 class="text-2xl font-bold text-text-primary-rest mb-4">Component Tokens</h2>
        <p class="text-text-secondary-rest mb-6">
          Component-specific tokens that define styles for UI components. These reference the semantic tokens.
        </p>
        
        <div v-for="compCategory in componentCategories" :key="compCategory.id" class="mb-12">
          <h3 class="text-xl font-semibold text-text-primary-rest mb-4">{{ compCategory.name }}</h3>
          
          <div class="overflow-x-auto">
            <table class="w-full border-collapse">
              <thead>
                <tr class="bg-surface-secondary-rest">
                  <th class="p-3 border border-border-primary-rest text-left text-text-primary-rest">Token</th>
                  <th class="p-3 border border-border-primary-rest text-left text-text-primary-rest">Value</th>
                  <th class="p-3 border border-border-primary-rest text-left text-text-primary-rest">Preview</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="tokenName in [
                    'main-radius',
                    'main-gap',
                    'main-h-padding-s',
                    'main-v-padding-s',
                    'main-h-padding-m',
                    'main-v-padding-m',
                    'main-h-padding-l',
                    'main-v-padding-l'
                  ]" 
                  :key="`${compCategory.id}-${tokenName}`"
                  class="border-t border-border-primary-rest"
                >
                  <td class="p-3 border border-border-primary-rest text-text-primary-rest">{{ compCategory.prefix }}-{{ tokenName }}</td>
                  <td class="p-3 border border-border-primary-rest text-text-secondary-rest font-mono text-sm">
                    var({{ getCssVar(`${compCategory.prefix.substring(2)}-${tokenName}`) }})
                  </td>
                  <td class="p-3 border border-border-primary-rest">
                    <div 
                      class="h-8 w-full" 
                      :style="{
                        background: tokenName.includes('radius') ? 'var(--color-fill-brand-rest)' : 'transparent',
                        borderRadius: tokenName.includes('radius') ? `var(${compCategory.prefix}-${tokenName})` : 0,
                        border: !tokenName.includes('radius') ? '1px dashed var(--color-border-primary-rest)' : 'none',
                        padding: tokenName.includes('padding') ? `var(${compCategory.prefix}-${tokenName})` : 0,
                      }"
                    ></div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
      
      <section id="token-usage" class="token-usage mb-12">
        <h2 class="text-2xl font-bold text-text-primary-rest mb-4">Using Tokens</h2>
        
        <div class="bg-surface-secondary-rest p-6 rounded-lg">
          <h3 class="text-xl font-semibold text-text-primary-rest mb-4">In CSS</h3>
          <pre class="bg-fill-grey-rest p-4 rounded-md overflow-x-auto text-sm mb-4">
.my-element {
  color: var(--color-text-primary-rest);
  background-color: var(--color-fill-neutral-rest);
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
}

/* For state variations */
.my-element:hover {
  background-color: var(--color-fill-neutral-hover);
}
</pre>

          <h3 class="text-xl font-semibold text-text-primary-rest mt-8 mb-4">In Vue Components with TypeScript</h3>
          <pre class="bg-fill-grey-rest p-4 rounded-md overflow-x-auto text-sm">
import { createTokenStyles, TOKEN_TYPES, TOKEN_STATES } from '../lib/tokens';

// In your component
const elementStyles = computed(() => {
  return createTokenStyles({
    backgroundColor: 'color-fill-brand-rest',
    color: 'color-text-neutrallight-rest',
    borderRadius: 'comp-button-main-radius'
  });
});

// Use in template
// &lt;div :style="elementStyles"&gt;Content&lt;/div&gt;
</pre>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.tokens-page {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.content-with-sidebar {
  margin-right: 16rem; /* Adjust for sidebar width */
}

.right-sidebar {
  z-index: 10;
  background-color: var(--color-surface-primary-rest);
  border-left: 1px solid var(--color-border-primary-rest);
  top: 4rem; /* Position below header (64px) */
  height: calc(100vh - 4rem); /* Subtract header height from viewport height */
  width: 16rem;
}

.header-controls {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--color-border-primary-rest);
}

.color-swatch {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.75rem;
}

/* Ensure token cards have consistent height */
.token-card {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.token-states {
  flex-grow: 1;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .right-sidebar {
    display: none; /* Hide sidebar on mobile */
  }
  
  .content-with-sidebar {
    margin-right: 0; /* Remove margin when sidebar is hidden */
  }
}

@media (max-width: 768px) {
  .header-controls .flex-col {
    gap: 1.5rem;
  }
  
  .header-controls .flex {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-controls .space-x-6 {
    margin-top: 1rem;
  }
  
  .brand-selector {
    margin-top: 0.5rem;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .brand-selector button {
    flex: 1;
    min-width: 140px;
  }
}
</style> 