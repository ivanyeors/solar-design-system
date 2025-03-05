<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from '../components/ui/Button.vue';
import ButtonPreview from '../components/showcase/ButtonPreview.vue';
import ComponentShowcase from '../components/showcase/ComponentShowcase.vue';
import PropRow from '../components/showcase/PropRow.vue';
import TokenTable from '../components/showcase/TokenTable.vue';
import SideNavigation from '../components/layout/SideNavigation.vue';

// Active section tracking
const activeSection = ref('overview');
const sections = [
  { id: 'overview', label: 'Overview' },
  { id: 'usage', label: 'Usage' },
  { id: 'specs', label: 'Specifications' },
  { id: 'anatomy', label: 'Anatomy' },
  { id: 'behaviors', label: 'Behaviors' },
  { id: 'development', label: 'Development' }
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
      >
        <i class="icon-menu w-6 h-6"></i>
      </button>

      <!-- Content Sections -->
      <div class="content-wrapper max-w-[1440px] mx-auto px-6 py-12">
        <div class="content-container max-w-[1080px] mx-auto">
          <section id="overview" class="mb-10 scroll-mt-16">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Button</h1>
            <p class="text-lg text-gray-600 dark:text-gray-400 mb-6">
              Buttons help people take actions, such as sending an email, sharing a document, or liking a comment.
            </p>
            
            <!-- Interactive Preview -->
            <div class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-4 lg:p-6">
              <h2 class="text-lg font-semibold mb-4">Interactive Preview</h2>
              <ButtonPreview />
            </div>
          </section>

          <section id="usage" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Usage</h2>
            
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
              </div>
              <div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg">
                <h3 class="text-red-700 dark:text-red-400 font-semibold mb-4">Don't</h3>
                <div class="flex gap-4 items-center">
                  <Button variant="primary">Click Here</Button>
                  <Button variant="secondary">Submit</Button>
                </div>
              </div>
            </div>
          </section>

          <section id="specs" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Specifications</h2>
            
            <!-- Design Tokens -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Design Tokens</h3>
              <TokenTable
                :tokens="[
                  { name: '--btn-height-sm', value: '32px', usage: 'Small button height' },
                  { name: '--btn-height-md', value: '40px', usage: 'Medium button height' },
                  { name: '--btn-height-lg', value: '48px', usage: 'Large button height' },
                  { name: '--btn-padding-x', value: '16px', usage: 'Horizontal padding' },
                  { name: '--btn-radius', value: '8px', usage: 'Corner radius' },
                  { name: '--btn-font-weight', value: '500', usage: 'Font weight' },
                  { name: '--btn-transition', value: '150ms ease', usage: 'Animation timing' }
                ]"
              />
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

          <section id="behaviors" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Behaviors</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6">
              <div>
                <h3 class="text-xl font-semibold mb-4">States</h3>
                <ul class="space-y-4">
                  <li>
                    <h4 class="font-semibold">Rest</h4>
                    <p class="text-gray-600 dark:text-gray-400">Default state of the button</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Hover</h4>
                    <p class="text-gray-600 dark:text-gray-400">When the cursor is over the button</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Active/Pressed</h4>
                    <p class="text-gray-600 dark:text-gray-400">When the button is being clicked</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Disabled</h4>
                    <p class="text-gray-600 dark:text-gray-400">When the button is not interactive</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Loading</h4>
                    <p class="text-gray-600 dark:text-gray-400">When the action is being processed</p>
                  </li>
                </ul>
              </div>
              <div>
                <h3 class="text-xl font-semibold mb-4">Interactions</h3>
                <ul class="space-y-4">
                  <li>
                    <h4 class="font-semibold">Click/Tap</h4>
                    <p class="text-gray-600 dark:text-gray-400">Primary interaction method</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Keyboard</h4>
                    <p class="text-gray-600 dark:text-gray-400">Enter/Space triggers the button</p>
                  </li>
                  <li>
                    <h4 class="font-semibold">Focus</h4>
                    <p class="text-gray-600 dark:text-gray-400">Visual indicator when focused via keyboard</p>
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section id="development" class="mb-10 scroll-mt-16">
            <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Development</h2>
            
            <!-- API Reference -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">API Reference</h3>
              <PropRow
                v-for="prop in props"
                :key="prop.name"
                v-bind="prop"
              />
            </div>

            <!-- Code Examples -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Examples</h3>
              <ComponentShowcase>
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
            </div>
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