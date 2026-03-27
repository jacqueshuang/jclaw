from typing import Protocol


class ModelProvider(Protocol):
    key: str

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str: ...
