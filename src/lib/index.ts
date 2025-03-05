import Button from '../components/ui/Button.vue';

// Export individual components
export { Button };

// Export all components as a plugin
export default {
  install: (app: any) => {
    app.component('SolarButton', Button);
    // Add more components as they are created
  }
}; 