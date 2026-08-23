"""Domain-specific validation errors."""


class IntentionError(Exception):
    """Base exception for deterministic, user-visible domain failures."""


class ContractValidationError(IntentionError, ValueError):
    """Raised when a domain contract violates a required invariant."""


class RegistryValidationError(IntentionError, ValueError):
    """Raised when an action or predicate registry is inconsistent."""
