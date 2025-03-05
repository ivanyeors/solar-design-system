<script setup lang="ts">
import Button from '../components/ui/Button.vue';
import ComponentShowcase from '../components/showcase/ComponentShowcase.vue';
import PropRow from '../components/showcase/PropRow.vue';
</script>

<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Button</h1>
      <p class="mt-2 text-lg text-gray-600 dark:text-gray-400">
        Buttons allow users to trigger an action or event with a single click.
      </p>
    </div>
    
    <div class="space-y-12">
      <!-- Basic Button -->
      <ComponentShowcase
        title="Basic Button"
        description="The default button component with various styles and states."
        componentName="Button"
      >
        <template #preview>
          <Button>Default Button</Button>
          <Button variant="primary">Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
        </template>
        
        <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button&gt;Default Button&lt;/Button&gt;
&lt;Button variant="primary"&gt;Primary&lt;/Button&gt;
&lt;Button variant="secondary"&gt;Secondary&lt;/Button&gt;
&lt;Button variant="outline"&gt;Outline&lt;/Button&gt;
&lt;Button variant="ghost"&gt;Ghost&lt;/Button&gt;
        </template>
        
        <template #props>
          <PropRow
            name="variant"
            type="'primary' | 'secondary' | 'outline' | 'ghost'"
            defaultValue="'primary'"
            description="The visual style of the button."
          />
          <PropRow
            name="size"
            type="'sm' | 'md' | 'lg'"
            defaultValue="'md'"
            description="The size of the button."
          />
          <PropRow
            name="disabled"
            type="boolean"
            defaultValue="false"
            description="Whether the button is disabled."
          />
          <PropRow
            name="loading"
            type="boolean"
            defaultValue="false"
            description="Whether the button is in a loading state."
          />
        </template>
      </ComponentShowcase>
      
      <!-- Button Sizes -->
      <ComponentShowcase
        title="Button Sizes"
        description="Buttons come in three different sizes."
        componentName="Button"
      >
        <template #preview>
          <Button size="sm">Small</Button>
          <Button size="md">Medium</Button>
          <Button size="lg">Large</Button>
        </template>
        
        <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button size="sm"&gt;Small&lt;/Button&gt;
&lt;Button size="md"&gt;Medium&lt;/Button&gt;
&lt;Button size="lg"&gt;Large&lt;/Button&gt;
        </template>
      </ComponentShowcase>
      
      <!-- Button States -->
      <ComponentShowcase
        title="Button States"
        description="Buttons can be disabled or show a loading state."
        componentName="Button"
      >
        <template #preview>
          <Button>Normal</Button>
          <Button disabled>Disabled</Button>
          <Button loading>Loading</Button>
        </template>
        
        <template #code>
import Button from '@/components/ui/Button.vue';

&lt;Button&gt;Normal&lt;/Button&gt;
&lt;Button disabled&gt;Disabled&lt;/Button&gt;
&lt;Button loading&gt;Loading&lt;/Button&gt;
        </template>
      </ComponentShowcase>
    </div>
  </div>
</template> 