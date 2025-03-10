import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: process.env.NODE_ENV === 'production' ? '/solar-design-system/' : '/',
  
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
        exports: 'named'
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
    }
  }
})
