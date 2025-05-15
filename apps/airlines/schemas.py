from apps.core.schemas import get_crud_schemas


# Airline ViewSet schemas
airline_schemas = get_crud_schemas(
    model_name="airline",
    tag_name="Airlines",
    admin_only=True,
)

# Aircraft ViewSet schemas
aircraft_schemas = get_crud_schemas(
    model_name="aircraft",
    tag_name="Aircraft",
    admin_only=True,
)
