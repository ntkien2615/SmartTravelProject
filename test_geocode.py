import requests

def geocode(location_name):
    """
    Tìm tọa độ từ tên địa điểm sử dụng Open-Meteo Geocoding API.
    """
    def _search(query):
        try:
            url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {
                "name": query,
                "count": 5,
                "language": "vi",
                "format": "json"
            }
            headers = {"User-Agent": "MyWeatherApp/1.0"}
            print(f"Searching for: {query}")
            r = requests.get(url, params=params, headers=headers, timeout=5)
            r.raise_for_status()
            data = r.json()
            if "results" in data and len(data["results"]) > 0:
                print(f"Found {len(data['results'])} results")
                result = data["results"][0]
                return result["latitude"], result["longitude"], result["name"]
            else:
                print("No results found")
        except Exception as e:
            print(f"Error: {e}")
            return None
        return None

    # 1. Thử tìm chính xác
    res = _search(location_name)
    if res: return res

    # 2. Thử bỏ phần sau dấu phẩy (ví dụ: "Dinh Độc Lập, TPHCM" -> "Dinh Độc Lập")
    if "," in location_name:
        simple_name = location_name.split(",")[0].strip()
        res = _search(simple_name)
        if res: return res
        
    return None

print("Testing 'TP.HCM, Việt Nam':", geocode("TP.HCM, Việt Nam"))
print("Testing 'Hồ Chí Minh':", geocode("Hồ Chí Minh"))
print("Testing 'Saigon':", geocode("Saigon"))
