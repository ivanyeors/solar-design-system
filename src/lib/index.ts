import { BaseButton } from '@/design-system/components/core/button';
import { BaseBadge } from '@/design-system/components/core/badge';
import * as TokenUtils from './tokens';

// Export individual components
export { BaseButton as Button, BaseBadge as Badge, TokenUtils };

// Export all components as a plugin
export default {
  install: (app: any) => {
    app.component('SolarButton', Button);
    app.component('SolarBadge', Badge);
    // Add more components as they are created
  }
}; 