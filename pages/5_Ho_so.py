import streamlit as st

# Auth Guard
if not st.session_state.get('logged_in'):
    st.warning("Bạn cần đăng nhập để truy cập trang này.")
    st.switch_page("pages/2_Dang_nhap.py")
    st.stop()

st.header("Hồ sơ của bạn")

tab1, tab2 = st.tabs(["Bộ sưu tập", "Tài khoản"])

with tab1:
    st.subheader("Bộ sưu tập của bạn")
    st.write("// Hiển thị và quản lý collections và saved_places từ SQLite")

with tab2:
    st.subheader("Thông tin tài khoản")
    st.write(f"Tên người dùng: **{st.session_state.username}**")

    if st.button("Đăng xuất", type="primary", use_container_width=True):
        st.session_state.clear() # Xóa toàn bộ session
        st.switch_page("SmartTravel.py") # Về trang chủ
