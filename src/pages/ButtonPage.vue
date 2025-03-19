<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import Button from '../components/ui/Button.vue';
import Playground from '../components/showcase/Playground.vue';
import ComponentShowcase from '../components/showcase/ComponentShowcase.vue';
import PropRow from '../components/showcase/PropRow.vue';
import SideNavigation from '../components/layout/SideNavigation.vue';
import AccessibilityChecklist from '../components/showcase/AccessibilityChecklist.vue';
import VersionHistory from '../components/showcase/VersionHistory.vue';
import RelatedComponentCard from '../components/showcase/RelatedComponentCard.vue';
import Icon from '../components/ui/Icon.vue';
import { getButtonTokens, getCommonButtonTokens, getButtonSizeTokens } from '../utils/tokenUtils';
import type { ButtonVariant } from '../utils/tokenUtils';

// Active section tracking
const activeSection = ref('overview');
const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'playground', label: 'Playground' },
  { id: 'guidelines', label: 'Guidelines' },
  { id: 'anatomy', label: 'Anatomy' },
  { id: 'states', label: 'States & Variations' },
  { id: 'accessibility', label: 'Accessibility' },
  { id: 'examples', label: 'Examples' },
  { id: 'related', label: 'Related Components' },
  { id: 'version', label: 'Version History' }
];

// Current theme tracking
const currentTheme = ref('light');

// Computed value to determine if dark mode is active
const isDarkTheme = computed(() => currentTheme.value === 'dark');

// Intersection Observer for active section
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeSection.value = entry.target.id;
      }
    });
  }, { threshold: 0.5 });

  sections.forEach(section => {
    const element = document.getElementById(section.id);
    if (element) observer.observe(element);
  });

  // Get initial theme from document
  const dataTheme = document.documentElement.getAttribute('data-theme') || 'light';
  currentTheme.value = dataTheme;

  // Add event listener for theme changes
  const updateTheme = () => {
    currentTheme.value = document.documentElement.getAttribute('data-theme') || 'light';
  };

  // Create a MutationObserver to watch for data-theme changes
  const themeObserver = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (
        mutation.type === 'attributes' && 
        mutation.attributeName === 'data-theme'
      ) {
        updateTheme();
      }
    });
  });

  // Start observing the document element for data-theme attribute changes
  themeObserver.observe(document.documentElement, { attributes: true });

  return () => themeObserver.disconnect();
});

const scrollToSection = (sectionId: string) => {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
    activeSection.value = sectionId;
  }
};

// Mobile navigation state
const showMobileNav = ref(false);
const isMobile = ref(window.innerWidth < 1024);

// Responsive handling
onMounted(() => {
  const handleResize = () => {
    isMobile.value = window.innerWidth < 1024;
    if (!isMobile.value) showMobileNav.value = false;
  };
  
  window.addEventListener('resize', handleResize);
  return () => window.removeEventListener('resize', handleResize);
});

// Props for API documentation
const props = [
  {
    name: 'variant',
    type: "'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'warning' | 'success'",
    defaultValue: "'primary'",
    description: "The visual style of the button."
  },
  {
    name: 'size',
    type: "'sm' | 'md' | 'lg'",
    defaultValue: "'md'",
    description: "The size of the button."
  },
  {
    name: 'disabled',
    type: 'boolean',
    defaultValue: 'false',
    description: "Whether the button is disabled."
  },
  {
    name: 'loading',
    type: 'boolean',
    defaultValue: 'false',
    description: "Whether the button is in a loading state."
  },
  {
    name: 'aria-label',
    type: 'string',
    defaultValue: 'undefined',
    description: "Accessible label for screen readers (required when button has no text)."
  },
  {
    name: 'type',
    type: "'button' | 'submit' | 'reset'",
    defaultValue: "'button'",
    description: "The type attribute of the button element."
  }
];

// Accessibility guidelines
const accessibilityItems = [
  {
    guideline: "WCAG 2.1 AA Compliant",
    status: true,
    description: "Meets WCAG 2.1 Level AA success criteria"
  },
  {
    guideline: "Keyboard Accessible",
    status: true,
    description: "Can be triggered using Enter or Space keys when focused"
  },
  {
    guideline: "Screen Reader Friendly",
    status: true,
    description: "Provides appropriate role and state information to assistive technologies"
  },
  {
    guideline: "Color Contrast",
    status: true,
    description: "Text has 4.5:1 contrast ratio with background"
  },
  {
    guideline: "Focus Indication",
    status: true,
    description: "Visible focus state that meets 3:1 contrast requirement"
  }
];

