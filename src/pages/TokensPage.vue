<script setup lang="ts">
import { ref, computed, inject } from 'vue';
import { TOKEN_TYPES, TOKEN_STATES, getCssVar } from '../lib/tokens';

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

  return tokens;
};

// Toggle dark/light mode
const toggleMode = () => {
  const newMode = effectiveTheme.value === 'light' ? 'dark' : 'light';
  setThemeMode(newMode);
};

// Switch brand
const switchBrand = (brand: string) => {
  setBrand(brand);
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
</script>

<template>
  <div class="tokens-page">
    <div class="header-controls bg-surface-primary mb-8 p-4 rounded-lg">
      <h1 class="text-3xl font-bold text-text-primary-rest mb-4">{{ props.title }}</h1>
      
      <div class="flex flex-wrap gap-4 mt-4">
        <div class="mode-toggle">
          <button 
            class="px-4 py-2 rounded-md border border-border-primary-rest hover:border-border-primary-hover focus:outline-none" 
            @click="toggleMode"
          >
            {{ effectiveTheme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode' }}
          </button>
        </div>
        
        <div class="brand-selector flex space-x-2">
          <button 
            v-for="brand in brands" 
            :key="brand.id"
            :class="[
              'px-4 py-2 rounded-md border focus:outline-none transition-colors',
              currentBrand === brand.id 
                ? 'bg-fill-brand-rest text-text-neutrallight-rest border-border-brand-rest' 
                : 'border-border-primary-rest hover:border-border-primary-hover'
            ]"
            @click="switchBrand(brand.id)"
          >
            {{ brand.name }}
          </button>
        </div>
        
        <div class="link-to-brands ml-auto">
          <router-link 
            to="/foundation/brands" 
            class="px-4 py-2 rounded-md border border-border-primary-rest hover:border-border-primary-hover focus:outline-none flex items-center transition-colors"
          >
            <span>View Brand Details</span>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 ml-2">
              <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
            </svg>
          </router-link>
        </div>
      </div>
    </div>
    
    <section class="token-categories mb-12">
      <h2 class="text-2xl font-bold text-text-primary-rest mb-4">Semantic Tokens</h2>
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
    
    <section class="component-tokens mb-12">
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
    
    <section class="token-usage mb-12">
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
</template>

<style scoped>
.tokens-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
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
</style> 