import re

from intention.llm.base import LLMClient


TOKEN_PATTERN = re.compile(r"[a-z0-9-]+")


class MockLLMClient(LLMClient):
    INTENTION_KEYWORDS = [
        ("compare", ("compare", "between", "versus", "vs")),
        ("predict", ("predict", "forecast", "estimate")),
        ("explain", ("explain", "why", "cause", "reason")),
        ("aggregate", ("aggregate", "count", "average", "summarize", "show", "by")),
        ("integrate", ("integrate", "join", "combine", "link")),
    ]

    def separate_query_and_intention(self, user_input: str) -> dict:
        tokens = TOKEN_PATTERN.findall(user_input.lower())
        token_set = set(tokens)
        intention_type = self._detect_intention(user_input.lower(), token_set)
        entities = self._extract_entities(user_input)
        attributes = self._extract_attributes(tokens)
        constraints = self._extract_constraints(user_input.lower())

        return {
            "query_profile": {
                "topic": self._topic(tokens),
                "entities": entities,
                "attributes": attributes,
                "constraints": constraints,
                "retrieval_query": user_input,
            },
            "raw_intention": {
                "intent_phrase": user_input,
                "candidate_intention_type": intention_type,
                "slots": {
                    "entities": entities,
                    "attributes": attributes,
                    "constraints": constraints,
                },
            },
        }

    def _detect_intention(self, lowered_input: str, token_set: set[str]) -> str:
        for intention_type, keywords in self.INTENTION_KEYWORDS:
            if any(keyword in token_set for keyword in keywords):
                return intention_type
            if intention_type == "compare" and " vs " in f" {lowered_input} ":
                return "compare"
        return "describe"

    def _extract_entities(self, user_input: str) -> list[str]:
        titled = re.findall(r"\b[A-Z][A-Za-z0-9-]*(?:\s+[A-Z][A-Za-z0-9-]*)*\b", user_input)
        return [entity for entity in titled if entity.lower() not in {"show", "compare", "predict", "explain", "integrate"}]

    def _extract_attributes(self, tokens: list[str]) -> list[str]:
        stopwords = {
            "a",
            "an",
            "and",
            "are",
            "as",
            "between",
            "by",
            "for",
            "from",
            "in",
            "of",
            "the",
            "to",
            "using",
            "with",
            "why",
        }
        return [token for token in tokens if token not in stopwords]

    def _extract_constraints(self, lowered_input: str) -> dict[str, str]:
        constraints: dict[str, str] = {}
        if "last quarter" in lowered_input:
            constraints["time"] = "last quarter"
        if "european" in lowered_input or "europe" in lowered_input:
            constraints["geography"] = "Europe"
        return constraints

    def _topic(self, tokens: list[str]) -> str:
        return " ".join(tokens[:6]) if tokens else "unspecified"
