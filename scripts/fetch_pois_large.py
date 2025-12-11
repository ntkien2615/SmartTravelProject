#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script lấy 1000-10000 POIs từ OpenStreetMap cho TP.HCM
Bao gồm: restaurants, cafes, shops, parks, museums, hotels, banks, hospitals, schools, etc.
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# TP.HCM bbox (mở rộng để bao gồm cả ngoại thành)
BBOX = "10.3,106.3,11.2,107.1"

def query_overpass(query, timeout=180):
    """Gửi query đến Overpass API với retry"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"    Attempt {attempt + 1}/{max_retries}...", end=" ")
            response = requests.post(
                OVERPASS_URL, 
                data={"data": query}, 
                timeout=timeout
            )
            response.raise_for_status()
            print("✓")
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 60 * (attempt + 1)
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"HTTP Error: {e}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(10)
            else:
                return None
    return None

def get_pois_comprehensive(category_queries, max_per_query=5000):
    """
    Lấy POIs toàn diện từ nhiều categories
    """
    all_pois = []
    total_categories = len(category_queries)
    
    for idx, cat_info in enumerate(category_queries, 1):
        category_name = cat_info["name"]
        tags = cat_info["tags"]
        queries = cat_info["queries"]
        
        print(f"\n[{idx}/{total_categories}] 🔍 {category_name}")
        
        for query_str in queries:
            query = f"""
            [out:json][timeout:180];
            (
              {query_str}
            );
            out center {max_per_query};
            """
            
            data = query_overpass(query)
            if not data or "elements" not in data:
                continue
            
            count = 0
            for element in data["elements"]:
                # Lấy tọa độ
                if "lat" in element and "lon" in element:
                    lat, lon = element["lat"], element["lon"]
                elif "center" in element:
                    lat, lon = element["center"]["lat"], element["center"]["lon"]
                else:
                    continue
                
                # Lấy thông tin từ tags
                elem_tags = element.get("tags", {})
                name = elem_tags.get("name", elem_tags.get("name:vi", elem_tags.get("name:en", "")))
                
                # Skip nếu không có tên hoặc tên quá ngắn
                if not name or len(name) < 2:
                    # Thử lấy brand hoặc operator
                    name = elem_tags.get("brand", elem_tags.get("operator", ""))
                    if not name or len(name) < 2:
                        continue
                
                # Rating (random 3.5-4.9)
                rating = 3.5 + (hash(name + str(lat)) % 15) / 10
                
                # Visit duration theo category
                visit_duration = cat_info.get("duration", 60)
                
                # Entry fee
                entry_fee = 0
                if elem_tags.get("fee") == "yes":
                    entry_fee = 20000 + (hash(name) % 8) * 10000
                elif "museum" in tags or "attraction" in tags:
                    entry_fee = 30000 + (hash(name) % 6) * 10000
                
                # Opening hours
                opening_hours = elem_tags.get("opening_hours", "")
                open_hour = cat_info.get("open_hour", 8)
                close_hour = cat_info.get("close_hour", 18)
                
                if "24/7" in opening_hours or "hotel" in tags:
                    open_hour = 0
                    close_hour = 23
                
                poi = {
                    "name": name,
                    "lat": round(lat, 6),
                    "lon": round(lon, 6),
                    "tags": tags,
                    "rating": round(rating, 1),
                    "visit_duration_min": visit_duration,
                    "entry_fee": entry_fee,
                    "open_hour": open_hour,
                    "close_hour": close_hour,
                }
                
                all_pois.append(poi)
                count += 1
            
            print(f"      → Collected {count} POIs")
            time.sleep(3)  # Rate limiting
    
    return all_pois

def main():
    print("="*80)
    print("   🗺️  LẤY DỮ LIỆU LỚN: 1000-10000 POIs TỪ OPENSTREETMAP (TP.HCM)")
    print("="*80)
    
    # Định nghĩa categories chi tiết
    category_queries = [
        # 1. Restaurants & Food (500+)
        {
            "name": "Restaurants & Dining",
            "tags": "food;restaurant",
            "queries": [
                f'node["amenity"="restaurant"]({BBOX});',
                f'way["amenity"="restaurant"]({BBOX});',
            ],
            "duration": 90,
            "open_hour": 10,
            "close_hour": 22
        },
        # 2. Cafes & Bakeries (300+)
        {
            "name": "Cafes & Bakeries",
            "tags": "food;cafe",
            "queries": [
                f'node["amenity"="cafe"]({BBOX});',
                f'way["amenity"="cafe"]({BBOX});',
            ],
            "duration": 60,
            "open_hour": 7,
            "close_hour": 22
        },
        # 3. Fast Food (200+)
        {
            "name": "Fast Food",
            "tags": "food;fast_food",
            "queries": [
                f'node["amenity"="fast_food"]({BBOX});',
                f'way["amenity"="fast_food"]({BBOX});',
            ],
            "duration": 30,
            "open_hour": 8,
            "close_hour": 22
        },
        # 4. Bars & Pubs (100+)
        {
            "name": "Bars & Nightlife",
            "tags": "nightlife;bar",
            "queries": [
                f'node["amenity"="bar"]({BBOX});',
                f'node["amenity"="pub"]({BBOX});',
            ],
            "duration": 120,
            "open_hour": 18,
            "close_hour": 2
        },
        # 5. Shops - General (500+)
        {
            "name": "Shops - General",
            "tags": "shopping;retail",
            "queries": [
                f'node["shop"="supermarket"]({BBOX});',
                f'node["shop"="convenience"]({BBOX});',
                f'node["shop"="mall"]({BBOX});',
                f'way["shop"="mall"]({BBOX});',
            ],
            "duration": 120,
            "open_hour": 8,
            "close_hour": 22
        },
        # 6. Shops - Specialty (300+)
        {
            "name": "Specialty Shops",
            "tags": "shopping;specialty",
            "queries": [
                f'node["shop"="clothes"]({BBOX});',
                f'node["shop"="books"]({BBOX});',
                f'node["shop"="electronics"]({BBOX});',
                f'node["shop"="jewelry"]({BBOX});',
            ],
            "duration": 90,
            "open_hour": 9,
            "close_hour": 21
        },
        # 7. Parks & Recreation (200+)
        {
            "name": "Parks & Recreation",
            "tags": "park;nature;relaxation",
            "queries": [
                f'node["leisure"="park"]({BBOX});',
                f'way["leisure"="park"]({BBOX});',
                f'node["leisure"="garden"]({BBOX});',
            ],
            "duration": 45,
            "open_hour": 5,
            "close_hour": 22
        },
        # 8. Museums & Culture (100+)
        {
            "name": "Museums & Galleries",
            "tags": "history;museum;culture",
            "queries": [
                f'node["tourism"="museum"]({BBOX});',
                f'node["tourism"="gallery"]({BBOX});',
                f'way["tourism"="museum"]({BBOX});',
            ],
            "duration": 90,
            "open_hour": 8,
            "close_hour": 17
        },
        # 9. Hotels & Accommodation (300+)
        {
            "name": "Hotels & Accommodation",
            "tags": "accommodation;hotel",
            "queries": [
                f'node["tourism"="hotel"]({BBOX});',
                f'node["tourism"="hostel"]({BBOX});',
                f'way["tourism"="hotel"]({BBOX});',
            ],
            "duration": 0,
            "open_hour": 0,
            "close_hour": 23
        },
        # 10. Banks & ATMs (400+)
        {
            "name": "Banks & Finance",
            "tags": "service;bank;finance",
            "queries": [
                f'node["amenity"="bank"]({BBOX});',
                f'node["amenity"="atm"]({BBOX});',
            ],
            "duration": 30,
            "open_hour": 8,
            "close_hour": 17
        },
        # 11. Healthcare (200+)
        {
            "name": "Healthcare",
            "tags": "service;healthcare;hospital",
            "queries": [
                f'node["amenity"="hospital"]({BBOX});',
                f'node["amenity"="clinic"]({BBOX});',
                f'node["amenity"="pharmacy"]({BBOX});',
            ],
            "duration": 60,
            "open_hour": 7,
            "close_hour": 22
        },
        # 12. Schools & Education (300+)
        {
            "name": "Education",
            "tags": "education;school",
            "queries": [
                f'node["amenity"="school"]({BBOX});',
                f'node["amenity"="university"]({BBOX});',
                f'node["amenity"="college"]({BBOX});',
            ],
            "duration": 0,
            "open_hour": 7,
            "close_hour": 17
        },
        # 13. Religious Sites (200+)
        {
            "name": "Religious Sites",
            "tags": "religious;culture;worship",
            "queries": [
                f'node["amenity"="place_of_worship"]({BBOX});',
                f'way["amenity"="place_of_worship"]({BBOX});',
            ],
            "duration": 45,
            "open_hour": 6,
            "close_hour": 18
        },
        # 14. Entertainment (150+)
        {
            "name": "Entertainment",
            "tags": "entertainment;attraction",
            "queries": [
                f'node["tourism"="attraction"]({BBOX});',
                f'node["amenity"="cinema"]({BBOX});',
                f'node["leisure"="sports_centre"]({BBOX});',
            ],
            "duration": 120,
            "open_hour": 9,
            "close_hour": 22
        },
        # 15. Transportation (300+)
        {
            "name": "Transportation",
            "tags": "service;transport",
            "queries": [
                f'node["amenity"="bus_station"]({BBOX});',
                f'node["amenity"="fuel"]({BBOX});',
                f'node["amenity"="parking"]({BBOX});',
            ],
            "duration": 15,
            "open_hour": 0,
            "close_hour": 23
        },
        # 16. Beauty & Wellness (200+)
        {
            "name": "Beauty & Wellness",
            "tags": "service;beauty;wellness",
            "queries": [
                f'node["shop"="beauty"]({BBOX});',
                f'node["shop"="hairdresser"]({BBOX});',
                f'node["leisure"="fitness_centre"]({BBOX});',
            ],
            "duration": 90,
            "open_hour": 8,
            "close_hour": 21
        },
        # 17. Landmarks (100+)
        {
            "name": "Historic Landmarks",
            "tags": "history;landmark",
            "queries": [
                f'node["historic"]({BBOX});',
                f'node["tourism"="viewpoint"]({BBOX});',
            ],
            "duration": 60,
            "open_hour": 8,
            "close_hour": 18
        },
        # 18. Markets (100+)
        {
            "name": "Markets",
            "tags": "shopping;food;market",
            "queries": [
                f'node["amenity"="marketplace"]({BBOX});',
                f'way["amenity"="marketplace"]({BBOX});',
            ],
            "duration": 90,
            "open_hour": 6,
            "close_hour": 18
        },
    ]
    
    # Lấy POIs
    print(f"\n🚀 Bắt đầu thu thập {len(category_queries)} categories...")
    print(f"⏰ Ước tính: ~{len(category_queries) * 5} phút\n")
    
    start_time = datetime.now()
    all_pois = get_pois_comprehensive(category_queries)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60
    
    print(f"\n{'='*80}")
    print(f"📊 Thu thập xong! Tổng số POIs: {len(all_pois):,}")
    print(f"⏱️  Thời gian: {duration:.1f} phút")
    print(f"{'='*80}")
    
    # Tạo DataFrame
    df = pd.DataFrame(all_pois)
    
    # Loại bỏ duplicates
    print(f"\n🧹 Đang làm sạch dữ liệu...")
    initial_count = len(df)
    
    # Loại bỏ duplicate theo tên + tọa độ gần nhau (trong bán kính 50m)
    df["lat_round"] = (df["lat"] * 100).round()
    df["lon_round"] = (df["lon"] * 100).round()
    df = df.drop_duplicates(subset=["name", "lat_round", "lon_round"], keep="first")
    df = df.drop(columns=["lat_round", "lon_round"])
    
    print(f"  • Removed {initial_count - len(df):,} duplicates")
    print(f"  • Final count: {len(df):,} POIs")
    
    # Thêm ID
    df.insert(0, "id", range(1, len(df) + 1))
    
    # Sắp xếp
    df = df.sort_values(["tags", "rating", "name"], ascending=[True, False, True])
    df["id"] = range(1, len(df) + 1)
    
    # Lưu file
    output_file = "data/pois_hcm_large.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
    
    print(f"\n{'='*80}")
    print(f"✅ ĐÃ LƯU {len(df):,} POIs VÀO: {output_file}")
    print(f"{'='*80}")
    
    # Thống kê
    print("\n📊 THỐNG KÊ THEO CATEGORY:")
    stats = df.groupby("tags").size().sort_values(ascending=False)
    for tag, count in stats.items():
        print(f"  • {tag}: {count:,} POIs")
    
    print(f"\n📈 PHÂN PHỐI RATING:")
    print(f"  • 4.5-5.0: {len(df[df['rating'] >= 4.5]):,} POIs")
    print(f"  • 4.0-4.4: {len(df[(df['rating'] >= 4.0) & (df['rating'] < 4.5)]):,} POIs")
    print(f"  • 3.5-3.9: {len(df[(df['rating'] >= 3.5) & (df['rating'] < 4.0)]):,} POIs")
    
    # Sample POIs
    print(f"\n🎯 SAMPLE POIs (random 10):")
    sample = df.sample(min(10, len(df)))
    for _, row in sample.iterrows():
        print(f"  {row['id']}. {row['name']} - {row['rating']}⭐ ({row['tags']})")
    
    print(f"\n💡 Để sử dụng trong web:")
    print(f"   csv_path = 'data/pois_hcm_large.csv'")
    print(f"\n⚠️  LƯU Ý: Dataset lớn có thể làm chậm thuật toán.")
    print(f"   Cân nhắc lọc theo tags hoặc rating trước khi dùng.\n")

if __name__ == "__main__":
    main()