// Version history data
const versionHistory = [
  {
    version: "1.3.0",
    date: "2024-03-18",
    changes: [
      "Added danger, warning, and success button variants",
      "Updated button documentation and examples",
      "Enhanced accessibility for status-indicating buttons"
    ]
  },
  {
    version: "1.2.0",
    date: "2023-06-15",
    changes: [
      "Added loading state with spinner animation",
      "Improved focus states for better accessibility",
      "Added support for custom classes"
    ]
  },
  {
    version: "1.1.0",
    date: "2023-04-02",
    changes: [
      "Added outline and ghost variants",
      "Introduced size options (sm, md, lg)"
    ]
  },
  {
    version: "1.0.0",
    date: "2023-02-10",
    changes: [
      "Initial release",
      "Supports primary and secondary variants"
    ]
  }
];

// Related components
const relatedComponents = [
  {
    name: "IconButton",
    description: "Button that displays only an icon with an accessible label",
    path: "/components/icon-button"
  },
  {
    name: "ButtonGroup",
    description: "Set of related buttons grouped together visually",
    path: "/components/button-group"
  },
  {
    name: "Link",
    description: "Navigational element styled as text",
    path: "/components/link"
  }
];

// Computed tokens based on selected variant
const selectedVariant = ref<ButtonVariant>('primary');
const buttonTokens = computed(() => {
  if (!selectedVariant.value) return [];
  return getButtonTokens(selectedVariant.value);
});

// Available variants for the selector
const availableVariants: ButtonVariant[] = ['primary', 'secondary', 'danger', 'warning', 'success'];

// Add size and state options
const sizeOptions = [
  { value: 'sm', label: 'Small' },
  { value: 'md', label: 'Medium' },
  { value: 'lg', label: 'Large' }
];

const stateOptions = [
  { value: 'rest', label: 'Default' },
  { value: 'hover', label: 'Hover' },
  { value: 'press', label: 'Pressed' },
  { value: 'focus', label: 'Focused' },
  { value: 'disabled', label: 'Disabled' }
];

// Add interface for playground configuration
interface PlaygroundConfig {
  size: string;
  state: string;
  type: string;
  showLabel: boolean;
  labelText: string;
  showLeadingIcon: boolean;
  showTrailingIcon: boolean;
  [key: string]: string | boolean; // Add index signature
}

// Update playground configuration with type
const playgroundConfig = ref<PlaygroundConfig>({
  size: 'md',
  state: 'rest',
  type: 'primary',
  showLabel: true,
  labelText: 'Button Label',
  showLeadingIcon: false,
  showTrailingIcon: false
});

const handlePlaygroundUpdate = (key: string, value: any) => {
  playgroundConfig.value[key] = value;
};
</script>

