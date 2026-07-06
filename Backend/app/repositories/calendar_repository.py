from datetime import date
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.calendar import CalendarEvent
from app.repositories.base_repository import BaseRepository


class CalendarRepository(BaseRepository[CalendarEvent]):

    def __init__(self):
        super().__init__(CalendarEvent)

    def get_by_activity(
        self,
        db: Session,
        activity_id: UUID,
    ) -> CalendarEvent | None:

        return (
            db.query(CalendarEvent)
            .filter(CalendarEvent.activity_id == activity_id)
            .first()
        )

    def get_by_date(
        self,
        db: Session,
        event_date: date,
    ) -> list[CalendarEvent]:

        return (
            db.query(CalendarEvent)
            .filter(CalendarEvent.event_date == event_date)
            .order_by(CalendarEvent.start_time.asc())
            .all()
        )

    def get_between_dates(
        self,
        db: Session,
        start_date: date,
        end_date: date,
    ) -> list[CalendarEvent]:

        return (
            db.query(CalendarEvent)
            .filter(
                CalendarEvent.event_date >= start_date,
                CalendarEvent.event_date <= end_date,
            )
            .order_by(
                CalendarEvent.event_date.asc(),
                CalendarEvent.start_time.asc(),
            )
            .all()
        )

    def get_reminder_events(
        self,
        db: Session,
    ) -> list[CalendarEvent]:

        return (
            db.query(CalendarEvent)
            .filter(CalendarEvent.reminder.is_(True))
            .order_by(
                CalendarEvent.event_date.asc(),
                CalendarEvent.start_time.asc(),
            )
            .all()
        )

    def delete_by_activity(
        self,
        db: Session,
        activity_id: UUID,
    ) -> bool:

        event = (
            db.query(CalendarEvent)
            .filter(CalendarEvent.activity_id == activity_id)
            .first()
        )

        if event is None:
            return False

        db.delete(event)
        db.commit()

        return True