<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps<{
  side: 'left' | 'right';
  minWidth: number;
  maxWidth: number;
  defaultWidth: number;
  isCollapsible?: boolean;
  id: string;
}>();

const STORAGE_KEY_WIDTH = `sidebar-${props.id}-width`;
const STORAGE_KEY_COLLAPSED = `sidebar-${props.id}-collapsed`;

const width = ref(props.defaultWidth);
const isResizing = ref(false);
const isCollapsed = ref(false);

onMounted(() => {
  try {
    const savedWidth = localStorage.getItem(STORAGE_KEY_WIDTH);
    if (savedWidth) {
      const parsedWidth = parseInt(savedWidth);
      if (!isNaN(parsedWidth) && parsedWidth >= props.minWidth && parsedWidth <= props.maxWidth) {
        width.value = parsedWidth;
      }
    }

    const savedCollapsed = localStorage.getItem(STORAGE_KEY_COLLAPSED);
    if (savedCollapsed) {
      isCollapsed.value = savedCollapsed === 'true';
    }
  } catch (error) {
    console.warn('Failed to load sidebar preferences:', error);
  }
});

watch(width, (newWidth) => {
  try {
    localStorage.setItem(STORAGE_KEY_WIDTH, newWidth.toString());
  } catch (error) {
    console.warn('Failed to save sidebar width:', error);
  }
});

watch(isCollapsed, (newState) => {
  try {
    localStorage.setItem(STORAGE_KEY_COLLAPSED, newState.toString());
  } catch (error) {
    console.warn('Failed to save sidebar collapsed state:', error);
  }
});

const startResizing = (event: MouseEvent) => {
  isResizing.value = true;
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', stopResizing);
};

const handleMouseMove = (event: MouseEvent) => {
  if (!isResizing.value) return;
  
  const newWidth = props.side === 'left' 
    ? event.clientX 
    : window.innerWidth - event.clientX;
    
  width.value = Math.min(
    Math.max(props.minWidth, newWidth),
    props.maxWidth
  );
};

const stopResizing = () => {
  isResizing.value = false;
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', stopResizing);
};

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
};

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', stopResizing);
});
</script>

<template>
  <div 
    class="relative flex"
    :class="[
      side === 'left' ? 'mr-2' : 'ml-2',
      isCollapsed ? 'w-12' : ''
    ]"
    :style="{ 
      width: isCollapsed ? '48px' : `${width}px`,
      transition: isResizing ? 'none' : 'width 0.2s ease'
    }"
  >
    <!-- Sidebar Content -->
    <div 
      class="h-screen overflow-y-auto bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800"
      :class="[
        side === 'left' ? 'border-r' : 'border-l',
        isCollapsed ? 'w-12 overflow-hidden' : 'w-full'
      ]"
    >
      <!-- Collapse Button -->
      <button
        v-if="isCollapsible"
        @click="toggleCollapse"
        class="absolute top-4 p-2 bg-gray-100 dark:bg-gray-800 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
        :class="side === 'left' ? 'right-0 translate-x-1/2' : 'left-0 -translate-x-1/2'"
      >
        <i 
          :class="[
            isCollapsed ? 'icon-chevron-right' : 'icon-chevron-left',
            side === 'right' && !isCollapsed ? 'transform rotate-180' : ''
          ]"
          class="w-4 h-4 text-gray-500"
        ></i>
      </button>

      <!-- Actual Content -->
      <div :class="isCollapsed ? 'opacity-0' : 'opacity-100'">
        <slot></slot>
      </div>
    </div>

    <!-- Resize Handle -->
    <div
      class="absolute top-0 bottom-0 w-1 cursor-col-resize hover:bg-blue-500 transition-colors"
      :class="[
        side === 'left' ? '-right-1' : '-left-1',
        isResizing ? 'bg-blue-500' : 'bg-transparent'
      ]"
      @mousedown="startResizing"
    ></div>
  </div>
</template>

<style scoped>
.resize-handle {
  touch-action: none;
}
</style> 