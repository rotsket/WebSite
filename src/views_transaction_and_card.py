import json
from collections import Counter
import functools
import re
from pathlib import Path
from pprint import pprint

import pandas as pd
import logging
import os
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar, Union
import requests
from dotenv import load_dotenv

import src
from src.utils import json_to_dict
from src.tools import financier_operation, find_object

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

def transactions(path):
    src.tools.path = path
    transaction = financier_operation()
    return transaction

def total_сount_сashback(path: Any = "../data/operations.csv") -> dict[str, Any]:
    """ Выводит общую сумму расходов и кешбек"""

    file = transactions(path)

    # Добавлены точные ключи из вашей выгрузки
    dictionary_total_price = ["Сумма операции", "Сумма", "сумма", "Amount", "amount"]
    dictionary_cashback = ["Бонусы (включая кэшбэк)", "Кешбэк", "кешбэк", "Cashback", "cashback"]

    dictionary_status = ["Статус", "статус", "States", "states", "status"]

    total_count = []
    cashback = []

    for item in file:
        status_flag = False
        status_value = ""
        found_price = None
        found_cashback = None

        for key, value in item.items():
            if key in dictionary_status:
                status_flag = True
                status_value = str(value).lower()
            elif key in dictionary_total_price and str(value).lower() != "nan":
                found_price = float(str(value).replace(",", "."))
            elif key in dictionary_cashback and str(value).lower() != "nan":
                found_cashback = float(str(value).replace(",", "."))

        if not status_flag or status_value == "ок":
            if found_price is not None:
                total_count.append(found_price)
            if found_cashback is not None:
                cashback.append(found_cashback)

    cashback_per_ruble = int(sum(cashback)) / 100

    return {
        "total_count": str(total_count),
        "cashback": str(cashback),
        "cashback_per_ruble": str(cashback_per_ruble),
    }


def leaders_transaction(path: Any = "../data/operations.csv", quantity: int = 5) -> dict[str, Any]:
    """Выводит quantity раз транзаций по сумме платежа"""
    file = transactions(path)

    dictionary_total_price = ["Сумма операции", "Сумма", "сумма", "Amount", "amount"]
    found_price = []
    for item in file:
        for key, value in item.items():
            if key in dictionary_total_price and str(value).lower() != "nan":
                found_price.append(float(str(value).replace(",", ".")))

    leaders = []
    for _ in range(quantity):
        max_num = None
        for num in found_price:
            if num not in leaders:
                if max_num is None or num > max_num:
                    max_num = num

        if max_num is not None:
            leaders.append(max_num)

    return leaders




# if __name__ == "__main__":
#     result1 = get_mask_account("4111 1111 1111 1111")
#     print(result1)

if __name__ == "__main__":
    result1 = leaders_transaction("../data/Operations Sun Nov 01 2026-Wed Nov 18 2026.csv")
    pprint(result1, indent=1)
