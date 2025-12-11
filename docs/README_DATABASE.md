# Hướng Dẫn Cấu Hình Database (Supabase)

Hiện tại dự án sử dụng Supabase để lưu trữ dữ liệu người dùng và lịch trình.
Bạn cần tạo các bảng trong Supabase để ứng dụng hoạt động đúng.

## Bước 1: Truy cập Supabase

1. Đăng nhập vào [Supabase Dashboard](https://supabase.com/dashboard).
2. Chọn Project của bạn.

## Bước 2: Mở SQL Editor

1. Ở thanh bên trái, chọn biểu tượng **SQL Editor**.
2. Nhấn **New query**.

## Bước 3: Chạy Script Tạo Bảng

1. Mở file `supabase_schema.sql` trong thư mục dự án này.
2. Copy toàn bộ nội dung của file.
3. Paste vào SQL Editor trên Supabase.
4. Nhấn **Run** (hoặc Ctrl+Enter).

## Bước 4: Kiểm Tra

1. Vào mục **Table Editor** (thanh bên trái).
2. Bạn sẽ thấy 2 bảng mới: `users` và `schedules`.

Sau khi hoàn tất, ứng dụng sẽ có thể lưu trữ và truy xuất dữ liệu.
