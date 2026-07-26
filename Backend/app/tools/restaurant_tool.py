class RestaurantTool:
    def __init__(self):
        pass

    def search_restaurants(self, location: str, food_preference: str) -> dict:
        return {
            "location": location,
            "cuisine": food_preference,
            "recommendations": [
                {"name": "Ichiran Ramen", "rating": 4.8, "avg_cost": 15.00},
                {"name": "Local Street Food Market", "rating": 4.5, "avg_cost": 8.00}
            ]
        }