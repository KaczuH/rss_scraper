from rest_framework import serializers

from rates.models import Currency, ExchangeRateLog


class NestedCurrencySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Currency
        fields = ("code", "name")

    def get_name(self, obj):
        return obj.get_code_display()


class CurrencySerializer(NestedCurrencySerializer):
    class Meta:
        model = Currency
        fields = (
            "code",
            "name",
            "exchange_rate",
            "last_fetched",
            "ecb_updated",
            "description",
        )


class ExchangeRateLogSerializer(serializers.ModelSerializer):
    currency = NestedCurrencySerializer()

    class Meta:
        model = ExchangeRateLog
        fields = ("id", "currency", "exchange_rate", "ecb_updated")
