"""Trang Chức năng với 4 nút lựa chọn"""
import streamlit as st
from datetime import time, datetime
import db_utils
from utils import time_to_minutes, minutes_to_str
import os

# Import algo1 modules
try:
    from core.solver_route import load_pois, plan_route
    ALGO_AVAILABLE = True
except ImportError:
    ALGO_AVAILABLE = False
    st.warning("⚠️ Không tìm thấy module thuật toán. Sử dụng chế độ demo.")


def page_chuc_nang():
    """Hiển thị nội dung trang chức năng với 4 nút lựa chọn."""
    st.markdown("<div class='section-title'>Chức năng</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Chọn chức năng bạn muốn sử dụng.</div>",
        unsafe_allow_html=True,
    )
    
    # Initialize selected function in session state
    if 'selected_function' not in st.session_state:
        st.session_state['selected_function'] = "Tìm kiếm nhanh"
    
    # ===== BỐ CỤC 4 NÚT CHỌN CHỨC NĂNG =====
    st.markdown("### Chọn chức năng")
    
    # Hàng 1: Tìm kiếm nhanh (full width)
    if st.button("🔍 Tìm kiếm nhanh", use_container_width=True, key="btn_tim_kiem_nhanh"):
        st.session_state['selected_function'] = "Tìm kiếm nhanh"
        st.rerun()
    
    # Hàng 2: 3 chức năng con
    col_btn2, col_btn3, col_btn4 = st.columns(3)
    with col_btn2:
        if st.button("🧩 Tạo danh sách gợi ý", use_container_width=True, key="btn_goi_y"):
            st.session_state['selected_function'] = "Tạo danh sách gợi ý"
            st.rerun()
    with col_btn3:
        if st.button("🚗 Tìm đường đi", use_container_width=True, key="btn_tim_duong"):
            st.session_state['selected_function'] = "Tìm đường đi"
            st.rerun()
    with col_btn4:
        if st.button("📷 Nhận diện vị trí ảnh", use_container_width=True, key="btn_nhan_dien"):
            st.session_state['selected_function'] = "Nhận diện vị trí ảnh"
            st.rerun()
    
    st.markdown("---")
    
    # ===== HIỂN THỊ NỘI DUNG THEO LỰA CHỌN =====
    selected = st.session_state['selected_function']
    st.info(f"✨ Đang hiển thị: **{selected}**")
    
    # 1. TÌM KIẾM NHANH
    if selected == "Tìm kiếm nhanh":
        render_tim_kiem_nhanh()
    
    # 2. TẠO DANH SÁCH GỢI Ý
    elif selected == "Tạo danh sách gợi ý":
        render_tao_danh_sach_goi_y()
    
    # 3. TÌM ĐƯỜNG ĐI
    elif selected == "Tìm đường đi":
        render_tim_duong_di()
    
    # 4. NHẬN DIỆN VỊ TRÍ ẢNH
    elif selected == "Nhận diện vị trí ảnh":
        render_nhan_dien_anh()


