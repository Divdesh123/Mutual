from fastapi import FastAPI, Depends, Header, HTTPException
import supabase
from supabase import create_client, Client

def get_user_id(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")

    jwt = authorization.split(" ")[1]

    user = supabase.auth.get_user(jwt).user

    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    return user.id

def update_type(from_user: str, to_user: str, new_type: str):
    supabase.table("requests") \
        .update({"type": new_type}) \
        .eq("from_user", from_user) \
        .eq("to_user", to_user) \
        .execute()

def set_committed(user_a: str, user_b: str):
    # user_a commits to user_b
    supabase.table("users") \
        .update({"committed_to": user_b}) \
        .eq("id", user_a) \
        .execute()
    remove_request(user_a, user_b, "like")
    # user_b commits to user_a
    supabase.table("users") \
        .update({"committed_to": user_a}) \
        .eq("id", user_b) \
        .execute()
    remove_request(user_b, user_a, "like")

def add_friends(user_a: str, user_b: str):
    supabase.table("friends").insert([{"usera": user_a, "userb": user_b},])\
        .execute()
    



def remove_request(from_user: str, to_user: str, type: str):
    supabase.table("requests") \
        .delete() \
        .eq("from_user", from_user) \
        .eq("to_user", to_user) \
        .eq("type", type) \
        .execute()

def add_request(from_user: str, to_user: str, type: str):
    supabase.table("requests") \
        .insert([{"from_user": from_user, "to_user": to_user, "type": type}]) \
        .execute()
    
def check_request(from_user: str, to_user: str, type: str):
    res = supabase.table("requests") \
        .select("*") \
        .eq("from_user", from_user) \
        .eq("to_user", to_user) \
        .eq("type", type) \
        .execute()
    return res.data