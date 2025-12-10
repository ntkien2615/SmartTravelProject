#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý thời tiết - lấy thông tin thời tiết từ OpenWeatherMap
"""

import requests

def get_weather(lat, lon):
    """
    Lấy thông tin thời tiết cho một địa điểm sử dụng wttr.in (không cần API Key).
    
    Args:
        lat, lon: Tọa độ địa điểm
        
    Returns:
        dict: Thông tin thời tiết hoặc None nếu lỗi
    """
    try:
        # Sử dụng wttr.in với format JSON (j1) và ngôn ngữ tiếng Việt
        url = f"https://wttr.in/{lat},{lon}?format=j1&lang=vi"
        
        # Thêm User-Agent để tránh bị chặn
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        current = data["current_condition"][0]
        
        # Lấy mô tả thời tiết (ưu tiên tiếng Việt)
        description = ""
        if "lang_vi" in current:
            description = current["lang_vi"][0]["value"]
        elif "weatherDesc" in current:
            description = current["weatherDesc"][0]["value"]
            
        # Chuyển đổi tốc độ gió từ km/h sang m/s
        wind_speed_kmph = float(current["windspeedKmph"])
        wind_speed_ms = round(wind_speed_kmph / 3.6, 1)
        
        return {
            "temp": float(current["temp_C"]),
            "feels_like": float(current["FeelsLikeC"]),
            "humidity": int(current["humidity"]),
            "description": description,
            "wind_speed": wind_speed_ms
        }
    except (requests.exceptions.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"Weather Error: {e}")
        return None

