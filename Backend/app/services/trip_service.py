from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.constants import TripStatus
from app.core.exceptions import (
    TripNotFoundError,
    TripValidationError,
)

from app.models.trip import Trip
from app.models.trip_day import TripDay
from app.models.activity import Activity

from app.repositories.trip_repository import (
    ActivityRepository,
    TripDayRepository,
    TripRepository,
)

from app.repositories.calendar_repository import (
    CalendarRepository,
)

from app.schemas.trip import (
    TripCreate,
    TripDetailResponse,
    TripResponse,
    TripUpdate,
)

from app.services.base_service import BaseService

class TripService(BaseService):
    """
    Business logic untuk seluruh proses Trip.

    Bertanggung jawab terhadap:

    - Create Trip
    - Update Trip
    - Delete Trip
    - Trip Detail
    - Trip Day
    - Activity
    - Calendar Integration
    """
    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.trip_repository = TripRepository()

        self.trip_day_repository = TripDayRepository()

        self.activity_repository = ActivityRepository()

        self.calendar_repository = CalendarRepository()

    #PRIVATE HELPERS

    def _get_trip(
        self,
        trip_id: UUID,
    ) -> Trip:
        """
        Mengambil Trip berdasarkan ID.

        Raises
        ------
        TripNotFoundError
        """

        trip = self.trip_repository.get_by_id(
            self.db,
            trip_id,
        )

        if trip is None:

            raise TripNotFoundError(
                "Trip not found.",
            )

        return trip
    
    def _validate_trip_owner(
        self,
        trip: Trip,
        user_id: UUID,
    ) -> None:
        """
        Memastikan user adalah pemilik trip.
        """

        if trip.user_id != user_id:

            raise TripValidationError(
                "You do not have access to this trip.",
            )
    
    def _ensure_trip_editable(
        self,
        trip: Trip,
    ) -> None:
        """
        Memastikan trip masih dapat diubah.
        """

        if trip.status in (
            TripStatus.COMPLETED.value,
            TripStatus.CANCELLED.value,
        ):

            raise TripValidationError(
                "Trip can no longer be modified.",
            )
        
    def _validate_budget(
        self,
        budget: Decimal,
    ) -> None:
        """
        Memastikan budget valid.
        """

        if budget < 0:

            raise TripValidationError(
                "Budget cannot be negative.",
            )
    
    def _validate_date(
        self,
        start_date: date,
        end_date: date,
    ) -> None:
        """
        Memastikan rentang tanggal valid.
        """

        if end_date < start_date:

            raise TripValidationError(
                "End date must be after start date.",
            )
        
    def _change_status(
        self,
        trip: Trip,
        status: TripStatus,
    ) -> None:
        """
        Mengubah status trip.
        """

        trip.status = status.value

        self.trip_repository.update(
            self.db,
            trip,
        )

    def _to_response(
        self,
        trip: Trip,
    ) -> TripResponse:
        """
        Mapping ORM menjadi Response Schema.
        """

        return TripResponse.model_validate(
            trip,
        )

    #PUBLIC METHODS

    def create_trip(
        self,
        user_id: UUID,
        data: TripCreate,
    ) -> TripResponse:
        """
        Membuat trip baru.
        """

        self._validate_budget(
            data.budget,
        )

        self._validate_date(
            data.start_date,
            data.end_date,
        )

        trip = Trip(
            user_id=user_id,
            title=data.title,
            destination=data.destination,
            start_date=data.start_date,
            end_date=data.end_date,
            budget=data.budget,
            total_estimated_cost=data.budget,
            status=TripStatus.PLANNING.value,
        )
        try:

            self.trip_repository.create(
                self.db,
                trip,
            )

            self.commit()

            self.refresh(
                trip,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            trip,
        )
    
    def get_trip(
        self,
        trip_id: UUID,
    ) -> TripResponse:
        """
        Mengambil satu trip.
        """

        trip = self._get_trip(
            trip_id,
        )

        return self._to_response(
            trip,
        )
    
    def get_user_trips(
        self,
        user_id: UUID,
    ) -> list[TripResponse]:
        """
        Mengambil seluruh trip milik user.
        """

        trips = self.trip_repository.get_by_user(
            self.db,
            user_id,
        )

        return [
            self._to_response(
                trip,
            )
            for trip in trips
        ]
    
    def update_trip(
        self,
        trip_id: UUID,
        data: TripUpdate,
    ) -> TripResponse:
        """
        Mengubah informasi trip.
        """

        trip = self._get_trip(
            trip_id,
        )

        if data.title is not None:
            trip.title = data.title

        if data.destination is not None:
            trip.destination = data.destination

        if data.start_date is not None:
            trip.start_date = data.start_date

        if data.end_date is not None:
            trip.end_date = data.end_date

        if (
            data.start_date is not None
            or data.end_date is not None
        ):
            self._validate_date(
                trip.start_date,
                trip.end_date,
            )

        if data.budget is not None:

            self._validate_budget(
                data.budget,
            )

            trip.budget = data.budget

        if data.total_estimated_cost is not None:

            self._validate_budget(
                data.total_estimated_cost,
            )

            trip.total_estimated_cost = (
                data.total_estimated_cost
            )

        if data.status is not None:
            trip.status = data.status.value

        try:

            self.trip_repository.update(
                self.db,
                trip,
            )

            self.commit()

            self.refresh(
                trip,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            trip,
        )
    
    def delete_trip(
        self,
        trip_id: UUID,
    ) -> None:
        """
        Menghapus trip.
        """

        trip = self._get_trip(
            trip_id,
        )

        try:

            self.trip_repository.delete(
                self.db,
                trip,
            )

            self.commit()

        except Exception:

            self.rollback()

            raise

    def change_status(
        self,
        trip_id: UUID,
        status: TripStatus,
    ) -> TripResponse:
        """
        Mengubah status trip.
        """

        trip = self._get_trip(
            trip_id,
        )

        trip.status = status.value

        try:

            self.trip_repository.update(
                self.db,
                trip,
            )

            self.commit()

            self.refresh(
                trip,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            trip,
        )
    
    def calculate_total_cost(
        self,
        trip_id: UUID,
    ) -> Decimal:
        """
        Menghitung total estimasi biaya seluruh activity.
        """

        trip = self.trip_repository.get_trip_detail(
            self.db,
            trip_id,
        )

        if trip is None:

            raise TripNotFoundError(
                "Trip not found.",
            )

        total = Decimal("0.00")

        for day in trip.trip_days:

            for activity in day.activities:

                if activity.estimated_cost is not None:

                    total += activity.estimated_cost

        trip.total_estimated_cost = total

        self.trip_repository.update(
            self.db,
            trip,
        )

        self.commit()

        self.refresh(
            trip,
        )

        return total
    
    def create_trip_day(
        self,
        trip_day: TripDay,
    ) -> TripDay:
        """
        Membuat hari baru pada trip.
        """

        self.trip_day_repository.create(
            self.db,
            trip_day,
        )

        self.commit()

        self.refresh(
            trip_day,
        )

        return trip_day
    
    def create_activity(
        self,
        activity: Activity,
    ) -> Activity:
        """
        Menambahkan activity ke Trip Day.
        """

        self.activity_repository.create(
            self.db,
            activity,
        )

        self.commit()

        self.refresh(
            activity,
        )

        return activity
    
    def delete_activity(
        self,
        activity: Activity,
    ) -> None:
        """
        Menghapus activity.
        """

        self.activity_repository.delete(
            self.db,
            activity,
        )

        self.commit()

    def get_trip_detail(
        self,
        trip_id: UUID,
    ) -> TripDetailResponse:
        """
        Mengambil detail lengkap trip beserta
        TripDay, Activity, dan Calendar.
        """

        trip = self.trip_repository.get_trip_detail(
            self.db,
            trip_id,
        )

        if trip is None:

            raise TripNotFoundError(
                "Trip not found.",
            )

        return TripDetailResponse.model_validate(
            trip,
        )