import os
from django.shortcuts import render
from .models import Message
import requests
from dotenv import load_dotenv, find_dotenv
from rich.console import Console

console = Console()
# Load in our API keys
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
console.print(f"[dark_orange]OPENAI_API_KEY: {OPENAI_API_KEY[:14]}...[/]")


# We add in our own system message
system_message = "You are a helpful assistant for a shoe store. If a user asks a question please be as helpful as possible and use a courteous and professional manner. You are provided with the following facts to help you. Please be CONCISE but SUGGESTIVE."

# We add our own supplementary facts, this is RAG in that we are AUGMENTING our GENERATION through the use of RETRIEVAL - in this case it is a list but this wouldbe obtained from DB queries etc...
FAQ = [
    "We only sell shoes.",
    "Our opening hours are Monday to Friday from 9am to 5pm.",
    "We are located at 123 Main Street, Brighton",
    "We specialise in red shoes but have all colours",
    "Our VAT rate is 20 percent and is applicable on all sales",
    "We only accept card payments",
]

# Create the base system message
system_message += "\n" + "\n".join(FAQ)


def chat_view(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_message = get_ai_response(user_message)
        Message.objects.create(user_message=user_message, bot_message=bot_message)
    messages = Message.objects.all()
    return render(request, "chat.html", {"messages": messages})


def get_ai_response(user_input: str) -> str:
    # Set up the API endpoint and headers for LLM query
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    # Data payload - We get all existing messages from the database
    messages = get_existing_messages()
    messages.append(
        {"role": "user", "content": f"{user_input}"},
    )
    messages.append(
        {"role": "system", "content": system_message},
    )
    data = {"model": "gpt-3.5-turbo", "messages": messages, "temperature": 0.7}
    # Here is our LLM query
    response = requests.post(endpoint, headers=headers, json=data)
    response_data = response.json()
    print(f"{response_data = }")
    # We can extract the response
    ai_message = response_data["choices"][0]["message"]["content"]
    return ai_message


def get_existing_messages() -> list:
    """
    Get all messages from the database and format them for the API in terms of user and assistant messages.
    """
    formatted_messages = []

    for message in Message.objects.values("user_message", "bot_message"):
        formatted_messages.append({"role": "user", "content": message["user_message"]})
        formatted_messages.append(
            {"role": "assistant", "content": message["bot_message"]}
        )

    return formatted_messages
