from dataclasses import asdict

from intention.schemas.profile import OperationalProfile


def validate_profile(profile: OperationalProfile, rules: dict) -> dict:
    data = asdict(profile)
    errors: list[str] = []

    for field in rules.get("required_fields", []):
        if not data.get(field):
            errors.append(f"missing required field: {field}")

    if profile.confidence < rules.get("min_confidence", 0):
        errors.append("confidence below minimum")

    allowed_types = set(rules.get("allowed_profile_types", []))
    if allowed_types and profile.profile_type not in allowed_types:
        errors.append("profile type is not allowed")

    return {"input_id": profile.input_id, "valid": not errors, "errors": errors}
