// Import our component export utility
import { createComponentExports } from '../../../../lib/utils/components';

// Import badge component
import BadgeComponent from './components/Badge.vue';

// Create standardized exports
export const { Badge, BaseBadge } = createComponentExports(BadgeComponent, 'Badge'); 