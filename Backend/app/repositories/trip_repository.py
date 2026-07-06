from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from decimal import Decimal
from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.models.activity import Activity
from app.models.calendar import CalendarEvent

from app.repositories.base_repository import BaseRepository


class TripRepository(BaseRepository[Trip]):

    def __init__(self):
        super().__init__(Trip)

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[Trip]:

        return (
            db.query(Trip)
            .filter(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
            .all()
        )

    def get_trip_detail(
        self,
        db: Session,
        trip_id: UUID,
    ) -> Optional[Trip]:

        return (
            db.query(Trip)
            .options(
                joinedload(Trip.trip_days)
                .joinedload(TripDay.activities)
                .joinedload(Activity.calendar_event)
            )
            .filter(Trip.id == trip_id)
            .first()
        )

    def update_status(
        self,
        db: Session,
        trip: Trip,
        status: str,
    ) -> Trip:

        trip.status = status

        return self.update(db, trip)

    def update_total_cost(
        self,
        db: Session,
        trip: Trip,
        total_cost: Decimal,
    ) -> Trip:

        trip.total_estimated_cost = total_cost

        return self.update(db, trip)


class TripDayRepository(BaseRepository[TripDay]):

    def __init__(self):
        super().__init__(TripDay)

    def get_by_trip(
        self,
        db: Session,
        trip_id: UUID,
    ) -> list[TripDay]:

        return (
            db.query(TripDay)
            .filter(TripDay.trip_id == trip_id)
            .order_by(TripDay.day_number.asc())
            .all()
        )


class ActivityRepository(BaseRepository[Activity]):

    def __init__(self):
        super().__init__(Activity)

    def get_by_trip_day(
        self,
        db: Session,
        trip_day_id: UUID,
    ) -> list[Activity]:

        return (
            db.query(Activity)
            .filter(Activity.trip_day_id == trip_day_id)
            .order_by(Activity.start_time.asc())
            .all()
        )


class CalendarRepository(BaseRepository[CalendarEvent]):

    def __init__(self):
        super().__init__(CalendarEvent)

    def get_by_activity(
        self,
        db: Session,
        activity_id: UUID,
    ) -> Optional[CalendarEvent]:

        return (
            db.query(CalendarEvent)
            .filter(CalendarEvent.activity_id == activity_id)
            .first()
        )