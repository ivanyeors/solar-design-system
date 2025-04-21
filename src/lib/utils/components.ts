/**
 * Component export utilities for consistent naming conventions
 */

/**
 * Creates standardized exports for components with both original and Base-prefixed names
 * @param component The component to export
 * @param baseName Optional base name (defaults to component name with Base prefix)
 * @returns Object with named exports
 */
export function createComponentExports<T>(
  component: T, 
  componentName: string
): Record<string, T> {
  const baseName = `Base${componentName}`;
  
  return {
    [componentName]: component,
    [baseName]: component
  };
} 