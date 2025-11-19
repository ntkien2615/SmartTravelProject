"""Trang Chức năng với 4 nút lựa chọn"""
import streamlit as st
import streamlit.components.v1 as components
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
        st.session_state['selected_function'] = "Tạo lịch trình"
    
    # ===== BỐ CỤC 4 NÚT CHỌN CHỨC NĂNG =====
    st.markdown("### Chọn chức năng")
    
    # Hàng 1: Tạo lịch trình (full width)
    if st.button("🗓️ Tạo lịch trình", use_container_width=True, key="btn_tim_kiem_nhanh"):
        st.session_state['selected_function'] = "Tạo lịch trình"
        st.rerun()
    
    # Hàng 2: 3 chức năng con
    col_btn2, col_btn3, col_btn4 = st.columns(3)
    with col_btn2:
        if st.button("📍 Gợi ý địa điểm", use_container_width=True, key="btn_goi_y"):
            st.session_state['selected_function'] = "Gợi ý địa điểm"
            st.rerun()
    with col_btn3:
        if st.button("🚗 Tìm đường đi", use_container_width=True, key="btn_tim_duong"):
            st.session_state['selected_function'] = "Tìm đường đi"
            st.rerun()
    with col_btn4:
        if st.button("📷 Tìm vị trí ảnh", use_container_width=True, key="btn_nhan_dien"):
            st.session_state['selected_function'] = "Tìm vị trí ảnh"
            st.rerun()
    
    st.markdown("---")
    
    # ===== HIỂN THỊ NỘI DUNG THEO LỰA CHỌN =====
    selected = st.session_state['selected_function']
    st.info(f"✨ Đang hiển thị: **{selected}**")
    
    # 1. TẠO LỊCH TRÌNH
    if selected == "Tạo lịch trình":
        render_tim_kiem_nhanh()
    
    # 2. GỢI Ý ĐỊA ĐIỂM
    elif selected == "Gợi ý địa điểm":
        render_tao_danh_sach_goi_y()
    
    # 3. TÌM ĐƯỜNG ĐI
    elif selected == "Tìm đường đi":
        render_tim_duong_di()
    
    # 4. TÌM VỊ TRÍ ẢNH
    elif selected == "Tìm vị trí ảnh":
        render_nhan_dien_anh()


