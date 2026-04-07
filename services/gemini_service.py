from google import genai
from google.genai import types


class GeminiService:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def call(self, prompt: str, temperature: float = 0.7) -> str:
        config = types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=8192,
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        return response.text

    @staticmethod
    def call_gemini(api_key: str, prompt: str, temperature: float = 0.7) -> str:
        return GeminiService(api_key).call(prompt, temperature)


def call_gemini(api_key: str, prompt: str, temperature: float = 0.7) -> str:
    return GeminiService.call_gemini(api_key, prompt, temperature)