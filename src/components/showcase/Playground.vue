<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { TokenDefinition } from '@/utils/tokenUtils';
import Button from '../ui/Button.vue';

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
    default: () => [
      { value: 'primary', label: 'Primary' },
      { value: 'secondary', label: 'Secondary' },
      { value: 'outline', label: 'Outline' },
      { value: 'ghost', label: 'Ghost' },
      { value: 'danger', label: 'Danger' },
      { value: 'warning', label: 'Warning' },
      { value: 'success', label: 'Success' },
    ]
  },
  tokens: {
    type: Array as () => TokenDefinition[],
    default: () => []
  },
  variant: {
    type: String,
    default: ''
  },
  showCommonTokens: {
    type: Boolean,
    default: true
  },
  showSizeTokens: {
    type: Boolean,
    default: true
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

const emit = defineEmits(['update:config', 'update:tokenValues']);

const copiedToken = ref<string | null>(null);
const activeTab = ref<'config' | 'tokens'>('config');
const showToast = ref(false);
const toastMessage = ref('');

const updateConfig = (key: string, value: any) => {
  emit('update:config', key, value);
};

const copyToClipboard = async (token: TokenDefinition) => {
  try {
    await navigator.clipboard.writeText(token.name);
    copiedToken.value = token.name;
    toastMessage.value = `Token copied: ${token.name}`;
    showToast.value = true;
    setTimeout(() => {
      copiedToken.value = null;
      showToast.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};

// Add size suffix mapping
const sizeSuffixMap = {
  'sm': '-s',
  'md': '-m',
  'lg': '-l',
  'xl': '-xl'
} as const;

// Update the computed properties and add new ones
const currentTokenValues = computed(() => ({
  padding: {
    sm: 'var(--comp-button-main-h-padding-s)',
    md: 'var(--comp-button-main-h-padding-m)',
    lg: 'var(--comp-button-main-h-padding-l)'
  }[props.currentSize],
  fontSize: {
    sm: 'var(--font-size-12)',
    md: 'var(--font-size-14)',
    lg: 'var(--font-size-16)'
  }[props.currentSize],
  background: `var(--color-fill-${props.currentType}-${props.currentState})`,
  text: `var(--color-text-${props.currentType}-${props.currentState})`,
  border: `var(--color-border-${props.currentType}-${props.currentState})`
}));

// Update the activeTokens computed property
const activeTokens = computed(() => {
  const tokens = [...props.tokens];
  const currentState = props.currentState;
  const currentSize = props.currentSize;
  const currentType = props.currentType;
  const sizeSuffix = sizeSuffixMap[currentSize as keyof typeof sizeSuffixMap];

  return tokens.filter(token => {
    // Always show token-code entries
    if (token.name.includes('token-code')) {
      return true;
    }

    // Filter size-specific tokens - only show tokens matching current size suffix
    if (token.name.includes('padding') || token.name.includes('height') || token.name.includes('width')) {
      return token.name.endsWith(sizeSuffix);
    }

    // Filter state-specific tokens
    if (token.name.includes(currentState)) return true;

    // Filter variant-specific tokens
    if (currentType && token.name.includes(currentType)) return true;

    // Keep common tokens that don't have size variations
    if (token.name.includes('main') && 
        !token.name.includes('padding') && 
        !token.name.includes('height') && 
        !token.name.includes('width')) return true;

    return false;
  });
});

// Update the groupedTokens computed property
const groupedTokens = computed(() => {
  const groups: { [key: string]: TokenDefinition[] } = {
    common: [],
    sizes: [],
    states: []
  };

  const sizeSuffix = sizeSuffixMap[props.currentSize as keyof typeof sizeSuffixMap];

  activeTokens.value.forEach(token => {
    // Group size-related tokens
    if (token.name.includes('token-code') || 
        (token.name.includes('padding') && token.name.endsWith(sizeSuffix)) || 
        (token.name.includes('height') && token.name.endsWith(sizeSuffix)) || 
        (token.name.includes('width') && token.name.endsWith(sizeSuffix))) {
      groups.sizes.push(token);
    }
    // Group state-related tokens
    else if (token.name.includes(props.currentState) || 
             token.name.includes('rest') || 
             token.name.includes('hover') || 
             token.name.includes('press') || 
             token.name.includes('focus') || 
             token.name.includes('disabled')) {
      groups.states.push(token);
    }
    // Group common tokens
    else if (!token.name.includes('padding') && 
             !token.name.includes('height') && 
             !token.name.includes('width')) {
      groups.common.push(token);
    }
  });

  // Sort size tokens to keep related tokens together
  groups.sizes.sort((a, b) => {
    // Keep token-code at the top
    if (a.name.includes('token-code')) return -1;
    if (b.name.includes('token-code')) return 1;

    // Then sort by type (padding, height, width)
    const order = ['padding', 'height', 'width'];
    const aType = order.find(type => a.name.includes(type)) || '';
    const bType = order.find(type => b.name.includes(type)) || '';
    
    if (aType !== bType) {
      return order.indexOf(aType) - order.indexOf(bType);
    }

    // Then sort by orientation (h vs v) for padding
    if (a.name.includes('padding') && b.name.includes('padding')) {
      return a.name.includes('-h-') ? -1 : 1;
    }

    return a.name.localeCompare(b.name);
  });

  return groups;
});

// Add methods for token group display logic
const shouldShowTokenGroup = (groupName: string) => {
  if (groupName === 'common' && props.showCommonTokens) return true;
  if (groupName === 'sizes' && props.showSizeTokens) return true;
  if (groupName === 'states') return true;
  return false;
};

// Update the token group title to include size
const getTokenGroupTitle = (groupName: string) => {
  switch (groupName) {
    case 'common':
      return 'Common Tokens';
    case 'sizes':
      return `Size Tokens (${props.currentSize.toUpperCase()})`;
    case 'states':
      return 'State Tokens';
    default:
      return groupName;
  }
};

// Add watchers for state changes
watch([() => props.currentSize, () => props.currentState, () => props.currentType], 
  ([size, state, type]) => {
    // Emit token values update
    emit('update:tokenValues', currentTokenValues.value);
    
    // Update preview styles
    const previewButton = document.querySelector('.preview-button');
    if (previewButton) {
      previewButton.style.setProperty('--button-background', currentTokenValues.value.background);
      previewButton.style.setProperty('--button-text', currentTokenValues.value.text);
      previewButton.style.setProperty('--button-border', currentTokenValues.value.border);
    }
  },
  { immediate: true }
);
</script>

<template>
  <div class="playground">
    <!-- Toast Notification -->
    <div 
      v-if="showToast" 
      class="toast-notification"
      :class="{ 'toast-notification--show': showToast }"
    >
      {{ toastMessage }}
    </div>

    <!-- Header -->
    <div class="playground-header">
      <h3 class="playground-title">{{ title }}</h3>
      <div class="icon-group">
        <button class="icon-button" aria-label="Copy component code">
          <i class="icon-copy"></i>
        </button>
        <button class="icon-button" aria-label="Reset to defaults">
          <i class="icon-refresh"></i>
        </button>
      </div>
    </div>

    <!-- Preview Section - Always visible -->
    <div class="preview-section">
      <div class="preview-area">
        <Button
          :size="currentSize"
          :variant="currentType"
          :disabled="currentState === 'disabled'"
          :loading="currentState === 'loading'"
          class="preview-button"
          :class="[
            `button-${currentType}`,
            `button-${currentSize}`,
            currentState === 'hover' && 'hover',
            currentState === 'press' && 'active',
            currentState === 'focus' && 'focus'
          ]"
          :style="{
            '--button-background': currentTokenValues.background,
            '--button-text': currentTokenValues.text,
            '--button-border': currentTokenValues.border
          }"
        >
          <template v-if="showLeadingIcon" #leading-icon>
            <i class="icon-mail"></i>
          </template>
          <span v-if="showLabel">{{ labelText }}</span>
          <template v-if="showTrailingIcon" #trailing-icon>
            <i class="icon-arrow-right"></i>
          </template>
        </Button>
      </div>
    </div>

    <!-- Split View Container -->
    <div class="split-view">
      <!-- Left Side: Configuration -->
      <div class="split-view-panel">
        <h4 class="panel-title">Configuration</h4>
        <div class="config-section">
          <!-- Existing configuration controls -->
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
        </div>
      </div>

      <!-- Right Side: Tokens -->
      <div class="split-view-panel">
        <h4 class="panel-title">Design Tokens</h4>
        <div class="tokens-section">
          <div v-for="(group, groupName) in groupedTokens" 
               :key="groupName" 
               class="token-table-container"
               v-show="shouldShowTokenGroup(groupName)"
          >
            <h5 class="token-group-title">
              {{ getTokenGroupTitle(groupName) }}
              <span v-if="groupName === 'states'" class="token-variant-label">
                {{ currentType }}/{{ currentState }}
              </span>
            </h5>
            <div class="token-table">
              <table class="min-w-full divide-y token-table-divider">
                <thead class="token-table-header">
                  <tr>
                    <th class="token-table-th">Token</th>
                    <th class="token-table-th">Value</th>
                    <th class="token-table-th">Usage</th>
                  </tr>
                </thead>
                <tbody class="token-table-body divide-y token-table-divider">
                  <tr 
                    v-for="token in group" 
                    :key="token.name"
                    @click="copyToClipboard(token)"
                    class="token-row"
                    :class="{
                      'active-token': token.name.includes(currentState),
                      'token-code-row': token.name.includes('token-code')
                    }"
                  >
                    <td class="token-table-td">
                      <div class="token-name-container">
                        <code class="token-code" :class="{ 'is-token-code': token.name.includes('token-code') }">
                          {{ token.name }}
                        </code>
                        <span class="copy-indicator" v-if="copiedToken === token.name">
                          <i class="icon-check"></i>
                        </span>
                      </div>
                    </td>
                    <td class="token-table-td">
                      <div class="token-value-container">
                        <code class="token-code token-value" :class="{ 'is-token-code': token.name.includes('token-code') }">
                          {{ token.value }}
                        </code>
                      </div>
                    </td>
                    <td class="token-table-td token-usage">{{ token.usage }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.playground {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
  background-color: var(--color-surface-secondary-rest);
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-h-padding-l);
}

.playground-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--comp-button-main-gap);
}

