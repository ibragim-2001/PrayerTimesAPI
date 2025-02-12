import requests

def get_prayers_times(today, latitude, longitude):
    """
    Функция возвращает время намаза и год по Хиджре
    :return:
    """
    url = f"http://api.aladhan.com/v1/timings/{today}?latitude={latitude}&longitude={longitude}&method=14"
    response = requests.get(url)
    data = response.json()

    fajr = data["data"]["timings"]["Fajr"]
    sunrise = data["data"]["timings"]["Sunrise"]
    dhuhr = data["data"]["timings"]["Dhuhr"]
    asr = data["data"]["timings"]["Asr"]
    maghrib = data["data"]["timings"]["Maghrib"]
    isha = data["data"]["timings"]["Isha"]

    hijri_date = data["data"]["date"]['hijri']["date"]

    return {"Хиджра": hijri_date, "Фаджр": fajr, "Восход солнца": sunrise, "Зухр": dhuhr, "Аср": asr,  "Магриб": maghrib, "Иша": isha }