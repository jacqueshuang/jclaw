class AnthropicProvider:
    key = "anthropic"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"anthropic:{user_prompt}"
