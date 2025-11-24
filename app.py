import streamlit as st
from datetime import time
# from streamlit_option_menu import option_menu  # Replaced with custom navigation
import json
import os
import db_utils  # SQLite database utilities
import utils  # Utility functions
import extra_streamlit_components as stx

# Import page modules
from pages.page_trang_chu import page_trang_chu
from pages.page_gioi_thieu import page_gioi_thieu
from pages.page_chuc_nang import page_chuc_nang
from pages.page_ho_so import page_ho_so
from pages.page_sign_in_up import page_sign_in_up

st.set_page_config(
    page_title="WindyAI - Smart Travel Website",
    page_icon="./logo/Final_WindyAI_Logo_WindyAI_Logo_(RemoveBackgroud).png.png",
    layout="wide",  
    initial_sidebar_state="collapsed"
)

# ======================
# COOKIE MANAGER SETUP
# ======================
# Initialize Cookie Manager
if 'cookie_manager' not in st.session_state:
    st.session_state.cookie_manager = stx.CookieManager()

cookie_manager = st.session_state.cookie_manager

# ======================
# DATABASE INITIALIZATION
# ======================
# Initialize database on first run
db_utils.init_database()

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "latest_schedule" not in st.session_state:
    st.session_state["latest_schedule"] = None

# Check for login cookie if not logged in
if not st.session_state.get("current_user"):
    # Get all cookies
    cookies = cookie_manager.get_all()
    user_email_cookie = cookies.get("user_email")
    
    if user_email_cookie:
        # Verify user exists in DB
        user = db_utils.get_user(user_email_cookie)
        if user and isinstance(user, dict):
            st.session_state["current_user"] = user.get("email")
            st.session_state["user_id"] = user.get("id")
            # st.toast(f"👋 Chào mừng trở lại, {user['email']}!", icon="🎉")

