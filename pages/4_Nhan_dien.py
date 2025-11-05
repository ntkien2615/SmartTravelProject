import streamlit as st
import pandas as pd

# Auth Guard
if not st.session_state.get('logged_in'):
    st.warning("Bạn cần đăng nhập để truy cập trang này.")
    st.switch_page("pages/2_Dang_nhap.py")
    st.stop()

st.header("Nhận diện địa điểm qua ảnh")

uploaded_file = st.file_uploader("Tải ảnh lên đây", type=['jpg', 'png'])

# 📍 Vị trí chờ API (Nhận diện ảnh):
def analyze_image_location(image_bytes):
    # ---- TODO: Kết nối API nhận diện ảnh ----
    # files = {'image': image_bytes}
    # response = requests.post("api/analyze", files=files)
    # return response.json()

    # ---- Dữ liệu giả lập (Mock data) cho UI ----
    return {'status': 'success', 'place_name': 'Nhà Thờ Đức Bà (Demo)', 'lat': 10.7797, 'lon': 106.6994}

if uploaded_file:
    with st.spinner("Đang phân tích ảnh..."):
        image_data = uploaded_file.getvalue()
        result = analyze_image_location(image_data)

    if result['status'] == 'success':
        st.success(f"Kết quả: {result['place_name']}")
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Ảnh bạn tải lên")
        with col2:
            st.map(pd.DataFrame({'lat': [result['lat']], 'lon': [result['lon']]}))
    else:
        st.error("Không thể nhận diện được địa điểm.")
