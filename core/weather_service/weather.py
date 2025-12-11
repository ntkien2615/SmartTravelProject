#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module xử lý thời tiết - lấy thông tin thời tiết từ OpenWeatherMap
"""

import requests

def get_weather_description(code):
    """Chuyển đổi mã WMO sang mô tả tiếng Việt"""
    wmo_codes = {
        0: "Trời quang",
        1: "Ít mây",
        2: "Mây rải rác",
        3: "Nhiều mây",
        45: "Sương mù",
        48: "Sương mù đọng băng",
        51: "Mưa phùn nhẹ",
        53: "Mưa phùn vừa",
        55: "Mưa phùn dày",
        56: "Mưa phùn băng giá nhẹ",
        57: "Mưa phùn băng giá dày",
        61: "Mưa nhỏ",
        63: "Mưa vừa",
        65: "Mưa to",
        66: "Mưa băng giá nhẹ",
        67: "Mưa băng giá nặng",
        71: "Tuyết rơi nhẹ",
        73: "Tuyết rơi vừa",
        75: "Tuyết rơi dày",
        77: "Tuyết hạt",
        80: "Mưa rào nhẹ",
        81: "Mưa rào vừa",
        82: "Mưa rào rất to",
        85: "Mưa tuyết nhẹ",
        86: "Mưa tuyết nặng",
        95: "Dông nhẹ hoặc vừa",
        96: "Dông mạnh",
        99: "Dông rất mạnh"
    }
    return wmo_codes.get(code, "Không xác định")

def get_weather(lat, lon):
    """
    Lấy thông tin thời tiết cho một địa điểm sử dụng Open-Meteo.
    
    Args:
        lat, lon: Tọa độ địa điểm
        
    Returns:
        dict: Thông tin thời tiết hoặc None nếu lỗi
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,uv_index_max",
            "timezone": "auto",
            "forecast_days": 4  # Lấy hôm nay + 3 ngày tới
        }
        
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        current = data["current"]
        daily = data["daily"]
        
        # Xử lý dự báo (bỏ qua hôm nay - index 0, lấy 3 ngày tiếp theo)
        forecast = []
        for i in range(1, 4):
            if i < len(daily["time"]):
                forecast.append({
                    "date": daily["time"][i],
                    "max_temp": daily["temperature_2m_max"][i],
                    "min_temp": daily["temperature_2m_min"][i],
                    "description": get_weather_description(daily["weather_code"][i]),
                    "uv": daily.get("uv_index_max", [0]*4)[i]
                })

        return {
            "temp": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "description": get_weather_description(current["weather_code"]),
            "wind_speed": current["wind_speed_10m"],
            "forecast": forecast
        }
    except Exception as e:
        print(f"Weather Error: {e}")

        return None

