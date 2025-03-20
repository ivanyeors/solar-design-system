<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import hljs from 'highlight.js/lib/core';
import javascript from 'highlight.js/lib/languages/javascript';
import xml from 'highlight.js/lib/languages/xml';
import 'highlight.js/styles/github-dark.css';

// Register languages
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('xml', xml);

defineProps<{
  title: string;
  description?: string;
  componentName: string;
}>();

const activeTab = ref('preview');
const showCopied = ref(false);
const codeRef = ref<HTMLElement | null>(null);

// Function to format code with Atlassian-style indentation
const formatCode = (code: string) => {
  const lines = code.split('\n');
  let indentLevel = 0;
  const indentSize = 2;
  const indentChar = ' ';
  
  return lines
    .map(line => {
      const trimmedLine = line.trim();
      
      // Handle closing brackets/tags - decrease indent before the line
      if (trimmedLine.match(/^[}\]>]/)) {
        indentLevel = Math.max(0, indentLevel - 1);
      }
      
      // Special handling for JSX/TSX closing tags
      if (trimmedLine.match(/^<\/[^>]+>/)) {
        indentLevel = Math.max(0, indentLevel - 1);
      }
      
      // Calculate current line indent
      const indent = indentChar.repeat(indentLevel * indentSize);
      const formattedLine = trimmedLine ? (indent + trimmedLine) : '';
      
      // Handle opening brackets/tags - increase indent after the line
      if (
        trimmedLine.match(/[{(<]$/) || // Opening brackets
        trimmedLine.match(/<[^/][^>]*>$/) || // Opening JSX/TSX tags
        trimmedLine.match(/[{([]$/) // Array/object literals
      ) {
        indentLevel++;
      }
      
      return formattedLine;
    })
    .filter(line => line.length > 0) // Remove empty lines
    .join('\n');
};

// Compute the number of lines in the code plus 1 extra line
const totalLines = computed(() => {
  const codeElement = codeRef.value;
  if (!codeElement) return 2;
  return codeElement.textContent?.split('\n').length ?? 1 + 1;
});

// Copy code function
const copyCode = async () => {
  try {
    const codeElement = document.querySelector('.code-block code') as HTMLElement;
    if (!codeElement) return;

    // Get the actual text content and format it
    const rawCode = codeElement.textContent || '';
    const formattedCode = formatCode(rawCode);

    // Copy the formatted code
    await navigator.clipboard.writeText(formattedCode);
    
    // Show success state
    showCopied.value = true;
    setTimeout(() => {
      showCopied.value = false;
    }, 2000);
  } catch (err) {
    console.error('Failed to copy code:', err);
  }
};

onMounted(() => {
  // Get the code content and store the reference
  const codeElement = document.querySelector('.code-block code') as HTMLElement;
  if (codeElement) {
    codeRef.value = codeElement;
    const rawCode = codeElement.textContent || '';
    const formattedCode = formatCode(rawCode);
    codeElement.textContent = formattedCode;
    hljs.highlightElement(codeElement);
  }
});
</script>

<template>
  <div class="showcase-container">
    <!-- Component header -->
    <div class="showcase-header">
      <h2 class="showcase-title">{{ title }}</h2>
      <p v-if="description" class="showcase-description">{{ description }}</p>
    </div>
    
    <!-- Tab navigation -->
    <div class="showcase-tabs-border">
      <nav class="flex -mb-px">
        <button
          @click="activeTab = 'preview'"
          :class="[
            'showcase-tab',
            activeTab === 'preview'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
          ]"
        >
          Preview
        </button>
        <button
          @click="activeTab = 'code'"
          :class="[
            'showcase-tab',
            activeTab === 'code'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
          ]"
        >
          Code
        </button>
        <button
          @click="activeTab = 'props'"
          :class="[
            'showcase-tab',
            activeTab === 'props'
              ? 'showcase-tab--active'
              : 'showcase-tab--inactive'
          ]"
        >
          Props
        </button>
      </nav>
    </div>
    
    <!-- Tab content -->
    <div>
      <!-- Preview tab -->
      <div v-if="activeTab === 'preview'" class="p-6">
        <div class="flex flex-wrap gap-4">
          <slot name="preview"></slot>
        </div>
      </div>
      
      <!-- Code tab -->
      <div v-if="activeTab === 'code'" class="p-6">
        <div class="code-container">
          <div class="code-header">
            <span class="code-language">{{ componentName }}.vue</span>
            <button 
              class="copy-button" 
              @click="copyCode"
              :class="{ 'copied': showCopied }"
            >
              <span class="button__icon button__icon--leading" v-if="!showCopied">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
              </span>
              <span class="button__content">
                {{ showCopied ? 'Copied!' : 'Copy' }}
              </span>
              <span class="button__icon button__icon--leading" v-if="showCopied">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </span>
            </button>
          </div>
          <div class="code-editor">
            <div class="code-editor__line-numbers">
              <template v-for="n in totalLines" :key="n">
                <div class="line-number">{{ n }}</div>
              </template>
            </div>
            <pre class="code-block"><code><slot name="code"></slot></code></pre>
          </div>
        </div>
      </div>
      
      <!-- Props tab -->
      <div v-if="activeTab === 'props'" class="p-6">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y showcase-table-divider">
            <thead>
              <tr>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Prop</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Type</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Default</th>
                <th scope="col" class="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider table-header">Description</th>
              </tr>
            </thead>
            <tbody class="showcase-table-body showcase-table-divider">
              <slot name="props"></slot>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.showcase-container {
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-xs);
  border: 1px solid var(--color-border-primary-rest);
  overflow: hidden;
}

