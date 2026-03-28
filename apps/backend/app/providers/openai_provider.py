class OpenAIProvider:
    key = "openai"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"openai:{user_prompt}"
