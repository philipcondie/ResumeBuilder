import anthropic
from dotenv import load_dotenv

from models import ResumeData

class LLM:
    def __init__(self, system_prompt) -> None:
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.max_tokens = 5096
        self.model = "claude-sonnet-4-5"
        self.temperature = 1.0
        self.system_prompt = system_prompt

    def send_message(self, message):
        response = self.client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            output_format=ResumeData,
            temperature=1.0,
            # thinking=anthropic.Thinking
        )
        return response.parsed_output.model_dump()