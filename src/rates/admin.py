from django.contrib import admin

from .models import Currency, ExchangeRateLog


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "update", "last_fetched", "exchange_rate", "ecb_updated")
    readonly_fields = ("last_fetched", "exchange_rate", "ecb_updated")
    list_filter = ("update",)


class ExchangeRateLogAdmin(admin.ModelAdmin):
    list_display = ("currency", "exchange_rate", "ecb_updated")
    list_filter = ("currency",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeRateLog, ExchangeRateLogAdmin)
