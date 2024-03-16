from fastapi.middleware.cors import CORSMiddleware

# List of allowed origins
origins = ["http://127.0.0.1:5500"]

# Function to create and configure CORS middleware
def create_cors_middleware(app):
    return CORSMiddleware(
        app,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )