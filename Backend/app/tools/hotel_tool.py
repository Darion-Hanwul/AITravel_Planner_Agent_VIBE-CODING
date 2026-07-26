class HotelTool:
    def __init__(self):
        self.base_search = True

    def search_hotels(self, location: str, stars: int, budget_max: float) -> dict:
        return {
            "location": location,
            "star_rating_filter": stars,
            "hotels": [
                {"name": "Grand Tokyo Hotel", "stars": 4, "price_per_night": 120.00, "currency": "USD"},
                {"name": "Shibuya Capsule Inn", "stars": 3, "price_per_night": 45.00, "currency": "USD"}
            ]
        }