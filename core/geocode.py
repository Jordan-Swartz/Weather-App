import requests

BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"

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