import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.ui_components import render_section_header

def render_discover_page():
    """Render discover/search page - now shows route finding."""
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 3rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h1 style="color: white; margin: 0; font-size: 3rem;">�️ Tìm đường đi</h1>
            <p style="margin: 1rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Tìm kiếm và lập kế hoạch hành trình của bạn</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="
            background: #FFF3CD;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #FFC107;
            margin: 3rem auto;
            max-width: 600px;
        ">
            <h2 style="color: #856404; margin: 0 0 1rem 0;">🚧 Đang phát triển</h2>
            <p style="color: #856404; font-size: 1.1rem; margin: 0;">Tính năng này đang được phát triển và sẽ sớm ra mắt!</p>
        </div>
    """, unsafe_allow_html=True)
    return

    # Sidebar for filters
    st.sidebar.header("Bộ lọc tìm kiếm")
    query_from_sidebar = st.sidebar.text_input("Tìm kiếm địa điểm", "")
    filters_from_sidebar = {
        "price_range": st.sidebar.slider("Khoảng giá", 0, 1000, (0, 1000)),
        "type": st.sidebar.multiselect("Loại hình", ["Nhà hàng", "Khách sạn", "Điểm tham quan", "Khác"])
    }

    # Main area for displaying results
    st.subheader("Kết quả tìm kiếm")

    # 📍 Vị trí chờ API (Tìm kiếm):
    def search_locations(query, filters):
        """Search locations (mock data for now)."""
        # ---- TODO: Kết nối API tìm kiếm ----
        # params = {'query': query, **filters}
        # response = requests.get("api/search", params=params)
        # return response.json()['results']

        # ---- Dữ liệu giả lập (Mock data) cho UI ----
        if query.lower() == "phở":
            return [
                {'id': 1, 'name': 'Quán Phở Ngon', 'img': 'https://via.placeholder.com/100/FF5733/FFFFFF?text=Pho', 'addr': '123 Đường ABC', 'lat': 10.7, 'lon': 106.6},
                {'id': 2, 'name': 'Phở Gia Truyền', 'img': 'https://via.placeholder.com/100/33FF57/FFFFFF?text=Pho', 'addr': '456 Đường XYZ', 'lat': 10.8, 'lon': 106.7}
            ]
        else:
            return [
                {'id': 3, 'name': 'Địa điểm A', 'img': 'https://via.placeholder.com/100/0000FF/FFFFFF?text=A', 'addr': '123 ABC', 'lat': 10.0, 'lon': 106.0},
                {'id': 4, 'name': 'Địa điểm B', 'img': 'https://via.placeholder.com/100/FF0000/FFFFFF?text=B', 'addr': '456 XYZ', 'lat': 10.1, 'lon': 106.1}
            ]

    results = search_locations(query_from_sidebar, filters_from_sidebar)

    if results:
        for item in results:
            st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.5rem;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    margin-bottom: 1rem;
                    transition: all 0.3s ease;
                    border: 1px solid #E0E0E0;
                ">
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(item['img'], use_container_width=True)
            with col2:
                st.markdown(f"### {item['name']}")
                st.caption(f"📍 {item['addr']}")
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("💾 Lưu", key=f"save_{item['id']}", use_container_width=True):
                        st.success(f"Đã lưu {item['name']}")
                with btn_col2:
                    if st.button("🗺️ Chỉ đường", key=f"nav_{item['id']}", use_container_width=True):
                        st.map(pd.DataFrame({'lat': [item['lat']], 'lon': [item['lon']]}))
            
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="
                text-align: center;
                padding: 3rem 2rem;
                background: white;
                border-radius: 12px;
                border: 2px dashed #E0E0E0;
            ">
                <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">🔍</div>
                <h3 style="color: #424242; margin-bottom: 0.5rem;">Không tìm thấy kết quả</h3>
                <p style="color: #757575;">Hãy thử tìm kiếm với từ khóa khác</p>
            </div>
        """, unsafe_allow_html=True)
