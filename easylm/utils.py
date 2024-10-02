import os
import datetime


def load_prompt(path: str, **kwargs) -> str:
    """Loads a prompt file and replaces the placeholders with the given kwargs"""
    with open(path, "r") as f:
        s = f.read()
    for key, value in kwargs.items():
        s = s.replace("{{" + key + "}}", value)
    return s


def save_llm_logs(prompt_name: str, prompt: str, answer: str) -> None:
    # [ex: logs/llm/prompt_name/date/h:m:s/prompt.txt and answer.txt]
    higher_date = datetime.datetime.now().strftime("%Y_%m_%d")
    lower_date = datetime.datetime.now().strftime("%H_%M_%S")
    path = os.path.join(
        os.path.dirname(__file__), "logs", "llm", prompt_name, higher_date, lower_date
    )
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "prompt.txt"), "w", encoding="utf-8") as f:
        f.write(prompt)
    with open(os.path.join(path, "answer.txt"), "w", encoding="utf-8") as f:
        f.write(answer)
