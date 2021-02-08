import feedparser
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Currency, ExchangeRateLog


@shared_task
def fetch_exchange_rates():
    """ Fetch exchange rate logs for all created Currency instances
    that are marked as ones to be updated. """

    for currency in Currency.objects.filter(update=True):
        data = feedparser.parse(
            f"https://www.ecb.europa.eu/rss/fxref-{currency.code.lower()}.html"
        )
        rates = []
        for entry in data.get("entries"):
            rates.append(
                ExchangeRateLog(
                    ecb_updated=entry.get("updated"),
                    exchange_rate=entry.get("cb_exchangerate").split("\n")[0],
                    currency=currency,
                )
            )
        with transaction.atomic():
            if rates:
                ExchangeRateLog.objects.bulk_create(rates, ignore_conflicts=True)
                currency.last_fetched = timezone.now()
                currency.exchange_rate = rates[0].exchange_rate
                currency.ecb_updated = rates[0].ecb_updated
                currency.save(
                    update_fields=["last_fetched", "exchange_rate", "ecb_updated"]
                )
