// @ts-ignore - TypeScript doesn't recognize importmap resolutions, but it works at runtime
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/home/HomePage.vue'
import ButtonPage from '../design-system/button/ButtonPage.vue'
import TokensPage from '../design-system/tokens/TokensPage.vue'
import BrandsPage from '../design-system/brands/BrandsPage.vue'

// Get base URL from Vite configuration, defaulting to /solar-design-system/ for GitHub Pages
const baseUrl = import.meta.env.BASE_URL || '/solar-design-system/'

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/components/button',
      name: 'button',
      component: ButtonPage
    },
    {
      path: '/foundation/tokens',
      name: 'tokens',
      component: TokensPage
    },
    {
      path: '/foundation/brands',
      name: 'brands',
      component: BrandsPage
    }
  ]
})

export default router 