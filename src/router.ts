import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/HomePage.vue';
import ButtonPage from './pages/ButtonPage.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/components/button',
    name: 'Button',
    component: ButtonPage,
  },
  // Add more routes as needed
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