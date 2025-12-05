"""Trang Chức năng với 4 nút lựa chọn"""
import streamlit as st
import streamlit.components.v1 as components
from datetime import time, datetime
import services.db as db_utils
from services.utils import time_to_minutes, minutes_to_str
import os

# Import algo1 modules (POI optimization)
try:
    from core.route_optimization import load_pois, plan_route
    ALGO_AVAILABLE = True
except ImportError:
    ALGO_AVAILABLE = False
    st.warning("⚠️ Không tìm thấy module route_optimization. Sử dụng chế độ demo.")

# Import algo2 modules (Routing/Navigation)
try:
    from core.map_integration import get_directions
    from core.map_integration.routing import geocode
    ROUTING_AVAILABLE = True
except ImportError:
    ROUTING_AVAILABLE = False
    geocode = None
    get_directions = None

# Import weather service
try:
    from core.weather_service.weather import get_weather
    WEATHER_AVAILABLE = True
except ImportError:
    WEATHER_AVAILABLE = False

# Import algo3 modules (Image Recognition)
try:
    from core.image_recognition.predict_vn import get_predictor
    from PIL import Image
    IMAGE_RECOGNITION_AVAILABLE = True
except ImportError:
    IMAGE_RECOGNITION_AVAILABLE = False


def page_chuc_nang():
    """Hiển thị nội dung trang chức năng với 4 nút lựa chọn."""
    st.markdown("<div class='section-title'>Chức năng</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Chọn chức năng bạn muốn sử dụng.</div>",
        unsafe_allow_html=True,
    )
    
    # Initialize selected function in session state
    if 'selected_function' not in st.session_state:
        st.session_state['selected_function'] = "Tạo lịch trình gợi ý"
    
    # ===== BỐ CỤC 5 NÚT CHỌN CHỨC NĂNG (1 ROW / 5 COL) =====
    st.markdown("### Chọn chức năng")
    
    # Hàng 1: 5 chức năng trong 1 row
    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
    with col_btn1:
        if st.button("🗓️ Tạo lịch trình gợi ý", width='stretch', key="btn_algo1"):
            st.session_state['selected_function'] = "Tạo lịch trình gợi ý"
            st.rerun()
    with col_btn2:
        if st.button("🚗 Tìm đường đi", width='stretch', key="btn_algo2"):
            st.session_state['selected_function'] = "Tìm đường đi"
            st.rerun()
    with col_btn3:
        if st.button("📷 Tìm vị trí ảnh", width='stretch', key="btn_algo3"):
            st.session_state['selected_function'] = "Tìm vị trí ảnh"
            st.rerun()
    with col_btn4:
        if st.button("🌤️ Báo thời tiết vị trí", width='stretch', key="btn_algo4"):
            st.session_state['selected_function'] = "Báo thời tiết vị trí"
            st.rerun()
    with col_btn5:
        if st.button("📍 Gợi ý địa điểm", width='stretch', key="btn_algo5"):
            st.session_state['selected_function'] = "Gợi ý địa điểm"
            st.rerun()
    
    st.markdown("---")
    
    # ===== HIỂN THỊ NỘI DUNG THEO LỰA CHỌN =====
    selected = st.session_state['selected_function']
    st.info(f"✨ Đang hiển thị: **{selected}**")
    
    # 1. TẠO LỊCH TRÌNH GỢI Ý (Route Optimization)
    if selected == "Tạo lịch trình gợi ý":
        render_tao_danh_sach_goi_y()
    
    # 2. TÌM ĐƯỜNG ĐI (Map Integration)
    elif selected == "Tìm đường đi":
        render_tim_duong_di()
    
    # 3. TÌM VỊ TRÍ ẢNH (Image Recognition)
    elif selected == "Tìm vị trí ảnh":
        render_nhan_dien_anh()
    
    # 4. BÁO THỜI TIẾT VỊ TRÍ (Weather Service)
    elif selected == "Báo thời tiết vị trí":
        render_bao_thoi_tiet()
    
    # 5. GỢI Ý ĐỊA ĐIỂM (Recommendation)
    elif selected == "Gợi ý địa điểm":
        render_goi_y_dia_diem()


