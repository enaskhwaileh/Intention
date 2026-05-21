from intention.llm.base import LLMClient


class MockLLMClient(LLMClient):
    def complete(self, prompt: str) -> str:
        return f"mock:{prompt[:80]}"
