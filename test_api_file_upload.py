"""
Test script for the file upload functionality of the Code Quality Analyzer API.
This script tests the /analyze-code endpoint by uploading a test file.
"""
import requests
import sys
import os

# Configure the API URL - change this to your Vercel URL when testing the deployed version
API_URL = "http://localhost:3000"
# API_URL = "https://your-vercel-app.vercel.app"  # Uncomment for testing deployed version

def test_analyze_code_endpoint():
    """Test the /analyze-code endpoint with a Python file."""
    print(f"Testing file upload to {API_URL}/analyze-code")
    
    # Example Python file content for testing
    python_code = """
def badFunction():
    x = 10
    y = 20
    # No docstring, bad naming, etc.
    return x+y
"""
    
    # Save test code to a temporary file
    with open("test_sample.py", "w") as f:
        f.write(python_code)
    
    try:
        # Upload the file to the analyze-code endpoint
        with open("test_sample.py", "rb") as f:
            files = {"file": ("test_sample.py", f, "text/plain")}
            
            # Make the POST request to the API
            response = requests.post(f"{API_URL}/analyze-code", files=files)
            
            # Print response details for debugging
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            
            try:
                print(f"Response JSON: {response.json()}")
            except:
                print(f"Raw Response: {response.text}")
                
    finally:
        # Clean up the temporary file
        if os.path.exists("test_sample.py"):
            os.remove("test_sample.py")

if __name__ == "__main__":
    test_analyze_code_endpoint() 