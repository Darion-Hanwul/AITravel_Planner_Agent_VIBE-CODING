"""
TravelPlannerAgent Repository Layer
"""

from .base_repository import BaseRepository

from .user_repository import (
    UserRepository,
    UserPreferenceRepository,
)

from .trip_repository import (
    TripRepository,
    TripDayRepository,
    ActivityRepository,
    CalendarRepository,
)

from .chat_repository import (
    ChatSessionRepository,
    ChatMessageRepository,
)

from .document_repository import (
    DocumentRepository,
)

from .currency_repository import (
    CurrencyRepository,
)

from .weather_repository import (
    WeatherRepository,
)

from .saved_place_repository import (
    SavedPlaceRepository,
)

from .tool_log_repository import (
    ToolLogRepository,
)

from .instances import (
    user_repository,
    user_preference_repository,
    trip_repository,
    trip_day_repository,
    activity_repository,
    calendar_repository,
    chat_session_repository,
    chat_message_repository,
    document_repository,
    currency_repository,
    weather_repository,
    saved_place_repository,
    tool_log_repository,
)

__all__ = [
    "BaseRepository",

    "UserRepository",
    "UserPreferenceRepository",

    "TripRepository",
    "TripDayRepository",
    "ActivityRepository",
    "CalendarRepository",

    "ChatSessionRepository",
    "ChatMessageRepository",

    "DocumentRepository",

    "CurrencyRepository",

    "WeatherRepository",

    "SavedPlaceRepository",

    "ToolLogRepository",

    "user_repository",
    "user_preference_repository",
    "trip_repository",
    "trip_day_repository",
    "activity_repository",
    "calendar_repository",
    "chat_session_repository",
    "chat_message_repository",
    "document_repository",
    "currency_repository",
    "weather_repository",
    "saved_place_repository",
    "tool_log_repository",
]