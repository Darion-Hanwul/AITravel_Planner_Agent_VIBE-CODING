from __future__ import annotations

from app.ai.sources.source import Source
from app.ai.sources.travel_sources import TRAVEL_SOURCES


class SourceRegistry:
    """
    Registry pusat untuk manajemen seluruh kompilasi knowledge source aktif.

    Responsibility
    --------------
    - Menampung seluruh data source yang terdaftar di dalam aplikasi.
    - Menyediakan antarmuka pencarian data source berdasarkan filter kategori dan nama.
    - Menjamin hanya data source berstatus aktif (enabled=True) yang dialirkan ke sistem.

    Tidak bertanggung jawab terhadap:
    - Proses pemanggilan HTTP request eksternal (tugas Loaders/Sources konkrit).
    """

    # Menggabungkan seluruh data source travel yang terdaftar
    SOURCES: list[Source] = [
        *TRAVEL_SOURCES,
    ]

    @classmethod
    def get_all(cls) -> list[Source]:
        """
        Mengambil seluruh daftar knowledge source yang berstatus aktif di dalam sistem.

        Responsibility
        --------------
        Menyaring properti `enabled` secara deterministik pada setiap entri SOURCES.

        Returns
        -------
        list[Source]
            Koleksi objek Source yang aktif dan siap digunakan.
        """
        return [
            source
            for source in cls.SOURCES
            if source.enabled
        ]

    @classmethod
    def get_by_category(cls, category: str) -> list[Source]:
        """
        Mencari dan menyaring knowledge source berdasarkan kategori domain tertentu.

        Responsibility
        --------------
        Melakukan pencocokan string kategori secara case-insensitive.

        Args:
            category: Nama kategori target pencarian (e.g., 'weather', 'visa').

        Returns:
            list[Source]: Daftar Source aktif yang sesuai dengan kategori input.
        """
        target_category = category.lower()
        return [
            source
            for source in cls.get_all()
            if source.category.lower() == target_category
        ]

    @classmethod
    def get_by_name(cls, name: str) -> Source | None:
        """
        Mencari entri spesifik satu objek knowledge source berdasarkan nama uniknya.

        Responsibility
        --------------
        Melakukan iterasi pencarian dan mengembalikan objek pertama yang cocok secara case-insensitive.

        Args:
            name: Nama unik data source yang dicari.

        Returns:
            Source | None: Objek Source jika ditemukan, atau None jika tidak terdaftar.
        """
        target_name = name.lower()
        for source in cls.get_all():
            if source.name.lower() == target_name:
                return source
        return None