.showcase-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.showcase-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary-rest);
}

.showcase-description {
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary-rest);
}

.showcase-tabs-border {
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.showcase-tab {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-m);
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  border-bottom: 2px solid transparent;
  transition: all var(--transition-fast);
}

.showcase-tab:focus {
  outline: none;
}

.showcase-tab:focus-visible {
  box-shadow: var(--shadow-focus);
}

.showcase-tab--active {
  color: var(--color-text-brand-rest);
  border-bottom-color: var(--color-border-brand-rest);
  background-color: transparent;
}

.showcase-tab--active:hover {
  color: var(--color-text-brand-hover);
  border-bottom-color: var(--color-border-brand-hover);
}

.showcase-tab--inactive {
  color: var(--color-text-secondary-rest);
  border-bottom-color: transparent;
  background-color: transparent;
}

.showcase-tab--inactive:hover {
  color: var(--color-text-secondary-hover);
  border-bottom-color: var(--color-border-secondary-hover);
  background-color: var(--color-surface-secondary-hover);
}

.code-container {
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: var(--color-surface-secondary-rest);
  border-bottom: 1px solid var(--color-border-primary-rest);
}

.code-language {
  font-size: var(--font-size-14);
  color: var(--color-text-secondary-rest);
  font-family: var(--font-family-mono);
}

.copy-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--comp-button-main-gap);
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-m);
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  color: var(--color-text-secondary-rest);
  background-color: transparent;
  border: 1px solid var(--color-border-primary-rest);
  border-radius: var(--comp-button-main-radius);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.copy-button:hover {
  background-color: var(--color-surface-primary-hover);
  color: var(--color-text-primary-hover);
  border-color: var(--color-border-primary-hover);
}

.copy-button.copied {
  background-color: var(--color-surface-success-rest);
  color: var(--color-text-success-rest);
  border-color: var(--color-border-success-rest);
}

.copy-button .button__icon {
  width: 20px;
  height: 20px;
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.copy-button .button__icon svg {
  width: 16px;
  height: 16px;
}

.copy-button .button__content {
  position: relative;
  display: inline-flex;
  align-items: center;
}

/* Animation for icon transition */
.copy-button .button__icon,
.copy-button .button__content {
  transition: transform var(--transition-fast);
}

.copy-button.copied .button__icon,
.copy-button.copied .button__content {
  transform: scale(1.05);
}

.code-editor {
  display: flex;
  background-color: var(--color-surface-code-rest);
  font-family: var(--font-family-mono);
  font-size: var(--font-size-14);
  line-height: 1.6;
}

.code-editor__line-numbers {
  flex-shrink: 0;
  padding: 1rem 0;
  background-color: var(--color-surface-code-rest);
  border-right: 1px solid var(--color-border-primary-rest);
  user-select: none;
  position: sticky;
  left: 0;
  z-index: 1;
}

.line-number {
  padding: 0 1rem;
  color: var(--color-text-secondary-rest);
  text-align: right;
  font-size: var(--font-size-12);
  min-width: 3ch;
  opacity: 0.5;
}

.code-block {
  flex-grow: 1;
  margin: 0;
  padding: 1rem;
  background-color: transparent;
  overflow-x: auto;
  color: var(--color-text-code-rest);
  white-space: pre;
  tab-size: 2;
  width: 100%;
  box-sizing: border-box;
}

.code-block code {
  display: block;
  font-family: var(--font-family-mono);
  line-height: 1.6;
}

/* Highlight.js theme overrides with Atlassian-like colors */
:deep(.hljs) {
  background: transparent;
  padding: 0;
  margin: 0;
}

:deep(.hljs-keyword),
:deep(.hljs-tag) {
  color: #0052CC;
  font-weight: 600;
}

:deep(.hljs-string) {
  color: #00875A;
}

:deep(.hljs-comment) {
  color: #5E6C84;
  font-style: italic;
}

:deep(.hljs-function) {
  color: #0747A6;
}

:deep(.hljs-number) {
  color: #00875A;
}

:deep(.hljs-operator) {
  color: #5E6C84;
}

:deep(.hljs-class) {
  color: #0052CC;
  font-weight: 600;
}

:deep(.hljs-attr) {
  color: #0747A6;
}

:deep(.hljs-name) {
  color: #0052CC;
}

.showcase-table-divider {
  border-color: var(--color-border-primary-rest);
}

.showcase-table-body {
  background-color: var(--color-surface-primary-rest);
}

.table-header {
  color: var(--color-text-secondary-rest);
  font-size: var(--font-size-12);
  font-weight: var(--font-weight-medium-500);
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wide);
}
</style> 