<template>
  <div class="button-page">
    <h1>Button Component</h1>
    
    <section class="section">
      <h2>Overview</h2>
      <p>The Button component is a fundamental UI element that follows our design system guidelines. It provides a consistent way to trigger actions across the application.</p>
      
      <div class="view-toggles">
        <button 
          @click="activeView = 'showcase'" 
          :class="{ active: activeView === 'showcase' }"
        >
          Design Showcase
        </button>
        <button 
          @click="activeView = 'developer'" 
          :class="{ active: activeView === 'developer' }"
        >
          Developer View
        </button>
        <button 
          @click="activeView = 'tokens'" 
          :class="{ active: activeView === 'tokens' }"
        >
          Token Explorer
        </button>
      </div>
    </section>

    <!-- Design Showcase View -->
    <div v-if="activeView === 'showcase'" class="section">
      <h2>Variants</h2>
      <p>Button variants offer different visual styles to indicate importance and purpose.</p>
      
      <!-- Interactive Token Explorer -->
      <div class="interactive-explorer">
        <div class="explorer-header">
          <h3>Interactive Token Explorer</h3>
          <p>Select different button variants to see how design tokens change in real-time.</p>
          
          <div class="explorer-theme-compare">
            <button 
              @click="toggleThemeCompare()" 
              :class="{ active: isCompareThemeMode }"
              class="compare-button"
            >
              {{ isCompareThemeMode ? 'Hide Theme Comparison' : 'Compare Light/Dark Tokens' }}
            </button>
          </div>
        </div>
        
        <div class="explorer-content">
          <div class="component-preview">
            <h4>Component Preview</h4>
            <div class="preview-variants">
              <div v-for="variant in variants" :key="`preview-${variant}`" class="preview-variant">
                <BaseButton 
                  :variant="variant"
                  @click="setActiveVariant(variant)"
                  :class="{ 'active-variant': activeVariant === variant }"
                >
                  {{ formatVariantName(variant) }}
                </BaseButton>
              </div>
            </div>
            
            <div class="preview-states">
              <h4>Interaction States</h4>
              <div class="states-row">
                <div v-for="state in interactionStates" :key="state" class="state-preview">
                  <BaseButton 
                    :variant="activeVariant" 
                    :class="[`button-state--${state}`, { 'disabled': state === 'disabled' }]"
                    :disabled="state === 'disabled'"
                  >
                    {{ formatStateName(state) }}
                  </BaseButton>
                  <div class="state-label">{{ formatStateName(state) }}</div>
                </div>
              </div>
            </div>
            
            <!-- Theme comparison preview -->
            <div v-if="isCompareThemeMode" class="theme-comparison-preview">
              <h4>Theme Comparison</h4>
              <div class="theme-grid">
                <div class="theme-column">
                  <div class="theme-label">Light Theme</div>
                  <div class="theme-sample light-theme">
                    <BaseButton :variant="activeVariant">
                      {{ formatVariantName(activeVariant) }}
                    </BaseButton>
                  </div>
                </div>
                <div class="theme-column">
                  <div class="theme-label">Dark Theme</div>
                  <div class="theme-sample dark-theme">
                    <BaseButton :variant="activeVariant">
                      {{ formatVariantName(activeVariant) }}
                    </BaseButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="token-display">
            <h4>
              Active Tokens for "{{ formatVariantName(activeVariant) }}"
              <span v-if="isCompareThemeMode" class="theme-compare-label">
                (Comparing Light vs Dark)
              </span>
            </h4>
            <div class="token-tabs">
              <button 
                v-for="category in tokenCategories" 
                :key="category.id"
                @click="activeTokenCategory = category.id"
                :class="{ active: activeTokenCategory === category.id }"
                class="token-tab"
              >
                {{ category.name }}
              </button>
            </div>
            
            <div class="token-list">
              <div 
                v-for="token in filteredTokensForDisplay" 
                :key="token.name" 
                class="token-item"
                :class="{ 
                  'token-changed': hasTokenChanged(token.name),
                  'token-theme-diff': isCompareThemeMode && hasThemeDifference(token.name)
                }"
              >
                <div class="token-item-header">
                  <div class="token-name">{{ token.name }}</div>
                  <div class="token-indicators">
                    <span class="token-indicator" v-if="hasTokenChanged(token.name)">
                      <span class="token-changed-label">Changed</span>
                    </span>
                    <span class="token-indicator" v-if="isCompareThemeMode && hasThemeDifference(token.name)">
                      <span class="token-theme-diff-label">Theme Specific</span>
                    </span>
                  </div>
                </div>
                
                <div class="token-preview" v-if="isColorToken(token.name)">
                  <div 
                    v-if="isCompareThemeMode && getThemeDifferenceValue(token.name)" 
                    class="theme-color-compare"
                  >
                    <div class="color-preview" :style="{ backgroundColor: token.value }"></div>
                    <div class="color-preview" :style="{ backgroundColor: getThemeDifferenceValue(token.name) || '' }"></div>
                    <div class="theme-indicator">
                      <span>Light</span>
                      <span>Dark</span>
                    </div>
                  </div>
                  <div v-else class="color-preview" :style="{ backgroundColor: token.value }"></div>
                </div>
                
                <div class="token-value">
                  <code>{{ token.value }}</code>
                  <span v-if="prevTokenValue(token.name)" class="token-previous">
                    was: <code>{{ prevTokenValue(token.name) }}</code>
                  </span>
                  <span v-if="isCompareThemeMode && getThemeDifferenceValue(token.name)" class="token-alternate-theme">
                    Dark: <code>{{ getThemeDifferenceValue(token.name) }}</code>
                  </span>
                </div>
                
                <div class="token-usage">{{ token.usage || 'Button styling' }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="variant-grid">
        <div v-for="variant in variants" :key="variant" class="component-card">
          <div class="card-content">
            <BaseButton :variant="variant">{{ formatVariantName(variant) }}</BaseButton>
          </div>
          <div class="card-label">{{ formatVariantName(variant) }}</div>
          <div class="card-description">{{ getVariantDescription(variant) }}</div>
        </div>
      </div>

      <h2>Sizes</h2>
      <p>Button sizes accommodate different UI contexts and hierarchy needs.</p>
      <div class="size-grid">
        <div v-for="size in sizes" :key="size" class="component-card">
          <div class="card-content">
            <BaseButton :size="size">{{ formatSizeName(size) }}</BaseButton>
          </div>
          <div class="card-label">{{ formatSizeName(size) }}</div>
          <div class="card-description">{{ getSizeDescription(size) }}</div>
        </div>
      </div>

      <h2>States</h2>
      <p>Buttons have different states to provide visual feedback to users.</p>
      <div class="state-grid">
        <div class="component-card">
          <div class="card-content">
            <BaseButton>Default State</BaseButton>
          </div>
          <div class="card-label">Default</div>
          <div class="card-description">Normal button state</div>
        </div>
        <div class="component-card">
          <div class="card-content">
            <BaseButton :disabled="true">Disabled</BaseButton>
          </div>
          <div class="card-label">Disabled</div>
          <div class="card-description">Button cannot be interacted with</div>
        </div>
        <div class="component-card">
          <div class="card-content">
            <BaseButton :loading="true">Loading</BaseButton>
          </div>
          <div class="card-label">Loading</div>
          <div class="card-description">Button is processing an action</div>
        </div>
      </div>

      <h2>Examples</h2>
      <div class="examples-section">
        <BasicExamples />
      </div>
    </div>

    <!-- Developer View -->
    <div v-if="activeView === 'developer'" class="section">
      <h2>Implementation</h2>
      <div class="code-example">
        <h3>Basic Usage</h3>
        <pre><code>&lt;BaseButton variant="primary" size="md"&gt;Click Me&lt;/BaseButton&gt;</code></pre>
        <h3>With Props</h3>
        <pre><code>&lt;BaseButton 
  variant="primary" 
  size="md" 
  :disabled="isDisabled" 
  :loading="isLoading" 
  @click="handleClick"
&gt;
  Submit
&lt;/BaseButton&gt;</code></pre>
      </div>

      <h2>Props</h2>
      <div class="props-table">
        <table>
          <thead>
            <tr>
              <th>Prop</th>
              <th>Type</th>
              <th>Default</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>variant</td>
              <td>string</td>
              <td>'primary'</td>
              <td>Button visual style: 'primary', 'secondary', 'outline', 'ghost', 'danger', 'warning', 'success'</td>
            </tr>
            <tr>
              <td>size</td>
              <td>string</td>
              <td>'md'</td>
              <td>Button size: 'sm', 'md', 'lg', 'xl'</td>
            </tr>
            <tr>
              <td>disabled</td>
              <td>boolean</td>
              <td>false</td>
              <td>Whether the button is disabled</td>
            </tr>
            <tr>
              <td>loading</td>
              <td>boolean</td>
              <td>false</td>
              <td>Whether the button is in loading state</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>Events</h2>
      <div class="events-table">
        <table>
          <thead>
            <tr>
              <th>Event</th>
              <th>Parameters</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>@click</td>
              <td>MouseEvent</td>
              <td>Emitted when the button is clicked (not emitted if disabled or loading)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2>Accessibility</h2>
      <div class="accessibility-info">
        <ul>
          <li>Follows WCAG 2.1 AA guidelines</li>
          <li>Properly handles disabled states with aria-disabled</li>
          <li>Loading states are announced to screen readers</li>
          <li>Maintains focus styles for keyboard navigation</li>
          <li>Color contrast meets WCAG requirements</li>
        </ul>
      </div>
    </div>

    <!-- Token Explorer View -->
    <div v-if="activeView === 'tokens'" class="section">
      <h2>Design Tokens</h2>
      <p>Explore the tokens that define the Button component's appearance across different themes and states.</p>
      
      <div class="token-view-toggles">
        <button 
          @click="tokenView = 'visual'" 
          :class="{ active: tokenView === 'visual' }"
        >
          Visual View
        </button>
        <button 
          @click="tokenView = 'code'" 
          :class="{ active: tokenView === 'code' }"
        >
          Code View
        </button>
      </div>

      <!-- Visual Token View -->
      <div v-if="tokenView === 'visual'" class="token-explorer">
        <div v-for="category in tokenCategories" :key="category.name" class="token-category">
          <h3>{{ category.name }}</h3>
          <p>{{ category.description }}</p>
          
          <div class="token-grid">
            <div v-for="token in category.tokens" :key="token.name" class="token-cell">
              <div v-if="isColorToken(token.name)" class="token-preview" :style="{ backgroundColor: token.value }"></div>
              <div v-else-if="isSizeToken(token.name)" class="token-size-preview" :style="getPreviewStyle(token)"></div>
              <div class="token-details">
                <div class="token-name">{{ token.name }}</div>
                <div class="token-value">{{ token.value }}</div>
                <div class="token-usage">{{ token.usage }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Code Token View -->
      <div v-if="tokenView === 'code'" class="token-code-view">
        <h3>Token Usage in CSS</h3>
        <pre><code>.custom-button {
  /* Size tokens */
  padding: var(--comp-button-main-v-padding-m) var(--comp-button-main-h-padding-m);
  border-radius: var(--comp-button-main-radius);
  gap: var(--comp-button-main-gap);
  
  /* Typography tokens */
  font-family: var(--font-family-DM-Sans);
  font-weight: var(--font-weight-semibold-600);
  font-size: var(--comp-button-main-font-size-m);
  line-height: var(--font-line-height-20);
  
  /* Color tokens - Primary variant */
  background-color: var(--comp-button-main-bg-primary);
  color: var(--comp-button-main-text-primary);
  border: 1px solid var(--comp-button-main-border-primary);
  
  /* Transition */
  transition: var(--comp-button-main-transition);
}</code></pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import BaseButton from '../../../design-system/components/core/button/BaseButton.vue';
import BasicExamples from '../../../design-system/components/core/button/examples/BasicExamples.vue';
import { 
  getAllTokensForTheme, 
  getButtonVariantTokens,
  getButtonSizeTokensBySize,
  getButtonStateTokens,
  getCommonButtonTokens,
  TokenDefinition
} from '../../../design-system/components/core/button/ButtonTokens';
import { 
  getComponentButtonTokens,
  getVariantSemanticTokens,
  getThemeAwareToken,
  watchThemeChanges
} from '../../../utils/tokenUtils';
import { TOKEN_TYPES, TOKEN_STATES } from '../../../lib/tokens';

// Component state
const activeView = ref('showcase');
const tokenView = ref('visual');
const buttonTokens = ref<TokenDefinition[]>([]);

// Theme comparison state
const currentTheme = ref(document.documentElement.getAttribute('data-theme') || 'light');
const isCompareThemeMode = ref(false);
const themeDifferences = ref<Record<string, string>>({});

// Interactive token explorer state
const activeVariant = ref<typeof variants[number]>('primary');
const previousVariant = ref<typeof variants[number] | null>(null);
const activeTokenCategory = ref('all');
const changedTokens = ref<Record<string, string>>({});
const interactionStates = ['default', 'hover', 'active', 'focus', 'disabled'];

// Button options
const variants = ['primary', 'secondary', 'outline', 'ghost', 'danger', 'warning', 'success'] as const;
const sizes = ['sm', 'md', 'lg', 'xl'] as const;

// Token categories for filtering
const tokenCategories = [
  { id: 'all', name: 'All Tokens' },
  { id: 'color', name: 'Colors' },
  { id: 'size', name: 'Sizes & Layout' },
  { id: 'state', name: 'States' },
  { id: 'typography', name: 'Typography' }
];

// Load tokens and watch for theme changes
onMounted(() => {
  buttonTokens.value = getAllTokensForTheme();
  
  // Watch for theme changes in the document
  const cleanup = watchThemeChanges(() => {
    // Update current theme when it changes
    currentTheme.value = document.documentElement.getAttribute('data-theme') || 'light';
    
    // If theme comparison is on, update differences
    if (isCompareThemeMode.value) {
      updateThemeDifferences();
    }
  });
  
  // Clean up the watcher when component is unmounted
  onUnmounted(() => {
    cleanup();
  });
});

// Format names for display
const formatVariantName = (variant: string) => {
  return variant.charAt(0).toUpperCase() + variant.slice(1);
};

const formatSizeName = (size: string) => {
  const sizeMap: Record<string, string> = {
    'sm': 'Small',
    'md': 'Medium',
    'lg': 'Large',
    'xl': 'Extra Large'
  };
  return sizeMap[size] || size.toUpperCase();
};

const formatStateName = (state: string) => {
  return state.charAt(0).toUpperCase() + state.slice(1);
};

// Toggle theme comparison mode
const toggleThemeCompare = () => {
  isCompareThemeMode.value = !isCompareThemeMode.value;
  
  if (isCompareThemeMode.value) {
    updateThemeDifferences();
  } else {
    themeDifferences.value = {};
  }
};

// Update theme differences by comparing light and dark theme tokens
const updateThemeDifferences = () => {
  themeDifferences.value = {};
  
  // Simulate getting tokens for both themes
  // This would typically make API calls to get both light and dark tokens
  // For now, we'll use a simplified approach with semantic tokens
  
  // Extract tokens that differ between themes 
  const tokenNames = [
    ...getVariantSemanticTokens(activeVariant.value as any).map(t => t.name),
    ...getComponentButtonTokens().map(t => t.name)
  ];
  
  // For each token, check if it has a different value in dark mode
  tokenNames.forEach(tokenName => {
    // Mock comparison - in a real system you'd get actual values from both themes
    if (tokenName.includes('color') || tokenName.includes('fill') || tokenName.includes('border')) {
      // Simulate different values for color tokens in dark mode
      const lightValue = `var(${tokenName})`;
      const darkValue = `var(${tokenName}-dark, ${lightValue})`;
      
      // Only add to differences if there is actually a difference
      if (lightValue !== darkValue) {
        themeDifferences.value[tokenName] = darkValue;
      }
    }
  });
};

// Set active variant and track changes
const setActiveVariant = (variant: typeof variants[number]) => {
  if (activeVariant.value !== variant) {
    previousVariant.value = activeVariant.value;
    
    // Store changed tokens for visual highlighting
    const currentTokens = getButtonVariantTokens(activeVariant.value);
    const newTokens = getButtonVariantTokens(variant);
    
    // Reset changed tokens
    changedTokens.value = {};
    
    // Compare and track changes
    newTokens.forEach(newToken => {
      const currentToken = currentTokens.find(t => {
        // Map corresponding token names across variants
        const currentName = t.name.replace(activeVariant.value, variant);
        return currentName === newToken.name;
      });
      
      if (currentToken && currentToken.value !== newToken.value) {
        changedTokens.value[newToken.name] = currentToken.value;
      }
    });
    
    activeVariant.value = variant;
    
    // If theme comparison is on, update differences for new variant
    if (isCompareThemeMode.value) {
      updateThemeDifferences();
    }
  }
};

// Check if a token has changed
const hasTokenChanged = (tokenName: string) => {
  return Object.keys(changedTokens.value).includes(tokenName);
};

// Get previous token value if it changed
const prevTokenValue = (tokenName: string) => {
  return changedTokens.value[tokenName] || null;
};

// Check if a token has a theme difference
const hasThemeDifference = (tokenName: string) => {
  return Object.keys(themeDifferences.value).includes(tokenName);
};

// Get the theme difference value for a token
const getThemeDifferenceValue = (tokenName: string) => {
  return themeDifferences.value[tokenName] || null;
};

// Filter tokens based on active category and variant
const filteredTokensForDisplay = computed(() => {
  // Start with variant-specific tokens
  let tokens = getButtonVariantTokens(activeVariant.value);
  
  // Add common tokens that apply to all buttons
  tokens = [...tokens, ...getCommonButtonTokens()];
  
  // Add state tokens
  tokens = [...tokens, ...getButtonStateTokens('rest')];
  
  // Filter by category if not showing all
  if (activeTokenCategory.value !== 'all') {
    tokens = tokens.filter(token => {
      if (activeTokenCategory.value === 'color') {
        return isColorToken(token.name);
      } else if (activeTokenCategory.value === 'size') {
        return isSizeToken(token.name);
      } else if (activeTokenCategory.value === 'state') {
        return token.name.includes('hover') || 
               token.name.includes('press') || 
               token.name.includes('focus') || 
               token.name.includes('disabled');
      } else if (activeTokenCategory.value === 'typography') {
        return token.name.includes('font') || token.name.includes('line-height');
      }
      return true;
    });
  }
  
  return tokens;
});

// Helper functions for token visualization
const isColorToken = (tokenName: string) => {
  return tokenName.includes('color') || 
         tokenName.includes('fill') || 
         tokenName.includes('border') || 
         tokenName.includes('bg');
};

const isSizeToken = (tokenName: string) => {
  return tokenName.includes('padding') || 
         tokenName.includes('radius') || 
         tokenName.includes('gap') || 
         tokenName.includes('size');
};

const getPreviewStyle = (token: TokenDefinition) => {
  if (token.name.includes('padding')) {
    return {
      padding: token.value,
      border: '1px dashed var(--color-border-secondary)',
      backgroundColor: 'var(--color-surface-secondary-hover)'
    };
  }
  if (token.name.includes('radius')) {
    return {
      borderRadius: token.value,
      width: '2rem',
      height: '2rem',
      backgroundColor: 'var(--color-surface-secondary)'
    };
  }
  if (token.name.includes('gap')) {
    return {
      width: token.value,
      height: '1rem',
      backgroundColor: 'var(--color-surface-secondary)'
    };
  }
  if (token.name.includes('size')) {
    return {
      fontSize: token.value,
      lineHeight: '1.5'
    };
  }
  return {};
};

// Descriptions for variants and sizes
const getVariantDescription = (variant: string) => {
  const descriptions: Record<string, string> = {
    'primary': 'Main call-to-action button for primary actions',
    'secondary': 'Used for secondary actions that require less emphasis',
    'outline': 'A subtle button with just an outline and transparent background',
    'ghost': 'The least prominent button, typically used for tertiary actions',
    'danger': 'Indicates a destructive or negative action',
    'warning': 'Indicates a potentially risky action that requires attention',
    'success': 'Indicates a positive or successful action'
  };
  return descriptions[variant] || '';
};

const getSizeDescription = (size: string) => {
  const descriptions: Record<string, string> = {
    'sm': 'Compact size for tight UI areas or secondary actions',
    'md': 'Standard size for most contexts',
    'lg': 'Larger size for primary actions or increased visibility',
    'xl': 'Extra large size for high-emphasis actions or hero sections'
  };
  return descriptions[size] || '';
};
</script>

<style scoped>
.button-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  color: var(--color-text-primary, #1f2937);
  background-color: var(--color-surface-primary, #ffffff);
}

h1 {
  margin-bottom: 2rem;
  font-size: 2.5rem;
  font-weight: 600;
}

.section {
  margin-bottom: 3rem;
}

h2 {
  margin: 2rem 0 1rem;
  font-size: 1.75rem;
  font-weight: 500;
  border-bottom: 1px solid var(--divider-color);
  padding-bottom: 0.5rem;
}

h3 {
  margin: 1.5rem 0 1rem;
  font-size: 1.25rem;
  font-weight: 500;
}

p {
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.view-toggles {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.view-toggles button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--card-border);
  background: var(--card-bg);
  border-radius: 0.25rem;
  cursor: pointer;
  font-weight: 500;
  color: var(--page-text);
}

.view-toggles button.active {
  background: var(--accent-color-light);
  border-color: var(--accent-color);
  color: var(--accent-color);
}

.interactive-explorer {
  margin-bottom: 3rem;
  border: 1px solid var(--card-border);
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: var(--card-shadow);
  background-color: var(--card-bg);
}

.explorer-header {
  background-color: var(--card-bg);
  padding: 1.5rem;
  border-bottom: 1px solid var(--divider-color);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 1rem;
}

.explorer-header h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--page-text);
}

.explorer-header p {
  margin: 0;
  color: var(--page-text);
  opacity: 0.8;
}

.explorer-theme-compare {
  margin-top: 1rem;
}

.compare-button {
  padding: 0.375rem 0.75rem;
  background-color: var(--accent-color-light);
  color: var(--accent-color);
  border: 1px solid var(--accent-color);
  border-radius: 0.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.compare-button.active {
  background-color: var(--accent-color);
  color: white;
}

.explorer-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background-color: var(--divider-color);
}

.component-preview, .token-display {
  background-color: var(--card-bg);
  padding: 1.5rem;
}

.component-preview h4, .token-display h4 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--page-text);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-compare-label {
  font-size: 0.75rem;
  font-weight: normal;
  color: var(--theme-label-text);
  background-color: var(--theme-label-bg);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.preview-variants {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.active-variant {
  outline: 3px solid var(--accent-color);
  outline-offset: 2px;
}

.preview-states {
  margin-top: 2rem;
}

.states-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
}

.state-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.state-label {
  font-size: 0.875rem;
  color: var(--page-text);
  opacity: 0.8;
}

/* Theme comparison preview */
.theme-comparison-preview {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--divider-color);
}

