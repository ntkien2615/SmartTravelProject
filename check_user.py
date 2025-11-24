import os
from dotenv import load_dotenv
from supabase import create_client

# Load env
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env")
    exit(1)

print(f"Connecting to: {url}")
supabase = create_client(url, key)

email_to_check = "test123@gmail.com"

print(f"1. Checking connection...")
try:
    # Try to select just one row to check connection
    res = supabase.table("users").select("id").limit(1).execute()
    print(f"   Table 'users' exists. Connection OK.")
except Exception as e:
    print(f"   ❌ Error checking table: {e}")

print(f"\n2. Checking user {email_to_check}...")
try:
    # Select specific columns to avoid serialization issues with weird columns
    response = supabase.table("users").select("id, email").eq("email", email_to_check).execute()
    
    if response.data:
        print("   ⚠️ FOUND USER!")
        print("   Data:", response.data)
    else:
        print("   ✅ User NOT found (Empty data).")

except Exception as e:
    print(f"   ❌ Error querying user: {e}")
    # Use getattr to avoid linter errors about unknown attributes
    details = getattr(e, 'details', None)
    code = getattr(e, 'code', None)
    
    if details:
        print(f"   Details: {details}")
    if code:
        print(f"   Code: {code}")

