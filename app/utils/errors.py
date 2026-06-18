"""
Custom exceptions for business logic.
"""

class ResourceNotFoundError(Exception):
    """Raised when a requested resource is not found (404)."""
    pass

class ResourceExistsError(Exception):
    """Raised when a resource already exists, causing a conflict (409)."""
    pass

class ValidationError(Exception):
    """Raised when data validation fails or business logic is invalid (400)."""
    pass