def render_tim_kiem_nhanh():
    """Render phần Tìm kiếm nhanh - Tạo lịch trình 1 ngày"""
    st.markdown("### 🔍 Tìm kiếm nhanh")
    st.markdown(
        "<p class='feature-muted'>Tạo lịch trình 1 ngày nhanh chóng với các điểm đến yêu thích.</p>",
        unsafe_allow_html=True,
    )
    
    col_form, col_result = st.columns([1.1, 1], gap="large")
    
    with col_form:
        st.markdown("#### 📝 Nhập thông tin chuyến đi")
        with st.form("quick_search_form"):
            start_location = st.text_input("Điểm xuất phát", value="Quận 1, TP.HCM", 
                                          help="Vị trí xuất phát của bạn")
            
            # Thay đổi: User chọn sở thích thay vì nhập địa điểm cụ thể
            st.markdown("**Sở thích của bạn:**")
            col_pref1, col_pref2 = st.columns(2)
            with col_pref1:
                pref_history = st.checkbox("🏛️ Lịch sử / Di tích", value=True)
                pref_food = st.checkbox("🍜 Ẩm thực", value=True)
                pref_shopping = st.checkbox("🛍️ Mua sắm", value=False)
                pref_nature = st.checkbox("🌳 Thiên nhiên / Công viên", value=False)
            with col_pref2:
                pref_modern = st.checkbox("🏙️ Hiện đại / Tòa nhà cao", value=False)
                pref_culture = st.checkbox("🎭 Văn hóa / Bảo tàng", value=False)
                pref_nightlife = st.checkbox("🌃 Giải trí / Phố đêm", value=False)
                pref_religious = st.checkbox("🙏 Tôn giáo / Chùa chiền", value=False)
            
            c1, c2 = st.columns(2)
            with c1:
                start_time = st.time_input("Giờ bắt đầu", value=time(9, 0))
            with c2:
                end_time = st.time_input("Giờ kết thúc", value=time(21, 0))
            budget = st.number_input(
                "Ngân sách tối đa (VND)",
                min_value=0,
                value=1000000,
                step=100000,
            )
            submitted = st.form_submit_button("🔍 Tạo lịch trình tối ưu")

        if not submitted:
            st.caption("⏳ Nhập xong và bấm **Tạo lịch trình** để xem kết quả.")

    with col_result:
        st.markdown("#### 📆 Kết quả lịch trình")
        if not submitted:
            st.info("Kết quả sẽ hiển thị ở đây sau khi bạn bấm nút.")
        else:
            # Thu thập sở thích người dùng
            user_prefs = []
            if pref_history: user_prefs.extend(["history", "landmark"])
            if pref_food: user_prefs.extend(["food", "street_food"])
            if pref_shopping: user_prefs.extend(["shopping", "market"])
            if pref_nature: user_prefs.extend(["nature", "park"])
            if pref_modern: user_prefs.extend(["modern", "viewpoint"])
            if pref_culture: user_prefs.extend(["culture", "museum"])
            if pref_nightlife: user_prefs.extend(["nightlife", "entertainment"])
            if pref_religious: user_prefs.extend(["religious", "architecture"])
            
            if not user_prefs:
                st.warning("⚠️ Vui lòng chọn ít nhất 1 sở thích!")
            else:
                # Kiểm tra thời gian hợp lệ
                start_min = time_to_minutes(start_time)
                end_min = time_to_minutes(end_time)
                if end_min <= start_min:
                    st.error("Giờ kết thúc phải lớn hơn giờ bắt đầu!")
                else:
                    # Format thời gian cho algo
                    today = datetime.now().strftime("%Y-%m-%d")
                    time_window = (
                        f"{today} {start_time.strftime('%H:%M')}",
                        f"{today} {end_time.strftime('%H:%M')}"
                    )
                    
                    # Chạy thuật toán
                    if ALGO_AVAILABLE:
                        with st.spinner("🔄 Đang tính toán lộ trình tối ưu..."):
                            try:
                                # Load POIs
                                csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm.csv")
                                pois = load_pois(csv_path)
                                
                                # Gọi thuật toán
                                route = plan_route(
                                    pois=pois,
                                    user_prefs=user_prefs,
                                    start_loc=(10.7769, 106.7006),  # Tọa độ Quận 1
                                    time_window=time_window,
                                    budget=float(budget)
                                )
                                
                                if not route:
                                    st.error("❌ Không tìm thấy lịch trình phù hợp. Thử tăng ngân sách hoặc mở rộng thời gian.")
                                else:
                                    # Hiển thị kết quả
                                    st.success(f"✅ Tìm thấy lộ trình với **{len(route)}** điểm đến!")
                                    
                                    total_cost = sum(r['travel_cost'] + r['entry_fee'] for r in route)
                                    st.write(f"**📍 Điểm xuất phát:** {start_location}")
                                    st.write(f"**⏰ Thời gian:** {start_time.strftime('%H:%M')} – {end_time.strftime('%H:%M')}")
                                    st.write(f"**💰 Tổng chi phí:** {total_cost:,.0f} VND / {budget:,.0f} VND")
                                    st.write(f"**🎯 Sở thích:** {', '.join(set(user_prefs))}")
                                    st.markdown("---")
                                    
                                    # Hiển thị từng điểm
                                    for i, stop in enumerate(route, 1):
                                        mode_icon = {"walking": "🚶", "motorbike": "🏍️", "taxi": "🚕"}.get(stop['mode'], "🚗")
                                        with st.expander(
                                            f"{i}. {stop['name']} ({stop['arrive_time'].strftime('%H:%M')} - {stop['depart_time'].strftime('%H:%M')})"
                                        ):
                                            st.write(f"**🚗 Di chuyển:** {mode_icon} {stop['mode'].title()}")
                                            st.write(f"**⏰ Đến:** {stop['arrive_time'].strftime('%H:%M')}")
                                            st.write(f"**⏰ Rời:** {stop['depart_time'].strftime('%H:%M')}")
                                            st.write(f"**💵 Chi phí di chuyển:** {stop['travel_cost']:,.0f} VND")
                                            st.write(f"**🎫 Vé vào cửa:** {stop['entry_fee']:,.0f} VND")
                                    
                                    # Lưu vào session
                                    schedule_data = {
                                        "route": route,
                                        "preferences": user_prefs,
                                        "total_cost": total_cost,
                                        "budget": budget
                                    }
                                    st.session_state["latest_schedule"] = schedule_data
                                    
                                    # Nút lưu
                                    if st.session_state.get("current_user"):
                                        st.markdown("---")
                                        if st.button("💾 Lưu lịch trình vào hồ sơ"):
                                            user_id = st.session_state.get("user_id")
                                            if user_id:
                                                dest_names = ", ".join([r['name'] for r in route])
                                                success = db_utils.add_schedule(
                                                    user_id,
                                                    dest_names,
                                                    budget,
                                                    start_time.strftime('%H:%M'),
                                                    end_time.strftime('%H:%M'),
                                                    schedule_data,
                                                )
                                                if success:
                                                    st.success("✅ Đã lưu!")
                                                else:
                                                    st.error("❌ Lỗi khi lưu.")
                                    else:
                                        st.info("💡 Đăng nhập để lưu lịch trình.")
                                        
                            except Exception as e:
                                st.error(f"❌ Lỗi khi tính toán: {str(e)}")
                                st.error("Vui lòng kiểm tra lại dữ liệu hoặc liên hệ admin.")
                    else:
                        st.error("❌ Module thuật toán chưa được cài đặt. Vui lòng kiểm tra lại.")


