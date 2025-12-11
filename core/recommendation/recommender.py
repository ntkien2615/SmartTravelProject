import os
import pandas as pd
# Import load_pois from sibling package
# Note: In a real package structure, this might need adjustment depending on how it's run.
# But since we are running from root (app.py), absolute imports from core... work.
from core.route_optimization import load_pois

def recommend_places(csv_path, user_prefs, num_results=20, min_rating=3.5):
    """
    Gợi ý địa điểm dựa trên sở thích người dùng.
    
    Args:
        csv_path (str): Đường dẫn đến file CSV dữ liệu POI.
        user_prefs (list): Danh sách các tags sở thích (ví dụ: ['food', 'history']).
        num_results (int): Số lượng kết quả tối đa trả về.
        min_rating (float): Đánh giá tối thiểu.
        
    Returns:
        list: Danh sách các địa điểm (dict) đã được sắp xếp theo rating giảm dần.
    """
    if not user_prefs:
        return []

    # Sử dụng hàm load_pois có sẵn để lọc theo tags và rating
    # load_pois đã xử lý việc lọc theo tags (OR logic - có ít nhất 1 tag)
    pois = load_pois(
        csv_path, 
        filter_tags=user_prefs,
        min_rating=min_rating,
        max_pois=None  # Lấy tất cả để sort chính xác hơn
    )
    
    if not pois:
        return []
        
    # Sắp xếp theo rating giảm dần
    # Có thể mở rộng thêm logic scoring phức tạp hơn ở đây nếu cần
    pois_sorted = sorted(pois, key=lambda x: x.get('rating', 0), reverse=True)
    
    return pois_sorted[:num_results]
