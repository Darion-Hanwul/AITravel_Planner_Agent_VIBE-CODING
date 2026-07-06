from app.repositories.user_repository import (
    UserRepository,
    UserPreferenceRepository,
)

from app.repositories.trip_repository import (
    TripRepository,
    TripDayRepository,
    ActivityRepository,
    CalendarRepository,
)

from app.repositories.chat_repository import (
    ChatSessionRepository,
    ChatMessageRepository,
)

from app.repositories.document_repository import (
    DocumentRepository,
)

from app.repositories.currency_repository import (
    CurrencyRepository,
)

from app.repositories.weather_repository import (
    WeatherRepository,
)

from app.repositories.saved_place_repository import (
    SavedPlaceRepository,
)

from app.repositories.tool_log_repository import (
    ToolLogRepository,
)


user_repository = UserRepository()

user_preference_repository = UserPreferenceRepository()

trip_repository = TripRepository()

trip_day_repository = TripDayRepository()

activity_repository = ActivityRepository()

calendar_repository = CalendarRepository()

chat_session_repository = ChatSessionRepository()

chat_message_repository = ChatMessageRepository()

document_repository = DocumentRepository()

currency_repository = CurrencyRepository()

weather_repository = WeatherRepository()

saved_place_repository = SavedPlaceRepository()

tool_log_repository = ToolLogRepository()