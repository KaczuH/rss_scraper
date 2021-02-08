from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .models import Currency, ExchangeRateLog
from .serializers import CurrencySerializer, ExchangeRateLogSerializer


class ExchangeRateLogsViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    queryset = ExchangeRateLog.objects.all()
    serializer_class = ExchangeRateLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        currency_code = self.request.query_params.get("code")
        if currency_code:
            queryset = queryset.filter(currency__code=currency_code)
        return queryset

    @swagger_auto_schema(manual_parameters=[Parameter("code", in_="query", type="str")])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CurrenciesViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Currency.objects.all().order_by("code")
    serializer_class = CurrencySerializer
    lookup_field = "code"

    @action(methods=["GET"], detail=False)
    def without_pagination(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