<template>
  <div class="main-container">
    <!-- Navigation Sidebar -->
    <SideNavigation
      :is-mobile-menu-open="showMobileNav"
      @close-mobile-menu="showMobileNav = false"
    />

    <!-- Main Content -->
    <main 
      class="main-content"
      :class="{ 
        'lg:ml-[280px]': !showMobileNav, 
        'lg:ml-[48px]': showMobileNav 
      }"
    >
      <!-- Mobile Navigation Toggle -->
      <button 
        v-if="isMobile"
        class="mobile-nav-toggle"
        @click="showMobileNav = !showMobileNav"
        aria-label="Toggle navigation menu"
      >
        <i class="icon-menu w-6 h-6"></i>
      </button>

      <!-- Content Sections -->
      <div class="content-wrapper max-w-[1440px] mx-auto px-6 pt-20 pb-12">
        <div class="content-container max-w-[1080px] mx-auto">
          <section id="overview" class="mb-10 scroll-mt-16">
            <h1 class="text-3xl font-bold section-heading mb-4">Button</h1>
            <p class="text-lg section-text mb-6">
              Buttons help people take actions, such as sending an email, sharing a document, or liking a comment.
            </p>
            
            <div class="flex flex-wrap gap-2 mb-6">
              <span class="status-badge status-badge-success">
                <span class="w-2 h-2 mr-1 rounded-full bg-green-500"></span> Stable
              </span>
              <span class="status-badge status-badge-info">
                WCAG AA Compliant
              </span>
              <span class="status-badge status-badge-neutral">
                v1.3.0
              </span>
            </div>
            
            <div class="showcase-container p-6 mb-6">
              <div class="flex flex-wrap gap-4">
                <Button variant="primary">Primary</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="danger">Danger</Button>
                <Button variant="warning">Warning</Button>
                <Button variant="success">Success</Button>
              </div>
            </div>
          </section>

          <section id="playground" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Interactive Playground</h2>
            <p class="section-text mb-6">
              Customize the button properties to see different variations and use cases.
            </p>
            
            <!-- Interactive Preview -->
            <div class="showcase-container p-4 lg:p-6">
              <Playground
                title="Button Playground"
                :current-size="playgroundConfig.size"
                :current-state="playgroundConfig.state"
                :current-type="playgroundConfig.type"
                :show-label="playgroundConfig.showLabel"
                :label-text="playgroundConfig.labelText"
                :show-leading-icon="playgroundConfig.showLeadingIcon"
                :show-trailing-icon="playgroundConfig.showTrailingIcon"
                :size-options="sizeOptions"
                :state-options="stateOptions"
                :tokens="buttonTokens"
                :variant="selectedVariant"
                @update:config="handlePlaygroundUpdate"
              />
            </div>
          </section>

          <section id="guidelines" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Design Guidelines</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 mb-8">
              <div>
                <h3 class="text-xl font-semibold mb-4">When to use</h3>
                <ul class="guideline-item">
                  <li>• Use buttons to help users take clear actions</li>
                  <li>• Primary buttons for main actions in a section</li>
                  <li>• Secondary buttons for alternative actions</li>
                  <li>• Ghost buttons for less prominent actions</li>
                </ul>
              </div>
              <div>
                <h3 class="text-xl font-semibold mb-4">When not to use</h3>
                <ul class="guideline-item">
                  <li>• Avoid using too many primary buttons on one page</li>
                  <li>• Don't use buttons for navigation - use links instead</li>
                  <li>• Avoid using ghost buttons for primary actions</li>
                </ul>
              </div>
            </div>

            <!-- Best Practices -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
              <div class="guideline-panel-do">
                <h3 class="font-semibold mb-4">Do</h3>
                <div class="flex gap-4 items-center">
                  <Button variant="primary">Save Changes</Button>
                  <Button variant="secondary">Cancel</Button>
                </div>
                <p class="mt-4 guideline-text">Use clear, concise action verbs that describe what the button does</p>
              </div>
              <div class="guideline-panel-dont">
                <h3 class="font-semibold mb-4">Don't</h3>
                <div class="flex gap-4 items-center">
                  <Button variant="primary">Click Here</Button>
                  <Button variant="secondary">Submit</Button>
                </div>
                <p class="mt-4 guideline-text">Avoid vague labels that don't clearly communicate the action</p>
              </div>
            </div>
          </section>

          <section id="anatomy" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Anatomy</h2>
            <div class="anatomy-container">
              <Button variant="primary" size="lg" class="mx-auto">
                <template #leading-icon>
                  <i class="icon-mail"></i>
                </template>
                Send Message
                <template #trailing-icon>
                  <i class="icon-arrow-right"></i>
                </template>
              </Button>
              
              <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">
                <div>
                  <h4 class="font-semibold mb-2 anatomy-label">1. Container</h4>
                  <p class="anatomy-text">
                    The button's background container that provides visual prominence
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2 anatomy-label">2. Label</h4>
                  <p class="anatomy-text">
                    Text that describes the button's action
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2 anatomy-label">3. Leading Icon (Optional)</h4>
                  <p class="anatomy-text">
                    Icon that appears before the label
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2 anatomy-label">4. Trailing Icon (Optional)</h4>
                  <p class="anatomy-text">
                    Icon that appears after the label
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section id="states" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">States & Variations</h2>
            
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">States</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary">Default</Button>
                  <span class="mt-2 text-sm state-label">Default</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="hover">Hover</Button>
                  <span class="mt-2 text-sm state-label">Hover</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="active">Active</Button>
                  <span class="mt-2 text-sm state-label">Active</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="focus">Focus</Button>
                  <span class="mt-2 text-sm state-label">Focus</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" disabled>Disabled</Button>
                  <span class="mt-2 text-sm state-label">Disabled</span>
                </div>
              </div>
            </div>
            
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Variants</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary">Primary</Button>
                  <span class="mt-2 text-sm state-label">Primary</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="secondary">Secondary</Button>
                  <span class="mt-2 text-sm state-label">Secondary</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="outline">Outline</Button>
                  <span class="mt-2 text-sm state-label">Outline</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="ghost">Ghost</Button>
                  <span class="mt-2 text-sm state-label">Ghost</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="danger">Danger</Button>
                  <span class="mt-2 text-sm state-label">Danger</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="warning">Warning</Button>
                  <span class="mt-2 text-sm state-label">Warning</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="success">Success</Button>
                  <span class="mt-2 text-sm state-label">Success</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-xl font-semibold mb-4">Sizes</h3>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="sm">Small</Button>
                  <span class="mt-2 text-sm state-label">Small</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="md">Medium</Button>
                  <span class="mt-2 text-sm state-label">Medium</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="lg">Large</Button>
                  <span class="mt-2 text-sm state-label">Large</span>
                </div>
              </div>
            </div>
          </section>

          <section id="accessibility" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Accessibility</h2>
            
            <p class="section-text mb-6">
              Buttons are designed to be accessible to all users, including those using assistive technologies.
            </p>
            
            <AccessibilityChecklist :items="accessibilityItems" />
            
            <div class="mt-6 space-y-4">
              <div>
                <h3 class="text-xl font-semibold mb-2">Keyboard Support</h3>
                <ul class="accessibility-list">
                  <li>Focusable with <kbd>Tab</kbd> key</li>
                  <li>Activate with <kbd>Enter</kbd> or <kbd>Space</kbd> key</li>
                </ul>
              </div>
              
              <div>
                <h3 class="text-xl font-semibold mb-2">Screen Reader Considerations</h3>
                <ul class="accessibility-list">
                  <li>Use <code>aria-label</code> for buttons with icons only</li>
                  <li>Use appropriate semantic HTML (<code>&lt;button&gt;</code> element)</li>
                  <li>Dynamically update <code>aria-disabled</code> to match disabled state</li>
                </ul>
              </div>
            </div>
          </section>

          <section id="examples" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Examples</h2>
            
            <!-- Basic Example -->
            <ComponentShowcase
              title="Basic Button Examples"
              componentName="Button"
              class="component-showcase"
            >
              <template #preview>
                <div class="flex gap-4">
                  <Button>Default Button</Button>
                  <Button variant="primary">Primary</Button>
                  <Button variant="secondary">Secondary</Button>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button&gt;Default Button&lt;/Button&gt;
