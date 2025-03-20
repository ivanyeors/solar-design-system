import fs from 'fs';
import path from 'path';
import plugin from 'tailwindcss/plugin';
import { fileURLToPath } from 'url';

// Get __dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Function to extract token variables from SCSS files
function extractTokenVariables(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const regex = /--([a-zA-Z0-9-]+):/g;
    const matches = [...content.matchAll(regex)];
    return matches.map(match => match[1]);
  } catch (error) {
    console.error(`Error reading token file ${filePath}:`, error);
    return [];
  }
}

// Function to categorize tokens
function categorizeTokens(tokens) {
  const categories = {
    text: [],
    bg: [],
    border: [],
    other: []
  };

  tokens.forEach(token => {
    if (token.includes('text')) {
      categories.text.push(token);
    } else if (token.includes('fill')) {
      categories.bg.push(token);
    } else if (token.includes('stroke')) {
      categories.border.push(token);
    } else {
      categories.other.push(token);
    }
  });

  return categories;
}

// Generated on: 2025-03-20T05:58:25.775Z
export default plugin(function({ addUtilities }) {
  // Get tokens directory
  const tokensDir = path.join(__dirname, 'tokens/semantic-tokens');
  
  let allTokens = [];
  
  // Read all token files if directory exists
  if (fs.existsSync(tokensDir)) {
    try {
      const files = fs.readdirSync(tokensDir);
      files.forEach(file => {
        if (file.endsWith('.scss')) {
          const tokens = extractTokenVariables(path.join(tokensDir, file));
          allTokens = [...allTokens, ...tokens];
        }
      });
    } catch (error) {
      console.error('Error reading token directory:', error);
    }
  }
  
  // Remove duplicates
  allTokens = [...new Set(allTokens)];
  
  // Categorize tokens
  const categorizedTokens = categorizeTokens(allTokens);
  
  // Create utility classes
  const semanticUtilities = {};
  
  // Text utilities
  categorizedTokens.text.forEach(token => {
    // Convert token variable to class name
    // e.g. color-text-primary-rest -> text-primary
    const baseName = token.replace('color-text-', '').split('-')[0];
    const state = token.split('-').slice(-1)[0];
    
    const className = state === 'rest' 
      ? `.text-${baseName}` 
      : `.text-${baseName}-${state}`;
    
    semanticUtilities[className] = {
      color: `var(--${token})`
    };
  });
  
  // Background utilities
  categorizedTokens.bg.forEach(token => {
    // Convert token variable to class name
    // e.g. color-fill-brand-rest -> bg-brand
    const baseName = token.replace('color-fill-', '').split('-')[0];
    const state = token.split('-').slice(-1)[0];
    
    const className = state === 'rest' 
      ? `.bg-${baseName}` 
      : `.bg-${baseName}-${state}`;
    
    semanticUtilities[className] = {
      backgroundColor: `var(--${token})`
    };
  });
  
  // Border utilities
  categorizedTokens.border.forEach(token => {
    // Convert token variable to class name
    // e.g. color-stroke-brand-rest -> border-brand
    const baseName = token.replace('color-stroke-', '').split('-')[0];
    const state = token.split('-').slice(-1)[0];
    
    const className = state === 'rest' 
      ? `.border-${baseName}` 
      : `.border-${baseName}-${state}`;
    
    semanticUtilities[className] = {
      borderColor: `var(--${token})`
    };
  });
  
  // If no dynamic tokens were found, use hardcoded fallbacks
  if (Object.keys(semanticUtilities).length === 0) {
    console.warn('No semantic tokens found, using fallback hardcoded utilities');
    
    // TEXT COLORS
    semanticUtilities['.text-primary'] = {
      color: 'var(--color-text-primary-rest)'
    };
    semanticUtilities['.text-secondary'] = {
      color: 'var(--color-text-secondary-rest)'
    };
    semanticUtilities['.text-brand'] = {
      color: 'var(--color-text-brand-rest)'
    };
    
    // BACKGROUND COLORS
    semanticUtilities['.bg-primary'] = {
      backgroundColor: 'var(--color-fill-brand-rest)'
    };
    semanticUtilities['.bg-neutral'] = {
      backgroundColor: 'var(--color-fill-neutral-rest)'
    };
    
    // BORDER COLORS
    semanticUtilities['.border-primary'] = {
      borderColor: 'var(--color-stroke-brand-rest)'
    };
  }

  addUtilities(semanticUtilities);
});