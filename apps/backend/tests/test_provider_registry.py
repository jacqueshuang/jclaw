from app.providers.registry import ProviderRegistry


def test_registry_exposes_expected_provider_keys() -> None:
    registry = ProviderRegistry()

    assert sorted(registry.keys()) == ["anthropic", "gemini", "openai"]
