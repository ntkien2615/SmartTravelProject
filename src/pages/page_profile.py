
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.ui_components import render_section_header

def render_profile_page():
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="color: white; margin: 0;">👤 Hồ sơ của bạn</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Quản lý thông tin và bộ sưu tập của bạn</p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Bộ sưu tập", "Tài khoản"])

    with tab1:
        render_section_header("Bộ sưu tập của bạn", "Quản lý các địa điểm đã lưu", "💾")
        
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
                <h4 style="color: #1E88E5; margin: 0 0 0.5rem 0;">🏖️ Kỳ nghỉ hè 2025</h4>
                <p style="color: #757575; font-size: 0.875rem; margin: 0 0 0.5rem 0;">12 địa điểm đã lưu</p>
                <p style="color: #9E9E9E; font-size: 0.875rem; margin: 0;">Tạo ngày 15/01/2025</p>
            </div>
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); margin-bottom: 1rem;">
                <h4 style="color: #26A69A; margin: 0 0 0.5rem 0;">🍜 Ẩm thực Việt</h4>
                <p style="color: #757575; font-size: 0.875rem; margin: 0 0 0.5rem 0;">8 địa điểm đã lưu</p>
                <p style="color: #9E9E9E; font-size: 0.875rem; margin: 0;">Tạo ngày 20/02/2025</p>
            </div>
        """, unsafe_allow_html=True)

    with tab2:
        render_section_header("Thông tin tài khoản", icon="🔐")
        
        username = st.session_state.get('username', 'Người dùng')
        
        st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                <div style="margin-bottom: 1.5rem;">
                    <label style="color: #757575; font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">Tên người dùng</label>
                    <p style="color: #212121; font-size: 1.125rem; font-weight: 500; margin: 0;">{username}</p>
                </div>
                <div style="margin-bottom: 1.5rem;">
                    <label style="color: #757575; font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">Email</label>
                    <p style="color: #212121; font-size: 1.125rem; margin: 0;">user@example.com</p>
                </div>
                <div>
                    <label style="color: #757575; font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">Thành viên từ</label>
                    <p style="color: #212121; font-size: 1.125rem; margin: 0;">01/01/2025</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
