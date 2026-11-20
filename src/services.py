import json
import math
import re
from datetime import datetime
import logging
from pprint import pprint
from typing import Any
import calendar
import src
from src.tools import financier_operation


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
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



if __name__ == "__main__":
    file = transactions("../data/Operations Sun Nov 01 2026-Wed Nov 18 2026.csv")
    result = investment_bank("2026-10", file, 10)
    pprint (result, indent=4)

# if __name__ == "__main__":
#     investment_bank("2027-05")