"""
Database utilities for WindyAI
Using Supabase API (via supabase-py)
"""
import os
import json
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase Client
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Connected to Supabase: {SUPABASE_URL}")
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")

# ======================
# CORE FUNCTIONS
# ======================

def init_database():
    """
    Initialize database tables.
    Since we are using Supabase API, tables should be created via SQL Editor.
    """
    # Suppress noisy logs
    pass

def add_user(email, password):
    """Add a new user with hashed password"""
    if not supabase:
        return False, "Supabase not configured"
    
    try:
        # Check if user exists
        existing = supabase.table("users").select("id").eq("email", email).execute()
        if existing.data:
            return False, "Email already registered"
            
        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert new user
        data = {
            "email": email,
            "password": hashed,
            "created_at": datetime.utcnow().isoformat()
        }
        # Use returning='minimal' to avoid 556 error if permissions are tricky
        supabase.table("users").insert(data, returning='minimal').execute()
        
        # Fetch the created user to get ID
        created_user = supabase.table("users").select("id").eq("email", email).execute()
        if created_user.data:
            return True, created_user.data[0]['id']
            
        return False, "User created but ID not found"
    except Exception as e:
        print(f"Error adding user: {e}")
        return False, str(e)

def get_user(email):
    """Get user by email"""
    if not supabase:
        return None
        
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def verify_user(email, password):
    """Verify user credentials with hashed password"""
    user = get_user(email)
    if user:
        stored_password = user['password']
        # Check if password matches hash
        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True, user['id']
        except ValueError:
            # Fallback for old plain text passwords (optional, for migration)
            if stored_password == password:
                return True, user['id']
                
    return False, None

def add_schedule(user_id, destination, budget, start_time, end_time, timeline):
    """Add a new schedule for user"""
    if not supabase:
        return None
        
    try:
        # Convert timeline list to JSON string
        timeline_str = json.dumps(timeline, ensure_ascii=False)
        
        data = {
            "user_id": user_id,
            "destination": destination,
            "budget": budget,
            "start_time": start_time,
            "end_time": end_time,
            "timeline_json": timeline_str,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Use returning='minimal' to avoid 556 error
        supabase.table("schedules").insert(data, returning='minimal').execute()
        
        # Fetch the created schedule ID (assuming latest for this user)
        # This is a bit risky if multiple inserts happen at once, but acceptable for this scale
        created = supabase.table("schedules").select("id").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        
        if created.data:
            return created.data[0]['id']
        return None
    except Exception as e:
        print(f"Error adding schedule: {e}")
        return None

def get_user_schedules(user_id):
    """Get all schedules for a user"""
    if not supabase:
        return []
        
    try:
        response = supabase.table("schedules").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        
        schedules = []
        for item in response.data:
            # Parse JSON timeline
            item['timeline'] = json.loads(item['timeline_json'])
            schedules.append(item)
            
        return schedules
    except Exception as e:
        print(f"Error getting schedules: {e}")
        return []

def delete_schedule(schedule_id, user_id):
    """Delete a schedule (with user ownership check)"""
    if not supabase:
        return False
        
    try:
        # Check ownership first
        check = supabase.table("schedules").select("id").eq("id", schedule_id).eq("user_id", user_id).execute()
        if not check.data:
            return False
            
        supabase.table("schedules").delete().eq("id", schedule_id).execute()
        return True
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        return False

def migrate_from_json(json_file="database.json"):
    """Migrate data from JSON to Database (one-time migration)"""
    if not os.path.exists(json_file):
        return False, "JSON file not found"
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        users_data = data.get('users', {})
        user_data = data.get('user_data', {})
        
        # Migrate users
        email_to_id = {}
        for email, password in users_data.items():
            # Check if user exists first
            existing = get_user(email)
            if not existing:
                success, user_id = add_user(email, password)
                if success:
                    email_to_id[email] = user_id
            else:
                email_to_id[email] = existing['id']
        
        # Migrate schedules
        count_schedules = 0
        for email, udata in user_data.items():
            if email in email_to_id:
                user_id = email_to_id[email]
                schedules = udata.get('schedules', [])
                
                for schedule in schedules:
                    add_schedule(
                        user_id=user_id,
                        destination=schedule.get('destination', 'Unknown'),
                        budget=schedule.get('budget', 0),
                        start_time=schedule.get('start_time', ''),
                        end_time=schedule.get('end_time', ''),
                        timeline=schedule.get('timeline', [])
                    )
                    count_schedules += 1
        
        return True, f"Migrated users and {count_schedules} schedules successfully"
    
    except Exception as e:
        return False, f"Migration error: {str(e)}"

