from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import seluruh model

from app.models.user import User
from app.models.preference import UserPreference
from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.models.activity import Activity
from app.models.calendar import CalendarEvent
from app.models.place import SavedPlace
from app.models.session import ChatSession
from app.models.message import ChatMessage
from app.models.document import Document
from app.models.currency import CurrencyHistory
from app.models.weather import WeatherCache
from app.models.tool_log import ToolLog