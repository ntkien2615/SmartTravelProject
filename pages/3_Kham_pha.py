import streamlit as st
import pandas as pd

# Auth Guard
if not st.session_state.get('logged_in'):
    st.warning("Bạn cần đăng nhập để truy cập trang này.")
    st.switch_page("pages/2_Dang_nhap.py")
    st.stop()

st.header("Khám phá địa điểm")

# Sidebar for filters
st.sidebar.header("Bộ lọc tìm kiếm")
query_from_sidebar = st.sidebar.text_input("Tìm kiếm địa điểm", "")
# Add more filters here (e.g., price, type)
filters_from_sidebar = {
    "price_range": st.sidebar.slider("Khoảng giá", 0, 1000, (0, 1000)),
    "type": st.sidebar.multiselect("Loại hình", ["Nhà hàng", "Khách sạn", "Điểm tham quan", "Khác"])
}

# Main area for displaying results
st.subheader("Kết quả tìm kiếm")

# 📍 Vị trí chờ API (Tìm kiếm):
def search_locations(query, filters):
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
        with st.container(border=True): # Áp dụng CSS 'Card'
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item['img'], width=100)
            with col2:
                st.subheader(item['name'])
                st.caption(item['addr'])
                
                # Use a unique key for each button
                if st.button("Lưu", key=f"save_{item['id']}"):
                    st.info(f"Đã lưu {item['name']} (chức năng lưu sẽ được phát triển)")

                # 📍 Vị trí chờ API (Tìm đường)
                if st.button("Chỉ đường", key=f"nav_{item['id']}"):
                    # route = get_directions_api(start, (item['lat'], item['lon']))
                    # st.map(route['data'])
                    st.map(pd.DataFrame({'lat': [item['lat']], 'lon': [item['lon']]}))
else:
    st.info("Không tìm thấy địa điểm nào phù hợp.")
