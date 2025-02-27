from fastapi import HTTPException
import stytch
from config import STYTCH_PROJECT_ID, STYTCH_SECRET

async def verify_token(token: str):
    client = stytch.Client(
        project_id=STYTCH_PROJECT_ID,
        secret=STYTCH_SECRET
    )
    try:
        payload = await client.sessions.authenticate_jwt_async(session_jwt=token)
        return payload 
    except Exception as error:
        raise HTTPException(status_code=401, detail="Invalid token")