.theme-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.theme-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.theme-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--page-text);
}

.theme-sample {
  padding: 1.5rem;
  border-radius: 0.375rem;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.light-theme {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
}

.dark-theme {
  background-color: #1f2937;
  border: 1px solid #374151;
}

/* Button state styling for demo */
.button-state--hover:not(.disabled) {
  filter: brightness(0.95);
}

.button-state--active:not(.disabled) {
  filter: brightness(0.9);
  transform: scale(0.98);
}

.button-state--focus:not(.disabled) {
  outline: 2px solid var(--accent-color);
  outline-offset: 2px;
}

.token-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--divider-color);
  padding-bottom: 0.5rem;
}

.token-tab {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 500;
  cursor: pointer;
  color: var(--page-text);
  opacity: 0.7;
}

.token-tab.active {
  background-color: var(--accent-color-light);
  color: var(--accent-color);
  opacity: 1;
}

.token-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.token-item {
  padding: 1rem;
  border: 1px solid var(--card-border);
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  background-color: var(--card-bg);
}

.token-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.token-indicators {
  display: flex;
  gap: 0.5rem;
}

.token-name {
  font-family: monospace;
  font-weight: 600;
  color: var(--page-text);
}

.token-changed {
  border-left: 4px solid var(--accent-color);
  background-color: var(--accent-color-light);
}

