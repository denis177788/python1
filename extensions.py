import requests
import json
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except:
            raise APIException(f'Не удалось обработать количество {amount}')

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

        total_amount = round(float(json.loads(r.content)[keys[base]]) * amount, 4)
        return total_amount
