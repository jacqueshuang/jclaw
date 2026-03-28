import pytest

from app.providers.registry import ProviderRegistry, UnknownProviderKeyError


def test_registry_exposes_expected_provider_keys() -> None:
    registry = ProviderRegistry()

    assert registry.keys() == ["anthropic", "gemini", "openai"]


def test_registry_get_returns_provider_for_known_key() -> None:
    registry = ProviderRegistry()

    provider = registry.get("openai")

    assert provider.key == "openai"


def test_registry_get_raises_diagnosable_error_for_unknown_key() -> None:
    registry = ProviderRegistry()

    with pytest.raises(UnknownProviderKeyError) as exc_info:
        registry.get("does-not-exist")

    message = str(exc_info.value)
    assert "Unknown provider key 'does-not-exist'." in message
    assert "Available provider keys: anthropic, gemini, openai" in message
