<script setup lang="ts">
defineProps({
  versions: {
    type: Array,
    required: true,
    default: () => []
  }
});
</script>

<template>
  <div class="space-y-6">
    <div 
      v-for="(version, index) in versions" 
      :key="index"
      class="timeline-item"
      :class="index !== versions.length - 1 ? 'timeline-line' : ''"
    >
      <!-- Version dot -->
      <div class="timeline-dot"></div>
      
      <!-- Version content -->
      <div class="version-card">
        <div class="flex flex-wrap justify-between items-start mb-3">
          <h3 class="version-title">{{ version.version }}</h3>
          <span class="version-date">{{ version.date }}</span>
        </div>
        
        <ul class="space-y-2">
          <li 
            v-for="(change, changeIndex) in version.changes" 
            :key="changeIndex"
            class="version-change-item"
          >
            <span class="change-bullet">•</span>
            <span>{{ change }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-item {
  position: relative;
  padding-left: 2rem;
  padding-bottom: 1.5rem;
}

.timeline-line {
  border-left: 2px solid var(--color-border-primary-rest);
}

.timeline-dot {
  position: absolute;
  left: -8px;
  width: 1rem;
  height: 1rem;
  border-radius: 9999px;
  background-color: var(--color-primary-rest);
  border: 4px solid var(--color-surface-primary-rest);
}

.version-card {
  background-color: var(--color-surface-secondary-rest);
  border-radius: 0.5rem;
  padding: 1rem;
  margin-left: 1rem;
}

.version-title {
  font-weight: 600;
  font-size: 1.125rem;
  color: var(--color-text-primary-rest);
}

.version-date {
  font-size: 0.875rem;
  color: var(--color-text-tertiary-rest);
}

.version-change-item {
  color: var(--color-text-secondary-rest);
  display: flex;
  align-items: flex-start;
}

.change-bullet {
  color: var(--color-primary-rest);
  margin-right: 0.5rem;
}

/* Timeline styling */
.timeline-item:last-child {
  padding-bottom: 0;
}
</style> 