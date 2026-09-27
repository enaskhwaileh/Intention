"""Project anchored Groq configuration. Never include values in diagnostics."""

import os
import re
from pathlib import Path

from dotenv import load_dotenv

from .provider_errors import MissingGroqCredentialError, MissingGroqModelError


ENV_PATH = Path(__file__).resolve().parent / ".env"
_MODEL_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/+:-]{0,127}\Z")


def load_project_env():
    """Load the package-root .env if present, preserving exported variables."""
    if ENV_PATH.is_file():
        load_dotenv(dotenv_path=ENV_PATH, override=False, interpolate=False)


def groq_api_key():
    load_project_env()
    key = os.environ.get("GROQ_API_KEY", "")
    if not key.strip():
        raise MissingGroqCredentialError("GROQ_API_KEY is missing or empty")
    return key


def groq_model_id(model=None):
    load_project_env()
    selected = model if model is not None else os.environ.get("GROQ_MODEL_ID", "")
    if not isinstance(selected, str) or not selected.strip():
        raise MissingGroqModelError("GROQ_MODEL_ID is missing or empty")
    if not _MODEL_ID.fullmatch(selected):
        raise MissingGroqModelError("GROQ_MODEL_ID must be a valid model ID")
    return selected