&lt;Button variant="primary"&gt;Primary&lt;/Button&gt;
&lt;Button variant="secondary"&gt;Secondary&lt;/Button&gt;
              </template>
            </ComponentShowcase>
            
            <!-- Size Variations -->
            <ComponentShowcase
              title="Button Sizes"
              componentName="Button"
              class="mt-6 component-showcase"
            >
              <template #preview>
                <div class="flex items-center gap-4">
                  <Button variant="primary" size="sm">Small</Button>
                  <Button variant="primary" size="md">Medium</Button>
                  <Button variant="primary" size="lg">Large</Button>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button variant="primary" size="sm"&gt;Small&lt;/Button&gt;
&lt;Button variant="primary" size="md"&gt;Medium&lt;/Button&gt;
&lt;Button variant="primary" size="lg"&gt;Large&lt;/Button&gt;
              </template>
            </ComponentShowcase>
            
            <!-- Variant Showcase -->
            <ComponentShowcase
              title="Button Variants"
              componentName="Button"
              class="mt-6 component-showcase"
            >
              <template #preview>
                <div class="grid grid-cols-1 gap-4">
                  <div v-if="!isDarkTheme" class="space-y-3">
                    <h4 class="font-medium text-sm section-subheading">Light Theme</h4>
                    <div class="theme-preview-light flex flex-wrap gap-3 p-4 rounded">
                      <Button variant="primary">Primary</Button>
                      <Button variant="secondary">Secondary</Button>
                      <Button variant="outline">Outline</Button>
                      <Button variant="ghost">Ghost</Button>
                    </div>
                  </div>
                  <div v-if="isDarkTheme" class="space-y-3">
                    <h4 class="font-medium text-sm section-subheading">Dark Theme</h4>
                    <div class="theme-preview-dark flex flex-wrap gap-3 p-4 rounded">
                      <Button variant="primary">Primary</Button>
                      <Button variant="secondary">Secondary</Button>
                      <Button variant="outline">Outline</Button>
                      <Button variant="ghost">Ghost</Button>
                    </div>
                  </div>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button variant="primary"&gt;Primary&lt;/Button&gt;
&lt;Button variant="secondary"&gt;Secondary&lt;/Button&gt;
&lt;Button variant="outline"&gt;Outline&lt;/Button&gt;
&lt;Button variant="ghost"&gt;Ghost&lt;/Button&gt;
              </template>
            </ComponentShowcase>
            
            <!-- Icon Button Example -->
            <ComponentShowcase
              title="Button with Icons"
              componentName="Button"
              class="mt-6 component-showcase"
            >
              <template #preview>
                <div class="flex gap-4">
                  <Button variant="primary">
                    <template #leading-icon>
                      <span class="material-symbols-rounded">add</span>
                    </template>
                    Add Item
                  </Button>
                  <Button variant="outline">
                    Share
                    <template #trailing-icon>
                      <span class="material-symbols-rounded">share</span>
                    </template>
                  </Button>
                  <Button variant="secondary" size="sm">
                    <template #leading-icon>
                      <span class="material-symbols-rounded">cloud_download</span>
                    </template>
                    Download
                  </Button>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button variant="primary"&gt;
  &lt;template #leading-icon&gt;
    &lt;span class="material-symbols-rounded"&gt;add&lt;/span&gt;
  &lt;/template&gt;
  Add Item
&lt;/Button&gt;

