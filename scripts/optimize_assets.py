from PIL import Image
import os

def optimize_image(filepath):
    try:
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        
        # Chỉ xử lý file ảnh
        if ext.lower() not in ['.png', '.jpg', '.jpeg']:
            return
            
        print(f"Đang xử lý: {filename} ({os.path.getsize(filepath) / 1024 / 1024:.2f} MB)")
        
        with Image.open(filepath) as img:
            # Chuyển sang RGB nếu là RGBA (để lưu thành JPG)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
                
            # Resize nếu quá lớn (giữ nguyên tỉ lệ, max width 1920)
            if img.width > 1920:
                ratio = 1920 / img.width
                new_height = int(img.height * ratio)
                img = img.resize((1920, new_height), Image.Resampling.LANCZOS)
            
            # Tạo tên file mới .jpg
            new_filename = f"{name}_optimized.jpg"
            new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
            
            # Lưu với chất lượng 80
            img.save(new_filepath, "JPEG", quality=80, optimize=True)
            
            print(f" -> Đã tạo: {new_filename} ({os.path.getsize(new_filepath) / 1024 / 1024:.2f} MB)")
            return new_filename
            
    except Exception as e:
        print(f"Lỗi khi xử lý {filepath}: {e}")
        return None

# Đường dẫn thư mục
bg_dir = r"d:\doantuduytinhtoan\assets\background"
files = ["section-1.png", "section-2.png"]

optimized_files = {}

for f in files:
    path = os.path.join(bg_dir, f)
    if os.path.exists(path):
        new_name = optimize_image(path)
        if new_name:
            optimized_files[f] = new_name

print("Hoàn tất tối ưu hóa.")
