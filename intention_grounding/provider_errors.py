"""Small, allowlisted provider diagnostics; never serialize exception messages."""


class MissingGroqCredentialError(RuntimeError):
    """The process has no GROQ_API_KEY."""


_SAFE_TYPES = {
    "RuntimeError", "ImportError", "ModuleNotFoundError", "TimeoutError",
    "ConnectionError", "APIError", "APIConnectionError", "APITimeoutError",
    "APIStatusError", "AuthenticationError", "PermissionDeniedError",
    "BadRequestError", "NotFoundError", "ConflictError",
    "UnprocessableEntityError", "RateLimitError", "InternalServerError",
    "APIResponseValidationError",
}
_SAFE_CODES = {
    "invalid_api_key", "authentication_error", "permission_denied",
    "model_not_found", "rate_limit_exceeded", "invalid_request_error",
    "insufficient_quota",
}


def provider_diagnostic(exc):
    """Return only fixed labels and bounded numeric status, never str(exc)."""
    if isinstance(exc, MissingGroqCredentialError):
        return {"exception_type": "MissingGroqCredentialError",
                "error_code": "MISSING_GROQ_API_KEY"}

    kind = type(exc)
    trusted_module = kind.__module__ == "builtins" or kind.__module__.startswith("groq.")
    name = kind.__name__ if trusted_module and kind.__name__ in _SAFE_TYPES else "ProviderError"
    result = {"exception_type": name}
    try:
        status = getattr(exc, "status_code", None)
    except Exception:
        status = None
    if type(status) is int and 100 <= status <= 599:
        result["http_status"] = status
    try:
        code = getattr(exc, "code", None)
    except Exception:
        code = None
    if type(code) is str and code in _SAFE_CODES:
        result["error_code"] = code
    return result
