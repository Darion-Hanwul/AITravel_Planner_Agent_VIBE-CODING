import requests

class MapsTool:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"

    def get_coordinates(self, place_name: str) -> dict:
        headers = {"User-Agent": "TravelPlannerAgent/1.0"}
        params = {"q": place_name, "format": "json", "limit": 1}
        response = requests.get(f"{self.base_url}/search", params=params, headers=headers).json()
        if response:
            return {
                "place": place_name,
                "latitude": float(response[0]["lat"]),
                "longitude": float(response[0]["lon"])
            }
        return {"error": "Location not found"}