def render_tim_kiem_nhanh():
    """Render phần Tạo lịch trình - Tạo lịch trình 1 ngày"""
    st.markdown("### 🗓️ Tạo lịch trình")
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
    """Render phần Gợi ý địa điểm - TÍCH HỢP ALGO1"""
    st.markdown("### 📍 Gợi ý địa điểm")
    st.markdown(
        "<p class='feature-muted'>🎯 Nhập sở thích và yêu cầu, thuật toán AI sẽ tối ưu lịch trình cho bạn!</p>",
        unsafe_allow_html=True,
    )
    
    # Form nhập liệu ở trên cùng
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
                            # Load POIs - Dataset lớn với filter (7,743 POIs)
                            csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm_large.csv")
                            
                            # Filter POIs: chỉ lấy tourism-related, rating >= 3.8, tối đa 500 POIs
                            tourism_tags = [
                                "food", "restaurant", "cafe", "park", "nature", 
                                "museum", "history", "entertainment", "shopping", 
                                "landmark", "religious", "culture", "nightlife"
                            ]
                            pois = load_pois(
                                csv_path, 
                                filter_tags=tourism_tags,
                                min_rating=3.8,
                                max_pois=500  # Giới hạn để thuật toán chạy nhanh
                            )
                            
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
                                
                                # Layout: Lịch trình | Chi tiết
                                # Layout: Lịch trình gợi ý | Chi tiết từng điểm
                                col_summary, col_details = st.columns([1, 1], gap="large")
                                
                                with col_summary:
                                    st.markdown("#### 🗺️ Lịch trình gợi ý")
                                    
                                    # Styled info boxes
                                    st.markdown("""
                                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                                padding: 1.2rem; border-radius: 12px; color: white; margin-bottom: 1rem;'>
                                        <div style='font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.3rem;'>📍 Xuất phát</div>
                                        <div style='font-size: 1.1rem; font-weight: 600;'>{}</div>
                                    </div>
                                    """.format(start_location), unsafe_allow_html=True)
                                    
                                    col_time, col_budget = st.columns(2)
                                    with col_time:
                                        st.markdown("""
                                        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                                    padding: 1rem; border-radius: 12px; color: white; text-align: center;'>
                                            <div style='font-size: 0.85rem; opacity: 0.9;'>⏰ Thời gian</div>
                                            <div style='font-size: 1rem; font-weight: 600; margin-top: 0.3rem;'>{} – {}</div>
                                        </div>
                                        """.format(start_time.strftime('%H:%M'), end_time.strftime('%H:%M')), unsafe_allow_html=True)
                                    with col_budget:
                                        st.markdown("""
                                        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                                    padding: 1rem; border-radius: 12px; color: white; text-align: center;'>
                                            <div style='font-size: 0.85rem; opacity: 0.9;'>💰 Chi phí dự kiến</div>
                                            <div style='font-size: 1rem; font-weight: 600; margin-top: 0.3rem;'>{:,} VND</div>
                                        </div>
                                        """.format(int(round(total_cost))), unsafe_allow_html=True)
                                    
                                    st.write(f"**💰 Tổng chi phí:** {int(round(total_cost)):,} / {budget:,.0f} VND")
                                    st.write(f"**🎯 Sở thích:** {', '.join(set(user_prefs))}")
                                    
                                    # Bản đồ tổng quan
                                    st.markdown("---")
                                    st.markdown("##### 🗺️ Bản đồ tổng quan")
                                    
                                    # Tạo Leaflet map với tất cả điểm đến
                                    all_lats = [stop.get('lat', 0) for stop in route if stop.get('lat', 0) != 0]
                                    all_lons = [stop.get('lon', 0) for stop in route if stop.get('lon', 0) != 0]
                                    
                                    if all_lats and all_lons:
                                        center_lat = sum(all_lats) / len(all_lats)
                                        center_lon = sum(all_lons) / len(all_lons)
                                        
                                        # Tạo danh sách markers cho map
                                        markers_js = ""
                                        for idx, stop in enumerate(route, 1):
                                            lat = stop.get('lat', 0)
                                            lon = stop.get('lon', 0)
                                            if lat != 0 and lon != 0:
                                                name = stop['name'].replace("'", "\\'").replace('"', '\\"')
                                                arrive = stop['arrive_time'].strftime('%H:%M')
                                                depart = stop['depart_time'].strftime('%H:%M')
                                                markers_js += f"""
                                        L.marker([{lat}, {lon}], {{
                                            icon: L.divIcon({{
                                                html: '<div style="background: #2563eb; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{idx}</div>',
                                                className: '',
                                                iconSize: [28, 28],
                                                iconAnchor: [14, 14]
                                            }})
                                        }}).bindPopup('<b>{idx}. {name}</b><br>⏰ {arrive} - {depart}').addTo(map);
                                        """
                                        
                                        map_html = f"""
                                        <!DOCTYPE html>
                                        <html>
                                        <head>
                                            <meta charset="utf-8" />
                                            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                                            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                                            <style>
                                                body {{ margin: 0; padding: 0; }}
                                                #map {{ width: 100%; height: 400px; }}
                                            </style>
                                        </head>
                                        <body>
                                            <div id="map"></div>
                                            <script>
                                                var map = L.map('map').setView([{center_lat}, {center_lon}], 12);
                                                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                                                    attribution: '&copy; OpenStreetMap',
                                                    maxZoom: 19
                                                }}).addTo(map);
                                                {markers_js}
                                                
                                                // Vẽ đường nối các điểm
                                                var latlngs = [{', '.join([f'[{stop.get("lat", 0)}, {stop.get("lon", 0)}]' for stop in route if stop.get('lat', 0) != 0])}];
                                                L.polyline(latlngs, {{
                                                    color: '#f5576c',
                                                    weight: 3,
                                                    opacity: 0.7,
                                                    dashArray: '10, 5'
                                                }}).addTo(map);
                                                
                                                // Fit bounds
                                                if (latlngs.length > 0) {{
                                                    map.fitBounds(latlngs, {{padding: [30, 30]}});
                                                }}
                                            </script>
                                        </body>
                                        </html>
                                        """
                                        
                                        components.html(map_html, height=400)
                                
                                with col_details:
                                    st.markdown("#### 📍 Chi tiết từng điểm")
                                    
                                    # Display each stop with address
                                    for i, stop in enumerate(route, 1):
                                        mode_icon = {"walking": "🚶", "motorbike": "🏍️", "taxi": "🚕"}.get(stop['mode'], "🚗")
                                        lat = stop.get('lat', 0)
                                        lon = stop.get('lon', 0)
                                        
                                        with st.expander(
                                            f"{i}. {stop['name']} ({stop['arrive_time'].strftime('%H:%M')} - {stop['depart_time'].strftime('%H:%M')})",
                                            expanded=(i==1)
                                        ):
                                            # Địa chỉ POI với link Google Maps
                                            st.markdown(f"""
                                            <div style='background: linear-gradient(120deg, #ffecd2 0%, #fcb69f 100%); 
                                                        padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem;'>
                                                <div style='color: #1e293b; font-weight: 600; margin-bottom: 0.3rem;'>📍 {stop['name']}</div>
                                                <div style='color: #475569; font-size: 0.85rem;'>Tọa độ: {lat:.4f}, {lon:.4f}</div>
                                                <a href='https://www.google.com/maps/search/?api=1&query={lat},{lon}' 
                                                   target='_blank' 
                                                   style='color: #2563eb; font-size: 0.85rem; text-decoration: none; font-weight: 500;'>
                                                   🗺️ Xem trên Google Maps →
                                                </a>
                                            </div>
                                            """, unsafe_allow_html=True)
                                            
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
                
                # Hiển thị thông tin tổng quan với màu sắc đẹp
                st.markdown("#### 📊 Thông tin tổng quan")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 1.2rem; border-radius: 12px; color: white; text-align: center;'>
                        <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.3rem;'>📏 Quãng đường</div>
                        <div style='font-size: 1.5rem; font-weight: 700;'>{result['route']['distance_km']:.1f} km</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                padding: 1.2rem; border-radius: 12px; color: white; text-align: center;'>
                        <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.3rem;'>⏱️ Thời gian</div>
                        <div style='font-size: 1.5rem; font-weight: 700;'>{result['route']['duration_min']:.0f} phút</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    hours = result['route']['duration_min'] / 60
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                padding: 1.2rem; border-radius: 12px; color: white; text-align: center;'>
                        <div style='font-size: 0.85rem; opacity: 0.9; margin-bottom: 0.3rem;'>🕐 Tổng thời gian</div>
                        <div style='font-size: 1.5rem; font-weight: 700;'>{hours:.1f}h</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Hiển thị địa chỉ đầy đủ với màu gradient
                st.markdown(f"""
                <div style='background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%); 
                            padding: 1rem; border-radius: 12px; margin-bottom: 1rem;'>
                    <div style='color: #1e293b; font-weight: 600; margin-bottom: 0.5rem;'>📍 Địa chỉ chi tiết</div>
                    <div style='color: #475569; margin-bottom: 0.3rem;'><strong>Điểm bắt đầu:</strong> {result['start']['name']}</div>
                    <div style='color: #475569;'><strong>Điểm kết thúc:</strong> {result['end']['name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Thêm bản đồ OSM với Leaflet
                st.markdown("#### 🗺️ Bản đồ đường đi")
                lat1, lon1 = result['start']['lat'], result['start']['lon']
                lat2, lon2 = result['end']['lat'], result['end']['lon']
                center_lat = (lat1 + lat2) / 2
                center_lon = (lon1 + lon2) / 2
                
                # Tạo bản đồ Leaflet với OSRM routing
                map_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
                    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
                    <style>
                        body {{ margin: 0; padding: 0; }}
                        #map {{ width: 100%; height: 450px; }}
                    </style>
                </head>
                <body>
                    <div id="map"></div>
                    <script>
                        var map = L.map('map').setView([{center_lat}, {center_lon}], 13);
                        
                        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                            maxZoom: 19
                        }}).addTo(map);
                        
                        // Markers
                        var startIcon = L.icon({{
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        }});
                        
                        var endIcon = L.icon({{
                            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                            iconSize: [25, 41],
                            iconAnchor: [12, 41],
                            popupAnchor: [1, -34],
                            shadowSize: [41, 41]
                        }});
                        
                        L.marker([{lat1}, {lon1}], {{icon: startIcon}})
                            .bindPopup('<b>🟢 Điểm bắt đầu</b><br>{result['start']['name'].replace("'", "\\'")}')
                            .addTo(map);
                        
                        L.marker([{lat2}, {lon2}], {{icon: endIcon}})
                            .bindPopup('<b>🔴 Điểm kết thúc</b><br>{result['end']['name'].replace("'", "\\'")}')
                            .addTo(map);
                        
                        // Get route from OSRM
                        fetch('https://router.project-osrm.org/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson')
                            .then(response => response.json())
                            .then(data => {{
                                if (data.routes && data.routes.length > 0) {{
                                    var route = data.routes[0];
                                    var coords = route.geometry.coordinates.map(c => [c[1], c[0]]);
                                    
                                    L.polyline(coords, {{
                                        color: '#2563eb',
                                        weight: 5,
                                        opacity: 0.7
                                    }}).addTo(map).bindPopup('<b>Lộ trình</b><br>' + 
                                        (route.distance/1000).toFixed(1) + ' km<br>' + 
                                        (route.duration/60).toFixed(0) + ' phút');
                                    
                                    map.fitBounds(L.polyline(coords).getBounds(), {{padding: [50, 50]}});
                                }}
                            }})
                            .catch(err => console.error('Route error:', err));
                    </script>
                </body>
                </html>
                """
                
                # Hiển thị map
                components.html(map_html, height=450)
                
                # Link mở Google Maps
                google_maps_url = f"https://www.google.com/maps/dir/?api=1&origin={lat1},{lon1}&destination={lat2},{lon2}&travelmode={'driving' if vehicle_type == 'driving' else 'bicycling'}"
                st.markdown(f"""
                <div style='text-align: center; margin-top: 0.5rem;'>
                    <a href='{google_maps_url}' target='_blank' 
                       style='color: #2563eb; text-decoration: none; font-weight: 600;'>
                       🗺️ Mở trong Google Maps →
                    </a>
                </div>
                """, unsafe_allow_html=True)
                
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
    """Render phần Tìm vị trí ảnh"""
    st.markdown("### 📷 Tìm vị trí ảnh")
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
