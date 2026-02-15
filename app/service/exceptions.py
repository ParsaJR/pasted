class ServiceError(Exception):
    """Base exception for service errors."""

    pass


class AuthenticationError(ServiceError):
    pass


class AuthorizationError(ServiceError):
    pass
