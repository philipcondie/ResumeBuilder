import anthropic
from dotenv import load_dotenv

from models import ResumeData

class LLM:
    def __init__(self, system_prompt) -> None:
        load_dotenv()
        self.client = anthropic.Anthropic()
        self.max_tokens = 5096
        self.model = "claude-opus-4-6"
        self.temperature = 1.0
        self.system_prompt = system_prompt

    def send_message(self, message):
        response = self.client.messages.parse(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            thinking={"type": "adaptive"},
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            output_config={"effort":"medium"},
            output_format=ResumeData,
            # temperature=1.0,
        )
        print(response)
        return response.parsed_output.model_dump()