.token-theme-diff {
  border-left: 4px solid var(--theme-label-text);
}

.token-changed-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--changed-label-text);
  background-color: var(--changed-label-bg);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.token-theme-diff-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--theme-label-text);
  background-color: var(--theme-label-bg);
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
}

.token-value {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.token-value code {
  font-family: monospace;
  background-color: var(--code-bg);
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.875rem;
  color: var(--page-text);
}

.token-previous, .token-alternate-theme {
  font-size: 0.75rem;
  color: var(--page-text);
  opacity: 0.8;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.token-previous code {
  text-decoration: line-through;
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.theme-color-compare {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-indicator {
  display: flex;
  flex-direction: column;
  font-size: 0.75rem;
  color: var(--page-text);
  opacity: 0.8;
}

.color-preview {
  width: 2rem;
  height: 2rem;
  border-radius: 0.25rem;
  border: 1px solid var(--card-border);
  margin-right: 0.25rem;
}

.variant-grid,
.size-grid,
.state-grid {
  display: grid;
  gap: 2rem;
  margin: 1.5rem 0 3rem;
}

.component-card {
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.card-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 5rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 0.25rem;
}

.card-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.card-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.4;
}

.code-example {
  background: #f8f9fc;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.code-example pre {
  background: #f1f3f9;
  border-radius: 0.25rem;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.5rem 0 1.5rem;
}

.props-table table,
.events-table table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}

.props-table th,
.events-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  background: #f1f3f9;
  border-bottom: 2px solid #e1e5f1;
}

.props-table td,
.events-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #eee;
}

