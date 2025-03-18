import Button from '../components/ui/Button.vue';
import Badge from '../components/ui/Badge.vue';
import * as TokenUtils from './tokens';

// Export individual components
export { Button, Badge, TokenUtils };

// Export all components as a plugin
export default {
  install: (app: any) => {
    app.component('SolarButton', Button);
    app.component('SolarBadge', Badge);
    // Add more components as they are created
  }
}; 