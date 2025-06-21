from datetime import datetime

from django.shortcuts import render
from django.core.paginator import Paginator

from .currency_fetcher import get_rates_by_date


AVAILABLE_CURRENCIES = ['USD', 'EUR', 'PLN', 'GBP', 'CHF', 'CZK', 'SEK', 'NOK']

# Create your views here.
def currency_view(request):
    date_str = request.GET.get('date')
    currencies = request.GET.getlist('currencies')

    if date_str:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_obj = datetime.today().date()
    else:
        date_obj = datetime.today().date()

    currency_filter = currencies if currencies else AVAILABLE_CURRENCIES
    rates = get_rates_by_date(date_obj, currency_filter)

    paginator = Paginator(rates, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "scraping_app/news.html", {
        "page_obj": page_obj,
        "selected_date": date_obj,
        "available_currencies": AVAILABLE_CURRENCIES,
        "selected_currencies": currencies
    })
