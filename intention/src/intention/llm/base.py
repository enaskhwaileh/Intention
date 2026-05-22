from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def separate_query_and_intention(self, user_input: str) -> dict:
        """Return query profile and raw intention fields for a user input."""
