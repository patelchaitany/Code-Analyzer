/**
 * Custom start script for React development server
 * to work around the allowedHosts configuration issue
 */
const { spawn } = require('child_process');
const path = require('path');

// Set environment variables
process.env.DANGEROUSLY_DISABLE_HOST_CHECK = 'true';
process.env.WDS_SOCKET_PORT = '0';
process.env.PORT = '3000';

// Launch React development server with modified settings
const startProcess = spawn(
  'node',
  [path.resolve('node_modules/react-scripts/scripts/start.js')],
  {
    stdio: 'inherit',
    env: {
      ...process.env,
      BROWSER: 'none',
    },
  }
);

// Handle process exit
startProcess.on('exit', (code) => {
  process.exit(code);
});

// Handle process errors
startProcess.on('error', (err) => {
  console.error('Failed to start development server:', err);
  process.exit(1);
}); 