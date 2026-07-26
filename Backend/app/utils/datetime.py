from datetime import date, datetime, timedelta
from typing import List


def calculate_trip_duration(start_date: date, end_date: date) -> int:
    if start_date > end_date:
        return 0
    return (end_date - start_date).days + 1


def generate_date_range_list(start_date: date, end_date: date) -> List[date]:
    duration = calculate_trip_duration(start_date, end_date)
    return [start_date + timedelta(days=i) for i in range(duration)]


def format_date_to_human(target_date: date, include_day_name: bool = True) -> str:
    months = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Ototber", "November", "Desember"
    ]
    days = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    
    day_name = days.get(target_date.strftime("%A"), "")
    day_num = target_date.day
    month_name = months[target_date.month - 1]
    year = target_date.year
    
    if include_day_name and day_name:
        return f"{day_name}, {day_num} {month_name} {year}"
    return f"{day_num} {month_name} {year}"


def is_date_overlapping(
    start_a: date, end_a: date, start_b: date, end_b: date
) -> bool:
    return start_a <= end_b and start_b <= end_a