// Import our component export utility
import { createComponentExports } from '../../../../lib/utils/components';

// Import button components
import ButtonMainComponent from './components/ButtonMain.vue';
import ButtonOptionComponent from './components/ButtonOption.vue';
import ButtonPillComponent from './components/ButtonPill.vue';
import ButtonCardComponent from './components/ButtonCard.vue';

// Create standardized exports
export const { Button, BaseButton } = createComponentExports(ButtonMainComponent, 'Button');
export const { ButtonOption, BaseButtonOption } = createComponentExports(ButtonOptionComponent, 'ButtonOption');
export const { ButtonPill, BaseButtonPill } = createComponentExports(ButtonPillComponent, 'ButtonPill');
export const { ButtonCard, BaseButtonCard } = createComponentExports(ButtonCardComponent, 'ButtonCard');

// Export token utilities
export * from './ButtonTokens'; 