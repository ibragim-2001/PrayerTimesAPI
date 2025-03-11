import os
import requests
from typing import Dict

def get_prayers_times(today: str, latitude: float, longitude: float) -> Dict[str, str]:
    url = f'{os.getenv("PRAYER_TIME_API")}/v1/timings/{today}?latitude={latitude}&longitude={longitude}&method=14'
    data = requests.get(url).json()

    fajr = data["data"]["timings"]["Fajr"]
    sunrise = data["data"]["timings"]["Sunrise"]
    dhuhr = data["data"]["timings"]["Dhuhr"]
    asr = data["data"]["timings"]["Asr"]
    maghrib = data["data"]["timings"]["Maghrib"]
    isha = data["data"]["timings"]["Isha"]

    hijri_date = data["data"]["date"]["hijri"]["date"]

    return {
        "Хиджра": hijri_date,
        "Фаджр": fajr,
        "Восход солнца": sunrise,
        "Зухр": dhuhr,
        "Аср": asr,
        "Магриб": maghrib,
        "Иша": isha
    }