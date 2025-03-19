import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/solar-design-system/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      'vue-router': 'vue-router/dist/vue-router.esm-bundler.js'
    },
  },
  
  build: process.env.BUILD_LIB ? {
    // Library build configuration
    lib: {
      entry: './src/lib/index.ts',
      name: 'SolarDesignSystem',
      fileName: (format) => `solar-design-system.${format}.js`,
    },
    rollupOptions: {
      external: ['vue'],
      output: {
        globals: {
          vue: 'Vue',
        },
        exports: 'named',
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router']
        }
      },
    }
  } : {
    // GitHub Pages build configuration
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: './index.html',
      },
      output: {
        manualChunks: {
          'vue-vendor': ['vue', 'vue-router']
        }
      }
    }
  }
})
