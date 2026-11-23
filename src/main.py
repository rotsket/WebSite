import json

from src.services import curse_stock, get_rates
from src.tools import transaction_to_currency, stock_is_SP500
from src.views_greeting import greeting_home
from src.views_transaction_and_card import get_mask_account, total_count_cashback, leaders_transaction


def main():
    result = {
        "greeting": greeting_home("2020-01-10 10:23:22"),
        "cards":list(total_count_cashback()),
        "top_transactions":leaders_transaction(),
        "currency_rates": get_rates(),
        "stock_prices": stock_is_SP500()

    }
    json_response = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_response)
    return json_response

if __name__ == "__main__":
    main()