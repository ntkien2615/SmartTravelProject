#core/routing.py — Algo2: Tìm đường đi với OSRM + Nominatim
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

NOMINATIM = "https://nominatim.openstreetmap.org"
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def _fetch_osrm_data(lon1, lat1, lon2, lat2, vehicle_type, params):
    session = get_session()
    
    # List of servers to try
    servers = [
        "https://router.project-osrm.org",
        "http://router.project-osrm.org"
    ]
    
    # Add FOSSGIS servers as fallback
    if vehicle_type == "driving":
        servers.append("https://routing.openstreetmap.de/routed-car")
    elif vehicle_type == "bike":
        servers.append("https://routing.openstreetmap.de/routed-bike")
        
    for server in servers:
        try:
            url = f"{server}/route/v1/{vehicle_type}/{lon1},{lat1};{lon2},{lat2}"
            r = session.get(url, params=params, headers=UA, timeout=30)
            r.raise_for_status()
            data = r.json()
            if data.get("code") == "Ok":
                return data
        except Exception as e:
            print(f"Error connecting to {server}: {e}")
            continue
            
    return None

def geocode(location_name):
    """
    Tìm tọa độ từ tên địa điểm sử dụng Open-Meteo Geocoding API.
    """
    def _search(query):
        try:
            url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": query,
                "count": 1,
                "language": "vi",
                "format": "json"
            }
            headers = {"User-Agent": "MyWeatherApp/1.0"}
            r = requests.get(url, params=params, headers=headers, timeout=5)
            r.raise_for_status()
            data = r.json()
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"], result["name"]
        except Exception:
            return None
        return None

    # 0. Chuẩn hóa tên địa điểm phổ biến
    location_name = location_name.replace("TP.HCM", "Hồ Chí Minh").replace("TPHCM", "Hồ Chí Minh").replace("Sài Gòn", "Hồ Chí Minh")

    # 1. Thử tìm chính xác
    res = _search(location_name)
    if res: return res

    # 2. Thử bỏ phần sau dấu phẩy (ví dụ: "Dinh Độc Lập, TPHCM" -> "Dinh Độc Lập")
    if "," in location_name:
        simple_name = location_name.split(",")[0].strip()
        res = _search(simple_name)
        if res: return res
        
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
        data = _fetch_osrm_data(lon1, lat1, lon2, lat2, vehicle_type, {"overview": "full", "geometries": "geojson", "steps": "true"})
        
        if not data or not data.get("routes"):
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
            "steps": steps,
            "geometry": route["geometry"]
        }
    except Exception as e:
        print(f"OSRM error: {e}")
        return None

def get_route_geometry(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Lấy hình học tuyến đường để vẽ bản đồ.
    
    Args:
        lon1, lat1: Tọa độ điểm bắt đầu
        lon2, lat2: Tọa độ điểm đích
        vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy)
        
    Returns:
        tuple: (geometry, distance_km, duration_hours)
    """
    try:
        data = _fetch_osrm_data(lon1, lat1, lon2, lat2, vehicle_type, {"overview": "full", "geometries": "geojson"})
        
        if not data or not data.get("routes"):
            return None, None, None

        route = data["routes"][0]
        
        return (
            route["geometry"],
            route["distance"] / 1000.0,
            route["duration"] / 3600.0
        )
    except Exception as e:
        print(f"Route geometry error: {e}")
        return None, None, None


def get_route_steps(lon1, lat1, lon2, lat2, vehicle_type="driving"):
    """
    Lấy các bước chỉ dẫn chi tiết.
    
    Args:
        lon1, lat1: Tọa độ điểm bắt đầu
        lon2, lat2: Tọa độ điểm đích
        vehicle_type: "driving" (ô tô) hoặc "bike" (xe máy)
        
    Returns:
        dict: Thông tin route với keys: distance_km, duration_min, steps
    """
    route = osrm_route(lon1, lat1, lon2, lat2, vehicle_type)
    if not route:
        return None
    
    # Convert steps format for compatibility
    steps = []
    for step in route.get("steps", []):
        steps.append({
            "instruction": step.get("instruction", "Tiếp tục"),
            "street_name": step.get("street", ""),
            "distance": step.get("distance_m", 0)
        })
    
    return {
        "distance_km": route["distance_km"],
        "duration_min": route["duration_min"],
        "steps": steps
    }


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
