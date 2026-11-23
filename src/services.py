import json
import math
import os
import re
from datetime import datetime
import logging
from locale import currency
from pprint import pprint
from typing import Any
import calendar

import requests
from dotenv import load_dotenv

import src
from src.tools import financier_operation, transaction_to_currency, stock_is_SP500


load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY1 = os.getenv('API_KEY1')

CACHE: dict = {}


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """Округляет сууму и остаток ложит в банк"""
    pattern = r"\b\d{4}-\d{2}-\d{2}\b"

    dictionary_total_price = ["Сумма операции", "Сумма", "сумма", "Amount", "amount"]
    dictionary_data = ["Дата операции", "дата операции"]

    start_date = datetime.strptime(month, "%Y-%m").date()
    last_day = calendar.monthrange(start_date.year, start_date.month)[1]
    end_date = start_date.replace(day=last_day)

    piggy_bank = 0.0

    for item in transactions:
        datas = None
        price = None

        for key, value in item.items():
            if key in dictionary_data and str(value).lower() != "nan":
                datas = value
            if key in dictionary_total_price and str(value).lower() != "nan":
                price = value

        if datas is not None and price is not None:

            match = re.search(pattern, str(datas))

            if match:
                tx_date = datetime.strptime(match.group(0), "%Y-%m-%d").date()

                if start_date <= tx_date <= end_date:
                    clean_price = float(str(price).replace(",", ".").replace(" ", ""))
                    amount = abs(clean_price)
                    piggy_bank += math.ceil(amount / limit) * limit - amount

    return round(piggy_bank, 2)

def transactions(path):
    src.tools.path = path
    transaction = financier_operation()
    return transaction


def get_rates(currency: tuple = ("USD", "EUR"), base_currency: str = "RUB") -> list[dict]:
    """Возвращает список курсов запрошенных валют относительно base_currency.

    Пример результата:
        [{"currency": "USD", "rate": 73.21}, {"currency": "EUR", "rate": 87.08}]
    """
    global CACHE

    # --- один раз тянем курсы и кладём в кэш ---
    if not CACHE:
        try:
            url = f"https://api.apilayer.com/exchangerates_data/latest?base={base_currency}"
            headers = {"apikey": API_KEY}
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            if "rates" in data:
                CACHE = data["rates"]
                print("CACHE <-- кэш сохранён, запрос к API сделан один раз")
            else:
                print(f"API не вернул rates. Ответ: {data}")
        except requests.RequestException as e:
            print(f"Сетевая ошибка: {e}")
        except Exception as e:
            print(f"Ошибка при запросе к API: {e}")

    # --- собираем результат в нужном формате ---
    result: list[dict] = []
    for code in currency:
        if code in CACHE:
            result.append({
                "currency": code,
                "rate": round(float(CACHE[code]), 2),
            })
        else:
            print(f"Курс для {code} не найден в кэше")

    return result


def curse_stock():
    return stock_is_SP500()





# if __name__ == "__main__":
#     file = transactions("../data/Operations Sun Nov 01 2026-Wed Nov 18 2026.csv")
#     result = investment_bank("2026-10", file, 10)
#     pprint (result, indent=4)

# if __name__ == "__main__":
#     investment_bank("2027-05")

if __name__ == "__main__":
    result = get_rates(currency=("USD", "EUR"))
    print(result)