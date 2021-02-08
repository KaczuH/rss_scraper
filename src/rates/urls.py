from django.urls import include, path
from rest_framework import routers

from .views import ExchangeRateLogsViewSet, CurrenciesViewSet

router = routers.SimpleRouter()
router.register("historical", ExchangeRateLogsViewSet)
router.register("current", CurrenciesViewSet)

urlpatterns = [path("exchange_rates/", include(router.urls))]
