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
from typing import Any, Callable, ParamSpec, TypeVar, Union, Generator, Iterator
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


def transactions(path):
    src.tools.path = path
    transaction = financier_operation()
    return transaction


def get_mask_account(path: Union[int, str, list[dict]]) -> list[str]:
    """Берет из словаря номер карты"""
    if isinstance(path, list):
        file = path
    else:
        file = transactions(path)

    found_card_number: list[str] = []
    for item in file:
        found_card_number.append(item["Номер карты"])

    return found_card_number


def total_count_cashback(path: Any = "../data/operations.csv") -> Iterator[str]:
    """ Выводит общую сумму расходов и кешбек"""
    file = transactions(path)

    keys_price = {"Сумма операции", "Сумма", "сумма", "Amount", "amount"}
    keys_cashback = {"Бонусы (включая кэшбэк)", "Кешбэк", "кешбэк", "Cashback", "cashback"}
    keys_status = {"Статус", "статус", "States", "states", "status"}
    keys_card = {"Номер карты", "номер карты", "Card", "card"}

    # Словарь для накопления данных: {"*1234": {"spent": 0.0, "cashback": 0.0}}
    cards_stats: dict[str, dict[str, float]] = {}

    for item in file:
        status_value = ""
        found_price = 0.0
        found_cashback = 0.0
        card_number = ""

        for key, value in item.items():
            clean_key = str(key).strip()
            val_str = str(value).strip()
            if not val_str or val_str.lower() == "nan":
                continue

            if clean_key in keys_status:
                status_value = val_str.lower()
            elif clean_key in keys_price:
                found_price = float(val_str.replace(",", "."))
            elif clean_key in keys_cashback:
                found_cashback = float(val_str.replace(",", "."))
            elif clean_key in keys_card:
                card_number = val_str[-4:]

        # Учитываем и русскую 'ок', и английскую 'ok'
        if (not status_value or status_value in {"ок", "ok"}) and card_number:
            if card_number not in cards_stats:
                cards_stats[card_number] = {"spent": 0.0, "cashback": 0.0}

            cards_stats[card_number]["spent"] += found_price
            cards_stats[card_number]["cashback"] += found_cashback

    # Выдаем по одному словарю для каждой уникальной карты
    for digits, stats in cards_stats.items():
        yield {
            "last_digits": digits,
            "total_spent": round(abs(stats["spent"]), 2),
            "cashback": round(stats["cashback"] / 100, 2),
        }
    #     {
    #     "total_count": str(total_count),
    #     "cashback": str(cashback),
    #     "cashback_per_ruble": str(cashback_per_ruble),
    # }


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
    for card_info in total_count_cashback("../data/operations.csv"):
        print(card_info)

# def get_mask_account(path: Any = "../data/operations.csv") -> list[str]:
#     """Оставляет последние 4 цифры: **XXXX."""
#
#     file = transactions(path)
#
#     found_card_number = []
#     for item in file:
#         # for key, value in item.items():
#         #     if key in dictionary_card:
#                 # found_card_number.append(value)
#
#                 found_card_number.append({
#                     "last_digits": item["Номер карты"],
#                     "total_spent": item["Сумма операции"],
#                     "cashback": float(item["Сумма операции"].replace(",", ".")) / 100
#                 })
#     return found_card_number
