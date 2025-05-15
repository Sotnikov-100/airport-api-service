from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from drf_spectacular.utils import extend_schema


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


def get_crud_schemas(
        model_name,
        tag_name,
        list_description=None,
        retrieve_description=None,
        create_description=None,
        update_description=None,
        partial_update_description=None,
        destroy_description=None,
        admin_only=False,
):
    """
    Generate standard CRUD operation schemas for viewsets.

    Args:
        model_name: The name of the model (e.g., 'airline', 'flight')
        tag_name: The API tag for grouping (e.g., 'Airlines', 'Flights')
        list_description: Custom description for list action
        retrieve_description: Custom description for retrieve action
        create_description: Custom description for create action
        update_description: Custom description for update action
        partial_update_description: Custom description for partial_update action
        destroy_description: Custom description for destroy action
        admin_only: Whether the create/update/delete operations are admin-only

    Returns:
        Dictionary of schema decorators for each CRUD operation
    """
    admin_suffix = " (admin only)" if admin_only else ""

    if list_description is None:
        list_description = f"Returns a list of all {model_name}s in the system"

    if retrieve_description is None:
        retrieve_description = f"Returns details of a specific {model_name}"

    if create_description is None:
        create_description = f"Create a new {model_name}{admin_suffix}"

    if update_description is None:
        update_description = f"Update an existing {model_name}{admin_suffix}"

    if partial_update_description is None:
        partial_update_description = f"Partially update an existing {model_name}{admin_suffix}"

    if destroy_description is None:
        destroy_description = f"Delete an existing {model_name}{admin_suffix}"

    return {
        "list": extend_schema(
            summary=f"List all {model_name}s",
            description=list_description,
            tags=[tag_name],
        ),
        "retrieve": extend_schema(
            summary=f"Get a {model_name} by ID",
            description=retrieve_description,
            tags=[tag_name],
        ),
        "create": extend_schema(
            summary=f"Create a new {model_name}",
            description=create_description,
            tags=[tag_name],
        ),
        "update": extend_schema(
            summary=f"Update a {model_name}",
            description=update_description,
            tags=[tag_name],
        ),
        "partial_update": extend_schema(
            summary=f"Partially update a {model_name}",
            description=partial_update_description,
            tags=[tag_name],
        ),
        "destroy": extend_schema(
            summary=f"Delete a {model_name}",
            description=destroy_description,
            tags=[tag_name],
        ),
    }
