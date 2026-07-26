import requests

class FlightTool:
    def __init__(self):
        self.mock_data = True

    def search_flights(self, origin: str, destination: str, departure_date: str) -> dict:
        return {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "flights": [
                {"carrier": "Garuda Indonesia", "flight_number": "GA-882", "price": 450.00, "currency": "USD"},
                {"carrier": "Japan Airlines", "flight_number": "JL-726", "price": 520.00, "currency": "USD"}
            ]
        }