<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from '../components/ui/Button.vue';
import ButtonPreview from '../components/showcase/ButtonPreview.vue';
import ComponentShowcase from '../components/showcase/ComponentShowcase.vue';
import PropRow from '../components/showcase/PropRow.vue';
import TokenTable from '../components/showcase/TokenTable.vue';
import SideNavigation from '../components/layout/SideNavigation.vue';
import AccessibilityChecklist from '../components/showcase/AccessibilityChecklist.vue';
import VersionHistory from '../components/showcase/VersionHistory.vue';
import RelatedComponentCard from '../components/showcase/RelatedComponentCard.vue';
import Icon from '../components/ui/Icon.vue';

// Active section tracking
const activeSection = ref('overview');
const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'playground', label: 'Playground' },
  { id: 'guidelines', label: 'Guidelines' },
  { id: 'anatomy', label: 'Anatomy' },
  { id: 'states', label: 'States & Variations' },
  { id: 'accessibility', label: 'Accessibility' },
  { id: 'implementation', label: 'Implementation' },
  { id: 'examples', label: 'Examples' },
  { id: 'related', label: 'Related Components' },
  { id: 'version', label: 'Version History' }
];

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
    type: "'primary' | 'secondary' | 'outline' | 'ghost'",
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
</script>

<template>
  <div class="flex h-screen w-full overflow-hidden fixed inset-0 bg-white dark:bg-gray-900">
    <!-- Navigation Sidebar -->
    <SideNavigation
      :is-mobile-menu-open="showMobileNav"
      @close-mobile-menu="showMobileNav = false"
    />

    <!-- Main Content -->
    <main 
      class="main-content flex-1 h-screen overflow-y-auto bg-white dark:bg-gray-900 transition-all duration-300"
      :class="{ 
        'lg:ml-[280px]': !showMobileNav, 
        'lg:ml-[48px]': showMobileNav 
      }"
    >
      <!-- Mobile Navigation Toggle -->
      <button 
        v-if="isMobile"
        class="fixed top-4 left-4 z-50 p-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg"
        @click="showMobileNav = !showMobileNav"
        aria-label="Toggle navigation menu"
      >
        <i class="icon-menu w-6 h-6"></i>
      </button>

      <!-- Content Sections -->
      <div class="content-wrapper max-w-[1440px] mx-auto px-6 pt-20 pb-12">
        <div class="content-container max-w-[1080px] mx-auto">
          <section id="overview" class="mb-10 scroll-mt-16">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Button</h1>
            <p class="text-lg text-gray-600 dark:text-gray-400 mb-6">
              Buttons help people take actions, such as sending an email, sharing a document, or liking a comment.
            </p>
            
            <div class="flex flex-wrap gap-2 mb-6">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400">
                <span class="w-2 h-2 mr-1 rounded-full bg-green-500"></span> Stable
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400">
                WCAG AA Compliant
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300">
                v1.2.0
              </span>
            </div>
            
            <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6 mb-6">
              <div class="flex flex-wrap gap-4">
                <Button variant="primary">Primary</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
              </div>
            </div>
          </section>

          <section id="playground" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Interactive Playground</h2>
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Customize the button properties to see different variations and use cases.
            </p>
            
            <!-- Interactive Preview -->
            <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4 lg:p-6">
              <ButtonPreview />
            </div>
          </section>

          <section id="guidelines" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Design Guidelines</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 mb-8">
              <div>
                <h3 class="text-xl font-semibold mb-4">When to use</h3>
                <ul class="space-y-3 text-gray-600 dark:text-gray-400">
                  <li>• Use buttons to help users take clear actions</li>
                  <li>• Primary buttons for main actions in a section</li>
                  <li>• Secondary buttons for alternative actions</li>
                  <li>• Ghost buttons for less prominent actions</li>
                </ul>
              </div>
              <div>
                <h3 class="text-xl font-semibold mb-4">When not to use</h3>
                <ul class="space-y-3 text-gray-600 dark:text-gray-400">
                  <li>• Avoid using too many primary buttons on one page</li>
                  <li>• Don't use buttons for navigation - use links instead</li>
                  <li>• Avoid using ghost buttons for primary actions</li>
                </ul>
              </div>
            </div>

            <!-- Best Practices -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
              <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg">
                <h3 class="text-green-700 dark:text-green-400 font-semibold mb-4">Do</h3>
                <div class="flex gap-4 items-center">
                  <Button variant="primary">Save Changes</Button>
                  <Button variant="secondary">Cancel</Button>
                </div>
                <p class="mt-4 text-gray-700 dark:text-gray-300">Use clear, concise action verbs that describe what the button does</p>
              </div>
              <div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg">
                <h3 class="text-red-700 dark:text-red-400 font-semibold mb-4">Don't</h3>
                <div class="flex gap-4 items-center">
                  <Button variant="primary">Click Here</Button>
                  <Button variant="secondary">Submit</Button>
                </div>
                <p class="mt-4 text-gray-700 dark:text-gray-300">Avoid vague labels that don't clearly communicate the action</p>
              </div>
            </div>
          </section>

          <section id="anatomy" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Anatomy</h2>
            <div class="relative p-4 lg:p-6 border border-gray-200 dark:border-gray-700 rounded-xl">
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
                  <h4 class="font-semibold mb-2">1. Container</h4>
                  <p class="text-gray-600 dark:text-gray-400">
                    The button's background container that provides visual prominence
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2">2. Label</h4>
                  <p class="text-gray-600 dark:text-gray-400">
                    Text that describes the button's action
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2">3. Leading Icon (Optional)</h4>
                  <p class="text-gray-600 dark:text-gray-400">
                    Icon that appears before the label
                  </p>
                </div>
                <div>
                  <h4 class="font-semibold mb-2">4. Trailing Icon (Optional)</h4>
                  <p class="text-gray-600 dark:text-gray-400">
                    Icon that appears after the label
                  </p>
                </div>
              </div>
            </div>
          </section>

          <section id="states" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">States & Variations</h2>
            
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">States</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary">Default</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Default</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="hover">Hover</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Hover</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="active">Active</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Active</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" class="focus">Focus</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Focus</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" disabled>Disabled</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Disabled</span>
                </div>
              </div>
            </div>
            
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Variants</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary">Primary</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Primary</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="secondary">Secondary</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Secondary</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="outline">Outline</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Outline</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="ghost">Ghost</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Ghost</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-xl font-semibold mb-4">Sizes</h3>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="sm">Small</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Small</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="md">Medium</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Medium</span>
                </div>
                <div class="flex flex-col items-center">
                  <Button variant="primary" size="lg">Large</Button>
                  <span class="mt-2 text-sm text-gray-600 dark:text-gray-400">Large</span>
                </div>
              </div>
            </div>
          </section>

          <section id="accessibility" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Accessibility</h2>
            
            <p class="text-gray-600 dark:text-gray-400 mb-6">
              Buttons are designed to be accessible to all users, including those using assistive technologies.
            </p>
            
            <AccessibilityChecklist :items="accessibilityItems" />
            
            <div class="mt-6 space-y-4">
              <div>
                <h3 class="text-xl font-semibold mb-2">Keyboard Support</h3>
                <ul class="list-disc pl-5 text-gray-600 dark:text-gray-400">
                  <li>Focusable with <kbd>Tab</kbd> key</li>
                  <li>Activate with <kbd>Enter</kbd> or <kbd>Space</kbd> key</li>
                </ul>
              </div>
              
              <div>
                <h3 class="text-xl font-semibold mb-2">Screen Reader Considerations</h3>
                <ul class="list-disc pl-5 text-gray-600 dark:text-gray-400">
                  <li>Use <code>aria-label</code> for buttons with icons only</li>
                  <li>Use appropriate semantic HTML (<code>&lt;button&gt;</code> element)</li>
                  <li>Dynamically update <code>aria-disabled</code> to match disabled state</li>
                </ul>
              </div>
            </div>
          </section>

          <section id="implementation" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Implementation</h2>
            
            <!-- Design Tokens -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Design Tokens</h3>
              <TokenTable
                :tokens="[
                  { name: '--comp-button-main-radius', value: '8px', usage: 'Button corner radius' },
                  { name: '--comp-button-main-gap', value: '8px', usage: 'Gap between elements in button' },
                  { name: '--comp-button-main-text-weight', value: '500', usage: 'Button text font weight' },
                  { name: '--comp-button-main-transition', value: '0.2s ease', usage: 'Transition timing for state changes' },
                  { name: '--comp-button-main-height-s', value: '32px', usage: 'Height for small buttons' },
                  { name: '--comp-button-main-height-m', value: '40px', usage: 'Height for medium buttons' },
                  { name: '--comp-button-main-height-l', value: '48px', usage: 'Height for large buttons' },
                  { name: '--comp-button-main-fill-rest-pri', value: 'var(--color-fill-brand-rest)', usage: 'Primary button background' },
                  { name: '--comp-button-main-text-color-fill-pri', value: 'var(--color-text-neutrallight-rest)', usage: 'Primary button text color' },
                  { name: '--comp-button-main-focus-width', value: '3px', usage: 'Width of focus outline' },
                  { name: '--comp-button-main-focus-offset', value: '2px', usage: 'Offset for focus outline' },
                  { name: '--comp-button-main-disabled-opacity', value: '0.5', usage: 'Opacity for disabled buttons' }
                ]"
              />
            </div>
            
            <!-- API Reference -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">API Reference</h3>
              <PropRow
                v-for="prop in props"
                :key="prop.name"
                v-bind="prop"
              />
            </div>
            
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Event Handlers</h3>
              <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4">
                <table class="w-full">
                  <thead>
                    <tr class="border-b border-gray-200 dark:border-gray-700">
                      <th class="text-left p-2">Event</th>
                      <th class="text-left p-2">Description</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr class="border-b border-gray-200 dark:border-gray-700">
                      <td class="p-2 font-mono text-sm">@click</td>
                      <td class="p-2">Triggered when button is clicked</td>
                    </tr>
                    <tr class="border-b border-gray-200 dark:border-gray-700">
                      <td class="p-2 font-mono text-sm">@focus</td>
                      <td class="p-2">Triggered when button receives focus</td>
                    </tr>
                    <tr>
                      <td class="p-2 font-mono text-sm">@blur</td>
                      <td class="p-2">Triggered when button loses focus</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>

          <section id="examples" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Examples</h2>
            
            <!-- Basic Example -->
            <ComponentShowcase
              title="Basic Button Examples"
              componentName="Button"
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
              class="mt-6"
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
              class="mt-6"
            >
              <template #preview>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="space-y-3">
                    <h4 class="font-medium text-sm text-gray-600">Light Background</h4>
                    <div class="flex flex-wrap gap-3 p-4 bg-white rounded">
                      <Button variant="primary">Primary</Button>
                      <Button variant="secondary">Secondary</Button>
                      <Button variant="outline">Outline</Button>
                      <Button variant="ghost">Ghost</Button>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <h4 class="font-medium text-sm text-gray-600">Dark Background</h4>
                    <div class="flex flex-wrap gap-3 p-4 bg-gray-900 rounded">
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
              class="mt-6"
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
              class="mt-6"
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
              class="mt-6"
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

