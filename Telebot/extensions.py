import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Вы переводите одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]
        new_price = total_base * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {quote} в {base} : {new_price}"

        return message
