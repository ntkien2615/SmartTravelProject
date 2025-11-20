"""Trang Giới thiệu"""
import streamlit as st
import base64
import os

def get_image_base64(image_path):
    """Chuyển đổi ảnh sang base64 để hiển thị trong HTML."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def page_gioi_thieu():
    """Hiển thị nội dung trang giới thiệu."""
    
    # Load logo base64
    logo_path = "./logo/Final_WindyAI_Logo_WindyAI_Logo_(RemoveBackgroud).png.png"
    logo_base64 = get_image_base64(logo_path)
    img_src = f"data:image/png;base64,{logo_base64}" if logo_base64 else "https://via.placeholder.com/150"

    # --- SECTION 1: VỀ DỰ ÁN ---
    st.markdown("<div class='section-title'>Về dự án</div>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .feature-box {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 20px;
            height: 100%;
            transition: transform 0.2s;
        }
        .feature-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-color: #2563EB;
        }
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
            color: #2563EB;
        }
        .feature-title {
            font-weight: 700;
            font-size: 1.1rem;
            color: #1E293B;
            margin-bottom: 8px;
        }
        .feature-desc {
            color: #64748B;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Grid layout cho các tính năng
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">Tối ưu hóa lộ trình</div>
            <div class="feature-desc">
                Sử dụng thuật toán thông minh để sắp xếp thứ tự các điểm đến, giúp bạn tiết kiệm thời gian và chi phí di chuyển tối đa trong chuyến đi.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🗺️</div>
            <div class="feature-title">Bản đồ tương tác</div>
            <div class="feature-desc">
                Trực quan hóa lộ trình trên bản đồ số, hỗ trợ xem chi tiết đường đi, khoảng cách và thời gian di chuyển giữa các điểm.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📍</div>
            <div class="feature-title">Gợi ý địa điểm</div>
            <div class="feature-desc">
                Hệ thống đề xuất các địa điểm du lịch hấp dẫn dựa trên sở thích, thời gian và vị trí của bạn để tạo nên trải nghiệm tốt nhất.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📅</div>
            <div class="feature-title">Lịch trình cá nhân hóa</div>
            <div class="feature-desc">
                Tạo ra lịch trình du lịch chi tiết, linh hoạt, phù hợp với nhu cầu riêng biệt của từng cá nhân hoặc nhóm du khách.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- SECTION 2: VỀ THÀNH VIÊN ---
    st.markdown("<div class='section-title'>Về thành viên</div>", unsafe_allow_html=True)
    
    # Dữ liệu thành viên
    members = [
        {"mssv": "24127486", "name": "Hoàng Cao Phong", "role": "Trưởng nhóm", "tech_role": "Project Manager & AI Engineer"},
        {"mssv": "24127294", "name": "Võ Mỹ Ngọc", "role": "Thư ký", "tech_role": "Tester & Frontend Dev"},
        {"mssv": "24127570", "name": "Võ Thúc Trí", "role": "Thành viên", "tech_role": "AI Engineer & Backend Dev"},
        {"mssv": "24127068", "name": "Nguyễn Trung Kiên", "role": "Thành viên", "tech_role": "Data Engineer & Fullstack Dev"},
        {"mssv": "24127569", "name": "Nguyễn Minh Trí", "role": "Thành viên", "tech_role": "UX & Frontend Dev"},
    ]

    # CSS cho thẻ thành viên
    st.markdown("""
    <style>
    .member-card {
        background-color: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .member-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #2563EB;
    }
    .member-avatar {
        width: 80px;
        height: 80px;
        margin: 0 auto 15px auto;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #EFF6FF;
        background-color: #F8FAFC;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .member-avatar img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 5px;
    }
    .member-name {
        font-weight: 700;
        color: #1E293B;
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .member-mssv {
        color: #64748B;
        font-size: 0.9rem;
        margin-bottom: 10px;
        font-family: monospace;
    }
    .member-role-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .role-leader {
        background-color: #DBEAFE;
        color: #1D4ED8;
    }
    .role-secretary {
        background-color: #FCE7F3;
        color: #BE185D;
    }
    .role-member {
        background-color: #F1F5F9;
        color: #475569;
    }
    .member-tech-role {
        color: #334155;
        font-size: 0.95rem;
        font-weight: 500;
        border-top: 1px solid #F1F5F9;
        padding-top: 10px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hiển thị thành viên dạng lưới (3 cột hàng trên, 2 cột hàng dưới)
    
    # Hàng 1: 3 thành viên đầu
    cols1 = st.columns(3)
    for i in range(3):
        member = members[i]
        role_class = "role-leader" if "Trưởng nhóm" in member["role"] else ("role-secretary" if "Thư ký" in member["role"] else "role-member")
        
        with cols1[i]:
            st.markdown(f"""
            <div class="member-card">
                <div class="member-avatar">
                    <img src="{img_src}" alt="Avatar"> 
                </div>
                <div class="member-name">{member['name']}</div>
                <div class="member-mssv">{member['mssv']}</div>
                <span class="member-role-badge {role_class}">{member['role']}</span>
                <div class="member-tech-role">{member['tech_role']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)

    # Hàng 2: 2 thành viên cuối (căn giữa)
    cols2 = st.columns([1, 2, 2, 1])
    
    with cols2[1]:
        member = members[3]
        role_class = "role-member"
        st.markdown(f"""
        <div class="member-card">
            <div class="member-avatar">
                 <img src="{img_src}" alt="Avatar">
            </div>
            <div class="member-name">{member['name']}</div>
            <div class="member-mssv">{member['mssv']}</div>
            <span class="member-role-badge {role_class}">{member['role']}</span>
            <div class="member-tech-role">{member['tech_role']}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with cols2[2]:
        member = members[4]
        role_class = "role-member"
        st.markdown(f"""
        <div class="member-card">
            <div class="member-avatar">
                 <img src="{img_src}" alt="Avatar">
            </div>
            <div class="member-name">{member['name']}</div>
            <div class="member-mssv">{member['mssv']}</div>
            <span class="member-role-badge {role_class}">{member['role']}</span>
            <div class="member-tech-role">{member['tech_role']}</div>
        </div>
        """, unsafe_allow_html=True)
