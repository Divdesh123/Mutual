from fastapi import FastAPI, Depends, Header, HTTPException
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from helper import get_user_id, set_committed, update_type, add_friends, remove_request


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")



supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_KEY
)



app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    res = supabase.table("users").select("id").limit(1).execute()
    return {"data": res.data}

@app.post("/like/{to_user_id}")
def like_user(to_user_id: str, current_user=Depends(get_user_id)):
    if current_user == to_user_id:
        raise HTTPException(400, "Cannot like yourself")

    committed = supabase.table("users")\
        .select("committed_to") \
        .eq("id", current_user) \
        .execute()
    
    if committed.data and committed.data[0]["committed_to"]:
        raise HTTPException(400, "You are already committed to someone")

    # Check if already liked
    exist_like = supabase.table("requests") \
        .select("*") \
        .eq("from_user", current_user) \
        .eq("to_user", to_user_id) \
        .eq("type", "like") \
        .execute()
    
    exist_friend = supabase.table("requests") \
        .select("*") \
        .eq("from_user", current_user) \
        .eq("to_user", to_user_id) \
        .eq("type", "friend") \
        .execute()
    
    if exist_like.data:
        return {"status": "already liked"}
    elif exist_friend.data:
        supabase.table("requests") \
        .update({"type": "like"}) \
        .eq("from_user", current_user) \
        .eq("to_user", to_user_id) \
        .execute()
    else:
        supabase.table("requests") \
        .insert([{"from_user": current_user, "to_user": to_user_id, "type": "like"}]) \
        .execute()

    # Check reverse like
    reverse_like = supabase.table("requests") \
        .select("*") \
        .eq("from_user", to_user_id) \
        .eq("to_user", current_user) \
        .eq("type", "like") \
        .execute()

    if reverse_like.data:
        set_committed(current_user, to_user_id)
    
    reverse_friend = supabase.table("requests") \
        .select("*") \
        .eq("from_user", to_user_id) \
        .eq("to_user", current_user) \
        .eq("type", "friend") \
        .execute()
    
    if reverse_friend.data:
        add_friends(current_user, to_user_id)
        remove_request(current_user, to_user_id, type="friend")
            