&lt;Button variant="outline"&gt;
  Share
  &lt;template #trailing-icon&gt;
    &lt;span class="material-symbols-rounded"&gt;share&lt;/span&gt;
  &lt;/template&gt;
&lt;/Button&gt;

&lt;Button variant="secondary" size="sm"&gt;
  &lt;template #leading-icon&gt;
    &lt;span class="material-symbols-rounded"&gt;cloud_download&lt;/span&gt;
  &lt;/template&gt;
  Download
&lt;/Button&gt;
              </template>
            </ComponentShowcase>
            
            <!-- Icon Component Example -->
            <ComponentShowcase
              title="Using the Icon Component"
              componentName="Icon"
              class="mt-6 component-showcase"
            >
              <template #preview>
                <div class="flex gap-4">
                  <Button variant="primary">
                    <template #leading-icon>
                      <Icon name="favorite" filled color="inherit" />
                    </template>
                    Favorite
                  </Button>
                  <Button variant="secondary">
                    Settings
                    <template #trailing-icon>
                      <Icon name="settings" size="md" />
                    </template>
                  </Button>
                  <Button variant="outline">
                    <template #leading-icon>
                      <Icon name="notifications" :weight="500" color="brand" />
                    </template>
                    Notifications
                  </Button>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';
import Icon from '@/components/ui/Icon.vue';

&lt;Button variant="primary"&gt;
  &lt;template #leading-icon&gt;
    &lt;Icon name="favorite" filled color="inherit" /&gt;
  &lt;/template&gt;
  Favorite
&lt;/Button&gt;

&lt;Button variant="secondary"&gt;
  Settings
  &lt;template #trailing-icon&gt;
    &lt;Icon name="settings" size="md" /&gt;
  &lt;/template&gt;
&lt;/Button&gt;

&lt;Button variant="outline"&gt;
  &lt;template #leading-icon&gt;
    &lt;Icon name="notifications" :weight="500" color="brand" /&gt;
  &lt;/template&gt;
  Notifications
&lt;/Button&gt;
              </template>
            </ComponentShowcase>
            
            <!-- State Examples -->
            <ComponentShowcase
              title="Button States"
              componentName="Button"
              class="mt-6 component-showcase"
            >
              <template #preview>
                <div class="space-y-4">
                  <div class="flex flex-wrap gap-4">
                    <Button variant="primary" loading>Loading</Button>
                    <Button variant="secondary" loading>Loading</Button>
                    <Button variant="outline" loading>Loading</Button>
                  </div>
                  <div class="flex flex-wrap gap-4">
                    <Button variant="primary" disabled>Disabled</Button>
                    <Button variant="secondary" disabled>Disabled</Button>
                    <Button variant="outline" disabled>Disabled</Button>
                  </div>
                </div>
              </template>
              <template #code>
import Button from '@/components/ui/Button.vue';

// Loading States
&lt;Button variant="primary" loading&gt;Loading&lt;/Button&gt;
&lt;Button variant="secondary" loading&gt;Loading&lt;/Button&gt;
&lt;Button variant="outline" loading&gt;Loading&lt;/Button&gt;
&lt;Button variant="danger" loading&gt;Loading&lt;/Button&gt;
&lt;Button variant="warning" loading&gt;Loading&lt;/Button&gt;
&lt;Button variant="success" loading&gt;Loading&lt;/Button&gt;

// Disabled States
&lt;Button variant="primary" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="secondary" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="outline" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="danger" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="warning" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="success" disabled&gt;Disabled&lt;/Button&gt;
              </template>
            </ComponentShowcase>
          </section>

          <section id="related" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Related Components</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <a 
                v-for="component in relatedComponents" 
                :key="component.name"
                :href="component.path"
                class="related-component-card"
              >
                <h3 class="text-lg font-semibold mb-2">{{ component.name }}</h3>
                <p class="text-sm section-text">{{ component.description }}</p>
              </a>
            </div>
          </section>

          <section id="version" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold section-heading mb-4">Version History</h2>
            
            <div class="version-history">
              <div v-for="(version, index) in versionHistory" :key="index" class="version-item">
                <div class="flex justify-between items-center mb-2">
                  <h3 class="text-lg font-semibold version-title">{{ version.version }}</h3>
                  <span class="text-sm version-date">{{ version.date }}</span>
                </div>
                <ul class="space-y-1">
                  <li v-for="(change, changeIndex) in version.changes" :key="changeIndex" class="version-change">
                    • {{ change }}
                  </li>
                </ul>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>

    <!-- Right Sidebar -->
    <aside class="right-sidebar">
      <nav class="p-5">
        <h3 class="text-sm font-semibold sidebar-heading uppercase tracking-wider mb-4">
          On This Page
        </h3>
        <ul class="space-y-2">
          <li v-for="section in sections" :key="section.id">
            <a 
              :href="`#${section.id}`"
              @click="scrollToSection(section.id)"
              class="sidebar-link"
              :class="[
                activeSection === section.id 
                  ? 'sidebar-link-active'
                  : 'sidebar-link-inactive'
              ]"
            >
              {{ section.label }}
            </a>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Mobile Navigation Overlay -->
    <div 
      v-if="showMobileNav"
      class="mobile-nav-overlay"
      @click="showMobileNav = false"
    >
      <div 
        class="mobile-nav-panel"
        :class="showMobileNav ? 'translate-x-0' : '-translate-x-full'"
        @click.stop
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold mobile-panel-heading">Navigation</h2>
          <button 
            class="mobile-close-btn"
            @click="showMobileNav = false"
            aria-label="Close navigation menu"
          >
            <i class="icon-x w-5 h-5"></i>
          </button>
        </div>
        <ul class="space-y-2">
          <li v-for="section in sections" :key="section.id">
            <a 
              :href="`#${section.id}`"
              @click="scrollToSection(section.id); showMobileNav = false"
              class="mobile-nav-link"
              :class="[
                activeSection === section.id 
                  ? 'mobile-nav-link-active'
                  : 'mobile-nav-link-inactive'
              ]"
            >
              {{ section.label }}
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Base styles */
:deep(*) {
  scroll-behavior: smooth;
}

