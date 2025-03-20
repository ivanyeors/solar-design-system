<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';

// Note: Removed SCSS imports since they should already be included in the main application
// The following should be done in your main styles instead 
// import '@/styles/tokens/option-tokens/colors_light.scss';
// import '@/styles/tokens/option-tokens/colors_dark.scss';

// Define color categories with their token names
const colorCategories = [
  {
    name: 'Brick',
    description: 'Red-orange hues for errors, alerts, and warnings',
    prefix: 'color-brick',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Cerulean',
    description: 'Blue hues for primary actions and links',
    prefix: 'color-cerulean',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Cobalt',
    description: 'Deep blue hues for secondary elements',
    prefix: 'color-cobalt',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Crimson',
    description: 'Deep red hues for critical errors and dangers',
    prefix: 'color-crimson',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Grape',
    description: 'Purple hues for tertiary elements',
    prefix: 'color-grape',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Jade',
    description: 'Green hues for success and completion',
    prefix: 'color-jade',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Lavender',
    description: 'Light purple hues for highlights',
    prefix: 'color-lavender',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Lemon',
    description: 'Yellow hues for warnings and highlights',
    prefix: 'color-lemon',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Lime',
    description: 'Light green hues for success and positivity',
    prefix: 'color-lime',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Marmalade',
    description: 'Orange hues for alerts and attention',
    prefix: 'color-marmalade',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Merigold',
    description: 'Gold hues for premium and exclusive elements',
    prefix: 'color-merigold',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Stone',
    description: 'Neutral grays for text, backgrounds, and borders',
    prefix: 'color-stone',
    shades: ['00-white', '25', '50', '100', '150', '200', '250', '300', '400', '500', '600', '650', '700', '750', '800', '850', '900', '950', '1000-black', 'transparent']
  },
  {
    name: 'Rose',
    description: 'Pink hues for feminine and gentle elements',
    prefix: 'color-rose',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Sea',
    description: 'Deep blue hues for depth and stability',
    prefix: 'color-sea',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Turquoise',
    description: 'Teal hues for trust and calm',
    prefix: 'color-turquoise',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  },
  {
    name: 'Violet',
    description: 'Deep purple hues for creativity and wisdom',
    prefix: 'color-violet',
    shades: ['25', '50', '100', '150', '200', '250', '300', '400', '500-main', '600', '650', '700', '750', '800', '850', '900', '950']
  }
];

// Track theme state
const currentTheme = ref('light');

// Listen for theme changes
onMounted(() => {
  // Get initial theme from document
  const dataTheme = document.documentElement.getAttribute('data-theme') || 'light';
  currentTheme.value = dataTheme;
  
  // Create custom event listener for theme changes
  const handleThemeChange = (event: Event) => {
    const evt = event as CustomEvent<{theme: string}>;
    if (evt.detail && evt.detail.theme) {
      currentTheme.value = evt.detail.theme;
    }
  };
  
  // Add event listener
  window.addEventListener('theme-change', handleThemeChange as EventListener);
  
  // Add MutationObserver to detect attribute changes on document.documentElement
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'data-theme') {
        const newTheme = document.documentElement.getAttribute('data-theme') || 'light';
        currentTheme.value = newTheme;
      }
    });
  });
  
  observer.observe(document.documentElement, { attributes: true });
  
  // Clean up on unmount
  return () => {
    window.removeEventListener('theme-change', handleThemeChange as EventListener);
    observer.disconnect();
  };
});

// Function to get the CSS variable value
const getCssVar = (varName: string) => {
  return getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
};

// Function to get the computed background color for a color token
const getComputedColor = (prefix: string, shade: string) => {
  return `var(--${prefix}-${shade})`;
};

// Function to get the contrasting text color for better readability
const getContrastingTextColor = (backgroundColor: string) => {
  // This is a simplified version - we use CSS variables for light/dark text
  return 'var(--color-text-primary-inverse)';
};

// Generate the SCSS variable name (for display purposes)
const getSassVariableName = (prefix: string, shade: string) => {
  return `$${prefix}-${shade}`;
};

// Track active category for tab switching
const activeCategoryIndex = ref(-1); // Start with -1 to show all categories by default

const setActiveCategory = (index: number) => {
  activeCategoryIndex.value = index;
};

// Helper function to check if a category should be visible
const isCategoryVisible = (index: number) => {
  return activeCategoryIndex.value === -1 || activeCategoryIndex.value === index;
};

