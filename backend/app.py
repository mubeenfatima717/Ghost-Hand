import os
import time
from dotenv import load_dotenv
from google import genai  
from fastapi import FastAPI

# Load variables from .env
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# Initialize FastAPI app
app = FastAPI(title="Project Ghost-Hand API")
# Rate Limit logic
LAST_REQUEST_TIME = 0
REQUEST_DELAY = 4 

def safe_generate_content(prompt_text):
    global LAST_REQUEST_TIME
    
    # Rate limit check
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)
    
    response = client.models.generate_content(
        model='gemini-1.5-flash', 
        contents=prompt_text
    )
    
    LAST_REQUEST_TIME = time.time()
    return response

@app.get("/")
def home():
    return {"status": "Ghost-Hand Backend Online"}

@app.get("/test-ai")
def test_ai():
    try:
        response = safe_generate_content("Say: Ghost-Hand is ready.")
        return {"response": response.text}
    except Exception as e:
        return {"error": str(e)}