/* Container styles */
.main-container {
  @apply flex h-screen w-full overflow-hidden fixed inset-0;
  background-color: var(--color-surface-primary-rest);
}

/* Main content styles */
.main-content {
  @apply flex-1 h-screen overflow-y-auto transition-all duration-300;
  background-color: var(--color-surface-primary-rest);
  margin-right: 280px; /* Right sidebar margin */
}

/* Section text styles */
.section-heading {
  color: var(--color-text-primary-rest);
}

.section-subheading {
  color: var(--color-text-secondary-rest);
}

.section-text {
  color: var(--color-text-secondary-rest);
}

/* Component preview area */
.preview-area {
  @apply flex-1 rounded-lg p-8 flex items-center justify-center;
  background-color: var(--color-surface-secondary-rest);
}

/* Table and divide styling */
.table-divide {
  @apply min-w-full divide-y;
  border-color: var(--color-border-primary-rest);
}

.table-divide tr {
  border-color: var(--color-border-primary-rest);
}

/* API Reference section */
.api-reference-container {
  @apply rounded-xl p-4;
  background-color: var(--color-surface-secondary-rest);
}

/* Event handlers section */
.event-handlers-container {
  @apply rounded-xl p-4;
  background-color: var(--color-surface-secondary-rest);
}

.event-row {
  border-color: var(--color-border-primary-rest);
}

/* Design guidelines do/don't panels */
.guideline-item {
  @apply space-y-3;
  color: var(--color-text-secondary-rest);
}

.guideline-panel-do {
  @apply p-6 rounded-lg;
  background-color: var(--color-surface-success-muted);
}

.guideline-panel-do h3 {
  color: var(--color-text-success-rest);
}

.guideline-panel-dont {
  @apply p-6 rounded-lg;
  background-color: var(--color-surface-error-muted);
}

.guideline-panel-dont h3 {
  color: var(--color-text-error-rest);
}

.guideline-text {
  color: var(--color-text-secondary-rest);
}

/* Anatomy section */
.anatomy-container {
  @apply relative p-4 lg:p-6 rounded-xl;
  border: 1px solid var(--color-border-primary-rest);
}

.anatomy-label {
  color: var(--color-text-primary-rest);
}

.anatomy-text {
  color: var(--color-text-secondary-rest);
}

/* States section */
.state-label {
  color: var(--color-text-secondary-rest);
}

/* Accessibility section */
.accessibility-container {
  @apply rounded-xl p-4 lg:p-6;
  background-color: var(--color-surface-secondary-rest);
}

.accessibility-list {
  @apply list-disc pl-5;
  color: var(--color-text-secondary-rest);
}

/* Examples section */
.example-header {
  @apply px-6 py-4 border-b;
  border-color: var(--color-border-primary-rest);
}

.example-title {
  @apply text-xl font-semibold;
  color: var(--color-text-primary-rest);
}

.example-container {
  background-color: var(--color-surface-primary-rest);
  border: 1px solid var(--color-border-primary-rest);
  border-radius: 0.5rem;
  overflow: hidden;
}

.example-description {
  color: var(--color-text-secondary-rest);
}

.example-preview {
  padding: 1.5rem;
  background-color: var(--color-surface-secondary-rest);
}

.example-tab {
  @apply px-4 py-3 text-sm font-medium border-b-2 focus:outline-none;
  color: var(--color-text-secondary-rest);
  border-color: transparent;
}

