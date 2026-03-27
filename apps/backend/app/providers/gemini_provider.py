class GeminiProvider:
    key = "gemini"

    def generate_text(self, *, system_prompt: str, user_prompt: str) -> str:
        return f"gemini:{user_prompt}"
