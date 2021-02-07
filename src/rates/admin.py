from django.contrib import admin

from .models import ExchangeRate


class ExchangeRateAdmin(admin.ModelAdmin):
    list_filter = ("currency",)
    list_display = ("currency", "exchange_rate", "ecb_updated")
    ordering = ("-ecb_updated",)


admin.site.register(ExchangeRate, ExchangeRateAdmin)