.playground-title {
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-primary-rest);
}

.icon-group {
  display: flex;
  gap: var(--comp-button-main-gap);
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

/* Configuration Panel Styles */
.config-section {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
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

.control-options {
  display: flex;
  gap: var(--comp-button-main-gap);
}

.control-options--wrap {
  flex-wrap: wrap;
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

.control-button--selected {
  background-color: var(--color-fill-brand-rest);
  color: var(--color-text-primary-inverse);
  border-color: var(--color-border-brand-rest);
}

/* Token Table Styles */
.tokens-section {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.token-table-container {
  margin-bottom: var(--comp-button-main-gap);
}

.token-table {
  overflow-x: auto;
  border: none;
  border-radius: var(--comp-button-main-radius);
}

.token-table-divider {
  border: none;
}

.token-table-header {
  background-color: transparent;
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.token-table-th {
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  text-align: left;
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  text-transform: uppercase;
  vertical-align: middle;
  border: none;
}

.token-table-td {
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  white-space: nowrap;
  vertical-align: middle;
  border: none;
  cursor: pointer;
}

.token-code {
  font-family: monospace;
  font-size: var(--font-size-12);
  color: var(--color-text-primary-rest);
  background-color: transparent;
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  border-radius: calc(var(--comp-button-main-radius) * 0.75);
  position: relative;
  z-index: 1;
}

.token-value-container {
  display: flex;
  align-items: center;
  gap: var(--comp-button-main-gap);
}

.copy-button {
  padding: var(--comp-button-main-v-padding-xs);
  border-radius: calc(var(--comp-button-main-radius) * 0.75);
  color: var(--color-icon-secondary-rest);
  transition: all 0.2s ease;
}

.copy-button:hover {
  color: var(--color-icon-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

.copy-button.copied {
  color: var(--color-success-rest);
}

.token-usage {
  color: var(--color-text-secondary-rest);
  font-size: var(--font-size-12);
  position: relative;
  z-index: 1;
}

/* Shared Styles */
.control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.toggle-switch--active {
  background-color: var(--color-fill-brand-rest);
  border-color: var(--color-border-brand-rest);
}

.toggle-switch__handle {
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: var(--color-fill-neutral-rest);
  position: absolute;
  top: 0.25rem;
  left: 0.25rem;
  transition: all 0.2s ease;
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

.config-input:focus {
  border-color: var(--color-border-brand-focus);
  outline: none;
}

/* Update the preview section styles */
.preview-section {
  padding: var(--comp-button-main-v-padding-l) 0;
  border-bottom: 1px solid var(--color-border-primary-rest);
  margin-bottom: var(--comp-button-main-gap);
}

.preview-area {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  padding: var(--comp-button-main-v-padding-xl);
  border-radius: var(--comp-button-main-radius);
  position: relative;
  background-color: var(--color-fill-grey-rest);
  border: 2px dotted var(--color-border-primary-rest);
  transition: all 0.2s ease;
}

/* Remove the checkerboard pattern */
.preview-area::before {
  content: none;
}

/* Add hover effect */
.preview-area:hover {
  border-color: var(--color-border-brand-rest);
  background-color: var(--color-fill-grey-hover);
}

/* Dark mode adjustments */
:root[data-theme="dark"] .preview-area {
  background-color: var(--color-surface-secondary-rest);
  border-color: var(--color-border-primary-rest);
}

:root[data-theme="dark"] .preview-area:hover {
  border-color: var(--color-border-brand-rest);
  background-color: var(--color-surface-secondary-hover);
}

/* Add a subtle shadow for depth */
.preview-area::after {
  content: 'Preview';
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  font-size: var(--font-size-12);
  color: var(--color-text-secondary-rest);
  pointer-events: none;
}

.token-variant-label {
  color: var(--color-text-brand-rest);
  font-size: var(--font-size-12);
  font-weight: normal;
  margin-left: var(--comp-button-main-gap);
}

/* State simulation styles */
:deep(.hover) {
  opacity: 0.9;
}

:deep(.active) {
  opacity: 0.8;
}

:deep(.focus) {
  outline: 2px solid var(--color-border-brand-focus);
  outline-offset: 2px;
}

/* Split View Styles */
.split-view {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--comp-button-main-gap);
  margin-top: var(--comp-button-main-gap);
}

.split-view-panel {
  background-color: transparent;
  border: none;
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-h-padding-l);
  height: fit-content;
  max-height: 800px;
  overflow-y: auto;
}

.panel-title {
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  margin-bottom: var(--comp-button-main-gap);
}

.token-group-title {
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  margin-bottom: var(--comp-button-main-gap);
  display: flex;
  align-items: center;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .split-view {
    grid-template-columns: 1fr;
  }
}

/* Scrollbar styles for panels */
.split-view-panel {
  scrollbar-width: thin;
  scrollbar-color: var(--color-scrollbar-thumb-rest) transparent;
}

.split-view-panel::-webkit-scrollbar {
  width: 6px;
}

.split-view-panel::-webkit-scrollbar-track {
  background: transparent;
}

.split-view-panel::-webkit-scrollbar-thumb {
  background-color: var(--color-scrollbar-thumb-rest);
  border-radius: 3px;
}

.split-view-panel::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-scrollbar-thumb-hover);
}

/* Add hover state for table rows */
.token-table tbody tr {
  transition: background-color 0.2s ease;
}

.token-table tbody tr:hover {
  background-color: var(--color-surface-secondary-hover);
}

/* Add click feedback */
.token-table tbody tr:active {
  background-color: var(--color-surface-secondary-press);
}

/* Toast notification styles */
.toast-notification {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: var(--comp-button-main-v-padding-m) var(--comp-button-main-h-padding-l);
  background-color: var(--color-surface-success-rest);
  color: var(--color-text-success-rest);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  opacity: 0;
  transform: translateY(1rem);
  transition: all 0.2s ease;
  z-index: 50;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.toast-notification--show {
  opacity: 1;
  transform: translateY(0);
}

/* Make the entire row clickable for copying */
.token-table tbody tr {
  cursor: pointer;
}

/* Remove copy button since entire row is clickable */
.copy-button {
  display: none;
}

/* Add styles for token row */
.token-row {
  position: relative;
  transition: background-color 0.2s ease;
}

.token-row::after {
  content: none;
}

.token-row:hover {
  background-color: var(--color-surface-secondary-hover);
}

.token-row:active {
  background-color: var(--color-surface-secondary-press);
}

/* Dark mode adjustments */
:root[data-theme="dark"] .token-row:hover {
  background-color: var(--color-surface-secondary-hover);
}

:root[data-theme="dark"] .token-row:active {
  background-color: var(--color-surface-secondary-press);
}

/* Remove table dividers since we're using hover states */
.token-table-divider {
  border: none;
}

/* Add subtle spacing between rows */
.token-table-td {
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  white-space: nowrap;
  vertical-align: middle;
  border: none;
  cursor: pointer;
}

/* Add styles for dynamic token highlighting */
.token-row.active-token {
  background-color: var(--color-surface-brand-rest);
}

.token-row.active-token .token-code {
  color: var(--color-text-primary-rest);
}

.token-row.active-token .token-usage {
  color: var(--color-text-secondary-rest);
}

/* Update preview button styles */
.preview-button {
  background-color: var(--button-background) !important;
  color: var(--button-text) !important;
  border-color: var(--button-border) !important;
}

/* Improve hover state visibility */
.token-row:hover .token-code {
  color: var(--color-text-primary-rest);
}

.token-row:hover .token-usage {
  color: var(--color-text-secondary-rest);
}

/* Dark mode adjustments */
:root[data-theme="dark"] .token-row:hover .token-code {
  color: var(--color-text-primary-rest);
}

:root[data-theme="dark"] .token-row:hover .token-usage {
  color: var(--color-text-secondary-rest);
}

/* Add these new styles */
.token-name-container {
  display: flex;
  align-items: center;
  gap: var(--comp-button-main-gap);
  position: relative;
}

.token-code {
  font-family: monospace;
  font-size: var(--font-size-12);
  color: var(--color-text-primary-rest);
  background-color: transparent;
  padding: var(--comp-button-main-v-padding-xs) var(--comp-button-main-h-padding-xs);
  border-radius: calc(var(--comp-button-main-radius) * 0.75);
  position: relative;
  z-index: 1;
}

.token-code.token-value {
  color: var(--color-text-secondary-rest);
}

.copy-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-success-rest);
  font-size: var(--font-size-12);
  opacity: 0;
  transform: translateX(-0.5rem);
  transition: all 0.2s ease;
}

.token-row:hover .copy-indicator {
  opacity: 0.5;
  transform: translateX(0);
}

.token-row .copy-indicator i {
  width: 1rem;
  height: 1rem;
}

/* Update toast notification styles */
.toast-notification {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Update hover state for token rows */
.token-row {
  position: relative;
  transition: all 0.2s ease;
}

.token-row:hover .token-code:not(.token-value) {
  color: var(--color-text-brand-rest);
}

.token-row:active .token-code:not(.token-value) {
  color: var(--color-text-brand-press);
}

/* Dark mode adjustments */
:root[data-theme="dark"] .token-row:hover .token-code:not(.token-value) {
  color: var(--color-text-brand-rest);
}

:root[data-theme="dark"] .token-row:active .token-code:not(.token-value) {
  color: var(--color-text-brand-press);
}

/* Add these new styles */
.token-code-row {
  background-color: var(--color-surface-secondary-rest);
}

.token-code-row:hover {
  background-color: var(--color-surface-secondary-hover);
}

.token-code.is-token-code {
  color: var(--color-text-brand-rest);
  font-weight: var(--font-weight-medium-500);
}

.token-code-row .token-value {
  color: var(--color-text-secondary-rest) !important;
}

/* Update existing token row styles */
.token-row {
  position: relative;
  transition: all 0.2s ease;
}

.token-row:not(.token-code-row):hover .token-code:not(.token-value) {
  color: var(--color-text-brand-rest);
}

.token-row:not(.token-code-row):active .token-code:not(.token-value) {
  color: var(--color-text-brand-press);
}

/* Dark mode adjustments */
:root[data-theme="dark"] .token-code-row {
  background-color: var(--color-surface-secondary-rest);
}

:root[data-theme="dark"] .token-code-row:hover {
  background-color: var(--color-surface-secondary-hover);
}

:root[data-theme="dark"] .token-code.is-token-code {
  color: var(--color-text-brand-rest);
}
</style> 