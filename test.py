from easylm import ask, add_provider
from easylm.answer import example_query


def test_example_query():
    response = example_query("What is the capital of France?")
    assert "Paris" in response.content


def test_follow_up():
    response = example_query("What is the capital of France?")
    follow_up = response.reply("What's the population of that city?")
    follow_up_2 = follow_up.reply(
        "Sorry I forgot, what was the name of the country again?"
    )
    assert "France" in follow_up_2.content


def test_default_provider():
    @ask(model="qwen/qwen-2-7b-instruct")
    def calculate(question: str) -> str:
        return f"Calculate this: {question}"

    response = calculate("What is 2 + 2?")
    assert "4" in response.content


def test_add_provider():
    from easylm.config import PROVIDERS_MAP

    add_provider("qwen", "https://qwen.ai/api/v1/chat/completions", "QWEN_API_KEY")
    assert "qwen" in PROVIDERS_MAP
