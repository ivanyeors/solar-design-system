import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    lib: {
      entry: './src/lib/index.ts',
      name: 'VueDesignSystem',
      fileName: (format) => `vue-design-system.${format}.js`,
    },
    rollupOptions: {
      // Externalize dependencies that shouldn't be bundled
      external: ['vue'],
      output: {
        // Global variables to use in UMD build
        globals: {
          vue: 'Vue',
        },
        exports: 'named'
      },
    },
  },
})
