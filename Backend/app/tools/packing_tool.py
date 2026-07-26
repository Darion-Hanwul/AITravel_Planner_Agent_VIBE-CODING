class PackingTool:
    def __init__(self):
        pass

    def generate_packing_list(self, destination: str, duration_days: int, weather_condition: str) -> dict:
        items = ["Paspor", "Pakaian Utama", "Pengisi Daya Elektronik", "Perlengkapan Mandi"]
        if "rain" in weather_condition.lower():
            items.append("Payung / Jas Hujan")
        if "cold" in weather_condition.lower() or "snow" in weather_condition.lower():
            items.append("Jaket Tebal & Sarung Tangan")
        return {
            "destination": destination,
            "duration": duration_days,
            "suggested_items": items
        }