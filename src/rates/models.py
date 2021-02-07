from django.db import models
from django.utils.translation import gettext_lazy as _


class ExchangeRate(models.Model):
    class Currencies(models.TextChoices):
        JPY = "JPY", _("Japanese yen")
        BGN = "BGN", _("Bulgarian lev")
        CZK = "CZK", _("Czech koruna")
        DKK = "DKK", _("Danish krone")
        EEK = "EEK", _("Estonian kroon")
        GBP = "GBP", _("Pound sterling")
        HUF = "HUF", _("Hungarian forint")
        PLN = "PLN", _("Polish zloty")
        RON = "RON", _("Romanian leu")
        SEK = "SEK", _("Swedish krona")
        CHF = "CHF", _("Swiss franc")
        ISK = "ISK", _("Icelandic krona")
        NOK = "NOK", _("Norwegian krone")
        HRK = "HRK", _("Croatian kuna")
        RUB = "RUB", _("Russian rouble")
        TRY = "TRY", _("Turkish lira")
        AUD = "AUD", _("Australian dollar")
        BRL = "BRL", _("Brasilian real")
        CAD = "CAD", _("Canadian dollar")
        CNY = "CNY", _("Chinese yuan renminbi")
        HKD = "HKD", _("Hong Kong dollar")
        IDR = "IDR", _("Indonesian rupiah")
        INR = "INR", _("Indian rupee")
        KRW = "KRW", _("South Korean won")
        MXN = "MXN", _("Mexican peso")
        MYR = "MYR", _("Malaysian ringgit")
        NZD = "NZD", _("New Zealand dollar")
        PHP = "PHP", _("Philippine peso")
        SGD = "SGD", _("Singapore dollar")
        THB = "THB", _("Thai baht")
        ZAR = "ZAR", _("South African rand")

    currency = models.CharField(_("currency"), max_length=3, choices=Currencies.choices)
    exchange_rate = models.DecimalField(
        _("exchange rate"), max_digits=20, decimal_places=4
    )
    ecb_updated = models.DateTimeField(_("ecb updated"))

    class Meta:
        unique_together = ("currency", "ecb_updated")
        verbose_name = _("exchange rate")
        verbose_name_plural = _("exchange rates")

    def __str__(self):
        return self.get_currency_display()

    @property
    def description(self):
        return f"1 EUR buys {self.exchange_rate} {self.get_currency_display()} ({self.currency})"
