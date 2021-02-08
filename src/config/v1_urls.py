from django.conf import settings
from django.urls import include, path


urlpatterns = [
    path("", include("rates.urls")),
]

if settings.DEBUG:
    from rest_framework import permissions
    from rest_framework.authentication import BasicAuthentication

    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    schema_view = get_schema_view(
        openapi.Info(
            title="Project Template API",
            default_version="v1",
            description="Backend communication API",
        ),
        authentication_classes=(BasicAuthentication,),
        permission_classes=(permissions.IsAuthenticated,),
    )

    urlpatterns += [
        path(
            "docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        )
    ]