def render_tao_danh_sach_goi_y():
    """Render phần Tạo lịch trình gợi ý - TÍCH HỢP ROUTE OPTIMIZATION"""
    st.markdown("### 🗓️ Tạo lịch trình gợi ý")
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
        submitted = st.form_submit_button("🎯 Tạo lịch trình tối ưu", width='stretch')

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
                                if st.session_state.get("current_user") is not None:
                                    st.markdown("---")
                                    if st.button("💾 Lưu lịch trình vào hồ sơ", width='stretch'):
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
    """Render phần Tìm đường đi - TÍCH HỢP MAP INTEGRATION"""
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
            find_route = st.form_submit_button("🗺️ Tìm đường!", width='stretch')
    
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
                # Pre-process names to avoid backslash in f-string (Python < 3.12 issue)
                start_name_safe = result['start']['name'].replace("'", "\\'")
                end_name_safe = result['end']['name'].replace("'", "\\'")
                
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
                            .bindPopup('<b>🟢 Điểm bắt đầu</b><br>{start_name_safe}')
                            .addTo(map);
                        
                        L.marker([{lat2}, {lon2}], {{icon: endIcon}})
                            .bindPopup('<b>🔴 Điểm kết thúc</b><br>{end_name_safe}')
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

    if not IMAGE_RECOGNITION_AVAILABLE:
        st.error("❌ Module nhận diện ảnh chưa được cài đặt hoặc bị lỗi.")
        return

    img_file = st.file_uploader("Tải ảnh địa điểm (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if img_file is not None:
        image = Image.open(img_file)
        st.image(image, caption="Ảnh đã tải lên", use_column_width=True)
        
        if st.button("🔍 Nhận diện ngay"):
            with st.spinner("Đang phân tích ảnh..."):
                try:
                    predictor = get_predictor()
                    label, confidence = predictor.predict_pil_image(image)
                    
                    st.success(f"📍 Kết quả: **{label}**")
                    st.info(f"🎯 Độ tin cậy: **{confidence*100:.2f}%**")
                except Exception as e:
                    st.error(f"Lỗi khi nhận diện: {str(e)}")
    else:
        st.caption("📷 Chưa có ảnh nào được chọn.")


def render_bao_thoi_tiet():
    """Render phần Báo thời tiết vị trí"""
    st.markdown("### 🌤️ Báo thời tiết vị trí")
    st.markdown(
        "<p class='feature-muted'>Xem thời tiết tại vị trí bạn muốn đến.</p>",
        unsafe_allow_html=True,
    )
    
    with st.form("weather_form"):
        location = st.text_input(
            "📍 Vị trí",
            value="TP.HCM, Việt Nam",
            help="Nhập tên địa điểm hoặc tọa độ"
        )
        submitted = st.form_submit_button("🌤️ Xem thời tiết", width='stretch')
    
    if submitted:
        if not WEATHER_AVAILABLE:
             st.error("❌ Module thời tiết chưa được cài đặt.")
             return

        if not ROUTING_AVAILABLE or geocode is None:
             st.error("❌ Không thể tìm kiếm địa điểm (Module Routing/Geocoding thiếu hoặc bị lỗi).")
             return

        with st.spinner(f"🔍 Đang tìm kiếm '{location}'..."):
            geo = geocode(location)
        
        if not geo:
            st.error("❌ Không tìm thấy địa điểm. Vui lòng thử lại.")
        else:
            lat, lon, name = geo
            st.success(f"📍 Đã tìm thấy: **{name}**")
            
            with st.spinner("🌤️ Đang lấy dữ liệu thời tiết..."):
                weather = get_weather(lat, lon)
            
            if not weather:
                st.warning("⚠️ Không thể lấy dữ liệu thời tiết. Vui lòng kiểm tra API Key.")
                st.info("💡 Bạn cần cấu hình `OPENWEATHER_API_KEY` trong `config.py`.")
            else:
                # Display weather info
                st.markdown("#### 🌤️ Thông tin thời tiết")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌡️ Nhiệt độ", f"{weather['temp']:.1f}°C", f"Cảm giác: {weather['feels_like']:.1f}°C")
                    st.metric("💧 Độ ẩm", f"{weather['humidity']}%")
                with col2:
                    st.metric("☁️ Tình trạng", weather['description'].title())
                    st.metric("💨 Gió", f"{weather['wind_speed']} m/s")
    else:
        st.caption("⏳ Nhập vị trí và bấm nút để xem thời tiết.")


def render_goi_y_dia_diem():
    """Render phần Gợi ý địa điểm - Recommendation: Chỉ gợi ý danh sách địa điểm"""
    st.markdown("### 📍 Gợi ý địa điểm")
    st.markdown(
        "<p class='feature-muted'>🎯 Chọn sở thích của bạn để nhận danh sách địa điểm phù hợp.</p>",
        unsafe_allow_html=True,
    )
    
    # Form nhập liệu
    st.markdown("#### 📝 Sở thích của bạn")
    with st.form("suggest_poi_form"):
        # Chọn sở thích
        st.markdown("**Chọn loại địa điểm bạn quan tâm:**")
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
        
        num_results = st.slider("Số lượng địa điểm gợi ý", min_value=5, max_value=50, value=20, step=5)
        
        submitted = st.form_submit_button("🔍 Tìm địa điểm", width='stretch')

    if not submitted:
        st.caption("⏳ Chọn sở thích và bấm nút để nhận gợi ý địa điểm.")
    else:
        # Thu thập sở thích
        user_prefs = []
        if pref_history: user_prefs.extend(["history", "landmark"])
        if pref_food: user_prefs.extend(["food", "restaurant", "cafe"])
        if pref_shopping: user_prefs.extend(["shopping", "market"])
        if pref_nature: user_prefs.extend(["nature", "park"])
        if pref_modern: user_prefs.extend(["modern", "viewpoint"])
        if pref_culture: user_prefs.extend(["culture", "museum"])
        if pref_nightlife: user_prefs.extend(["nightlife", "entertainment"])
        if pref_religious: user_prefs.extend(["religious", "architecture"])
        
        if not user_prefs:
            st.warning("⚠️ Vui lòng chọn ít nhất 1 sở thích!")
        else:
            # Load và filter POIs
            if ALGO_AVAILABLE:
                with st.spinner("🔍 Đang tìm kiếm địa điểm phù hợp..."):
                    try:
                        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm_large.csv")
                        
                        # Filter POIs theo sở thích
                        tourism_tags = list(set(user_prefs))
                        pois = load_pois(
                            csv_path, 
                            filter_tags=tourism_tags,
                            min_rating=3.5,
                            max_pois=num_results * 2  # Lấy nhiều hơn để sort
                        )
                        
                        if not pois:
                            st.error("❌ Không tìm thấy địa điểm nào phù hợp với sở thích của bạn.")
                        else:
                            # Sort theo rating và hiển thị
                            pois_sorted = sorted(pois, key=lambda x: x.get('rating', 0), reverse=True)[:num_results]
                            
                            st.success(f"✅ Tìm thấy **{len(pois_sorted)}** địa điểm phù hợp!")
                            
                            # Hiển thị danh sách
                            col_list, col_map = st.columns([1, 1], gap="large")
                            
                            with col_list:
                                st.markdown("#### 📋 Danh sách địa điểm")
                                for i, poi in enumerate(pois_sorted, 1):
                                    rating = poi.get('rating', 0)
                                    name = poi.get('name', 'Không tên')
                                    tags = poi.get('tags', [])
                                    lat = poi.get('lat', 0)
                                    lon = poi.get('lon', 0)
                                    
                                    with st.expander(f"{i}. {name} ⭐ {rating:.1f}", expanded=(i <= 3)):
                                        st.write(f"**Tên:** {name}")
                                        st.write(f"**Đánh giá:** ⭐ {rating:.1f}/5.0")
                                        if tags:
                                            st.write(f"**Loại:** {', '.join(tags[:5])}")
                                        if lat != 0 and lon != 0:
                                            st.write(f"**Tọa độ:** {lat:.4f}, {lon:.4f}")
                                            maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                                            st.markdown(f"[🗺️ Xem trên Google Maps]({maps_link})")
                            
                            with col_map:
                                st.markdown("#### 🗺️ Bản đồ")
                                if pois_sorted:
                                    all_lats = [p.get('lat', 0) for p in pois_sorted if p.get('lat', 0) != 0]
                                    all_lons = [p.get('lon', 0) for p in pois_sorted if p.get('lon', 0) != 0]
                                    
                                    if all_lats and all_lons:
                                        center_lat = sum(all_lats) / len(all_lats)
                                        center_lon = sum(all_lons) / len(all_lons)
                                        
                                        markers_js = ""
                                        for idx, poi in enumerate(pois_sorted, 1):
                                            lat = poi.get('lat', 0)
                                            lon = poi.get('lon', 0)
                                            if lat != 0 and lon != 0:
                                                name = poi['name'].replace("'", "\\'").replace('"', '\\"')
                                                rating = poi.get('rating', 0)
                                                markers_js += f"""
                                        L.marker([{lat}, {lon}], {{
                                            icon: L.divIcon({{
                                                html: '<div style="background: #10b981; color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{idx}</div>',
                                                className: '',
                                                iconSize: [28, 28],
                                                iconAnchor: [14, 14]
                                            }})
                                        }}).bindPopup('<b>{idx}. {name}</b><br>⭐ {rating:.1f}').addTo(map);
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
                                                #map {{ width: 100%; height: 500px; }}
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
                                                
                                                // Fit bounds
                                                var latlngs = [{', '.join([f'[{p.get("lat", 0)}, {p.get("lon", 0)}]' for p in pois_sorted if p.get('lat', 0) != 0])}];
                                                if (latlngs.length > 0) {{
                                                    var bounds = L.latLngBounds(latlngs);
                                                    map.fitBounds(bounds, {{padding: [30, 30]}});
                                                }}
                                            </script>
                                        </body>
                                        </html>
                                        """
                                        
                                        components.html(map_html, height=500)
                    except Exception as e:
                        st.error(f"❌ Lỗi: {str(e)}")
                        st.info("Vui lòng kiểm tra lại dữ liệu hoặc liên hệ admin.")
            else:
                st.error("❌ Module thuật toán chưa được cài đặt.")
