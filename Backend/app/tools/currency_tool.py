import uuid
import requests
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.db.models import CurrencyHistory
from app.config.settings import settings

class CurrencyTool:
    def __init__(self, db: Session):
        self.db = db
        self.base_url = "https://v6.exchangerate-api.com/v6"
        self.api_key = "0676cee8865b14cff5b13028"

    def convert(self, from_curr: str, to_curr: str, amount: float) -> dict:
        url = f"{self.base_url}/{self.api_key}/pair/{from_curr.upper()}/{to_curr.upper()}"
        response = requests.get(url).json()
        if response.get("result") == "success":
            rate = response.get("conversion_rate")
            converted = amount * rate
            history = CurrencyHistory(
                id=uuid.uuid4(),
                base_currency=from_curr.upper(),
                target_currency=to_curr.upper(),
                exchange_rate=Decimal(str(rate)),
                fetched_at=datetime.utcnow()
            )
            self.db.add(history)
            self.db.commit()
            return {"rate": rate, "converted_amount": converted}
        return {"error": "Conversion failed"}