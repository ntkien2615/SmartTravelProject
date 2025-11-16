# 📁 CẤU TRÚC PROJECT - SMART TRAVEL OPTIMIZATION

## 🎯 Tổng Quan
Project được tổ chức lại theo cấu trúc modular, tách biệt rõ ràng giữa:
- **Web Interface** (Streamlit)
- **Algorithm Core** (Algo1)
- **Data & Database**

---

## 📂 Cấu Trúc Thư Mục

```
SmartTravelProject/
│
├── 🚀 app.py                      # Main entry point - Chạy web app
│
├── 📄 pages/                      # Modular pages (Web interface)
│   ├── page_trang_chu.py         # Trang chủ
│   ├── page_gioi_thieu.py        # Giới thiệu
│   ├── page_chuc_nang.py         # ⭐ Chức năng (tích hợp algo1)
│   ├── page_ho_so.py             # Hồ sơ người dùng
│   └── page_sign_in_up.py        # Đăng nhập/Đăng ký
│
├── 🧠 core/                       # Algo1 - Thuật toán tối ưu
│   ├── solver_route.py           # ⭐ Main algorithm (Greedy + Lookahead)
│   ├── scorer.py                 # Đánh giá và chấm điểm POI
│   ├── optimizer.py              # Tối ưu hậu kỳ (2-opt)
│   ├── utils_geo.py              # Tính khoảng cách, thời gian, chi phí
│   ├── config.py                 # Cấu hình (speeds, costs, weights)
│   └── __init__.py
│
├── 📊 data/                       # Dữ liệu
│   └── pois_hcm.csv              # POIs Hồ Chí Minh (20 địa điểm)
│
├── 🗄️ Database & Utilities
│   ├── db_utils.py               # SQLite database operations
│   ├── utils.py                  # Helper functions (time conversion)
│   └── smarttravel.db            # SQLite database (users, schedules)
│
├── 🎨 Frontend Assets
│   └── style.css                 # CSS styling cho web
│
├── 🧪 Testing & Demo
│   ├── run_demo.py               # Test algo1 độc lập
│   └── algo1-flowchart.md        # Flowchart thuật toán
│
├── 📦 Configuration
│   ├── requirements.txt          # Python dependencies
│   ├── .gitignore                # Git ignore rules
│   └── start.ps1                 # PowerShell start script
│
├── 📖 Documentation
│   ├── README.md                 # Main documentation
│   ├── CHANGELOG.md              # Change history
│   ├── CHANGELOG_v2.md           # Version 2 changes
│   ├── CODE_RULES.md             # Development rules
│   ├── PROJECT_STRUCTURE.md     # ⭐ This file
│   └── LICENSE                   # License
│
└── 🧹 Scripts
    └── cleanup_project.ps1       # Script dọn dẹp file thừa
```

---

## 🔗 Luồng Hoạt Động

### 1. **User Interface Flow**
```
app.py
  ├── pages/page_trang_chu.py    → Home page
  ├── pages/page_chuc_nang.py    → ⭐ Tích hợp algo1
  │     └── calls: core/solver_route.plan_route()
  └── pages/page_ho_so.py        → Profile & saved schedules
```

### 2. **Algorithm Flow (Algo1)**
```
pages/page_chuc_nang.py
  └── core/solver_route.plan_route()
        ├── load_pois() from data/pois_hcm.csv
        ├── core/scorer.score_candidate()
        ├── core/utils_geo.travel_info()
        └── Return optimized route
```

### 3. **Data Flow**
```
User Input → page_chuc_nang.py → algo1 → Optimized Route → Display
                                    ↓
                            Save to smarttravel.db (via db_utils.py)
```

---

## 🚀 Cách Chạy

### Chạy Web App (Streamlit)
```bash
streamlit run app.py
# hoặc
python -m streamlit run app.py
```

### Test Thuật Toán Riêng
```bash
python run_demo.py
```

### Dọn Dẹp Project
```powershell
.\cleanup_project.ps1
```

---

## ⚙️ Cấu Hình Algo1

File `core/config.py` chứa các tham số:
```python
SPEEDS_KMH = {"walking": 5.0, "motorbike": 25.0, "taxi": 35.0}
COST_PER_KM = {"walking": 0.0, "motorbike": 2000.0, "taxi": 12000.0}

# Trọng số scoring
ALPHA = 1.0      # Travel time weight
BETA = 0.5       # Visit duration weight
GAMMA = 0.000001 # Cost scaling
DELTA = 2.0      # Rating bonus
EPSILON = 3.0    # Preference bonus
```

---

## 📊 Dữ Liệu POIs

File `data/pois_hcm.csv` format:
```csv
id,name,lat,lon,tags,rating,visit_duration_min,entry_fee,open_hour,close_hour
1,Nhà thờ Đức Bà,10.7797,106.6990,history;landmark;religious,4.5,45,0,8,17
```

**Columns:**
- `id`: Unique identifier
- `name`: Tên địa điểm
- `lat`, `lon`: Tọa độ GPS
- `tags`: Danh sách tag (phân cách bằng `;`)
- `rating`: Đánh giá (0-5)
- `visit_duration_min`: Thời gian tham quan (phút)
- `entry_fee`: Phí vào cửa (VND)
- `open_hour`, `close_hour`: Giờ mở/đóng cửa

---

## 🔧 Thêm POIs Mới

Chỉnh sửa `data/pois_hcm.csv`:
```csv
21,Địa điểm mới,10.xxxx,106.xxxx,food;shopping,4.5,60,0,8,22
```

Restart app để load dữ liệu mới.

---

## 📦 Dependencies

Xem file `requirements.txt`:
```txt
streamlit
pandas
numpy
```

---

## 🧹 Files Đã Xóa (Không Dùng Nữa)

Các file sau đã được đánh dấu xóa bởi `cleanup_project.ps1`:
- ❌ `SmartTravel.py` - Entry point cũ
- ❌ `flask_backend.py` - Flask backend không dùng
- ❌ `src/` - Thư mục cấu trúc cũ
- ❌ `static/` - CSS đã copy sang root
- ❌ `page_chuc_nang_new.py` - File test
- ❌ `__pycache__/` - Python cache

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

## 📞 Liên Hệ

- **GitHub:** [HoangCaoPhong/SmartTravelProject](https://github.com/HoangCaoPhong/SmartTravelProject)
- **Email:** hcphong2425@clc.fitus.edu.vn

---

**Last Updated:** 2025-11-16
**Version:** 2.0 (Modular + Algo1 Integrated)
