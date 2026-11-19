import json
import re
from datetime import datetime, time, date
from typing import Any, Union

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

def length_check_card_number(correct_card_number: str) -> None:
    """ Проверяет длину номера карты."""
    len_correct_card_number = len(correct_card_number)
    valid_lengths = (13, 15, 16, 19)

    if len_correct_card_number not in valid_lengths:

        raise ValueError("Введен некорректный номер карты")


def get_mask_account(card_number: Union[int, str]) -> str:
    """Оставляет последние 4 цифры: **XXXX."""

    correct_card_number = re.sub(
        r"[a-zA-Zа-яА-Я]", "", str(card_number).replace(" ", "")
    )
    length_check_card_number(correct_card_number)

    last_four = correct_card_number[-4:]
    return json.dumps(f"**{last_four}")



if __name__ == "__main__":
    result = greeting_home("2020-01-10 10:23:22")
    print(result)
    print(type(result))