.example-tab:hover {
  color: var(--color-text-secondary-hover);
  border-color: var(--color-border-secondary-hover);
}

.example-tab-active {
  color: var(--color-text-brand-rest);
  border-color: var(--color-border-brand-rest);
}

.example-code {
  @apply p-4 rounded-md overflow-x-auto text-sm;
  background-color: var(--color-surface-code-rest);
  color: var(--color-text-code-rest);
}

.example-tabs-border {
  border-color: var(--color-border-primary-rest);
}

/* Related components */
.related-component-card {
  @apply block p-5 rounded-xl border transition-all duration-200;
  background-color: var(--color-surface-secondary-rest);
  border-color: var(--color-border-primary-rest);
}

.related-component-card:hover {
  @apply shadow-md;
  border-color: var(--color-border-brand-hover);
  background-color: var(--color-surface-brand-muted);
}

/* Version history */
.version-item {
  @apply border-b pb-4 mb-4;
  border-color: var(--color-border-primary-rest);
}

.version-title {
  color: var(--color-text-primary-rest);
}

.version-date {
  color: var(--color-text-secondary-rest);
}

.version-change {
  color: var(--color-text-secondary-rest);
}

/* Status badges */
.status-badge {
  @apply inline-flex items-center px-3 py-1 rounded-full text-xs font-medium;
}

.status-badge-success {
  background-color: var(--color-surface-success-rest);
  color: var(--color-text-success-rest);
}

.status-badge-info {
  background-color: var(--color-surface-info-rest);
  color: var(--color-text-info-rest);
}

.status-badge-neutral {
  background-color: var(--color-surface-neutral-rest);
  color: var(--color-text-neutral-rest);
}

/* Showcase containers */
.showcase-container {
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.75rem;
}

/* Theme preview containers */
.theme-preview-light {
  background-color: var(--color-surface-light-rest);
}

.theme-preview-dark {
  background-color: var(--color-surface-dark-rest);
}

/* Right sidebar styles */
.right-sidebar {
  @apply fixed top-16 right-0 z-40 w-[280px] h-[calc(100vh-4rem)] overflow-y-auto;
  background-color: var(--color-surface-primary-rest);
  border-left: 1px solid var(--color-border-primary-rest);
}

.sidebar-heading {
  color: var(--color-text-secondary-rest);
}

.sidebar-link {
  @apply block py-2 px-3 rounded-lg transition-colors duration-200;
}

.sidebar-link-active {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

.sidebar-link-inactive {
  color: var(--color-text-secondary-rest);
}

.sidebar-link-inactive:hover {
  background-color: var(--color-surface-secondary-hover);
  color: var(--color-text-secondary-hover);
}

/* Mobile navigation toggle button */
.mobile-nav-toggle {
  @apply fixed top-4 left-4 z-50 p-2 rounded-lg shadow-lg;
  background-color: var(--color-surface-primary-rest);
}

/* Mobile navigation overlay */
.mobile-nav-overlay {
  @apply fixed inset-0 z-40;
  background-color: var(--color-overlay-rest);
  backdrop-filter: blur(4px);
}

/* Mobile navigation panel */
.mobile-nav-panel {
  @apply w-64 h-full p-6 shadow-xl transform transition-transform;
  background-color: var(--color-surface-primary-rest);
}

.mobile-panel-heading {
  color: var(--color-text-primary-rest);
}

.mobile-close-btn {
  @apply p-2 rounded-lg;
  color: var(--color-icon-secondary-rest);
  background-color: transparent;
}

.mobile-close-btn:hover {
  background-color: var(--color-surface-secondary-hover);
  color: var(--color-icon-secondary-hover);
}

.mobile-nav-link {
  @apply block py-2 px-4 rounded-lg transition-colors duration-200;
}

.mobile-nav-link-active {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

.mobile-nav-link-inactive {
  color: var(--color-text-secondary-rest);
}

.mobile-nav-link-inactive:hover {
  background-color: var(--color-surface-secondary-hover);
  color: var(--color-text-secondary-hover);
}

/* Navigation link styles - remove as handled by individual link styles */
:deep(.nav-link) {
  @apply block py-2 px-3 rounded-lg transition-colors duration-200;
}

:deep(.nav-link-active) {
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
}

:deep(.nav-link-inactive) {
  color: var(--color-text-secondary-rest);
}

/* Content layout */
.content-container {
  @apply w-full;
}

/* Section spacing and scroll behavior */
section {
  scroll-margin-top: 4rem;
  transition: margin 0.3s ease-in-out;
}

/* Responsive layout adjustments */
@media (max-width: 1024px) {
  .main-content {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  section {
    scroll-margin-top: 2rem;
  }

  .content-wrapper {
    @apply px-4;
  }
}

@media (max-width: 768px) {
  .grid-container {
    @apply gap-4;
  }

  section {
    @apply mb-8;
  }

  .content-wrapper {
    @apply px-3;
  }
}

/* Dark mode transitions */
:deep(.dark-mode-transition) {
  transition: background-color 0.3s ease-in-out, 
             color 0.3s ease-in-out,
             border-color 0.3s ease-in-out;
}

/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--color-scrollbar-thumb-rest);
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-scrollbar-thumb-hover);
}