def render_tao_danh_sach_goi_y():
    """Render phần Tạo danh sách gợi ý"""
    st.markdown("### 🧩 Tạo danh sách gợi ý")
    st.markdown(
        "<p class='feature-muted'>Nhập sở thích, hệ thống sẽ gợi ý danh sách địa điểm phù hợp.</p>",
        unsafe_allow_html=True,
    )
    col_left, col_right = st.columns([1.2, 1])
    with col_left:
        interests = st.text_area(
            "Sở thích / loại địa điểm (ví dụ: bảo tàng, quán cà phê, biển...)",
            height=100,
        )
        budget_suggest = st.number_input(
            "Ngân sách dự kiến (VND)",
            min_value=0,
            value=500000,
            step=50000,
        )
        city = st.text_input("Thành phố / khu vực", value="TP.HCM")
        if st.button("Tạo danh sách gợi ý"):
            st.success("Đây là nơi hiển thị danh sách gợi ý địa điểm.")
    with col_right:
        st.markdown("#### 💡 Gợi ý")
        st.write("- Ưu tiên địa điểm gần nhau")
        st.write("- Cân đối tham quan, ăn uống, thư giãn")
        st.write("- Kết hợp điểm 'must-try' trong khu vực")


def render_tim_duong_di():
    """Render phần Tìm đường đi"""
    st.markdown("### 🚗 Tìm đường đi")
    st.markdown(
        "<p class='feature-muted'>Tìm đường đi tối ưu giữa các địa điểm.</p>",
        unsafe_allow_html=True,
    )
    with st.form("route_form"):
        start_point = st.text_input("Điểm bắt đầu", value="Quận 1")
        end_point = st.text_input("Điểm kết thúc", value="Nhà thờ Đức Bà")
        col1, col2 = st.columns(2)
        with col1:
            mode = st.selectbox(
                "Phương tiện",
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
        st.markdown("#### 📍 Kết quả")
        st.write(f"- **Từ:** {start_point}")
        st.write(f"- **Đến:** {end_point}")
        st.write(f"- **Phương tiện:** {mode}")
        st.write(f"- **Thời gian ước tính:** ~{max_time} phút")
        st.info("💡 Phiên bản đầy đủ có thể tích hợp API bản đồ (Google Maps, OpenStreetMap).")


def render_nhan_dien_anh():
    """Render phần Nhận diện vị trí ảnh"""
    st.markdown("### 📷 Nhận diện vị trí ảnh")
    st.markdown(
        "<p class='feature-muted'>Tải lên ảnh địa điểm, hệ thống sẽ nhận diện loại địa điểm.</p>",
        unsafe_allow_html=True,
    )
    img = st.file_uploader("Tải ảnh địa điểm (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if img is not None:
        st.image(img, use_container_width=True)
        st.success("💡 Hệ thống có thể trả về nhãn: 'biển', 'núi', 'cafe', 'trung tâm thương mại'...")
    else:
        st.caption("📷 Chưa có ảnh nào được chọn.")
