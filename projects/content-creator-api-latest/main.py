from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Import the crew creation function from our agent file
from agent import create_content_crew

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the FastAPI app
app = FastAPI(
    title="Content Creator Agent API",
    description="An API to trigger a CrewAI agent for content creation.",
    version="1.0.0"
)

# Define the request body model using Pydantic
# This ensures the input data is validated
class ContentRequest(BaseModel):
    topic: str

# Define the API endpoint
@app.post("/create-content", summary="Create Content", description="Trigger the CrewAI agent to create a blog post on a given topic.")
async def create_content(request: ContentRequest):
    """
    This endpoint receives a topic, triggers the CrewAI agent,
    and returns the generated content.
    """
    try:
        logging.info(f"Received request to create content for topic: {request.topic}")
        
        # Call the synchronous crew function
        # In a real production app, you might run this in a separate thread
        # or use a task queue like Celery to avoid blocking.
        result = create_content_crew(request.topic)
        
        if not result:
            logging.error("Content creation failed. The crew returned an empty result.")
            raise HTTPException(status_code=500, detail="Content creation failed, received no output from the agent.")
            
        logging.info(f"Successfully generated content for topic: {request.topic}")
        return {"content": result}

    except Exception as e:
        # Catch any other exceptions and log them
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        # Return a generic 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")

# Add a root endpoint for health checks
@app.get("/", summary="Health Check", description="Check if the API is running.")
def read_root():
    return {"status": "ok"}


#Terminal 1: uvicorn main:app --reload
#Terminal 2: ngrok http 8000
#IMPORTANT: Copy ngrok URL
#Paste into the Google Apps Script and save
#Finish: Ctrl + C