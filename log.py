import logging
from fastapi import FastAPI

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)  # Set log level to DEBUG

# Log a message
logging.debug("This is a debug message")
