import streamlit as st

# Đặt ở đầu mỗi file trong thư mục pages/
if not st.session_state.get('logged_in'):
    st.warning("Bạn cần đăng nhập để truy cập trang này.")
    st.switch_page("pages/2_Dang_nhap.py")
    st.stop()

st.header(f"Chào mừng trở lại, {st.session_state.username}!")

# Bố cục st.columns([2, 1]) (cột trái 60%, cột phải 40%).
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Lịch sử tìm kiếm")
    st.write("// Vị trí hiển thị lịch sử tìm kiếm từ SQLite")

    st.subheader("Các Bộ sưu tập")
    st.write("// Vị trí hiển thị các bộ sưu tập từ SQLite")

with col_right:
    st.subheader("Gợi ý cho bạn hôm nay")

    # 📍 Vị trí chờ API (Đề xuất):
    def get_ai_recommendations(user_id):
        # ---- TODO: Kết nối API thuật toán đề xuất ----
        # response = requests.get(f"api/recommend?user={user_id}")
        # return response.json()['recommendations']

        # ---- Dữ liệu giả lập (Mock data) cho UI ----
        return [
            {'name': 'Quán Phở Demo', 'img': 'url1', 'desc': 'Gợi ý vì bạn thích phở'},
            {'name': 'Cafe Yên Tĩnh', 'img': 'url2', 'desc': 'Gợi ý vì bạn tìm "yên tĩnh"'}
        ]

    recommendations = get_ai_recommendations(st.session_state['user_id'])
    for item in recommendations:
        with st.container(border=True):
            st.write(item['name'])
            st.caption(item['desc'])
