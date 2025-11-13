import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.ui_components import render_hero_section, render_feature_card, render_section_header


def render_home_page():
    """Render home page with features overview."""
    # Hero Section
    render_hero_section(
        "Chào mừng đến với SmartTravel",
        "Khám phá thế giới với SmartTravel - người bạn đồng hành thông minh cho mọi chuyến đi!",
        "✈️"
    )
    
    # Features Section
    render_section_header(
        "Tính năng nổi bật",
        "Những công cụ mạnh mẽ giúp bạn khám phá và quản lý chuyến đi",
        "⭐"
    )
    
    col1, col2, col3 = st.columns(3)
    
    render_feature_card(
        icon="🔍",
        title="Tìm kiếm thông minh",
        description="Dễ dàng tìm kiếm hàng ngàn địa điểm du lịch, nhà hàng, khách sạn với bộ lọc nâng cao.",
        col=col1
    )
    
    render_feature_card(
        icon="🤖",
        title="Nhận diện AI",
        description="Tải ảnh lên và để AI của chúng tôi nhận diện địa điểm tự động, nhanh chóng và chính xác.",
        col=col2
    )
    
    render_feature_card(
        icon="📋",
        title="Quản lý chuyến đi",
        description="Lưu trữ và tổ chức những địa điểm yêu thích, tạo bộ sưu tập cho từng chuyến đi.",
        col=col3
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional Info Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #1E88E5;
            ">
                <h3 style="color: #1E88E5; margin-bottom: 1rem;">🎯 Sứ mệnh</h3>
                <p style="color: #616161; line-height: 1.8;">
                    SmartTravel ra đời với mục tiêu giúp mọi người dễ dàng khám phá và trải nghiệm 
                    những điểm đến tuyệt vời trên khắp thế giới. Chúng tôi tin rằng công nghệ có thể 
                    làm cho du lịch trở nên đơn giản và thú vị hơn.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                border-left: 4px solid #26A69A;
            ">
                <h3 style="color: #26A69A; margin-bottom: 1rem;">💡 Công nghệ</h3>
                <p style="color: #616161; line-height: 1.8;">
                    Sử dụng trí tuệ nhân tạo (AI) và machine learning tiên tiến để cung cấp 
                    trải nghiệm cá nhân hóa. Nhận diện hình ảnh tự động và đề xuất thông minh 
                    giúp bạn tiết kiệm thời gian.
                </p>
            </div>
        """, unsafe_allow_html=True)


def render_about_page():
    """Render about page."""
    render_hero_section(
        "Giới thiệu về SmartTravel",
        "Giải pháp du lịch thông minh toàn diện",
        "🌍"
    )
    
    st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #1E88E5; margin-bottom: 1rem;">Về chúng tôi</h3>
            <p style="color: #616161; line-height: 1.8; font-size: 1.1rem;">
                SmartTravel là ứng dụng du lịch thông minh được phát triển với mục tiêu mang đến 
                trải nghiệm tốt nhất cho người dùng. Chúng tôi kết hợp công nghệ AI hiện đại với 
                giao diện thân thiện để tạo ra một nền tảng du lịch hoàn hảo.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_section_header("Chúng tôi cung cấp", icon="🎁")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: #E3F2FD; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4 style="color: #1565C0;">🔍 Khám phá</h4>
                <p style="color: #424242;">Tìm kiếm và khám phá những địa điểm mới tuyệt vời</p>
            </div>
            <div style="background: #E8F5E9; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4 style="color: #2E7D32;">📸 Nhận diện</h4>
                <p style="color: #424242;">Nhận diện các điểm đến từ ảnh bằng AI</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: #FFF3E0; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4 style="color: #EF6C00;">🗺️ Quản lý</h4>
                <p style="color: #424242;">Quản lý và tổ chức các chuyến đi của bạn</p>
            </div>
            <div style="background: #FCE4EC; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <h4 style="color: #C2185B;">💾 Lưu trữ</h4>
                <p style="color: #424242;">Lưu trữ những địa điểm yêu thích</p>
            </div>
        """, unsafe_allow_html=True)


def render_features_page():
    """Render features page."""
    render_hero_section(
        "Các tính năng",
        "Khám phá những gì SmartTravel có thể làm cho bạn",
        "🚀"
    )
    
    features = [
        {
            "icon": "🔍",
            "title": "Tìm kiếm thông minh",
            "desc": "Tìm kiếm địa điểm với các bộ lọc nâng cao (giá, loại hình, đánh giá)",
            "color": "#1E88E5"
        },
        {
            "icon": "📸",
            "title": "Nhận diện ảnh",
            "desc": "Tải ảnh lên và nhận diện địa điểm tự động bằng AI",
            "color": "#26A69A"
        },
        {
            "icon": "💾",
            "title": "Lưu bộ sưu tập",
            "desc": "Tạo và quản lý các bộ sưu tập địa điểm yêu thích",
            "color": "#FF7043"
        },
        {
            "icon": "🗺️",
            "title": "Chỉ đường",
            "desc": "Xem bản đồ và nhận hướng dẫn chỉ đường tới địa điểm",
            "color": "#FFC107"
        },
        {
            "icon": "📊",
            "title": "Thống kê",
            "desc": "Xem lịch sử tìm kiếm và phân tích xu hướng du lịch của bạn",
            "color": "#9C27B0"
        },
        {
            "icon": "🤖",
            "title": "Gợi ý AI",
            "desc": "Nhận gợi ý địa điểm phù hợp dựa trên sở thích của bạn",
            "color": "#E91E63"
        }
    ]
    
    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(features):
                feature = features[i + j]
                with col:
                    st.markdown(f"""
                        <div style="
                            background: white;
                            padding: 2rem;
                            border-radius: 12px;
                            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                            border-top: 4px solid {feature['color']};
                            margin-bottom: 1rem;
                            height: 100%;
                        ">
                            <div style="font-size: 3rem; margin-bottom: 1rem;">{feature['icon']}</div>
                            <h3 style="color: {feature['color']}; margin-bottom: 0.5rem;">{feature['title']}</h3>
                            <p style="color: #616161; line-height: 1.6;">{feature['desc']}</p>
                        </div>
                    """, unsafe_allow_html=True)

