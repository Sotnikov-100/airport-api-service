from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


api_info = openapi.Info(
    title="Airport API Service",
    default_version="v1",
    description="API for airport management system",
)


schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)
