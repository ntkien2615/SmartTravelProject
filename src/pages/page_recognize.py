import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.constants import ALLOWED_IMAGE_TYPES

def render_recognition_page():
    """Render image recognition page."""
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 3rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h1 style="color: white; margin: 0; font-size: 3rem;">📸 Nhận diện địa điểm qua ảnh</h1>
            <p style="margin: 1rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Tải ảnh lên và để AI nhận diện địa điểm cho bạn</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: #FFF3CD;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #FFC107;
            margin: 3rem auto;
            max-width: 600px;
        ">
            <h2 style="color: #856404; margin: 0 0 1rem 0;">🚧 Đang phát triển</h2>
            <p style="color: #856404; font-size: 1.1rem; margin: 0;">Tính năng này đang được phát triển và sẽ sớm ra mắt!</p>
        </div>
    """, unsafe_allow_html=True)
    return

    st.markdown("""
        <div style="background: #E3F2FD; padding: 1rem 1.5rem; border-radius: 8px; border-left: 4px solid #2196F3; margin-bottom: 1.5rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">ℹ️</span>
            <span style="color: #424242;">Chỉ hỗ trợ định dạng JPG, PNG, JPEG</span>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Tải ảnh lên đây", type=ALLOWED_IMAGE_TYPES)

    # 📍 Vị trí chờ API (Nhận diện ảnh):
    def analyze_image_location(image_bytes):
        """Analyze image and return location (mock data for now)."""
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
            st.markdown("""
                <div style="background: #E8F5E9; padding: 1rem 1.5rem; border-radius: 8px; border-left: 4px solid #4CAF50; margin-bottom: 1.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">✅</span>
                    <span style="color: #2E7D32;"><strong>Nhận diện thành công!</strong></span>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 1.5rem;">
                    <h3 style="color: #1E88E5; margin: 0 0 0.5rem 0;">📍 {result['place_name']}</h3>
                    <p style="color: #757575; margin: 0;">Tọa độ: {result['lat']}, {result['lon']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<h4 style='color: #424242;'>Ảnh đã tải lên</h4>", unsafe_allow_html=True)
                st.image(uploaded_file, use_container_width=True)
            with col2:
                st.markdown("<h4 style='color: #424242;'>Vị trí trên bản đồ</h4>", unsafe_allow_html=True)
                st.map(pd.DataFrame({'lat': [result['lat']], 'lon': [result['lon']]}))
        else:
            st.markdown("""
                <div style="background: #FFEBEE; padding: 1rem 1.5rem; border-radius: 8px; border-left: 4px solid #F44336;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">❌</span>
                    <span style="color: #C62828;">Không thể nhận diện được địa điểm. Vui lòng thử ảnh khác.</span>
                </div>
            """, unsafe_allow_html=True)

