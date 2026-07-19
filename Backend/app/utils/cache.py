"""
Cache Utilities.

Utility untuk membantu validasi cache
berdasarkan waktu kedaluwarsa.
"""

from __future__ import annotations

from datetime import datetime, timedelta


def is_cache_valid(
    fetched_at: datetime | None,
    expire_minutes: int,
) -> bool:
    """
    Mengecek apakah cache masih berlaku.

    Args:
        fetched_at:
            Waktu cache dibuat.

        expire_minutes:
            Lama cache berlaku (menit).

    Returns:
        bool
    """

    if fetched_at is None:
        return False

    expire_time = fetched_at + timedelta(
        minutes=expire_minutes,
    )

    return datetime.utcnow() < expire_time


def get_expire_time(
    fetched_at: datetime,
    expire_minutes: int,
) -> datetime:
    """
    Menghasilkan waktu kedaluwarsa cache.
    """

    return fetched_at + timedelta(
        minutes=expire_minutes,
    )


def get_remaining_seconds(
    fetched_at: datetime | None,
    expire_minutes: int,
) -> int:
    """
    Menghitung sisa umur cache dalam detik.

    Returns:
        0 jika cache telah kedaluwarsa.
    """

    if fetched_at is None:
        return 0

    expire_time = get_expire_time(
        fetched_at,
        expire_minutes,
    )

    remaining = (
        expire_time - datetime.utcnow()
    ).total_seconds()

    return max(
        int(remaining),
        0,
    )