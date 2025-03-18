<script setup lang="ts">
import { ref } from 'vue';
import Button from '../ui/Button.vue';
import ConfigPanel from './ConfigPanel.vue';

type ButtonSize = 'sm' | 'md' | 'lg';
type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost';

const size = ref<ButtonSize>('sm');
const state = ref('rest');
const type = ref<ButtonVariant>('primary');
const showLabel = ref(true);
const showLeadingIcon = ref(true);
const showTrailingIcon = ref(false);
const label = ref('Open Mail');
const leadingIcon = ref('mail-01');

// Handle config updates from ConfigPanel
const updateConfig = (configKey: string, value: any) => {
  if (configKey === 'size') size.value = value;
  if (configKey === 'state') state.value = value;
  if (configKey === 'type') type.value = value;
  if (configKey === 'showLabel') showLabel.value = value;
  if (configKey === 'showLeadingIcon') showLeadingIcon.value = value;
  if (configKey === 'showTrailingIcon') showTrailingIcon.value = value;
  if (configKey === 'label') label.value = value;
};

// Token values passed to ConfigPanel
const tokenValues = {
  padding: {
    sm: '0.5rem 1rem',
    md: '0.75rem 1.5rem',
    lg: '1rem 2rem'
  } as const,
  fontSize: {
    sm: '0.875rem',
    md: '1rem',
    lg: '1.125rem'
  } as const
};

const copyTokenValue = async (value: string) => {
  try {
    await navigator.clipboard.writeText(value);
    // You could add a toast notification here
  } catch (err) {
    console.error('Failed to copy:', err);
  }
};

const sizes = [
  { value: 'sm', label: 'Small' },
  { value: 'md', label: 'Medium' },
  { value: 'lg', label: 'Large' }
];

const states = [
  { value: 'rest', label: 'Rest' },
  { value: 'hover', label: 'Hover' },
  { value: 'disabled', label: 'Disabled' },
  { value: 'loading', label: 'Loading' }
];

const types = [
  { value: 'primary', label: 'Primary' },
  { value: 'secondary', label: 'Secondary' },
  { value: 'outline', label: 'Outline' },
  { value: 'ghost', label: 'Ghost' }
];
</script>

<template>
  <div class="flex flex-col lg:flex-row gap-8">
    <!-- Preview Area -->
    <div class="flex-1 preview-background rounded-lg p-8 flex items-center justify-center">
      <Button
        :size="size"
        :variant="type"
        :disabled="state === 'disabled'"
        :loading="state === 'loading'"
      >
        <template v-if="showLeadingIcon" #leading-icon>
          <i :class="`icon-${leadingIcon}`"></i>
        </template>
        <span v-if="showLabel">{{ label }}</span>
        <template v-if="showTrailingIcon" #trailing-icon>
          <i class="icon-arrow-right"></i>
        </template>
      </Button>
    </div>

    <!-- Controls Area - Using ConfigPanel -->
    <ConfigPanel 
      title="button-main-v1.2.0"
      :current-size="size"
      :current-state="state"
      :current-type="type"
      :show-label="showLabel"
      :label-text="label"
      :show-leading-icon="showLeadingIcon"
      :show-trailing-icon="showTrailingIcon"
      :size-options="[
        { value: 'sm', label: 'Small' },
        { value: 'md', label: 'Medium' },
        { value: 'lg', label: 'Large' }
      ]"
      :state-options="[
        { value: 'rest', label: 'Rest' },
        { value: 'hover', label: 'Hover' },
        { value: 'disabled', label: 'Disabled' },
        { value: 'loading', label: 'Loading' }
      ]"
      :type-options="[
        { value: 'primary', label: 'Primary' },
        { value: 'secondary', label: 'Secondary' },
        { value: 'outline', label: 'Outline' },
        { value: 'ghost', label: 'Ghost' }
      ]"
      :token-values="{
        padding: tokenValues.padding[size],
        fontSize: tokenValues.fontSize[size],
        brand: 'Auto (EVYDCore)',
        colorMode: 'Auto (Light/Dark)',
        tokenColor: 'Auto (EVYD Core)'
      }"
      @update:config="updateConfig"
    />
  </div>
</template>

<style scoped>
.icon-copy {
  width: 1rem;
  height: 1rem;
}

.preview-background {
  background-color: var(--color-surface-secondary-rest);
}
</style> 