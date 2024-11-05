import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.llms.base import LLM
from typing import Optional, List

# Load environment variables and configure Gemini API
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_key)
gemini_model = genai.GenerativeModel('gemini-1.5-flash-001')

class GeminiLLM(LLM):
    """
    A custom LangChain-compatible LLM wrapper for Google Gemini.
    """
    model: genai.GenerativeModel

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Generate a response from the Gemini model based on the prompt.
        """
        response = self.model.generate_content(prompt)
        generated_text = response.text
        return generated_text


# Instantiate the custom Gemini LLM
custom_gemini_llm = GeminiLLM(model=gemini_model)


