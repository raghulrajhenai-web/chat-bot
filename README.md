# AI Chatbot 🤖

A simple chatbot application built with FastAPI and Google's Gemini AI, featuring a beautiful HTML frontend and chat history support.

## Features

- ✨ Beautiful and responsive UI
- 💬 Real-time chat with Gemini AI
- 📝 Chat history persistence (per session)
- 🤖 Intelligent AI responses
- 🚀 FastAPI backend
- 🎨 Modern gradient design

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key and paste it in your `.env` file

### 4. Run the Application

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

### 5. Open in Browser

Navigate to: `http://localhost:8000`

## API Endpoints

- `GET /` - Serves the HTML frontend
- `POST /chat` - Send a message to the chatbot
  ```json
  {
    "message": "Hello!",
    "session_id": "user_123"
  }
  ```
- `DELETE /chat/{session_id}` - Clear chat history for a session

## Project Structure

```
chat-bot/
├── main.py              # FastAPI backend
├── index.html           # Frontend UI
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .env.example         # Example environment file
└── README.md           # This file
```

## Technologies Used

- **Backend**: FastAPI, Python
- **AI**: Google Gemini AI (gemini-2.0-flash-exp)
- **Frontend**: HTML, CSS, JavaScript
- **Environment**: python-dotenv

## Features Explained

### Chat History
The chatbot maintains conversation history within each session using Gemini's chat functionality. This allows for contextual responses based on previous messages.

### Session Management
Each user gets a unique session ID, allowing multiple users to chat simultaneously without interference.

## Customization

You can customize the chatbot by modifying the Gemini model or adding system instructions in `main.py`.

## Troubleshooting

- **API Key Error**: Make sure your `.env` file has the correct Gemini API key
- **Port Already in Use**: Change the port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- **Module Not Found**: Install dependencies with `pip install -r requirements.txt`

## License

MIT License - feel free to use and modify!