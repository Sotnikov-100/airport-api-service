from apps.core.schemas import get_crud_schemas


# Passenger ViewSet schemas
passenger_schemas = get_crud_schemas(
    model_name="passenger",
    tag_name="Passengers",
    list_description="Returns a list of all passengers accessible to the authenticated user",
)

# Booking ViewSet schemas
booking_schemas = get_crud_schemas(
    model_name="booking",
    tag_name="Bookings",
    list_description="Returns a list of all bookings accessible to the authenticated user. Regular users see only their own bookings, staff see all bookings.",
    retrieve_description="Returns details of a specific booking if accessible to the user",
    create_description="Create a new booking. The current user will be set as the booking owner.",
    update_description="Update an existing booking if the user is the owner or admin",
    partial_update_description="Partially update an existing booking if the user is the owner or admin",
    destroy_description="Delete an existing booking if the user is the owner or admin",
)
