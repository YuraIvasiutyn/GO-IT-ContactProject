import requests
from .models import ExchangeRate
from datetime import datetime


def fetch_and_save_nbu_rates_for_date(date_obj: datetime, currencies: list):
    date_str = date_obj.strftime('%Y%m%d')
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date_str}&json"
    response = requests.get(url)
    data = response.json()

    saved_rates = []

    for item in data:
        if currencies is None or item['cc'] in currencies:
            rate_obj, created = ExchangeRate.objects.get_or_create(
                currency_code=item['cc'],
                date=date_obj,
                defaults={
                    'currency_name': item['txt'],
                    'rate': round(item['rate'], 2)
                }
            )
            saved_rates.append(rate_obj)

    return saved_rates


def get_rates_by_date(date_obj: datetime, currencies: list = None):
    if currencies:
        existing_rates = ExchangeRate.objects.filter(date=date_obj, currency_code__in=currencies)
        existing_codes = set(rate.currency_code for rate in existing_rates)

        missing_currencies = list(set(currencies) - existing_codes)

        if missing_currencies:
            new_rates = fetch_and_save_nbu_rates_for_date(date_obj, missing_currencies)
        else:
            new_rates = []
        return list(existing_rates) + new_rates
    else:
        rates = ExchangeRate.objects.filter(date=date_obj)
        if rates.exists():
            return list(rates)
        else:
            return fetch_and_save_nbu_rates_for_date(date_obj, currencies=[])
