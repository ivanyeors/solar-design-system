<script setup lang="ts">
import { defineProps, defineEmits } from 'vue';

interface Option {
  value: string;
  label: string;
}

interface TokenValues {
  padding: string;
  fontSize: string;
  brand: string;
  colorMode: string;
  tokenColor: string;
}

const props = defineProps({
  title: {
    type: String,
    default: 'component-v1.0.0'
  },
  currentSize: {
    type: String,
    default: 'sm'
  },
  currentState: {
    type: String,
    default: 'rest'
  },
  currentType: {
    type: String,
    default: 'primary'
  },
  showLabel: {
    type: Boolean,
    default: true
  },
  labelText: {
    type: String,
    default: 'Button Label'
  },
  showLeadingIcon: {
    type: Boolean,
    default: false
  },
  showTrailingIcon: {
    type: Boolean,
    default: false
  },
  sizeOptions: {
    type: Array as () => Option[],
    default: () => []
  },
  stateOptions: {
    type: Array as () => Option[],
    default: () => []
  },
  typeOptions: {
    type: Array as () => Option[],
    default: () => []
  },
  tokenValues: {
    type: Object as () => TokenValues,
    default: () => ({
      padding: '0.5rem 1rem',
      fontSize: '0.875rem',
      brand: 'Auto (Default)',
      colorMode: 'Auto (Light/Dark)',
      tokenColor: 'Auto (Default)'
    })
  }
});

const emit = defineEmits(['update:config']);

const updateConfig = (key: string, value: any) => {
  emit('update:config', key, value);
};

