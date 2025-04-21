import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/home';
import ButtonPage from './pages/components/button';
import TokensPage from './pages/foundation/tokens';
import BrandsPage from './pages/foundation/brands';
import PlaceholderPage from './components/global/PlaceholderPage.vue';
import { ColorPage } from './design-system/color';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  // Foundation routes
  {
    path: '/foundation/tokens',
    name: 'Design Tokens',
    component: TokensPage,
  },
  {
    path: '/foundation/brands',
    name: 'Brands',
    component: BrandsPage,
  },
  {
    path: '/foundation/colors',
    name: 'Colors',
    component: ColorPage,
  },
  {
    path: '/foundation/typography',
    name: 'Typography',
    component: PlaceholderPage,
    props: { title: 'Typography' }
  },
  {
    path: '/foundation/spacing',
    name: 'Spacing',
    component: PlaceholderPage,
    props: { title: 'Spacing' }
  },
  {
    path: '/foundation/breakpoints',
    name: 'Breakpoints',
    component: PlaceholderPage,
    props: { title: 'Breakpoints' }
  },
  // Component routes
  {
    path: '/components/button',
    name: 'Button',
    component: ButtonPage,
  },
  {
    path: '/components/input',
    name: 'Input',
    component: PlaceholderPage,
    props: { title: 'Input' }
  },
  {
    path: '/components/card',
    name: 'Card',
    component: PlaceholderPage,
    props: { title: 'Card' }
  },
  {
    path: '/components/badge',
    name: 'Badge',
    component: PlaceholderPage,
    props: { title: 'Badge' }
  }
];

const router = createRouter({
  history: createWebHistory('/solar-design-system/'),
  routes,
  scrollBehavior(to, _from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    }
    
    if (savedPosition) {
      return savedPosition;
    }
    
    return { top: 0 };
  },
});

export default router; 