def load_css(file_name):
    """Tải file CSS để áp dụng vào ứng dụng."""
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ======================
# CUSTOM NAVIGATION FUNCTION
# ======================
def render_custom_nav(options, icons, active_page):
    """Render custom navigation bar using Streamlit buttons with CSS styling"""
    
    # Add custom CSS for navigation buttons
    st.markdown("""
    <style>
        /* Navigation Container */
        div[data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Base Button Style - với màu chữ đen để thấy rõ trên nền trắng */
        .stButton > button {
            width: 100%;
            background-color: transparent;
            color: #0F172A !important;
            border: 2px solid #CBD5E1 !important;
            padding: 0.6rem 1.2rem;
            font-size: 0.95rem;
            font-weight: 500;
            border-radius: 0.75rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        /* Hover State */
        .stButton > button:hover {
            background-color: #EFF6FF;
            border: 2px solid #2563EB !important;
            color: #1D4ED8 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        /* Focus State */
        .stButton > button:focus {
            border: 2px solid #2563EB !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            color: #1D4ED8 !important;
        }
        
        /* Active/Selected Button */
        .stButton > button[kind="primary"] {
            background-color: transparent !important;
            color: #2563EB !important;
            border: none !important;
            border-bottom: 3px solid #2563EB !important;
            border-radius: 0 !important;
            font-weight: 600 !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #EFF6FF !important;
            color: #1D4ED8 !important;
            transform: translateY(-1px);
        }
        
        /* Fix button text - ensure no <p> tags styling issues */
        .stButton > button p {
            color: inherit !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stButton > button[kind="primary"] p {
            color: #2563EB !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation bar
    cols = st.columns(len(options))
    
    # Icon mapping
    icon_map = {
        "house": "🏠",
        "info-circle": "ℹ️",
        "check2-square": "✅",
        "calendar-check": "📅",
        "person-circle": "👤",
        "person-badge": "👤"
    }
    
    for i, (col, option, icon) in enumerate(zip(cols, options, icons)):
        with col:
            is_active = (option == active_page)
            button_type = "primary" if is_active else "secondary"
            icon_emoji = icon_map.get(icon, "📌")
            
            if st.button(f"{icon_emoji} {option}", 
                         key=f"nav_{option}_{i}", 
                         type=button_type,
                         use_container_width=True):
                st.session_state['current_page'] = option
                st.rerun()

# ======================
# BIẾN CẤU HÌNH MENU (Legacy - không dùng nữa)
# ======================
MENU_STYLES = {
    "container": {
        "padding": "0.4rem 1.2rem",
        "background-color": "#FFFFFF",
        "border": "2px solid #2563EB",
        "border-radius": "999px",
        "margin-bottom": "1.2rem",
        "margin-left": "1rem",
        "margin-right": "1rem",
    },
    "nav-link": {
        "font-size": "0.95rem",
        "font-weight": "500",
        "color": "#0F172A",
        "background-color": "transparent",
        "border-radius": "0.5rem",
        "margin": "0.2rem 0.2rem",
        "text-align": "center",
        "padding": "0.6rem 1.2rem",
        "--hover-color": "#EFF6FF",
    },
    "nav-link-selected": {
        "background-color": "transparent",
        "color": "#2563EB",
        "font-weight": "600",
        "border-radius": "0",
        "border-bottom": "3px solid #2563EB",
    },
    "icon": {
        "font-size": "1.1rem",
        "margin-right": "0.45rem",
    },
}

# ======================
# DATABASE INITIALIZATION (SQLite)
# ======================
# Initialize database on first run
# db_utils.init_database() -> Moved up

# Initialize session state -> Moved up


# Legacy JSON database functions (kept for compatibility, can be removed later)
DB_FILE = "database.json"

def load_database():
    """Load database from JSON (legacy - for migration only)"""
    if not os.path.exists(DB_FILE):
        return {"users": {}, "user_data": {}}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": {}, "user_data": {}}

# One-time migration from JSON to SQLite (if needed)
if 'db_migrated' not in st.session_state:
    if os.path.exists(DB_FILE):
        success, message = db_utils.migrate_from_json(DB_FILE)
        if success:
            st.toast(f"✅ {message}", icon="✅")
            # Rename old JSON file to backup
            os.rename(DB_FILE, DB_FILE + ".backup")
    st.session_state['db_migrated'] = True

# ======================
# Hàm tiện ích
# ======================
def time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def minutes_to_str(m: int) -> str:
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.image("./logo/Final_WindyAI_Logo_WindyAI_Logo_(RemoveBackgroud).png.png", width=120)
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.sidebar.caption("© 2025 WindyAI")

# ======================================================
# THANH ĐIỀU HƯỚNG VÀ ROUTING
# ======================================================

# Initialize current_page in session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Trang chủ"

if st.session_state.get("current_user"):
    menu_options = ["Trang chủ", "Giới thiệu", "Chức năng", "Hồ sơ"]
    menu_icons = ["house", "info-circle", "check2-square", "person-badge"]
else:
    menu_options = ["Trang chủ", "Giới thiệu", "Chức năng", "Sign in / Sign up"]
    menu_icons = ["house", "info-circle", "check2-square", "person-circle"]

# Add CSS for navigation with logo
st.markdown("""
<style>
    /* Base Button Style */
    .stButton > button {
        width: 100%;
        background-color: transparent;
        color: #0F172A !important;
        border: 2px solid #CBD5E1 !important;
        padding: 0.6rem 1.2rem;
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 0.75rem;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 50px;
    }
    
    /* Hover State */
    .stButton > button:hover {
        background-color: #EFF6FF;
        border: 2px solid #2563EB !important;
        color: #1D4ED8 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Active/Selected Button */
    .stButton > button[kind="primary"] {
        background-color: transparent !important;
        color: #2563EB !important;
        border: none !important;
        border-bottom: 3px solid #2563EB !important;
        border-radius: 0 !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #EFF6FF !important;
        color: #1D4ED8 !important;
    }
    
    /* Fix button text - căn giữa theo chiều dọc */
    .stButton > button p {
        color: inherit !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.5;
    }
    
    .stButton > button[kind="primary"] p {
        color: #2563EB !important;
    }
</style>
""", unsafe_allow_html=True)

# CSS cho navigation bar với viền
st.markdown("""
<style>
    /* Căn giữa logo và nav buttons theo chiều dọc */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Viền cho navigation container - sử dụng :has() selector để target chính xác block chứa marker */
    div[data-testid="stHorizontalBlock"]:has(div.nav-marker) {
        border: 2px solid #2563EB;
        border-radius: 12px;
        padding: 0.8rem 1.2rem;
        background-color: #FFFFFF;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
        margin-bottom: 1.5rem;
        align-items: center; /* Căn giữa theo chiều dọc */
    }
    
    /* Ẩn marker */
    div.nav-marker {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

nav_cols = st.columns([0.18] + [0.82 / len(menu_options)] * len(menu_options))

# Logo ở cột đầu tiên
with nav_cols[0]:
    # Marker để CSS target đúng block này
    st.markdown('<div class="nav-marker"></div>', unsafe_allow_html=True)
    
    # Load logo base64
    logo_path = "./logo/Final_WindyAI_Logo_WindyAI_Logo_(RemoveBackgroud).png.png"
    logo_base64 = utils.get_image_base64(logo_path)
    img_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""
    
    # Render logo centered with HTML
    st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <img src="{img_src}" width="100" style="display: block; margin-bottom: 15px;">
        </div>
    """, unsafe_allow_html=True)

# Navigation buttons ở các cột còn lại
icon_map = {
    "house": "🏠",
    "info-circle": "ℹ️",
    "check2-square": "✅",
    "person-circle": "👤",
    "person-badge": "👤"
}

for i, (option, icon) in enumerate(zip(menu_options, menu_icons)):
    with nav_cols[i + 1]:
        is_active = (option == st.session_state['current_page'])
        button_type = "primary" if is_active else "secondary"
        icon_emoji = icon_map.get(icon, "📌")
        
        if st.button(f"{icon_emoji} {option}", 
                     key=f"nav_{option}_{i}", 
                     type=button_type,
                     use_container_width=True):
            st.session_state['current_page'] = option
            st.rerun()

# Get current page
page = st.session_state['current_page']

# ======================
# BỘ ĐIỀU HƯỚNG TRANG
# ======================
page_container = st.container()

with page_container:
    if page == "Trang chủ":
        page_trang_chu()
    elif page == "Giới thiệu":
        page_gioi_thieu()
    elif page == "Chức năng":
        page_chuc_nang()
    elif page == "Hồ sơ":
        page_ho_so()
    elif page == "Sign in / Sign up":
        page_sign_in_up()

