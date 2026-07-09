from datetime import date, time
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
    ValidationError,
)

from app.models.calendar import CalendarEvent

from app.repositories.calendar_repository import (
    CalendarRepository,
)

from app.schemas.calendar import (
    CalendarEventCreate,
    CalendarEventResponse,
    CalendarEventUpdate,
)

from app.services.base_service import BaseService


class CalendarService(BaseService):
    """
    Business logic untuk Calendar Event.

    Bertanggung jawab terhadap:

    - Create Calendar Event
    - Update Calendar Event
    - Delete Calendar Event
    - Get Calendar Event
    - Get Calendar by Date
    - Reminder Event
    """

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.calendar_repository = CalendarRepository()

    # ======================================================
    # PRIVATE HELPERS
    # ======================================================

    def _get_event(
        self,
        event_id: UUID,
    ) -> CalendarEvent:
        """
        Mengambil calendar event berdasarkan ID.

        Raises
        ------
        ResourceNotFoundError
        """

        event = self.calendar_repository.get_by_id(
            self.db,
            event_id,
        )

        if event is None:

            raise ResourceNotFoundError(
                "Calendar event not found.",
            )

        return event

    def _validate_time(
        self,
        start_time: time,
        end_time: time,
    ) -> None:
        """
        Memastikan jam selesai tidak
        lebih awal dari jam mulai.
        """

        if end_time <= start_time:

            raise ValidationError(
                "End time must be after start time.",
            )
        
    def _validate_date_range(
        self,
        start_date: date,
        end_date: date,
    ) -> None:
        """
        Memastikan rentang tanggal valid.
        """

        self._validate_date_range(
            start_date,
            end_date,
        )

    def _to_response(
        self,
        event: CalendarEvent,
    ) -> CalendarEventResponse:
        """
        Mapping ORM menjadi Response Schema.
        """

        return CalendarEventResponse.model_validate(
            event,
        )
    
    # ======================================================
    # PUBLIC METHODS
    # ======================================================

    def create_event(
        self,
        data: CalendarEventCreate,
    ) -> CalendarEventResponse:
        """
        Membuat Calendar Event baru.
        """

        self._validate_time(
            data.start_time,
            data.end_time,
        )

        event = CalendarEvent(
            activity_id=data.activity_id,
            event_title=data.event_title,
            event_date=data.event_date,
            start_time=data.start_time,
            end_time=data.end_time,
            reminder=data.reminder,
        )

        try:

            self.calendar_repository.create(
                self.db,
                event,
            )

            self.commit()

            self.refresh(
                event,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            event,
        )

    def get_event(
        self,
        event_id: UUID,
    ) -> CalendarEventResponse:
        """
        Mengambil satu Calendar Event.
        """

        event = self._get_event(
            event_id,
        )

        return self._to_response(
            event,
        )

    def update_event(
        self,
        event_id: UUID,
        data: CalendarEventUpdate,
    ) -> CalendarEventResponse:
        """
        Mengubah Calendar Event.
        """

        event = self._get_event(
            event_id,
        )

        if data.event_title is not None:
            event.event_title = data.event_title

        if data.event_date is not None:
            event.event_date = data.event_date

        if data.start_time is not None:
            event.start_time = data.start_time

        if data.end_time is not None:
            event.end_time = data.end_time

        if (
            data.start_time is not None
            or data.end_time is not None
        ):
            self._validate_time(
                event.start_time,
                event.end_time,
            )

        if data.reminder is not None:
            event.reminder = data.reminder

        try:

            self.calendar_repository.update(
                self.db,
                event,
            )

            self.commit()

            self.refresh(
                event,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            event,
        )

    def delete_event(
        self,
        event_id: UUID,
    ) -> None:
        """
        Menghapus Calendar Event.
        """

        event = self._get_event(
            event_id,
        )

        try:

            self.calendar_repository.delete(
                self.db,
                event,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise

    def get_events_by_date(
        self,
        event_date: date,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh event pada tanggal tertentu.
        """

        events = self.calendar_repository.get_by_date(
            self.db,
            event_date,
        )

        return [
            self._to_response(
                event,
            )
            for event in events
        ]

    def get_events_between(
        self,
        start_date: date,
        end_date: date,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh event dalam rentang tanggal.
        """

        if end_date < start_date:

            raise ValidationError(
                "End date must be after start date.",
            )

        events = self.calendar_repository.get_between_dates(
            self.db,
            start_date,
            end_date,
        )

        return [
            self._to_response(
                event,
            )
            for event in events
        ]

    def get_reminder_events(
        self,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh event yang memiliki reminder.
        """

        events = self.calendar_repository.get_reminder_events(
            self.db,
        )

        return [
            self._to_response(
                event,
            )
            for event in events
        ]
    