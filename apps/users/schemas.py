from drf_spectacular.utils import extend_schema


# User registration schema
user_registration_schema = extend_schema(
    summary="Register a new user",
    description="Create a new user account with username, email, and password",
    tags=["Authentication"],
    responses={201: "UserRegistrationSerializer"},
)
