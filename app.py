import streamlit as st
from datetime import time
# from streamlit_option_menu import option_menu  # Replaced with custom navigation
import json
import os
import db_utils  # SQLite database utilities

st.set_page_config(
    page_title="Smart 1-Day Trip Planner",
    layout="wide",  
    initial_sidebar_state="collapsed"
)

def load_css(file_name):
    """Tải file CSS để áp dụng vào ứng dụng."""
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ======================
# CUSTOM NAVIGATION FUNCTION
# ======================
def render_custom_nav(options, icons, active_page):
    """Render custom navigation bar using Streamlit buttons with CSS styling"""
    
    # Add custom CSS for navigation buttons
    st.markdown("""
    <style>
        /* Navigation Container */
        div[data-testid="column"] {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Base Button Style - với màu chữ đen để thấy rõ trên nền trắng */
        .stButton > button {
            width: 100%;
            background-color: transparent;
            color: #0F172A !important;
            border: 2px solid #CBD5E1 !important;
            padding: 0.6rem 1.2rem;
            font-size: 0.95rem;
            font-weight: 500;
            border-radius: 0.75rem;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        /* Hover State */
        .stButton > button:hover {
            background-color: #EFF6FF;
            border: 2px solid #2563EB !important;
            color: #1D4ED8 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        }
        
        /* Focus State */
        .stButton > button:focus {
            border: 2px solid #2563EB !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            color: #1D4ED8 !important;
        }
        
        /* Active/Selected Button */
        .stButton > button[kind="primary"] {
            background-color: transparent !important;
            color: #2563EB !important;
            border: none !important;
            border-bottom: 3px solid #2563EB !important;
            border-radius: 0 !important;
            font-weight: 600 !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #EFF6FF !important;
            color: #1D4ED8 !important;
            transform: translateY(-1px);
        }
        
        /* Fix button text - ensure no <p> tags styling issues */
        .stButton > button p {
            color: inherit !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stButton > button[kind="primary"] p {
            color: #2563EB !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create navigation bar
    cols = st.columns(len(options))
    
    # Icon mapping
    icon_map = {
        "house": "🏠",
        "info-circle": "ℹ️",
        "check2-square": "✅",
        "calendar-check": "📅",
        "person-circle": "👤",
        "person-badge": "👤"
    }
    
    for i, (col, option, icon) in enumerate(zip(cols, options, icons)):
        with col:
            is_active = (option == active_page)
            button_type = "primary" if is_active else "secondary"
            icon_emoji = icon_map.get(icon, "📌")
            
            if st.button(f"{icon_emoji} {option}", 
                         key=f"nav_{option}_{i}", 
                         type=button_type,
                         use_container_width=True):
                st.session_state['current_page'] = option
                st.rerun()

# ======================
# BIẾN CẤU HÌNH MENU (Legacy - không dùng nữa)
# ======================
MENU_STYLES = {
    "container": {
        "padding": "0.4rem 1.2rem",
        "background-color": "#FFFFFF",
        "border": "2px solid #2563EB",
        "border-radius": "999px",
        "margin-bottom": "1.2rem",
        "margin-left": "1rem",
        "margin-right": "1rem",
    },
    "nav-link": {
        "font-size": "0.95rem",
        "font-weight": "500",
        "color": "#0F172A",
        "background-color": "transparent",
        "border-radius": "0.5rem",
        "margin": "0.2rem 0.2rem",
        "text-align": "center",
        "padding": "0.6rem 1.2rem",
        "--hover-color": "#EFF6FF",
    },
    "nav-link-selected": {
        "background-color": "transparent",
        "color": "#2563EB",
        "font-weight": "600",
        "border-radius": "0",
        "border-bottom": "3px solid #2563EB",
    },
    "icon": {
        "font-size": "1.1rem",
        "margin-right": "0.45rem",
    },
}

# ======================
# DATABASE INITIALIZATION (SQLite)
# ======================
# Initialize database on first run
db_utils.init_database()

# Initialize session state
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "latest_schedule" not in st.session_state:
    st.session_state["latest_schedule"] = None

# Legacy JSON database functions (kept for compatibility, can be removed later)
DB_FILE = "database.json"

def load_database():
    """Load database from JSON (legacy - for migration only)"""
    if not os.path.exists(DB_FILE):
        return {"users": {}, "user_data": {}}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": {}, "user_data": {}}

# One-time migration from JSON to SQLite (if needed)
if 'db_migrated' not in st.session_state:
    if os.path.exists(DB_FILE):
        success, message = db_utils.migrate_from_json(DB_FILE)
        if success:
            st.toast(f"✅ {message}", icon="✅")
            # Rename old JSON file to backup
            os.rename(DB_FILE, DB_FILE + ".backup")
    st.session_state['db_migrated'] = True

# ======================
# Hàm tiện ích
# ======================
def time_to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute

def minutes_to_str(m: int) -> str:
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.sidebar.caption("© 2025 Smart 1-Day Trip Planner")

# ======================================================
# CÁC HÀM XỬ LÝ CÁC TRANG
# ======================================================

def page_trang_chu():
    """Hiển thị nội dung trang chủ."""
    col_text, col_image = st.columns([1.05, 1], gap="large")
    with col_text:
        st.markdown(
            "<div class='badge-pill'>✨ Smart 1-Day Trip Planner</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <h1 class='home-title'
                style='font-size: 3.4rem; font-weight: 750; line-height: 1.15; margin-bottom: 1.2rem; margin-top: 1.2rem;'>
                1 CÂU GIỚI THIỆU.
            </h1>
            """,
            unsafe_allow_html=True,
        )
        st.write(
            "Chỉ cần nhập điểm đến, ngân sách và thời gian rảnh, hệ thống sẽ giúp bạn tạo lịch trình "
            "du lịch **thông minh – nhanh chóng – tối ưu** cho một ngày."
        )

        st.markdown("#### Điểm nổi bật")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("⏱️ Tối ưu thời gian")
        with c2:
            st.caption("💸 Cân đối chi phí")
        with c3:
            st.caption("🧭 Dễ dùng cho mọi người")

        st.markdown("")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Thời gian chuẩn bị</div>
                    <div class='home-stat-value'>~ 2 phút</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Số điểm đến trong ngày</div>
                    <div class='home-stat-value'>3 – 6 điểm</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s3:
            st.markdown(
                """
                <div class='home-stat-card'>
                    <div class='home-stat-label'>Trải nghiệm</div>
                    <div class='home-stat-value'>Thoải mái</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with col_image:
        st.image(
            "https_images.unsplash.com/photo-1500835556837-99ac94a94552?w=900&auto=format&fit=crop&q=60"
            .replace("_", "://"),
            use_container_width=True,
            output_format="PNG",
        )

def page_gioi_thieu():
    """Hiển thị nội dung trang giới thiệu."""
    st.markdown("<div class='section-title'>Giới thiệu đề tài</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Tổng quan ngắn gọn về hệ thống du lịch thông minh tối ưu hóa lịch trình trong 1 ngày.</div>",
        unsafe_allow_html=True,
    )
    st.write(
        """Thông tin các tv""")

def page_chuc_nang():
    """Hiển thị nội dung trang chức năng - bao gồm Tìm kiếm nhanh và 3 chức năng phụ."""
    st.markdown("<div class='section-title'>Chức năng chính</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Tìm kiếm nhanh hoặc khám phá các chức năng hỗ trợ du lịch thông minh.</div>",
        unsafe_allow_html=True,
    )
    
    # ===== PHẦN 1: TÌM KIẾM NHANH (LÊN LỊCH TRÌNH) =====
    st.markdown("### 🔍 Tìm kiếm nhanh")
    st.markdown(
        "<p style='color: #64748B; margin-bottom: 1.5rem;'>Form minh họa cách người dùng nhập thông tin. Kết quả hiện tại chỉ là mô phỏng, chưa có thuật toán tối ưu thực tế.</p>",
        unsafe_allow_html=True,
    )

    col_form, col_result = st.columns([1.1, 1], gap="large")
    with col_form:
        st.markdown("#### 📝 Nhập thông tin chuyến đi")
        with st.form("quick_search_form"):
            start_location = st.text_input("Điểm xuất phát", value="Quận 1, TP.HCM")
            destinations_text = st.text_area(
                "Danh sách điểm muốn đến (mỗi dòng một địa điểm)",
                value="Nhà thờ Đức Bà\nPhố đi bộ Nguyễn Huệ\nLandmark 81",
                height=150,
            )
            food_text = st.text_area(
                "Danh sách món ăn / quán ăn muốn thử (mỗi dòng một món hoặc một quán)",
                value="Phở bò\nBánh mì thịt\nTrà sữa\nHủ tiếu",
                height=120,
            )
            c1, c2 = st.columns(2)
            with c1:
                start_time = st.time_input("Giờ bắt đầu", value=time(8, 0))
            with c2:
                end_time = st.time_input("Giờ kết thúc", value=time(20, 0))
            budget = st.number_input(
                "Ngân sách tối đa (VND)",
                min_value=0,
                value=800000,
                step=50000,
            )
            submitted = st.form_submit_button("Tạo lịch trình ")

        if not submitted:
            st.caption("⏳ Nhập xong và bấm **Tạo lịch trình** để xem kết quả.")
            st.session_state["latest_schedule"] = None

    with col_result:
        st.markdown("#### 📆 Kết quả lịch trình")
        if not submitted:
            st.info(
                "Kết quả sẽ hiển thị ở đây sau khi bạn bấm nút. "
            )
        else:
            dest_lines = [line.strip() for line in destinations_text.splitlines() if line.strip()]
            food_lines = [line.strip() for line in food_text.splitlines() if line.strip()]

            if not dest_lines:
                st.error("Vui lòng nhập ít nhất 1 điểm đến.")
            else:
                start_min = time_to_minutes(start_time)
                end_min = time_to_minutes(end_time)
                if end_min <= start_min:
                    st.warning("Giờ kết thúc phải lớn hơn giờ bắt đầu. Đang dùng mặc định 08:00 – 20:00.")
                    start_min = 8 * 60
                    end_min = 20 * 60

                total_minutes = end_min - start_min
                block = max(total_minutes // len(dest_lines), 30)
                current = start_min

                st.write(f"**Điểm xuất phát:** {start_location}")
                st.write(f"**Thời gian tổng:** {minutes_to_str(start_min)} – {minutes_to_str(end_min)}")
                st.write(f"**Ngân sách tối đa:** {budget:,} VND")
                st.markdown("---")
                st.write("**⏱️ Timeline gợi ý**")

                schedule_data = {
                    "id": f"{start_min}-{len(dest_lines)}",
                    "start_location": start_location,
                    "destinations": dest_lines,
                    "food": food_lines,
                    "start_time": minutes_to_str(start_min),
                    "end_time": minutes_to_str(end_min),
                    "budget": budget,
                    "timeline": [],
                }

                for i, place in enumerate(dest_lines, start=1):
                    arrive = current
                    depart = min(current + block, end_min)
                    current = depart
                    schedule_data["timeline"].append(
                        {
                            "place": place,
                            "arrive": minutes_to_str(arrive),
                            "depart": minutes_to_str(depart),
                        }
                    )
                    with st.expander(
                        f"📍 {i}. {place} ({minutes_to_str(arrive)} – {minutes_to_str(depart)})"
                    ):
                        st.write(f"**Thời gian:** {minutes_to_str(arrive)} – {minutes_to_str(depart)}")
                        st.write("**Hoạt động:** Tham quan, chụp ảnh, nghỉ ngơi.")
                        st.write(f"**Chi phí gợi ý:** {budget // len(dest_lines):,} VND")

                if food_lines:
                    st.markdown("---")
                    st.write("**🍜 Món ăn gợi ý**")
                    for food in food_lines:
                        st.write(f"- {food}")

                st.session_state["latest_schedule"] = schedule_data

                # Save button (only if logged in)
                if st.session_state.get("current_user"):
                    st.markdown("---")
                    col_save, col_space = st.columns([1, 2])
                    with col_save:
                        if st.button("💾 Lưu lịch trình"):
                            user_id = st.session_state.get("user_id")
                            if user_id:
                                success = db_utils.add_schedule(
                                    user_id,
                                    ', '.join(dest_lines),
                                    budget,
                                    minutes_to_str(start_min),
                                    minutes_to_str(end_min),
                                    schedule_data,
                                )
                                if success:
                                    st.success("✅ Lịch trình đã được lưu vào hồ sơ của bạn!")
                                else:
                                    st.error("❌ Có lỗi khi lưu lịch trình.")
                else:
                    st.info("💡 Đăng nhập để lưu lịch trình vào hồ sơ của bạn.")

    # ===== PHẦN 2: CÁC CHỨC NĂNG HỖ TRỢ =====
    st.markdown("---")
    st.markdown("### 🎯 Các chức năng hỗ trợ")
    
    tab_gợi_ý, tab_tìm_đường, tab_nhận_diện = st.tabs(
        ["Tạo danh sách gợi ý", "Tìm đường đi", "Nhận diện ảnh"]
    )

    # 1. Tạo danh sách gợi ý
    with tab_gợi_ý:
        st.markdown("### 🧩 1. Tạo danh sách gợi ý")
        st.markdown(
            "<p class='feature-muted'>Nhập các điểm bạn quan tâm, hệ thống sẽ gợi ý danh sách địa điểm phù hợp với ngân sách và thời gian.</p>",
            unsafe_allow_html=True,
        )
        col_left, col_right = st.columns([1.2, 1])
        with col_left:
            interests = st.text_area(
                "Sở thích / loại địa điểm (ví dụ: bảo tàng, quán cà phê, biển, công viên...)",
                height=120,
            )
            budget_suggest = st.number_input(
                "Ngân sách dự kiến (VND)",
                min_value=0,
                value=500000,
                step=50000,
            )
            city = st.text_input("Thành phố / khu vực", value="TP.HCM")
            if st.button("Tạo danh sách gợi ý"):
                st.success("Đây là nơi bạn sẽ hiển thị danh sách gợi ý địa điểm .")
        with col_right:
            st.markdown("#### Gợi ý mô tả ")
            st.write("- Ưu tiên các địa điểm gần nhau để giảm thời gian di chuyển.")
            st.write("- Cân đối giữa tham quan, ăn uống và thư giãn.")
            st.write("- Có thể kết hợp 1–2 điểm “must-try” trong khu vực bạn chọn.")
        st.markdown("</div>", unsafe_allow_html=True)

    # 2. Tìm đường đi
    with tab_tìm_đường:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 🚗 2. Tìm đường đi")
        st.markdown(
            "<p class='feature-muted'>Hỗ trợ tìm đường đi tối ưu giữa các địa điểm, tính toán thời gian và chi phí di chuyển .</p>",
            unsafe_allow_html=True,
        )
        with st.form("route_form"):
            start_point = st.text_input("Điểm bắt đầu", value="Quận 1")
            end_point = st.text_input("Điểm kết thúc", value="Nhà thờ Đức Bà")
            col1, col2 = st.columns(2)
            with col1:
                mode = st.selectbox(
                    "Phương tiện di chuyển",
                    ["Xe máy", "Ô tô", "Đi bộ", "Phương tiện công cộng"],
                )
            with col2:
                max_time = st.number_input(
                    "Thời gian tối đa (phút)",
                    min_value=10,
                    value=45,
                    step=5,
                )
            c1, c2, c3 = st.columns([2, 1, 2])
            with c2:
                find_route = st.form_submit_button("Tìm đường!")
        if find_route:
            st.markdown("---")
            st.markdown("#### Kết quả ")
            st.write(f"- **Từ**: {start_point}")
            st.write(f"- **Đến**: {end_point}")
            st.write(f"- **Phương tiện**: {mode}")
            st.write(f"- **Thời gian ước tính**: ~{max_time} phút")
            st.info(
                "Phiên bản đầy đủ có thể tích hợp API bản đồ (Google Maps, OpenStreetMap, v.v.) để tính đường thực tế."
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # 3. Nhận diện ảnh
    with tab_nhận_diện:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("### 📷 3. Nhận diện ảnh ")
        st.markdown(
            "<p class='feature-muted'>Tải lên một bức ảnh địa điểm, hệ thống sẽ thử đoán đó là loại địa điểm nào .</p>",
            unsafe_allow_html=True,
        )
        img = st.file_uploader("Tải ảnh địa điểm (JPG/PNG)", type=["jpg", "jpeg", "png"])
        if img is not None:
            st.image(img, use_container_width=True)
            st.success(
                ": Hệ thống có thể trả về nhãn như 'biển', 'núi', 'cafe', 'trung tâm thương mại'..."
            )
        else:
            st.caption("📷 Chưa có ảnh nào được chọn.")
        st.markdown("</div>", unsafe_allow_html=True)

def page_ho_so():
    """Hiển thị nội dung trang Hồ sơ."""
    st.markdown("<div class='section-title'>Hồ sơ của bạn</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Xem lại tài khoản và các lịch trình đã lưu.</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.get("current_user"):
        st.success(f"Bạn đang đăng nhập với tài khoản: **{st.session_state['current_user']}**")

        st.markdown("### 👤 Thông tin tài khoản")
        st.write(f"**Email:** {st.session_state['current_user']}")

        st.markdown("### 🗂️ Lịch trình đã lưu")

        user_id = st.session_state.get("user_id")
        
        if user_id:
            schedules = db_utils.get_user_schedules(user_id)
            
            if not schedules:
                st.info("Bạn chưa có lịch trình nào được lưu. Hãy qua trang **Chức năng** > **Tìm kiếm nhanh** để tạo và lưu nhé!")
            else:
                st.write(f"Bạn có **{len(schedules)}** lịch trình đã lưu:")

                for schedule in schedules:
                    title = f"Lịch trình: {schedule['destination']} ({schedule['start_time']} – {schedule['end_time']})"

                    with st.expander("📅 " + title):
                        st.write(f"**Điểm đến:** {schedule['destination']}")
                        st.write(f"**Ngân sách:** {schedule['budget']:,} VND")
                        st.markdown("---")
                        st.write("**Timeline chi tiết:**")
                        for item in schedule["timeline"]:
                            st.markdown(
                                f"- **{item['place']}**: {item['arrive']} – {item['depart']}"
                            )
                        st.markdown("---")

                        if st.button("🗑️ Xóa lịch trình này", key=f"delete_{schedule['id']}"):
                            if db_utils.delete_schedule(schedule['id'], user_id):
                                st.success("Đã xóa lịch trình.")
                                st.rerun()
                            else:
                                st.error("Lỗi khi xóa lịch trình.")

        st.markdown("---")
        if st.button("Đăng xuất (Log out)"):
            st.session_state["current_user"] = None
            st.session_state["user_id"] = None
            st.rerun()
    else:
        st.error("Bạn cần đăng nhập để xem trang này.")
        st.info("Vui lòng chọn **Sign in / Sign up** từ thanh menu để đăng nhập.")

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
                # Add user using SQLite
                success, user_id = db_utils.add_user(email_up, password_up)
                if success:
                    # Tự động đăng nhập sau khi đăng ký thành công
                    st.session_state["current_user"] = email_up
                    st.session_state["user_id"] = user_id
                    st.session_state["current_page"] = "Trang chủ"  # Chuyển về trang chủ
                    st.success(f"Đăng ký thành công! Xin chào **{email_up}** 🎉")
                    st.rerun()
                else:
                    st.error("Email này đã được đăng ký.")

# ======================
# THANH ĐIỀU HƯỚNG 
# ======================
# Initialize current_page in session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Trang chủ"

if st.session_state.get("current_user"):
    menu_options = ["Trang chủ", "Giới thiệu", "Chức năng", "Hồ sơ"]
    menu_icons = ["house", "info-circle", "check2-square", "person-badge"]
else:
    menu_options = ["Trang chủ", "Giới thiệu", "Chức năng", "Sign in / Sign up"]
    menu_icons = ["house", "info-circle", "check2-square", "person-circle"]

# Render custom navigation
render_custom_nav(menu_options, menu_icons, st.session_state['current_page'])

# Get current page
page = st.session_state['current_page']

# ======================
# BỘ ĐIỀU HƯỚNG TRANG
# ======================
page_container = st.container()

with page_container:
    if page == "Trang chủ":
        page_trang_chu()
    elif page == "Giới thiệu":
        page_gioi_thieu()
    elif page == "Chức năng":
        page_chuc_nang()
    elif page == "Hồ sơ":
        page_ho_so()
    elif page == "Sign in / Sign up":
        page_sign_in_up()