// Copy color to clipboard
const copyToClipboard = (text: string) => {
  navigator.clipboard.writeText(text).then(() => {
    // You could add a toast notification here
    console.log('Copied to clipboard:', text);
  });
};
</script>

<template>
  <div class="colors-page">
    <div class="page-header">
      <h1>Color System</h1>
      <p>Explore the complete color palette of the Solar Design System. The colors are designed to work in both light and dark modes.</p>
      <div class="current-theme">
        <span>Current theme: </span>
        <span class="theme-badge" :class="currentTheme">{{ currentTheme }}</span>
      </div>
    </div>
    
    <div class="color-nav">
      <button 
        class="color-nav-button"
        :class="{ active: activeCategoryIndex === -1 }"
        @click="setActiveCategory(-1)"
      >
        All
      </button>
      <button 
        v-for="(category, index) in colorCategories" 
        :key="category.prefix"
        @click="setActiveCategory(index)"
        :class="['color-nav-button', { active: activeCategoryIndex === index }]"
      >
        {{ category.name }}
      </button>
    </div>
    
    <div class="color-categories" :class="{ 'show-all': activeCategoryIndex === -1 }">
      <div 
        v-for="(category, categoryIndex) in colorCategories" 
        :key="category.prefix"
        class="color-category"
        :class="{ 'active': isCategoryVisible(categoryIndex) }"
      >
        <div class="category-header">
          <h2>{{ category.name }}</h2>
          <p>{{ category.description }}</p>
        </div>
        
        <div class="color-swatches">
          <div 
            v-for="shade in category.shades" 
            :key="`${category.prefix}-${shade}`"
            class="color-swatch"
            :style="{
              backgroundColor: getComputedColor(category.prefix, shade),
            }"
            @click="copyToClipboard(`var(--${category.prefix}-${shade})`)"
          >
            <div class="color-info">
              <div class="color-name">{{ category.prefix }}-{{ shade }}</div>
              <div class="color-code">{{ getSassVariableName(category.prefix, shade) }}</div>
              <div class="copy-hint">Click to copy CSS variable</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.colors-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary-rest);
}

.page-header p {
  font-size: 1.125rem;
  color: var(--color-text-secondary-rest);
  margin-bottom: 1rem;
}

.current-theme {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  color: var(--color-text-secondary-rest);
}

.theme-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.theme-badge.light {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

.theme-badge.dark {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

.color-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border-primary-rest);
  padding-bottom: 1rem;
}

.color-nav-button {
  padding: 0.5rem 1rem;
  border-radius: var(--comp-button-main-radius, 0.375rem);
  font-size: 0.875rem;
  font-weight: 500;
  background-color: var(--color-surface-primary-rest);
  color: var(--color-text-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  cursor: pointer;
  transition: all 0.2s ease;
}

.color-nav-button:hover {
  background-color: var(--color-surface-primary-hover);
  color: var(--color-text-secondary-hover);
}

.color-nav-button.active {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
  border-color: var(--color-border-brand-rest);
}

.color-categories {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.color-category {
  display: none;
}

.color-category.active {
  display: block;
}

.category-header {
  margin-bottom: 1.5rem;
}

.category-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: var(--color-text-primary-rest);
}

.category-header p {
  color: var(--color-text-secondary-rest);
}

.color-swatches {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.color-swatch {
  height: 100px;
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.color-swatch:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.color-swatch:hover .copy-hint {
  opacity: 1;
}

.color-info {
  background-color: rgba(0, 0, 0, 0.2);
  color: #fff;
  backdrop-filter: blur(4px);
  border-radius: 0.25rem;
  padding: 0.5rem;
  transition: all 0.2s ease;
}

.color-name {
  font-weight: 500;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  white-space: nowrap;
}

.color-code {
  font-size: 0.75rem;
  font-family: monospace;
  opacity: 0.9;
  white-space: nowrap;
}

.copy-hint {
  font-size: 0.75rem;
  margin-top: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
}

@media (max-width: 768px) {
  .colors-page {
    padding: 1rem;
  }
  
  .color-swatches {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  
  .color-swatch {
    height: 80px;
  }
}

.color-categories.show-all {
  display: flex;
  flex-direction: column;
  gap: 4rem;
}

.color-categories.show-all .color-category {
  display: block;
  border-bottom: 1px solid var(--color-border-primary-rest);
  padding-bottom: 2rem;
}

.color-categories.show-all .color-category:last-child {
  border-bottom: none;
}
</style>
