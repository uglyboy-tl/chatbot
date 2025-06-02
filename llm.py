from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from openai import OpenAI

SYSTEM_PROMPT = """
You are a friendly chatbot. Engage in casual conversation.
"""


@dataclass
class LLM:
    model: str = field(default="google/gemini-2.0-flash-lite-001")
    client: OpenAI = field(default_factory=OpenAI)
    stream: bool = field(default=True)

    def chat_bot(self, message_history: list[dict[str, str]]) -> Iterator[str] | str:
        if message_history[0].get("role") != "system":
            message_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        response = self.client.chat.completions.create(
            model=self.model, messages=message_history, stream=self.stream, extra_body={"enable_search": True}
        )
        if self.stream and isinstance(response, Iterator):
            return (
                item.choices[0].delta.content
                for item in response
                if isinstance(item.choices, list) and len(item.choices) > 0
            )
        else:
            return response.choices[0].message.content
