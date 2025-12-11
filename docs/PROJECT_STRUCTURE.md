# 📁 CẤU TRÚC PROJECT - WINDYAI SMART TRAVEL

## 🎯 Tổng Quan
Project **WindyAI** (tiền thân là Smart Travel Optimization) được tổ chức lại theo cấu trúc modular, tách biệt rõ ràng giữa:
- **Web Interface** (Streamlit)
- **Algorithm Core** (Route Optimization, Mapping, etc.)
- **Data & Database**
- **Services** (Database & Utilities)

---

## 📂 Cấu Trúc Thư Mục

```
WindyAI/
│
├── 🚀 app.py                      # Main entry point - Chạy web app
│
├── 📄 pages/                      # Modular pages (Web interface)
│   ├── page_trang_chu.py         # Trang chủ
│   ├── page_gioi_thieu.py        # Giới thiệu (Về dự án & Thành viên)
│   ├── page_chuc_nang.py         # ⭐ Chức năng (tích hợp các thuật toán)
│   ├── page_ho_so.py             # Hồ sơ người dùng
│   └── page_sign_in_up.py        # Đăng nhập/Đăng ký
│
├── 🧠 core/                       # Core Algorithms
│   ├── route_optimization/       # (Algo1) Tối ưu lịch trình
│   │   ├── solver_route.py       # ⭐ Main algorithm (Greedy + Lookahead)
│   │   ├── scorer.py             # Đánh giá và chấm điểm POI
│   │   ├── optimizer.py          # Tối ưu hậu kỳ (2-opt)
│   │   ├── utils_geo.py          # Tính khoảng cách, thời gian, chi phí
│   │   ├── config.py             # Cấu hình (speeds, costs, weights)
│   │   └── __init__.py
│   │
│   ├── map_integration/          # (Algo2) Bản đồ & Chỉ đường
│   │   ├── routing.py            # OSRM Routing
│   │   ├── mapping.py            # Folium Map generation
│   │   └── __init__.py
│   │
│   ├── image_recognition/        # (Algo3) Nhận diện ảnh
│   │   └── __init__.py
│   │
│   ├── weather_service/          # (Algo4) Dịch vụ thời tiết
│   │   ├── weather.py
│   │   └── __init__.py
│   │
│   └── recommendation/           # (Algo5) Gợi ý địa điểm
│       └── __init__.py
│
├── 🛠️ services/                   # Core Services
│   ├── db.py                     # Database operations (Supabase)
│   ├── utils.py                  # Helper functions
│   └── __init__.py
│
├── 📜 scripts/                    # Scripts & Tools
│   ├── fetch_pois_large.py       # Script lấy dữ liệu POI
│   ├── fetch_pois_osm.py         # Script lấy dữ liệu OSM
│   ├── check_user.py             # Script kiểm tra user
│   └── legacy/                   # Code cũ (đã ngưng sử dụng)
│       ├── main.py
│       └── ui.py
│
├── 📊 data/                       # Dữ liệu
│   ├── pois_hcm_large.csv        # POIs Hồ Chí Minh
│   └── README.md
│
├── 🎨 Frontend Assets
│   ├── style.css                 # CSS styling cho web
│   └── logo/                     # Logo assets
│
├── 📦 Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── runtime.txt               # Python runtime version
│   ├── start.ps1                 # PowerShell start script
│   ├── WEATHER_SETUP.md          # Hướng dẫn setup thời tiết
│   └── PROJECT_STRUCTURE.md      # ⭐ This file
│
└── 📖 Documentation
    ├── README.md                 # Main documentation
    └── LICENSE                   # License
```

---

## 🔗 Luồng Hoạt Động

### 1. **User Interface Flow**
```
app.py
  ├── pages/page_trang_chu.py    → Home page
  ├── pages/page_chuc_nang.py    → ⭐ Tích hợp thuật toán
  │     └── calls: core/route_optimization/solver_route.plan_route()
  └── pages/page_ho_so.py        → Profile & saved schedules
```

### 2. **Algorithm Flow (Route Optimization)**
```
pages/page_chuc_nang.py
  └── core/route_optimization/solver_route.plan_route()
        ├── load_pois() from data/pois_hcm_large.csv
        ├── core/route_optimization/scorer.score_candidate()
        ├── core/route_optimization/utils_geo.travel_info()
        └── Return optimized route
```

### 3. **Data Flow**
```
User Input → page_chuc_nang.py → Route Optimization → Optimized Route → Display
                                    ↓
                            Save to Supabase (via services/db.py)
```

---

## 🚀 Cách Chạy

### Chạy Web App (Streamlit)
```bash
streamlit run app.py
# hoặc
python -m streamlit run app.py
```

---

## ⚙️ Cấu Hình Route Optimization

File `core/route_optimization/config.py` chứa các tham số:
```python
SPEEDS_KMH = {"walking": 5.0, "motorbike": 25.0, "taxi": 35.0}
COST_PER_KM = {"walking": 0.0, "motorbike": 2000.0, "taxi": 12000.0}
```

---

## 📦 Dependencies

Xem file `requirements.txt`:
```txt
streamlit
pandas
numpy
supabase
...
```

---

## 🎯 Next Steps

1. **Tối ưu thuật toán:**
   - Thêm 2-opt optimization
   - Cache tính toán khoảng cách
   - Multi-threading cho large datasets

2. **Mở rộng dữ liệu:**
   - Thêm POIs (hiện tại: 20 → mục tiêu: 100+)
   - Tích hợp Google Maps API
   - Real-time traffic data

3. **UI Improvements:**
   - Map visualization
   - Route preview
   - Export to PDF/Calendar

---

**Last Updated:** 2025-11-28
**Version:** 2.3 (Renamed Core Modules)
