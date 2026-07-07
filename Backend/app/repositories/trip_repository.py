from decimal import Decimal
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.models.activity import Activity
from app.models.calendar import CalendarEvent
from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.repositories.base_repository import BaseRepository


class TripRepository(BaseRepository[Trip]):

    def __init__(self) -> None:
        super().__init__(Trip)

    # =====================================================
    # GET TRIPS BY USER
    # =====================================================

    def get_by_user(
        self,
        db: Session,
        user_id: UUID,
    ) -> list[Trip]:

        stmt = (
            select(Trip)
            .where(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
        )

        return list(db.scalars(stmt))

    # =====================================================
    # GET COMPLETE TRIP
    # =====================================================

    def get_trip_detail(
        self,
        db: Session,
        trip_id: UUID,
    ) -> Optional[Trip]:

        stmt = (
            select(Trip)
            .options(
                joinedload(Trip.trip_days)
                .joinedload(TripDay.activities)
                .joinedload(Activity.calendar_event)
            )
            .where(Trip.id == trip_id)
        )

        return db.scalar(stmt)

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    def update_status(
        self,
        db: Session,
        trip: Trip,
        status: str,
    ) -> Trip:

        trip.status = status

        return self.update(
            db,
            trip,
        )

    # =====================================================
    # UPDATE TOTAL COST
    # =====================================================

    def update_total_cost(
        self,
        db: Session,
        trip: Trip,
        total_cost: Decimal,
    ) -> Trip:

        trip.total_estimated_cost = total_cost

        return self.update(
            db,
            trip,
        )


class TripDayRepository(BaseRepository[TripDay]):

    def __init__(self) -> None:
        super().__init__(TripDay)

    # =====================================================
    # GET BY TRIP
    # =====================================================

    def get_by_trip(
        self,
        db: Session,
        trip_id: UUID,
    ) -> list[TripDay]:

        stmt = (
            select(TripDay)
            .where(TripDay.trip_id == trip_id)
            .order_by(TripDay.day_number.asc())
        )

        return list(
            db.scalars(stmt)
        )


class ActivityRepository(BaseRepository[Activity]):

    def __init__(self) -> None:
        super().__init__(Activity)

    # =====================================================
    # GET BY TRIP DAY
    # =====================================================

    def get_by_trip_day(
        self,
        db: Session,
        trip_day_id: UUID,
    ) -> list[Activity]:

        stmt = (
            select(Activity)
            .where(
                Activity.trip_day_id == trip_day_id
            )
            .order_by(
                Activity.start_time.asc()
            )
        )

        return list(
            db.scalars(stmt)
        )