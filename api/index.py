from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add the backend directory to the path so we can import from it
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app from the backend
from backend.main import app as backend_app

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

# Route all requests to the backend app
@app.middleware("http")
async def route_to_backend(request: Request, call_next):
    # Make the backend app handle the request
    response = await backend_app(request.scope, request.receive, request.send)
    return response

# Add the backend app's routes to this app
app.routes.extend(backend_app.routes) 