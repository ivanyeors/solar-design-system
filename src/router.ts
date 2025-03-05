import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/HomePage.vue';
import ButtonPage from './pages/ButtonPage.vue';
import PlaceholderPage from './components/PlaceholderPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  // Foundation routes
  {
    path: '/foundation/colors',
    name: 'Colors',
    component: PlaceholderPage,
    props: { title: 'Colors' }
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