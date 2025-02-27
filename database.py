import asyncio
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def insert_message(chat_id: str, role: str, content: str):
    print("Inserting message:", chat_id, role, content)
    response = supabase.table("messages").insert({
        "chatId": chat_id,
        "role": role,
        "content": content
    }).execute()
    print("Insert message response:", response)

async def insert_message_async(chat_id: str, role: str, content: str):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, insert_message, chat_id, role, content)

def create_chat(user_id: str = "unknown", title: str = "New Chat", visibility: str = "public"):
    response = supabase.table("chats").insert({
        "title": title,
        "userId": user_id,
        "visibility": visibility,
    }).execute()
    print("Create chat response:", response)
    if response.data and len(response.data) > 0:
        return response.data[0]["id"]
    return None

async def create_chat_async(user_id: str = "unknown", title: str = "New Chat", visibility: str = "public"):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, create_chat, user_id, title, visibility)

def get_chat_for_user(user_id: str):
    response = supabase.table("chats").select("*").eq("userId", user_id).execute()
    if response.data and len(response.data) > 0:
        return response.data[0]["id"]
    return None

async def get_or_create_chat(user_id: str, title: str = "New Chat", visibility: str = "public"):
    loop = asyncio.get_event_loop()
    chat_id = await loop.run_in_executor(None, get_chat_for_user, user_id)
    if not chat_id:
        chat_id = await create_chat_async(user_id=user_id, title=title, visibility=visibility)
    return chat_id

def load_conversation_history(chat_id: str):
    response = supabase.table("messages").select("*").eq("chatId", chat_id).order("created_at", desc=False).execute()
    history = []
    if response.data:
        for item in response.data:
            history.append({
                "role": item["role"],
                "message": item["content"]
            })
    return history

async def load_conversation_history_async(chat_id: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, load_conversation_history, chat_id)
