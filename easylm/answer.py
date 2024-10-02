import requests
from typing import List, Dict, Any, Callable
import logging
import functools
import json

from . import utils
from .config import DEFAULT_SETTINGS, PROVIDERS_MAP, get_api_key

logger = logging.getLogger(__name__)


class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __str__(self):
        return f"{self.role.capitalize()}: {self.content}"

    def to_dict(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}


class Response:
    def __init__(self, content: str, llm_provider: "LLMProvider"):
        self.content = content
        self._llm_provider = llm_provider

    def __str__(self):
        return self.content

    def history(self) -> List[Message]:
        return self._llm_provider.get_history()

    def reply(self, message: str) -> "Response":
        return self._llm_provider.reply(message)


class LLMProvider:
    def __init__(self, provider: str, model: str, params: Dict[str, Any]):
        self.provider = provider
        self.model = model
        self.endpoint = PROVIDERS_MAP[provider]["endpoint"]
        self.api_key = get_api_key(provider)
        self.params = params
        self.conversation: List[Message] = []

    def request(self, prompt: str) -> Response:
        logger.info(f"Using model: {self.model}")
        logger.info(f"Requesting endpoint: {self.endpoint}")

        self.conversation.append(Message("user", prompt))
        messages = [msg.to_dict() for msg in self.conversation]

        response = requests.post(
            url=self.endpoint.format(model=self.model),
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": messages,
                **self.params,
            },
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            raise Exception(data["error"])

        content = data["choices"][0]["message"]["content"].strip()
        self.conversation.append(Message("assistant", content))
        return Response(content, self)

    def get_history(self) -> List[Message]:
        return self.conversation

    def reply(self, message: str) -> Response:
        return self.request(message)


def ask(
    model: str = DEFAULT_SETTINGS["model"],
    json_response: bool = False,
    save_logs: bool = True,
    params: Dict[str, Any] = DEFAULT_SETTINGS["params"],
) -> Callable:
    """
    A decorator factory for creating LLM query functions.

    Args:
        model (str): The model to use for the query.
        json_response (bool): Whether to parse the response as JSON.
        save_logs (bool): Whether to save the logs of the interaction.
        params (Dict[str, Any]): Additional parameters for the LLM request.

    Returns:
        Callable: A decorator function.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Response:
            prompt = func(*args, **kwargs)
            prompt_map: Dict[str, str] = {}

            if isinstance(prompt, dict):
                prompt, prompt_map = prompt
                assert prompt.endswith(
                    ".txt"
                ), "Prompt must be a .txt file if you return a tuple"

            if prompt.endswith(".txt"):
                prompt = utils.load_prompt(prompt, **prompt_map)

            provider, model_name = (
                model.split("/") if "/" in model else ("openrouter", model)
            )
            # check if provider is in the providers map
            if provider not in PROVIDERS_MAP:
                logger.warning(
                    f"Provider {provider} is not in the providers map. Using the default provider."
                )
                provider = "openrouter"
            model_name = (
                model.replace("openrouter/", "")
                if provider == "openrouter"
                else model_name
            )

            if json_response:
                params["response_format"] = {"type": "json_object"}

            llm_provider = LLMProvider(provider, model_name, params)
            response = llm_provider.request(prompt)

            if save_logs:
                utils.save_llm_logs(model_name, prompt, str(response))

            if json_response:
                response.content = json.loads(response.content)

            logger.info(
                f"Using provider: {llm_provider.provider}"
            )  # Log the provider used

            return response

        return wrapper

    return decorator


# Example usage:
@ask()
def example_query(question: str) -> str:
    return f"Answer this question: {question}"


# To use the function:
# response = example_query("What is the capital of France?")
# print(response)  # Prints the answer
# for message in response.history():
#     print(message)  # Prints each message in the conversation history
# follow_up = response.reply("What's the population of that city?")
# print(follow_up)  # Prints the answer to the follow-up question
