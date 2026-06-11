"""Custom exception classes."""


class STPParseError(Exception):
    """Raised when .stp file parsing fails."""
    pass


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class BlobStorageError(Exception):
    """Raised when blob storage operations fail."""
    pass
