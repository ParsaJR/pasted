class ServiceError(Exception):
    """Base exception for service errors."""

    pass

class GenericAuthError(ServiceError):
    pass

class AuthenticationError(GenericAuthError):
    pass


class AuthorizationError(GenericAuthError):
    pass
