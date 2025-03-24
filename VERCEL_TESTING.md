# Testing and Troubleshooting Your Vercel Deployment

This guide will help you test and troubleshoot your Code Quality Analyzer deployment on Vercel.

## Local Testing Before Deployment

Before deploying to Vercel, it's a good practice to test your serverless function locally:

1. Run the local test server:
   ```
   python test_vercel_api.py
   ```
   This will start your Vercel function at http://localhost:3000

2. Test the file upload endpoint:
   ```
   python test_api_file_upload.py
   ```
   This script will send a test file to the /analyze-code endpoint and print the response.

## Common Issues with Vercel Deployment

### 1. File Upload Issues

If you're experiencing issues with file uploads on Vercel, check the following:

- **Size limits**: Vercel has a 4.5MB payload size limit for serverless functions.
- **Timeout issues**: Serverless functions have a default timeout of 10 seconds.
- **Middleware handling**: The middleware might not be processing the request correctly.

### 2. Path Configuration Issues

- Make sure your `vercel.json` has the correct routes configured:
  ```json
  {
    "routes": [
      {
        "src": "/api/(.*)",
        "dest": "/api/index.py"
      },
      {
        "src": "/analyze-code",
        "dest": "/api/index.py"
      }
    ]
  }
  ```

### 3. Debug Deployment Issues

To debug Vercel deployment issues:

1. Check the Vercel deployment logs in your Vercel dashboard
2. Use the `vercel logs` command in your terminal
3. Add print statements in your code to track flow
4. Test with the local development server to verify functionality

## Testing the Deployed Application

To test your deployed application:

1. Update the `API_URL` in `test_api_file_upload.py` to your Vercel URL
2. Run the test script:
   ```
   python test_api_file_upload.py
   ```

3. Check the response to see any error messages or status codes

## Fixes for Common Issues

### Fix for 500 Server Error

If you're getting 500 errors:

1. Make sure your function isn't exceeding the memory or timeout limits
2. Ensure all dependencies are correctly specified in requirements.txt
3. Check that your file handling logic works correctly

### Fix for CORS Issues

If you're experiencing CORS issues:

1. Your CORS middleware is already set up in api/index.py
2. Make sure your frontend is sending the correct headers
3. Try specifying your frontend URL in allow_origins instead of "*" 