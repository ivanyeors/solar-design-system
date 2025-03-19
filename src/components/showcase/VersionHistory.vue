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
  <div class="version-history">
    <div 
      v-for="(version, index) in versions" 
      :key="index"
      class="version-item"
      :class="index !== versions.length - 1 ? 'version-item--with-line' : ''"
    >
      <!-- Version marker -->
      <div class="version-marker"></div>
      
      <!-- Version content -->
      <div class="version-content">
        <div class="version-header">
          <h3 class="version-title">{{ version.version }}</h3>
          <span class="version-date">{{ version.date }}</span>
        </div>
        
        <ul class="version-changes">
          <li 
            v-for="(change, changeIndex) in version.changes" 
            :key="changeIndex"
            class="version-change"
          >
            <span class="change-bullet">•</span>
            <span class="change-text">{{ change }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.version-history {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.version-item {
  position: relative;
  padding-left: var(--comp-button-main-h-padding-l);
  padding-bottom: var(--comp-button-main-v-padding-l);
}

.version-item--with-line {
  border-left: 2px solid var(--color-border-primary-rest);
}

.version-marker {
  position: absolute;
  left: -6px;
  width: 12px;
  height: 12px;
  border-radius: var(--comp-button-main-radius);
  background-color: var(--color-fill-brand-rest);
  border: 2px solid var(--color-surface-primary-rest);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.version-content {
  background-color: var(--color-surface-secondary-rest);
  border-radius: var(--comp-button-main-radius);
  padding: var(--comp-button-main-v-padding-m) var(--comp-button-main-h-padding-m);
  margin-left: var(--comp-button-main-gap);
  border: 1px solid var(--color-border-primary-rest);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.version-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--comp-button-main-gap);
}

.version-title {
  font-weight: var(--font-weight-semibold-600);
  font-size: var(--font-size-16);
  color: var(--color-text-primary-rest);
  transition: color 0.2s ease;
}

.version-date {
  font-size: var(--font-size-14);
  color: var(--color-text-secondary-rest);
  transition: color 0.2s ease;
}

.version-changes {
  display: flex;
  flex-direction: column;
  gap: var(--comp-button-main-gap);
}

.version-change {
  display: flex;
  align-items: flex-start;
  gap: var(--comp-button-main-gap);
  color: var(--color-text-secondary-rest);
  transition: color 0.2s ease;
}

.change-bullet {
  color: var(--color-text-brand-rest);
  font-size: var(--font-size-16);
  line-height: 1;
  transition: color 0.2s ease;
}

.change-text {
  font-size: var(--font-size-14);
  line-height: 1.5;
  transition: color 0.2s ease;
}

/* Dark mode adjustments */
:root[data-theme="dark"] {
  .version-marker {
    background-color: var(--color-fill-brand-rest);
    border-color: var(--color-surface-secondary-rest);
  }

  .version-content {
    background-color: var(--color-surface-secondary-rest);
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

  .change-bullet {
    color: var(--color-text-brand-rest);
  }

  /* Add hover effects for dark mode */
  .version-content:hover {
    background-color: var(--color-surface-secondary-hover);
    border-color: var(--color-border-brand-hover);
  }

  .version-marker:hover {
    background-color: var(--color-fill-brand-hover);
  }
}

/* Add hover effects for light mode */
@media (hover: hover) {
  .version-content:hover {
    background-color: var(--color-surface-secondary-hover);
    border-color: var(--color-border-brand-hover);
  }

  .version-marker:hover {
    background-color: var(--color-fill-brand-hover);
  }
}
</style> 