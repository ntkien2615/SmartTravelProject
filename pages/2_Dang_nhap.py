import streamlit as st
import sqlite3
import bcrypt

# Redirect if logged in
if st.session_state.get('logged_in'):
    st.switch_page("pages/1_Dashboard.py")

st.title("Đăng nhập / Đăng ký")

tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])

# --- Login Tab ---
with tab1:
    with st.form("login_form"):
        st.subheader("Đăng nhập")
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submit_button = st.form_submit_button("Đăng nhập")

        if submit_button:
            with sqlite3.connect("smarttravel.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
                user_data = cursor.fetchone()

                if user_data:
                    user_id, db_username, password_hash = user_data
                    if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = db_username
                        st.session_state['user_id'] = user_id
                        st.success("Đăng nhập thành công!")
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error("Sai mật khẩu.")
                else:
                    st.error("Tên đăng nhập không tồn tại.")

# --- Register Tab ---
with tab2:
    with st.form("register_form"):
        st.subheader("Đăng ký tài khoản mới")
        new_username = st.text_input("Tên đăng nhập mới")
        new_password = st.text_input("Mật khẩu", type="password", key="reg_password")
        confirm_password = st.text_input("Xác nhận mật khẩu", type="password", key="reg_confirm_password")
        register_button = st.form_submit_button("Đăng ký")

        if register_button:
            if new_password != confirm_password:
                st.error("Mật khẩu xác nhận không khớp.")
            elif len(new_username) < 3:
                st.error("Tên đăng nhập phải có ít nhất 3 ký tự.")
            elif len(new_password) < 6:
                st.error("Mật khẩu phải có ít nhất 6 ký tự.")
            else:
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                try:
                    with sqlite3.connect("smarttravel.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (new_username, hashed_password))
                        conn.commit()
                    st.success("Đăng ký thành công! Vui lòng đăng nhập.")
                except sqlite3.IntegrityError:
                    st.error("Tên đăng nhập đã tồn tại.")
