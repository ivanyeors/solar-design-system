import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: '/solar-design-system/',
  
  // Only use library mode when explicitly building the library
  ...(process.env.BUILD_LIB ? {
    build: {
      lib: {
        entry: './src/lib/index.ts',
        name: 'SolarDesignSystem',
        fileName: (format) => `solar-design-system.${format}.js`,
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
    }
  } : {})
})
