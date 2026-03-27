from app.providers.anthropic_provider import AnthropicProvider
from app.providers.base import ModelProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ModelProvider] = {
            "anthropic": AnthropicProvider(),
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider(),
        }

    def get(self, key: str) -> ModelProvider:
        return self._providers[key]

    def keys(self) -> list[str]:
        return list(self._providers.keys())
