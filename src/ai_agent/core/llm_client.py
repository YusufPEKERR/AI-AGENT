import time
from typing import Any, Generator
from openai import OpenAI
from ai_agent.config import settings
from ai_agent.logging_conf import logger
from ai_agent.exceptions import LLMAPIError


class LLMClient:
    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key
        )

    def stream_chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_retries: int = 5,
        retry_delay: int = 2
    ) -> Generator[Any, None, None]:
        """Streams chat completions with exponential retry on 429 / worker limit."""
        for attempt in range(1, max_retries + 1):
            try:
                completion = self.client.chat.completions.create(
                    model=settings.model_name,
                    messages=messages,
                    tools=tools,
                    temperature=settings.temperature,
                    top_p=settings.top_p,
                    max_tokens=settings.max_tokens,
                    extra_body={
                        "chat_template_kwargs": {"enable_thinking": settings.enable_reasoning},
                        "reasoning_budget": settings.reasoning_budget
                    },
                    stream=True
                )
                for chunk in completion:
                    yield chunk
                return
            except Exception as e:
                err_msg = str(e)
                if ("ResourceExhausted" in err_msg or "32/32" in err_msg or "429" in err_msg or "limit" in err_msg.lower()) and attempt < max_retries:
                    logger.warning("api_rate_limit_retry", attempt=attempt, delay=retry_delay, error=err_msg)
                    time.sleep(retry_delay)
                    retry_delay += 2
                    continue
                else:
                    logger.error("api_call_failed", error=err_msg)
                    raise LLMAPIError(f"NVIDIA LLM API Hatası: {err_msg}")
