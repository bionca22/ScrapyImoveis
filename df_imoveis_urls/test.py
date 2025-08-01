import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

print("Current directory:", os.getcwd())

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)



response = (
    supabase.table("teste")
    .select("*")
    .execute()
)

print(response)