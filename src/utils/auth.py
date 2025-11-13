
import streamlit as st
import sqlite3
import bcrypt
import logging
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from constants import (
    USERNAME_MIN_LENGTH,
    PASSWORD_MIN_LENGTH,
    ERROR_INVALID_USERNAME,
    ERROR_INVALID_PASSWORD,
    ERROR_PASSWORD_MISMATCH,
    ERROR_LOGIN_FAILED,
    ERROR_USER_NOT_FOUND,
    ERROR_USER_EXISTS,
    ERROR_DB_ERROR,
    SUCCESS_LOGIN,
    SUCCESS_REGISTER,
)
from db_utils import DATABASE_NAME

logger = logging.getLogger(__name__)


def validate_username(username):
    """Validate username format."""
    if len(username) < USERNAME_MIN_LENGTH:
        return False, ERROR_INVALID_USERNAME.format(USERNAME_MIN_LENGTH)
    return True, ""


def validate_password(password):
    """Validate password format."""
    if len(password) < PASSWORD_MIN_LENGTH:
        return False, ERROR_INVALID_PASSWORD.format(PASSWORD_MIN_LENGTH)
    return True, ""


def validate_passwords_match(password, confirm_password):
    """Check if passwords match."""
    if password != confirm_password:
        return False, ERROR_PASSWORD_MISMATCH
    return True, ""


def get_user_by_username(username):
    """Fetch user from database by username."""
    try:
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return None


def authenticate_user(username, password):
    """Authenticate user with username and password."""
    user_data = get_user_by_username(username)
    
    if not user_data:
        return False, ERROR_USER_NOT_FOUND
    
    user_id, db_username, password_hash = user_data
    
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash):
        return False, ERROR_LOGIN_FAILED
    
    return True, {"id": user_id, "username": db_username}  # type: ignore


def register_user(username, password):
    """Register a new user."""
    # Validate inputs
    valid_user, user_msg = validate_username(username)
    if not valid_user:
        return False, user_msg
    
    valid_pass, pass_msg = validate_password(password)
    if not valid_pass:
        return False, pass_msg
    
    # Hash password and insert
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with sqlite3.connect(DATABASE_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        logger.info(f"User registered: {username}")
        return True, SUCCESS_REGISTER
    except sqlite3.IntegrityError:
        logger.warning(f"Duplicate username attempt: {username}")
        return False, ERROR_USER_EXISTS
    except sqlite3.Error as e:
        logger.error(f"Database error during registration: {e}")
        return False, ERROR_DB_ERROR.format(str(e))


def render_login_page():
    """Render login and registration UI."""
    st.title("Đăng nhập / Đăng ký")
    
    # Note about session persistence
    st.info("ℹ️ Lưu ý: Phiên đăng nhập sẽ tự động kết thúc khi tải lại trang (F5). Đây là hành vi bình thường của Streamlit.")

    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

    # --- Login Tab ---
    with tab1:
        with st.form("login_form"):
            st.subheader("Đăng nhập")
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit_button = st.form_submit_button("Đăng nhập")

            if submit_button:
                if not username or not password:
                    st.error("Vui lòng điền đầy đủ thông tin")
                else:
                    success, result = authenticate_user(username, password)
                    if success:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = result.get("username", "")  # type: ignore
                        st.session_state['user_id'] = result.get("id", None)  # type: ignore
                        
                        # Sync to Flask backend
                        try:
                            import requests as req
                            req.post('http://localhost:5000/api/session', 
                                    json={
                                        'logged_in': True,
                                        'username': result.get("username", ""),
                                        'user_id': result.get("id", None)
                                    },
                                    timeout=1)
                        except:
                            pass  # Backend not available
                        
                        st.success(SUCCESS_LOGIN)
                        st.rerun()
                    else:
                        st.error(result)

    # --- Register Tab ---
    with tab2:
        with st.form("register_form"):
            st.subheader("Đăng ký tài khoản mới")
            new_username = st.text_input("Tên đăng nhập mới")
            new_password = st.text_input("Mật khẩu", type="password", key="reg_password")
            confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key="reg_confirm_password")
            register_button = st.form_submit_button("Đăng ký")

            if register_button:
                if not new_username or not new_password or not confirm_password:
                    st.error("Vui lòng điền đầy đủ thông tin")
                else:
                    match_ok, match_msg = validate_passwords_match(new_password, confirm_password)
                    if not match_ok:
                        st.error(match_msg)
                    else:
                        success, message = register_user(new_username, new_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)
