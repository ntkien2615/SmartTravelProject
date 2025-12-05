"""Trang Trang chủ với Video Background"""
import streamlit as st
import base64
import os

@st.cache_data
def get_media_base64(filename):
    """Đọc file media (video/image) và chuyển sang base64 (có cache)"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(current_dir, "assets", "background", filename)
    
    if not os.path.exists(file_path):
        return None, None
        
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode("utf-8")
            
            ext = filename.split('.')[-1].lower()
            if ext in ['mp4', 'mov']:
                return b64, 'video/mp4'
            elif ext in ['png', 'jpg', 'jpeg']:
                return b64, f'image/{ext}'
            elif ext == 'gif':
                return b64, 'image/gif'
            else:
                return None, None
    except Exception as e:
        st.error(f"Lỗi khi đọc file {filename}: {e}")
        return None, None

def render_hero_section(filename, content_html, height="85vh", overlay_opacity=0.5):
    b64, mime = get_media_base64(filename)
    if not b64 or not mime:
        st.error(f"Không tìm thấy file {filename}")
        return

    media_html = ""
    if mime.startswith("video"):
        media_html = f"""
            <video class="video-bg" autoplay muted loop playsinline>
                <source src="data:{mime};base64,{b64}" type="{mime}">
            </video>
        """
    else:
        media_html = f"""
            <img class="video-bg" src="data:{mime};base64,{b64}" alt="Background">
        """

    st.markdown(f"""
    <div class="video-section" style="min-height: {height};">
        {media_html}
        <div class="overlay-dark" style="background: rgba(0,0,0,{overlay_opacity});"></div>
        <div class="content-box">
            {content_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_trang_chu():
    """Hiển thị nội dung trang chủ với video/image background."""
    
    # CSS Custom cho trang chủ
    st.markdown("""
    <style>
        /* Ẩn padding mặc định của block-container để video tràn viền đẹp hơn */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
            background-color: transparent !important; /* Để thấy nền tối của app */
            box-shadow: none !important;
        }
        
        .video-section {
            position: relative;
            width: 100%;
            min-height: 85vh; /* Chiều cao mỗi section */
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        
        .video-bg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 0;
        }
        
        .overlay-dark {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5); /* Lớp phủ tối để nổi bật chữ */
            z-index: 1;
        }
        
        .content-box {
            position: relative;
            z-index: 2;
            text-align: center;
            color: white;
            padding: 2rem;
            max-width: 900px;
            animation: fadeIn 1.5s ease-in-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .home-title {
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.5rem;
            text-shadow: 0 4px 10px rgba(0,0,0,0.5);
            background: linear-gradient(90deg, #60A5FA, #FFFFFF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .home-subtitle {
            font-size: 1.2rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            color: #E2E8F0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        
        .feature-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1.5rem;
            border-radius: 16px;
            margin: 10px;
            flex: 1;
            min-width: 200px;
            transition: transform 0.3s ease;
        }
        
        .feature-box:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #60A5FA;
            margin-bottom: 0.5rem;
        }
        
        .flex-row {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            justify-content: center;
            margin-top: 2rem;
        }
        
        .badge-pill {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: rgba(37, 99, 235, 0.8);
            color: white;
            border-radius: 99px;
            font-weight: 600;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- SECTION 1: HERO (City Night) ---
    render_hero_section("section-1.png", """
        <div class="badge-pill">✨ WindyAI - Smart Travel Website</div>
        <h1 class="home-title">Lên kế hoạch du lịch<br>thông minh với AI</h1>
        <p class="home-subtitle">
            Chỉ cần nhập điểm đến, ngân sách và thời gian rảnh.<br>
            Hệ thống sẽ giúp bạn tạo lịch trình <b>thông minh – nhanh chóng – tối ưu</b>.
        </p>
    """, overlay_opacity=0.5)

    # --- SECTION 2: HIGHLIGHTS (Global Connection) ---
    render_hero_section("section-2.png", """
        <h2 style="font-size: 2.5rem; margin-bottom: 2rem; font-weight: 700;">Điểm nổi bật</h2>
        <div class="flex-row">
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">⏱️</div>
                <h3>Tối ưu thời gian</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Sắp xếp lộ trình khoa học, không lo kẹt xe hay đi đường vòng.</p>
            </div>
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💸</div>
                <h3>Cân đối chi phí</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Gợi ý điểm đến phù hợp với túi tiền của bạn.</p>
            </div>
            <div class="feature-box">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧭</div>
                <h3>Dễ sử dụng</h3>
                <p style="font-size: 0.9rem; opacity: 0.9;">Giao diện thân thiện, thao tác đơn giản cho mọi lứa tuổi.</p>
            </div>
        </div>
    """, overlay_opacity=0.6)

    # --- SECTION 3: STATS (Coding/Encryption) ---
    render_hero_section("section-3.mp4", """
        <h2 style="font-size: 2.5rem; margin-bottom: 2rem; font-weight: 700;">Hiệu suất vượt trội</h2>
        <div class="flex-row">
            <div class="feature-box">
                <div class="stat-number">~ 2 phút</div>
                <div style="font-weight: 600;">Thời gian chuẩn bị</div>
            </div>
            <div class="feature-box">
                <div class="stat-number">3 – 6</div>
                <div style="font-weight: 600;">Điểm đến / ngày</div>
            </div>
            <div class="feature-box">
                <div class="stat-number">100%</div>
                <div style="font-weight: 600;">Tự động hóa</div>
            </div>
        </div>
    """, overlay_opacity=0.7)

    # --- SECTION 4: FOOTER (Clouds) ---
    render_hero_section("section-4.MP4", """
        <h2 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700;">Trải nghiệm ngay hôm nay</h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">Khám phá thế giới theo cách riêng của bạn.</p>
        <div style="font-size: 0.9rem; opacity: 0.8;">© 2025 WindyAI - Smart Travel Planner</div>
    """, height="60vh", overlay_opacity=0.3)
