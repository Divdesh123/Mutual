from fastapi import FastAPI
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


app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    res = supabase.table("users").select("id").limit(1).execute()
    return {"data": res.data}
