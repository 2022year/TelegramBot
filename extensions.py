import requests
import json
from config import money, payload, headers

sErInput="Ошибка ввода"
# Исключения
class APIException(Exception):
    pass


# Конвертер
class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException("Валюты должны отличаться")

        try:
            quote_ticker = money[quote][0]
        except KeyError:
            raise APIException(f"{sErInput} валюты <{quote}>")

        try:
            base_ticker = money[base][0]
        except KeyError:
            raise APIException(f"{sErInput} валюты <{base}>")

        try:
            amount_val = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f"{sErInput} количества валюты<{amount}>")
        if amount_val <=0:
            raise APIException("Количество должно быть положительным")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_ticker}& \
        from={quote_ticker}&amount={amount_val}"
        response = requests.request("GET", url, headers=headers, data=payload)
            
        result_json = json.loads(response.content)
        r=result_json['result']
        return r


# Склонение валют
class GetNoun:
    @staticmethod
    def get_noun(num, one, over):
        n = round(num)
        if n % 10 == 1 and n % 100 != 11:
            return one
        return over
