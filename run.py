"""
Run script for the Code Quality Analyzer backend server.
"""
import uvicorn

if __name__ == "__main__":
    # Run the FastAPI server with reload enabled for development
    print("Starting Code Quality Analyzer server at http://localhost:8000")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True) 