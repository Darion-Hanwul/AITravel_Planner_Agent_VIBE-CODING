from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.calendar import CalendarEvent
from app.repositories.base_repository import BaseRepository


class CalendarRepository(
    BaseRepository[CalendarEvent]
):

    def __init__(self) -> None:
        super().__init__(CalendarEvent)

    def get_by_activity(
        self,
        db: Session,
        activity_id: UUID,
    ) -> CalendarEvent | None:

        stmt = (
            select(CalendarEvent)
            .where(
                CalendarEvent.activity_id == activity_id
            )
        )

        return db.scalar(stmt)

    def get_by_date(
        self,
        db: Session,
        event_date: date,
    ) -> list[CalendarEvent]:

        stmt = (
            select(CalendarEvent)
            .where(
                CalendarEvent.event_date == event_date
            )
            .order_by(
                CalendarEvent.start_time.asc()
            )
        )

        return list(
            db.scalars(stmt)
        )

    def get_between_dates(
        self,
        db: Session,
        start_date: date,
        end_date: date,
    ) -> list[CalendarEvent]:

        stmt = (
            select(CalendarEvent)
            .where(
                CalendarEvent.event_date >= start_date,
                CalendarEvent.event_date <= end_date,
            )
            .order_by(
                CalendarEvent.event_date.asc(),
                CalendarEvent.start_time.asc(),
            )
        )

        return list(
            db.scalars(stmt)
        )

    def get_reminder_events(
        self,
        db: Session,
    ) -> list[CalendarEvent]:

        stmt = (
            select(CalendarEvent)
            .where(
                CalendarEvent.reminder.is_(True)
            )
            .order_by(
                CalendarEvent.event_date.asc(),
                CalendarEvent.start_time.asc(),
            )
        )

        return list(
            db.scalars(stmt)
        )

    def delete_by_activity(
        self,
        db: Session,
        activity_id: UUID,
    ) -> bool:

        event = self.get_by_activity(
            db,
            activity_id,
        )

        if event is None:
            return False

        self.delete(
            db,
            event,
        )

        return True