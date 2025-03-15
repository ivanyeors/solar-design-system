/**
 * Script to start the Storybook server and the browser-tools server concurrently
 */

// Check if browser-tools MCP is enabled - a simple environment variable check
// In a real scenario, you might have a more sophisticated way to detect this
const isBrowserToolsEnabled = process.env.BROWSER_TOOLS_ENABLED !== 'false';

if (isBrowserToolsEnabled) {
  console.log('🔧 Browser Tools MCP is enabled. Starting browser-tools server alongside Storybook...');
  
  // Using dynamic import for ESM compatibility
  import('concurrently').then(concurrently => {
    concurrently.default([
      { 
        command: 'npm run storybook:no-tools',
        name: 'storybook',
        prefixColor: 'green',
      },
      { 
        command: 'npm run browser-tools',
        name: 'browser-tools',
        prefixColor: 'magenta',
      }
    ], {
      prefix: 'name',
      killOthers: ['failure', 'success'],
      restartTries: 3,
    }).then(
      () => console.log('All processes exited successfully'),
      (error) => console.error('One or more processes failed:', error)
    );
  }).catch(error => {
    console.error('Failed to import concurrently:', error);
    process.exit(1);
  });
} else {
  console.log('📚 Starting Storybook...');
  // Simply run Storybook directly if browser-tools is not enabled
  import('child_process').then(childProcess => {
    const process = childProcess.spawn('npm', ['run', 'storybook:no-tools'], { 
      stdio: 'inherit',
      shell: true
    });
    
    process.on('error', (error) => {
      console.error('Failed to start Storybook:', error);
      process.exit(1);
    });
  });
} 