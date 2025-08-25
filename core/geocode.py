import requests

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
IP_URL = "https://ipapi.co/json/"

def search_places(query: str, count: int, language: str):
    #build query
    params = {"name": query, "count": count, "language": language}

    #send request
    req_obj = requests.get(BASE_URL, params=params, timeout=10)
    req_obj.raise_for_status()

    #process and normalize response into usable obj
    resp_obj = req_obj.json()
    results = resp_obj.get("results") or []

    places = []
    for r in results:
        label_parts = [r["name"], r.get("admin1"), r.get("country")]
        label = ", ".join([p for p in label_parts if p])
        places.append({
            "label": label,
            "lat": r["latitude"],
            "lon": r["longitude"],
        })
    return places

def get_ip_location():
    resp = requests.get(IP_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    lat = data.get("latitude")
    lon = data.get("longitude")
    if lat is None or lon is None:
        raise ValueError("IP lookup returned no coordinates")

    label = ", ".join(
        [p for p in [data.get("city"), data.get("region"), data.get("country_name")] if p]) or "My location"
    return {"label": label, "lat": lat, "lon": lon}