from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat sessions (in production, use a database)
chat_sessions = {}

class MessageRequest(BaseModel):
    message: str
    session_id: str = "default"

class MessageResponse(BaseModel):
    response: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Server is running"}

@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    print(f"Received message: {request.message}, session: {request.session_id}")
    try:
        session_id = request.session_id
        
        # Create or get existing chat session
        if session_id not in chat_sessions:
            print(f"Creating new chat session for {session_id}")
            model = genai.GenerativeModel('gemini-2.5-flash')
            chat_sessions[session_id] = model.start_chat(history=[])
            print(f"Created new chat session for {session_id}")
        
        chat = chat_sessions[session_id]
        
        # Send message directly to chatbot
        print(f"Sending message to Gemini...")
        response = chat.send_message(request.message)
        print(f"Received response: {response.text[:100]}...")
        
        return MessageResponse(response=response.text)
    
    except Exception as error:
        error_message = str(error)
        print(f"Error Type: {type(error).__name__}")
        print(f"Error Message: {error_message}")
        import traceback
        traceback.print_exc()
        
        # Check if it's a quota error
        if "quota" in error_message.lower() or "429" in error_message:
            raise HTTPException(
                status_code=429,
                detail="API quota exceeded. Please wait a moment and try again."
            )
        
        raise HTTPException(
            status_code=500,
            detail=f"Sorry, something went wrong: {error_message[:100]}"
        )

@app.delete("/chat/{session_id}")
async def clear_chat(session_id: str):
    """Clear chat history for a session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": "Chat history cleared"}
    return {"message": "Session not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
