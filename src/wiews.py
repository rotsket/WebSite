import json
from datetime import datetime, time, date
from typing import Any

def greeting_home(data: str) -> Any: # date = YYYY-MM-DD HH:MM:SS
    dt = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")

    greeting = []

    d = dt.date()
    time_hour = dt.hour

    if 6 < time_hour <= 12:
        greeting.append("Доброе Утро")
    if 12 <= time_hour <= 18:
        greeting.append("Добрый день")
    if 18 <= time_hour <= 24:
        greeting.append("Доброго вечера")
    if 0 <= time_hour <= 6:
        greeting.append("Доброй ночи")

    json_data = json.dumps(greeting, ensure_ascii=False)

    return json_data




if __name__ == "__main__":
    result = greeting_home("2020-01-10 10:23:22")
    print(result)
    print(type(result))

