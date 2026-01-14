from fastapi import FastAPI, Depends, Header, HTTPException
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")



supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)

def get_user_id(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = authorization.split(" ")[1]

    # For now we just return the token
    # Later we will extract user_id from JWT
    return token


app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    res = supabase.table("users").select("id").limit(1).execute()
    return {"data": res.data}

@app.post("/like/{to_user_id}")
def like_user(to_user_id: str, token=Depends(get_user_id)):
    pass
