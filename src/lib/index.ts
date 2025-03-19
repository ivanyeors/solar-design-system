import { ButtonMain as Button } from '../design-system/button';
import { Badge } from '../design-system/badge';
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