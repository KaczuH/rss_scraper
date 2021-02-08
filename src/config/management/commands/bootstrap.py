from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Q

from rates.models import Currency
from rates.tasks import fetch_exchange_rates

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("collectstatic", interactive=False)
        call_command("migrate", interactive=False)

        new_currency_created = False
        for code in Currency.Codes:
            _, created = Currency.objects.get_or_create(code=code)
            if created:
                new_currency_created = True
        if new_currency_created:
            fetch_exchange_rates.apply_async()

        if (
            settings.POPULATE_SUPERUSER
            and not User.objects.filter(
                Q(email=settings.SUPERUSER_EMAIL)
                | Q(username=settings.SUPERUSER_USERNAME)
            ).exists()
        ):
            User.objects.create_superuser(
                username=settings.SUPERUSER_USERNAME,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
            )
