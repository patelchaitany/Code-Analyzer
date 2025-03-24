const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // This proxy configuration is for development only
  // In production, the Vercel config handles routing
  if (process.env.NODE_ENV === 'development') {
    app.use(
      ['/api', '/analyze-code'],
      createProxyMiddleware({
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        pathRewrite: {
          '^/api': ''
        }
      })
    );
  }
}; 