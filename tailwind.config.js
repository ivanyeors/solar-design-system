/** @type {import('tailwindcss').Config} */
const semanticTokenPlugin = require('./src/styles/semanticTokenPlugin.js');

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Semantic text colors
        primary: 'var(--color-text-primary-rest)',
        secondary: 'var(--color-text-secondary-rest)',
        'primary-disabled': 'var(--color-text-primary-disabled)',
        'secondary-disabled': 'var(--color-text-secondary-disabled)',
        'primary-hover': 'var(--color-text-primary-hover)',
        'secondary-hover': 'var(--color-text-secondary-hover)',
        'primary-inverse': 'var(--color-text-primary-inverse)',
        
        // Brand colors
        brand: 'var(--color-text-brand-rest)',
        'brand-hover': 'var(--color-text-brand-hover)',
        'brand-press': 'var(--color-text-brand-press)',
        'brand-focus': 'var(--color-text-brand-focus)',
        'brand-disabled': 'var(--color-text-brand-disabled)',
        
        // Fill/background colors
        neutral: 'var(--color-fill-neutral-rest)',
        'neutral-hover': 'var(--color-fill-neutral-hover)',
        'neutral-press': 'var(--color-fill-neutral-press)',
        'neutral-disabled': 'var(--color-fill-neutral-disabled)',
        
        grey: 'var(--color-fill-grey-rest)',
        'grey-hover': 'var(--color-fill-grey-hover)',
        'grey-press': 'var(--color-fill-grey-press)',
        'grey-disabled': 'var(--color-fill-grey-disabled)',
        
        'brand-pale': 'var(--color-fill-brand-pale-rest)',
        'brand-pale-hover': 'var(--color-fill-brand-pale-hover)',
        'brand-pale-press': 'var(--color-fill-brand-pale-press)',
        'brand-pale-disabled': 'var(--color-fill-brand-pale-disabled)',
        
        // Status colors
        danger: 'var(--color-text-danger-rest)',
        success: 'var(--color-text-success-rest)',
        warning: 'var(--color-text-warning-rest)',
        info: 'var(--color-text-info-rest)',
        note: 'var(--color-text-note-rest)',
        
        // Button specific colors 
        'button-primary': 'var(--comp-button-main-fill-pri-focused)',
        'button-primary-hover': 'var(--comp-button-main-fill-pri-hover)',
        'button-primary-press': 'var(--comp-button-main-fill-pri-pressed)',
        'button-primary-disabled': 'var(--comp-button-main-fill-pri-disabled)',
        
        'button-secondary': 'var(--comp-button-main-fill-rest-sec)',
        'button-secondary-hover': 'var(--comp-button-main-fill-hover-sec)',
        'button-secondary-press': 'var(--comp-button-main-fill-pressed-sec)',
        'button-secondary-disabled': 'var(--comp-button-main-fill-disabled-sec)',
        
        // Border colors 
        'border-primary': 'var(--color-border-primary-rest)',
        'border-primary-hover': 'var(--color-border-primary-hover)',
        'border-primary-disabled': 'var(--color-border-primary-disabled)',
        'border-brand': 'var(--color-border-brand-rest)',
      },
      // Add component-specific sizes, spacing, etc. from the semantic tokens
      borderRadius: {
        'button': 'var(--comp-button-main-radius)',
        'card': 'var(--comp-button-card-radius)',
        'input': 'var(--comp-input-radius)',
        'modal': 'var(--comp-modal-radius)',
      },
      padding: {
        'button-h-sm': 'var(--comp-button-main-h-padding-s)',
        'button-v-sm': 'var(--comp-button-main-v-padding-s)',
        'button-h-md': 'var(--comp-button-main-h-padding-m)',
        'button-v-md': 'var(--comp-button-main-v-padding-m)',
        'button-h-lg': 'var(--comp-button-main-h-padding-l)',
        'button-v-lg': 'var(--comp-button-main-v-padding-l)',
      },
      gap: {
        'button': 'var(--comp-button-main-gap)',
        'input': 'var(--comp-input-gap)',
        'modal': 'var(--comp-modal-gap)',
      }
    },
  },
  plugins: [
    // Add a plugin to generate utility classes from semantic tokens
    function({ addBase }) {
      addBase({
        ':root': {
          // Import the semantic tokens CSS file
          '@import': "url('../src/styles/tokens/semantic-tokens/_evydcore_comp.scss')",
        }
      });
    }
  ],
} 