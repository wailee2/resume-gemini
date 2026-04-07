from google import genai            # Google GenAI Python SDK
from google.genai import types      # Typed config objects (GenerateContentConfig, etc.)


class GeminiService:
    """
    Thin wrapper around the Google GenAI client that provides a clean,
    reusable interface for calling Gemini models from anywhere in the app.

    Design choice: instantiation is kept cheap (just stores the client)
    so callers can create a new instance per request without overhead.
    """
    def __init__(self, api_key: str):
        """
        Initialise the GenAI client with the caller-supplied API key.

        Args:
            api_key: A valid Google Generative AI API key (starts with "AIza…").
                    The key is passed directly to the SDK; it is never stored
                    in session state or logged.
        """
        # Authenticate and store a reusable client object for this instance
        self.client = genai.Client(api_key=api_key)

    def call(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Send a single-turn prompt to Gemini and return the model's text response.

        Args:
            prompt:      The complete prompt string (system + user instructions merged).
            temperature: Sampling temperature — lower = more deterministic/factual, higher = more creative/varied.  Defaults to 0.7.

        Returns:
            The model's response as a plain string.

        Raises:
            ValueError: If the model returns no text (e.g. blocked by safety filters).
        """
        # Build a typed config object — max_output_tokens caps run-away responses
        config = types.GenerateContentConfig(
            temperature=temperature,        # Controls randomness of the output
            max_output_tokens=8192,         # Allow up to ~6 000 words per call
        )

        # Send the prompt to the specified model and wait for a synchronous response
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",       # Fast, cost-effective Gemini 2.5 variant
            contents=prompt,                # The full prompt string
            config=config,                  # Attach our generation parameters
        )
        
        # Guard against empty responses (can happen when safety filters block output)
        if response.text is None:
            raise ValueError("The model did not return any text. Check safety filters or finish reasons.")

        return response.text

    @staticmethod
    def call_gemini(api_key: str, prompt: str, temperature: float = 0.7) -> str:
        return GeminiService(api_key).call(prompt, temperature)


def call_gemini(api_key: str, prompt: str, temperature: float = 0.7) -> str:
    return GeminiService.call_gemini(api_key, prompt, temperature)