/* Smooth transitions for interactive elements */
button, a {
  transition: all 0.2s ease-in-out;
}

/* Button state simulation classes */
.hover {
  @apply opacity-90;
}

.active {
  @apply opacity-80;
}

.focus {
  @apply ring-2;
  ring-color: var(--color-border-brand-focus);
  ring-offset-color: var(--color-surface-primary-rest);
}

/* ResizableSidebar overrides */
:deep(.resizable-sidebar) {
  background-color: var(--color-surface-primary-rest);
  transition: transform 0.3s ease-in-out;
  z-index: 30; /* Lower than the anchor navigation */
}

:deep(.resizable-sidebar.collapsed) {
  @apply transform -translate-x-full;
}

:deep(.resize-handle) {
  @apply opacity-0 hover:opacity-100 transition-opacity duration-200;
}

/* For ComponentShowcase */
:deep(.component-showcase) {
  background-color: var(--color-surface-primary-rest) !important;
  border-color: var(--color-border-primary-rest) !important;
}

:deep(.component-showcase-header) {
  border-color: var(--color-border-primary-rest) !important;
}

:deep(.component-showcase-title) {
  color: var(--color-text-primary-rest) !important;
}

:deep(.component-showcase-description) {
  color: var(--color-text-secondary-rest) !important;
}

:deep(.component-showcase-tab) {
  color: var(--color-text-secondary-rest) !important;
}

:deep(.component-showcase-tab-active) {
  color: var(--color-text-brand-rest) !important;
  border-color: var(--color-border-brand-rest) !important;
}

:deep(.component-showcase-tab-border) {
  border-color: var(--color-border-primary-rest) !important;
}

:deep(.component-showcase-code) {
  background-color: var(--color-surface-code-rest) !important;
  color: var(--color-text-code-rest) !important;
}

:deep(.component-showcase-preview) {
  background-color: var(--color-surface-secondary-rest) !important;
}

:deep(.component-showcase-props-header) {
  color: var(--color-text-secondary-rest) !important;
}

:deep(.component-showcase-props-row) {
  border-color: var(--color-border-primary-rest) !important;
}

:deep(.component-showcase-props-body) {
  background-color: var(--color-surface-primary-rest) !important;
}

.token-selector {
  background-color: var(--color-surface-secondary-rest);
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-v-padding-m) var(--comp-button-main-h-padding-m);
  border: 1px solid var(--color-border-primary-rest);
}

.token-selector-label {
  color: var(--color-text-secondary-rest);
  font-weight: var(--font-weight-medium-500);
}

.variant-selector-btn {
  padding: var(--comp-button-main-v-padding-s) var(--comp-button-main-h-padding-s);
  border-radius: var(--comp-button-main-radius);
  font-size: var(--font-size-14);
  font-weight: var(--font-weight-medium-500);
  transition: all 0.2s ease-in-out;
  border: 1px solid transparent;
  min-width: 80px;
  text-align: center;
}

.variant-selector-btn:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-border-brand-focus);
}

.variant-selector-btn:disabled {
  opacity: var(--comp-button-main-disabled-opacity);
  cursor: not-allowed;
}

.variant-selector-btn--selected {
  background-color: var(--color-fill-brand-rest);
  color: var(--color-text-primary-inverse);
  border-color: var(--color-border-brand-rest);
}

.variant-selector-btn--selected:hover:not(:disabled) {
  background-color: var(--color-fill-brand-hover);
  border-color: var(--color-border-brand-hover);
}

.variant-selector-btn--selected:active:not(:disabled) {
  background-color: var(--color-fill-brand-press);
  border-color: var(--color-border-brand-press);
}

.variant-selector-btn--unselected {
  background-color: var(--color-surface-primary-rest);
  color: var(--color-text-secondary-rest);
  border-color: var(--color-border-primary-rest);
}

.variant-selector-btn--unselected:hover:not(:disabled) {
  background-color: var(--color-surface-primary-hover);
  color: var(--color-text-primary-rest);
  border-color: var(--color-border-primary-hover);
}

.variant-selector-btn--unselected:active:not(:disabled) {
  background-color: var(--color-surface-primary-press);
  color: var(--color-text-primary-press);
  border-color: var(--color-border-primary-press);
}
</style> 