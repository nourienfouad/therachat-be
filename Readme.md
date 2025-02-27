# Mental Well-being Recommendation Chatbot

This project is a FastAPI application that provides a real-time conversation interface between users and an AI-driven mental health chatbot advisor. It uses a WebSocket endpoint to communicate with users, leverages LangChain/OpenAI for generating conversational responses, and integrates Stytch for token-based authentication. Conversation history is persisted in a Supabase database, ensuring that each user has a single, continuous chat session.

## Features

- **Real-Time WebSocket Communication:**  
  Enables live chat between the user and the agent.
  
- **AI-Driven Responses:**  
  Uses OpenAI (via LangChain) to generate context-aware messages based on the conversation history.
  
- **Authentication:**  
  Utilizes Stytch for JWT authentication to secure the WebSocket connection.
  
- **Persistent Conversation History:**  
  Stores chat sessions and messages in Supabase. Each user has a single persistent chat that serves as the conversation history.
  
- **Final Recommendation and Rating:**  
  When the user signals the end of the conversation (by typing "done"), the agent generates a final recommendation and a rating.

## Project Structure

\`\`\`
my_project/
├── main.py                # Application entry point
├── config.py              # Environment variable configuration
├── auth.py                # Authentication logic using Stytch
├── database.py            # Supabase integration for chats and messages
├── prompts.py             # Prompt templates and helper functions for conversation
├── websocket.py           # WebSocket endpoint implementation
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation (this file)
\`\`\`

## Installation

1. **Clone the Repository:**

   \`\`\`bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   \`\`\`

2. **Create and Activate a Virtual Environment (Optional but recommended):**

   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   \`\`\`

3. **Install Dependencies:**

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Configure Environment Variables:**

   Create a \`.env\` file in the root of your project with the following variables:

   \`\`\`env
   OPENAI_API_KEY=your_openai_api_key
   STYTCH_SECRET=your_stytch_secret
   STYTCH_PROJECT_ID=your_stytch_project_id
   SUPABASE_URL=https://your-supabase-url.supabase.co
   SUPABASE_KEY=your_supabase_anon_key
   \`\`\`

## Running the Application

To start the FastAPI server with automatic reloading (for development):

\`\`\`bash
uvicorn main:app --reload
\`\`\`

The application will be accessible at [http://localhost:8000](http://localhost:8000). The WebSocket endpoint is available at \`ws://localhost:8000/ws\`.

## Usage

- **WebSocket Connection:**  
  Clients must supply a valid JWT token (stored, for example, in cookies) as a query parameter when connecting to the WebSocket endpoint:
  
  \`\`\`
  ws://localhost:8000/ws?token=your_jwt_token
  \`\`\`
  
- **Chat Interaction:**  
  When a client connects:
  - If no conversation history exists, the agent sends a greeting.
  - If previous messages exist, the stored conversation is loaded and sent to the client.
  - The agent generates a response only after the user sends a message.
  - Typing "done" triggers the generation of a final recommendation.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests with improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
