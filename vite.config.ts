import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/solar-design-system/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
    dedupe: ['vue', 'vue-router']
  },
  optimizeDeps: {
    include: ['vue-router'],
    force: true
  },
  build: process.env.BUILD_LIB ? {
    // Library build configuration
    lib: {
      entry: './src/lib/index.ts',
      name: 'SolarDesignSystem',
      fileName: (format) => `solar-design-system.${format}.js`,
    },
    rollupOptions: {
      external: ['vue', 'vue-router'],
      output: {
        globals: {
          vue: 'Vue',
          'vue-router': 'VueRouter'
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
    modulePreload: {
      polyfill: true
    },
    rollupOptions: {
      external: ['vue', 'vue-router'],
      input: {
        main: './index.html',
      },
      output: {
        manualChunks: undefined, // Let Vite handle the chunks
        globals: {
          vue: 'Vue',
          'vue-router': 'VueRouter'
        }
      }
    }
  }
})
