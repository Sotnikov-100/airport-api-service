from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)

from apps.core.schemas import get_crud_schemas


# Country ViewSet schemas
country_schemas = get_crud_schemas(
    model_name="country",
    tag_name="Countries",
    admin_only=True,
)

# City ViewSet schemas
city_schemas = get_crud_schemas(
    model_name="city",
    tag_name="Cities",
    admin_only=True,
)

# Airport ViewSet schemas
airport_schemas = get_crud_schemas(
    model_name="airport",
    tag_name="Airports",
    admin_only=True,
)

# Flight ViewSet schemas
flight_schemas = get_crud_schemas(
    model_name="flight",
    tag_name="Flights",
    admin_only=True,
    retrieve_description="Returns detailed information about a specific flight",
)

# Flight action schemas
flight_action_schemas = {
    "available_seats": extend_schema(
        summary="Get available seats",
        description="Returns the number of available seats for a specific flight",
        responses={200: OpenApiResponse(description="Number of available seats")},
        tags=["Flights"],
    ),

    "search": extend_schema(
        summary="Search flights",
        description="Search flights with from-to airport codes and optional date",
        parameters=[
            OpenApiParameter(
                name="from",
                description="Departure airport code",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="to",
                description="Arrival airport code",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="date",
                description="Departure date (YYYY-MM-DD)",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: "FlightSerializer(many=True)",
            400: OpenApiResponse(description="Bad request - invalid parameters"),
        },
        tags=["Flights"],
    ),

    "statistics": extend_schema(
        summary="Get flight statistics",
        description="Returns statistics about flights grouped by status",
        responses={
            200: OpenApiResponse(
                description="Flight statistics",
                examples=[
                    OpenApiExample(
                        "Example response",
                        value=[
                            {"status": "scheduled", "count": 42},
                            {"status": "delayed", "count": 7},
                            {"status": "in_air", "count": 12},
                            {"status": "landed", "count": 30},
                            {"status": "cancelled", "count": 3},
                        ],
                    )
                ],
            )
        },
        tags=["Flights"],
    ),

    "upcoming": extend_schema(
        summary="Get upcoming flights",
        description="Returns a list of upcoming scheduled flights within the next 24 hours",
        responses={200: "FlightSerializer(many=True)"},
        tags=["Flights"],
    ),

    "update_status": extend_schema(
        summary="Update flight status",
        description="Update the status of a specific flight (admin only)",
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": [
                            "scheduled",
                            "delayed",
                            "in_air",
                            "landed",
                            "cancelled",
                        ],
                    }
                },
                "required": ["status"],
            }
        },
        responses={
            200: "FlightSerializer",
            400: OpenApiResponse(description="Invalid status value"),
        },
        tags=["Flights"],
    ),
}