const copyToClipboard = async (text: string) => {
  try {
    await navigator.clipboard.writeText(text);
    // You could add a toast notification here
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};
</script>

<template>
  <div class="config-panel">
    <div class="header">
      <h3 class="config-title">{{ title }}</h3>
      <div class="icon-group">
        <button class="icon-button" aria-label="Copy component code">
          <i class="icon-copy"></i>
        </button>
        <button class="icon-button" aria-label="Reset to defaults">
          <i class="icon-refresh"></i>
        </button>
      </div>
    </div>

    <!-- Size Control -->
    <div class="control-group">
      <label class="control-label">Size</label>
      <div class="control-options">
        <button 
          v-for="option in sizeOptions" 
          :key="option.value"
          class="control-button"
          :class="{ 'control-button--selected': currentSize === option.value }"
          @click="updateConfig('size', option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <!-- State Control -->
    <div class="control-group">
      <label class="control-label">State</label>
      <div class="control-options control-options--wrap">
        <button 
          v-for="option in stateOptions" 
          :key="option.value"
          class="control-button"
          :class="{ 'control-button--selected': currentState === option.value }"
          @click="updateConfig('state', option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <!-- Type Control -->
    <div class="control-group">
      <label class="control-label">Type</label>
      <div class="control-options control-options--wrap">
        <button 
          v-for="option in typeOptions" 
          :key="option.value"
          class="control-button"
          :class="{ 'control-button--selected': currentType === option.value }"
          @click="updateConfig('type', option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>

    <!-- Label Controls -->
    <div class="control-group">
      <div class="control-row">
        <label class="control-label">Show Label</label>
        <button 
          class="toggle-switch" 
          :class="{ 'toggle-switch--active': showLabel }"
          @click="updateConfig('showLabel', !showLabel)"
        >
          <span class="toggle-switch__handle"></span>
        </button>
      </div>
      <input 
        v-if="showLabel"
        :value="labelText"
        @input="updateConfig('label', ($event.target as HTMLInputElement).value)"
        class="config-input" 
        placeholder="Button Label"
      >
    </div>

    <!-- Icon Controls -->
    <div class="control-group">
      <div class="control-row">
        <label class="control-label">Show Leading Icon</label>
        <button 
          class="toggle-switch" 
          :class="{ 'toggle-switch--active': showLeadingIcon }"
          @click="updateConfig('showLeadingIcon', !showLeadingIcon)"
        >
          <span class="toggle-switch__handle"></span>
        </button>
      </div>
      <div class="control-row">
        <label class="control-label">Show Trailing Icon</label>
        <button 
          class="toggle-switch" 
          :class="{ 'toggle-switch--active': showTrailingIcon }"
          @click="updateConfig('showTrailingIcon', !showTrailingIcon)"
        >
          <span class="toggle-switch__handle"></span>
        </button>
      </div>
    </div>

    <!-- Token Values -->
    <div class="token-section">
      <h4 class="token-section__title">Token Values</h4>
      
      <!-- Size-specific tokens -->
      <div class="token-group">
        <div class="token-row">
          <span class="token-label">Padding</span>
          <button class="token-value" @click="copyToClipboard(tokenValues.padding)">
            {{ tokenValues.padding }}
            <i class="icon-copy"></i>
          </button>
        </div>
        <div class="token-row">
          <span class="token-label">Font Size</span>
          <button class="token-value" @click="copyToClipboard(tokenValues.fontSize)">
            {{ tokenValues.fontSize }}
            <i class="icon-copy"></i>
          </button>
        </div>
      </div>

      <!-- Theme tokens -->
      <div class="token-group">
        <div class="token-row">
          <span class="token-label">Brand</span>
          <button class="token-value" @click="copyToClipboard(tokenValues.brand)">
            {{ tokenValues.brand }}
            <i class="icon-copy"></i>
          </button>
        </div>
        <div class="token-row">
          <span class="token-label">Color Mode</span>
          <button class="token-value" @click="copyToClipboard(tokenValues.colorMode)">
            {{ tokenValues.colorMode }}
            <i class="icon-copy"></i>
          </button>
        </div>
        <div class="token-row">
          <span class="token-label">Token Color</span>
          <button class="token-value" @click="copyToClipboard(tokenValues.tokenColor)">
            {{ tokenValues.tokenColor }}
            <i class="icon-copy"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.config-panel {
  width: 20rem;
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
  background-color: var(--color-surface-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-h-padding-l);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.icon-group {
  display: flex;
  gap: var(--comp-button-main-gap);
}

.control-options {
  display: flex;
  gap: var(--comp-button-main-gap);
}

.control-options--wrap {
  flex-wrap: wrap;
}

.control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-title {
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-primary-rest);
}

.icon-button {
  color: var(--color-icon-secondary-rest);
  padding: var(--comp-button-main-v-padding-s);
  border-radius: var(--comp-button-main-radius);
  transition: all 0.2s ease;
}

.icon-button:hover {
  color: var(--color-icon-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.control-label {
  font-size: var(--font-size-14);
  color: var(--color-text-secondary-rest);
}

.control-button {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-14);
  background-color: var(--color-surface-secondary-rest);
  color: var(--color-text-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

.control-button:hover {
  background-color: var(--color-surface-secondary-hover);
  border-color: var(--color-border-primary-hover);
}

.control-button:active {
  background-color: var(--color-surface-secondary-press);
  border-color: var(--color-border-primary-press);
}

.control-button--selected {
  background-color: var(--color-fill-brand-rest);
  color: var(--color-text-primary-inverse);
  border-color: var(--color-border-brand-rest);
}

.control-button--selected:hover {
  background-color: var(--color-fill-brand-hover);
  border-color: var(--color-border-brand-hover);
}

.control-button--selected:active {
  background-color: var(--color-fill-brand-press);
  border-color: var(--color-border-brand-press);
}

.toggle-switch {
  width: 2.5rem;
  height: 1.5rem;
  border-radius: var(--comp-toggle-radius);
  background-color: var(--color-surface-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  position: relative;
  transition: all 0.2s ease;
}

.toggle-switch:hover {
  background-color: var(--color-surface-secondary-hover);
  border-color: var(--color-border-primary-hover);
}

.toggle-switch--active {
  background-color: var(--color-fill-brand-rest);
  border-color: var(--color-border-brand-rest);
}

.toggle-switch--active:hover {
  background-color: var(--color-fill-brand-hover);
  border-color: var(--color-border-brand-hover);
}

.toggle-switch__handle {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: var(--color-fill-neutral-rest);
  position: absolute;
  top: 0.25rem;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px var(--color-border-primary-rest);
}

.toggle-switch:not(.toggle-switch--active) .toggle-switch__handle {
  left: 0.25rem;
}

.toggle-switch--active .toggle-switch__handle {
  left: 1.25rem;
}

.config-input {
  width: 100%;
  padding: var(--comp-input-v-padding-m) var(--comp-input-h-padding-m);
  border-radius: var(--comp-input-radius);
  background-color: var(--color-surface-secondary-rest);
  color: var(--color-text-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

.config-input:hover {
  border-color: var(--color-border-primary-hover);
}

.config-input:focus {
  border-color: var(--color-border-brand-focus);
  outline: none;
  box-shadow: 0 0 0 2px var(--color-border-brand-focus);
}

.config-input::placeholder {
  color: var(--color-text-secondary-rest);
}

.token-section {
  padding-top: var(--comp-button-main-v-padding-l);
  border-top: 1px solid var(--color-border-primary-rest);
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.token-section__title {
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
}

.token-group {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.token-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-14);
}

.token-label {
  color: var(--color-text-secondary-rest);
}

.token-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-primary-rest);
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s);
  border-radius: var(--comp-button-main-radius);
  transition: all 0.2s ease;
}

.token-value:hover {
  color: var(--color-text-primary-hover);
  background-color: var(--color-surface-secondary-hover);
}

.token-value:active {
  color: var(--color-text-primary-press);
  background-color: var(--color-surface-secondary-press);
}

.token-value i {
  color: var(--color-icon-secondary-rest);
  transition: color 0.2s ease;
}

.token-value:hover i {
  color: var(--color-icon-secondary-hover);
}

.token-value:active i {
  color: var(--color-icon-secondary-pressed);
}
</style> 