from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class JWTTokenScheme(OpenApiAuthenticationExtension):
    target_class = "rest_framework_simplejwt.authentication.JWTAuthentication"
    name = "JWT Authentication"

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix="Bearer",
            bearer_format="JWT",
        )


def get_error_schema():
    from drf_spectacular.utils import inline_serializer
    from rest_framework import serializers

    return inline_serializer(
        name="ErrorResponse",
        fields={
            "error": serializers.CharField(),
            "detail": serializers.CharField(required=False),
        },
    )
