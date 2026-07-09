from enum import StrEnum


class TripStatus(StrEnum):
    """
    Status perjalanan.
    """

    PLANNING = "planning"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"