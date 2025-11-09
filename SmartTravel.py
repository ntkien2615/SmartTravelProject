import streamlit as st
# from streamlit_option_menu import option_menu  # Not needed - using custom HTML nav
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.auth import render_login_page
from src.pages.page_dashboard import render_dashboard
from src.pages.page_discover import render_discover_page
from src.pages.page_home import render_home_page, render_about_page, render_features_page
from src.pages.page_recognize import render_recognition_page
from src.pages.page_profile import render_profile_page
from src.utils.db_utils import init_db
from src.utils.constants import PAGE_TITLE, PAGE_LAYOUT, PRIMARY_COLOR, BACKGROUND_COLOR

# --- Cấu hình Trang & Theme ---
st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
)

# Apply custom CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "css", "style.css")
with open(css_path, encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Additional CSS for modern navigation
st.markdown("""
    <style>
        /* === Modern Navigation Bar Styling === */
        
        /* Force white background everywhere */
        .stApp, .main, body, html {
            background-color: #FFFFFF !important;
        }
        
        /* Remove ALL black decoration bars and elements */
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        .stDeployButton,
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Force white for app view container */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }
        
        /* Remove any divs with background color set inline */
        div[style*="background-color: black"],
        div[style*="background-color: rgb(0, 0, 0)"],
        div[style*="background-color:#000"] {
            display: none !important;
        }
        
        /* Make the entire app background white - NO BLACK ANYWHERE */
        body, html, .stApp, 
        [data-testid="stAppViewContainer"],
        [data-testid="stDecoration"] {
            background-color: #FFFFFF !important;
        }
        
        /* Modern Navigation Container - Full Width Sticky */
        .main .block-container > div:first-child {
            width: 100vw !important;
            position: sticky;
            top: 0;
            left: 50% !important;
            right: 50% !important;
            margin-left: -50vw !important;
            margin-right: -50vw !important;
            padding: 0 !important;
            margin-bottom: 0 !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-bottom: 1px solid #E8E8E8;
            z-index: 1000;
            overflow: hidden !important;
        }
        
        /* Force hide any child divs after the navigation that might be black bars */
        .main .block-container > div:first-child > * {
            background-color: transparent !important;
        }
        
        .main .block-container > div:first-child::after {
            display: none !important;
        }
        
        /* Navigation content centering */
        .main .block-container > div:first-child [data-testid="stHorizontalBlock"] {
            max-width: 1400px;
            margin: 0 auto;
            padding: 8px 24px;
            background-color: #FFFFFF !important;
        }
        
        /* The vertical block containing the navigation */
        [data-testid="stVerticalBlock"]:has(iframe[title*="streamlit_option_menu"]) {
            width: 100% !important;
            padding: 0 !important;
            background-color: #FFFFFF !important;
        }
        
        /* Option menu is no longer used - using custom HTML navigation instead */
        
        /* Navigation hover effects */
        .element-container:has(iframe[title*="streamlit_option_menu"]) {
            transition: all 0.3s ease;
        }
        
        /* Remove extra spacing after navigation */
        .main .block-container {
            padding-top: 0 !important;
            max-width: 1400px;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
        
        /* Content spacing below nav */
        .main .block-container > div:first-child + div {
            margin-top: 2rem !important;
        }
        
        /* Ensure all backgrounds are transparent except nav */
        .element-container {
            background-color: transparent !important;
        }
        
        [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }
        
        /* Remove any empty divs that might create black bars */
        div:empty,
        div[style*="height: 0"],
        div[style*="width: 100%"][style*="height"] {
            display: none !important;
        }
        
        /* Specifically target and hide spacer elements */
        .main .block-container > div:first-child [data-testid="stVerticalBlock"] > div:empty,
        .main .block-container > div:first-child [data-testid="stVerticalBlock"] > div[style*="background"] {
            display: none !important;
        }
        
        /* Hide any horizontal lines/dividers */
        hr {
            display: none !important;
        }
        
        /* Hide the black decoration bar that appears below navigation */
        .main .block-container > div:first-child > div[data-testid="stVerticalBlock"] > div:last-child {
            display: none !important;
        }
        
        /* Remove all default Streamlit dividers and separators */
        [data-testid="stHorizontalBlock"] + div[style*="height"] {
            display: none !important;
        }
        
        /* Force remove any black bars or decorations */
        .main > div:first-child > div[style*="background"],
        .main > div:first-child > div[style*="black"] {
            display: none !important;
        }
        
        /* Logo and brand styling */
        .main h2 {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Modern card styling for content */
        .main .block-container > div:not(:first-child) {
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Ensure database is initialized on startup
init_db()

# --- Khởi tạo Session State với Flask backend ---
import requests as req

# Try to restore session from Flask backend
if 'session_checked' not in st.session_state:
    try:
        response = req.get('http://localhost:5000/api/session', timeout=1)
        if response.ok:
            data = response.json()
            st.session_state['logged_in'] = data.get('logged_in', False)
            st.session_state['username'] = data.get('username', '')
            st.session_state['user_id'] = data.get('user_id', None)
    except:
        # Flask backend not running, use default values
        pass
    st.session_state['session_checked'] = True

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Sync session to Flask backend whenever it changes
def sync_session_to_backend():
    """Sync Streamlit session to Flask backend"""
    try:
        req.post('http://localhost:5000/api/session', 
                json={
                    'logged_in': st.session_state.get('logged_in', False),
                    'username': st.session_state.get('username', ''),
                    'user_id': st.session_state.get('user_id', None)
                },
                timeout=1)
    except:
        pass  # Backend not available

# --- Helper function for custom navigation ---
def render_custom_nav(options, icons, active_page):
    """Render a custom navigation bar using Streamlit columns"""
    
    # Add custom CSS for modern navigation
    st.markdown(f"""
    <style>
        /* Custom Navigation Styling */
        div[data-testid="column"] {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .stButton > button {{
            width: 100%;
            background-color: transparent;
            color: #333333;
            border: 2px solid #E0E0E0 !important;
            padding: 12px 20px;
            font-size: 15px;
            font-weight: 500;
            border-radius: 8px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .stButton > button:hover {{
            background-color: #F0F2F5;
            transform: translateY(-1px);
            border: 2px solid #1877F2 !important;
            box-shadow: 0 2px 6px rgba(24, 119, 242, 0.15);
        }}
        
        .stButton > button:focus {{
            border: 2px solid {PRIMARY_COLOR} !important;
            box-shadow: 0 0 0 3px rgba(24, 119, 242, 0.1);
        }}
        
        .stButton > button[kind="primary"] {{
            background-color: {PRIMARY_COLOR} !important;
            color: #FFFFFF !important;
            border: 3px solid #0D47A1 !important;
            box-shadow: 0 3px 10px rgba(30, 136, 229, 0.4);
        }}
        
        .stButton > button[kind="primary"]:hover {{
            background-color: #0D6EFD !important;
            border: 3px solid #0A58CA !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(30, 136, 229, 0.5);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation bar with columns
    cols = st.columns(len(options))
    
    for i, (col, option, icon) in enumerate(zip(cols, options, icons)):
        with col:
            is_active = (option == active_page)
            button_type = "primary" if is_active else "secondary"
            
            # Add icon to button label
            if st.button(f"{'🏠' if icon == 'house' else '📖' if icon == 'info-circle' else '⭐' if icon == 'star' else '🔐' if icon == 'box-arrow-in-right' else '📊' if icon == 'speedometer2' else '🔍' if icon == 'search' else '📷' if icon == 'image' else '👤' if icon == 'person-circle' else '🚪'} {option}", 
                         key=f"nav_{option}", 
                         type=button_type,
                         use_container_width=True):
                st.query_params['page'] = option
                st.rerun()

# --- A. LOGIC ĐIỀU HƯỚNG (PHẦN CHÍNH) ---

# Get page from query parameters
query_params = st.query_params
current_page = query_params.get('page', 'Home')

if not st.session_state['logged_in']:
    # ---- 1. GIAO DIỆN CHƯA ĐĂNG NHẬP (NAV NGANG CÔNG KHAI) ----
    render_custom_nav(
        options=["Home", "About", "Tính năng", "Đăng nhập"],
        icons=["house", "info-circle", "star", "box-arrow-in-right"],
        active_page=current_page
    )
    
    if current_page == "Home":
        render_home_page()
    elif current_page == "About":
        render_about_page()
    elif current_page == "Tính năng":
        render_features_page()
    elif current_page == "Đăng nhập":
        render_login_page()
    else:
        render_home_page()

else:
    # ---- 2. GIAO DIỆN ĐÃ ĐĂNG NHẬP (NAV NGANG THÀNH VIÊN) ----
    # Default to Tổng quan if no page specified for logged in users
    if current_page in ["Home", "About", "Tính năng", "Đăng nhập"]:
        current_page = "Tổng quan"
    
    render_custom_nav(
        options=["Tổng quan", "Tìm đường đi", "Gợi ý", "Nhận diện", "Hồ sơ", "Đăng xuất"],
        icons=["speedometer2", "search", "star", "image", "person-circle", "box-arrow-left"],
        active_page=current_page
    )

    if current_page == "Tổng quan":
        render_dashboard(st.session_state.get('username', ''))
    elif current_page == "Tìm đường đi":
        render_discover_page()
    elif current_page == "Gợi ý":
        # Render suggestions page - under development
        st.markdown(f"""
        <div style='text-align: center; padding: 60px 20px;'>
            <h1 style='color: {PRIMARY_COLOR}; font-size: 48px; margin-bottom: 20px;'>✨ Gợi ý cho bạn</h1>
            <p style='font-size: 20px; color: #666; margin-bottom: 40px;'>Tính năng này đang được phát triển</p>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 40px; border-radius: 15px; max-width: 600px; margin: 0 auto;'>
                <p style='color: white; font-size: 18px; line-height: 1.6;'>
                    🚀 Chúng tôi đang xây dựng hệ thống gợi ý thông minh dựa trên sở thích và lịch sử của bạn.
                    <br><br>
                    Sắp ra mắt!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif current_page == "Nhận diện":
        render_recognition_page()
    elif current_page == "Hồ sơ":
        render_profile_page()
    elif current_page == "Đăng xuất":
        # Clear Flask backend session
        try:
            req.delete('http://localhost:5000/api/session', timeout=1)
        except:
            pass
        
        st.session_state.clear()
        st.session_state['logged_in'] = False
        st.query_params.clear()
        st.rerun()
    else:
        render_dashboard(st.session_state.get('username', ''))
