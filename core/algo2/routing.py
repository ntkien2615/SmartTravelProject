#core/routing.py — Algo2: Tìm đường đi với OSRM + Nominatim
import time
import requests

NOMINATIM = "https://nominatim.openstreetmap.org"
OSRM = "https://router.project-osrm.org"
UA = {"User-Agent": "SmartTravel-Web/1.0"}

def geocode(address):
    """
    Chuyển địa chỉ thành tọa độ (lat, lon).
    Returns: (lat, lon, display_name) hoặc None nếu lỗi
    """
    try:
        time.sleep(1.0)  # Rate limiting
        r = requests.get(
            f"{NOMINATIM}/search", 
            params={"q": address, "format": "jsonv2", "limit": 1}, 
            headers=UA,
            timeout=10
        )
        r.raise_for_status()
        j = r.json()
        if not j:
            return None
        return float(j[0]["lat"]), float(j[0]["lon"]), j[0].get("display_name", address)
    except Exception as e:
        print(f"Geocode error: {e}")
        return None

def osrm_route(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Tìm đường đi bằng OSRM API.
    vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy)
    
    Returns: {
        'distance_km': float,
        'duration_min': float,
        'steps': [{'instruction': str, 'street': str, 'distance_m': float}, ...]
    }
    hoặc None nếu lỗi
    """
    try:
        r = requests.get(
            f"{OSRM}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}",
            params={"overview": "false", "steps": "true"}, 
            headers=UA,
            timeout=15
        )
        r.raise_for_status()
        data = r.json()
        
        if not data.get("routes"):
            return None
            
        route = data["routes"][0]
        distance_km = route["distance"] / 1000.0
        duration_min = route["duration"] / 60.0
        
        # Extract step-by-step directions
        steps = []
        for leg in route["legs"]:
            for step in leg["steps"]:
                instruction = step.get("maneuver", {}).get("instruction", "Tiếp tục")
                street = step.get("name", "")
                distance_m = step.get("distance", 0)
                steps.append({
                    "instruction": instruction,
                    "street": street,
                    "distance_m": distance_m
                })
        
        return {
            "distance_km": distance_km,
            "duration_min": duration_min,
            "steps": steps
        }
    except Exception as e:
        print(f"OSRM error: {e}")
        return None

def get_directions(start_address, end_address, vehicle_type="driving"):
    """
    Hàm chính: Lấy chỉ dẫn từ địa chỉ đầu đến địa chỉ cuối.
    
    Args:
        start_address: Địa chỉ bắt đầu
        end_address: Địa chỉ kết thúc
        vehicle_type: "driving" hoặc "bike"
    
    Returns: {
        'start': {'lat': float, 'lon': float, 'name': str},
        'end': {'lat': float, 'lon': float, 'name': str},
        'route': {'distance_km': float, 'duration_min': float, 'steps': [...]},
        'vehicle': str
    }
    hoặc None nếu lỗi
    """
    # Geocode start
    start_geo = geocode(start_address)
    if not start_geo:
        return None
    lat1, lon1, name1 = start_geo
    
    # Geocode end
    end_geo = geocode(end_address)
    if not end_geo:
        return None
    lat2, lon2, name2 = end_geo
    
    # Get route
    route = osrm_route(lon1, lat1, lon2, lat2, vehicle_type)
    if not route:
        return None
    
    return {
        "start": {"lat": lat1, "lon": lon1, "name": name1},
        "end": {"lat": lat2, "lon": lon2, "name": name2},
        "route": route,
        "vehicle": vehicle_type
    }
