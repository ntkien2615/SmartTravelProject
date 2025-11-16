# Script dọn dẹp project - Xóa các file/folder thừa
# Chạy script này để tái tổ chức project

Write-Host "🧹 BẮT ĐẦU DỌN DẸP PROJECT..." -ForegroundColor Cyan
Write-Host ""

# Danh sách các file/folder CẦN XÓA (không dùng nữa)
$itemsToRemove = @(
    "SmartTravel.py",           # File cũ, đã thay bằng app.py
    "flask_backend.py",         # Không dùng Flask backend
    "src",                      # Thư mục cũ, đã thay bằng pages/
    "static",                   # CSS đã copy vào root
    "frontend",                 # Chỉ còn flowchart, có thể giữ hoặc xóa
    "page_chuc_nang_new.py",   # File thử nghiệm, đã merge vào pages/
    "__pycache__"               # Python cache, sẽ tự tạo lại
)

# Danh sách các file/folder KHÔNG XÓA (đang dùng)
$keepItems = @(
    "app.py",                   # ✅ Main entry point
    "pages/",                   # ✅ Modular pages
    "core/",                    # ✅ Algo1 - thuật toán
    "data/",                    # ✅ POIs data
    "db_utils.py",              # ✅ Database utilities
    "utils.py",                 # ✅ Helper functions
    "style.css",                # ✅ CSS styling
    "requirements.txt",         # ✅ Dependencies
    "README.md",                # ✅ Documentation
    "smarttravel.db",           # ✅ SQLite database
    "run_demo.py",              # ✅ Algo test script
    "algo1-flowchart.md",       # ✅ Algorithm docs
    "CODE_RULES.md",            # ✅ Development rules
    "CHANGELOG*.md",            # ✅ Change logs
    "LICENSE",                  # ✅ License file
    ".git/",                    # ✅ Git repository
    ".gitignore",               # ✅ Git ignore rules
    "start.ps1"                 # ✅ Start script
)

Write-Host "📋 CÁC FILE/FOLDER SẼ BỊ XÓA:" -ForegroundColor Yellow
foreach ($item in $itemsToRemove) {
    if (Test-Path $item) {
        Write-Host "  ❌ $item" -ForegroundColor Red
    } else {
        Write-Host "  ⚠️  $item (không tồn tại)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "✅ CÁC FILE/FOLDER SẼ GIỮ LẠI:" -ForegroundColor Green
foreach ($item in $keepItems) {
    if (Test-Path $item) {
        Write-Host "  ✓ $item" -ForegroundColor Green
    }
}

Write-Host ""
$confirm = Read-Host "Bạn có chắc muốn xóa các file trên? (y/n)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host ""
    Write-Host "🗑️  ĐANG XÓA..." -ForegroundColor Yellow
    
    foreach ($item in $itemsToRemove) {
        if (Test-Path $item) {
            try {
                Remove-Item $item -Recurse -Force
                Write-Host "  ✅ Đã xóa: $item" -ForegroundColor Green
            } catch {
                Write-Host "  ❌ Lỗi khi xóa: $item - $_" -ForegroundColor Red
            }
        }
    }
    
    Write-Host ""
    Write-Host "✨ HOÀN TẤT!" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📁 CẤU TRÚC PROJECT SAU KHI DỌN DẸP:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "doantuduytinhtoan/" -ForegroundColor White
    Write-Host "├── app.py                  # 🚀 Main entry point" -ForegroundColor White
    Write-Host "├── pages/                  # 📄 Modular pages" -ForegroundColor White
    Write-Host "│   ├── page_trang_chu.py" -ForegroundColor DarkGray
    Write-Host "│   ├── page_gioi_thieu.py" -ForegroundColor DarkGray
    Write-Host "│   ├── page_chuc_nang.py  # 🔍 Tích hợp algo1" -ForegroundColor Yellow
    Write-Host "│   ├── page_ho_so.py" -ForegroundColor DarkGray
    Write-Host "│   └── page_sign_in_up.py" -ForegroundColor DarkGray
    Write-Host "├── core/                   # 🧠 Algo1 - Thuật toán tối ưu" -ForegroundColor White
    Write-Host "│   ├── solver_route.py     # Greedy + Lookahead" -ForegroundColor Yellow
    Write-Host "│   ├── scorer.py" -ForegroundColor DarkGray
    Write-Host "│   ├── optimizer.py" -ForegroundColor DarkGray
    Write-Host "│   ├── utils_geo.py" -ForegroundColor DarkGray
    Write-Host "│   └── config.py" -ForegroundColor DarkGray
    Write-Host "├── data/                   # 📊 POIs data" -ForegroundColor White
    Write-Host "│   └── pois_hcm.csv" -ForegroundColor DarkGray
    Write-Host "├── db_utils.py             # 🗄️ Database" -ForegroundColor White
    Write-Host "├── utils.py                # 🛠️ Helpers" -ForegroundColor White
    Write-Host "├── style.css               # 🎨 Styling" -ForegroundColor White
    Write-Host "├── smarttravel.db          # 💾 SQLite DB" -ForegroundColor White
    Write-Host "├── requirements.txt        # 📦 Dependencies" -ForegroundColor White
    Write-Host "├── README.md               # 📖 Documentation" -ForegroundColor White
    Write-Host "└── run_demo.py             # 🧪 Test algo1" -ForegroundColor White
    Write-Host ""
    Write-Host "🚀 Để chạy app: streamlit run app.py" -ForegroundColor Cyan
    Write-Host "🧪 Để test algo1: python run_demo.py" -ForegroundColor Cyan
    
} else {
    Write-Host ""
    Write-Host "❌ ĐÃ HỦY. Không có file nào bị xóa." -ForegroundColor Yellow
}

Write-Host ""
