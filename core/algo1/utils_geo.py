#core/algo1/utils_geo.py — Hàm hỗ trợ khoảng cách, thời gian, chi phí
import math
from .config import SPEEDS_KMH, COST_PER_KM

def haversine_km(a, b):
    R = 6371
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def travel_info(a, b, mode="motorbike"):
    d = haversine_km(a, b)
    speed = SPEEDS_KMH.get(mode, 25)
    time_min = (d / speed) * 60
    cost = d * COST_PER_KM.get(mode, 0)
    return d, time_min, cost
