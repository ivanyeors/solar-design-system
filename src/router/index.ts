// @ts-ignore - TypeScript doesn't recognize importmap resolutions, but it works at runtime
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import HomePage from '@/pages/home/HomePage.vue'
import ButtonPage from '@/design-system/components/core/button/ButtonPage.vue'
import TokensPage from '@/design-system/tokens/TokensPage.vue'
import BrandsPage from '@/design-system/brands/BrandsPage.vue'
import ColorPage from '@/design-system/color/ColorPage.vue'
import PlaceholderPage from '@/components/global/PlaceholderPage.vue'

// Get base URL from Vite configuration, defaulting to /solar-design-system/ for GitHub Pages
const baseUrl = import.meta.env.BASE_URL || '/solar-design-system/'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  // Foundation routes
  {
    path: '/foundation/tokens',
    name: 'tokens',
    component: TokensPage
  },
  {
    path: '/foundation/brands',
    name: 'brands',
    component: BrandsPage
  },
  {
    path: '/foundation/colors',
    name: 'colors',
    component: ColorPage
  },
  {
    path: '/foundation/typography',
    name: 'typography',
    component: PlaceholderPage,
    props: { title: 'Typography' }
  },
  {
    path: '/foundation/spacing',
    name: 'spacing',
    component: PlaceholderPage,
    props: { title: 'Spacing' }
  },
  {
    path: '/foundation/breakpoints',
    name: 'breakpoints',
    component: PlaceholderPage,
    props: { title: 'Breakpoints' }
  },
  // Component routes
  {
    path: '/components/button',
    name: 'button',
    component: ButtonPage
  },
  {
    path: '/components/input',
    name: 'input',
    component: PlaceholderPage,
    props: { title: 'Input' }
  },
  {
    path: '/components/card',
    name: 'card',
    component: PlaceholderPage,
    props: { title: 'Card' }
  },
  {
    path: '/components/badge',
    name: 'badge',
    component: PlaceholderPage,
    props: { title: 'Badge' }
  },
  // Catch-all route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: PlaceholderPage,
    props: { title: 'Page Not Found', isError: true }
  }
]

const router = createRouter({
  history: createWebHistory(baseUrl),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

export default router 