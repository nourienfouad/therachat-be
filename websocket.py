import asyncio
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from langchain_openai import OpenAI
from prompts import greeting, conversation_prompt_template, conversation_prompt, build_history_string
from auth import verify_token
from database import get_or_create_chat, insert_message_async, load_conversation_history_async
from config import OPENAI_API_KEY

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

async def websocket_endpoint(websocket: WebSocket):
    # Extract token from query parameters
    token = websocket.query_params.get("token")
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Verify token and extract user info
    try:
        user_payload = await verify_token(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    user_id = user_payload.session.user_id

    # Get or create a single persistent chat for the user
    chat_id = await get_or_create_chat(user_id=user_id)

    # Load the stored conversation history from Supabase
    history = await load_conversation_history_async(chat_id)
    await websocket.accept()

    # If no history exists, send the greeting and persist it.
    if not history:
        await websocket.send_text(greeting)
        await insert_message_async(chat_id, "agent", greeting)

    try:
        while True:
            # Wait for the user to send a message.
            user_input = await websocket.receive_text()
            user_input = user_input.strip()
            if not user_input:
                continue

            # Persist the user's message.
            await insert_message_async(chat_id, "user", user_input)

            # If user signals completion, generate final recommendation.
            if user_input.lower() == "done":
                history = await load_conversation_history_async(chat_id)
                history_str = build_history_string(history)
                final_prompt_template = conversation_prompt_template + "\nSince the user has finished providing details, please provide your final recommendation."
                final_prompt = conversation_prompt.__class__(template=final_prompt_template, input_variables=["conversation_history"])
                prompt_text = final_prompt.format(conversation_history=history_str)
                final_recommendation = llm(prompt_text).strip()
                final_recommendation = final_recommendation.replace("Agent:", "")
                await insert_message_async(chat_id, "agent", final_recommendation)
                await websocket.send_text(final_recommendation)
                break

            # Reload conversation history from the database.
            history = await load_conversation_history_async(chat_id)
            history_str = build_history_string(history)
            prompt_text = conversation_prompt.format(conversation_history=history_str)
            agent_message = llm(prompt_text).strip()
            agent_message = agent_message.replace("Agent:", "")
            await insert_message_async(chat_id, "agent", agent_message)
            await websocket.send_text(agent_message)

            if agent_message.startswith("Final Recommendation:"):
                break

    except WebSocketDisconnect:
        print("Client disconnected")
