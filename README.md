# EasyLM
Easily integrate language models (LLMs) into your applications with a user-friendly interface. EasyLM simplifies the process of making requests to various LLM providers, allowing you to focus on building intelligent features.

[![Downloads](https://static.pepy.tech/badge/easylm/month)](https://pepy.tech/project/easylm)

## Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
  - [Basic Interaction](#basic-interaction)
  - [Conversation History](#conversation-history)
  - [Follow-up Questions](#follow-up-questions)
  - [Using Different Models](#using-different-models)
  - [Loading Prompts from Files](#loading-prompts-from-files)
  - [Custom Hyperparameters](#custom-hyperparameters)
  - [RAG (Retrieval-Augmented Generation)](#rag-retrieval-augmented-generation)
  - [Customizing Response Format](#customizing-response-format)
- [Available Options](#available-options)
- [Providers](#providers)

## Installation
To install EasyLM, run:
```bash
pip install easylm
```

## Features
- **User-Friendly API**: Intuitive decorators for easy integration with your existing codebase.
- **Conversation Management**: Keep track of message history for dynamic interactions.
- **Provider Flexibility**: Easily switch between multiple LLM providers.
- **Customizable Requests**: Adjust parameters such as temperature and response formats.
- **Support for Long Prompts**: Load prompts from text files for complex queries with variables.

## Usage

### Basic Interaction
Define a query function using the `@ask` decorator. Here’s a simple example:
```python
from easylm import ask

@ask()
def simple_query(question: str) -> str:
    return f"What is your response to: {question}?"
```
Invoke the function to get a response:
```python
response = simple_query("What is the capital of France?")
print(response)  # Prints the answer
```

### Conversation History
Track conversation history with the `.history()` method:
```python
for message in response.history():
    print(message)  # Prints each message in the conversation history
```

### Follow-up Questions
Utilize the `.reply()` method to ask follow-up questions:
```python
follow_up = response.reply("Can you tell me more about that city?")
print(follow_up)  # Prints the answer to the follow-up question
```

### Using Different Models
Specify different models by passing the model name when decorating your function:
```python
@ask(model="meta-llama/llama-3.2-3b-instruct")
def advanced_query(question: str) -> str:
    return f"Explain this: {question}"
```

### Loading Prompts from Files
For longer prompts, load them from `.txt` files. This is useful for managing complex queries with variables and formatting. 
You can usue {{my_variable}} in your prompt file and pass the value of my_variable as a parameter to the function:
```python
@ask()
def file_query() -> str:
    return "path/to/your_prompt.txt", {"my_variable": "value"}
```
This method simplifies the management of complex prompts.

### Custom Hyperparameters
Adjust your requests with additional parameters to optimize responses:
```python
@ask(params={"temperature": 0.7, "max_tokens": 150})
def tailored_query(question: str) -> str:
    return f"Analyze this: {question}"
```

### RAG (Retrieval-Augmented Generation)
Integrate retrieval with generation for sophisticated applications:
```python
@ask(model="openrouter/retrieval_model")
def rag_query(data_source: str, user_question: str) -> str:
    retrieved_data = utils.fetch_data(data_source)  # Custom data fetching logic
    return f"Using this information: {retrieved_data}. Now answer: {user_question}"
```
This integration allows for contextualized responses based on external data.

### Customizing Response Format
Specify the `json_response` parameter to customize how the response is returned:
```python
@ask(json_response=True)
def json_format_query(question: str) -> str:
    return f"Provide data for: {question}"
```
This returns the response as a JSON object for easier parsing.

## Available Options
| Parameter          | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `model`            | Specify the LLM model to use for generating responses.       |
| `json_response`    | If true, return the response in JSON format.                |
| `save_logs`        | If true, logs the interaction for review and debugging.     |
| `params`           | Additional parameters to customize the request (e.g., temperature, max_tokens). |

## Providers
EasyLM supports multiple language model providers. By default, it uses **OpenRouter**, but you can switch to others as needed. Here’s a brief overview of supported providers:

- **OpenAI**: Leading provider of language models with a wide range of capabilities.
- **OpenRouter**: Versatile model provider with broad capabilities.

You can also add your own provider if they use a compatible API. Simply user `add_provider()` to register your provider with EasyLM.
```python
from easylm.config import PROVIDERS_MAP
add_provider("qwen", "https://qwen.ai/api/v1/chat/completions", "QWEN_API_KEY")
```

## License
[MIT](https://github.com/moehmeni/easylm/blob/master/LICENSE)

## Citation
If you use this library in your research, you can cite it as follows:
```bibtex
@misc{easylm,
  author = {Momeni, Mohammad},
  title = {EasyLM},
  year = {2024},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/moehmeni/easylm}},
}
```
