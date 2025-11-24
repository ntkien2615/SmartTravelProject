"""Trang Đăng nhập / Đăng ký"""
import streamlit as st
import db_utils


def page_sign_in_up():
    """Hiển thị nội dung trang Đăng nhập / Đăng ký."""
    st.markdown("<div class='section-title'>Đăng nhập / Đăng ký</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Quản lý tài khoản để lưu lại các lịch trình yêu thích của bạn.</div>",
        unsafe_allow_html=True,
    )

    tab_signin, tab_signup = st.tabs(["Sign in", "Sign up"])

    # SIGN IN
    with tab_signin:
        with st.form("signin_form"):
            email_in = st.text_input("Email", key="signin_email")
            password_in = st.text_input("Password", type="password", key="signin_pass")
            submitted_in = st.form_submit_button("Sign in")

        if submitted_in:
            if not email_in or not password_in:
                st.error("Vui lòng nhập đầy đủ Email và Password.")
            else:
                # Verify using SQLite
                success, user_id = db_utils.verify_user(email_in, password_in)
                if success:
                    st.session_state["current_user"] = email_in
                    st.session_state["user_id"] = user_id
                    st.session_state["current_page"] = "Trang chủ"  # Chuyển về trang chủ
                    
                    # Set cookie (expires in 7 days)
                    if 'cookie_manager' in st.session_state:
                        st.session_state.cookie_manager.set("user_email", email_in, key="set_login_cookie")
                    
                    st.success(f"Đăng nhập thành công! Xin chào **{email_in}** 🎉")
                    st.rerun()
                else:
                    st.error("Email hoặc mật khẩu không đúng.")

    # SIGN UP
    with tab_signup:
        with st.form("signup_form"):
            email_up = st.text_input("Email", key="signup_email")
            password_up = st.text_input("Password", type="password", key="signup_pass")
            confirm_up = st.text_input("Confirm password", type="password", key="signup_confirm")
            submitted_up = st.form_submit_button("Sign up")

        if submitted_up:
            if not email_up or not password_up or not confirm_up:
                st.error("Vui lòng nhập đầy đủ Email và Password.")
            elif "@" not in email_up:
                st.error("Email không hợp lệ.")
            elif password_up != confirm_up:
                st.error("Password nhập lại không khớp.")
            else:
                # Add user using Supabase
                success, result = db_utils.add_user(email_up, password_up)
                if success:
                    user_id = result
                    # Tự động đăng nhập sau khi đăng ký thành công
                    st.session_state["current_user"] = email_up
                    st.session_state["user_id"] = user_id
                    st.session_state["current_page"] = "Trang chủ"  # Chuyển về trang chủ
                    
                    # Set cookie
                    if 'cookie_manager' in st.session_state:
                        st.session_state.cookie_manager.set("user_email", email_up, key="set_signup_cookie")
                        
                    st.success(f"Đăng ký thành công! Xin chào **{email_up}** 🎉")
                    st.rerun()
                else:
                    # result contains error message if success is False
                    if result and "already registered" in str(result):
                         st.error("Email này đã được đăng ký.")
                    else:
                         st.error(f"Lỗi đăng ký: {result if result else 'Email đã tồn tại hoặc lỗi hệ thống'}")