.accessibility-info ul {
  list-style-type: disc;
  padding-left: 1.5rem;
  margin-bottom: 2rem;
}

.accessibility-info li {
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

.token-explorer {
  margin-top: 2rem;
}

.token-category {
  margin-bottom: 3rem;
}

.token-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.token-cell {
  display: flex;
  flex-direction: column;
  border: 1px solid #eee;
  border-radius: 0.5rem;
  overflow: hidden;
  padding: 1rem;
}

.token-preview, .token-size-preview {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.25rem;
  margin-bottom: 0.75rem;
}

.token-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.token-name {
  font-family: monospace;
  font-size: 0.9rem;
  color: #0066cc;
}

.token-value {
  font-family: monospace;
  font-size: 0.875rem;
  color: #666;
}

.token-usage {
  font-size: 0.875rem;
  color: #666;
  margin-top: 0.5rem;
}

.token-code-view pre {
  background: #f1f3f9;
  border-radius: 0.25rem;
  padding: 1rem;
  overflow-x: auto;
  margin: 0.5rem 0 1.5rem;
  font-family: monospace;
  font-size: 0.9rem;
  line-height: 1.5;
}

@media (min-width: 768px) {
  .variant-grid,
  .size-grid,
  .state-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .explorer-content {
    grid-template-columns: 1fr;
  }
  
  .token-tabs {
    overflow-x: auto;
    padding-bottom: 0.5rem;
  }
  
  .theme-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style> 