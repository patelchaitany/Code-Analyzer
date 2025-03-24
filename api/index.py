from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os
import traceback

# Add the backend directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app and necessary functions from the backend
from backend.main import app as backend_app
from backend.main import analyze_python_code, analyze_js_code

# Create a new FastAPI app for the Vercel serverless function
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Re-export all routes from the backend app
for route in backend_app.routes:
    app.routes.append(route)

# Add a root handler for the API
@app.get("/api")
def read_api_root():
    return {"message": "Code Quality Analyzer API is running on Vercel"}

# Explicitly define the analyze-code endpoint for Vercel
@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    """
    Analyze a code file and return quality metrics.
    
    This is a duplicate of the backend endpoint, specifically for Vercel deployment.
    """
    # Check file extension
    filename = file.filename
    if not filename or not (filename.endswith(".py") or filename.endswith(".js") or filename.endswith(".jsx")):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .py, .js, and .jsx files are supported."
        )
        
    content = await file.read()
    file_extension = os.path.splitext(filename)[1]
    
    try:
        if file_extension == ".py":
            return analyze_python_code(content.decode())
        else:
            return analyze_js_code(content.decode())
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing code: {str(e)}"
        )

# Add custom exception handler for better error reporting
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = {
        "error": str(exc),
        "type": type(exc).__name__,
        "traceback": traceback.format_exc()
    }
    
    # Print error for Vercel logs
    print(f"Error in API: {error_detail['type']}: {error_detail['error']}")
    print(error_detail['traceback'])
    
    return JSONResponse(
        status_code=500,
        content={"detail": "An error occurred processing your request", "error_info": error_detail}
    )

# Route all requests to the backend app using middleware
@app.middleware("http")
async def route_to_backend(request: Request, call_next):
    try:
        # Make the backend app handle the request
        response = await call_next(request)
        return response
    except Exception as e:
        # Provide better error handling for debugging
        print(f"Error in Vercel serverless function: {str(e)}")
        raise 