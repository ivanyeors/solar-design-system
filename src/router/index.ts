// @ts-ignore - TypeScript doesn't recognize importmap resolutions, but it works at runtime
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/home/HomePage.vue'
import ButtonPage from '../design-system/button/ButtonPage.vue'
import TokensPage from '../design-system/tokens/TokensPage.vue'
import BrandsPage from '../design-system/brands/BrandsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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