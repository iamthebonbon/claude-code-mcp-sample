import json
import logging
from anthropic import Anthropic
from anthropic.types import Message

logger = logging.getLogger(__name__)


class Claude:
    def __init__(self, model: str):
        self.client = Anthropic()
        self.model = model

    def add_user_message(self, messages: list, message):
        user_message = {
            "role": "user",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(user_message)

    def add_assistant_message(self, messages: list, message):
        assistant_message = {
            "role": "assistant",
            "content": message.content
            if isinstance(message, Message)
            else message,
        }
        messages.append(assistant_message)

    def text_from_message(self, message: Message):
        return "\n".join(
            [block.text for block in message.content if block.type == "text"]
        )

    def chat(
        self,
        messages,
        system=None,
        temperature=1.0,
        stop_sequences=[],
        tools=None,
        thinking=False,
        thinking_budget=1024,
    ) -> Message:
        params = {
            "model": self.model,
            "max_tokens": 8000,
            "messages": messages,
            "temperature": temperature,
            "stop_sequences": stop_sequences,
        }

        if thinking:
            params["thinking"] = {
                "type": "enabled",
                "budget_tokens": thinking_budget,
            }

        if tools:
            params["tools"] = tools

        if system:
            params["system"] = system

        logger.debug(
            "Calling Claude — model=%s, messages=%d, tools=%d, thinking=%s",
            self.model,
            len(messages),
            len(tools) if tools else 0,
            thinking,
        )
        logger.debug("Claude raw request:\n%s", json.dumps(params, indent=2, default=str))

        message = self.client.messages.create(**params)

        logger.debug(
            "Claude response — stop_reason=%s, in=%d out=%d tokens",
            message.stop_reason,
            message.usage.input_tokens,
            message.usage.output_tokens,
        )

        logger.debug("Claude raw response:\n%s", message.model_dump_json(indent=2))

        return message
