import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import os

# SmartTravel.py (dòng đầu tiên)
st.set_page_config(
    page_title="SmartTravelProject",
    page_icon="✈️",
    layout="wide",
    # Cấu hình theme màu xanh chủ đạo
    initial_sidebar_state="expanded"
)

# Apply custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Database Initialization
DATABASE_NAME = "smarttravel.db"

def init_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saved_places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_id INTEGER,
                place_name TEXT,
                address TEXT,
                image_url TEXT,
                latitude REAL,
                longitude REAL,
                FOREIGN KEY (collection_id) REFERENCES collections(id)
            )
        """)
        conn.commit()

# Ensure database is initialized on startup
init_db()

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Redirect if logged in
if st.session_state.get('logged_in'):
    st.switch_page("pages/1_Dashboard.py")

# Public Homepage UI
st.title("Chào mừng đến với SmartTravelProject ✈️")

st.write("Khám phá thế giới với SmartTravelProject - người bạn đồng hành thông minh cho mọi chuyến đi!")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("https://via.placeholder.com/150/0000FF/FFFFFF?text=Search", caption="Tìm kiếm địa điểm")
    st.subheader("Tìm kiếm thông minh")
    st.write("Dễ dàng tìm kiếm hàng ngàn địa điểm du lịch, nhà hàng, khách sạn.")

with col2:
    st.image("https://via.placeholder.com/150/FF0000/FFFFFF?text=AI+Detect", caption="Nhận diện địa điểm")
    st.subheader("Nhận diện AI")
    st.write("Tải ảnh lên và để AI của chúng tôi nhận diện địa điểm cho bạn.")

with col3:
    st.image("https://via.placeholder.com/150/00FF00/FFFFFF?text=Plan+Trip", caption="Lên kế hoạch chuyến đi")
    st.subheader("Lên kế hoạch")
    st.write("Lưu lại những địa điểm yêu thích và tạo bộ sưu tập cho chuyến đi của bạn.")

st.markdown("---")

st.subheader("Bắt đầu hành trình của bạn ngay hôm nay!")
login_col, register_col = st.columns(2)

with login_col:
    if st.button("Đăng nhập", type="primary", use_container_width=True):
        st.switch_page("pages/2_Dang_nhap.py")

with register_col:
    if st.button("Đăng ký", use_container_width=True):
        st.switch_page("pages/2_Dang_nhap.py")
