# Danh sách API & Dịch vụ sử dụng trong dự án

Dự án Smart Travel sử dụng các API và dịch vụ sau đây. Hầu hết là mã nguồn mở và miễn phí.

## 1. Bản đồ & Định vị (Map & Geocoding)

### Nominatim (OpenStreetMap)
- **Chức năng**: Chuyển đổi tên địa điểm sang tọa độ (Geocoding) và ngược lại.
- **URL**: `https://nominatim.openstreetmap.org`
- **Sử dụng**: 
  - Tìm kiếm địa điểm chính xác (POI).
  - Ưu tiên số 1 trong module `core/map_integration/routing.py`.
- **Lưu ý**: Cần set `User-Agent` và `Referer` để tránh lỗi 403.

### Photon (Komoot)
- **Chức năng**: Geocoding dự phòng (Fallback).
- **URL**: `https://photon.komoot.io/api/`
- **Sử dụng**: 
  - Tìm kiếm khi Nominatim bị lỗi hoặc quá tải.
  - Tốc độ nhanh, ít bị chặn.

### Open-Meteo Geocoding
- **Chức năng**: Geocoding dự phòng cuối cùng.
- **URL**: `https://geocoding-api.open-meteo.com/v1/search`
- **Sử dụng**: 
  - Tìm kiếm tên thành phố, quận huyện nếu các dịch vụ trên thất bại.

## 2. Dẫn đường & Giao thông (Routing)

### OSRM (Open Source Routing Machine)
- **Chức năng**: Tìm đường đi, tính toán khoảng cách và thời gian di chuyển.
- **URL**: `https://router.project-osrm.org`
- **Sử dụng**: 
  - Tính toán lộ trình cho Ô tô (`driving`) và Xe máy (`bike` - sử dụng server thay thế nếu cần).
  - Trả về geometry để vẽ bản đồ và các bước chỉ dẫn (steps).

## 3. Thời tiết (Weather)

### Open-Meteo Weather API
- **Chức năng**: Cung cấp dữ liệu thời tiết hiện tại và dự báo.
- **URL**: `https://api.open-meteo.com/v1/forecast`
- **Sử dụng**: 
  - Lấy nhiệt độ, độ ẩm, tốc độ gió, UV index.
  - Dự báo thời tiết 3 ngày tới.
  - Không cần API Key.

## 4. Cơ sở dữ liệu & Backend

### Supabase
- **Chức năng**: Backend-as-a-Service (BaaS).
- **Sử dụng**: 
  - Authentication (Đăng ký/Đăng nhập).
  - Database (PostgreSQL) để lưu trữ User và Lịch trình (Schedules).
- **Cấu hình**: Yêu cầu `SUPABASE_URL` và `SUPABASE_KEY` trong file `.env`.

## 5. AI & Machine Learning (Local)

### PyTorch (ResNet18)
- **Chức năng**: Nhận diện địa điểm qua ảnh.
- **Loại**: Offline Model (chạy local, không gọi API).
- **File**: `core/image_recognition/model_vietnam.pth`.
