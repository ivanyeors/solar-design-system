<script setup lang="ts">
defineProps<{
  title: string;
  isError?: boolean;
}>();
</script>

<template>
  <div class="placeholder-page">
    <div class="content-wrapper">
      <div class="icon-wrapper" :class="{ 'error': isError }">
        <svg v-if="isError" xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <h1 class="title">{{ title }}</h1>
      <p class="message" v-if="isError">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <p class="message" v-else>
        This component is currently under development.
        <br>Check back soon for updates!
      </p>
      <router-link to="/" class="back-link">
        Return to Home
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.placeholder-page {
  min-height: calc(100vh - 4rem);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.content-wrapper {
  text-align: center;
  max-width: 32rem;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  background-color: var(--color-fill-brand-pale-rest);
  color: var(--color-icon-brand-rest);
  margin-bottom: 1.5rem;
}

.icon-wrapper.error {
  background-color: var(--color-fill-error-pale-rest);
  color: var(--color-icon-error-rest);
}

.icon {
  width: 2rem;
  height: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary-rest);
  margin-bottom: 1rem;
}

.message {
  font-size: 1.125rem;
  color: var(--color-text-secondary-rest);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.back-link {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-radius: var(--comp-button-main-radius);
  background-color: var(--color-surface-brand-rest);
  color: var(--color-text-brand-rest);
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-link:hover {
  background-color: var(--color-surface-brand-hover);
  color: var(--color-text-brand-hover);
}

.back-link:active {
  background-color: var(--color-surface-brand-press);
  color: var(--color-text-brand-press);
}
</style> 