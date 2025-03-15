/**
 * Example: Using the extracted design tokens in a frontend application
 */

// Import all tokens
import tokens from '../src/tokens';

// Or import specific token categories
import { optionColors, optionScale, brands, themes } from '../src/tokens';

/**
 * Example 1: Using option tokens directly
 */
function createColorPalette() {
  const container = document.createElement('div');
  container.className = 'color-palette';
  
  // Get all stone color tokens
  const stoneColors = Object.entries(optionColors)
    .filter(([key]) => key.includes('stone'))
    .map(([key, value]) => ({ key, value }));
  
  stoneColors.forEach(({ key, value }) => {
    const colorSwatch = document.createElement('div');
    colorSwatch.className = 'color-swatch';
    colorSwatch.style.backgroundColor = value;
    colorSwatch.style.width = '100px';
    colorSwatch.style.height = '100px';
    colorSwatch.style.margin = '10px';
    colorSwatch.style.display = 'inline-block';
    colorSwatch.style.position = 'relative';
    
    const label = document.createElement('span');
    label.innerText = key;
    label.style.position = 'absolute';
    label.style.bottom = '5px';
    label.style.left = '5px';
    label.style.fontSize = '12px';
    label.style.fontFamily = 'monospace';
    
    colorSwatch.appendChild(label);
    container.appendChild(colorSwatch);
  });
  
  return container;
}

/**
 * Example 2: Creating a themed component using semantic tokens
 */
function createThemedButton(theme = 'light', text = 'Click Me') {
  const button = document.createElement('button');
  button.innerText = text;
  button.className = `button button-${theme}`;
  
  // Apply theme tokens
  button.style.backgroundColor = themes['color.fill.brand-rest'];
  button.style.color = themes['color.text.neutrallight-rest'];
  button.style.border = `1px solid ${themes['color.border.brand-rest']}`;
  button.style.borderRadius = '4px';
  button.style.padding = '10px 20px';
  button.style.cursor = 'pointer';
  button.style.transition = 'all 0.2s ease';
  
  // Add hover state
  button.addEventListener('mouseover', () => {
    button.style.backgroundColor = themes['color.fill.brand-hover'];
    button.style.borderColor = themes['color.border.brand-hover'];
  });
  
  button.addEventListener('mouseout', () => {
    button.style.backgroundColor = themes['color.fill.brand-rest'];
    button.style.borderColor = themes['color.border.brand-rest'];
  });
  
  // Add press state
  button.addEventListener('mousedown', () => {
    button.style.backgroundColor = themes['color.fill.brand-press'];
    button.style.borderColor = themes['color.border.brand-press'];
  });
  
  button.addEventListener('mouseup', () => {
    button.style.backgroundColor = themes['color.fill.brand-hover'];
    button.style.borderColor = themes['color.border.brand-hover'];
  });
  
  return button;
}

/**
 * Example 3: Using scaled tokens for consistent spacing and sizing
 */
function createLayout() {
  const layout = document.createElement('div');
  layout.className = 'layout';
  layout.style.display = 'flex';
  layout.style.flexDirection = 'column';
  layout.style.gap = optionScale['base.gap.size-5'];
  layout.style.padding = optionScale['base.padding.size-6'];
  
  const header = document.createElement('header');
  header.className = 'header';
  header.innerText = 'Token Example Header';
  header.style.fontSize = '24px';
  header.style.fontWeight = 'bold';
  header.style.marginBottom = optionScale['base.gap.size-4'];
  
  const content = document.createElement('main');
  content.className = 'content';
  content.innerText = 'This layout uses consistent spacing from design tokens.';
  content.style.padding = optionScale['base.padding.size-5'];
  content.style.backgroundColor = optionColors['color-stone-50'];
  content.style.borderRadius = optionScale['base.radius.size-3'] + 'px';
  
  layout.appendChild(header);
  layout.appendChild(content);
  layout.appendChild(createThemedButton('light', 'Primary Button'));
  
  return layout;
}

/**
 * Example 4: Creating a component with support for both light and dark themes
 */
function createThemeSwitchableComponent() {
  const container = document.createElement('div');
  container.className = 'theme-container';
  container.style.padding = '20px';
  container.style.display = 'flex';
  container.style.flexDirection = 'column';
  container.style.gap = '20px';
  
  // Theme toggle
  const toggle = document.createElement('button');
  toggle.innerText = 'Toggle Theme';
  toggle.className = 'theme-toggle';
  toggle.style.padding = '8px 16px';
  toggle.style.alignSelf = 'flex-start';
  
  // Card component
  const card = document.createElement('div');
  card.className = 'card';
  card.style.padding = '20px';
  card.style.borderRadius = '8px';
  card.style.transition = 'all 0.3s ease';
  
  const cardTitle = document.createElement('h3');
  cardTitle.innerText = 'Themed Card Component';
  cardTitle.style.marginTop = '0';
  cardTitle.style.transition = 'color 0.3s ease';
  
  const cardContent = document.createElement('p');
  cardContent.innerText = 'This card changes its appearance based on the current theme.';
  cardContent.style.transition = 'color 0.3s ease';
  
  card.appendChild(cardTitle);
  card.appendChild(cardContent);
  
  let isDarkTheme = false;
  
  function applyTheme() {
    // Apply theme tokens based on current mode
    if (isDarkTheme) {
      container.style.backgroundColor = '#17191a'; // Dark background
      card.style.backgroundColor = '#242629'; // Dark card
      card.style.boxShadow = 'none';
      cardTitle.style.color = '#ffffff';
      cardContent.style.color = '#9aa2ad';
    } else {
      container.style.backgroundColor = '#ffffff'; // Light background
      card.style.backgroundColor = '#ffffff'; // Light card
      card.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
      cardTitle.style.color = '#17191a';
      cardContent.style.color = '#7e8794';
    }
  }
  
  // Initial theme application
  applyTheme();
  
  // Theme toggle functionality
  toggle.addEventListener('click', () => {
    isDarkTheme = !isDarkTheme;
    applyTheme();
  });
  
  container.appendChild(toggle);
  container.appendChild(card);
  
  return container;
}

// Demo initialization
document.addEventListener('DOMContentLoaded', () => {
  const app = document.getElementById('app');
  if (app) {
    app.appendChild(createColorPalette());
    app.appendChild(document.createElement('hr'));
    app.appendChild(createLayout());
    app.appendChild(document.createElement('hr'));
    app.appendChild(createThemeSwitchableComponent());
  }
});

// Export examples for reuse
export {
  createColorPalette,
  createThemedButton,
  createLayout,
  createThemeSwitchableComponent
}; 