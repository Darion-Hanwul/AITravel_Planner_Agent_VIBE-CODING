"""
Global Application Constants

Berisi nilai-nilai konstan dan enumerasi statis yang digunakan di seluruh aplikasi.
Konstanta di sini tidak bergantung pada environment (.env).
"""

from enum import Enum

# ==========================================================
# TRIP & ITINERARY STATUS
# ==========================================================
class TripStatus(str, Enum):
    """Status tahapan perjalanan sesuai skema database."""
    PLANNING = "planning"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ==========================================================
# SAVED PLACE CATEGORIES
# ==========================================================
class PlaceCategory(str, Enum):
    """
    Kategori tempat tersimpan yang dipetakan secara akurat
    berdasarkan entitas geospasial (OpenStreetMap/Nominatim).
    """
    ACCOMMODATION = "ACCOMMODATION"  # Hotel, hostel, resort, guesthouse
    RESTAURANT = "RESTAURANT"        # Cafe, restoran, kuliner lokal
    ATTRACTION = "ATTRACTION"        # Tempat wisata, museum, taman, landmark
    TRANSPORTATION = "TRANSPORTATION"# Bandara, stasiun kereta, terminal bus, pelabuhan
    SHOPPING = "SHOPPING"            # Mall, pasar tradisional, pusat oleh-oleh
    ENTERTAINMENT = "ENTERTAINMENT"  # Bioskop, teater, club, konser hall
    NATURE = "NATURE"                # Pantai, gunung, air terjun, cagar alam


# ==========================================================
# TRAVEL TRANSPORTATION MODES
# ==========================================================
class TravelMode(str, Enum):
    """Metode transportasi dasar untuk mobilitas antar-titik rute harian."""
    WALKING = "WALKING"
    DRIVING = "DRIVING"
    TRANSIT = "TRANSIT"  # Transportasi publik (KRL, MRT, Busway)
    BICYCLING = "BICYCLING"


# ==========================================================
# SYSTEM STANDARDIZED ERROR MESSAGES
# ==========================================================
class ErrorMessage:
    """Pesan kesalahan standar untuk konsistensi respons API."""
    NOT_FOUND = "Resource atau data yang Anda cari tidak ditemukan."
    UNAUTHORIZED = "Kredensial tidak ditemukan, silakan login kembali."
    FORBIDDEN = "Anda tidak memiliki hak akses untuk melakukan aksi ini."
    VALIDATION_ERROR = "Validasi gagal. Mohon periksa kembali input Anda."
    INTERNAL_SERVER_ERROR = "Terjadi kegagalan sistem pada internal server."


# ==========================================================
# FINANCIAL & DATA CACHING CONFIGURATIONS
# ==========================================================
DEFAULT_CURRENCY = "USD"

# Seluruh daftar mata uang dunia aktif (Standar ISO 4217) untuk ExchangeRate API
SUPPORTED_CURRENCIES = {
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN",
    "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND", "BOB", "BRL",
    "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY",
    "COP", "CRC", "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP",
    "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL", "GGP", "GHS",
    "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF",
    "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JMD", "JOD", "JPY",
    "KES", "KGS", "KHR", "KID", "KMF", "KPW", "KRW", "KWD", "KYD", "KZT",
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD",
    "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN", "MYR", "MZN",
    "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK",
    "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR",
    "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL", "SOS", "SRD",
    "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY",
    "TTD", "TVD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS", "VES",
    "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR",
    "ZMW", "ZWL"
}