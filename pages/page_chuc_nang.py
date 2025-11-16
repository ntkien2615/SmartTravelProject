"""Trang Chức năng với 4 nút lựa chọn"""
import streamlit as st
from datetime import time, datetime
import db_utils
from utils import time_to_minutes, minutes_to_str
import os

# Import algo1 modules (POI optimization)
try:
    from core.algo1 import load_pois, plan_route
    ALGO_AVAILABLE = True
except ImportError:
    ALGO_AVAILABLE = False
    st.warning("⚠️ Không tìm thấy module algo1. Sử dụng chế độ demo.")

# Import algo2 modules (Routing/Navigation)
try:
    from core.algo2 import get_directions
    ROUTING_AVAILABLE = True
except ImportError:
    ROUTING_AVAILABLE = False


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
            start_location = st.text_input("Điểm xuất phát", value="Quận 1, TP.HCM")
            destinations_text = st.text_area(
                "Danh sách điểm muốn đến (mỗi dòng một địa điểm)",
                value="Nhà thờ Đức Bà\nPhố đi bộ Nguyễn Huệ\nLandmark 81",
                height=120,
            )
            food_text = st.text_area(
                "Danh sách món ăn muốn thử (mỗi dòng một món)",
                value="Phở bò\nBánh mì thịt\nTrà sữa",
                height=100,
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
            submitted = st.form_submit_button("🔍 Tạo lịch trình")

        if not submitted:
            st.caption("⏳ Nhập xong và bấm **Tạo lịch trình** để xem kết quả.")

    with col_result:
        st.markdown("#### 📆 Kết quả lịch trình")
        if not submitted:
            st.info("Kết quả sẽ hiển thị ở đây sau khi bạn bấm nút.")
        else:
            dest_lines = [line.strip() for line in destinations_text.splitlines() if line.strip()]
            food_lines = [line.strip() for line in food_text.splitlines() if line.strip()]

            if not dest_lines:
                st.error("Vui lòng nhập ít nhất 1 điểm đến.")
            else:
                start_min = time_to_minutes(start_time)
                end_min = time_to_minutes(end_time)
                if end_min <= start_min:
                    st.warning("Giờ kết thúc phải lớn hơn giờ bắt đầu. Dùng mặc định 08:00 – 20:00.")
                    start_min = 8 * 60
                    end_min = 20 * 60

                total_minutes = end_min - start_min
                block = max(total_minutes // len(dest_lines), 30)
                current = start_min

                st.write(f"**Điểm xuất phát:** {start_location}")
                st.write(f"**Thời gian:** {minutes_to_str(start_min)} – {minutes_to_str(end_min)}")
                st.write(f"**Ngân sách:** {budget:,} VND")
                st.markdown("---")

                schedule_data = {
                    "destinations": dest_lines,
                    "start_time": minutes_to_str(start_min),
                    "end_time": minutes_to_str(end_min),
                    "budget": budget,
                    "timeline": [],
                }

                for i, place in enumerate(dest_lines, start=1):
                    arrive = current
                    depart = min(current + block, end_min)
                    current = depart
                    schedule_data["timeline"].append({
                        "place": place,
                        "arrive": minutes_to_str(arrive),
                        "depart": minutes_to_str(depart),
                    })
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

                # Nút lưu (nếu đã đăng nhập)
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
                                    st.success("✅ Lịch trình đã được lưu!")
                                else:
                                    st.error("❌ Có lỗi khi lưu lịch trình.")
                else:
                    st.info("💡 Đăng nhập để lưu lịch trình vào hồ sơ.")


def render_tao_danh_sach_goi_y():
    """Render phần Tạo danh sách gợi ý - TÍCH HỢP ALGO1"""
    st.markdown("### 🧩 Tạo danh sách gợi ý")
    st.markdown(
        "<p class='feature-muted'>🎯 Nhập sở thích và yêu cầu, thuật toán AI sẽ tối ưu lịch trình cho bạn!</p>",
        unsafe_allow_html=True,
    )
    
    col_form, col_result = st.columns([1.1, 1], gap="large")
    
    with col_form:
        st.markdown("#### 📝 Thông tin và sở thích")
        with st.form("suggest_form"):
            start_location = st.text_input("Điểm xuất phát", value="Quận 1, TP.HCM", 
                                          help="Vị trí bạn bắt đầu hành trình")
            
            # Chọn sở thích
            st.markdown("**Sở thích của bạn:**")
            col_pref1, col_pref2 = st.columns(2)
            with col_pref1:
                pref_history = st.checkbox("🏛️ Lịch sử / Di tích", value=True)
                pref_food = st.checkbox("🍜 Ẩm thực", value=True)
                pref_shopping = st.checkbox("🛍️ Mua sắm", value=False)
                pref_nature = st.checkbox("🌳 Thiên nhiên", value=False)
            with col_pref2:
                pref_modern = st.checkbox("🏙️ Hiện đại", value=False)
                pref_culture = st.checkbox("🎭 Văn hóa", value=False)
                pref_nightlife = st.checkbox("🌃 Giải trí", value=False)
                pref_religious = st.checkbox("🙏 Tôn giáo", value=False)
            
            st.markdown("**Kế hoạch:**")
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
            submitted = st.form_submit_button("🎯 Tạo lịch trình tối ưu", use_container_width=True)

        if not submitted:
            st.caption("⏳ Điền thông tin và bấm nút để nhận gợi ý tối ưu.")
    
    with col_result:
        st.markdown("#### 🗺️ Lịch trình gợi ý")
        if not submitted:
            st.info("📍 Kết quả sẽ hiển thị ở đây sau khi bạn bấm nút.")
        else:
            # Thu thập sở thích
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
                # Validate time
                start_min = time_to_minutes(start_time)
                end_min = time_to_minutes(end_time)
                if end_min <= start_min:
                    st.error("❌ Giờ kết thúc phải lớn hơn giờ bắt đầu!")
                else:
                    # Format time for algo
                    today = datetime.now().strftime("%Y-%m-%d")
                    time_window = (
                        f"{today} {start_time.strftime('%H:%M')}",
                        f"{today} {end_time.strftime('%H:%M')}"
                    )
                    
                    # Run algorithm
                    if ALGO_AVAILABLE:
                        with st.spinner("🔄 Đang tính toán lộ trình tối ưu bằng AI..."):
                            try:
                                # Load POIs
                                csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm.csv")
                                pois = load_pois(csv_path)
                                
                                # Call algorithm
                                route = plan_route(
                                    pois=pois,
                                    user_prefs=user_prefs,
                                    start_loc=(10.7769, 106.7006),
                                    time_window=time_window,
                                    budget=float(budget)
                                )
                                
                                if not route:
                                    st.error("❌ Không tìm thấy lịch trình phù hợp.")
                                    st.info("💡 Gợi ý: Tăng ngân sách, mở rộng thời gian hoặc chọn thêm sở thích.")
                                else:
                                    # Display results
                                    st.success(f"✅ Tìm thấy lộ trình với **{len(route)}** điểm đến!")
                                    
                                    total_cost = sum(r['travel_cost'] + r['entry_fee'] for r in route)
                                    st.write(f"**📍 Xuất phát:** {start_location}")
                                    st.write(f"**⏰ Thời gian:** {start_time.strftime('%H:%M')} – {end_time.strftime('%H:%M')}")
                                    st.write(f"**💰 Tổng chi phí:** {total_cost:,.0f} / {budget:,.0f} VND")
                                    st.write(f"**🎯 Sở thích:** {', '.join(set(user_prefs))}")
                                    st.markdown("---")
                                    
                                    # Display each stop
                                    for i, stop in enumerate(route, 1):
                                        mode_icon = {"walking": "🚶", "motorbike": "🏍️", "taxi": "🚕"}.get(stop['mode'], "🚗")
                                        with st.expander(
                                            f"{i}. {stop['name']} ({stop['arrive_time'].strftime('%H:%M')} - {stop['depart_time'].strftime('%H:%M')})",
                                            expanded=(i==1)
                                        ):
                                            st.write(f"**🚗 Di chuyển:** {mode_icon} {stop['mode'].title()}")
                                            st.write(f"**⏰ Đến:** {stop['arrive_time'].strftime('%H:%M')}")
                                            st.write(f"**⏰ Rời:** {stop['depart_time'].strftime('%H:%M')}")
                                            st.write(f"**💵 Chi phí di chuyển:** {stop['travel_cost']:,.0f} VND")
                                            st.write(f"**🎫 Vé vào cửa:** {stop['entry_fee']:,.0f} VND")
                                    
                                    # Save to session
                                    schedule_data = {
                                        "route": route,
                                        "preferences": user_prefs,
                                        "total_cost": total_cost,
                                        "budget": budget
                                    }
                                    st.session_state["latest_schedule"] = schedule_data
                                    
                                    # Save button
                                    if st.session_state.get("current_user"):
                                        st.markdown("---")
                                        if st.button("💾 Lưu lịch trình vào hồ sơ", use_container_width=True):
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
                                                    st.success("✅ Đã lưu thành công!")
                                                else:
                                                    st.error("❌ Lỗi khi lưu.")
                                    else:
                                        st.info("💡 Đăng nhập để lưu lịch trình vào hồ sơ.")
                                        
                            except Exception as e:
                                st.error(f"❌ Lỗi: {str(e)}")
                                st.info("Vui lòng kiểm tra lại dữ liệu hoặc liên hệ admin.")
                    else:
                        st.error("❌ Module thuật toán chưa được cài đặt.")


def render_tim_duong_di():
    """Render phần Tìm đường đi - TÍCH HỢP ALGO2"""
    st.markdown("### 🚗 Tìm đường đi")
    st.markdown(
        "<p class='feature-muted'>Tìm đường đi tối ưu giữa các địa điểm với OpenStreetMap.</p>",
        unsafe_allow_html=True,
    )
    
    with st.form("route_form"):
        start_point = st.text_input(
            "📍 Điểm bắt đầu", 
            value="Dinh Độc Lập, TPHCM",
            help="Nhập địa chỉ đầy đủ để có kết quả chính xác"
        )
        end_point = st.text_input(
            "🎯 Điểm kết thúc", 
            value="Chợ Bến Thành, TPHCM",
            help="Nhập địa chỉ đầy đủ để có kết quả chính xác"
        )
        
        mode = st.selectbox(
            "🚦 Phương tiện",
            ["Ô tô", "Xe máy"],
            help="Ô tô dùng đường lớn, Xe máy có thể đi đường hẹp"
        )
        
        c1, c2, c3 = st.columns([2, 1, 2])
        with c2:
            find_route = st.form_submit_button("🗺️ Tìm đường!", use_container_width=True)
    
    if find_route:
        st.markdown("---")
        
        if not ROUTING_AVAILABLE:
            st.warning("⚠️ Module routing chưa được cài đặt. Sử dụng chế độ demo.")
            st.markdown("#### 📍 Kết quả (Demo)")
            st.write(f"- **Từ:** {start_point}")
            st.write(f"- **Đến:** {end_point}")
            st.write(f"- **Phương tiện:** {mode}")
            st.info("💡 Cài đặt `requests` để sử dụng tính năng thực tế.")
        else:
            # Chuyển đổi tên phương tiện
            vehicle_type = "driving" if mode == "Ô tô" else "bike"
            vehicle_icon = "🚗" if mode == "Ô tô" else "🏍️"
            
            with st.spinner(f"🔍 Đang tìm đường cho {vehicle_icon} {mode}..."):
                result = get_directions(start_point, end_point, vehicle_type)
            
            if not result:
                st.error("❌ Không tìm thấy đường đi. Vui lòng kiểm tra lại địa chỉ.")
            else:
                st.success(f"✅ Tìm thấy lộ trình {vehicle_icon} {mode}!")
                
                # Hiển thị thông tin tổng quan
                st.markdown("#### 📊 Thông tin tổng quan")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📏 Quãng đường", f"{result['route']['distance_km']:.1f} km")
                with col2:
                    st.metric("⏱️ Thời gian", f"{result['route']['duration_min']:.0f} phút")
                with col3:
                    hours = result['route']['duration_min'] / 60
                    st.metric("🕐 Giờ", f"{hours:.1f}h")
                
                # Hiển thị địa chỉ đầy đủ
                with st.expander("📍 Xem địa chỉ chi tiết"):
                    st.write(f"**Điểm bắt đầu:** {result['start']['name']}")
                    st.write(f"**Điểm kết thúc:** {result['end']['name']}")
                
                # Hiển thị chỉ dẫn từng bước
                st.markdown("#### 🛣️ Chỉ dẫn đường đi")
                steps = result['route']['steps']
                
                for i, step in enumerate(steps, 1):
                    instruction = step['instruction']
                    street = step['street']
                    distance_m = step['distance_m']
                    
                    if street:
                        st.write(f"**{i}.** {instruction} vào **{street}** ({distance_m:.0f}m)")
                    else:
                        st.write(f"**{i}.** {instruction} ({distance_m:.0f}m)")
                
                st.success(f"✅ Đã đến đích! Tổng quãng đường: {result['route']['distance_km']:.1f} km")
                st.info(f"💡 Lưu ý: Thời gian và quãng đường có thể thay đổi tùy điều kiện giao thông thực tế.")


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
