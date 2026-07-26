class VisaTool:
    def __init__(self):
        pass

    def check_requirement(self, citizen_country: str, destination_country: str) -> dict:
        if citizen_country.lower() == "indonesia" and destination_country.lower() == "jepang":
            return {
                "requirement": "Visa Required / E-Visa (Visa Waiver Available for e-passport)",
                "max_stay_days": 15,
                "notes": "Registrasi pra-keberangkatan diperlukan untuk bebas visa IC."
            }
        return {
            "requirement": "Standard Tourist Visa Required",
            "max_stay_days": 30,
            "notes": "Hubungi kedutaan besar terkait sebelum jadwal keberangkatan."
        }