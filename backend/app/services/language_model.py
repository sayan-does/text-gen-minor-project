# app/services/language_model.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.core.settings import settings


class LanguageModelService:
    def __init__(self, model_name: str = None):
        """
        Initializes the language model service.

        :param model_name: Optional model name to override the default from settings.
        """
        self.model_name = model_name or settings.MODEL_NAME
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def generate_response(self, message: str, context: str) -> str:
        """
        Generates a response to the given user message in the specified context.

        :param message: The user's message.
        :param context: Context information to include in the prompt.
        :return: The generated response as a string.
        """
        prompt = f"""Context: {context}
User: {message}
Assistant: """

        inputs = self.tokenizer(
            prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_length=settings.MAX_RESPONSE_LENGTH,
            temperature=settings.TEMPERATURE,
            num_return_sequences=settings.NUM_RETURN_SEQUENCES
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
