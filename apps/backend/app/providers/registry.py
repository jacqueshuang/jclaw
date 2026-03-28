from app.providers.anthropic_provider import AnthropicProvider
from app.providers.base import ModelProvider
from app.providers.gemini_provider import GeminiProvider
from app.providers.openai_provider import OpenAIProvider


class UnknownProviderKeyError(KeyError):
    def __init__(self, key: str, available_keys: list[str]) -> None:
        message = (
            f"Unknown provider key '{key}'. "
            f"Available provider keys: {', '.join(available_keys)}"
        )
        super().__init__(message)


class ProviderRegistry:
    def __init__(self) -> None:
        providers: list[ModelProvider] = [
            AnthropicProvider(),
            OpenAIProvider(),
            GeminiProvider(),
        ]
        self._providers: dict[str, ModelProvider] = {
            provider.key: provider for provider in providers
        }

    def get(self, key: str) -> ModelProvider:
        provider = self._providers.get(key)
        if provider is None:
            raise UnknownProviderKeyError(key, self.keys())
        return provider

    def keys(self) -> list[str]:
        return sorted(self._providers.keys())
