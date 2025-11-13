import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.ui_components import render_section_header, render_stat_card

def render_dashboard(username):
    """Render dashboard page - simplified version with welcome message only."""
    # Welcome Header
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="color: white; margin: 0;">👋 Chào mừng trở lại, {username}!</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Sẵn sàng khám phá những điểm đến mới hôm nay?</p>
        </div>
    """, unsafe_allow_html=True)

    # Under Development Message
    st.markdown("""
        <div style='text-align: center; padding: 80px 20px;'>
            <div style='font-size: 80px; margin-bottom: 20px;'>🚧</div>
            <h2 style='color: #1E88E5; margin-bottom: 15px;'>Trang Tổng quan đang được phát triển</h2>
            <p style='font-size: 18px; color: #666; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
                Chúng tôi đang xây dựng bảng điều khiển với nhiều tính năng thú vị như:
                <br><br>
                📊 Thống kê hoạt động<br>
                🕐 Lịch sử tìm kiếm<br>
                📚 Bộ sưu tập địa điểm<br>
                ✨ Gợi ý thông minh<br>
                <br>
                Vui lòng quay lại sau!
            </p>
        </div>
    """, unsafe_allow_html=True)

