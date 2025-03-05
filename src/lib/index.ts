import Button from '../components/ui/Button.vue';

// Export individual components
export { Button };

// Export all components as a plugin
export default {
  install: (app: any) => {
    app.component('DsButton', Button);
    // Add more components as they are created
  }
}; 