from enum import Enum

class TripStatus(str, Enum):
    PLANNING = "planning"
    CONFIRMED = "confirmed"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
class PlaceCategory(str, Enum):
    ACCOMMODATION = "ACCOMMODATION"  
    RESTAURANT = "RESTAURANT"        
    ATTRACTION = "ATTRACTION"       
    TRANSPORTATION = "TRANSPORTATION"
    SHOPPING = "SHOPPING"           
    ENTERTAINMENT = "ENTERTAINMENT" 
    NATURE = "NATURE"               
class TravelMode(str, Enum):
    WALKING = "WALKING"
    DRIVING = "DRIVING"
    TRANSIT = "TRANSIT"
    BICYCLING = "BICYCLING"
class ErrorMessage:
    NOT_FOUND = "Resource atau data yang Anda cari tidak ditemukan."
    UNAUTHORIZED = "Kredensial tidak ditemukan, silakan login kembali."
    FORBIDDEN = "Anda tidak memiliki hak akses untuk melakukan aksi ini."
    VALIDATION_ERROR = "Validasi gagal. Mohon periksa kembali input Anda."
    INTERNAL_SERVER_ERROR = "Terjadi kegagalan sistem pada internal server."

DEFAULT_CURRENCY = "USD"

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