// Disabled States
&lt;Button variant="primary" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="secondary" disabled&gt;Disabled&lt;/Button&gt;
&lt;Button variant="outline" disabled&gt;Disabled&lt;/Button&gt;
              </template>
            </ComponentShowcase>
          </section>

          <section id="related" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Related Components</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <RelatedComponentCard 
                v-for="component in relatedComponents" 
                :key="component.name"
                :name="component.name"
                :description="component.description"
                :path="component.path"
              />
            </div>
          </section>

          <section id="version" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Version History</h2>
            
            <VersionHistory :versions="versionHistory" />
          </section>
        </div>
      </div>
    </main>

    <!-- Right Sidebar -->
    <aside class="fixed top-16 right-0 z-40 w-[280px] h-[calc(100vh-4rem)] overflow-y-auto border-l border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
      <nav class="p-5">
        <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider dark:text-gray-400 mb-4">
          On This Page
        </h3>
        <ul class="space-y-2">
          <li v-for="section in sections" :key="section.id">
            <a 
              :href="`#${section.id}`"
              @click="scrollToSection(section.id)"
              class="block py-2 px-3 rounded-lg transition-colors duration-200"
              :class="[
                activeSection === section.id 
                  ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
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
      class="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-40"
      @click="showMobileNav = false"
    >
      <div 
        class="w-64 h-full bg-white dark:bg-gray-900 p-6 shadow-xl transform transition-transform"
        :class="showMobileNav ? 'translate-x-0' : '-translate-x-full'"
        @click.stop
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold">Navigation</h2>
          <button 
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800"
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
              class="block py-2 px-4 rounded-lg transition-colors duration-200"
              :class="[
                activeSection === section.id 
                  ? 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400'
                  : 'hover:bg-gray-100 dark:hover:bg-gray-800'
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

/* Navigation link styles */
:deep(.nav-link) {
  @apply block py-2 px-3 rounded-lg transition-colors duration-200;
}

:deep(.nav-link-active) {
  @apply bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-400;
}

:deep(.nav-link-inactive) {
  @apply text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800;
}

/* Content layout */
.main-content {
  @apply relative;
  margin-right: 280px; /* Right sidebar margin */
}

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
  background: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.7);
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
  @apply ring-2 ring-blue-500 ring-offset-2 dark:ring-offset-gray-900;
}

/* ResizableSidebar overrides */
:deep(.resizable-sidebar) {
  @apply bg-white dark:bg-gray-900;
  transition: transform 0.3s ease-in-out;
  z-index: 30; /* Lower than the anchor navigation */
}

:deep(.resizable-sidebar.collapsed) {
  @apply transform -translate-x-full;
}

:deep(.resize-handle) {
  @apply opacity-0 hover:opacity-100 transition-opacity duration-200;
}
</style> 