// Import our component export utility
import { createComponentExports } from '../../../../lib/utils/components';

// Import icon component
import IconComponent from './components/Icon.vue';

// Create standardized exports
export const { Icon, BaseIcon } = createComponentExports(IconComponent, 'Icon'); 